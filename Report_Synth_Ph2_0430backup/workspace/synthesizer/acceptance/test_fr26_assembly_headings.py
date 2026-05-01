# synthesizer/acceptance/test_fr26_assembly_headings.py
"""Acceptance test for FR-26: Assembly heading level correctness (§19).

Finalizes 4 sections at depth_levels 1, 2, 2, 1. Assembles the report.
Asserts heading levels in the output markdown match:
  - depth 1 → level 1 headings (adjusted by base_heading_level)
  - depth 2 → level 2 headings
"""

import os
import re
import tempfile
import shutil
import pytest
from pathlib import Path

from synthesizer.assembly.assembler import (
    assemble_report,
    _adjust_heading_levels,
    _find_latest_draft,
)
from synthesizer.models.enums import SectionType
from synthesizer.models.report_plan import ReportPlan, SectionNode


def _make_four_section_plan():
    """Create a 4-section plan with depth_levels [1, 2, 2, 1]."""
    sections = [
        SectionNode(
            section_id="intro",
            title="Introduction",
            section_type=SectionType.NARRATIVE_SYNTHESIS,
            depth_level=1,
            description="Introduction section.",
            source_queries=["intro query"],
            dependency_edges=[],
        ),
        SectionNode(
            section_id="background",
            title="Background",
            section_type=SectionType.NARRATIVE_SYNTHESIS,
            depth_level=2,
            description="Background subsection.",
            source_queries=["background query"],
            dependency_edges=[],
        ),
        SectionNode(
            section_id="methods",
            title="Methods",
            section_type=SectionType.NARRATIVE_SYNTHESIS,
            depth_level=2,
            description="Methods subsection.",
            source_queries=["methods query"],
            dependency_edges=[],
        ),
        SectionNode(
            section_id="conclusion",
            title="Conclusion",
            section_type=SectionType.NARRATIVE_SYNTHESIS,
            depth_level=1,
            description="Conclusion section.",
            source_queries=["conclusion query"],
            dependency_edges=[],
        ),
    ]

    return ReportPlan(
        plan_id="test_plan_fr26",
        title="FR-26 Test Plan",
        version="1.0",
        sections=sections,
    )


@pytest.fixture
def output_dir():
    """Create a temporary output directory and clean up after test."""
    tmpdir = tempfile.mkdtemp(prefix="test_fr26_")
    yield Path(tmpdir)
    shutil.rmtree(tmpdir, ignore_errors=True)


def _write_section_draft(output_dir: Path, section_id: str, content: str, version: int = 1):
    """Write a draft file for a section."""
    section_dir = output_dir / "sections" / section_id
    os.makedirs(section_dir, exist_ok=True)
    draft_path = section_dir / f"draft_v{version}.md"
    draft_path.write_text(content, encoding="utf-8")


