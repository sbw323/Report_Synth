# synthesizer/loaders/style_loader.py
"""Style sheet loader (§7, §10.5).

Loads a JSON style sheet from disk, parses it into a validated StyleSheet
object (FR-04). Citation pattern regex compilation is enforced by the
StyleSheet model's field validator.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from synthesizer.config import STYLE_SHEET_PATH
from synthesizer.models.style_sheet import StyleSheet


class StyleSheetLoadError(Exception):
    """Raised when style sheet loading or validation fails.

    Wraps Pydantic ValidationError, JSON decode errors, and
    regex-compilation errors with descriptive context.
    """


def load_style_sheet(path: Optional[Path] = None) -> StyleSheet:
    """Load and validate a style sheet from a JSON file.

    Performs, in order:
      1. File read and JSON parse
      2. Pydantic schema validation, including citation_pattern regex
         compilation check (FR-04)

    Parameters
    ----------
    path : Path, optional
        Explicit path to the style sheet JSON. If *None*, falls back to
        ``STYLE_SHEET_PATH`` from the synthesizer config (§16).

    Returns
    -------
    StyleSheet
        Fully validated style sheet.

    Raises
    ------
    StyleSheetLoadError
        On any validation or I/O failure, with a descriptive message.
    """
    resolved_path = path or STYLE_SHEET_PATH
    if resolved_path is None:
        raise StyleSheetLoadError(
            "No style sheet path provided and STYLE_SHEET_PATH is not "
            "configured. Set the STYLE_SHEET_PATH environment variable "
            "or pass an explicit path."
        )

    resolved_path = Path(resolved_path)

    # 1. File read + JSON parse
    try:
        raw_text = resolved_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise StyleSheetLoadError(
            f"Style sheet file not found: {resolved_path}"
        ) from exc
    except OSError as exc:
        raise StyleSheetLoadError(
            f"Failed to read style sheet file {resolved_path}: {exc}"
        ) from exc

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise StyleSheetLoadError(
            f"Style sheet is not valid JSON: {exc}"
        ) from exc

    # 2. Pydantic schema validation (FR-04)
    #    citation_pattern regex compilation is enforced by the
    #    StyleSheet model's field_validator.
    try:
        style_sheet = StyleSheet.model_validate(data)
    except ValidationError as exc:
        raise StyleSheetLoadError(
            f"Style sheet schema validation failed:\n{exc}"
        ) from exc

    return style_sheet