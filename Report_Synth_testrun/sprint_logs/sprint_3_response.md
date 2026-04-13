Looking at the sprint requirements, I need to implement:
1. `SectionOutput` models (§10.8-10.9)
2. Retrieval adapter wrapping Stage 05 (§14.1, FR-09, FR-10)
3. Planning context loader for Stage 06 (DR-06)
4. Context channel packaging (§13)
5. Prompt assembly (§9.2.1, FR-11, FR-12, FR-13)
6. Comprehensive tests

Let me trace through the spec carefully and implement each artifact.

### `synthesizer/models/section_output.py`
```python
# synthesizer/models/section_output.py
"""Section output Pydantic models (§10.8, §10.9).

Base SectionOutput and four per-type subclasses:
  - NarrativeSynthesisOutput
  - EvidenceTableOutput
  - CrossReferenceOutput
  - MethodologyDescriptionOutput

Supports: FR-13, FR-14, FR-26.
"""

from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.enums import SectionType


class SectionOutput(BaseModel):
    """Base model for generated section content (§10.8).

    Extended by per-type models (§10.9).
    Supports: FR-13, FR-14, FR-26.
    """

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(
        ...,
        description="Must match the SectionNode.section_id.",
    )
    content_markdown: str = Field(
        ...,
        min_length=1,
        description="Generated Markdown content.",
    )
    word_count: int = Field(
        ...,
        ge=1,
        description="Word count of content_markdown.",
    )
    heading_level: int = Field(
        ...,
        ge=1,
        le=6,
        description="Markdown heading level (1-6). Derived from depth_level.",
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Generation metadata (model, timestamp, etc.).",
    )


class NarrativeSynthesisOutput(SectionOutput):
    """Output for narrative_synthesis sections (§10.9).

    Extends base with synthesis-specific fields.
    Supports: FR-13.
    """

    themes_addressed: List[str] = Field(
        default_factory=list,
        description="Thematic tags covered in this section.",
    )
    cross_references: List[str] = Field(
        default_factory=list,
        description="section_ids referenced in the text.",
    )


class EvidenceTableOutput(SectionOutput):
    """Output for evidence_table sections (§10.9).

    Extends base with tabular structure.
    Supports: FR-13.
    """

    column_definitions: List[str] = Field(
        ...,
        min_length=1,
        description="Column headers for the evidence table.",
    )
    rows: List[Dict[str, str]] = Field(
        ...,
        description="Table rows as column→value mappings.",
    )


class CrossReferenceOutput(SectionOutput):
    """Output for cross_reference sections (§10.9).

    Extends base with reference mapping.
    Supports: FR-13.
    """

    referenced_sections: List[str] = Field(
        ...,
        min_length=1,
        description="section_ids this section cross-references.",
    )
    comparison_dimensions: List[str] = Field(
        default_factory=list,
        description="Dimensions along which sections are compared.",
    )


class MethodologyDescriptionOutput(SectionOutput):
    """Output for methodology_description sections (§10.9).

    Extends base with methodology fields.
    Supports: FR-13.
    """

    methodologies_described: List[str] = Field(
        default_factory=list,
        description="Named methodologies covered.",
    )
    equations_referenced: List[str] = Field(
        default_factory=list,
        description="LaTeX equation strings referenced.",
    )


# ---------------------------------------------------------------------------
# FR-13  Section-type dispatch registry
# ---------------------------------------------------------------------------

SECTION_TYPE_TO_OUTPUT_MODEL: Dict[SectionType, type[SectionOutput]] = {
    SectionType.NARRATIVE_SYNTHESIS: NarrativeSynthesisOutput,
    SectionType.EVIDENCE_TABLE: EvidenceTableOutput,
    SectionType.CROSS_REFERENCE: CrossReferenceOutput,
    SectionType.METHODOLOGY_DESCRIPTION: MethodologyDescriptionOutput,
}
"""Maps SectionType enum → corresponding SectionOutput subclass (FR-13)."""


def get_output_model(section_type: SectionType) -> type[SectionOutput]:
    """Return the SectionOutput subclass for a given section type (FR-13).

    Parameters
    ----------
    section_type : SectionType
        The section type from the report plan.

    Returns
    -------
    type[SectionOutput]
        The Pydantic model class for the section type's output.

    Raises
    ------
    ValueError
        If the section type has no registered output model.
    """
    model = SECTION_TYPE_TO_OUTPUT_MODEL.get(section_type)
    if model is None:
        raise ValueError(
            f"No output model registered for section type '{section_type.value}'. "
            f"Known types: {sorted(t.value for t in SECTION_TYPE_TO_OUTPUT_MODEL)}"
        )
    return model


def get_output_schema_json(section_type: SectionType) -> str:
    """Return a JSON-schema string for the output model of a section type.

    Used in prompt assembly to instruct the LLM on the expected output
    format (FR-13, §9.2.1).

    Parameters
    ----------
    section_type : SectionType
        The section type.

    Returns
    -------
    str
        Pretty-printed JSON schema string.
    """
    import json

    model = get_output_model(section_type)
    schema = model.model_json_schema()
    return json.dumps(schema, indent=2)
```

