# synthesizer/assembly/assembler.py
"""Final report assembler — concatenates finalized sections with heading adjustment (§9.2.5, §15).

Reads each finalized section's latest draft from the output directory,
adjusts markdown heading levels based on the section's depth_level in the
report plan, and concatenates them in plan order into a single document.

Governing spec sections: §9.2.5, §15
Functional requirements: FR-26 (heading hierarchy), FR-27 (assembly readiness)
Non-functional requirements: NFR-04 (deterministic output structure)
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import List, Optional

from synthesizer.models.report_plan import ReportPlan, SectionNode

logger = logging.getLogger(__name__)


def _find_latest_draft(section_dir: Path) -> Optional[Path]:
    """Find the highest-versioned draft_v{N}.md file in a section directory.

    Parameters
    ----------
    section_dir : Path
        Path to the section's output directory (output_dir/sections/{section_id}/).

    Returns
    -------
    Path or None
        Path to the latest draft file, or None if no drafts exist.

    Supports
    --------
    FR-26 : Reads finalized section content for assembly.
    """
    if not section_dir.is_dir():
        return None

    draft_pattern = re.compile(r"^draft_v(\d+)\.md$")
    max_version = -1
    latest_path: Optional[Path] = None

    for entry in section_dir.iterdir():
        match = draft_pattern.match(entry.name)
        if match:
            version = int(match.group(1))
            if version > max_version:
                max_version = version
                latest_path = entry

    return latest_path


def _adjust_heading_levels(content: str, depth_level: int, base_heading_level: int) -> str:
    """Adjust markdown heading levels in content based on depth_level.

    Each ``#`` heading in the content is shifted by ``(depth_level - 1 + base_heading_level - 1)``
    levels. For example, with base_heading_level=1 and depth_level=2, a ``# Heading``
    becomes ``## Heading``.

    The adjustment formula: a heading with N ``#`` characters becomes
    ``(N + depth_level + base_heading_level - 2)`` ``#`` characters, clamped to
    a minimum of 1 and maximum of 6 (markdown spec limit).

    Parameters
    ----------
    content : str
        Markdown content with headings to adjust.
    depth_level : int
        The section's depth_level from the report plan (0 = top-level).
    base_heading_level : int
        The base heading level for the assembled report (default 1).

    Returns
    -------
    str
        Content with adjusted heading levels.

    Supports
    --------
    FR-26 : Heading hierarchy matches report plan depth_level values.
    """
    # The offset to add to each heading's # count.
    # depth_level=0 at base=1 means no shift (top-level sections keep their headings).
    # depth_level=1 at base=1 means +1 shift, etc.
    offset = depth_level + base_heading_level - 1

    if offset <= 0:
        # No adjustment needed (or negative, which shouldn't happen)
        return content

    def _replace_heading(match: re.Match) -> str:
        original_hashes = match.group(1)
        rest = match.group(2)
        new_level = len(original_hashes) + offset
        # Clamp to markdown spec limits
        new_level = max(1, min(6, new_level))
        return "#" * new_level + rest

    # Match markdown headings at the start of a line: one or more # followed by a space
    heading_pattern = re.compile(r"^(#{1,6})(\s+.*)$", re.MULTILINE)
    return heading_pattern.sub(_replace_heading, content)


def assemble_report(
    report_plan: ReportPlan,
    output_dir: Path,
    base_heading_level: int = 1,
) -> Path:
    """Assemble finalized sections into the final report document (§9.2.5, §15).

    Reads each section's latest draft from ``output_dir/sections/{section_id}/``,
    adjusts heading levels based on the section's ``depth_level``, and
    concatenates them in the order specified by the report plan's ``sections``
    array. Writes the result to ``output_dir/report/literature_review.md``.

    Parameters
    ----------
    report_plan : ReportPlan
        The report plan defining section order and depth levels.
    output_dir : Path
        Root output directory containing ``sections/`` subdirectories.
    base_heading_level : int
        Base heading level for the assembled report (default 1).
        A ``#`` heading in a depth_level=0 section stays at level
        ``base_heading_level``.

    Returns
    -------
    Path
        Path to the assembled report file.

    Raises
    ------
    FileNotFoundError
        If a section's draft file cannot be found.

    Supports
    --------
    FR-26 : Heading hierarchy adjusted per depth_level.
    FR-27 : Assembly produces the final output document.
    NFR-04 : Deterministic output path.
    """
    assembled_parts: List[str] = []

    for section in report_plan.sections:
        section_dir = output_dir / "sections" / section.section_id
        draft_path = _find_latest_draft(section_dir)

        if draft_path is None:
            logger.warning(
                "No draft found for section '%s' in %s. "
                "Including placeholder.",
                section.section_id,
                section_dir,
            )
            # Include a placeholder for missing sections (e.g., escalated sections
            # that may not have a clean draft)
            adjusted_heading = "#" * max(1, min(6, section.depth_level + base_heading_level)) + f" {section.title}"
            assembled_parts.append(
                f"{adjusted_heading}\n\n"
                f"*[Section content unavailable — section was escalated or missing]*\n"
            )
            continue

        raw_content = draft_path.read_text(encoding="utf-8")

        # Adjust heading levels based on depth_level
        adjusted_content = _adjust_heading_levels(
            content=raw_content,
            depth_level=section.depth_level,
            base_heading_level=base_heading_level,
        )

        assembled_parts.append(adjusted_content)
        logger.debug(
            "Assembled section '%s' (depth_level=%d) from %s",
            section.section_id,
            section.depth_level,
            draft_path,
        )

    # Join sections with double newlines
    full_report = "\n\n".join(assembled_parts)

    # Write to output_dir/report/literature_review.md
    report_dir = output_dir / "report"
    os.makedirs(report_dir, exist_ok=True)
    report_path = report_dir / "literature_review.md"
    report_path.write_text(full_report, encoding="utf-8")

    logger.info(
        "Assembled report written to %s (%d sections, %d characters)",
        report_path,
        len(report_plan.sections),
        len(full_report),
    )

    return report_path