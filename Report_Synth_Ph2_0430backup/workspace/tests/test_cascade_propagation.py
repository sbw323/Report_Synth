# tests/test_cascade_propagation.py
"""Tests for cascade propagation logic (FR-23, FR-24, FR-25).

Covers:
  - 3-section content chain: root changes → dependents invalidated (FR-23)
  - Cascade stops at CASCADE_DEPTH_LIMIT (FR-24)
  - Reference dep change → re-validate only, no re-generation (FR-25)
"""

import pytest
from datetime import datetime, timezone

from synthesizer.models.enums import (
    DependencyKind,
    SectionLifecycleState,
    SectionType,
)
from synthesizer.models.report_plan import DependencyEdge, ReportPlan, SectionNode
from synthesizer.models.state import RunState, SectionState
from synthesizer.dag import DAG, build_generation_dag, build_finalization_dag
from synthesizer.orchestrator.lifecycle import (
    invalidate_content_dependents,
    check_generation_prerequisites,
    get_reference_dependents,
    mark_sections_for_reference_revalidation,
)


def _make_section(section_id: str, title: str, deps=None, depth_level: int = 0) -> SectionNode:
    """Helper to create a SectionNode with minimal required fields."""
    return SectionNode(
        section_id=section_id,
        title=title,
        section_type=SectionType.NARRATIVE_SYNTHESIS,
        description=f"Description for {section_id}.",
        source_queries=[f"query for {section_id}"],
        dependency_edges=deps or [],
        depth_level=depth_level,
    )


def _make_section_state(section_id: str, state: SectionLifecycleState) -> SectionState:
    """Helper to create a SectionState."""
    return SectionState(
        section_id=section_id,
        state=state,
        version=1,
        last_transition_timestamp=datetime.now(timezone.utc).isoformat(),
        validation_history=[],
        claim_table=None,
        summary_abstract=f"Summary for {section_id}",
        retry_counters={},
        cascade_depth=0,
    )


def _build_3_section_chain_plan() -> ReportPlan:
    """Build a plan with A → B → C content dependency chain."""
    section_a = _make_section("section_a", "Section A")
    section_b = _make_section(
        "section_b", "Section B",
        deps=[DependencyEdge(
            source_section_id="section_b",
            target_section_id="section_a",
            kind=DependencyKind.CONTENT,
        )],
    )
    section_c = _make_section(
        "section_c", "Section C",
        deps=[DependencyEdge(
            source_section_id="section_c",
            target_section_id="section_b",
            kind=DependencyKind.CONTENT,
        )],
    )
    return ReportPlan(
        plan_id="test_plan",
        title="Test Plan",
        version="1.0",
        sections=[section_a, section_b, section_c],
    )


class TestCascadePropagation3SectionChain:
    """FR-23: 3-section content chain A→B→C — root changes → dependents invalidated."""

    def test_invalidate_b_and_c_when_a_changes(self):
        """When section A is re-generated, B and C should be invalidated (FR-23)."""
        plan = _build_3_section_chain_plan()
        gen_dag = build_generation_dag(plan)

        # All sections start as FINALIZED
        section_states = {
            "section_a": _make_section_state("section_a", SectionLifecycleState.FINALIZED),
            "section_b": _make_section_state("section_b", SectionLifecycleState.FINALIZED),
            "section_c": _make_section_state("section_c", SectionLifecycleState.FINALIZED),
        }

        # Simulate A changed → invalidate dependents
        affected = invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
            cascade_depth_limit=10,  # High limit so no escalation
        )

        # B should be invalidated
        assert section_states["section_b"].state == SectionLifecycleState.INVALIDATED
        # C should be invalidated (transitive)
        assert section_states["section_c"].state == SectionLifecycleState.INVALIDATED
        # A should remain FINALIZED (it's the source of change, not a dependent)
        assert section_states["section_a"].state == SectionLifecycleState.FINALIZED

        # Check affected list contains both B and C
        affected_ids = {sid for sid, _ in affected}
        assert "section_b" in affected_ids
        assert "section_c" in affected_ids

    def test_invalidation_clears_claim_table_and_summary(self):
        """FR-23: Invalidated sections should have claim_table and summary_abstract cleared."""
        plan = _build_3_section_chain_plan()
        gen_dag = build_generation_dag(plan)

        section_states = {
            "section_a": _make_section_state("section_a", SectionLifecycleState.FINALIZED),
            "section_b": _make_section_state("section_b", SectionLifecycleState.FINALIZED),
            "section_c": _make_section_state("section_c", SectionLifecycleState.FINALIZED),
        }

        # Ensure B and C have summary_abstract set
        assert section_states["section_b"].summary_abstract is not None
        assert section_states["section_c"].summary_abstract is not None

        invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
            cascade_depth_limit=10,
        )

        assert section_states["section_b"].claim_table is None
        assert section_states["section_b"].summary_abstract is None
        assert section_states["section_b"].validation_history == []
        assert section_states["section_c"].claim_table is None
        assert section_states["section_c"].summary_abstract is None
        assert section_states["section_c"].validation_history == []

    def test_cascade_depth_tracked(self):
        """FR-23: cascade_depth should be set correctly for each level."""
        plan = _build_3_section_chain_plan()
        gen_dag = build_generation_dag(plan)

        section_states = {
            "section_a": _make_section_state("section_a", SectionLifecycleState.FINALIZED),
            "section_b": _make_section_state("section_b", SectionLifecycleState.FINALIZED),
            "section_c": _make_section_state("section_c", SectionLifecycleState.FINALIZED),
        }

        invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
            cascade_depth_limit=10,
        )

        assert section_states["section_b"].cascade_depth == 1
        assert section_states["section_c"].cascade_depth == 2


