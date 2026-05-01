# tests/test_assembly.py
"""Tests for report assembly (FR-26, FR-27).

Covers:
  - 4 sections at varying depths produce correctly adjusted heading levels (FR-26)
  - Assembly blocked when a section is in non-terminal state with descriptive error (FR-27)
"""

import os
import tempfile
from pathlib import Path

import pytest

from synthesizer.assembly.assembler import (
    assemble_report,
    _adjust_heading_levels,
    _find_latest_draft,
)
from synthesizer.models.enums import SectionLifecycleState, SectionType
from synthesizer.models.report_plan import ReportPlan, SectionNode
from synthesizer.models.state import SectionState
from synthesizer.orchestrator.lifecycle import (
    AssemblyNotReadyError,
    check_assembly_readiness,
)


def _make_section(
    section_id: str,
    title: str,
    depth_level: int = 0,
    deps=None,
) -> SectionNode:
    """Helper to create a SectionNode."""
    return SectionNode(
        section_id=section_id,
        title=title,
        section_type=SectionType.NARRATIVE_SYNTHESIS,
        description=f"Description for {section_id}.",
        source_queries=[f"query for {section_id}"],
        dependency_edges=deps or [],
        depth_level=depth_level,
    )


def _make_section_state(
    section_id: str,
    state: SectionLifecycleState,
) -> SectionState:
    """Helper to create a SectionState."""
    from datetime import datetime, timezone
    return SectionState(
        section_id=section_id,
        state=state,
        version=1,
        last_transition_timestamp=datetime.now(timezone.utc).isoformat(),
        validation_history=[],
        retry_counters={},
        cascade_depth=0,
    )


@pytest.fixture
def tmp_output_dir():
    """Create a temporary output directory and clean up after test."""
    tmpdir = tempfile.mkdtemp()
    yield Path(tmpdir)
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)


class TestHeadingLevelAdjustment:
    """FR-26: Heading hierarchy matches report plan depth_level values."""

    def test_adjust_heading_levels_depth_0(self):
        """FR-26: depth_level=0 with base=1 → offset=0, headings unchanged."""
        content = "# Top Heading\n\nSome text.\n\n## Sub Heading\n"
        result = _adjust_heading_levels(content, depth_level=0, base_heading_level=1)
        # offset = 0 + 1 - 1 = 0 → no change
        assert "# Top Heading" in result
        assert "## Sub Heading" in result

    def test_adjust_heading_levels_depth_1(self):
        """FR-26: depth_level=1 with base=1 → offset=1, # becomes ##."""
        content = "# Heading\n\nText.\n\n## Sub\n"
        result = _adjust_heading_levels(content, depth_level=1, base_heading_level=1)
        # offset = 1 + 1 - 1 = 1
        assert "## Heading" in result
        assert "### Sub" in result

    def test_adjust_heading_levels_depth_2(self):
        """FR-26: depth_level=2 with base=1 → offset=2, # becomes ###."""
        content = "# Heading\n\nText.\n"
        result = _adjust_heading_levels(content, depth_level=2, base_heading_level=1)
        # offset = 2 + 1 - 1 = 2
        assert "### Heading" in result

    def test_heading_level_clamped_to_6(self):
        """FR-26: Heading level should not exceed 6 (markdown spec limit)."""
        content = "##### Deep Heading\n"
        result = _adjust_heading_levels(content, depth_level=3, base_heading_level=1)
        # Original: 5 hashes, offset = 3 → 5+3=8, clamped to 6
        assert "###### Deep Heading" in result
        # Should not have more than 6 hashes
        assert "####### " not in result


