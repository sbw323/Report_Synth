# synthesizer/observability/metrics.py
"""Post-run metrics computation and persistence (§17.2, NFR-07).

Computes all seven metrics defined in §17.2 and writes them to
``{SYNTHESIZER_OUTPUT_DIR}/run_metrics.json`` at run conclusion.

Metrics:
  1. structural_compliance_rate — % sections passing L1 on first attempt (≥90%)
  2. style_compliance_rate — % sections passing L2 on first attempt (≥85%)
  3. dependency_completeness — % upstream claim entries engaged by downstream (≥80%)
  4. unsupported_claim_rate — % claims not traceable to evidence (≤10%)
  5. revision_churn — average generation attempts per section (≤2.0)
  6. claim_table_completeness — % sections with non-partial claim tables (≥90%)
  7. evidence_claim_agreement — % claim entries with consistent confidence_tag (≥85%)

Supports: NFR-07.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from synthesizer.models.claims import ClaimTable
from synthesizer.models.enums import (
    ConfidenceTag,
    DependencyKind,
    SectionLifecycleState,
    ValidationLayer,
)
from synthesizer.models.report_plan import DependencyEdge
from synthesizer.models.state import RunState, SectionState

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Metric key constants (§17.2)
# ---------------------------------------------------------------------------

METRIC_STRUCTURAL_COMPLIANCE_RATE = "structural_compliance_rate"
METRIC_STYLE_COMPLIANCE_RATE = "style_compliance_rate"
METRIC_DEPENDENCY_COMPLETENESS = "dependency_completeness"
METRIC_UNSUPPORTED_CLAIM_RATE = "unsupported_claim_rate"
METRIC_REVISION_CHURN = "revision_churn"
METRIC_CLAIM_TABLE_COMPLETENESS = "claim_table_completeness"
METRIC_EVIDENCE_CLAIM_AGREEMENT = "evidence_claim_agreement"

ALL_METRIC_KEYS = frozenset({
    METRIC_STRUCTURAL_COMPLIANCE_RATE,
    METRIC_STYLE_COMPLIANCE_RATE,
    METRIC_DEPENDENCY_COMPLETENESS,
    METRIC_UNSUPPORTED_CLAIM_RATE,
    METRIC_REVISION_CHURN,
    METRIC_CLAIM_TABLE_COMPLETENESS,
    METRIC_EVIDENCE_CLAIM_AGREEMENT,
})


# ---------------------------------------------------------------------------
# Metric 1: Structural compliance rate (§17.2)
# ---------------------------------------------------------------------------

def compute_structural_compliance_rate(
    section_states: Dict[str, SectionState],
) -> float:
    """% of sections passing Layer 1 on first attempt. Target: ≥90%.

    Examines each section's validation_history for STRUCTURAL layer
    results. A section counts as first-attempt pass if its first
    STRUCTURAL result has passed=True.
    """
    if not section_states:
        return 1.0

    total = 0
    first_attempt_pass = 0

    for ss in section_states.values():
        # Only count sections that reached at least drafted state
        if ss.state == SectionLifecycleState.QUEUED:
            continue

        l1_results = [
            vr for vr in ss.validation_history
            if vr.layer == ValidationLayer.STRUCTURAL
        ]
        if l1_results:
            total += 1
            # First L1 result for this section
            if l1_results[0].passed:
                first_attempt_pass += 1
        # Sections without L1 results but past queued are counted in total
        elif ss.state not in (
            SectionLifecycleState.QUEUED,
            SectionLifecycleState.GENERATING,
        ):
            total += 1

    if total == 0:
        return 1.0
    return first_attempt_pass / total


# ---------------------------------------------------------------------------
# Metric 2: Style compliance rate (§17.2)
# ---------------------------------------------------------------------------

def compute_style_compliance_rate(
    section_states: Dict[str, SectionState],
) -> float:
    """% of sections passing Layer 2 on first attempt. Target: ≥85%."""
    if not section_states:
        return 1.0

    total = 0
    first_attempt_pass = 0

    for ss in section_states.values():
        if ss.state == SectionLifecycleState.QUEUED:
            continue

        l2_results = [
            vr for vr in ss.validation_history
            if vr.layer == ValidationLayer.RULE_BASED
        ]
        if l2_results:
            total += 1
            if l2_results[0].passed:
                first_attempt_pass += 1

    if total == 0:
        return 1.0
    return first_attempt_pass / total


# ---------------------------------------------------------------------------
# Metric 3: Dependency completeness (§17.2)
# ---------------------------------------------------------------------------

def compute_dependency_completeness(
    section_states: Dict[str, SectionState],
    generation_dag_edges: List[DependencyEdge],
    section_contents: Optional[Dict[str, str]] = None,
) -> float:
    """% of upstream claim table entries engaged by downstream sections.

    Target: ≥80%.

    Iterates upstream ClaimTable entries across content-dependency edges.
    For each claim, checks if the downstream section's text or claim table
    engages with it by looking for key words from the claim text.

    Parameters
    ----------
    section_states : dict
        Maps section_id → SectionState.
    generation_dag_edges : list of DependencyEdge
        Content-type dependency edges from RunState.
    section_contents : dict, optional
        Maps section_id → content_markdown. If not provided, engagement
        checking is done only against downstream claim tables.
    """
    content_edges = [
        e for e in generation_dag_edges
        if e.kind == DependencyKind.CONTENT
    ]

    if not content_edges:
        return 1.0

    total_upstream_claims = 0
    engaged_claims = 0
    section_contents = section_contents or {}

    for edge in content_edges:
        upstream_id = edge.target_section_id
        downstream_id = edge.source_section_id

        upstream_ss = section_states.get(upstream_id)
        downstream_ss = section_states.get(downstream_id)

        if upstream_ss is None or upstream_ss.claim_table is None:
            continue

        upstream_ct = upstream_ss.claim_table

        # Build downstream text corpus for engagement checking
        downstream_text_lower = ""
        if downstream_id in section_contents:
            downstream_text_lower = section_contents[downstream_id].lower()

        # Also check downstream claim table for engagement
        downstream_claim_texts: Set[str] = set()
        if downstream_ss is not None and downstream_ss.claim_table is not None:
            for dc in downstream_ss.claim_table.claims:
                downstream_claim_texts.add(dc.claim_text.lower())

        for claim in upstream_ct.claims:
            total_upstream_claims += 1
            # Engagement heuristic: check if significant words from the
            # claim text appear in the downstream text or claim table
            claim_words = set(claim.claim_text.lower().split())
            # Filter to meaningful words (>3 chars, not common stopwords)
            significant_words = {
                w for w in claim_words
                if len(w) > 3 and w not in _STOPWORDS
            }
            if not significant_words:
                # Very short claim — count as engaged if downstream has any content
                if downstream_text_lower or downstream_claim_texts:
                    engaged_claims += 1
                continue

            # Check engagement against downstream content
            matched_in_content = sum(
                1 for w in significant_words if w in downstream_text_lower
            )
            content_ratio = matched_in_content / len(significant_words)

            # Check engagement against downstream claim table
            matched_in_claims = False
            for dct in downstream_claim_texts:
                dct_words = set(dct.split())
                overlap = len(significant_words & dct_words)
                if overlap >= max(1, len(significant_words) * 0.3):
                    matched_in_claims = True
                    break

            if content_ratio >= 0.3 or matched_in_claims:
                engaged_claims += 1

    if total_upstream_claims == 0:
        return 1.0
    return engaged_claims / total_upstream_claims


# Common English stopwords for engagement checking
_STOPWORDS = frozenset({
    "the", "and", "for", "are", "but", "not", "you", "all", "can",
    "had", "her", "was", "one", "our", "out", "has", "have", "been",
    "some", "them", "than", "its", "over", "such", "that", "this",
    "with", "will", "each", "from", "they", "were", "which", "their",
    "said", "what", "when", "where", "does", "also", "more", "very",
    "into", "most", "only", "other", "about", "these", "those",
})


# ---------------------------------------------------------------------------
# Metric 4: Unsupported claim rate (§17.2)
# ---------------------------------------------------------------------------

def compute_unsupported_claim_rate(
    section_states: Dict[str, SectionState],
    retrieval_chunk_ids: Optional[Dict[str, Set[str]]] = None,
) -> float:
    """% of claims not traceable to evidence. Target: ≤10%.

    For each section's ClaimTable, counts entries where source_chunk_ids
    is empty or all referenced chunk IDs are absent from the retrieval set.

    Parameters
    ----------
    section_states : dict
        Maps section_id → SectionState.
    retrieval_chunk_ids : dict, optional
        Maps section_id → set of chunk IDs that were retrieved for that
        section. If None, only checks for empty source_chunk_ids.
    """
    retrieval_chunk_ids = retrieval_chunk_ids or {}
    total_claims = 0
    unsupported = 0

    for section_id, ss in section_states.items():
        if ss.claim_table is None:
            continue

        available_chunks = retrieval_chunk_ids.get(section_id, set())

        for claim in ss.claim_table.claims:
            total_claims += 1

            # Check 1: empty source_chunk_ids
            if not claim.source_chunk_ids:
                unsupported += 1
                continue

            # Check 2: all referenced chunk IDs absent from retrieval set
            if available_chunks:
                valid_refs = [
                    cid for cid in claim.source_chunk_ids
                    if cid in available_chunks
                ]
                if not valid_refs:
                    unsupported += 1

    if total_claims == 0:
        return 0.0
    return unsupported / total_claims


# ---------------------------------------------------------------------------
# Metric 5: Revision churn (§17.2)
# ---------------------------------------------------------------------------

def compute_revision_churn(
    section_states: Dict[str, SectionState],
) -> float:
    """Average number of generation attempts per section. Target: ≤2.0.

    Uses SectionState.version (increments on each re-generation).
    """
    if not section_states:
        return 0.0

    # Only count sections that were actually generated
    versions = [
        ss.version for ss in section_states.values()
        if ss.state not in (SectionLifecycleState.QUEUED,)
    ]
    if not versions:
        return 0.0
    return sum(versions) / len(versions)


# ---------------------------------------------------------------------------
# Metric 6: Claim-table completeness (§17.2)
# ---------------------------------------------------------------------------

def compute_claim_table_completeness(
    section_states: Dict[str, SectionState],
) -> float:
    """% of sections with non-partial claim tables. Target: ≥90%."""
    if not section_states:
        return 1.0

    # Only count sections that reached finalized/stable/escalated
    finalized_states = {
        SectionLifecycleState.FINALIZED,
        SectionLifecycleState.STABLE,
        SectionLifecycleState.ESCALATED,
    }
    eligible = [
        ss for ss in section_states.values()
        if ss.state in finalized_states
    ]
    if not eligible:
        return 1.0

    non_partial = sum(
        1 for ss in eligible
        if ss.claim_table is not None and not ss.claim_table.partial
    )
    return non_partial / len(eligible)


# ---------------------------------------------------------------------------
# Metric 7: Evidence-claim agreement (§17.2)
# ---------------------------------------------------------------------------

def compute_evidence_claim_agreement(
    section_states: Dict[str, SectionState],
    chunk_texts: Optional[Dict[str, str]] = None,
) -> float:
    """% of claim entries with consistent confidence_tag. Target: ≥85%.

    For each ClaimEntry, verifies confidence_tag consistency using
    heuristic rules:
    - DIRECTLY_STATED: should have significant textual overlap with
      at least one source chunk (≥30% word overlap)
    - SYNTHESIZED: should reference multiple source chunks (≥2)
    - INFERRED: no strong constraint (always consistent)

    Parameters
    ----------
    section_states : dict
        Maps section_id → SectionState.
    chunk_texts : dict, optional
        Maps chunk_id → chunk text. If not provided, only structural
        checks are performed (SYNTHESIZED multi-source check).
    """
    chunk_texts = chunk_texts or {}
    total_entries = 0
    consistent_entries = 0

    for ss in section_states.values():
        if ss.claim_table is None:
            continue

        for claim in ss.claim_table.claims:
            total_entries += 1
            tag = claim.confidence_tag
            is_consistent = True

            if tag == ConfidenceTag.DIRECTLY_STATED:
                # Check for textual overlap with source chunks
                if chunk_texts:
                    found_overlap = False
                    claim_words = set(claim.claim_text.lower().split())
                    for cid in claim.source_chunk_ids:
                        ctext = chunk_texts.get(cid, "")
                        if ctext:
                            ctext_words = set(ctext.lower().split())
                            if ctext_words:
                                overlap = len(claim_words & ctext_words) / max(
                                    len(claim_words), 1
                                )
                                if overlap >= 0.3:
                                    found_overlap = True
                                    break
                    if not found_overlap and claim.source_chunk_ids:
                        is_consistent = False

            elif tag == ConfidenceTag.SYNTHESIZED:
                # Should reference multiple sources
                if len(claim.source_chunk_ids) < 2:
                    is_consistent = False

            # INFERRED: always consistent (no strong constraint)

            if is_consistent:
                consistent_entries += 1

    if total_entries == 0:
        return 1.0
    return consistent_entries / total_entries


# ---------------------------------------------------------------------------
# NFR-07  Aggregate computation and persistence
# ---------------------------------------------------------------------------

def compute_all_metrics(
    run_state: RunState,
    section_contents: Optional[Dict[str, str]] = None,
    retrieval_chunk_ids: Optional[Dict[str, Set[str]]] = None,
    chunk_texts: Optional[Dict[str, str]] = None,
) -> Dict[str, float]:
    """Compute all seven §17.2 metrics from the run state.

    Parameters
    ----------
    run_state : RunState
        The final run state after all processing.
    section_contents : dict, optional
        Maps section_id → content_markdown for dependency completeness.
    retrieval_chunk_ids : dict, optional
        Maps section_id → set of retrieved chunk IDs.
    chunk_texts : dict, optional
        Maps chunk_id → chunk text for evidence-claim agreement.

    Returns
    -------
    dict
        Maps metric key → float value. All seven keys are always present.
    """
    ss = run_state.section_states

    return {
        METRIC_STRUCTURAL_COMPLIANCE_RATE: compute_structural_compliance_rate(ss),
        METRIC_STYLE_COMPLIANCE_RATE: compute_style_compliance_rate(ss),
        METRIC_DEPENDENCY_COMPLETENESS: compute_dependency_completeness(
            ss, run_state.generation_dag_edges, section_contents
        ),
        METRIC_UNSUPPORTED_CLAIM_RATE: compute_unsupported_claim_rate(
            ss, retrieval_chunk_ids
        ),
        METRIC_REVISION_CHURN: compute_revision_churn(ss),
        METRIC_CLAIM_TABLE_COMPLETENESS: compute_claim_table_completeness(ss),
        METRIC_EVIDENCE_CLAIM_AGREEMENT: compute_evidence_claim_agreement(
            ss, chunk_texts
        ),
    }


def write_run_metrics(
    metrics: Dict[str, float],
    output_dir: Path,
) -> Path:
    """Write run_metrics.json to the output directory (NFR-07).

    Parameters
    ----------
    metrics : dict
        The seven metric values.
    output_dir : Path
        SYNTHESIZER_OUTPUT_DIR.

    Returns
    -------
    Path
        Path to the written run_metrics.json file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / "run_metrics.json"

    # Ensure all seven keys are present
    for key in ALL_METRIC_KEYS:
        if key not in metrics:
            logger.warning("Metric '%s' missing; defaulting to 0.0", key)
            metrics[key] = 0.0

    metrics_path.write_text(
        json.dumps(metrics, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    logger.info("Run metrics written to %s", metrics_path)
    return metrics_path