### `synthesizer/retrieval/__init__.py`
```python
# synthesizer/retrieval/__init__.py
"""Retrieval integration sub-package (§14).

Provides adapters for Stage 05 HybridRetriever and Stage 06 PaperSummary
loader.
"""
```

### `synthesizer/retrieval/adapter.py`
```python
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
```

### `synthesizer/retrieval/planning_context.py`
```python
# synthesizer/retrieval/planning_context.py
"""Stage 06 PaperSummary loader for planning context only (§14.1, DR-06).

Loads PaperSummary objects from Stage 06's ``load_all_summaries()``
function. These summaries are used exclusively for planning purposes
(e.g., retrieval query construction) and are **never** injected into
generation prompts as source evidence.

DR-06 (decided): Stage 06 summaries are used for planning only, not as
generation evidence. PaperSummary objects inform retrieval query
construction but are never injected into generation prompts as source
material. Summaries are abstractions; generation must be grounded in
primary chunk evidence from the vector store.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lightweight representation of PaperSummary data
# ---------------------------------------------------------------------------

@dataclass
class PaperSummaryInfo:
    """Planning-only representation of a Stage 06 PaperSummary.

    This is a read-only data class that captures the fields from
    Stage 06's PaperSummary relevant to planning. It is explicitly
    NOT a prompt context channel — see DR-06.

    Attributes
    ----------
    paper_id : str
        Unique paper identifier.
    title : str
        Paper title.
    authors : str
        Author string.
    year : str
        Publication year.
    objective : str
        Paper's stated objective.
    methodology : str
        Summary of methodology.
    key_findings : str
        Key findings summary.
    limitations : str
        Noted limitations.
    relevance_tags : list of str
        Tags indicating relevance domains.
    """

    paper_id: str = ""
    title: str = ""
    authors: str = ""
    year: str = ""
    objective: str = ""
    methodology: str = ""
    key_findings: str = ""
    limitations: str = ""
    relevance_tags: List[str] = field(default_factory=list)


def _convert_paper_summary(raw: Any) -> PaperSummaryInfo:
    """Convert a Stage 06 PaperSummary object to our planning-only dataclass.

    Handles both attribute-based objects and dict-like objects.
    """
    def _get(obj: Any, attr: str, default: Any = "") -> Any:
        if hasattr(obj, attr):
            return getattr(obj, attr)
        if isinstance(obj, dict):
            return obj.get(attr, default)
        return default

    return PaperSummaryInfo(
        paper_id=str(_get(raw, "paper_id", "")),
        title=str(_get(raw, "title", "")),
        authors=str(_get(raw, "authors", "")),
        year=str(_get(raw, "year", "")),
        objective=str(_get(raw, "objective", "")),
        methodology=str(_get(raw, "methodology", "")),
        key_findings=str(_get(raw, "key_findings", "")),
        limitations=str(_get(raw, "limitations", "")),
        relevance_tags=list(_get(raw, "relevance_tags", [])),
    )


def load_planning_summaries() -> List[PaperSummaryInfo]:
    """Load PaperSummary data from Stage 06 for planning use only (DR-06).

    Calls ``load_all_summaries()`` from ``06_review.py`` and converts
    the results to ``PaperSummaryInfo`` dataclass instances.

    These summaries are used for planning (e.g., query construction)
    and must NEVER be injected into generation prompts.

    Returns
    -------
    list of PaperSummaryInfo
        Planning-only summary representations. Empty list if Stage 06
        is not importable.
    """
    try:
        from importlib import import_module
        mod = import_module("06_review")
        load_fn = getattr(mod, "load_all_summaries", None)
        if load_fn is None:
            logger.warning(
                "06_review module does not expose load_all_summaries(). "
                "No planning summaries loaded."
            )
            return []
        raw_summaries = load_fn()
        result = [_convert_paper_summary(s) for s in raw_summaries]
        logger.info("Loaded %d planning summaries from Stage 06.", len(result))
        return result
    except (ImportError, ModuleNotFoundError):
        logger.warning(
            "Stage 06 (06_review) is not importable. "
            "No planning summaries loaded."
        )
        return []
    except Exception:
        logger.exception("Failed to load planning summaries from Stage 06.")
        return []


def get_summary_by_paper_id(
    summaries: List[PaperSummaryInfo],
    paper_id: str,
) -> Optional[PaperSummaryInfo]:
    """Look up a planning summary by paper_id.

    Parameters
    ----------
    summaries : list of PaperSummaryInfo
        Loaded planning summaries.
    paper_id : str
        The paper_id to search for.

    Returns
    -------
    PaperSummaryInfo or None
    """
    for s in summaries:
        if s.paper_id == paper_id:
            return s
    return None
```