class TestAssembly4Sections:
    """FR-26: 4 sections at varying depths produce correctly adjusted heading levels."""

    def _create_section_drafts(self, output_dir: Path) -> ReportPlan:
        """Create 4 mock section drafts at depth_levels 1, 2, 2, 1."""
        sections = [
            _make_section("intro", "Introduction", depth_level=1),
            _make_section("methods_a", "Methods A", depth_level=2),
            _make_section("methods_b", "Methods B", depth_level=2),
            _make_section("conclusion", "Conclusion", depth_level=1),
        ]

        plan = ReportPlan(
            plan_id="assembly_test",
            title="Assembly Test",
            version="1.0",
            sections=sections,
        )

        # Create draft files
        drafts = {
            "intro": "# Introduction\n\nThis is the introduction.\n\n## Background\n\nSome background.",
            "methods_a": "# Methods A\n\nMethod A description.\n\n## Details\n\nDetails here.",
            "methods_b": "# Methods B\n\nMethod B description.",
            "conclusion": "# Conclusion\n\nFinal thoughts.\n\n## Summary\n\nSummary here.",
        }

        for section_id, content in drafts.items():
            section_dir = output_dir / "sections" / section_id
            os.makedirs(section_dir, exist_ok=True)
            draft_path = section_dir / "draft_v1.md"
            draft_path.write_text(content, encoding="utf-8")

        return plan

    def test_assembly_adjusts_heading_levels_correctly(self, tmp_output_dir):
        """FR-26: Assembled report has correctly adjusted heading levels for all 4 sections."""
        plan = self._create_section_drafts(tmp_output_dir)

        report_path = assemble_report(
            report_plan=plan,
            output_dir=tmp_output_dir,
            base_heading_level=1,
        )

        assert report_path.exists()
        content = report_path.read_text(encoding="utf-8")

        # depth_level=1, base=1 → offset=1
        # "# Introduction" → "## Introduction"
        assert "## Introduction" in content
        # "## Background" → "### Background"
        assert "### Background" in content

        # depth_level=2, base=1 → offset=2
        # "# Methods A" → "### Methods A"
        assert "### Methods A" in content
        # "## Details" → "#### Details"
        assert "#### Details" in content

        # "# Methods B" → "### Methods B"
        assert "### Methods B" in content

        # depth_level=1, base=1 → offset=1
        # "# Conclusion" → "## Conclusion"
        assert "## Conclusion" in content
        # "## Summary" → "### Summary"
        assert "### Summary" in content

    def test_assembly_output_path(self, tmp_output_dir):
        """FR-26: Assembled report is written to output_dir/report/literature_review.md."""
        plan = self._create_section_drafts(tmp_output_dir)

        report_path = assemble_report(
            report_plan=plan,
            output_dir=tmp_output_dir,
        )

        expected_path = tmp_output_dir / "report" / "literature_review.md"
        assert report_path == expected_path
        assert expected_path.exists()

    def test_assembly_sections_in_plan_order(self, tmp_output_dir):
        """FR-26: Sections appear in the order specified by the report plan."""
        plan = self._create_section_drafts(tmp_output_dir)

        report_path = assemble_report(
            report_plan=plan,
            output_dir=tmp_output_dir,
        )

        content = report_path.read_text(encoding="utf-8")

        # Find positions of section headings
        intro_pos = content.find("## Introduction")
        methods_a_pos = content.find("### Methods A")
        methods_b_pos = content.find("### Methods B")
        conclusion_pos = content.find("## Conclusion")

        assert intro_pos < methods_a_pos < methods_b_pos < conclusion_pos

    def test_assembly_missing_section_gets_placeholder(self, tmp_output_dir):
        """FR-26: Missing section draft results in a placeholder in the assembled report."""
        sections = [
            _make_section("existing", "Existing Section", depth_level=0),
            _make_section("missing", "Missing Section", depth_level=1),
        ]
        plan = ReportPlan(
            plan_id="missing_test",
            title="Missing Test",
            version="1.0",
            sections=sections,
        )

        # Only create draft for "existing"
        section_dir = tmp_output_dir / "sections" / "existing"
        os.makedirs(section_dir, exist_ok=True)
        (section_dir / "draft_v1.md").write_text("# Existing\n\nContent here.", encoding="utf-8")

        # Don't create draft for "missing"
        os.makedirs(tmp_output_dir / "sections" / "missing", exist_ok=True)

        report_path = assemble_report(
            report_plan=plan,
            output_dir=tmp_output_dir,
        )

        content = report_path.read_text(encoding="utf-8")
        assert "unavailable" in content.lower() or "escalated" in content.lower() or "missing" in content.lower()


class TestFindLatestDraft:
    """Test _find_latest_draft helper."""

    def test_finds_highest_version(self, tmp_output_dir):
        """Should return the draft with the highest version number."""
        section_dir = tmp_output_dir / "sections" / "test_section"
        os.makedirs(section_dir, exist_ok=True)

        (section_dir / "draft_v1.md").write_text("v1 content", encoding="utf-8")
        (section_dir / "draft_v2.md").write_text("v2 content", encoding="utf-8")
        (section_dir / "draft_v3.md").write_text("v3 content", encoding="utf-8")

        result = _find_latest_draft(section_dir)
        assert result is not None
        assert result.name == "draft_v3.md"

    def test_returns_none_for_empty_dir(self, tmp_output_dir):
        """Should return None if no drafts exist."""
        section_dir = tmp_output_dir / "sections" / "empty_section"
        os.makedirs(section_dir, exist_ok=True)

        result = _find_latest_draft(section_dir)
        assert result is None

    def test_returns_none_for_nonexistent_dir(self, tmp_output_dir):
        """Should return None if directory doesn't exist."""
        section_dir = tmp_output_dir / "sections" / "nonexistent"
        result = _find_latest_draft(section_dir)
        assert result is None