class TestFR26AssemblyHeadings:
    """FR-26: Assembly heading levels match report plan depth_level values."""

    def test_heading_levels_match_depth_levels(self, output_dir):
        """FR-26: Assembled report has correct heading levels for each depth_level."""
        plan = _make_four_section_plan()

        # Write draft content with # headings for each section
        _write_section_draft(output_dir, "intro", "# Introduction\n\nThis is the introduction.")
        _write_section_draft(output_dir, "background", "# Background\n\nThis is the background.")
        _write_section_draft(output_dir, "methods", "# Methods\n\nThis is the methods section.")
        _write_section_draft(output_dir, "conclusion", "# Conclusion\n\nThis is the conclusion.")

        report_path = assemble_report(
            report_plan=plan,
            output_dir=output_dir,
            base_heading_level=1,
        )

        assert report_path.exists(), "Report file should exist"
        content = report_path.read_text(encoding="utf-8")

        # Extract all headings from the assembled report
        heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
        headings = heading_pattern.findall(content)

        assert len(headings) >= 4, f"Expected at least 4 headings, found {len(headings)}"

        # Map section titles to expected heading levels
        # depth_level=1, base=1: offset = 1+1-1 = 1, so # becomes ##
        # depth_level=2, base=1: offset = 2+1-1 = 2, so # becomes ###
        expected = {
            "Introduction": 2,   # depth 1: # + offset(1) = ##
            "Background": 3,     # depth 2: # + offset(2) = ###
            "Methods": 3,        # depth 2: # + offset(2) = ###
            "Conclusion": 2,     # depth 1: # + offset(1) = ##
        }

        for hashes, title in headings:
            title_stripped = title.strip()
            if title_stripped in expected:
                actual_level = len(hashes)
                expected_level = expected[title_stripped]
                assert actual_level == expected_level, (
                    f"Heading '{title_stripped}' should be level {expected_level}, "
                    f"got level {actual_level}"
                )

    def test_depth_0_sections_keep_original_level(self, output_dir):
        """FR-26: depth_level=0 sections with base_heading_level=1 have no offset."""
        plan = ReportPlan(
            plan_id="test_depth0",
            title="Depth 0 Test",
            version="1.0",
            sections=[
                SectionNode(
                    section_id="top",
                    title="Top Level",
                    section_type=SectionType.NARRATIVE_SYNTHESIS,
                    depth_level=0,
                    description="Top level section.",
                    source_queries=["query"],
                    dependency_edges=[],
                ),
            ],
        )

        _write_section_draft(output_dir, "top", "# Top Level\n\nContent here.")

        report_path = assemble_report(
            report_plan=plan,
            output_dir=output_dir,
            base_heading_level=1,
        )

        content = report_path.read_text(encoding="utf-8")
        heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
        headings = heading_pattern.findall(content)

        # depth_level=0, base=1: offset = 0+1-1 = 0, no change
        # Actually offset = 0, so no adjustment
        assert len(headings) >= 1
        # With depth_level=0 and base=1, offset = 0+1-1 = 0, so no shift
        # The heading stays at level 1 (#)
        # Wait, let's check the code: offset = depth_level + base_heading_level - 1
        # = 0 + 1 - 1 = 0, so if offset <= 0, no adjustment
        assert headings[0][0] == "#", (
            f"depth_level=0 heading should remain #, got {headings[0][0]}"
        )

    def test_heading_level_clamped_to_6(self, output_dir):
        """FR-26: Heading levels are clamped to maximum of 6."""
        plan = ReportPlan(
            plan_id="test_clamp",
            title="Clamp Test",
            version="1.0",
            sections=[
                SectionNode(
                    section_id="deep",
                    title="Deep Section",
                    section_type=SectionType.NARRATIVE_SYNTHESIS,
                    depth_level=5,
                    description="Very deep section.",
                    source_queries=["query"],
                    dependency_edges=[],
                ),
            ],
        )

        # Start with ### (level 3), depth_level=5, base=1
        # offset = 5+1-1 = 5, new_level = 3+5 = 8, clamped to 6
        _write_section_draft(output_dir, "deep", "### Deep Heading\n\nContent.")

        report_path = assemble_report(
            report_plan=plan,
            output_dir=output_dir,
            base_heading_level=1,
        )

        content = report_path.read_text(encoding="utf-8")
        heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
        headings = heading_pattern.findall(content)

        assert len(headings) >= 1
        assert len(headings[0][0]) == 6, (
            f"Heading should be clamped to 6, got {len(headings[0][0])}"
        )

    def test_adjust_heading_levels_function(self):
        """FR-26: _adjust_heading_levels correctly shifts heading levels."""
        content = "# Title\n\nSome text\n\n## Subtitle\n\nMore text"

        # depth_level=1, base=1: offset = 1
        adjusted = _adjust_heading_levels(content, depth_level=1, base_heading_level=1)

        assert "## Title" in adjusted, "# should become ## with offset 1"
        assert "### Subtitle" in adjusted, "## should become ### with offset 1"

    def test_missing_section_gets_placeholder(self, output_dir):
        """FR-26: Missing section drafts get a placeholder in the assembled report."""
        plan = _make_four_section_plan()

        # Only write drafts for 2 of 4 sections
        _write_section_draft(output_dir, "intro", "# Introduction\n\nContent.")
        _write_section_draft(output_dir, "conclusion", "# Conclusion\n\nContent.")
        # background and methods are missing

        report_path = assemble_report(
            report_plan=plan,
            output_dir=output_dir,
            base_heading_level=1,
        )

        content = report_path.read_text(encoding="utf-8")
        assert "unavailable" in content.lower() or "escalated" in content.lower(), (
            "Missing sections should have placeholder text"
        )

    def test_report_written_to_correct_path(self, output_dir):
        """FR-26/NFR-04: Report is written to output_dir/report/literature_review.md."""
        plan = _make_four_section_plan()

        _write_section_draft(output_dir, "intro", "# Intro\n\nText.")
        _write_section_draft(output_dir, "background", "# Background\n\nText.")
        _write_section_draft(output_dir, "methods", "# Methods\n\nText.")
        _write_section_draft(output_dir, "conclusion", "# Conclusion\n\nText.")

        report_path = assemble_report(
            report_plan=plan,
            output_dir=output_dir,
        )

        expected_path = output_dir / "report" / "literature_review.md"
        assert report_path == expected_path
        assert expected_path.exists()

    def test_find_latest_draft_selects_highest_version(self, output_dir):
        """FR-26: _find_latest_draft selects the highest version draft."""
        section_dir = output_dir / "sections" / "test_section"
        os.makedirs(section_dir, exist_ok=True)

        (section_dir / "draft_v1.md").write_text("v1 content", encoding="utf-8")
        (section_dir / "draft_v2.md").write_text("v2 content", encoding="utf-8")
        (section_dir / "draft_v3.md").write_text("v3 content", encoding="utf-8")

        latest = _find_latest_draft(section_dir)
        assert latest is not None
        assert latest.name == "draft_v3.md"
        assert latest.read_text(encoding="utf-8") == "v3 content"

    def test_sections_assembled_in_plan_order(self, output_dir):
        """FR-26: Sections are assembled in the order specified by the report plan."""
        plan = _make_four_section_plan()

        _write_section_draft(output_dir, "intro", "# Introduction\n\nFirst section.")
        _write_section_draft(output_dir, "background", "# Background\n\nSecond section.")
        _write_section_draft(output_dir, "methods", "# Methods\n\nThird section.")
        _write_section_draft(output_dir, "conclusion", "# Conclusion\n\nFourth section.")

        report_path = assemble_report(report_plan=plan, output_dir=output_dir)
        content = report_path.read_text(encoding="utf-8")

        # Check that sections appear in order
        intro_pos = content.find("First section")
        bg_pos = content.find("Second section")
        methods_pos = content.find("Third section")
        conclusion_pos = content.find("Fourth section")

        assert intro_pos < bg_pos < methods_pos < conclusion_pos, (
            "Sections should appear in plan order"
        )