# synthesizer/acceptance/test_fr23_cascade_invalidation.py
"""Acceptance test for FR-23: Cascade invalidation propagation (§19).

Creates a 3-section content chain A→B→C. Finalizes all three.
Re-generates A with changed content. Asserts B transitions to INVALIDATED.
Re-processes B; asserts C transitions to INVALIDATED when B is re-finalized
with changed content.
"""

import pytest
from datetime import datetime, timezone

from synthesizer.acceptance import (
    make_section_state,
    make_claim_table,
)
from synthesizer.dag import DAG, build_generation_dag
from synthesizer.models.enums import (
    DependencyKind,
    SectionLifecycleState,
    SectionType,
)
from synthesizer.models.report_plan import DependencyEdge, ReportPlan, SectionNode
from synthesizer.models.state import SectionState
from synthesizer.orchestrator.lifecycle import (
    invalidate_content_dependents,
    transition_section_state,
)


def _make_chain_plan():
    """Create a 3-section plan with content chain: A → B → C."""
    section_a = SectionNode(
        section_id="section_a",
        title="Section A",
        section_type=SectionType.NARRATIVE_SYNTHESIS,
        depth_level=1,
        description="Root section.",
        source_queries=["query_a"],
        dependency_edges=[],
    )
    section_b = SectionNode(
        section_id="section_b",
        title="Section B",
        section_type=SectionType.NARRATIVE_SYNTHESIS,
        depth_level=1,
        description="Middle section depending on A.",
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
        description="Leaf section depending on B.",
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
        plan_id="test_plan_fr23",
        title="FR-23 Test Plan",
        version="1.0",
        sections=[section_a, section_b, section_c],
    )
    return plan


def _make_finalized_states():
    """Create section states where all three sections are FINALIZED."""
    states = {}
    for sid in ["section_a", "section_b", "section_c"]:
        ss = make_section_state(
            section_id=sid,
            state=SectionLifecycleState.FINALIZED,
        )
        ss.claim_table = make_claim_table(sid)
        ss.summary_abstract = f"Summary for {sid}"
        states[sid] = ss
    return states