class TestCascadeDepthLimit:
    """FR-24: Cascade stops at CASCADE_DEPTH_LIMIT; deeper sections are escalated."""

    def _build_4_deep_chain_plan(self) -> ReportPlan:
        """Build a plan with A → B → C → D content dependency chain (4 deep)."""
        section_a = _make_section("section_a", "Section A")
        section_b = _make_section(
            "section_b", "Section B",
            deps=[DependencyEdge(
                source_section_id="section_b",
                target_section_id="section_a",
                kind=DependencyKind.CONTENT,
            )],
        )
        section_c = _make_section(
            "section_c", "Section C",
            deps=[DependencyEdge(
                source_section_id="section_c",
                target_section_id="section_b",
                kind=DependencyKind.CONTENT,
            )],
        )
        section_d = _make_section(
            "section_d", "Section D",
            deps=[DependencyEdge(
                source_section_id="section_d",
                target_section_id="section_c",
                kind=DependencyKind.CONTENT,
            )],
        )
        return ReportPlan(
            plan_id="test_plan_4deep",
            title="Test Plan 4 Deep",
            version="1.0",
            sections=[section_a, section_b, section_c, section_d],
        )

    def test_cascade_stops_at_depth_limit_2(self):
        """FR-24: With CASCADE_DEPTH_LIMIT=2, section at depth 3 is escalated."""
        plan = self._build_4_deep_chain_plan()
        gen_dag = build_generation_dag(plan)

        section_states = {
            "section_a": _make_section_state("section_a", SectionLifecycleState.FINALIZED),
            "section_b": _make_section_state("section_b", SectionLifecycleState.FINALIZED),
            "section_c": _make_section_state("section_c", SectionLifecycleState.FINALIZED),
            "section_d": _make_section_state("section_d", SectionLifecycleState.FINALIZED),
        }

        affected = invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
            cascade_depth_limit=2,
        )

        # B at depth 1 → INVALIDATED
        assert section_states["section_b"].state == SectionLifecycleState.INVALIDATED
        assert section_states["section_b"].cascade_depth == 1

        # C at depth 2 → INVALIDATED (still within limit)
        assert section_states["section_c"].state == SectionLifecycleState.INVALIDATED
        assert section_states["section_c"].cascade_depth == 2

        # D at depth 3 → ESCALATED (exceeds limit of 2)
        assert section_states["section_d"].state == SectionLifecycleState.ESCALATED
        assert section_states["section_d"].cascade_depth == 3

        # A unchanged
        assert section_states["section_a"].state == SectionLifecycleState.FINALIZED

    def test_escalated_section_not_further_propagated(self):
        """FR-24: Escalation terminates cascade — no further dependents enqueued."""
        plan = self._build_4_deep_chain_plan()
        gen_dag = build_generation_dag(plan)

        section_states = {
            "section_a": _make_section_state("section_a", SectionLifecycleState.FINALIZED),
            "section_b": _make_section_state("section_b", SectionLifecycleState.FINALIZED),
            "section_c": _make_section_state("section_c", SectionLifecycleState.FINALIZED),
            "section_d": _make_section_state("section_d", SectionLifecycleState.FINALIZED),
        }

        affected = invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
            cascade_depth_limit=1,
        )

        # B at depth 1 → INVALIDATED
        assert section_states["section_b"].state == SectionLifecycleState.INVALIDATED

        # C at depth 2 → ESCALATED (exceeds limit of 1)
        assert section_states["section_c"].state == SectionLifecycleState.ESCALATED

        # D should NOT be touched because escalation at C terminates cascade
        # D stays FINALIZED
        assert section_states["section_d"].state == SectionLifecycleState.FINALIZED

    def test_already_escalated_sections_skipped(self):
        """FR-24: Sections already in ESCALATED state are not re-processed."""
        plan = self._build_4_deep_chain_plan()
        gen_dag = build_generation_dag(plan)

        section_states = {
            "section_a": _make_section_state("section_a", SectionLifecycleState.FINALIZED),
            "section_b": _make_section_state("section_b", SectionLifecycleState.ESCALATED),
            "section_c": _make_section_state("section_c", SectionLifecycleState.FINALIZED),
            "section_d": _make_section_state("section_d", SectionLifecycleState.FINALIZED),
        }

        affected = invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
            cascade_depth_limit=10,
        )

        # B already ESCALATED → skipped
        assert section_states["section_b"].state == SectionLifecycleState.ESCALATED
        affected_ids = {sid for sid, _ in affected}
        assert "section_b" not in affected_ids


