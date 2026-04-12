Looking at the sprint requirements, I need to implement observability (events, metrics, token tracking), model initialization checks, and an acceptance harness. Let me trace each artifact to the governing specification and implement.

### `synthesizer/observability/__init__.py`
```python
# synthesizer/observability/__init__.py
"""Observability sub-package (§17).

Provides structured log events, post-run metrics, and token accounting.
"""
```

### `synthesizer/observability/events.py`
```python
# synthesizer/observability/events.py
"""Structured log event emitter for all state transitions (§17.1, NFR-06).

Emits JSON-structured events at every section state transition and
additional lifecycle events. Each event conforms to the schema defined
in §17.1:

    {
        "event_type": "state_transition",
        "section_id": "...",
        "from_state": "...",
        "to_state": "...",
        "timestamp": "ISO 8601",
        "metadata": { ... }
    }

Additional event types per §17.1:
    run_started, run_completed, run_failed, cascade_triggered,
    escalation_triggered, checkpoint_written, assembly_started,
    assembly_completed

Supports: NFR-06.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger("synthesizer.events")

# ---------------------------------------------------------------------------
# Event type constants (§17.1)
# ---------------------------------------------------------------------------

EVENT_STATE_TRANSITION = "state_transition"
EVENT_RUN_STARTED = "run_started"
EVENT_RUN_COMPLETED = "run_completed"
EVENT_RUN_FAILED = "run_failed"
EVENT_CASCADE_TRIGGERED = "cascade_triggered"
EVENT_ESCALATION_TRIGGERED = "escalation_triggered"
EVENT_CHECKPOINT_WRITTEN = "checkpoint_written"
EVENT_ASSEMBLY_STARTED = "assembly_started"
EVENT_ASSEMBLY_COMPLETED = "assembly_completed"
EVENT_LATENCY_ALERT = "latency_alert"
EVENT_BUDGET_EXCEEDED = "budget_exceeded"

ALL_EVENT_TYPES = frozenset({
    EVENT_STATE_TRANSITION,
    EVENT_RUN_STARTED,
    EVENT_RUN_COMPLETED,
    EVENT_RUN_FAILED,
    EVENT_CASCADE_TRIGGERED,
    EVENT_ESCALATION_TRIGGERED,
    EVENT_CHECKPOINT_WRITTEN,
    EVENT_ASSEMBLY_STARTED,
    EVENT_ASSEMBLY_COMPLETED,
    EVENT_LATENCY_ALERT,
    EVENT_BUDGET_EXCEEDED,
})


def _now_iso() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# In-memory event log for test / audit access
# ---------------------------------------------------------------------------

_event_log: List[Dict[str, Any]] = []


def get_event_log() -> List[Dict[str, Any]]:
    """Return the in-memory event log (for testing and audit).

    Returns a shallow copy so callers cannot accidentally mutate the log.
    """
    return list(_event_log)


def clear_event_log() -> None:
    """Clear the in-memory event log. Useful between test runs."""
    _event_log.clear()


# ---------------------------------------------------------------------------
# Core event emission
# ---------------------------------------------------------------------------

def _emit(event: Dict[str, Any]) -> None:
    """Write event to the structured logger and append to in-memory log."""
    _event_log.append(event)
    logger.info(json.dumps(event, default=str))


# ---------------------------------------------------------------------------
# §17.1  State transition event (NFR-06)
# ---------------------------------------------------------------------------

def emit_state_transition(
    section_id: str,
    from_state: str,
    to_state: str,
    *,
    trigger_event: Optional[str] = None,
    attempt: Optional[int] = None,
    model: Optional[str] = None,
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """Emit a state_transition event per §17.1 (NFR-06).

    Parameters
    ----------
    section_id : str
        Section undergoing the transition.
    from_state : str
        Previous lifecycle state.
    to_state : str
        New lifecycle state.
    trigger_event : str, optional
        The event that triggered the transition (e.g., "layer_1_pass").
    attempt : int, optional
        Current attempt number.
    model : str, optional
        Model identifier used.
    input_tokens : int, optional
        Input tokens consumed by this call.
    output_tokens : int, optional
        Output tokens consumed by this call.
    extra_metadata : dict, optional
        Additional metadata to include.
    timestamp : str, optional
        ISO 8601 timestamp; defaults to now.

    Returns
    -------
    dict
        The emitted event dictionary.
    """
    metadata: Dict[str, Any] = {}
    if trigger_event is not None:
        metadata["trigger_event"] = trigger_event
    if attempt is not None:
        metadata["attempt"] = attempt
    if model is not None:
        metadata["model"] = model
    if input_tokens is not None:
        metadata["input_tokens"] = input_tokens
    if output_tokens is not None:
        metadata["output_tokens"] = output_tokens
    if extra_metadata:
        metadata.update(extra_metadata)

    event: Dict[str, Any] = {
        "event_type": EVENT_STATE_TRANSITION,
        "section_id": section_id,
        "from_state": from_state,
        "to_state": to_state,
        "timestamp": timestamp or _now_iso(),
        "metadata": metadata,
    }
    _emit(event)
    return event


# ---------------------------------------------------------------------------
# Lifecycle events (§17.1)
# ---------------------------------------------------------------------------

def emit_run_started(
    run_id: str,
    report_plan_version: str,
    section_count: int,
    *,
    timestamp: Optional[str] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Emit a run_started event."""
    metadata: Dict[str, Any] = {
        "run_id": run_id,
        "report_plan_version": report_plan_version,
        "section_count": section_count,
    }
    if extra_metadata:
        metadata.update(extra_metadata)
    event: Dict[str, Any] = {
        "event_type": EVENT_RUN_STARTED,
        "section_id": None,
        "from_state": None,
        "to_state": None,
        "timestamp": timestamp or _now_iso(),
        "metadata": metadata,
    }
    _emit(event)
    return event


def emit_run_completed(
    run_id: str,
    *,
    sections_finalized: int = 0,
    sections_escalated: int = 0,
    total_input_tokens: int = 0,
    total_output_tokens: int = 0,
    wall_clock_seconds: Optional[float] = None,
    timestamp: Optional[str] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Emit a run_completed event."""
    metadata: Dict[str, Any] = {
        "run_id": run_id,
        "sections_finalized": sections_finalized,
        "sections_escalated": sections_escalated,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
    }
    if wall_clock_seconds is not None:
        metadata["wall_clock_seconds"] = wall_clock_seconds
    if extra_metadata:
        metadata.update(extra_metadata)
    event: Dict[str, Any] = {
        "event_type": EVENT_RUN_COMPLETED,
        "section_id": None,
        "from_state": None,
        "to_state": None,
        "timestamp": timestamp or _now_iso(),
        "metadata": metadata,
    }
    _emit(event)
    return event


def emit_run_failed(
    run_id: str,
    error: str,
    *,
    timestamp: Optional[str] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Emit a run_failed event."""
    metadata: Dict[str, Any] = {
        "run_id": run_id,
        "error": error,
    }
    if extra_metadata:
        metadata.update(extra_metadata)
    event: Dict[str, Any] = {
        "event_type": EVENT_RUN_FAILED,
        "section_id": None,
        "from_state": None,
        "to_state": None,
        "timestamp": timestamp or _now_iso(),
        "metadata": metadata,
    }
    _emit(event)
    return event


def emit_cascade_triggered(
    source_section_id: str,
    affected_sections: List[str],
    cascade_depth: int,
    *,
    timestamp: Optional[str] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Emit a cascade_triggered event (FR-23, FR-24)."""
    metadata: Dict[str, Any] = {
        "source_section_id": source_section_id,
        "affected_sections": affected_sections,
        "cascade_depth": cascade_depth,
    }
    if extra_metadata:
        metadata.update(extra_metadata)
    event: Dict[str, Any] = {
        "event_type": EVENT_CASCADE_TRIGGERED,
        "section_id": source_section_id,
        "from_state": None,
        "to_state": None,
        "timestamp": timestamp or _now_iso(),
        "metadata": metadata,
    }
    _emit(event)
    return event


def emit_escalation_triggered(
    section_id: str,
    reason: str,
    *,
    from_state: Optional[str] = None,
    timestamp: Optional[str] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Emit an escalation_triggered event (FR-19, FR-24)."""
    metadata: Dict[str, Any] = {"reason": reason}
    if extra_metadata:
        metadata.update(extra_metadata)
    event: Dict[str, Any] = {
        "event_type": EVENT_ESCALATION_TRIGGERED,
        "section_id": section_id,
        "from_state": from_state,
        "to_state": "escalated",
        "timestamp": timestamp or _now_iso(),
        "metadata": metadata,
    }
    _emit(event)
    return event


def emit_checkpoint_written(
    run_id: str,
    checkpoint_path: str,
    *,
    section_id: Optional[str] = None,
    timestamp: Optional[str] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Emit a checkpoint_written event (NFR-03)."""
    metadata: Dict[str, Any] = {
        "run_id": run_id,
        "checkpoint_path": checkpoint_path,
    }
    if extra_metadata:
        metadata.update(extra_metadata)
    event: Dict[str, Any] = {
        "event_type": EVENT_CHECKPOINT_WRITTEN,
        "section_id": section_id,
        "from_state": None,
        "to_state": None,
        "timestamp": timestamp or _now_iso(),
        "metadata": metadata,
    }
    _emit(event)
    return event


def emit_assembly_started(
    run_id: str,
    section_count: int,
    *,
    timestamp: Optional[str] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Emit an assembly_started event (FR-26)."""
    metadata: Dict[str, Any] = {
        "run_id": run_id,
        "section_count": section_count,
    }
    if extra_metadata:
        metadata.update(extra_metadata)
    event: Dict[str, Any] = {
        "event_type": EVENT_ASSEMBLY_STARTED,
        "section_id": None,
        "from_state": None,
        "to_state": None,
        "timestamp": timestamp or _now_iso(),
        "metadata": metadata,
    }
    _emit(event)
    return event


def emit_assembly_completed(
    run_id: str,
    output_path: str,
    *,
    total_word_count: Optional[int] = None,
    timestamp: Optional[str] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Emit an assembly_completed event (FR-26)."""
    metadata: Dict[str, Any] = {
        "run_id": run_id,
        "output_path": output_path,
    }
    if total_word_count is not None:
        metadata["total_word_count"] = total_word_count
    if extra_metadata:
        metadata.update(extra_metadata)
    event: Dict[str, Any] = {
        "event_type": EVENT_ASSEMBLY_COMPLETED,
        "section_id": None,
        "from_state": None,
        "to_state": None,
        "timestamp": timestamp or _now_iso(),
        "metadata": metadata,
    }
    _emit(event)
    return event


def emit_latency_alert(
    section_id: str,
    latency_seconds: float,
    threshold_seconds: float = 120.0,
    *,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """Emit a latency_alert event when section generation exceeds threshold (NFR-01)."""
    event: Dict[str, Any] = {
        "event_type": EVENT_LATENCY_ALERT,
        "section_id": section_id,
        "from_state": None,
        "to_state": None,
        "timestamp": timestamp or _now_iso(),
        "metadata": {
            "latency_seconds": latency_seconds,
            "threshold_seconds": threshold_seconds,
        },
    }
    _emit(event)
    logger.warning(
        "Section '%s' generation latency %.1fs exceeds threshold %.1fs (NFR-01)",
        section_id,
        latency_seconds,
        threshold_seconds,
    )
    return event


def emit_budget_exceeded(
    run_id: str,
    cumulative_tokens: int,
    ceiling: int,
    *,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """Emit a budget_exceeded event when token ceiling is reached (NFR-02)."""
    event: Dict[str, Any] = {
        "event_type": EVENT_BUDGET_EXCEEDED,
        "section_id": None,
        "from_state": None,
        "to_state": None,
        "timestamp": timestamp or _now_iso(),
        "metadata": {
            "run_id": run_id,
            "cumulative_tokens": cumulative_tokens,
            "ceiling": ceiling,
        },
    }
    _emit(event)
    return event
```