class TestFR23CascadeInvalidation:
    """FR-23: Cascade invalidation propagates through content dependency chain."""

    def test_invalidate_direct_dependent_on_upstream_change(self):
        """FR-23: When A changes, B (direct dependent) is invalidated."""
        plan = _make_chain_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_finalized_states()

        # Simulate A being re-generated with changed content
        # Trigger cascade invalidation from A
        affected = invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
        )

        # B should be INVALIDATED
        assert section_states["section_b"].state == SectionLifecycleState.INVALIDATED, (
            f"B should be INVALIDATED, got {section_states['section_b'].state}"
        )

        # B's claim_table and summary_abstract should be cleared
        assert section_states["section_b"].claim_table is None, (
            "B's claim_table should be cleared on invalidation"
        )
        assert section_states["section_b"].summary_abstract is None, (
            "B's summary_abstract should be cleared on invalidation"
        )
        assert section_states["section_b"].validation_history == [], (
            "B's validation_history should be cleared on invalidation"
        )

    def test_invalidate_transitive_dependent_on_upstream_change(self):
        """FR-23: When A changes, C (transitive dependent via B) is also invalidated."""
        plan = _make_chain_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_finalized_states()

        affected = invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
        )

        # C should also be INVALIDATED (transitive cascade)
        assert section_states["section_c"].state == SectionLifecycleState.INVALIDATED, (
            f"C should be INVALIDATED, got {section_states['section_c'].state}"
        )

        # C's claim_table and summary_abstract should be cleared
        assert section_states["section_c"].claim_table is None
        assert section_states["section_c"].summary_abstract is None

    def test_affected_list_contains_both_dependents(self):
        """FR-23: The affected list contains both B and C."""
        plan = _make_chain_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_finalized_states()

        affected = invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
        )

        affected_ids = {sid for sid, _ in affected}
        assert "section_b" in affected_ids, "B should be in affected list"
        assert "section_c" in affected_ids, "C should be in affected list"
        assert "section_a" not in affected_ids, "A should NOT be in affected list"

    def test_cascade_from_middle_only_affects_downstream(self):
        """FR-23: When B changes, only C is invalidated (not A)."""
        plan = _make_chain_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_finalized_states()

        affected = invalidate_content_dependents(
            changed_section_id="section_b",
            section_states=section_states,
            generation_dag=gen_dag,
        )

        # Only C should be affected
        affected_ids = {sid for sid, _ in affected}
        assert "section_c" in affected_ids, "C should be invalidated when B changes"
        assert "section_a" not in affected_ids, "A should NOT be affected when B changes"
        assert "section_b" not in affected_ids, "B should NOT be in its own affected list"

        # A should remain FINALIZED
        assert section_states["section_a"].state == SectionLifecycleState.FINALIZED

    def test_cascade_from_leaf_affects_nothing(self):
        """FR-23: When C changes, no sections are invalidated (C has no dependents)."""
        plan = _make_chain_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_finalized_states()

        affected = invalidate_content_dependents(
            changed_section_id="section_c",
            section_states=section_states,
            generation_dag=gen_dag,
        )

        assert len(affected) == 0, "No sections should be affected when leaf C changes"
        assert section_states["section_a"].state == SectionLifecycleState.FINALIZED
        assert section_states["section_b"].state == SectionLifecycleState.FINALIZED

    def test_cascade_depth_tracking(self):
        """FR-23: Cascade depth is tracked correctly for each affected section."""
        plan = _make_chain_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_finalized_states()

        affected = invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
        )

        # B is depth 1 from A, C is depth 2 from A
        assert section_states["section_b"].cascade_depth == 1, (
            f"B cascade_depth should be 1, got {section_states['section_b'].cascade_depth}"
        )
        assert section_states["section_c"].cascade_depth == 2, (
            f"C cascade_depth should be 2, got {section_states['section_c'].cascade_depth}"
        )

    def test_re_invalidation_after_reprocessing_b(self):
        """FR-23: After B is re-processed and re-finalized, changing B invalidates C again."""
        plan = _make_chain_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_finalized_states()

        # Step 1: Invalidate from A
        invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
        )
        assert section_states["section_b"].state == SectionLifecycleState.INVALIDATED
        assert section_states["section_c"].state == SectionLifecycleState.INVALIDATED

        # Step 2: Re-process B (simulate re-generation and re-finalization)
        transition_section_state(
            section_states["section_b"], SectionLifecycleState.FINALIZED
        )
        section_states["section_b"].claim_table = make_claim_table("section_b")
        section_states["section_b"].summary_abstract = "New summary for B"

        # Step 3: Re-process C (simulate re-generation and re-finalization)
        transition_section_state(
            section_states["section_c"], SectionLifecycleState.FINALIZED
        )
        section_states["section_c"].claim_table = make_claim_table("section_c")
        section_states["section_c"].summary_abstract = "New summary for C"

        # Step 4: Now change B again — C should be invalidated
        affected = invalidate_content_dependents(
            changed_section_id="section_b",
            section_states=section_states,
            generation_dag=gen_dag,
        )

        assert section_states["section_c"].state == SectionLifecycleState.INVALIDATED, (
            "C should be INVALIDATED after B is changed again"
        )
        affected_ids = {sid for sid, _ in affected}
        assert "section_c" in affected_ids

    def test_escalated_sections_not_re_invalidated(self):
        """FR-23: Sections already in ESCALATED state are not re-processed."""
        plan = _make_chain_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_finalized_states()

        # Set B to ESCALATED
        transition_section_state(
            section_states["section_b"], SectionLifecycleState.ESCALATED
        )

        affected = invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
        )

        # B should remain ESCALATED (not re-processed)
        assert section_states["section_b"].state == SectionLifecycleState.ESCALATED, (
            "ESCALATED sections should not be re-invalidated"
        )

    def test_cascade_depth_limit_triggers_escalation(self):
        """FR-24: When cascade depth exceeds limit, section is escalated instead of invalidated."""
        plan = _make_chain_plan()
        gen_dag = build_generation_dag(plan)
        section_states = _make_finalized_states()

        # Use a very low cascade depth limit of 1
        affected = invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
            cascade_depth_limit=1,
        )

        # B at depth 1 should be INVALIDATED (within limit)
        assert section_states["section_b"].state == SectionLifecycleState.INVALIDATED, (
            f"B should be INVALIDATED at depth 1, got {section_states['section_b'].state}"
        )

        # C at depth 2 should be ESCALATED (exceeds limit of 1)
        assert section_states["section_c"].state == SectionLifecycleState.ESCALATED, (
            f"C should be ESCALATED at depth 2 (limit=1), got {section_states['section_c'].state}"
        )