class TestReferenceDependencyRevalidation:
    """FR-25: Reference dep change → re-validate only, no re-generation."""

    def test_reference_dependents_identified(self):
        """FR-25: get_reference_dependents returns sections with reference-only deps."""
        # A is upstream. B has content dep on A. C has reference dep on A.
        section_a = _make_section("section_a", "Section A")
        section_b = _make_section(
            "section_b", "Section B",
            deps=[DependencyEdge(
                source_section_id="section_b",
                target_section_id="section_a",
                kind=DependencyKind.CONTENT,
            )],
        )
        section_c = _make_section(
            "section_c", "Section C",
            deps=[DependencyEdge(
                source_section_id="section_c",
                target_section_id="section_a",
                kind=DependencyKind.REFERENCE,
            )],
        )
        plan = ReportPlan(
            plan_id="ref_test",
            title="Ref Test",
            version="1.0",
            sections=[section_a, section_b, section_c],
        )

        gen_dag = build_generation_dag(plan)
        fin_dag = build_finalization_dag(plan)

        ref_deps = get_reference_dependents(
            changed_section_id="section_a",
            finalization_dag=fin_dag,
            generation_dag=gen_dag,
        )

        # C has reference dep on A but NOT content dep → should be in result
        assert "section_c" in ref_deps
        # B has content dep on A → should NOT be in result (it's a content dependent)
        assert "section_b" not in ref_deps

    def test_mark_sections_for_reference_revalidation(self):
        """FR-25: Only finalized/stable sections are flagged for re-validation."""
        section_states = {
            "section_c": _make_section_state("section_c", SectionLifecycleState.FINALIZED),
            "section_d": _make_section_state("section_d", SectionLifecycleState.QUEUED),
        }

        flagged = mark_sections_for_reference_revalidation(
            section_ids=["section_c", "section_d"],
            section_states=section_states,
        )

        assert "section_c" in flagged
        assert "section_d" not in flagged

    def test_reference_change_does_not_invalidate(self):
        """FR-25: Reference change should not cause content invalidation."""
        section_a = _make_section("section_a", "Section A")
        section_c = _make_section(
            "section_c", "Section C",
            deps=[DependencyEdge(
                source_section_id="section_c",
                target_section_id="section_a",
                kind=DependencyKind.REFERENCE,
            )],
        )
        plan = ReportPlan(
            plan_id="ref_test2",
            title="Ref Test 2",
            version="1.0",
            sections=[section_a, section_c],
        )

        gen_dag = build_generation_dag(plan)

        section_states = {
            "section_a": _make_section_state("section_a", SectionLifecycleState.FINALIZED),
            "section_c": _make_section_state("section_c", SectionLifecycleState.FINALIZED),
        }

        # Content cascade on A should NOT affect C (reference dep only, not in gen_dag)
        affected = invalidate_content_dependents(
            changed_section_id="section_a",
            section_states=section_states,
            generation_dag=gen_dag,
            cascade_depth_limit=10,
        )

        # C should remain FINALIZED — reference deps don't trigger content invalidation
        assert section_states["section_c"].state == SectionLifecycleState.FINALIZED
        affected_ids = {sid for sid, _ in affected}
        assert "section_c" not in affected_ids