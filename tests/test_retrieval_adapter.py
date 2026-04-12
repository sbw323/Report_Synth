# tests/test_retrieval_adapter.py
"""Tests for the retrieval adapter (§14.1).

Covers:
  FR-09 : Per-section retrieval executes all source_queries
  FR-10 : Stage 05 answer text is discarded
  DR-05 : Stage 05 answer text exclusion enforced
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple
from unittest.mock import MagicMock, call

import pytest

from synthesizer.models.enums import SectionType
from synthesizer.models.report_plan import SectionNode
from synthesizer.retrieval.adapter import (
    RankedChunk,
    RetrievalResult,
    RetrieverProtocol,
    retrieve_for_section,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_section(
    section_id: str = "test_section",
    source_queries: list[str] | None = None,
) -> SectionNode:
    """Create a minimal SectionNode for testing."""
    return SectionNode(
        section_id=section_id,
        title="Test Section",
        section_type=SectionType.NARRATIVE_SYNTHESIS,
        description="A test section for retrieval testing.",
        source_queries=source_queries or ["query one"],
        depth_level=0,
    )


def _make_chunk_dict(
    chunk_id: str,
    text: str = "Chunk text.",
    score: float = 0.5,
    rrf_score: float = 0.8,
    method: str = "hybrid",
    metadata: dict | None = None,
) -> Dict[str, Any]:
    """Create a raw chunk dict as returned by Stage 05."""
    return {
        "id": chunk_id,
        "text": text,
        "metadata": metadata or {"paper_title": "Paper A", "year": "2025"},
        "score": score,
        "method": method,
        "rrf_score": rrf_score,
    }


class MockRetriever:
    """Mock HybridRetriever for testing (§14.1 contract)."""

    def __init__(self, responses: Dict[str, Tuple[str, List[Dict[str, Any]]]]):
        """
        Parameters
        ----------
        responses : dict
            Maps query_text → (answer_text, ranked_chunks) tuples.
        """
        self._responses = responses
        self.calls: List[str] = []

    def query(self, query_text: str) -> Tuple[str, List[Dict[str, Any]]]:
        self.calls.append(query_text)
        if query_text in self._responses:
            return self._responses[query_text]
        return ("Default answer (should be discarded).", [])


# ---------------------------------------------------------------------------
# FR-09: Both queries executed, chunks aggregated
# ---------------------------------------------------------------------------


class TestRetrievalExecutesAllSourceQueries:
    """FR-09 acceptance: section with 2 source_queries → both executed,
    chunks aggregated."""

    def test_two_queries_both_executed(self) -> None:
        """FR-09: Both source queries are dispatched to the retriever."""
        section = _make_section(
            source_queries=["query about methods", "query about results"]
        )

        retriever = MockRetriever(
            {
                "query about methods": (
                    "Answer about methods (discarded).",
                    [_make_chunk_dict("chunk_m1"), _make_chunk_dict("chunk_m2")],
                ),
                "query about results": (