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