### `synthesizer/prompt/__init__.py`
```python
# synthesizer/prompt/__init__.py
"""Prompt assembly sub-package (§9.2.1, §13).

Provides context-channel packaging and full generation prompt assembly.
"""
```

### `synthesizer/prompt/context_channels.py`
```python
# synthesizer/prompt/context_channels.py
"""Context channel packaging for generation prompts (§13).

Three structured context channels carry information into generation prompts:
  1. Claim tables (§13.1) — from upstream content dependencies
  2. Summary abstracts (§13.2) — from upstream thematic dependencies
  3. Evidence pointers (§13.3) — from Stage 05 retrieval

Raw upstream prose (content_markdown) is explicitly excluded (DR-03, FR-12).
Stage 05 answer text is explicitly excluded (DR-05, FR-10).
Stage 06 summaries are explicitly excluded (DR-06).
"""

from __future__ import annotations

from typing import Dict, List, Optional

from synthesizer.models.claims import ClaimTable
from synthesizer.retrieval.adapter import RankedChunk


# ---------------------------------------------------------------------------
# §13.1  Claim table packaging (content dependencies)
# ---------------------------------------------------------------------------

def package_claim_tables(
    upstream_claim_tables: Dict[str, ClaimTable],
) -> str:
    """Serialize upstream claim tables for insertion into a generation prompt.

    Each claim table comes from a finalized upstream section that the
    current section has a content dependency on (§13.1). The downstream
    section must engage with the claims contained therein.

    Parameters
    ----------
    upstream_claim_tables : dict
        Maps upstream section_id → ClaimTable. Only tables from content
        dependencies should be passed here.

    Returns
    -------
    str
        Formatted text block for prompt insertion. Empty string if no
        claim tables are provided.

    Notes
    -----
    DR-03: Raw upstream prose is excluded. Only structured claim data
    is serialized — never the upstream section's content_markdown.
    """
    if not upstream_claim_tables:
        return ""

    parts: List[str] = []
    parts.append("=== UPSTREAM CLAIM TABLES (Content Dependencies) ===")
    parts.append(
        "The following claims are from upstream sections that this section "
        "depends on. You must engage with these claims in your synthesis."
    )

    for section_id in sorted(upstream_claim_tables):
        ct = upstream_claim_tables[section_id]
        parts.append(f"\n--- Claims from section: {section_id} ---")

        if ct.partial:
            parts.append(
                "[WARNING: This claim table is partial — extraction was "
                "incomplete. Some claims may be missing.]"
            )

        if not ct.claims:
            parts.append("(No claims extracted.)")
            continue

        for claim in ct.claims:
            parts.append(
                f"  [{claim.claim_id}] {claim.claim_text}\n"
                f"    Confidence: {claim.confidence_tag.value}\n"
                f"    Source chunks: {', '.join(claim.source_chunk_ids)}"
            )

    parts.append("\n=== END UPSTREAM CLAIM TABLES ===")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# §13.2  Summary abstract packaging (thematic dependencies)
# ---------------------------------------------------------------------------

def package_summary_abstracts(
    upstream_abstracts: Dict[str, str],
) -> str:
    """Serialize upstream summary abstracts for insertion into a generation prompt.

    Summary abstracts are 2-3 sentence summaries generated by the
    Summary Abstractifier (§9.2.4) from upstream sections. They provide
    high-level thematic context for sections with thematic (or content)
    dependencies (§13.2).

    Parameters
    ----------
    upstream_abstracts : dict
        Maps upstream section_id → summary abstract string. Only
        abstracts from thematic and content dependencies should be
        passed here.

    Returns
    -------
    str
        Formatted text block for prompt insertion. Empty string if no
        abstracts are provided.

    Notes
    -----
    DR-03: These are summary abstracts — NOT raw upstream prose.
    The full content_markdown of upstream sections is never included.
    """
    if not upstream_abstracts:
        return ""

    parts: List[str] = []
    parts.append("=== UPSTREAM SUMMARY ABSTRACTS (Thematic Context) ===")
    parts.append(
        "The following summaries provide thematic context from related "
        "sections. Use them to maintain narrative coherence."
    )

    for section_id in sorted(upstream_abstracts):
        abstract = upstream_abstracts[section_id]
        parts.append(f"\n--- Summary of section: {section_id} ---")
        parts.append(abstract.strip())

    parts.append("\n=== END UPSTREAM SUMMARY ABSTRACTS ===")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# §13.3  Evidence pointer packaging (retrieval chunks)
# ---------------------------------------------------------------------------

def package_evidence_chunks(
    chunks: List[RankedChunk],
) -> str:
    """Serialize ranked retrieval chunks for insertion into a generation prompt.

    Evidence pointers are the primary evidence base for generation (§13.3).
    Each chunk includes its ID, text, metadata, and retrieval score.

    Parameters
    ----------
    chunks : list of RankedChunk
        Ranked chunks from Stage 05 retrieval, already aggregated and
        deduplicated (FR-09). Answer text has already been discarded
        (FR-10, DR-05).

    Returns
    -------
    str
        Formatted text block for prompt insertion. Empty string if no
        chunks are provided.

    Notes
    -----
    FR-10, DR-05: Only chunk data is included. Stage 05 answer text
    has been discarded at the retrieval adapter layer and does not
    appear anywhere in the output of this function.
    """
    if not chunks:
        return ""

    parts: List[str] = []
    parts.append("=== EVIDENCE CHUNKS (Retrieved from Source Documents) ===")
    parts.append(
        "The following evidence chunks are retrieved from the source "
        "documents. Ground your synthesis in this evidence. Cite "
        "chunks by their IDs."
    )

    for i, chunk in enumerate(chunks, 1):
        meta_parts: List[str] = []
        if chunk.metadata.get("paper_title"):
            meta_parts.append(f"Paper: {chunk.metadata['paper_title']}")
        if chunk.metadata.get("authors"):
            meta_parts.append(f"Authors: {chunk.metadata['authors']}")
        if chunk.metadata.get("year"):
            meta_parts.append(f"Year: {chunk.metadata['year']}")
        if chunk.metadata.get("section"):
            meta_parts.append(f"Section: {chunk.metadata['section']}")

        meta_str = " | ".join(meta_parts) if meta_parts else "No metadata"

        parts.append(
            f"\n--- Chunk {i}: {chunk.id} "
            f"(score: {chunk.score:.4f}, rrf: {chunk.rrf_score:.4f}) ---"
        )
        parts.append(f"Metadata: {meta_str}")
        parts.append(f"Text:\n{chunk.text}")

    parts.append("\n=== END EVIDENCE CHUNKS ===")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Formatting helpers for style constraints
# ---------------------------------------------------------------------------

def package_style_constraints(
    tone_register: str,
    citation_pattern: str,
    forbidden_phrases: List[str],
    min_words: Optional[int] = None,
    max_words: Optional[int] = None,
    heading_format: Optional[str] = None,
    equation_inline: str = "$",
    equation_display: str = "$$",
    per_type_overrides: Optional[Dict[str, object]] = None,
) -> str:
    """Format style sheet constraints for prompt insertion (§9.2.1).

    Parameters
    ----------
    tone_register : str
        Required tone (e.g., "formal_academic").
    citation_pattern : str
        Regex pattern for valid citations.
    forbidden_phrases : list of str
        Phrases that must not appear.
    min_words : int, optional
        Minimum word count for this section's depth level.
    max_words : int, optional
        Maximum word count for this section's depth level.
    heading_format : str, optional
        Expected heading format (e.g., "##").
    equation_inline : str
        Inline equation delimiter.
    equation_display : str
        Display equation delimiter.
    per_type_overrides : dict, optional
        Type-specific overrides from the style sheet.

    Returns
    -------
    str
        Formatted style constraint block.
    """
    parts: List[str] = []
    parts.append("=== STYLE CONSTRAINTS ===")
    parts.append(f"Tone register: {tone_register}")
    parts.append(f"Citation format (regex): {citation_pattern}")

    if min_words is not None and max_words is not None:
        parts.append(f"Word count range: {min_words}–{max_words} words")
    elif max_words is not None:
        parts.append(f"Maximum word count: {max_words} words")

    if heading_format:
        parts.append(f"Heading format: {heading_format}")

    parts.append(f"Equation delimiters: inline={equation_inline}, display={equation_display}")

    if forbidden_phrases:
        parts.append(f"Forbidden phrases (do NOT use): {', '.join(repr(p) for p in forbidden_phrases)}")

    if per_type_overrides:
        parts.append(f"Type-specific overrides: {per_type_overrides}")

    parts.append("=== END STYLE CONSTRAINTS ===")
    return "\n".join(parts)


def package_retry_errors(
    error_descriptions: List[str],
    layer_name: str,
) -> str:
    """Format validation errors for a retry prompt (FR-15, FR-17).

    Parameters
    ----------
    error_descriptions : list of str
        Error/violation descriptions from the failing validation layer.
    layer_name : str
        Name of the validation layer that failed.

    Returns
    -------
    str
        Formatted error feedback block. Empty string if no errors.
    """
    if not error_descriptions:
        return ""

    parts: List[str] = []
    parts.append(f"=== VALIDATION ERRORS ({layer_name}) ===")
    parts.append(
        "Your previous output failed validation. Please fix the "
        "following issues in your regenerated output:"
    )
    for i, desc in enumerate(error_descriptions, 1):
        parts.append(f"  {i}. {desc}")
    parts.append("=== END VALIDATION ERRORS ===")
    return "\n".join(parts)
```

