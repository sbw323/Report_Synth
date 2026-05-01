# synthesizer/acceptance/test_fr08_dependency_ordering.py
"""Acceptance test for FR-08: Content dependency ordering enforcement (§19).

Creates a 3-section plan with content dependencies A→B→C.
Verifies that:
  - C cannot be processed before A is finalized (stays QUEUED)
  - After finalizing A, B can be processed
  - After finalizing B, C can be processed
  - Correct topological ordering is enforced
"""

import pytest
from datetime import datetime, timezone

from synthesizer.acceptance import (
    make_section_node,
    make_section_state,
    make_dependency_edge,
)
from synthesizer.dag import DAG, build_generation_dag, iter_topological
from synthesizer.models.enums import (
    DependencyKind,
    SectionLifecycleState,
    SectionType,
)
from synthesizer.models.report_plan import DependencyEdge, ReportPlan, SectionNode
from synthesizer.models.state import SectionState
from synthesizer.orchestrator.lifecycle import (
    check_generation_prerequisites,
    transition_section_state,
)


def _make_three_section_plan():
    """Create a 3-section plan with content dependencies: A → B → C.

    A has no dependencies.
    B depends on A (content).
    C depends on B (content).
    """
    section_a = SectionNode(
        section_id="section_a",
        title="Section A",
        section_type=SectionType.NARRATIVE_SYNTHESIS,
        depth_level=1,
        description="First section with no dependencies.",
        source_queries=["query_a"],
        dependency_edges=[],
    )
    section_b = SectionNode(
        section_id="section_b",
        title="Section B",
        section_type=SectionType.NARRATIVE_SYNTHESIS,
        depth_level=1,
        description="Second section depending on A.",
        source_queries=["query_b"],
        dependency_edges=[
            DependencyEdge(
                source_section_id="section_b",
                target_section_id="section_a",
                kind=DependencyKind.CONTENT,
            ),
        ],
    )
    section_c = SectionNode(
        section_id="section_c",
        title="Section C",
        section_type=SectionType.NARRATIVE_SYNTHESIS,
        depth_level=1,
        description="Third section depending on B.",
        source_queries=["query_c"],
        dependency_edges=[
            DependencyEdge(
                source_section_id="section_c",
                target_section_id="section_b",
                kind=DependencyKind.CONTENT,
            ),
        ],
    )

    plan = ReportPlan(
        plan_id="test_plan_fr08",
        title="FR-08 Test Plan",
        version="1.0",
        sections=[section_a, section_b, section_c],
    )
    return plan


def _make_section_states(plan):
    """Create initial QUEUED section states for all sections in the plan."""
    states = {}
    for section in plan.sections:
        states[section.section_id] = make_section_state(
            section_id=section.section_id,
            state=SectionLifecycleState.QUEUED,
        )
    return states


