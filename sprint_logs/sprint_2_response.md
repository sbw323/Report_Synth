Looking at the sprint requirements, I need to implement:
1. SectionState/RunState models (§10.12-10.13)
2. DAG construction (generation + finalization)
3. Lifecycle precondition checks and cascade logic
4. Checkpoint persistence/resume
5. Filesystem scaffolding
6. Supporting models needed by SectionState (ValidationResult, ClaimTable)

Let me implement all artifacts systematically.

### `synthesizer/models/validation_models.py`
```python
# synthesizer/models/validation_models.py
"""Validation result Pydantic models (§10.10).

These models are required by SectionState (§10.12) which stores
validation_history: List[ValidationResult].

Supports: FR-14 through FR-19.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.enums import ValidationLayer, ViolationSeverity


class Violation(BaseModel):
    """Single validation violation (§10.10).

    Supports: FR-14, FR-16, FR-18.
    """

    model_config = ConfigDict(extra="forbid")

    rule: str = Field(
        ...,
        min_length=1,
        description="Rule identifier (e.g., 'word_count_max', 'tone_formal').",
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Human-readable description of the violation.",
    )
    severity: ViolationSeverity = Field(
        ...,
        description="Error or warning.",
    )
    location: Optional[str] = Field(
        default=None,
        description="Character offset or field path where violation occurs.",
    )


class ValidationResult(BaseModel):
    """Output of a single validation pass (§10.10).

    See §12 for layer semantics.
    Supports: FR-14 through FR-19.
    """

    model_config = ConfigDict(extra="forbid")

    layer: ValidationLayer = Field(
        ...,
        description="Which validation layer produced this result.",
    )
    passed: bool = Field(
        ...,
        description="Whether validation passed.",
    )
    attempt: int = Field(
        ...,
        ge=1,
        description="Attempt number within this layer.",
    )
    violations: List[Violation] = Field(
        default_factory=list,
        description="Violations found (empty if passed).",
    )
    suggested_fix: Optional[str] = Field(
        default=None,
        description="LLM-suggested fix text (Layer 3 only).",
    )
```

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

### `synthesizer/models/state.py`
```python
# synthesizer/models/state.py
"""Section and run state Pydantic models (§10.12, §10.13).

Supports: FR-08, FR-19, FR-23, FR-24, FR-27, NFR-03.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.claims import ClaimTable
from synthesizer.models.enums import SectionLifecycleState
from synthesizer.models.report_plan import DependencyEdge
from synthesizer.models.validation_models import ValidationResult


def _now_iso() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


class SectionState(BaseModel):
    """Per-section lifecycle state tracked by the orchestrator (§10.12).

    See §11 for state transitions.
    Supports: FR-08, FR-19, FR-23, FR-27.
    """

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(
        ...,
        description="Unique section identifier.",
    )
    state: SectionLifecycleState = Field(
        ...,
        description="Current lifecycle state.",
    )
    version: int = Field(
        default=1,
        ge=1,
        description="Draft version counter. Increments on each re-generation.",
    )
    last_transition_timestamp: str = Field(
        default_factory=_now_iso,
        description="ISO 8601 timestamp of last state change.",
    )
    validation_history: List[ValidationResult] = Field(
        default_factory=list,
        description="Cumulative validation results.",
    )
    claim_table: Optional[ClaimTable] = Field(
        default=None,
        description="Current claim table (None until extraction).",
    )
    summary_abstract: Optional[str] = Field(
        default=None,
        description="2-3 sentence summary (None until abstraction).",
    )
    retry_counters: Dict[str, int] = Field(
        default_factory=dict,
        description="Maps layer name → current retry count.",
    )
    cascade_depth: int = Field(
        default=0,
        ge=0,
        description="Current cascade depth for this section.",
    )


class RunState(BaseModel):
    """Checkpoint object for the full orchestrator run (§10.13).

    Persisted to disk after every checkpoint-worthy state transition (§11).
    Supports: NFR-03, FR-24.
    """

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(
        ...,
        description="Unique run identifier (UUID).",
    )
    report_plan_version: str = Field(
        ...,
        description="Version of the report plan being executed.",
    )
    section_states: Dict[str, SectionState] = Field(
        ...,
        description="Maps section_id → SectionState.",
    )
    generation_dag_edges: List[DependencyEdge] = Field(
        ...,
        description="Content-dependency edges for generation ordering.",
    )
    finalization_dag_edges: List[DependencyEdge] = Field(
        ...,
        description="Content + reference edges for finalization ordering.",
    )
    started_at: str = Field(
        ...,
        description="ISO 8601 timestamp.",
    )
    last_checkpoint_at: str = Field(
        ...,
        description="ISO 8601 timestamp of last checkpoint write.",
    )
    cumulative_input_tokens: int = Field(
        default=0,
        ge=0,
        description="Total input tokens consumed across all LLM calls.",
    )
    cumulative_output_tokens: int = Field(
        default=0,
        ge=0,
        description="Total output tokens consumed across all LLM calls.",
    )
```

