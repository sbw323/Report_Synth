# synthesizer/models/validation.py
"""Validation models (§10.10) — Sprint 4 canonical import path.

Re-exports ValidationResult and Violation from the existing
validation_models module (created in Sprint 1) to satisfy the
sprint artifact requirement while maintaining backward compatibility.

Supports: FR-14 through FR-19.
"""

from __future__ import annotations

from synthesizer.models.validation_models import ValidationResult, Violation

__all__ = ["ValidationResult", "Violation"]