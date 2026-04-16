# synthesizer/validation/graph_validation.py
"""Graph-level validation for report plans (§10.2–10.4, §8).

Provides:
  - Dangling dependency-reference detection (FR-02)
  - Content-dependency cycle detection via topological sort (FR-03)
  - Depth-level consistency validation
  - Generation DAG construction (FR-06)
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

from synthesizer.models.enums import DependencyKind
from synthesizer.models.report_plan import DependencyEdge, ReportPlan


@dataclass
class GenerationDAG:
    """Result of DAG construction (FR-06).

    Attributes
    ----------
    adjacency : dict
        Maps each section_id to the list of section_ids that depend on it
        (i.e., successors in generation order). If A must be generated
        before B, then B is in adjacency[A].
    topological_order : list
        A valid topological ordering of section_ids for generation.
    nodes : set
        All section_ids present in the DAG (including isolated nodes).
    edges : list
        The content-type DependencyEdge objects used to build the DAG.
    """

    adjacency: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))
    topological_order: List[str] = field(default_factory=list)
    nodes: Set[str] = field(default_factory=set)
    edges: List[DependencyEdge] = field(default_factory=list)


def collect_all_edges(plan: ReportPlan) -> List[DependencyEdge]:
    """Collect every DependencyEdge from every section in the plan.

    Parameters
    ----------
    plan : ReportPlan
        Validated report plan.

    Returns
    -------
    list of DependencyEdge
        Flat list of all edges across all sections.
    """
    all_edges: List[DependencyEdge] = []
    for section in plan.sections:
        all_edges.extend(section.dependency_edges)
    return all_edges


def _get_section_id_set(plan: ReportPlan) -> Set[str]:
    """Return the set of all declared section_ids."""
    return {section.section_id for section in plan.sections}


# ---------------------------------------------------------------------------
# FR-02  Dangling dependency-reference detection
# ---------------------------------------------------------------------------

def validate_dependency_references(plan: ReportPlan) -> None:
    """Validate that every section_id in dependency_edges exists (FR-02).

    Checks both ``source_section_id`` and ``target_section_id`` for every
    edge on every section.

    Parameters
    ----------
    plan : ReportPlan
        Parsed (but not yet cross-validated) report plan.

    Raises
    ------
    ValueError
        If any referenced section_id does not exist as a declared section,
        with a message naming the dangling reference(s).
    """
    declared_ids = _get_section_id_set(plan)
    dangling: List[str] = []

    for section in plan.sections:
        for edge in section.dependency_edges:
            if edge.source_section_id not in declared_ids:
                dangling.append(
                    f"source_section_id '{edge.source_section_id}' "
                    f"(in edge on section '{section.section_id}')"
                )
            if edge.target_section_id not in declared_ids:
                dangling.append(
                    f"target_section_id '{edge.target_section_id}' "
                    f"(in edge on section '{section.section_id}')"
                )

    if dangling:
        details = "; ".join(dangling)
        raise ValueError(
            f"Dangling dependency reference(s) — the following section_ids "
            f"are referenced in dependency_edges but do not exist as "
            f"declared sections: {details}"
        )


# ---------------------------------------------------------------------------
# FR-03  Content-dependency cycle detection
# ---------------------------------------------------------------------------

def validate_no_content_cycles(plan: ReportPlan) -> None:
    """Validate that CONTENT-type edges contain no cycles (FR-03).

    Uses Kahn's algorithm (BFS topological sort) on content-type edges
    only. Non-content edge types (REFERENCE, THEMATIC, SOURCE) are
    excluded — they do not impose generation-ordering constraints (§8).

    Parameters
    ----------
    plan : ReportPlan
        Report plan that has already passed reference validation (FR-02).

    Raises
    ------
    ValueError
        If a cycle is detected among content-type edges, with a message
        identifying the section_ids involved in the cycle.
    """
    all_edges = collect_all_edges(plan)
    content_edges = [e for e in all_edges if e.kind == DependencyKind.CONTENT]

    if not content_edges:
        return  # No content edges → no cycle possible.

    declared_ids = _get_section_id_set(plan)

    # Build adjacency for content edges:
    #   target → source  (upstream → downstream in generation order)
    # i.e., target_section_id must be generated before source_section_id.
    adjacency: Dict[str, List[str]] = defaultdict(list)
    in_degree: Dict[str, int] = {sid: 0 for sid in declared_ids}

    for edge in content_edges:
        adjacency[edge.target_section_id].append(edge.source_section_id)
        in_degree[edge.source_section_id] = (
            in_degree.get(edge.source_section_id, 0) + 1
        )

    # Kahn's algorithm
    queue: deque[str] = deque(
        sid for sid, deg in in_degree.items() if deg == 0
    )
    visited_count = 0

    while queue:
        node = queue.popleft()
        visited_count += 1
        for successor in adjacency.get(node, []):
            in_degree[successor] -= 1
            if in_degree[successor] == 0:
                queue.append(successor)

    if visited_count < len(declared_ids):
        # Some nodes were never visited → cycle exists among them.
        cycle_members = sorted(
            sid for sid, deg in in_degree.items() if deg > 0
        )
        raise ValueError(
            f"Content-dependency cycle detected among sections: "
            f"{cycle_members}. The dependency graph must be acyclic for "
            f"content-type edges (§8.1, FR-03)."
        )


# ---------------------------------------------------------------------------
# Depth-level consistency
# ---------------------------------------------------------------------------

def validate_depth_levels(plan: ReportPlan) -> None:
    """Validate that each section's depth_level equals its ancestor chain length.

    The ancestor chain is computed by following parent_id links.
    A top-level section (parent_id is None) must have depth_level 0.

    Parameters
    ----------
    plan : ReportPlan
        Report plan to validate.

    Raises
    ------
    ValueError
        If any section's depth_level does not match its computed ancestor
        chain length, or if a parent_id references a non-existent section.
    """
    id_to_section = {s.section_id: s for s in plan.sections}
    errors: List[str] = []

    for section in plan.sections:
        # Compute ancestor chain length
        depth = 0
        current_parent = section.parent_id
        visited: Set[str] = {section.section_id}

        while current_parent is not None:
            if current_parent not in id_to_section:
                errors.append(
                    f"Section '{section.section_id}' references "
                    f"parent_id '{current_parent}' which does not exist."
                )
                break
            if current_parent in visited:
                errors.append(
                    f"Section '{section.section_id}' has a circular "
                    f"parent chain involving '{current_parent}'."
                )
                break
            visited.add(current_parent)
            depth += 1
            current_parent = id_to_section[current_parent].parent_id

        if section.depth_level != depth and not errors:
            errors.append(
                f"Section '{section.section_id}' has depth_level="
                f"{section.depth_level} but its ancestor chain length is "
                f"{depth}."
            )

    if errors:
        raise ValueError(
            "Depth-level consistency check failed: " + "; ".join(errors)
        )


# ---------------------------------------------------------------------------
# FR-06  Generation DAG construction
# ---------------------------------------------------------------------------

def build_generation_dag(plan: ReportPlan) -> GenerationDAG:
    """Build the generation DAG from content-type dependency edges (FR-06).

    The DAG encodes generation ordering: if section B has a content
    dependency on section A, then A must be generated (and finalized)
    before B. In the adjacency representation, A → B means "A is a
    prerequisite of B".

    Parameters
    ----------
    plan : ReportPlan
        Report plan that has already passed validation (FR-02, FR-03).

    Returns
    -------
    GenerationDAG
        DAG with adjacency, topological order, node set, and edge list.
    """
    declared_ids = _get_section_id_set(plan)
    all_edges = collect_all_edges(plan)
    content_edges = [e for e in all_edges if e.kind == DependencyKind.CONTENT]

    adjacency: Dict[str, List[str]] = defaultdict(list)
    in_degree: Dict[str, int] = {sid: 0 for sid in declared_ids}

    for edge in content_edges:
        # target (upstream) → source (downstream)
        adjacency[edge.target_section_id].append(edge.source_section_id)
        in_degree[edge.source_section_id] = (
            in_degree.get(edge.source_section_id, 0) + 1
        )

    # Topological sort (Kahn's algorithm) — deterministic via sorted queue
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

    dag = GenerationDAG(
        adjacency=dict(adjacency),
        topological_order=topo_order,
        nodes=declared_ids,
        edges=content_edges,
    )

    return dag


def build_finalization_dag(
    plan: ReportPlan,
) -> Tuple[Dict[str, List[str]], List[str]]:
    """Build the finalization DAG (FR-07) — content + reference edges."""
    declared_ids = _get_section_id_set(plan)
    all_edges = collect_all_edges(plan)
    fin_edges = [
        e
        for e in all_edges
        if e.kind in (DependencyKind.CONTENT, DependencyKind.REFERENCE)
    ]

    adjacency: Dict[str, List[str]] = defaultdict(list)
    in_degree: Dict[str, int] = {sid: 0 for sid in declared_ids}

    for edge in fin_edges:
        adjacency[edge.target_section_id].append(edge.source_section_id)
        in_degree[edge.source_section_id] = (
            in_degree.get(edge.source_section_id, 0) + 1
        )

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

    return (dict(adjacency), topo_order)