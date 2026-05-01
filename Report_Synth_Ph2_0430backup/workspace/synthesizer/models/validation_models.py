# synthesizer/models/validation_models.py
"""Validation result Pydantic models (§10.10).

These models are required by SectionState (§10.12) which stores
validation_history: List[ValidationResult].

Supports: FR-14 through FR-19.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.enums import ValidationLayer, ViolationSeverity


class Violation(BaseModel):
    """Single validation violation (§10.10).

    Supports: FR-14, FR-16, FR-18.
    """

    model_config = ConfigDict(extra="forbid")

    rule: str = Field(
        ...,
        min_length=1,
        description="Rule identifier (e.g., 'word_count_max', 'tone_formal').",
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Human-readable description of the violation.",
    )
    severity: ViolationSeverity = Field(
        ...,
        description="Error or warning.",
    )
    location: Optional[str] = Field(
        default=None,
        description="Character offset or field path where violation occurs.",
    )


class ValidationResult(BaseModel):
    """Output of a single validation pass (§10.10).

    See §12 for layer semantics.
    Supports: FR-14 through FR-19.
    """

    model_config = ConfigDict(extra="forbid")

    layer: ValidationLayer = Field(
        ...,
        description="Which validation layer produced this result.",
    )
    passed: bool = Field(
        ...,
        description="Whether validation passed.",
    )
    attempt: int = Field(
        ...,
        ge=1,
        description="Attempt number within this layer.",
    )
    violations: List[Violation] = Field(
        default_factory=list,
        description="Violations found (empty if passed).",
    )
    suggested_fix: Optional[str] = Field(
        default=None,
        description="LLM-suggested fix text (Layer 3 only).",
    )