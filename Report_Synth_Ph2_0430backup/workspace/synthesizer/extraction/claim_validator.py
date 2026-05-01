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