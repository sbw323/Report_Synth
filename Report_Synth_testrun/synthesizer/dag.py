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