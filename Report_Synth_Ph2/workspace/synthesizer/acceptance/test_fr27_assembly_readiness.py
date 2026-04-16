# synthesizer/acceptance/test_fr27_assembly_readiness.py
"""Acceptance test for FR-27: Assembly readiness blocking on non-finalized sections (§19).

Leaves one section in DRAFTED state. Attempts assembly.
Asserts AssemblyNotReadyError is raised with a message identifying
the non-finalized section.
"""

import pytest
from datetime import datetime, timezone

from synthesizer.acceptance import make_section_state
from synthesizer.models.enums import SectionLifecycleState
from synthesizer.models.state import SectionState
from synthesizer.orchestrator.lifecycle import (
    AssemblyNotReadyError,
    check_assembly_readiness,
)


class TestFR27AssemblyReadiness:
    """FR-27: Assembly readiness blocking on non-finalized sections."""

    def test_assembly_blocked_by_drafted_section(self):
        """FR-27: Assembly is blocked when one section is in DRAFTED state."""
        section_states = {
            "section_a": make_section_state(
                section_id="section_a",
                state=SectionLifecycleState.FINALIZED,
            ),
            "section_b": make_section_state(
                section_id="section_b",
                state=SectionLifecycleState.DRAFTED,
            ),
            "section_c": make_section_state(
                section_id="section_c",
                state=SectionLifecycleState.FINALIZED,
            ),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        error = exc_info.value
        assert "section_b" in str(error), (
            "Error message should identify the non-finalized section 'section_b'"
        )
        assert "drafted" in str(error).lower(), (
            "Error message should mention the 'drafted' state"
        )

        # Check the non_ready_sections attribute
        non_ready_ids = {sid for sid, _ in error.non_ready_sections}
        assert "section_b" in non_ready_ids

    def test_assembly_blocked_by_queued_section(self):
        """FR-27: Assembly is blocked when one section is in QUEUED state."""
        section_states = {
            "section_a": make_section_state(
                section_id="section_a",
                state=SectionLifecycleState.FINALIZED,
            ),
            "section_b": make_section_state(
                section_id="section_b",
                state=SectionLifecycleState.QUEUED,
            ),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        assert "section_b" in str(exc_info.value)

    def test_assembly_blocked_by_generating_section(self):
        """FR-27: Assembly is blocked when one section is in GENERATING state."""
        section_states = {
            "section_a": make_section_state(
                section_id="section_a",
                state=SectionLifecycleState.FINALIZED,
            ),
            "section_b": make_section_state(
                section_id="section_b",
                state=SectionLifecycleState.GENERATING,
            ),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        assert "section_b" in str(exc_info.value)

    def test_assembly_blocked_by_invalidated_section(self):
        """FR-27: Assembly is blocked when one section is in INVALIDATED state."""
        section_states = {
            "section_a": make_section_state(
                section_id="section_a",
                state=SectionLifecycleState.FINALIZED,
            ),
            "section_b": make_section_state(
                section_id="section_b",
                state=SectionLifecycleState.INVALIDATED,
            ),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        assert "section_b" in str(exc_info.value)

    def test_assembly_allowed_when_all_finalized(self):
        """FR-27: Assembly is allowed when all sections are FINALIZED."""
        section_states = {
            "section_a": make_section_state(
                section_id="section_a",
                state=SectionLifecycleState.FINALIZED,
            ),
            "section_b": make_section_state(
                section_id="section_b",
                state=SectionLifecycleState.FINALIZED,
            ),
            "section_c": make_section_state(
                section_id="section_c",
                state=SectionLifecycleState.FINALIZED,
            ),
        }

        result = check_assembly_readiness(section_states)
        assert result is True

    def test_assembly_allowed_when_all_stable(self):
        """FR-27: Assembly is allowed when all sections are STABLE."""
        section_states = {
            "section_a": make_section_state(
                section_id="section_a",
                state=SectionLifecycleState.STABLE,
            ),
            "section_b": make_section_state(
                section_id="section_b",
                state=SectionLifecycleState.STABLE,
            ),
        }

        result = check_assembly_readiness(section_states)
        assert result is True

    def test_assembly_allowed_with_escalated_sections(self):
        """FR-27: Assembly is allowed when sections are ESCALATED (human-reviewed)."""
        section_states = {
            "section_a": make_section_state(
                section_id="section_a",
                state=SectionLifecycleState.FINALIZED,
            ),
            "section_b": make_section_state(
                section_id="section_b",
                state=SectionLifecycleState.ESCALATED,
            ),
        }

        result = check_assembly_readiness(section_states)
        assert result is True

    def test_assembly_allowed_with_mixed_ready_states(self):
        """FR-27: Assembly is allowed with mix of FINALIZED, STABLE, and ESCALATED."""
        section_states = {
            "section_a": make_section_state(
                section_id="section_a",
                state=SectionLifecycleState.FINALIZED,
            ),
            "section_b": make_section_state(
                section_id="section_b",
                state=SectionLifecycleState.STABLE,
            ),
            "section_c": make_section_state(
                section_id="section_c",
                state=SectionLifecycleState.ESCALATED,
            ),
        }

        result = check_assembly_readiness(section_states)
        assert result is True

    def test_multiple_non_ready_sections_all_identified(self):
        """FR-27: Error identifies ALL non-ready sections, not just the first."""
        section_states = {
            "section_a": make_section_state(
                section_id="section_a",
                state=SectionLifecycleState.DRAFTED,
            ),
            "section_b": make_section_state(
                section_id="section_b",
                state=SectionLifecycleState.QUEUED,
            ),
            "section_c": make_section_state(
                section_id="section_c",
                state=SectionLifecycleState.FINALIZED,
            ),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        error = exc_info.value
        non_ready_ids = {sid for sid, _ in error.non_ready_sections}
        assert "section_a" in non_ready_ids, "section_a (DRAFTED) should be identified"
        assert "section_b" in non_ready_ids, "section_b (QUEUED) should be identified"
        assert "section_c" not in non_ready_ids, "section_c (FINALIZED) should NOT be identified"
        assert len(error.non_ready_sections) == 2

    def test_empty_section_states_passes(self):
        """FR-27: Empty section states trivially passes assembly readiness."""
        section_states = {}
        # No sections means nothing to block
        result = check_assembly_readiness(section_states)
        assert result is True

    def test_error_message_contains_state_info(self):
        """FR-27: Error message contains both section_id and state information."""
        section_states = {
            "my_section": make_section_state(
                section_id="my_section",
                state=SectionLifecycleState.DRAFTED,
            ),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        error_msg = str(exc_info.value)
        assert "my_section" in error_msg
        assert "drafted" in error_msg.lower()
        assert "Assembly blocked" in error_msg or "assembly" in error_msg.lower()