### `synthesizer/prompt/assembly.py`
```python
# synthesizer/prompt/assembly.py
"""Full generation prompt assembly per §9.2.1.

Composes system prompt + user message for the Generator role, including
all five context channels:
  1. Section description and type (from ReportPlan)
  2. Retrieved chunks (from Stage 05 via retrieval adapter)
  3. Upstream claim tables (for content dependencies, §13.1)
  4. Upstream summary abstracts (for thematic dependencies, §13.2)
  5. Style sheet constraints (from StyleSheet)

Plus a retry-error feedback slot for re-generation attempts.

Enforced exclusions:
  - FR-10 / DR-05: No Stage 05 answer text
  - FR-12 / DR-03: No raw upstream content_markdown
  - DR-06: No Stage 06 PaperSummary data in generation prompts

DR-18 remains open: input token budgets per prompt role are not enforced
here. Prompt assembly produces the complete prompt; token budget enforcement
is deferred to the orchestrator/caller.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.claims import ClaimTable
from synthesizer.models.enums import SectionType
from synthesizer.models.report_plan import SectionNode
from synthesizer.models.section_output import (
    get_output_model,
    get_output_schema_json,
)
from synthesizer.models.style_sheet import StyleSheet
from synthesizer.prompt.context_channels import (
    package_claim_tables,
    package_evidence_chunks,
    package_retry_errors,
    package_style_constraints,
    package_summary_abstracts,
)
from synthesizer.retrieval.adapter import RankedChunk


# ---------------------------------------------------------------------------
# Prompt data container
# ---------------------------------------------------------------------------

class GenerationPrompt(BaseModel):
    """Assembled generation prompt ready for LLM invocation (§9.2.1).

    Contains the system prompt, user message, and metadata needed
    by the orchestrator to dispatch the LLM call.
    """

    model_config = ConfigDict(extra="forbid")

    system_prompt: str = Field(
        ...,
        description="System-level instructions for the Generator.",
    )
    user_message: str = Field(
        ...,
        description="User-level message with all context channels.",
    )
    section_id: str = Field(
        ...,
        description="The section being generated.",
    )
    section_type: SectionType = Field(
        ...,
        description="Type of the section being generated.",
    )
    expected_output_model_name: str = Field(
        ...,
        description="Name of the expected SectionOutput subclass (FR-13).",
    )
    max_output_tokens: int = Field(
        default=4000,
        description="Output token cap for Generator (§9.2.1, partially open DR-18).",
    )


# ---------------------------------------------------------------------------
# System prompt construction
# ---------------------------------------------------------------------------

def _build_system_prompt(
    section_type: SectionType,
    style: StyleSheet,
    depth_level: int,
) -> str:
    """Construct the Generator system prompt (§9.2.1).

    System prompt content per spec:
      - Role as scientific literature review writer
      - Output format instructions referencing the target SectionOutput subclass
      - Style sheet constraints (tone, citation format, word limits, forbidden phrases)
      - Equation delimiter configuration
    """
    output_model = get_output_model(section_type)
    output_schema = get_output_schema_json(section_type)

    level_constraint = style.per_level_constraints.get(depth_level)
    word_constraint_text = ""
    if level_constraint:
        word_constraint_text = (
            f"Word count: {level_constraint.min_words}–{level_constraint.max_words} words.\n"
            f"Heading format: {level_constraint.heading_format}\n"
        )

    type_override_text = ""
    type_overrides = style.per_type_overrides.get(section_type)
    if type_overrides:
        type_override_text = (
            f"\nType-specific overrides for '{section_type.value}':\n"
            f"{type_overrides}\n"
        )

    forbidden_text = ""
    if style.forbidden_phrases:
        phrases = ", ".join(repr(p) for p in style.forbidden_phrases)
        forbidden_text = f"\nForbidden phrases (NEVER use): {phrases}\n"

    return (
        "You are a scientific literature review writer. Your task is to "
        "generate a section of a structured literature review based on "
        "evidence chunks retrieved from source documents and structured "
        "context from upstream sections.\n\n"
        "OUTPUT FORMAT:\n"
        f"You MUST produce valid JSON conforming to the {output_model.__name__} schema.\n"
        f"Schema:\n{output_schema}\n\n"
        "STYLE REQUIREMENTS:\n"
        f"Tone register: {style.tone_register}\n"
        f"Citation format (regex pattern): {style.citation_pattern}\n"
        f"{word_constraint_text}"
        f"Equation delimiters: inline={style.equation_delimiters.inline}, "
        f"display={style.equation_delimiters.display}\n"
        f"{forbidden_text}"
        f"{type_override_text}"
        "CRITICAL RULES:\n"
        "- Ground ALL claims in the provided evidence chunks.\n"
        "- Use the citation format specified above.\n"
        "- Stay within the word count limits.\n"
        "- Engage with upstream claim tables when provided.\n"
        "- Do NOT fabricate references or evidence.\n"
        "- Produce valid JSON only — no markdown fences around the JSON.\n"
    )


# ---------------------------------------------------------------------------
# User message construction
# ---------------------------------------------------------------------------

def _build_user_message(
    section: SectionNode,
    evidence_text: str,
    claim_tables_text: str,
    summary_abstracts_text: str,
    style_constraints_text: str,
    retry_errors_text: str,
) -> str:
    """Construct the Generator user message with all context channels (§9.2.1).

    User message composition per spec:
      1. Section description and type from the report plan
      2. Retrieved chunks from Stage 05
      3. Upstream claim tables for content dependencies
      4. Upstream summary abstracts for thematic dependencies
      5. Style sheet constraints relevant to this section's type and depth level
      6. On retry: validation error list from the failing layer
    """
    parts: List[str] = []

    # 1. Section description and type
    parts.append("=== SECTION TO GENERATE ===")
    parts.append(f"Section ID: {section.section_id}")
    parts.append(f"Section title: {section.title}")
    parts.append(f"Section type: {section.section_type.value}")
    parts.append(f"Depth level: {section.depth_level}")
    parts.append(f"Description: {section.description}")
    parts.append("=== END SECTION DESCRIPTION ===\n")

    # 2. Retrieved chunks (evidence pointers — §13.3)
    if evidence_text:
        parts.append(evidence_text)
        parts.append("")

    # 3. Upstream claim tables (§13.1)
    if claim_tables_text:
        parts.append(claim_tables_text)
        parts.append("")

    # 4. Upstream summary abstracts (§13.2)
    if summary_abstracts_text:
        parts.append(summary_abstracts_text)
        parts.append("")

    # 5. Style constraints
    if style_constraints_text:
        parts.append(style_constraints_text)
        parts.append("")

    # 6. Retry errors (if re-generating after validation failure)
    if retry_errors_text:
        parts.append(retry_errors_text)
        parts.append("")

    parts.append(
        "Please generate the section content as valid JSON conforming to "
        "the schema specified in the system instructions."
    )

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# FR-11  Full prompt assembly
# ---------------------------------------------------------------------------

def assemble_generation_prompt(
    section: SectionNode,
    style: StyleSheet,
    retrieved_chunks: List[RankedChunk],
    upstream_claim_tables: Optional[Dict[str, ClaimTable]] = None,
    upstream_summary_abstracts: Optional[Dict[str, str]] = None,
    retry_errors: Optional[List[str]] = None,
    retry_layer: Optional[str] = None,
) -> GenerationPrompt:
    """Assemble a complete generation prompt for a section (FR-11, §9.2.1).

    Composes the system prompt and user message with all five context
    channels from §9.2.1, plus optional retry error feedback.

    Parameters
    ----------
    section : SectionNode
        The section to generate. Provides description, type, depth_level,
        and section_id.
    style : StyleSheet
        The style sheet with formatting and tone constraints.
    retrieved_chunks : list of RankedChunk
        Evidence chunks from Stage 05 retrieval (§13.3). Answer text
        has already been discarded by the retrieval adapter (FR-10).
    upstream_claim_tables : dict, optional
        Maps upstream section_id → ClaimTable for content dependencies
        (§13.1). None or empty dict if no content deps.
    upstream_summary_abstracts : dict, optional
        Maps upstream section_id → summary abstract string for thematic
        dependencies (§13.2). None or empty dict if no thematic deps.
    retry_errors : list of str, optional
        Validation error descriptions from a previous attempt (FR-15, FR-17).
    retry_layer : str, optional
        Name of the validation layer that failed (for error context).

    Returns
    -------
    GenerationPrompt
        Fully assembled prompt ready for LLM dispatch.

    Raises
    ------
    ValueError
        If the section type has no registered output model.

    Enforced exclusions
    -------------------
    FR-10 / DR-05 : answer_text is never present — it was discarded
        at the retrieval adapter layer. This function receives only
        RankedChunk objects, not raw Stage 05 output.
    FR-12 / DR-03 : raw upstream content_markdown is never included.
        Upstream context is provided exclusively via claim tables
        (structured ClaimTable objects) and summary abstracts
        (2-3 sentence strings), never as raw prose.
    DR-06 : Stage 06 PaperSummary data is never included in generation
        prompts. It is consumed by the planning context loader only.
    """
    claim_tables = upstream_claim_tables or {}
    abstracts = upstream_summary_abstracts or {}
    errors = retry_errors or []
    layer = retry_layer or ""

    # Resolve output model for this section type (FR-13)
    output_model = get_output_model(section.section_type)

    # Get level constraints for style packaging
    level_constraint = style.per_level_constraints.get(section.depth_level)
    type_overrides = style.per_type_overrides.get(section.section_type)

    # Package all context channels
    evidence_text = package_evidence_chunks(retrieved_chunks)
    claim_tables_text = package_claim_tables(claim_tables)
    summary_abstracts_text = package_summary_abstracts(abstracts)
    style_constraints_text = package_style_constraints(
        tone_register=style.tone_register,
        citation_pattern=style.citation_pattern,
        forbidden_phrases=style.forbidden_phrases,
        min_words=level_constraint.min_words if level_constraint else None,
        max_words=level_constraint.max_words if level_constraint else None,
        heading_format=level_constraint.heading_format if level_constraint else None,
        equation_inline=style.equation_delimiters.inline,
        equation_display=style.equation_delimiters.display,
        per_type_overrides=type_overrides,
    )
    retry_errors_text = package_retry_errors(errors, layer) if errors else ""

    # Build system prompt
    system_prompt = _build_system_prompt(
        section_type=section.section_type,
        style=style,
        depth_level=section.depth_level,
    )

    # Build user message
    user_message = _build_user_message(
        section=section,
        evidence_text=evidence_text,
        claim_tables_text=claim_tables_text,
        summary_abstracts_text=summary_abstracts_text,
        style_constraints_text=style_constraints_text,
        retry_errors_text=retry_errors_text,
    )

    return GenerationPrompt(
        system_prompt=system_prompt,
        user_message=user_message,
        section_id=section.section_id,
        section_type=section.section_type,
        expected_output_model_name=output_model.__name__,
        max_output_tokens=4000,  # §9.2.1 output token cap
    )
```