### `synthesizer/observability/metrics.py`
```python
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
```

### `synthesizer/observability/tokens.py`
```python
# synthesizer/observability/tokens.py
"""Token accounting and budget enforcement (§5, §16, §17, NFR-02).

Tracks cumulative input and output tokens across all LLM calls within a
run. Enforces TOKEN_BUDGET_CEILING (DR-17: open, defaults to None).

Also provides per-section generation latency tracking with alert
on >120s (NFR-01).

Supports: NFR-01, NFR-02.
DR-17 (open): TOKEN_BUDGET_CEILING defaults to None (no limit).
DR-18 (open): Per-role input token budgets remain open.
"""

from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Generator, List, Optional

from synthesizer.config import TOKEN_BUDGET_CEILING

logger = logging.getLogger(__name__)

# NFR-01: Maximum generation latency per section (seconds)
DEFAULT_LATENCY_THRESHOLD_SECONDS = 120.0


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class TokenBudgetExceededError(Exception):
    """Raised when cumulative tokens exceed TOKEN_BUDGET_CEILING (NFR-02).

    Attributes
    ----------
    cumulative_tokens : int
        Total tokens consumed at the time of the error.
    ceiling : int
        The configured budget ceiling.
    """

    def __init__(
        self,
        cumulative_tokens: int,
        ceiling: int,
        *,
        message: Optional[str] = None,
    ) -> None:
        self.cumulative_tokens = cumulative_tokens
        self.ceiling = ceiling
        msg = message or (
            f"Token budget exceeded: {cumulative_tokens} tokens consumed, "
            f"ceiling is {ceiling}. Generation halted per NFR-02."
        )
        super().__init__(msg)


# ---------------------------------------------------------------------------
# Per-call record
# ---------------------------------------------------------------------------

@dataclass
class LLMCallRecord:
    """Record of a single LLM invocation for accounting purposes."""

    role: str  # e.g., "generator", "validator", "claim_extractor", "summary_abstractifier"
    section_id: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""
    latency_seconds: float = 0.0
    timestamp: str = ""


# ---------------------------------------------------------------------------
# Section latency timer
# ---------------------------------------------------------------------------

@dataclass
class SectionLatencyRecord:
    """Latency record for a single section generation (NFR-01)."""

    section_id: str
    start_time: float = 0.0
    end_time: float = 0.0
    latency_seconds: float = 0.0
    threshold_exceeded: bool = False


# ---------------------------------------------------------------------------
# Token tracker (NFR-02)
# ---------------------------------------------------------------------------

@dataclass
class TokenTracker:
    """Cumulative token accounting with budget ceiling enforcement (NFR-02).

    Tracks input and output tokens across all LLM calls in a run.
    Raises TokenBudgetExceededError when TOKEN_BUDGET_CEILING is reached.

    DR-17 (open): ceiling defaults to None (no limit).
    DR-18 (open): Per-role input budgets are not enforced here.

    Attributes
    ----------
    ceiling : int or None
        Maximum cumulative tokens (input + output). None = no limit.
    cumulative_input_tokens : int
        Total input tokens consumed.
    cumulative_output_tokens : int
        Total output tokens consumed.
    call_records : list of LLMCallRecord
        Individual call records for auditing.
    latency_records : list of SectionLatencyRecord
        Per-section latency records (NFR-01).
    latency_threshold : float
        Threshold in seconds for latency alerts (NFR-01, default 120s).
    """

    ceiling: Optional[int] = None
    cumulative_input_tokens: int = 0
    cumulative_output_tokens: int = 0
    call_records: List[LLMCallRecord] = field(default_factory=list)
    latency_records: List[SectionLatencyRecord] = field(default_factory=list)
    latency_threshold: float = DEFAULT_LATENCY_THRESHOLD_SECONDS

    def __post_init__(self) -> None:
        # If ceiling not explicitly provided, use config default
        if self.ceiling is None:
            self.ceiling = TOKEN_BUDGET_CEILING

    @property
    def cumulative_total_tokens(self) -> int:
        """Total tokens consumed (input + output)."""
        return self.cumulative_input_tokens + self.cumulative_output_tokens

    def record_call(
        self,
        role: str,
        input_tokens: int,
        output_tokens: int,
        *,
        section_id: Optional[str] = None,
        model: str = "",
        latency_seconds: float = 0.0,
    ) -> LLMCallRecord:
        """Record an LLM call and enforce budget ceiling (NFR-02).

        Parameters
        ----------
        role : str
            LLM role (e.g., "generator", "validator").
        input_tokens : int
            Input tokens consumed.
        output_tokens : int
            Output tokens consumed.
        section_id : str, optional
            Associated section ID.
        model : str
            Model identifier used.
        latency_seconds : float
            Call latency in seconds.

        Returns
        -------
        LLMCallRecord
            The recorded call.

        Raises
        ------
        TokenBudgetExceededError
            If cumulative tokens exceed the ceiling after this call.
        """
        self.cumulative_input_tokens += input_tokens
        self.cumulative_output_tokens += output_tokens

        record = LLMCallRecord(
            role=role,
            section_id=section_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model=model,
            latency_seconds=latency_seconds,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.call_records.append(record)

        logger.debug(
            "LLM call recorded: role=%s section=%s in=%d out=%d cumulative=%d",
            role, section_id, input_tokens, output_tokens,
            self.cumulative_total_tokens,
        )

        # NFR-02: Enforce budget ceiling
        self._check_ceiling()

        return record

    def _check_ceiling(self) -> None:
        """Check if cumulative tokens exceed the ceiling. Raise if so."""
        if self.ceiling is not None and self.cumulative_total_tokens >= self.ceiling:
            from synthesizer.observability.events import emit_budget_exceeded
            emit_budget_exceeded(
                run_id="",  # Caller should set context; this is a safety net
                cumulative_tokens=self.cumulative_total_tokens,
                ceiling=self.ceiling,
            )
            raise TokenBudgetExceededError(
                cumulative_tokens=self.cumulative_total_tokens,
                ceiling=self.ceiling,
            )

    def check_budget_before_call(self, estimated_tokens: int = 0) -> bool:
        """Pre-check whether there's budget remaining for another call.

        Parameters
        ----------
        estimated_tokens : int
            Estimated tokens for the upcoming call.

        Returns
        -------
        bool
            True if budget is sufficient, False if it would be exceeded.
        """
        if self.ceiling is None:
            return True
        return (self.cumulative_total_tokens + estimated_tokens) < self.ceiling

    @contextmanager
    def track_section_latency(
        self,
        section_id: str,
    ) -> Generator[SectionLatencyRecord, None, None]:
        """Context manager to track per-section generation latency (NFR-01).

        Usage::

            with tracker.track_section_latency("my_section") as record:
                # ... generation code ...
            # record.latency_seconds is now set

        If latency exceeds the threshold, a latency_alert event is emitted
        and a warning is logged (NFR-01).
        """
        record = SectionLatencyRecord(
            section_id=section_id,
            start_time=time.monotonic(),
        )
        try:
            yield record
        finally:
            record.end_time = time.monotonic()
            record.latency_seconds = record.end_time - record.start_time

            if record.latency_seconds > self.latency_threshold:
                record.threshold_exceeded = True
                from synthesizer.observability.events import emit_latency_alert
                emit_latency_alert(
                    section_id=section_id,
                    latency_seconds=record.latency_seconds,
                    threshold_seconds=self.latency_threshold,
                )

            self.latency_records.append(record)

    def get_summary(self) -> Dict[str, Any]:
        """Return a summary of token accounting for reporting."""
        return {
            "cumulative_input_tokens": self.cumulative_input_tokens,
            "cumulative_output_tokens": self.cumulative_output_tokens,
            "cumulative_total_tokens": self.cumulative_total_tokens,
            "ceiling": self.ceiling,
            "total_calls": len(self.call_records),
            "calls_by_role": self._calls_by_role(),
            "sections_exceeding_latency": [
                r.section_id for r in self.latency_records
                if r.threshold_exceeded
            ],
        }

    def _calls_by_role(self) -> Dict[str, int]:
        """Count calls grouped by role."""
        counts: Dict[str, int] = {}
        for rec in self.call_records:
            counts[rec.role] = counts.get(rec.role, 0) + 1
        return counts
```

