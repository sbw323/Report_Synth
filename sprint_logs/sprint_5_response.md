Looking at the sprint requirements, I need to implement claim extraction, summary abstraction, cascade propagation, final assembly, and provenance records. Let me trace through the spec carefully and implement each artifact.

### `synthesizer/models/claims.py`
```python
# synthesizer/models/claims.py
"""Claim table Pydantic models (§10.6, §10.7).

These models are required by SectionState (§10.12) which stores
claim_table: Optional[ClaimTable].

Supports: FR-20, FR-21, FR-22, FR-11.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field, model_validator

from synthesizer.models.enums import ConfidenceTag


class TextSpan(BaseModel):
    """Character offset range within a text (§10.6).

    Supports: FR-20, FR-21.
    """

    model_config = ConfigDict(extra="forbid")

    start: int = Field(
        ...,
        ge=0,
        description="Start character offset (0-indexed, inclusive).",
    )
    end: int = Field(
        ...,
        gt=0,
        description="End character offset (exclusive). Must be > start.",
    )

    @model_validator(mode="after")
    def check_end_greater_than_start(self) -> TextSpan:
        """Enforce end > start as required by §10.6."""
        if self.end <= self.start:
            raise ValueError(
                f"end ({self.end}) must be greater than start ({self.start})"
            )
        return self


class ClaimEntry(BaseModel):
    """Single claim extracted from a finalized section (§10.6).

    Supports: FR-20, FR-21.
    """

    model_config = ConfigDict(extra="forbid")

    claim_id: str = Field(
        ...,
        pattern=r"^claim_[0-9]+$",
        description="Unique within the parent ClaimTable. Pattern: claim_[0-9]+.",
    )
    claim_text: str = Field(
        ...,
        min_length=1,
        description="The claim statement as extracted.",
    )
    source_chunk_ids: List[str] = Field(
        ...,
        min_length=1,
        description="Chunk IDs from retrieval that support this claim.",
    )
    confidence_tag: ConfidenceTag = Field(
        ...,
        description="Classification of claim confidence.",
    )
    section_text_span: TextSpan = Field(
        ...,
        description="Character offsets locating the claim in section text.",
    )


class ClaimTable(BaseModel):
    """Collection of claims for a section (§10.7).

    Primary context channel for downstream sections (§13).
    Supports: FR-20, FR-21, FR-22, FR-11.
    """

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(
        ...,
        description="Section this claim table belongs to.",
    )
    version: int = Field(
        ...,
        ge=1,
        description="Extraction version (increments on re-extraction).",
    )
    claims: List[ClaimEntry] = Field(
        ...,
        description="Extracted claims.",
    )
    partial: bool = Field(
        default=False,
        description="Whether extraction was incomplete (DR-14).",
    )
    extraction_attempt: int = Field(
        ...,
        ge=1,
        description="Which attempt produced this table.",
    )
```

