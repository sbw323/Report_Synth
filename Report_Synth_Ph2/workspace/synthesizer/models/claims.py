# synthesizer/models/claims.py
"""Claim table Pydantic models (§10.6, §10.7).

These models are required by SectionState (§10.12) which stores
claim_table: Optional[ClaimTable].

Supports: FR-20, FR-21, FR-22, FR-11.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field, model_validator

from synthesizer.models.enums import ConfidenceTag


class TextSpan(BaseModel):
    """Character offset range within a text (§10.6).

    Supports: FR-20, FR-21.
    """

    model_config = ConfigDict(extra="forbid")

    start: int = Field(
        ...,
        ge=0,
        description="Start character offset (0-indexed, inclusive).",
    )
    end: int = Field(
        ...,
        gt=0,
        description="End character offset (exclusive). Must be > start.",
    )

    @model_validator(mode="after")
    def check_end_greater_than_start(self) -> TextSpan:
        """Enforce end > start as required by §10.6."""
        if self.end <= self.start:
            raise ValueError(
                f"end ({self.end}) must be greater than start ({self.start})"
            )
        return self


class ClaimEntry(BaseModel):
    """Single claim extracted from a finalized section (§10.6).

    Supports: FR-20, FR-21.
    """

    model_config = ConfigDict(extra="forbid")

    claim_id: str = Field(
        ...,
        pattern=r"^claim_[0-9]+$",
        description="Unique within the parent ClaimTable. Pattern: claim_[0-9]+.",
    )
    claim_text: str = Field(
        ...,
        min_length=1,
        description="The claim statement as extracted.",
    )
    source_chunk_ids: List[str] = Field(
        ...,
        min_length=1,
        description="Chunk IDs from retrieval that support this claim.",
    )
    confidence_tag: ConfidenceTag = Field(
        ...,
        description="Classification of claim confidence.",
    )
    section_text_span: TextSpan = Field(
        ...,
        description="Character offsets locating the claim in section text.",
    )


class ClaimTable(BaseModel):
    """Collection of claims for a section (§10.7).

    Primary context channel for downstream sections (§13).
    Supports: FR-20, FR-21, FR-22, FR-11.
    """

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(
        ...,
        description="Section this claim table belongs to.",
    )
    version: int = Field(
        ...,
        ge=1,
        description="Extraction version (increments on re-extraction).",
    )
    claims: List[ClaimEntry] = Field(
        ...,
        description="Extracted claims.",
    )
    partial: bool = Field(
        default=False,
        description="Whether extraction was incomplete (DR-14).",
    )
    extraction_attempt: int = Field(
        ...,
        ge=1,
        description="Which attempt produced this table.",
    )