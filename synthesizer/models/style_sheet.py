# synthesizer/models/style_sheet.py
"""Style sheet Pydantic models (§10.5).

Supports: FR-04, FR-05, FR-16.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from synthesizer.models.enums import SectionType


class EquationDelimiters(BaseModel):
    """LaTeX equation delimiter configuration (§10.5)."""

    model_config = ConfigDict(extra="forbid")

    inline: str = Field(
        default="$",
        description="Inline equation delimiter.",
    )
    display: str = Field(
        default="$$",
        description="Display equation delimiter.",
    )


class LevelConstraint(BaseModel):
    """Per-depth-level formatting constraints (§10.5)."""

    model_config = ConfigDict(extra="forbid")

    min_words: int = Field(
        ...,
        ge=0,
        description="Minimum word count. Constraint: ≥0.",
    )
    max_words: int = Field(
        ...,
        gt=0,
        description="Maximum word count. Constraint: > min_words.",
    )
    heading_format: str = Field(
        ...,
        min_length=1,
        description='Markdown heading format (e.g., "##", "###").',
    )

    @model_validator(mode="after")
    def check_max_greater_than_min(self) -> LevelConstraint:
        """Enforce max_words > min_words as required by §10.5."""
        if self.max_words <= self.min_words:
            raise ValueError(
                f"max_words ({self.max_words}) must be greater than "
                f"min_words ({self.min_words})"
            )
        return self


class StyleSheet(BaseModel):
    """Formatting and tone rules applied during generation and validation (§10.5).

    Tier 2 source of truth (§7).
    Supports: FR-04, FR-05, FR-16.
    """

    model_config = ConfigDict(extra="forbid")

    citation_pattern: str = Field(
        ...,
        description=(
            "Regex pattern for valid citations "
            '(e.g., r"\\([A-Z][a-z]+ et al\\., \\d{4}\\)").'
        ),
    )
    tone_register: str = Field(
        ...,
        min_length=1,
        description='Tone descriptor (e.g., "formal_academic", "technical_review").',
    )
    per_level_constraints: Dict[int, LevelConstraint] = Field(
        ...,
        description="Maps depth_level → constraints.",
    )
    per_type_overrides: Dict[SectionType, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Type-specific rule overrides.",
    )
    forbidden_phrases: List[str] = Field(
        default_factory=list,
        description="Phrases that must not appear in generated text.",
    )
    equation_delimiters: EquationDelimiters = Field(
        default_factory=EquationDelimiters,
        description="LaTeX delimiter config.",
    )

    @field_validator("citation_pattern")
    @classmethod
    def validate_citation_pattern_is_compilable(cls, v: str) -> str:
        """FR-04: Validate that citation_pattern is a compilable regex."""
        try:
            re.compile(v)
        except re.error as exc:
            raise ValueError(
                f"citation_pattern is not a valid regex: {exc}"
            ) from exc
        return v