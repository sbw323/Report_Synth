# synthesizer/config.py
"""Synthesizer configuration surface (§16).

Adds synthesizer-specific keys per §16 table. Does not modify existing
pipeline keys. Reads from environment variables where set; falls back
to documented defaults.

Open decisions preserved as configurable:
  - DR-16: SYNTHESIZER_MODEL defaults to PIPELINE_MODEL (open — may differ per role)
  - DR-17: TOKEN_BUDGET_CEILING defaults to None (open — no limit)
  - DR-18: Per-role input token budgets remain open (not defined here)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Import pipeline-level constants from existing config, with safe fallbacks.
# The synthesizer wraps (never refactors) the existing pipeline (§14.2).
# ---------------------------------------------------------------------------
try:
    from config import DATA_DIR as _PIPELINE_DATA_DIR  # type: ignore[import-untyped]
except ImportError:
    _PIPELINE_DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))

try:
    from config import PIPELINE_MODEL as _PIPELINE_MODEL  # type: ignore[import-untyped]
except ImportError:
    _PIPELINE_MODEL = os.environ.get("PIPELINE_MODEL", "claude-sonnet-4-20250514")


# ---------------------------------------------------------------------------
# §16  Synthesizer configuration keys
# ---------------------------------------------------------------------------

# Required — no default; None signals "not yet configured".
REPORT_PLAN_PATH: Optional[Path] = (
    Path(os.environ["REPORT_PLAN_PATH"])
    if "REPORT_PLAN_PATH" in os.environ
    else None
)

STYLE_SHEET_PATH: Optional[Path] = (
    Path(os.environ["STYLE_SHEET_PATH"])
    if "STYLE_SHEET_PATH" in os.environ
    else None
)

# Optional — documented defaults from §16.
SYNTHESIZER_OUTPUT_DIR: Path = Path(
    os.environ.get(
        "SYNTHESIZER_OUTPUT_DIR",
        str(_PIPELINE_DATA_DIR / "synthesis"),
    )
)

CASCADE_DEPTH_LIMIT: int = int(
    os.environ.get("CASCADE_DEPTH_LIMIT", "3")
)

LAYER1_RETRY_LIMIT: int = int(
    os.environ.get("LAYER1_RETRY_LIMIT", "3")
)

LAYER2_RETRY_LIMIT: int = int(
    os.environ.get("LAYER2_RETRY_LIMIT", "3")
)

LAYER3_RETRY_LIMIT: int = int(
    os.environ.get("LAYER3_RETRY_LIMIT", "2")
)

CLAIM_EXTRACTION_RETRY_LIMIT: int = int(
    os.environ.get("CLAIM_EXTRACTION_RETRY_LIMIT", "1")
)

# DR-16 (open): Model selection per role. Currently a single configurable
# key. May be split per-role in a future sprint after benchmarking.
SYNTHESIZER_MODEL: str = os.environ.get(
    "SYNTHESIZER_MODEL", _PIPELINE_MODEL
)

# DR-17 (open): Token budget ceiling per run. None = no limit.
TOKEN_BUDGET_CEILING: Optional[int] = (
    int(os.environ["TOKEN_BUDGET_CEILING"])
    if "TOKEN_BUDGET_CEILING" in os.environ
    else None
)