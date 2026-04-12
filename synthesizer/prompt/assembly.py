# synthesizer/prompt/assembly.py
"""Full generation prompt assembly per §9.2.1.

Composes system prompt + user message for the Generator role, including
all five context channels:
  1. Section description and type (from ReportPlan)
  2. Retrieved chunks (from Stage 05 via retrieval adapter)
  3. Upstream claim tables (for content dependencies, §13.1)
  4. Upstream summary abstracts (for thematic dependencies, §13.2)
  5. Style sheet constraints (from StyleSheet)

Plus a retry-error feedback slot for re-generation attempts.

Enforced exclusions:
  - FR-10 / DR-05: No Stage 05 answer text
  - FR-12 / DR-03: No raw upstream content_markdown
  - DR-06: No Stage 06 PaperSummary data in generation prompts

DR-18 remains open: input token budgets per prompt role are not enforced
here. Prompt assembly produces the complete prompt; token budget enforcement
is deferred to the orchestrator/caller.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.claims import ClaimTable
from synthesizer.models.enums import SectionType
from synthesizer.models.report_plan import SectionNode
from synthesizer.models.section_output import (
    get_output_model,
    get_output_schema_json,
)
from synthesizer.models.style_sheet import StyleSheet
from synthesizer.prompt.context_channels import (
    package_claim_tables,
    package_evidence_chunks,
    package_retry_errors,
    package_style_constraints,
    package_summary_abstracts,
)
from synthesizer.retrieval.adapter import RankedChunk


# ---------------------------------------------------------------------------
# Prompt data container
# ---------------------------------------------------------------------------

class GenerationPrompt(BaseModel):
    """Assembled generation prompt ready for LLM invocation (§9.2.1).

    Contains the system prompt, user message, and metadata needed
    by the orchestrator to dispatch the LLM call.
    """

    model_config = ConfigDict(extra="forbid")

    system_prompt: str = Field(
        ...,
        description="System-level instructions for the Generator.",
    )
    user_message: str = Field(
        ...,
        description="User-level message with all context channels.",
    )
    section_id: str = Field(
        ...,
        description="The section being generated.",
    )
    section_type: SectionType = Field(
        ...,
        description="Type of the section being generated.",
    )
    expected_output_model_name: str = Field(
        ...,
        description="Name of the expected SectionOutput subclass (FR-13).",
    )
    max_output_tokens: int = Field(
        default=4000,
        description="Output token cap for Generator (§9.2.1, partially open DR-18).",
    )


# ---------------------------------------------------------------------------
# System prompt construction
# ---------------------------------------------------------------------------

def _build_system_prompt(
    section_type: SectionType,
    style: StyleSheet,
    depth_level: int,
) -> str:
    """Construct the Generator system prompt (§9.2.1).

    System prompt content per spec:
      - Role as scientific literature review writer
      - Output format instructions referencing the target SectionOutput subclass
      - Style sheet constraints (tone, citation format, word limits, forbidden phrases)
      - Equation delimiter configuration
    """
    output_model = get_output_model(section_type)
    output_schema = get_output_schema_json(section_type)

    level_constraint = style.per_level_constraints.get(depth_level)
    word_constraint_text = ""
    if level_constraint:
        word_constraint_text = (
            f"Word count: {level_constraint.min_words}–{level_constraint.max_words} words.\n"
            f"Heading format: {level_constraint.heading_format}\n"
        )

    type_override_text = ""
    type_overrides = style.per_type_overrides.get(section_type)
    if type_overrides:
        type_override_text = (
            f"\nType-specific overrides for '{section_type.value}':\n"
            f"{type_overrides}\n"
        )

    forbidden_text = ""
    if style.forbidden_phrases:
        phrases = ", ".join(repr(p) for p in style.forbidden_phrases)
        forbidden_text = f"\nForbidden phrases (NEVER use): {phrases}\n"

    return (
        "You are a scientific literature review writer. Your task is to "
        "generate a section of a structured literature review based on "
        "evidence chunks retrieved from source documents and structured "
        "context from upstream sections.\n\n"
        "OUTPUT FORMAT:\n"
        f"You MUST produce valid JSON conforming to the {output_model.__name__} schema.\n"
        f"Schema:\n{output_schema}\n\n"
        "STYLE REQUIREMENTS:\n"
        f"Tone register: {style.tone_register}\n"
        f"Citation format (regex pattern): {style.citation_pattern}\n"
        f"{word_constraint_text}"
        f"Equation delimiters: inline={style.equation_delimiters.inline}, "
        f"display={style.equation_delimiters.display}\n"
        f"{forbidden_text}"
        f"{type_override_text}"
        "CRITICAL RULES:\n"
        "- Ground ALL claims in the provided evidence chunks.\n"
        "- Use the citation format specified above.\n"
        "- Stay within the word count limits.\n"
        "- Engage with upstream claim tables when provided.\n"
        "- Do NOT fabricate references or evidence.\n"
        "- Produce valid JSON only — no markdown fences around the JSON.\n"
    )


# ---------------------------------------------------------------------------
# User message construction
# ---------------------------------------------------------------------------

def _build_user_message(
    section: SectionNode,
    evidence_text: str,
    claim_tables_text: str,
    summary_abstracts_text: str,
    style_constraints_text: str,
    retry_errors_text: str,
) -> str:
    """Construct the Generator user message with all context channels (§9.2.1).

    User message composition per spec:
      1. Section description and type from the report plan
      2. Retrieved chunks from Stage 05
      3. Upstream claim tables for content dependencies
      4. Upstream summary abstracts for thematic dependencies
      5. Style sheet constraints relevant to this section's type and depth level
      6. On retry: validation error list from the failing layer
    """
    parts: List[str] = []

    # 1. Section description and type
    parts.append("=== SECTION TO GENERATE ===")
    parts.append(f"Section ID: {section.section_id}")
    parts.append(f"Section title: {section.title}")
    parts.append(f"Section type: {section.section_type.value}")
    parts.append(f"Depth level: {section.depth_level}")
    parts.append(f"Description: {section.description}")
    parts.append("=== END SECTION DESCRIPTION ===\n")

    # 2. Retrieved chunks (evidence pointers — §13.3)
    if evidence_text:
        parts.append(evidence_text)
        parts.append("")

    # 3. Upstream claim tables (§13.1)
    if claim_tables_text:
        parts.append(claim_tables_text)
        parts.append("")

    # 4. Upstream summary abstracts (§13.2)
    if summary_abstracts_text:
        parts.append(summary_abstracts_text)
        parts.append("")

    # 5. Style constraints
    if style_constraints_text:
        parts.append(style_constraints_text)
        parts.append("")

    # 6. Retry errors (if re-generating after validation failure)
    if retry_errors_text:
        parts.append(retry_errors_text)
        parts.append("")

    parts.append(
        "Please generate the section content as valid JSON conforming to "
        "the schema specified in the system instructions."
    )

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# FR-11  Full prompt assembly
# ---------------------------------------------------------------------------

def assemble_generation_prompt(
    section: SectionNode,
    style: StyleSheet,
    retrieved_chunks: List[RankedChunk],
    upstream_claim_tables: Optional[Dict[str, ClaimTable]] = None,
    upstream_summary_abstracts: Optional[Dict[str, str]] = None,
    retry_errors: Optional[List[str]] = None,
    retry_layer: Optional[str] = None,
) -> GenerationPrompt:
    """Assemble a complete generation prompt for a section (FR-11, §9.2.1).

    Composes the system prompt and user message with all five context
    channels from §9.2.1, plus optional retry error feedback.

    Parameters
    ----------
    section : SectionNode
        The section to generate. Provides description, type, depth_level,
        and section_id.
    style : StyleSheet
        The style sheet with formatting and tone constraints.
    retrieved_chunks : list of RankedChunk
        Evidence chunks from Stage 05 retrieval (§13.3). Answer text
        has already been discarded by the retrieval adapter (FR-10).
    upstream_claim_tables : dict, optional
        Maps upstream section_id → ClaimTable for content dependencies
        (§13.1). None or empty dict if no content deps.
    upstream_summary_abstracts : dict, optional
        Maps upstream section_id → summary abstract string for thematic
        dependencies (§13.2). None or empty dict if no thematic deps.
    retry_errors : list of str, optional
        Validation error descriptions from a previous attempt (FR-15, FR-17).
    retry_layer : str, optional
        Name of the validation layer that failed (for error context).

    Returns
    -------
    GenerationPrompt
        Fully assembled prompt ready for LLM dispatch.

    Raises
    ------
    ValueError
        If the section type has no registered output model.

    Enforced exclusions
    -------------------
    FR-10 / DR-05 : answer_text is never present — it was discarded
        at the retrieval adapter layer. This function receives only
        RankedChunk objects, not raw Stage 05 output.
    FR-12 / DR-03 : raw upstream content_markdown is never included.
        Upstream context is provided exclusively via claim tables
        (structured ClaimTable objects) and summary abstracts
        (2-3 sentence strings), never as raw prose.
    DR-06 : Stage 06 PaperSummary data is never included in generation
        prompts. It is consumed by the planning context loader only.
    """
    claim_tables = upstream_claim_tables or {}
    abstracts = upstream_summary_abstracts or {}
    errors = retry_errors or []
    layer = retry_layer or ""

    # Resolve output model for this section type (FR-13)
    output_model = get_output_model(section.section_type)

    # Get level constraints for style packaging
    level_constraint = style.per_level_constraints.get(section.depth_level)
    type_overrides = style.per_type_overrides.get(section.section_type)

    # Package all context channels
    evidence_text = package_evidence_chunks(retrieved_chunks)
    claim_tables_text = package_claim_tables(claim_tables)
    summary_abstracts_text = package_summary_abstracts(abstracts)
    style_constraints_text = package_style_constraints(
        tone_register=style.tone_register,
        citation_pattern=style.citation_pattern,
        forbidden_phrases=style.forbidden_phrases,
        min_words=level_constraint.min_words if level_constraint else None,
        max_words=level_constraint.max_words if level_constraint else None,
        heading_format=level_constraint.heading_format if level_constraint else None,
        equation_inline=style.equation_delimiters.inline,
        equation_display=style.equation_delimiters.display,
        per_type_overrides=type_overrides,
    )
    retry_errors_text = package_retry_errors(errors, layer) if errors else ""

    # Build system prompt
    system_prompt = _build_system_prompt(
        section_type=section.section_type,
        style=style,
        depth_level=section.depth_level,
    )

    # Build user message
    user_message = _build_user_message(
        section=section,
        evidence_text=evidence_text,
        claim_tables_text=claim_tables_text,
        summary_abstracts_text=summary_abstracts_text,
        style_constraints_text=style_constraints_text,
        retry_errors_text=retry_errors_text,
    )

    return GenerationPrompt(
        system_prompt=system_prompt,
        user_message=user_message,
        section_id=section.section_id,
        section_type=section.section_type,
        expected_output_model_name=output_model.__name__,
        max_output_tokens=4000,  # §9.2.1 output token cap
    )