### `synthesizer/models/provenance.py`
```python
# synthesizer/models/provenance.py
"""Provenance record Pydantic model (§10.11).

Audit trail for a finalized section. Written once on finalization.
See Appendix D of the governing specification for an example.

Supports: FR-26.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.validation_models import ValidationResult


class ProvenanceRecord(BaseModel):
    """Audit trail for a finalized section (§10.11).

    Written once on finalization. Contains full generation and
    validation history for traceability.

    Supports: FR-26.
    """

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(
        ...,
        description="Section identifier.",
    )
    finalized_at: str = Field(
        ...,
        description="ISO 8601 timestamp of finalization.",
    )
    generation_model: str = Field(
        ...,
        description="Model identifier used for generation.",
    )
    generation_attempts: int = Field(
        ...,
        ge=1,
        description="Total generation attempts.",
    )
    validation_history: List[ValidationResult] = Field(
        ...,
        description="All validation results across all attempts.",
    )
    claim_table_version: Optional[int] = Field(
        default=None,
        description="Version of the extracted claim table.",
    )
    claim_table_partial: bool = Field(
        default=False,
        description="Whether claim table is partial.",
    )
    source_chunk_ids: List[str] = Field(
        ...,
        description="All chunk IDs used as evidence.",
    )
    upstream_dependencies_consumed: Dict[str, List[str]] = Field(
        ...,
        description="Maps DependencyKind → list of section_ids.",
    )
    cascade_triggers_received: int = Field(
        default=0,
        ge=0,
        description="Number of cascade invalidations received.",
    )
    word_count: int = Field(
        ...,
        ge=1,
        description="Final word count.",
    )
    heading_level: int = Field(
        ...,
        ge=1,
        le=6,
        description="Final heading level.",
    )


def write_provenance_record(
    record: ProvenanceRecord,
    output_dir: Path,
) -> Path:
    """Write a ProvenanceRecord to disk as JSON (§15.1).

    Writes to ``{output_dir}/sections/{section_id}/provenance.json``.

    Parameters
    ----------
    record : ProvenanceRecord
        The provenance record to persist.
    output_dir : Path
        Root synthesizer output directory (SYNTHESIZER_OUTPUT_DIR).

    Returns
    -------
    Path
        Path to the written provenance.json file.
    """
    section_dir = output_dir / "sections" / record.section_id
    section_dir.mkdir(parents=True, exist_ok=True)
    provenance_path = section_dir / "provenance.json"
    provenance_path.write_text(
        record.model_dump_json(indent=2),
        encoding="utf-8",
    )
    return provenance_path
```

### `synthesizer/extraction/__init__.py`
```python
# synthesizer/extraction/__init__.py
"""Claim extraction and summary abstraction sub-package (§9.2.3, §9.2.4, §12.4)."""
```