### `synthesizer/orchestrator/model_init.py`
```python
# synthesizer/orchestrator/model_init.py
"""Model availability check with graceful degradation (§5, NFR-09).

Verifies at initialization time that the configured SYNTHESIZER_MODEL
is likely available. Raises a descriptive error if not, preventing
silent failures mid-generation.

DR-16 (open): Model selection per role remains configurable.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from synthesizer.config import SYNTHESIZER_MODEL

logger = logging.getLogger(__name__)


class ModelNotAvailableError(Exception):
    """Raised when the configured model is not available (NFR-09).

    Provides a descriptive error message to help diagnose the issue.

    Attributes
    ----------
    model : str
        The model identifier that was checked.
    reason : str
        Human-readable reason for unavailability.
    """

    def __init__(self, model: str, reason: str) -> None:
        self.model = model
        self.reason = reason
        super().__init__(
            f"Model '{model}' is not available: {reason}. "
            f"Please check your SYNTHESIZER_MODEL configuration and "
            f"ANTHROPIC_API_KEY environment variable."
        )


def check_model_availability(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    *,
    probe_api: bool = False,
) -> str:
    """Verify that the configured model is available before generation (NFR-09).

    Performs checks in order:
      1. Model string is non-empty and valid
      2. ``anthropic`` package is importable
      3. ``ANTHROPIC_API_KEY`` is configured
      4. Anthropic client can be instantiated
      5. (Optional) Lightweight API probe if ``probe_api=True``

    Parameters
    ----------
    model : str, optional
        Model identifier to check. Defaults to SYNTHESIZER_MODEL from
        config. DR-16: this is configurable per role.
    api_key : str, optional
        API key to use. Defaults to ANTHROPIC_API_KEY env var.
    probe_api : bool
        If True, attempt a minimal API call to verify connectivity.
        Default False to avoid unnecessary API usage during testing.

    Returns
    -------
    str
        The validated model identifier.

    Raises
    ------
    ModelNotAvailableError
        If any check fails, with a descriptive error message indicating
        the specific failure point.
    """
    resolved_model = model or SYNTHESIZER_MODEL
    resolved_key = api_key or os.environ.get("ANTHROPIC_API_KEY")

    # Check 1: Model string validity
    if not resolved_model or not isinstance(resolved_model, str):
        raise ModelNotAvailableError(
            model=str(resolved_model),
            reason="Model identifier is empty or not a string",
        )

    if len(resolved_model.strip()) == 0:
        raise ModelNotAvailableError(
            model=resolved_model,
            reason="Model identifier is blank",
        )

    # Check 2: anthropic package importable
    try:
        import anthropic  # noqa: F401
    except ImportError:
        raise ModelNotAvailableError(
            model=resolved_model,
            reason=(
                "The 'anthropic' Python package is not installed. "
                "Install it with: pip install anthropic"
            ),
        )

    # Check 3: API key configured
    if not resolved_key:
        raise ModelNotAvailableError(
            model=resolved_model,
            reason=(
                "ANTHROPIC_API_KEY environment variable is not set. "
                "Set it to a valid API key."
            ),
        )

    # Check 4: Client instantiation
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=resolved_key)
    except Exception as exc:
        raise ModelNotAvailableError(
            model=resolved_model,
            reason=f"Failed to instantiate Anthropic client: {exc}",
        )

    # Check 5: Optional API probe
    if probe_api:
        try:
            # Minimal call to verify connectivity and model access
            response = client.messages.create(
                model=resolved_model,
                max_tokens=10,
                messages=[{"role": "user", "content": "ping"}],
            )
            logger.info(
                "Model probe successful: %s (stop_reason=%s)",
                resolved_model,
                getattr(response, "stop_reason", "unknown"),
            )
        except Exception as exc:
            raise ModelNotAvailableError(
                model=resolved_model,
                reason=f"API probe failed: {exc}",
            )

    logger.info("Model availability check passed: %s", resolved_model)
    return resolved_model


def model_for_role(
    role: str,
    *,
    model_override: Optional[str] = None,
) -> str:
    """Return the model identifier for a given LLM role (DR-16).

    DR-16 (open): Model selection per role remains configurable. Currently
    all roles use SYNTHESIZER_MODEL. This function provides the extension
    point for future per-role model differentiation.

    Parameters
    ----------
    role : str
        LLM role name: "generator", "validator", "claim_extractor",
        "summary_abstractifier".
    model_override : str, optional
        Override model for this specific role.

    Returns
    -------
    str
        Model identifier to use for this role.
    """
    if model_override:
        return model_override

    # DR-16: Currently all roles use the same model.
    # Future: read per-role config (e.g., SYNTHESIZER_VALIDATOR_MODEL)
    role_env_key = f"SYNTHESIZER_{role.upper()}_MODEL"
    env_value = os.environ.get(role_env_key)
    if env_value:
        return env_value

    return SYNTHESIZER_MODEL
```

### `synthesizer/acceptance/__init__.py`
```python
# synthesizer/acceptance/__init__.py
"""Acceptance test harness sub-package (§18, §