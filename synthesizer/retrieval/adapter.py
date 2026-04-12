# synthesizer/retrieval/adapter.py
"""Thin wrapper around Stage 05 HybridRetriever (§14.1).

Provides per-section retrieval that:
  - Executes all source_queries for a section (FR-09)
  - Aggregates ranked chunks across queries with deduplication
  - Discards answer_text from Stage 05 (FR-10, DR-05)

Integration strategy (§14.2): wraps existing pipeline code as library
import. Does not refactor Stage 05.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Protocol, Tuple, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.report_plan import SectionNode

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Protocol for Stage 05 HybridRetriever (§14.1)
# ---------------------------------------------------------------------------

@runtime_checkable
class RetrieverProtocol(Protocol):
    """Protocol matching the Stage 05 HybridRetriever.query() interface.

    Per §14.1:
      Input:  query_text: str
      Output: Tuple[str, List[Dict]]
              (answer_text, ranked_chunks)

    Each chunk dict contains: id, text, metadata, score, method, rrf_score.
    """

    def query(self, query_text: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Execute a retrieval query.

        Returns
        -------
        tuple of (answer_text, ranked_chunks)
            answer_text is discarded by the adapter (DR-05).
        """
        ...


# ---------------------------------------------------------------------------
# Typed chunk model (§13.3, §14.1)
# ---------------------------------------------------------------------------

class RankedChunk(BaseModel):
    """A single ranked chunk from Stage 05 retrieval (§13.3, §14.1).

    Fields match the chunk dict contract from §14.1:
      id, text, metadata, score, method, rrf_score.

    Extra fields from the chunk dict are preserved in case Stage 05
    adds supplementary data.
    """

    model_config = ConfigDict(extra="allow")

    id: str = Field(
        ...,
        description="Chunk identifier (e.g., 'paper_a_intro_0_0').",
    )
    text: str = Field(
        ...,
        description="Full chunk text.",
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Chunk metadata (paper title, authors, year, section).",
    )
    score: float = Field(
        default=0.0,
        description="Primary retrieval score.",
    )
    method: str = Field(
        default="",
        description="Retrieval method that produced this chunk.",
    )
    rrf_score: float = Field(
        default=0.0,
        description="Reciprocal Rank Fusion score.",
    )


# ---------------------------------------------------------------------------
# Aggregated retrieval result
# ---------------------------------------------------------------------------

class RetrievalResult(BaseModel):
    """Aggregated retrieval result for a section (FR-09).

    Contains only ranked chunks — answer text has been discarded
    (FR-10, DR-05).
    """

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(
        ...,
        description="The section these chunks were retrieved for.",
    )
    chunks: List[RankedChunk] = Field(
        default_factory=list,
        description="Aggregated ranked chunks from all source queries.",
    )
    queries_executed: List[str] = Field(
        default_factory=list,
        description="Source queries that were executed.",
    )


# ---------------------------------------------------------------------------
# FR-09, FR-10  Per-section retrieval
# ---------------------------------------------------------------------------

def retrieve_for_section(
    section: SectionNode,
    retriever: RetrieverProtocol,
) -> RetrievalResult:
    """Execute all source_queries for a section and return aggregated chunks.

    For each query in ``section.source_queries``, calls
    ``retriever.query()`` and collects the ranked chunk list. The
    answer_text returned by Stage 05 is **discarded** (FR-10, DR-05).

    Chunks are deduplicated by ``id``; when the same chunk appears in
    results from multiple queries, the instance with the higher
    ``rrf_score`` is kept.

    Parameters
    ----------
    section : SectionNode
        The section whose source_queries drive retrieval.
    retriever : RetrieverProtocol
        Stage 05 HybridRetriever (or compatible mock).

    Returns
    -------
    RetrievalResult
        Aggregated chunks with answer text excluded.

    Supports
    --------
    FR-09 : All source_queries executed; ranked chunks aggregated.
    FR-10 : answer_text discarded; only ranked_chunks passed forward.
    DR-05 : Stage 05 answer text exclusion enforced.
    """
    best_chunks: Dict[str, RankedChunk] = {}
    queries_executed: List[str] = []

    for query_text in section.source_queries:
        logger.debug(
            "Executing retrieval query for section '%s': %s",
            section.section_id,
            query_text[:80],
        )

        # §14.1: query() returns (answer_text, ranked_chunks)
        answer_text, raw_chunks = retriever.query(query_text)

        # FR-10, DR-05: Discard answer_text entirely.
        # We do NOT store, log, or propagate it.
        del answer_text

        queries_executed.append(query_text)

        for chunk_dict in raw_chunks:
            chunk = RankedChunk.model_validate(chunk_dict)
            existing = best_chunks.get(chunk.id)
            if existing is None or chunk.rrf_score > existing.rrf_score:
                best_chunks[chunk.id] = chunk

    # Preserve a stable ordering by rrf_score descending, then id ascending
    sorted_chunks = sorted(
        best_chunks.values(),
        key=lambda c: (-c.rrf_score, c.id),
    )

    logger.info(
        "Retrieved %d unique chunks for section '%s' from %d queries.",
        len(sorted_chunks),
        section.section_id,
        len(queries_executed),
    )

    return RetrievalResult(
        section_id=section.section_id,
        chunks=sorted_chunks,
        queries_executed=queries_executed,
    )


# ---------------------------------------------------------------------------
# Helper: import the real HybridRetriever (optional)
# ---------------------------------------------------------------------------

def load_hybrid_retriever() -> Optional[Any]:
    """Attempt to import the Stage 05 HybridRetriever.

    Returns the HybridRetriever class if available, or None if the
    pipeline module is not importable. Callers should handle the None
    case (e.g., in test environments).

    Returns
    -------
    HybridRetriever class or None
    """
    try:
        from importlib import import_module
        mod = import_module("05_query")
        return getattr(mod, "HybridRetriever", None)
    except (ImportError, ModuleNotFoundError):
        logger.warning(
            "Stage 05 (05_query) is not importable. "
            "HybridRetriever will not be available."
        )
        return None