### `synthesizer/extraction/claim_extractor.py`
```python
# synthesizer/extraction/claim_extractor.py
"""Claim table extraction from finalized section text (§9.2.3, §12.4).

Invokes an LLM to extract structured ClaimTable (§10.7) from finalized
section content and its retrieval chunks.

Supports: FR-20, FR-22.
DR-14: CLAIM_EXTRACTION_RETRY_LIMIT is configurable (default 1).
DR-16: Model selection remains open — LLM client is injected via protocol.
DR-18: Output budget is 2000 tokens per §9.2.3; input budget remains open.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from synthesizer.config import CLAIM_EXTRACTION_RETRY_LIMIT
from synthesizer.models.claims import ClaimTable
from synthesizer.models.enums import ConfidenceTag
from synthesizer.retrieval.adapter import RankedChunk

logger = logging.getLogger(__name__)

# Output token cap per §9.2.3 (partially open DR-18)
CLAIM_EXTRACTOR_OUTPUT_TOKENS = 2000


# ---------------------------------------------------------------------------
# LLM client protocol (DR-16: model selection configurable per role)
# ---------------------------------------------------------------------------

@runtime_checkable
class LLMClient(Protocol):
    """Protocol for LLM invocation used by the claim extractor.

    DR-16 (open): Implementations may use different models per role.
    """

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int = CLAIM_EXTRACTOR_OUTPUT_TOKENS,
    ) -> str:
        """Invoke the LLM and return the response text."""
        ...


# ---------------------------------------------------------------------------
# System prompt (§9.2.3)
# ---------------------------------------------------------------------------

_CLAIM_EXTRACTOR_SYSTEM_PROMPT = (
    "You are a claim extraction specialist. Your task is to extract "
    "structured claims from a finalized section of a scientific literature "
    "review.\n\n"
    "For each claim you identify in the section text, produce a JSON entry "
    "with:\n"
    "- claim_id: unique identifier in format 'claim_0', 'claim_1', etc.\n"
    "- claim_text: the claim statement as it appears or is expressed in "
    "the section\n"
    "- source_chunk_ids: list of chunk IDs from the provided evidence "
    "chunks that support this claim (at least one required)\n"
    "- confidence_tag: one of 'directly_stated' (claim appears verbatim "
    "or near-verbatim in a source chunk), 'inferred' (reasonable "
    "inference from a source chunk), or 'synthesized' (combines "
    "information from multiple source chunks)\n"
    "- section_text_span: {\"start\": <int>, \"end\": <int>} character "
    "offsets locating the claim in the section text (0-indexed, start "
    "inclusive, end exclusive)\n\n"
    "Respond with ONLY valid JSON in this exact format:\n"
    "{\n"
    '  "section_id": "<section_id>",\n'
    '  "version": 1,\n'
    '  "claims": [<list of claim entries>],\n'
    '  "partial": false,\n'
    '  "extraction_attempt": 1\n'
    "}\n\n"
    "Extract ALL substantive claims from the section. Every claim must "
    "be traceable to at least one evidence chunk.\n"
)


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def _parse_claim_table_response(
    raw_response: str,
    section_id: str,
    version: int,
    attempt: int,
) -> ClaimTable:
    """Parse LLM response into a validated ClaimTable.

    Raises ValueError if parsing or validation fails.
    """
    text = raw_response.strip()
    # Handle markdown fences
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines)

    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object, got {type(data).__name__}")

    # Override metadata fields to ensure consistency
    data["section_id"] = section_id
    data["version"] = version
    data["extraction_attempt"] = attempt

    return ClaimTable.model_validate(data)


# ---------------------------------------------------------------------------
# FR-20, FR-22  Claim extraction with retry and partial fallback
# ---------------------------------------------------------------------------

def extract_claim_table(
    section_id: str,
    content_markdown: str,
    retrieved_chunks: List[RankedChunk],
    llm_client: LLMClient,
    version: int = 1,
    retry_limit: int = CLAIM_EXTRACTION_RETRY_LIMIT,
) -> ClaimTable:
    """Extract a ClaimTable from finalized section text (FR-20, FR-22).

    Invokes the LLM to extract structured claims, then validates the
    result. On failure, retries up to ``retry_limit`` times. If all
    attempts fail, returns a partial ClaimTable (FR-22).

    Parameters
    ----------
    section_id : str
        The section this claim table is for.
    content_markdown : str
        Finalized section content in Markdown.
    retrieved_chunks : list of RankedChunk
        Evidence chunks used during section generation.
    llm_client : LLMClient
        LLM client for claim extraction. DR-16: model configurable.
    version : int
        Claim table version (increments on re-extraction).
    retry_limit : int
        Maximum retries on failure. DR-14: configurable, default 1.

    Returns
    -------
    ClaimTable
        Extracted claim table. May have partial=True on retry exhaustion.

    Supports
    --------
    FR-20 : Produces ClaimTable with ClaimEntry instances.
    FR-22 : On retry exhaustion, sets partial=True and returns.
    DR-14 : retry_limit is configurable.
    DR-16 : LLM client is injected, model selection is open.
    DR-18 : Output budget is 2000 tokens; input budget remains open.
    """
    # Format evidence chunks for the prompt
    chunks_text_parts: List[str] = []
    for chunk in retrieved_chunks:
        meta = chunk.metadata
        meta_str = ", ".join(
            f"{k}: {v}" for k, v in sorted(meta.items()) if v
        ) or "no metadata"
        chunks_text_parts.append(
            f"  [{chunk.id}] ({meta_str})\n  {chunk.text}"
        )
    chunks_text = "\n".join(chunks_text_parts) if chunks_text_parts else "(No evidence chunks)"

    user_message = (
        f"Section ID: {section_id}\n\n"
        f"=== SECTION TEXT ===\n{content_markdown}\n"
        f"=== END SECTION TEXT ===\n\n"
        f"=== EVIDENCE CHUNKS ===\n{chunks_text}\n"
        f"=== END EVIDENCE CHUNKS ===\n\n"
        "Extract all substantive claims from the section text. "
        "Map each claim to supporting evidence chunk(s) by their IDs."
    )

    last_error: Optional[str] = None

    # Initial attempt + retries
    total_attempts = 1 + retry_limit
    for attempt_num in range(1, total_attempts + 1):
        try:
            prompt = user_message
            if last_error and attempt_num > 1:
                prompt += (
                    f"\n\nPrevious extraction attempt failed: {last_error}\n"
                    "Please fix the issues and try again."
                )

            raw_response = llm_client.invoke(
                system_prompt=_CLAIM_EXTRACTOR_SYSTEM_PROMPT,
                user_message=prompt,
                max_output_tokens=CLAIM_EXTRACTOR_OUTPUT_TOKENS,
            )

            claim_table = _parse_claim_table_response(
                raw_response, section_id, version, attempt_num
            )

            logger.info(
                "Claim extraction succeeded for section '%s' on attempt %d "
                "with %d claims.",
                section_id, attempt_num, len(claim_table.claims),
            )
            return claim_table

        except Exception as exc:
            last_error = str(exc)
            logger.warning(
                "Claim extraction attempt %d/%d failed for section '%s': %s",
                attempt_num, total_attempts, section_id, last_error,
            )

    # FR-22: All attempts exhausted — return partial claim table
    logger.warning(
        "Claim extraction exhausted all %d attempts for section '%s'. "
        "Returning partial claim table (FR-22).",
        total_attempts, section_id,
    )
    return ClaimTable(
        section_id=section_id,
        version=version,
        claims=[],
        partial=True,
        extraction_attempt=total_attempts,
    )
```

