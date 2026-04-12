# synthesizer/loaders/plan_loader.py
"""Report plan loader (§7, §10.2–10.4).

Loads a JSON report plan from disk, parses it into a validated ReportPlan
object, and runs cross-section validations (FR-01, FR-02, FR-03).

Source-of-truth hierarchy (§7):
  Tier 1 — Report Plan (highest authority)
  Tier 2 — Style Sheet
  Tier 3 — Directory Tree (derived, never canonical)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from synthesizer.config import REPORT_PLAN_PATH
from synthesizer.models.report_plan import ReportPlan
from synthesizer.validation.graph_validation import (
    validate_dependency_references,
    validate_depth_levels,
    validate_no_content_cycles,
)


class ReportPlanLoadError(Exception):
    """Raised when report plan loading or validation fails.

    Wraps Pydantic ValidationError, JSON decode errors, and
    graph-validation errors with descriptive context.
    """


def load_report_plan(path: Optional[Path] = None) -> ReportPlan:
    """Load and fully validate a report plan from a JSON file.

    Performs, in order:
      1. File read and JSON parse
      2. Pydantic schema validation (FR-01)
      3. Dependency-reference validation — all section_ids in
         dependency_edges must exist (FR-02)
      4. Content-cycle detection — no cycles among CONTENT edges (FR-03)
      5. Depth-level consistency — each section's depth_level must match
         its ancestor-chain length

    Parameters
    ----------
    path : Path, optional
        Explicit path to the report plan JSON. If *None*, falls back to
        ``REPORT_PLAN_PATH`` from the synthesizer config (§16).

    Returns
    -------
    ReportPlan
        Fully validated report plan.

    Raises
    ------
    ReportPlanLoadError
        On any validation or I/O failure, with a descriptive message.
    """
    resolved_path = path or REPORT_PLAN_PATH
    if resolved_path is None:
        raise ReportPlanLoadError(
            "No report plan path provided and REPORT_PLAN_PATH is not "
            "configured. Set the REPORT_PLAN_PATH environment variable "
            "or pass an explicit path."
        )

    resolved_path = Path(resolved_path)

    # 1. File read + JSON parse
    try:
        raw_text = resolved_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ReportPlanLoadError(
            f"Report plan file not found: {resolved_path}"
        ) from exc
    except OSError as exc:
        raise ReportPlanLoadError(
            f"Failed to read report plan file {resolved_path}: {exc}"
        ) from exc

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ReportPlanLoadError(
            f"Report plan is not valid JSON: {exc}"
        ) from exc

    # 2. Pydantic schema validation (FR-01)
    try:
        plan = ReportPlan.model_validate(data)
    except ValidationError as exc:
        raise ReportPlanLoadError(
            f"Report plan schema validation failed:\n{exc}"
        ) from exc

    # 3. Dependency-reference validation (FR-02)
    try:
        validate_dependency_references(plan)
    except ValueError as exc:
        raise ReportPlanLoadError(str(exc)) from exc

    # 4. Content-cycle detection (FR-03)
    try:
        validate_no_content_cycles(plan)
    except ValueError as exc:
        raise ReportPlanLoadError(str(exc)) from exc

    # 5. Depth-level consistency
    try:
        validate_depth_levels(plan)
    except ValueError as exc:
        raise ReportPlanLoadError(str(exc)) from exc

    return plan