class TestAssemblyReadiness:
    """FR-27: Assembly blocked when a section is in non-terminal state."""

    def test_all_finalized_passes(self):
        """FR-27: All sections FINALIZED → assembly readiness check passes."""
        section_states = {
            "s1": _make_section_state("s1", SectionLifecycleState.FINALIZED),
            "s2": _make_section_state("s2", SectionLifecycleState.FINALIZED),
        }
        assert check_assembly_readiness(section_states) is True

    def test_finalized_and_stable_passes(self):
        """FR-27: Mix of FINALIZED and STABLE → passes."""
        section_states = {
            "s1": _make_section_state("s1", SectionLifecycleState.FINALIZED),
            "s2": _make_section_state("s2", SectionLifecycleState.STABLE),
        }
        assert check_assembly_readiness(section_states) is True

    def test_finalized_and_escalated_passes(self):
        """FR-27: Mix of FINALIZED and ESCALATED → passes (escalated = human-reviewed)."""
        section_states = {
            "s1": _make_section_state("s1", SectionLifecycleState.FINALIZED),
            "s2": _make_section_state("s2", SectionLifecycleState.ESCALATED),
        }
        assert check_assembly_readiness(section_states) is True

    def test_drafted_section_blocks_assembly(self):
        """FR-27: A section in DRAFTED state blocks assembly with descriptive error."""
        section_states = {
            "s1": _make_section_state("s1", SectionLifecycleState.FINALIZED),
            "s2": _make_section_state("s2", SectionLifecycleState.DRAFTED),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        error = exc_info.value
        assert "s2" in str(error)
        assert "drafted" in str(error).lower()
        assert len(error.non_ready_sections) == 1
        assert error.non_ready_sections[0][0] == "s2"
        assert error.non_ready_sections[0][1] == SectionLifecycleState.DRAFTED

    def test_queued_section_blocks_assembly(self):
        """FR-27: A section in QUEUED state blocks assembly."""
        section_states = {
            "s1": _make_section_state("s1", SectionLifecycleState.FINALIZED),
            "s2": _make_section_state("s2", SectionLifecycleState.QUEUED),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        error = exc_info.value
        assert "s2" in str(error)
        assert len(error.non_ready_sections) == 1

    def test_generating_section_blocks_assembly(self):
        """FR-27: A section in GENERATING state blocks assembly."""
        section_states = {
            "s1": _make_section_state("s1", SectionLifecycleState.FINALIZED),
            "s2": _make_section_state("s2", SectionLifecycleState.GENERATING),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        assert "s2" in str(exc_info.value)

    def test_multiple_non_ready_sections_listed(self):
        """FR-27: Multiple non-ready sections are all listed in the error."""
        section_states = {
            "s1": _make_section_state("s1", SectionLifecycleState.QUEUED),
            "s2": _make_section_state("s2", SectionLifecycleState.DRAFTED),
            "s3": _make_section_state("s3", SectionLifecycleState.FINALIZED),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        error = exc_info.value
        assert len(error.non_ready_sections) == 2
        non_ready_ids = {sid for sid, _ in error.non_ready_sections}
        assert "s1" in non_ready_ids
        assert "s2" in non_ready_ids
        assert "s3" not in non_ready_ids

    def test_invalidated_section_blocks_assembly(self):
        """FR-27: A section in INVALIDATED state blocks assembly."""
        section_states = {
            "s1": _make_section_state("s1", SectionLifecycleState.FINALIZED),
            "s2": _make_section_state("s2", SectionLifecycleState.INVALIDATED),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        assert "s2" in str(exc_info.value)

    def test_error_message_is_descriptive(self):
        """FR-27: Error message identifies blocking sections and their states."""
        section_states = {
            "intro": _make_section_state("intro", SectionLifecycleState.DRAFTED),
            "body": _make_section_state("body", SectionLifecycleState.FINALIZED),
            "conclusion": _make_section_state("conclusion", SectionLifecycleState.QUEUED),
        }

        with pytest.raises(AssemblyNotReadyError) as exc_info:
            check_assembly_readiness(section_states)

        msg = str(exc_info.value)
        assert "Assembly blocked" in msg
        assert "intro" in msg
        assert "conclusion" in msg
        assert "drafted" in msg.lower()
        assert "queued" in msg.lower()