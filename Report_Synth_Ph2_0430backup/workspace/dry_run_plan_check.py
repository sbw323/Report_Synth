# dry_run_plan_check.py
"""Pre-flight check for a new report plan + style sheet.

Exercises the same loaders the orchestrator calls, plus a depth ↔
per_level_constraints cross-check that the loaders don't enforce.
Does NOT call the LLM, the retriever, or touch the vectorstore.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from synthesizer.loaders.plan_loader import load_report_plan, ReportPlanLoadError
from synthesizer.loaders.style_loader import load_style_sheet, StyleSheetLoadError
from synthesizer.dag import build_generation_dag, build_finalization_dag, iter_topological


def _die(msg: str) -> None:
    print(f"[FAIL] {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    plan_path = Path(os.environ["REPORT_PLAN_PATH"])
    style_path = Path(os.environ["STYLE_SHEET_PATH"])
    print(f"Report plan:  {plan_path}")
    print(f"Style sheet:  {style_path}\n")

    # 1. Load + validate the plan (FR-01, FR-02, FR-03, depth consistency)
    try:
        plan = load_report_plan(plan_path)
    except ReportPlanLoadError as exc:
        _die(f"Report plan failed to load:\n{exc}")
    print(f"[ OK ] Plan '{plan.plan_id}' v{plan.version} loaded — "
          f"{len(plan.sections)} sections")

    # 2. Load + validate the style sheet (FR-04, citation regex compiles)
    try:
        style = load_style_sheet(style_path)
    except StyleSheetLoadError as exc:
        _die(f"Style sheet failed to load:\n{exc}")
    print(f"[ OK ] Style sheet loaded — tone='{style.tone_register}', "
          f"citation_pattern={style.citation_pattern!r}")

    # 3. Build both DAGs and compute topological order (FR-06)
    gen_dag = build_generation_dag(plan)
    fin_dag = build_finalization_dag(plan)
    topo = list(iter_topological(gen_dag))
    print(f"[ OK ] DAGs built — generation edges={len(gen_dag.edges)}, "
          f"finalization edges={len(fin_dag.edges)}")
    print(f"[ OK ] Topological order ({len(topo)} sections):")
    for i, sid in enumerate(topo, 1):
        print(f"         {i:>2}. {sid}")

    # 4. Cross-check depth ↔ per_level_constraints (the loaders validate
    #    these independently but not against each other)
    plan_depths = {s.depth_level for s in plan.sections}
    style_levels = set(style.per_level_constraints.keys())
    missing = plan_depths - style_levels
    if missing:
        _die(f"Plan uses depth levels {sorted(missing)} that have no "
             f"per_level_constraints entry in the style sheet.")
    print(f"[ OK ] All plan depth levels {sorted(plan_depths)} covered by "
          f"style sheet per_level_constraints")

    # 5. Cross-check section_type ↔ per_type_overrides (advisory, not fatal)
    plan_types = {s.section_type for s in plan.sections}
    override_types = set(style.per_type_overrides.keys())
    unused = override_types - plan_types
    if unused:
        print(f"[WARN] per_type_overrides defines entries not used by this "
              f"plan: {sorted(unused)}")

    print("\nDry run passed. Safe to invoke 'python -m synthesizer'.")


if __name__ == "__main__":
    main()