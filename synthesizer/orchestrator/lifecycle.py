# synthesizer/orchestrator/lifecycle.py
"""Lifecycle precondition checks, state transitions, and cascade logic (§11).

Provides:
  - Generation prerequisite check (FR-08): content deps must be finalized
  - Finalization prerequisite check (FR-07): content + reference deps finalized
  - State transition with timestamp update
  - Cascade invalidation with depth limit (FR-23, FR-24)
  - Reference-change re-validation trigger (FR-25)
  - Assembly readiness pre-check (FR-27)

All functions operate on SectionState dictionaries and DAG objects;
they do not perform I/O or LLM calls.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from synthesizer.config import CASCADE_DEPTH_LIMIT
from synthesizer.dag import DAG
from synthesizer.models.enums import SectionLifecycleState
from synthesizer.models.state import SectionState


# States that indicate a section has completed its content generation
# and can serve as a fulfilled prerequisite.
_FINALIZED_STATES: frozenset[SectionLifecycleState] = frozenset({
    SectionLifecycleState.FINALIZED,
    SectionLifecycleState.STABLE,
})

# States acceptable for final assembly (FR-27):
# finalized, stable, or escalated (human-reviewed).
_ASSEMBLY_READY_STATES: frozenset[SectionLifecycleState] = frozenset({
    SectionLifecycleState.FINALIZED,
    SectionLifecycleState.STABLE,
    SectionLifecycleState.ESCALATED,
})


def _now_iso() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# FR-08  Generation prerequisite check
# ---------------------------------------------------------------------------

def check_generation_prerequisites(
    section_id: str,
    section_states: Dict[str, SectionState],
    generation_dag: DAG,
) -> bool:
    """Check whether all content-dependency predecessors are finalized (FR-08).

    A section cannot transition from ``queued`` to ``generating`` until
    every section it has a content dependency on has reached ``finalized``
    or ``stable`` state (§8.1, §11.2).

    Parameters
    ----------
    section_id : str
        The section to check.
    section_states : dict
        Maps section_id → SectionState.
    generation_dag : DAG
        The generation DAG (content edges only).

    Returns
    -------
    bool
        True if all content predecessors are finalized/stable, False otherwise.
    """
    predecessors = generation_dag.predecessors(section_id)
    if not predecessors:
        return True  # No content dependencies → prerequisites trivially met.

    for pred_id in predecessors:
        pred_state = section_states.get(pred_id)
        if pred_state is None:
            return False  # Unknown section → not met.
        if pred_state.state not in _FINALIZED_STATES:
            return False

    return True


# ---------------------------------------------------------------------------
# FR-07  Finalization prerequisite check
# ---------------------------------------------------------------------------

def check_finalization_prerequisites(
    section_id: str,
    section_states: Dict[str, SectionState],
    finalization_dag: DAG,
) -> bool:
    """Check whether all finalization predecessors are finalized (FR-07).

    A section cannot transition to ``finalized`` until all of its
    content *and* reference predecessors have reached ``finalized`` or
    ``stable`` state (§8.2, §11).

    Parameters
    ----------
    section_id : str
        The section to check.
    section_states : dict
        Maps section_id → SectionState.
    finalization_dag : DAG
        The finalization DAG (content + reference edges).

    Returns
    -------
    bool
        True if all finalization predecessors are finalized/stable.
    """
    predecessors = finalization_dag.predecessors(section_id)
    if not predecessors:
        return True

    for pred_id in predecessors:
        pred_state = section_states.get(pred_id)
        if pred_state is None:
            return False
        if pred_state.state not in _FINALIZED_STATES:
            return False

    return True


# ---------------------------------------------------------------------------
# State transitions
# ---------------------------------------------------------------------------

def transition_section_state(
    section_state: SectionState,
    new_state: SectionLifecycleState,
    *,
    timestamp: Optional[str] = None,
) -> SectionState:
    """Transition a section to a new lifecycle state (§11).

    Updates ``state`` and ``last_transition_timestamp``. Does NOT
    perform prerequisite checks — callers must check prerequisites
    before calling.

    Parameters
    ----------
    section_state : SectionState
        The current section state (mutated in-place and returned).
    new_state : SectionLifecycleState
        Target state.
    timestamp : str, optional
        ISO 8601 timestamp; defaults to current UTC time.

    Returns
    -------
    SectionState
        The updated section state (same object).
    """
    section_state.state = new_state
    section_state.last_transition_timestamp = timestamp or _now_iso()
    return section_state


# ---------------------------------------------------------------------------
# FR-23, FR-24  Cascade invalidation
# ---------------------------------------------------------------------------

def invalidate_content_dependents(
    changed_section_id: str,
    section_states: Dict[str, SectionState],
    generation_dag: DAG,
    cascade_depth_limit: int = CASCADE_DEPTH_LIMIT,
    *,
    _current_depth: int = 0,
) -> List[Tuple[str, SectionLifecycleState]]:
    """Invalidate all transitive content dependents up to the cascade depth limit.

    Performs a BFS over the generation DAG starting from
    ``changed_section_id``. Each level of dependents gets an
    incremented cascade_depth. When cascade_depth would exceed
    ``cascade_depth_limit``, the section transitions to ``escalated``
    instead of ``invalidated`` (FR-24, §11.1).

    Sections already in ``escalated`` state are not re-processed.

    On invalidation (§11.1 finalized → invalidated actions):
      - claim_table cleared to None
      - summary_abstract cleared to None
      - validation_history cleared

    Parameters
    ----------
    changed_section_id : str
        The section whose content changed.
    section_states : dict
        Maps section_id → SectionState. Mutated in-place.
    generation_dag : DAG
        The generation DAG (content edges only).
    cascade_depth_limit : int
        Maximum cascade depth (DR-04, default from config).
    _current_depth : int
        Internal — current depth in the cascade traversal.

    Returns
    -------
    list of (section_id, new_state) tuples
        All sections affected by the cascade and their new states.
    """
    affected: List[Tuple[str, SectionLifecycleState]] = []
    queue: deque[Tuple[str, int]] = deque()

    # Seed with the direct dependents of the changed section
    for dep_id in generation_dag.successors(changed_section_id):
        queue.append((dep_id, _current_depth + 1))

    visited: set[str] = {changed_section_id}

    while queue:
        dep_id, depth = queue.popleft()
        if dep_id in visited:
            continue
        visited.add(dep_id)

        dep_state = section_states.get(dep_id)
        if dep_state is None:
            continue

        # Skip if already escalated — terminal state, no further processing
        if dep_state.state == SectionLifecycleState.ESCALATED:
            continue

        ts = _now_iso()

        if depth > cascade_depth_limit:
            # FR-24: cascade depth exceeded → escalate
            dep_state.state = SectionLifecycleState.ESCALATED
            dep_state.cascade_depth = depth
            dep_state.last_transition_timestamp = ts
            affected.append((dep_id, SectionLifecycleState.ESCALATED))
            # Do NOT enqueue further dependents — escalation terminates
        else:
            # FR-23: invalidate the dependent
            dep_state.state = SectionLifecycleState.INVALIDATED
            dep_state.cascade_depth = depth
            dep_state.claim_table = None
            dep_state.summary_abstract = None
            dep_state.validation_history = []
            dep_state.last_transition_timestamp = ts
            affected.append((dep_id, SectionLifecycleState.INVALIDATED))

            # Enqueue transitive dependents for further propagation
            for next_dep_id in generation_dag.successors(dep_id):
                if next_dep_id not in visited:
                    queue.append((next_dep_id, depth + 1))

    return affected


# ---------------------------------------------------------------------------
# FR-25  Reference-change re-validation trigger
# ---------------------------------------------------------------------------

def get_reference_dependents(
    changed_section_id: str,
    finalization_dag: DAG,
    generation_dag: DAG,
) -> List[str]:
    """Identify sections that need re-validation (not re-generation) on reference change.

    When an upstream reference dependency changes (e.g., heading change),
    sections with a reference dependency on it should be re-validated
    but NOT re-generated (FR-25, §8.2).

    Returns the section_ids that have a reference-only dependency on
    ``changed_section_id`` (i.e., they appear in the finalization DAG
    but NOT in the generation DAG as dependents of changed_section_id).

    Parameters
    ----------
    changed_section_id : str
        The section whose reference-relevant content changed.
    finalization_dag : DAG
        The finalization DAG (content + reference edges).
    generation_dag : DAG
        The generation DAG (content edges only).

    Returns
    -------
    list of str
        Section IDs that need reference re-validation only.
    """
    fin_dependents = set(finalization_dag.successors(changed_section_id))
    gen_dependents = set(generation_dag.successors(changed_section_id))

    # Reference-only dependents: in finalization DAG but NOT generation DAG
    return sorted(fin_dependents - gen_dependents)


def mark_sections_for_reference_revalidation(
    section_ids: List[str],
    section_states: Dict[str, SectionState],
) -> List[str]:
    """Mark sections for reference re-validation without changing their state.

    FR-25: On upstream reference change, re-validate reference pointers
    only — do NOT re-generate. The section state does not change if
    pointers are still valid.

    This function returns the list of sections that need re-validation.
    Actual re-validation logic is deferred to the validation sprint.

    Parameters
    ----------
    section_ids : list of str
        Sections to flag for re-validation.
    section_states : dict
        Maps section_id → SectionState.

    Returns
    -------
    list of str
        Section IDs marked for re-validation.
    """
    flagged: List[str] = []
    for sid in section_ids:
        ss = section_states.get(sid)
        if ss is not None and ss.state in _FINALIZED_STATES:
            flagged.append(sid)
    return flagged


# ---------------------------------------------------------------------------
# FR-27  Assembly readiness pre-check
# ---------------------------------------------------------------------------

class AssemblyNotReadyError(Exception):
    """Raised when assembly is attempted but sections are not ready (FR-27).

    Attributes
    ----------
    non_ready_sections : list of (section_id, state) tuples
        Sections that are not in an assembly-ready state.
    """

    def __init__(self, non_ready_sections: List[Tuple[str, SectionLifecycleState]]) -> None:
        self.non_ready_sections = non_ready_sections
        details = ", ".join(
            f"'{sid}' (state={state.value})" for sid, state in non_ready_sections
        )
        super().__init__(
            f"Assembly blocked: the following section(s) are not in a "
            f"finalized/stable/escalated state: {details}"
        )


def check_assembly_readiness(
    section_states: Dict[str, SectionState],
) -> bool:
    """Check whether all sections are ready for final assembly (FR-27).

    All sections must be in ``finalized``, ``stable``, or ``escalated``
    state before assembly can begin.

    Parameters
    ----------
    section_states : dict
        Maps section_id → SectionState.

    Returns
    -------
    bool
        True if all sections are assembly-ready.

    Raises
    ------
    AssemblyNotReadyError
        If any section is not in an assembly-ready state, with a
        descriptive message identifying the