class TestFR08DependencyOrdering:
    """FR-08: Content dependency ordering enforcement."""

    def test_topological_order_respects_dependencies(self):
        """FR-08: Topological order places A before B before C."""
        plan = _make_three_section_plan()
        gen_dag = build_generation_dag(plan)
        topo_order = iter_topological(gen_dag)

        idx_a = topo_order.index("section_a")
        idx_b = topo_order.index("section_b")
        idx_c = topo_order.index("section_c")

        assert idx_a < idx_b, "A must come before B in topological order"
        assert idx_b < idx_c, "B must come before C in topological order"

    def test_c_cannot_generate_before_a_finalized(self):
        """FR-08: C remains QUEUED when A is not finalized."""
        plan = _make_three_section_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_section_states(plan)

        # All sections are QUEUED — C's prerequisite (B) is not finalized
        can_generate_c = check_generation_prerequisites(
            "section_c", section_states, gen_dag
        )
        assert can_generate_c is False, "C should not be processable when B is QUEUED"

        # B's prerequisite (A) is also not finalized
        can_generate_b = check_generation_prerequisites(
            "section_b", section_states, gen_dag
        )
        assert can_generate_b is False, "B should not be processable when A is QUEUED"

    def test_a_can_generate_with_no_dependencies(self):
        """FR-08: A can generate immediately (no content dependencies)."""
        plan = _make_three_section_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_section_states(plan)

        can_generate_a = check_generation_prerequisites(
            "section_a", section_states, gen_dag
        )
        assert can_generate_a is True, "A should be processable with no dependencies"

    def test_b_can_generate_after_a_finalized(self):
        """FR-08: B can generate after A is finalized."""
        plan = _make_three_section_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_section_states(plan)

        # Finalize A
        transition_section_state(
            section_states["section_a"], SectionLifecycleState.FINALIZED
        )

        can_generate_b = check_generation_prerequisites(
            "section_b", section_states, gen_dag
        )
        assert can_generate_b is True, "B should be processable after A is finalized"

        # C still cannot generate (B is not finalized)
        can_generate_c = check_generation_prerequisites(
            "section_c", section_states, gen_dag
        )
        assert can_generate_c is False, "C should not be processable when B is not finalized"

    def test_c_can_generate_after_b_finalized(self):
        """FR-08: C can generate after both A and B are finalized."""
        plan = _make_three_section_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_section_states(plan)

        # Finalize A and B
        transition_section_state(
            section_states["section_a"], SectionLifecycleState.FINALIZED
        )
        transition_section_state(
            section_states["section_b"], SectionLifecycleState.FINALIZED
        )

        can_generate_c = check_generation_prerequisites(
            "section_c", section_states, gen_dag
        )
        assert can_generate_c is True, "C should be processable after A and B are finalized"

    def test_stable_state_also_satisfies_prerequisites(self):
        """FR-08: STABLE state also satisfies content dependency prerequisites."""
        plan = _make_three_section_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_section_states(plan)

        # Set A to STABLE instead of FINALIZED
        transition_section_state(
            section_states["section_a"], SectionLifecycleState.STABLE
        )

        can_generate_b = check_generation_prerequisites(
            "section_b", section_states, gen_dag
        )
        assert can_generate_b is True, "B should be processable when A is STABLE"

    def test_escalated_state_does_not_satisfy_prerequisites(self):
        """FR-08: ESCALATED state does NOT satisfy content dependency prerequisites."""
        plan = _make_three_section_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_section_states(plan)

        # Set A to ESCALATED
        transition_section_state(
            section_states["section_a"], SectionLifecycleState.ESCALATED
        )

        can_generate_b = check_generation_prerequisites(
            "section_b", section_states, gen_dag
        )
        assert can_generate_b is False, "B should NOT be processable when A is ESCALATED"

    def test_full_sequential_processing_order(self):
        """FR-08: Full sequential processing respects A→B→C ordering."""
        plan = _make_three_section_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_section_states(plan)
        topo_order = iter_topological(gen_dag)

        processed_order = []

        for section_id in topo_order:
            can_generate = check_generation_prerequisites(
                section_id, section_states, gen_dag
            )
            if can_generate:
                processed_order.append(section_id)
                # Simulate processing: transition to FINALIZED
                transition_section_state(
                    section_states[section_id],
                    SectionLifecycleState.FINALIZED,
                )

        assert processed_order == ["section_a", "section_b", "section_c"], (
            f"Expected processing order [A, B, C], got {processed_order}"
        )

    def test_unknown_predecessor_blocks_generation(self):
        """FR-08: If a predecessor section_id is unknown, prerequisites are not met."""
        plan = _make_three_section_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_section_states(plan)

        # Remove section_a from states to simulate unknown predecessor
        del section_states["section_a"]

        can_generate_b = check_generation_prerequisites(
            "section_b", section_states, gen_dag
        )
        assert can_generate_b is False, "B should not be processable when A is unknown"