### `synthesizer/extraction/claim_validator.py`
```python
# synthesizer/extraction/claim_validator.py
"""Claim table validation with four sub-checks (§12.4, FR-21).

Four sub-checks validate an extracted ClaimTable before it is made
available to downstream sections (DR-02):

1. Completeness: key claims from section text are represented (≥90%).
2. Traceability: every ClaimEntry has ≥1 valid source_chunk_id.
3. Label consistency: confidence_tag values are appropriate.
4. Cross-validation: claims do not contradict the section text.

Supports: FR-21.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from synthesizer.models.claims import ClaimTable
from synthesizer.models.enums import ConfidenceTag

logger = logging.getLogger(__name__)


@dataclass
class ClaimValidationResult:
    """Result of claim table validation (§12.4).

    Each of the four sub-checks produces a pass/fail with details.
    The overall result passes only if all sub-checks pass.
    """

    completeness_passed: bool = True
    completeness_details: str = ""
    completeness_ratio: float = 1.0

    traceability_passed: bool = True
    traceability_details: str = ""
    untraceable_claims: List[str] = field(default_factory=list)

    label_consistency_passed: bool = True
    label_consistency_details: str = ""
    inconsistent_claims: List[str] = field(default_factory=list)

    cross_validation_passed: bool = True
    cross_validation_details: str = ""
    contradicting_claims: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Overall pass: all four sub-checks must pass."""
        return (
            self.completeness_passed
            and self.traceability_passed
            and self.label_consistency_passed
            and self.cross_validation_passed
        )

    @property
    def failure_reasons(self) -> List[str]:
        """Human-readable list of failed sub-check reasons."""
        reasons: List[str] = []
        if not self.completeness_passed:
            reasons.append(f"Completeness: {self.completeness_details}")
        if not self.traceability_passed:
            reasons.append(f"Traceability: {self.traceability_details}")
        if not self.label_consistency_passed:
            reasons.append(f"Label consistency: {self.label_consistency_details}")
        if not self.cross_validation_passed:
            reasons.append(f"Cross-validation: {self.cross_validation_details}")
        return reasons


# ---------------------------------------------------------------------------
# Sub-check 1: Completeness (§12.4)
# ---------------------------------------------------------------------------

def check_completeness(
    claim_table: ClaimTable,
    section_text: str,
    expected_claim_count: Optional[int] = None,
    threshold: float = 0.9,
) -> tuple[bool, str, float]:
    """Check that key claims from the section text are represented (§12.4).

    Target: ≥90% of identifiable claims covered.

    If ``expected_claim_count`` is not provided, estimates the number
    of substantive claims by counting sentences that contain assertion
    indicators (verbs, findings, etc.).

    Parameters
    ----------
    claim_table : ClaimTable
        Extracted claim table to validate.
    section_text : str
        Original section text.
    expected_claim_count : int, optional
        Known expected claim count (for testing). If None, estimated.
    threshold : float
        Minimum ratio of extracted claims to expected claims.

    Returns
    -------
    (passed, details, ratio)
    """
    if expected_claim_count is None:
        # Heuristic: count sentences with assertion-like patterns
        # This is a rough estimate; LLM-based counting would be more accurate
        sentences = [
            s.strip() for s in section_text.replace("\n", " ").split(".")
            if len(s.strip()) > 20
        ]
        # Filter to substantive sentences (not headings, not very short)
        substantive = [
            s for s in sentences
            if not s.strip().startswith("#") and len(s.split()) >= 5
        ]
        expected_claim_count = max(len(substantive), 1)

    actual_count = len(claim_table.claims)
    ratio = actual_count / max(expected_claim_count, 1)

    if ratio >= threshold:
        return (
            True,
            f"Completeness ratio {ratio:.2f} >= {threshold:.2f} "
            f"({actual_count}/{expected_claim_count} claims).",
            ratio,
        )
    else:
        return (
            False,
            f"Completeness ratio {ratio:.2f} < {threshold:.2f} "
            f"({actual_count}/{expected_claim_count} claims). "
            f"Expected at least {int(expected_claim_count * threshold)} claims.",
            ratio,
        )


# ---------------------------------------------------------------------------
# Sub-check 2: Traceability (§12.4)
# ---------------------------------------------------------------------------

def check_traceability(
    claim_table: ClaimTable,
    available_chunk_ids: Set[str],
) -> tuple[bool, str, List[str]]:
    """Check that every ClaimEntry has ≥1 valid source_chunk_id (§12.4).

    No orphan claims allowed. Each source_chunk_id must exist in the
    set of available chunk IDs from retrieval.

    Parameters
    ----------
    claim_table : ClaimTable
        Extracted claim table to validate.
    available_chunk_ids : set of str
        Valid chunk IDs from the retrieval results.

    Returns
    -------
    (passed, details, untraceable_claim_ids)
    """
    untraceable: List[str] = []

    for claim in claim_table.claims:
        # Check that at least one source_chunk_id is valid
        valid_ids = [
            cid for cid in claim.source_chunk_ids
            if cid in available_chunk_ids
        ]
        if not valid_ids:
            untraceable.append(claim.claim_id)

    if not untraceable:
        return (
            True,
            f"All {len(claim_table.claims)} claims are traceable to "
            f"valid source chunks.",
            [],
        )
    else:
        return (
            False,
            f"{len(untraceable)} claim(s) have no valid source_chunk_ids: "
            f"{untraceable}. Available chunk IDs: "
            f"{sorted(list(available_chunk_ids)[:5])}{'...' if len(available_chunk_ids) > 5 else ''}",
            untraceable,
        )


# ---------------------------------------------------------------------------
# Sub-check 3: Label consistency (§12.4)
# ---------------------------------------------------------------------------

def check_label_consistency(
    claim_table: ClaimTable,
    chunk_texts: Dict[str, str],
) -> tuple[bool, str, List[str]]:
    """Check that confidence_tag values are appropriate (§12.4).

    - DIRECTLY_STATED: claim should closely match source chunk text
      (high textual overlap)
    - INFERRED: claim is a reasonable inference (moderate overlap)
    - SYNTHESIZED: claim combines multiple sources (multiple source_chunk_ids)

    Parameters
    ----------
    claim_table : ClaimTable
        Extracted claim table to validate.
    chunk_texts : dict
        Maps chunk_id → chunk text for overlap comparison.

    Returns
    -------
    (passed, details, inconsistent_claim_ids)
    """
    inconsistent: List[str] = []

    for claim in claim_table.claims:
        tag = claim.confidence_tag

        if tag == ConfidenceTag.DIRECTLY_STATED:
            # Check: claim text should have significant overlap with
            # at least one source chunk
            claim_words = set(claim.claim_text.lower().split())
            found_overlap = False
            for cid in claim.source_chunk_ids:
                chunk_text = chunk_texts.get(cid, "")
                if chunk_text:
                    chunk_words = set(chunk_text.lower().split())
                    if chunk_words:
                        overlap = len(claim_words & chunk_words) / max(
                            len(claim_words), 1
                        )
                        if overlap >= 0.3:
                            found_overlap = True
                            break
            if not found_overlap and claim.source_chunk_ids:
                inconsistent.append(claim.claim_id)

        elif tag == ConfidenceTag.SYNTHESIZED:
            # SYNTHESIZED claims should reference multiple sources
            if len(claim.source_chunk_ids) < 2:
                inconsistent.append(claim.claim_id)

    if not inconsistent:
        return (
            True,
            f"All {len(claim_table.claims)} claims have consistent "
            f"confidence tags.",
            [],
        )
    else:
        return (
            False,
            f"{len(inconsistent)} claim(s) have inconsistent confidence "
            f"tags: {inconsistent}.",
            inconsistent,
        )


# ---------------------------------------------------------------------------
# Sub-check 4: Cross-validation (§12.4)
# ---------------------------------------------------------------------------

def check_cross_validation(
    claim_table: ClaimTable,
    section_text: str,
) -> tuple[bool, str, List[str]]:
    """Check that claims do not contradict the section text (§12.4).

    Verifies that each claim's text can be located (approximately) in
    the section text and does not contain obvious contradictions.

    Parameters
    ----------
    claim_table : ClaimTable
        Extracted claim table to validate.
    section_text : str
        Original section content_markdown.

    Returns
    -------
    (passed, details, contradicting_claim_ids)
    """
    contradicting: List[str] = []
    section_lower = section_text.lower()

    for claim in claim_table.claims:
        # Check 1: Verify the claim's text_span is within bounds
        span = claim.section_text_span
        if span.end > len(section_text):
            contradicting.append(claim.claim_id)
            continue

        # Check 2: Verify some textual overlap between claim text
        # and the span region of the section text
        span_text = section_text[span.start:span.end].lower()
        claim_words = set(claim.claim_text.lower().split())
        span_words = set(span_text.split())

        if span_words:
            overlap = len(claim_words & span_words) / max(len(claim_words), 1)
            if overlap < 0.15:
                # Claim text has very little overlap with its declared span
                contradicting.append(claim.claim_id)

    if not contradicting:
        return (
            True,
            f"All {len(claim_table.claims)} claims are consistent with "
            f"section text.",
            [],
        )
    else:
        return (
            False,
            f"{len(contradicting)} claim(s) contradict or are "
            f"inconsistent with section text: {contradicting}.",
            contradicting,
        )


# ---------------------------------------------------------------------------
# FR-21  Aggregate claim table validation
# ---------------------------------------------------------------------------

def validate_claim_table(
    claim_table: ClaimTable,
    section_text: str,
    available_chunk_ids: Set[str],
    chunk_texts: Optional[Dict[str, str]] = None,
    expected_claim_count: Optional[int] = None,
    completeness_threshold: float = 0.9,
) -> ClaimValidationResult:
    """Run all four claim table validation sub-checks (§12.4, FR-21).

    Parameters
    ----------
    claim_table : ClaimTable
        Extracted claim table to validate.
    section_text : str
        Finalized section content_markdown.
    available_chunk_ids : set of str
        Valid chunk IDs from retrieval.
    chunk_texts : dict, optional
        Maps chunk_id → chunk text. Required for label consistency check.
        If None, label consistency is skipped with a warning.
    expected_claim_count : int, optional
        Expected number of claims for completeness check.
    completeness_threshold : float
        Threshold for completeness sub-check (default 0.9 per §12.4).

    Returns
    -------
    ClaimValidationResult
        Aggregate result of all four sub-checks.
    """
    result = ClaimValidationResult()

    # Sub-check 1: Completeness
    comp_pass, comp_detail, comp_ratio = check_completeness(
        claim_table, section_text, expected_claim_count, completeness_threshold
    )
    result.completeness_passed = comp_pass
    result.completeness_details = comp_detail
    result.completeness_ratio = comp_ratio

    # Sub-check 2: Traceability
    trace_pass, trace_detail, trace_untraceable = check_traceability(
        claim_table, available_chunk_ids
    )
    result.traceability_passed = trace_pass
    result.traceability_details = trace_detail
    result.untraceable_claims = trace_untraceable

    # Sub-check 3: Label consistency
    if chunk_texts is not None:
        label_pass, label_detail, label_inconsistent = check_label_consistency(
            claim_table, chunk_texts
        )
        result.label_consistency_passed = label_pass
        result.label_consistency_details = label_detail
        result.inconsistent_claims = label_inconsistent
    else:
        logger.warning(
            "Chunk texts not provided for section '%s'; "
            "skipping label consistency check.",
            claim_table.section_id,
        )

    # Sub-check 4: Cross-validation
    cross_pass, cross_detail, cross_contradicting = check_cross_validation(
        claim_table, section_text
    )
    result.cross_validation_passed = cross_pass
    result.cross_validation_details = cross_detail
    result.contradicting_claims = cross_contradicting

    if result.passed:
        logger.info(
            "Claim table validation passed for section '%s' (%d claims).",
            claim_table.section_id, len(claim_table.claims),
        )
    else:
        logger.warning(
            "Claim table validation failed for section '%s': %s",
            claim_table.section_id, result.failure_reasons,
        )

    return result
```