### `synthesizer/dag.py`
```python
# synthesizer/dag.py
"""DAG construction for generation and finalization ordering (§8, §11).

Provides:
  - Generation DAG: content edges only (FR-06)
  - Finalization DAG: content + reference edges (FR-07)
  - Topological-order iterators
  - Predecessor/successor lookup helpers

The generation DAG determines which sections can begin generation;
the finalization DAG determines which sections can finalize.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List, Set

from synthesizer.models.enums import DependencyKind
from synthesizer.models.report_plan import DependencyEdge, ReportPlan


@dataclass
class DAG:
    """Directed acyclic graph over section_ids.

    Attributes
    ----------
    adjacency : dict
        Maps each section_id to a list of its *successors* (dependents).
        If A must precede B, then B is in adjacency[A].
    reverse_adjacency : dict
        Maps each section_id to a list of its *predecessors* (dependencies).
        If B depends on A, then A is in reverse_adjacency[B].
    topological_order : list
        A deterministic topological ordering of all section_ids.
    nodes : frozenset
        All section_ids in the DAG (including isolated nodes).
    edges : list
        The DependencyEdge objects used to build this DAG.
    """

    adjacency: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))
    reverse_adjacency: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))
    topological_order: List[str] = field(default_factory=list)
    nodes: FrozenSet[str] = field(default_factory=frozenset)
    edges: List[DependencyEdge] = field(default_factory=list)

    def predecessors(self, section_id: str) -> List[str]:
        """Return the list of direct predecessors (upstream deps) for a section."""
        return list(self.reverse_adjacency.get(section_id, []))

    def successors(self, section_id: str) -> List[str]:
        """Return the list of direct successors (downstream dependents) for a section."""
        return list(self.adjacency.get(section_id, []))

    def has_predecessors(self, section_id: str) -> bool:
        """Return True if the section has any predecessors in this DAG."""
        return len(self.reverse_adjacency.get(section_id, [])) > 0


def _collect_all_edges(plan: ReportPlan) -> List[DependencyEdge]:
    """Collect every DependencyEdge from every section in the plan."""
    edges: List[DependencyEdge] = []
    for section in plan.sections:
        edges.extend(section.dependency_edges)
    return edges


def _get_section_ids(plan: ReportPlan) -> Set[str]:
    """Return the set of all declared section_ids."""
    return {section.section_id for section in plan.sections}


def _build_dag(
    plan: ReportPlan,
    edge_kinds: Set[DependencyKind],
) -> DAG:
    """Internal DAG builder for a given set of edge kinds.

    Parameters
    ----------
    plan : ReportPlan
        Validated report plan (must pass FR-02 and FR-03 checks).
    edge_kinds : set of DependencyKind
        Which edge kinds to include.

    Returns
    -------
    DAG
        Constructed DAG with adjacency, reverse adjacency, topological
        order, nodes, and filtered edges.
    """
    declared_ids = _get_section_ids(plan)
    all_edges = _collect_all_edges(plan)
    filtered_edges = [e for e in all_edges if e.kind in edge_kinds]

    adjacency: Dict[str, List[str]] = defaultdict(list)
    reverse_adjacency: Dict[str, List[str]] = defaultdict(list)
    in_degree: Dict[str, int] = {sid: 0 for sid in declared_ids}

    for edge in filtered_edges:
        # target_section_id (upstream) → source_section_id (downstream)
        # The upstream must be generated/finalized before the downstream.
        adjacency[edge.target_section_id].append(edge.source_section_id)
        reverse_adjacency[edge.source_section_id].append(edge.target_section_id)
        in_degree[edge.source_section_id] = (
            in_degree.get(edge.source_section_id, 0) + 1
        )

    # Kahn's algorithm — deterministic via sorted initial queue and sorted successors
    queue: deque[str] = deque(
        sorted(sid for sid, deg in in_degree.items() if deg == 0)
    )
    topo_order: List[str] = []

    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for successor in sorted(adjacency.get(node, [])):
            in_degree[successor] -= 1
            if in_degree[successor] == 0:
                queue.append(successor)

    return DAG(
        adjacency=dict(adjacency),
        reverse_adjacency=dict(reverse_adjacency),
        topological_order=topo_order,
        nodes=frozenset(declared_ids),
        edges=filtered_edges,
    )


def build_generation_dag(plan: ReportPlan) -> DAG:
    """Build the generation DAG from content-type edges only (FR-06).

    The generation DAG encodes generation ordering: if section B has
    a content dependency on section A, then A must be generated (and
    finalized) before B can begin generation.

    Parameters
    ----------
    plan : ReportPlan
        Validated report plan (post FR-02, FR-03).

    Returns
    -------
    DAG
        Generation DAG with content edges only.
    """
    return _build_dag(plan, {DependencyKind.CONTENT})


def build_finalization_dag(plan: ReportPlan) -> DAG:
    """Build the finalization DAG from content + reference edges (FR-07).

    The finalization DAG includes both CONTENT and REFERENCE edges.
    A section cannot finalize until all of its content *and* reference
    predecessors have finalized.

    Parameters
    ----------
    plan : ReportPlan
        Validated report plan (post FR-02, FR-03).

    Returns
    -------
    DAG
        Finalization DAG with content + reference edges.
    """
    return _build_dag(plan, {DependencyKind.CONTENT, DependencyKind.REFERENCE})


def iter_topological(dag: DAG) -> List[str]:
    """Return the topological order of the DAG (FR-06).

    This is a convenience accessor; the order is computed during
    DAG construction and cached.

    Parameters
    ----------
    dag : DAG
        A constructed DAG.

    Returns
    -------
    list of str
        Section IDs in topological generation/finalization order.
    """
    return list(dag.topological_order)
```

### `synthesizer/orchestrator/__init__.py`
```python
# synthesizer/orchestrator/__init__.py
"""Orchestrator sub-package for lifecycle, checkpoint, and runtime control."""
```

### `synthesizer/orchestrator/lifecycle.py`
```python
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