### `synthesizer/models/__init__.py`
```python
# synthesizer/models/__init__.py
"""Pydantic models and enumerations for the Report Synthesizer (§10)."""

from synthesizer.models.enums import (
    ConfidenceTag,
    DependencyKind,
    SectionLifecycleState,
    SectionType,
    ValidationLayer,
    ViolationSeverity,
)
from synthesizer.models.report_plan import (
    DependencyEdge,
    ReportPlan,
    SectionNode,
)
from synthesizer.models.section_output import (
    CrossReferenceOutput,
    EvidenceTableOutput,
    MethodologyDescriptionOutput,
    NarrativeSynthesisOutput,
    SectionOutput,
    get_output_model,
)
from synthesizer.models.style_sheet import (
    EquationDelimiters,
    LevelConstraint,
    StyleSheet,
)

__all__ = [
    "ConfidenceTag",
    "CrossReferenceOutput",
    "DependencyKind",
    "DependencyEdge",
    "EquationDelimiters",
    "EvidenceTableOutput",
    "LevelConstraint",
    "MethodologyDescriptionOutput",
    "NarrativeSynthesisOutput",
    "ReportPlan",
    "SectionLifecycleState",
    "SectionNode",
    "SectionOutput",
    "SectionType",
    "StyleSheet",
    "ValidationLayer",
    "ViolationSeverity",
    "get_output_model",
]
```

### `tests/__init__.py`
```python
# tests/__init__.py
"""Test package for the Report Synthesizer Agent."""
```

### `tests/test_retrieval_adapter.py`
```python
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