# synthesizer/models/section_output.py
"""Section output Pydantic models (§10.8, §10.9).

Base SectionOutput and four per-type subclasses:
  - NarrativeSynthesisOutput
  - EvidenceTableOutput
  - CrossReferenceOutput
  - MethodologyDescriptionOutput

Supports: FR-13, FR-14, FR-26.
"""

from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.enums import SectionType


class SectionOutput(BaseModel):
    """Base model for generated section content (§10.8).

    Extended by per-type models (§10.9).
    Supports: FR-13, FR-14, FR-26.
    """

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(
        ...,
        description="Must match the SectionNode.section_id.",
    )
    content_markdown: str = Field(
        ...,
        min_length=1,
        description="Generated Markdown content.",
    )
    word_count: int = Field(
        ...,
        ge=1,
        description="Word count of content_markdown.",
    )
    heading_level: int = Field(
        ...,
        ge=1,
        le=6,
        description="Markdown heading level (1-6). Derived from depth_level.",
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Generation metadata (model, timestamp, etc.).",
    )


class NarrativeSynthesisOutput(SectionOutput):
    """Output for narrative_synthesis sections (§10.9).

    Extends base with synthesis-specific fields.
    Supports: FR-13.
    """

    themes_addressed: List[str] = Field(
        default_factory=list,
        description="Thematic tags covered in this section.",
    )
    cross_references: List[str] = Field(
        default_factory=list,
        description="section_ids referenced in the text.",
    )


class EvidenceTableOutput(SectionOutput):
    """Output for evidence_table sections (§10.9).

    Extends base with tabular structure.
    Supports: FR-13.
    """

    column_definitions: List[str] = Field(
        ...,
        min_length=1,
        description="Column headers for the evidence table.",
    )
    rows: List[Dict[str, str]] = Field(
        ...,
        description="Table rows as column→value mappings.",
    )


class CrossReferenceOutput(SectionOutput):
    """Output for cross_reference sections (§10.9).

    Extends base with reference mapping.
    Supports: FR-13.
    """

    referenced_sections: List[str] = Field(
        ...,
        min_length=1,
        description="section_ids this section cross-references.",
    )
    comparison_dimensions: List[str] = Field(
        default_factory=list,
        description="Dimensions along which sections are compared.",
    )


class MethodologyDescriptionOutput(SectionOutput):
    """Output for methodology_description sections (§10.9).

    Extends base with methodology fields.
    Supports: FR-13.
    """

    methodologies_described: List[str] = Field(
        default_factory=list,
        description="Named methodologies covered.",
    )
    equations_referenced: List[str] = Field(
        default_factory=list,
        description="LaTeX equation strings referenced.",
    )


# ---------------------------------------------------------------------------
# FR-13  Section-type dispatch registry
# ---------------------------------------------------------------------------

SECTION_TYPE_TO_OUTPUT_MODEL: Dict[SectionType, type[SectionOutput]] = {
    SectionType.NARRATIVE_SYNTHESIS: NarrativeSynthesisOutput,
    SectionType.EVIDENCE_TABLE: EvidenceTableOutput,
    SectionType.CROSS_REFERENCE: CrossReferenceOutput,
    SectionType.METHODOLOGY_DESCRIPTION: MethodologyDescriptionOutput,
}
"""Maps SectionType enum → corresponding SectionOutput subclass (FR-13)."""


def get_output_model(section_type: SectionType) -> type[SectionOutput]:
    """Return the SectionOutput subclass for a given section type (FR-13).

    Parameters
    ----------
    section_type : SectionType
        The section type from the report plan.

    Returns
    -------
    type[SectionOutput]
        The Pydantic model class for the section type's output.

    Raises
    ------
    ValueError
        If the section type has no registered output model.
    """
    model = SECTION_TYPE_TO_OUTPUT_MODEL.get(section_type)
    if model is None:
        raise ValueError(
            f"No output model registered for section type '{section_type.value}'. "
            f"Known types: {sorted(t.value for t in SECTION_TYPE_TO_OUTPUT_MODEL)}"
        )
    return model


def get_output_schema_json(section_type: SectionType) -> str:
    """Return a JSON-schema string for the output model of a section type.

    Used in prompt assembly to instruct the LLM on the expected output
    format (FR-13, §9.2.1).

    Parameters
    ----------
    section_type : SectionType
        The section type.

    Returns
    -------
    str
        Pretty-printed JSON schema string.
    """
    import json

    model = get_output_model(section_type)
    schema = model.model_json_schema()
    return json.dumps(schema, indent=2)