### `synthesizer/extraction/summary_abstractifier.py`
```python
# synthesizer/extraction/summary_abstractifier.py
"""Summary abstractifier — generates 2-3 sentence section summaries (§9.2.4).

Generates summary abstracts from finalized section text for use as
thematic context in downstream generation prompts (§13.2).

Supports: FR-20 (post-finalization processing).
DR-16: Model selection remains open — LLM client is injected via protocol.
DR-18: Output budget is 200 tokens per §9.2.4; input budget remains open.
"""

from __future__ import annotations

import logging
from typing import Protocol, runtime_checkable

logger = logging.getLogger(__name__)

# Output token cap per §9.2.4 (partially open DR-18)
SUMMARY_ABSTRACTIFIER_OUTPUT_TOKENS = 200

# Word count constraints per §9.2.4
MIN_WORDS = 20
MAX_WORDS = 100


# ---------------------------------------------------------------------------
# LLM client protocol (DR-16: model selection configurable per role)
# ---------------------------------------------------------------------------

@runtime_checkable
class LLMClient(Protocol):
    """Protocol for LLM invocation used by the summary abstractifier.

    DR-16 (open): May use a lighter model than the Generator.
    """

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int = SUMMARY_ABSTRACTIFIER_OUTPUT_TOKENS,
    ) -> str:
        """Invoke the LLM and return the response text."""
        ...


# ---------------------------------------------------------------------------
# System prompts (§9.2.4)
# ---------------------------------------------------------------------------

_SUMMARY_SYSTEM_PROMPT = (
    "You are a scientific summarizer. Your task is to produce a concise "
    "summary abstract of a finalized section from a scientific literature "
    "review.\n\n"
    "Requirements:\n"
    "- Produce exactly 2-3 sentences\n"
    "- Stay within 50-100 words\n"
    "- Capture the section's key points and conclusions\n"
    "- Use formal academic tone\n"
    "- Do NOT include citations or references\n"
    "- Respond with ONLY the summary text, no JSON or formatting\n"
)

_TIGHTER_SUMMARY_SYSTEM_PROMPT = (
    "You are a scientific summarizer. Your previous summary was too "
    "long or too short. Please produce a concise summary abstract.\n\n"
    "STRICT requirements:\n"
    "- Produce EXACTLY 2-3 sentences\n"
    "- MUST be between 50 and 100 words (count carefully)\n"
    "- Capture only the most important point(s)\n"
    "- Use formal academic tone\n"
    "- Respond with ONLY the summary text\n"
)


def _count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def _count_sentences(text: str) -> int:
    """Approximate sentence count."""
    import re
    sentences = re.split(r'[.!?