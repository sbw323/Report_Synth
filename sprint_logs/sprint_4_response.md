Looking at the sprint requirements, I need to implement the three-layer validation pipeline, retry/escalation logic, and coordinator. Let me trace through all the spec sections and build each component.

### `synthesizer/models/validation.py`
```python
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
```

### `synthesizer/validation/layer1_structural.py`
```python
# synthesizer/validation/layer1_structural.py
"""Layer 1 — Structural validation (§12.1, FR-14).

Deterministic. Validates that the Generator's raw JSON output conforms
to the type-specific SectionOutput schema (§10.8–10.9) via Pydantic.
Returns field-level errors on failure.

No LLM call.
"""

from __future__ import annotations

import json
from typing import List, Optional, Tuple

from pydantic import ValidationError

from synthesizer.models.enums import SectionType, ValidationLayer, ViolationSeverity
from synthesizer.models.section_output import SectionOutput, get_output_model
from synthesizer.models.validation_models import ValidationResult, Violation


def validate_layer1(
    raw_json: str,
    section_type: SectionType,
    section_id: str,
    attempt: int = 1,
) -> Tuple[ValidationResult, Optional[SectionOutput]]:
    """Run Layer 1 structural validation on raw Generator output (FR-14).

    Attempts to:
      1. Parse raw_json as JSON
      2. Validate the parsed dict against the type-specific
         SectionOutput Pydantic model (§10.8–10.9)
      3. Verify section_id matches

    Parameters
    ----------
    raw_json : str
        Raw JSON string from the Generator LLM call.
    section_type : SectionType
        The section's type — determines which SectionOutput subclass
        to validate against (FR-13).
    section_id : str
        Expected section_id. Checked against the output's section_id field.
    attempt : int
        Current validation attempt number (≥1).

    Returns
    -------
    (ValidationResult, Optional[SectionOutput])
        The validation result and, if successful, the parsed SectionOutput.
        On failure, the SectionOutput is None.

    Notes
    -----
    §12.1: On failure, error list includes field names, expected types,
    and actual values. These are appended to the Generator retry prompt
    via the retry module (FR-15).
    """
    violations: List[Violation] = []

    # Step 1: JSON parse
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        violations.append(Violation(
            rule="json_parse",
            description=f"Output is not valid JSON: {exc}",
            severity=ViolationSeverity.ERROR,
            location=f"character {exc.pos}" if hasattr(exc, "pos") else None,
        ))
        return (
            ValidationResult(
                layer=ValidationLayer.STRUCTURAL,
                passed=False,
                attempt=attempt,
                violations=violations,
            ),
            None,
        )

    if not isinstance(data, dict):
        violations.append(Violation(
            rule="json_type",
            description=f"Expected a JSON object (dict), got {type(data).__name__}.",
            severity=ViolationSeverity.ERROR,
        ))
        return (
            ValidationResult(
                layer=ValidationLayer.STRUCTURAL,
                passed=False,
                attempt=attempt,
                violations=violations,
            ),
            None,
        )

    # Step 2: Pydantic model validation
    output_model = get_output_model(section_type)

    try:
        parsed = output_model.model_validate(data)
    except ValidationError as exc:
        for error in exc.errors():
            field_path = " → ".join(str(loc) for loc in error["loc"])
            violations.append(Violation(
                rule="schema_field",
                description=(
                    f"Field '{field_path}': {error['msg']} "
                    f"(type={error['type']})"
                ),
                severity=ViolationSeverity.ERROR,
                location=field_path,
            ))
        return (
            ValidationResult(
                layer=ValidationLayer.STRUCTURAL,
                passed=False,
                attempt=attempt,
                violations=violations,
            ),
            None,
        )

    # Step 3: section_id consistency check
    if parsed.section_id != section_id:
        violations.append(Violation(
            rule="section_id_mismatch",
            description=(
                f"Output section_id '{parsed.section_id}' does not match "
                f"expected section_id '{section_id}'."
            ),
            severity=ViolationSeverity.ERROR,
            location="section_id",
        ))
        return (
            ValidationResult(
                layer=ValidationLayer.STRUCTURAL,
                passed=False,
                attempt=attempt,
                violations=violations,
            ),
            None,
        )

    # All checks passed
    return (
        ValidationResult(
            layer=ValidationLayer.STRUCTURAL,
            passed=True,
            attempt=attempt,
            violations=[],
        ),
        parsed,
    )


def format_layer1_errors(result: ValidationResult) -> List[str]:
    """Format Layer 1 errors for inclusion in a retry prompt (FR-15).

    Parameters
    ----------
    result : ValidationResult
        A failed Layer 1 result.

    Returns
    -------
    list of str
        Human-readable error descriptions.
    """
    return [v.description for v in result.violations if v.severity == ViolationSeverity.ERROR]
```

### `synthesizer/validation/layer2_rules.py`
```python
# synthesizer/validation/layer2_rules.py
"""Layer 2 — Rule-based validation (§12.2, FR-16, FR-05).

Deterministic. Checks style sheet compliance:
  - Word count within per_level_constraints min/max
  - Heading level matches per_level_constraints heading_format
  - Citation format matches citation_pattern regex
  - No forbidden_phrases in text
  - Equation delimiters compliance
  - Per-type overrides applied and checked (FR-05)

No LLM call.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from synthesizer.models.enums import SectionType, ValidationLayer, ViolationSeverity
from synthesizer.models.section_output import SectionOutput
from synthesizer.models.style_sheet import LevelConstraint, StyleSheet
from synthesizer.models.validation_models import ValidationResult, Violation


def _heading_format_to_level(heading_format: str) -> int:
    """Convert heading format string (e.g. '##') to heading level int (e.g. 2)."""
    stripped = heading_format.strip()
    if stripped and all(c == "#" for c in stripped):
        return len(stripped)
    return 0  # Unknown format


def _resolve_constraints(
    style: StyleSheet,
    depth_level: int,
    section_type: SectionType,
) -> Dict[str, Any]:
    """Resolve effective constraints by merging level constraints with per-type overrides (FR-05).

    Per-type overrides take precedence over per_level_constraints when
    present (§7: style sheet Tier 2, but type overrides refine level constraints).

    Known override keys: min_words, max_words, heading_format.
    """
    effective: Dict[str, Any] = {}

    # Base from per_level_constraints
    level_constraint = style.per_level_constraints.get(depth_level)
    if level_constraint is not None:
        effective["min_words"] = level_constraint.min_words
        effective["max_words"] = level_constraint.max_words
        effective["heading_format"] = level_constraint.heading_format
    else:
        effective["min_words"] = None
        effective["max_words"] = None
        effective["heading_format"] = None

    # Apply per-type overrides (FR-05)
    overrides = style.per_type_overrides.get(section_type, {})
    for key in ("min_words", "max_words", "heading_format"):
        if key in overrides:
            effective[key] = overrides[key]

    return effective


def _check_word_count(
    output: SectionOutput,
    min_words: Optional[int],
    max_words: Optional[int],
) -> List[Violation]:
    """Check word count against min/max constraints."""
    violations: List[Violation] = []

    if min_words is not None and output.word_count < min_words:
        violations.append(Violation(
            rule="word_count_min",
            description=(
                f"Word count {output.word_count} is below the minimum "
                f"of {min_words}."
            ),
            severity=ViolationSeverity.ERROR,
            location="word_count",
        ))

    if max_words is not None and output.word_count > max_words:
        violations.append(Violation(
            rule="word_count_max",
            description=(
                f"Word count {output.word_count} exceeds the maximum "
                f"of {max_words}."
            ),
            severity=ViolationSeverity.ERROR,
            location="word_count",
        ))

    # Also verify the stated word_count matches actual content
    actual_words = len(output.content_markdown.split())
    if abs(actual_words - output.word_count) > max(5, actual_words * 0.1):
        violations.append(Violation(
            rule="word_count_mismatch",
            description=(
                f"Stated word_count ({output.word_count}) does not match "
                f"actual word count ({actual_words}) of content_markdown."
            ),
            severity=ViolationSeverity.WARNING,
            location="word_count",
        ))

    return violations


def _check_heading_level(
    output: SectionOutput,
    heading_format: Optional[str],
) -> List[Violation]:
    """Check heading level matches expected format."""
    violations: List[Violation] = []

    if heading_format is not None:
        expected_level = _heading_format_to_level(heading_format)
        if expected_level > 0 and output.heading_level != expected_level:
            violations.append(Violation(
                rule="heading_level",
                description=(
                    f"Heading level {output.heading_level} does not match "
                    f"expected level {expected_level} (from heading_format "
                    f"'{heading_format}')."
                ),
                severity=ViolationSeverity.ERROR,
                location="heading_level",
            ))

    return violations


def _check_citation_format(
    content: str,
    citation_pattern: str,
) -> List[Violation]:
    """Check that citations in content match the configured pattern.

    Heuristic: find parenthetical expressions containing 4-digit years
    (likely citations) and verify they match the citation_pattern regex.
    """
    violations: List[Violation] = []

    try:
        citation_re = re.compile(citation_pattern)
    except re.error:
        # Pattern already validated at load time (FR-04); defensive only
        return violations

    # Find potential citations: parenthetical expressions with years
    potential_citations = re.findall(
        r"\([^)]*(?:19|20)\d{2}[^)]*\)",
        content,
    )

    for citation_text in potential_citations:
        if not citation_re.search(citation_text):
            violations.append(Violation(
                rule="citation_format",
                description=(
                    f"Citation '{citation_text}' does not match the "
                    f"required pattern: {citation_pattern}"
                ),
                severity=ViolationSeverity.ERROR,
                location=f"content: '{citation_text}'",
            ))

    return violations


def _check_forbidden_phrases(
    content: str,
    forbidden_phrases: List[str],
) -> List[Violation]:
    """Check that no forbidden phrases appear in content."""
    violations: List[Violation] = []
    content_lower = content.lower()

    for phrase in forbidden_phrases:
        phrase_lower = phrase.lower()
        idx = content_lower.find(phrase_lower)
        if idx != -1:
            violations.append(Violation(
                rule="forbidden_phrase",
                description=(
                    f"Forbidden phrase '{phrase}' found in content."
                ),
                severity=ViolationSeverity.ERROR,
                location=f"character offset {idx}",
            ))

    return violations


def _check_equation_delimiters(
    content: str,
    inline_delim: str,
    display_delim: str,
) -> List[Violation]:
    """Check that equations use the configured delimiters.

    Heuristic: flag common non-standard delimiters if they differ
    from the configured ones.
    """
    violations: List[Violation] = []

    # Check for common alternative display delimiters
    if display_delim != "\\[":
        if "\\[" in content and "\\]" in content:
            violations.append(Violation(
                rule="equation_delimiter_display",
                description=(
                    f"Found '\\[...\\]' display equation delimiter; "
                    f"expected '{display_delim}' per style sheet."
                ),
                severity=ViolationSeverity.WARNING,
                location="content",
            ))

    if display_delim != "\\begin{equation}":
        if "\\begin{equation}" in content:
            violations.append(Violation(
                rule="equation_delimiter_display",
                description=(
                    f"Found '\\begin{{equation}}' display equation delimiter; "
                    f"expected '{display_delim}' per style sheet."
                ),
                severity=ViolationSeverity.WARNING,
                location="content",
            ))

    # Check for common alternative inline delimiters
    if inline_delim != "\\(":
        if "\\(" in content and "\\)" in content:
            violations.append(Violation(
                rule="equation_delimiter_inline",
                description=(
                    f"Found '\\(...\\)' inline equation delimiter; "
                    f"expected '{inline_delim}' per style sheet."
                ),
                severity=ViolationSeverity.WARNING,
                location="content",
            ))

    return violations


def validate_layer2(
    output: SectionOutput,
    style: StyleSheet,
    depth_level: int,
    section_type: SectionType,
    attempt: int = 1,
) -> ValidationResult:
    """Run Layer 2 rule-based validation (§12.2, FR-16, FR-05).

    Checks all style sheet compliance rules listed in §12.2:
      1. Word count within per_level_constraints
      2. Heading level correctness
      3. Citation format compliance
      4. Forbidden phrase detection
      5. Equation delimiter compliance
      6. Per-type overrides (FR-05)

    Parameters
    ----------
    output : SectionOutput
        Parsed and Layer-1-validated section output.
    style : StyleSheet
        Active style sheet (Tier 2 source of truth, §7).
    depth_level : int
        Section's nesting depth (from SectionNode).
    section_type : SectionType
        Section's type (for per-type overrides, FR-05).
    attempt : int
        Current validation attempt number (≥1).

    Returns
    -------
    ValidationResult
        Layer 2 result with any violations found.
    """
    all_violations: List[Violation] = []

    # Resolve effective constraints (FR-05: merge level constraints with type overrides)
    effective = _resolve_constraints(style, depth_level, section_type)

    # 1. Word count check
    all_violations.extend(
        _check_word_count(output, effective["min_words"], effective["max_words"])
    )

    # 2. Heading level check
    all_violations.extend(
        _check_heading_level(output, effective["heading_format"])
    )

    # 3. Citation format check
    all_violations.extend(
        _check_citation_format(output.content_markdown, style.citation_pattern)
    )

    # 4. Forbidden phrases check
    all_violations.extend(
        _check_forbidden_phrases(output.content_markdown, style.forbidden_phrases)
    )

    # 5. Equation delimiters check
    all_violations.extend(
        _check_equation_delimiters(
            output.content_markdown,
            style.equation_delimiters.inline,
            style.equation_delimiters.display,
        )
    )

    # Determine pass/fail: errors block progression; warnings do not
    has_errors = any(v.severity == ViolationSeverity.ERROR for v in all_violations)

    return ValidationResult(
        layer=ValidationLayer.RULE_BASED,
        passed=not has_errors,
        attempt=attempt,
        violations=all_violations,
    )


def format_layer2_errors(result: ValidationResult) -> List[str]:
    """Format Layer 2 violations for inclusion in a retry prompt (FR-17).

    Parameters
    ----------
    result : ValidationResult
        A failed Layer 2 result.

    Returns
    -------
    list of str
        Human-readable violation descriptions (errors only).
    """
    return [
        f"[{v.rule}] {v.description}"
        for v in result.violations
        if v.severity == ViolationSeverity.ERROR
    ]
```

### `synthesizer/validation/layer3_semantic.py`
```python
# synthesizer/validation/layer3_semantic.py
"""Layer 3 — Semantic validation (§12.3, §9.2.2, FR-18).

LLM-based. Three independent sub-checks, all must pass:
  A. Tone compliance
  B. Dependency contract fulfillment
  C. Unsupported claim detection

Each sub-check produces a separate ValidationResult. Layer 3 passes
only if all three pass.

DR-16 (open): Model selection — the LLM client is injected via protocol,
allowing per-role model configuration.
DR-18 (open): Output token budget is 1000 per sub-check per §9.2.2.
Input token budget remains open.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from synthesizer.models.claims import ClaimTable
from synthesizer.models.enums import ValidationLayer, ViolationSeverity
from synthesizer.models.section_output import SectionOutput
from synthesizer.models.validation_models import ValidationResult, Violation
from synthesizer.retrieval.adapter import RankedChunk

logger = logging.getLogger(__name__)

# Output token cap per sub-check (§9.2.2, partially open DR-18)
LAYER3_OUTPUT_TOKENS_PER_SUBCHECK = 1000


# ---------------------------------------------------------------------------
# LLM client protocol (DR-16: model selection remains configurable per role)
# ---------------------------------------------------------------------------

@runtime_checkable
class LLMClient(Protocol):
    """Protocol for LLM invocation used by Layer 3 semantic validation.

    DR-16 (open): Implementations may use different models per role.
    DR-18 (open): Input budget is not enforced by this interface.
    """

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int = LAYER3_OUTPUT_TOKENS_PER_SUBCHECK,
    ) -> str:
        """Invoke the LLM and return the response text.

        Parameters
        ----------
        system_prompt : str
            System-level instructions.
        user_message : str
            User-level message with context.
        max_output_tokens : int
            Maximum output tokens for this call.

        Returns
        -------
        str
            Raw response text from the LLM.
        """
        ...


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def _parse_llm_validation_response(
    raw_response: str,
    rule_name: str,
) -> Dict[str, Any]:
    """Parse an LLM validation sub-check response.

    Expected format:
    {
        "passed": true/false,
        "violations": [{"description": "...", "severity": "error|warning"}],
        "suggested_fix": "optional text"
    }
    """
    try:
        # Handle potential markdown fences
        text = raw_response.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines)
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except (json.JSONDecodeError, ValueError):
        pass

    # Fallback: treat non-JSON response as a failure with the raw text
    return {
        "passed": False,
        "violations": [
            {
                "description": f"LLM response could not be parsed as JSON: {raw_response[:200]}",
                "severity": "error",
            }
        ],
        "suggested_fix": None,
    }


def _llm_response_to_validation_result(
    parsed: Dict[str, Any],
    rule_name: str,
    attempt: int,
) -> ValidationResult:
    """Convert a parsed LLM response into a ValidationResult."""
    passed = bool(parsed.get("passed", False))
    violations: List[Violation] = []

    for v in parsed.get("violations", []):
        if isinstance(v, dict):
            violations.append(Violation(
                rule=rule_name,
                description=str(v.get("description", "Unknown violation")),
                severity=ViolationSeverity(v.get("severity", "error")),
                location=v.get("location"),
            ))
        elif isinstance(v, str):
            violations.append(Violation(
                rule=rule_name,
                description=v,
                severity=ViolationSeverity.ERROR,
            ))

    suggested_fix = parsed.get("suggested_fix")
    if suggested_fix is not None:
        suggested_fix = str(suggested_fix)

    return ValidationResult(
        layer=ValidationLayer.SEMANTIC,
        passed=passed,
        attempt=attempt,
        violations=violations,
        suggested_fix=suggested_fix,
    )


# ---------------------------------------------------------------------------
# Sub-check A: Tone compliance (§9.2.2)
# ---------------------------------------------------------------------------

_TONE_SYSTEM_PROMPT = (
    "You are a validation agent assessing whether a scientific literature "
    "review section uses the correct tone and register.\n\n"
    "You will be given:\n"
    "1. The section content in Markdown\n"
    "2. The expected tone register\n\n"
    "Evaluate whether the section:\n"
    "- Matches the expected tone register\n"
    "- Uses appropriate formality level\n"
    "- Contains no inappropriate colloquialisms or casual language\n\n"
    "Respond with ONLY valid JSON in this format:\n"
    '{"passed": true/false, "violations": [{"description": "...", "severity": "error"}], '
    '"suggested_fix": "optional suggestion"}\n'
)


def check_tone_compliance(
    content_markdown: str,
    tone_register: str,
    llm_client: LLMClient,
    attempt: int = 1,
) -> ValidationResult:
    """Sub-check A: Tone compliance (§9.2.2).

    Parameters
    ----------
    content_markdown : str
        The section's generated Markdown content.
    tone_register : str
        Expected tone from StyleSheet.tone_register.
    llm_client : LLMClient
        LLM client for semantic evaluation.
    attempt : int
        Current attempt number.

    Returns
    -------
    ValidationResult
        Result with rule="tone_compliance".
    """
    user_message = (
        f"=== SECTION CONTENT ===\n{content_markdown}\n"
        f"=== END SECTION CONTENT ===\n\n"
        f"Expected tone register: {tone_register}\n\n"
        "Assess whether this section matches the expected tone register."
    )

    try:
        raw = llm_client.invoke(
            system_prompt=_TONE_SYSTEM_PROMPT,
            user_message=user_message,
            max_output_tokens=LAYER3_OUTPUT_TOKENS_PER_SUBCHECK,
        )
        parsed = _parse_llm_validation_response(raw, "tone_compliance")
        return _llm_response_to_validation_result(parsed, "tone_compliance", attempt)
    except Exception as exc:
        logger.error("Tone compliance check failed with exception: %s", exc)
        return ValidationResult(
            layer=ValidationLayer.SEMANTIC,
            passed=False,
            attempt=attempt,
            violations=[Violation(
                rule="tone_compliance",
                description=f"Tone compliance check failed: {exc}",
                severity=ViolationSeverity.ERROR,
            )],
        )


# ---------------------------------------------------------------------------
# Sub-check B: Dependency contract fulfillment (§9.2.2)
# ---------------------------------------------------------------------------

_DEPENDENCY_SYSTEM_PROMPT = (
    "You are a validation agent assessing whether a scientific literature "
    "review section properly engages with claims from upstream sections.\n\n"
    "You will be given:\n"
    "1. The section content in Markdown\n"
    "2. Upstream claim tables with key claims the section should engage with\n\n"
    "Evaluate whether the section:\n"
    "- Engages with the key claims from each upstream claim table\n"
    "- Does not contradict upstream claims without justification\n"
    "- Properly builds upon the upstream analysis\n\n"
    "Respond with ONLY valid JSON in this format:\n"
    '{"passed": true/false, "violations": [{"description": "...", "severity": "error"}], '
    '"suggested_fix": "optional suggestion"}\n'
    "List any unengaged claims as violations.\n"
)


def check_dependency_contract(
    content_markdown: str,
    upstream_claim_tables: Dict[str, ClaimTable],
    llm_client: LLMClient,
    attempt: int = 1,
) -> ValidationResult:
    """Sub-check B: Dependency contract fulfillment (§9.2.2, FR-18).

    Checks that the downstream section engages with key claims from
    each upstream claim table.

    Parameters
    ----------
    content_markdown : str
        The section's generated Markdown content.
    upstream_claim_tables : dict
        Maps upstream section_id → ClaimTable for all content dependencies.
    llm_client : LLMClient
        LLM client for semantic evaluation.
    attempt : int
        Current attempt number.

    Returns
    -------
    ValidationResult
        Result with rule="dependency_contract".
    """
    if not upstream_claim_tables:
        # No content dependencies → sub-check trivially passes
        return ValidationResult(
            layer=ValidationLayer.SEMANTIC,
            passed=True,
            attempt=attempt,
            violations=[],
        )

    # Format upstream claims for the prompt
    claims_text_parts: List[str] = []
    for section_id in sorted(upstream_claim_tables):
        ct = upstream_claim_tables[section_id]
        claims_text_parts.append(f"\n--- Claims from section: {section_id} ---")
        if ct.partial:
            claims_text_parts.append("[Note: This claim table is partial.]")
        for claim in ct.claims:
            claims_text_parts.append(
                f"  [{claim.claim_id}] {claim.claim_text} "
                f"(confidence: {claim.confidence_tag.value})"
            )
    claims_text = "\n".join(claims_text_parts)

    user_message = (
        f"=== SECTION CONTENT ===\n{content_markdown}\n"
        f"=== END SECTION CONTENT ===\n\n"
        f"=== UPSTREAM CLAIM TABLES ===\n{claims_text}\n"
        f"=== END UPSTREAM CLAIM TABLES ===\n\n"
        "Assess whether this section properly engages with the upstream claims. "
        "List any unengaged or contradicted claims as violations."
    )

    try:
        raw = llm_client.invoke(
            system_prompt=_DEPENDENCY_SYSTEM_PROMPT,
            user_message=user_message,
            max_output_tokens=LAYER3_OUTPUT_TOKENS_PER_SUBCHECK,
        )
        parsed = _parse_llm_validation_response(raw, "dependency_contract")
        return _llm_response_to_validation_result(parsed, "dependency_contract", attempt)
    except Exception as exc:
        logger.error("Dependency contract check failed with exception: %s", exc)
        return ValidationResult(
            layer=ValidationLayer.SEMANTIC,
            passed=False,
            attempt=attempt,
            violations=[Violation(
                rule="dependency_contract",
                description=f"Dependency contract check failed: {exc}",
                severity=ViolationSeverity.ERROR,
            )],
        )


# ---------------------------------------------------------------------------
# Sub-check C: Unsupported claim detection (§9.2.2)
# ---------------------------------------------------------------------------

_UNSUPPORTED_CLAIMS_SYSTEM_PROMPT = (
    "You are a validation agent detecting unsupported claims in a "
    "scientific literature review section.\n\n"
    "You will be given:\n"
    "1. The section content in Markdown\n"
    "2. Evidence chunks from source documents\n"
    "3. Upstream claim tables (if any)\n\n"
    "Evaluate whether:\n"
    "- All claims in the section are traceable to the evidence chunks "
    "or upstream claim tables\n"
    "- No claims are fabricated or unsupported by the provided evidence\n"
    "- References and citations correspond to real evidence\n\n"
    "Respond with ONLY valid JSON in this format:\n"
    '{"passed": true/false, "violations": [{"description": "...", "severity": "error"}], '
    '"suggested_fix": "optional suggestion"}\n'
    "List any unsupported claims as violations.\n"
)


def check_unsupported_claims(
    content_markdown: str,
    retrieved_chunks: List[RankedChunk],
    upstream_claim_tables: Dict[str, ClaimTable],
    llm_client: LLMClient,
    attempt: int = 1,
) -> ValidationResult:
    """Sub-check C: Unsupported claim detection (§9.2.2).

    Checks that claims in the section are traceable to retrieval chunks
    or upstream claim tables.

    Parameters
    ----------
    content_markdown : str
        The section's generated Markdown content.
    retrieved_chunks : list of RankedChunk
        Evidence chunks used during generation.
    upstream_claim_tables : dict
        Maps upstream section_id → ClaimTable.
    llm_client : LLMClient
        LLM client for semantic evaluation.
    attempt : int
        Current attempt number.

    Returns
    -------
    ValidationResult
        Result with rule="unsupported_claims".
    """
    # Format evidence chunks
    chunks_text_parts: List[str] = []
    for chunk in retrieved_chunks:
        meta = chunk.metadata
        meta_str = ", ".join(
            f"{k}: {v}" for k, v in sorted(meta.items()) if v
        ) or "no metadata"
        chunks_text_parts.append(
            f"  [{chunk.id}] ({meta_str})\n  {chunk.text[:500]}"
        )
    chunks_text = "\n".join(chunks_text_parts) if chunks_text_parts else "(No evidence chunks)"

    # Format upstream claims
    claims_parts: List[str] = []
    for section_id in sorted(upstream_claim_tables):
        ct = upstream_claim_tables[section_id]
        for claim in ct.claims:
            claims_parts.append(
                f"  [{claim.claim_id} from {section_id}] {claim.claim_text}"
            )
    claims_text = "\n".join(claims_parts) if claims_parts else "(No upstream claims)"

    user_message = (
        f"=== SECTION CONTENT ===\n{content_markdown}\n"
        f"=== END SECTION CONTENT ===\n\n"
        f"=== EVIDENCE CHUNKS ===\n{chunks_text}\n"
        f"=== END EVIDENCE CHUNKS ===\n\n"
        f"=== UPSTREAM CLAIMS ===\n{claims_text}\n"
        f"=== END UPSTREAM CLAIMS ===\n\n"
        "Assess whether all claims in this section are supported by the "
        "provided evidence chunks or upstream claims. List any unsupported "
        "claims as violations."
    )

    try:
        raw = llm_client.invoke(
            system_prompt=_UNSUPPORTED_CLAIMS_SYSTEM_PROMPT,
            user_message=user_message,
            max_output_tokens=LAYER3_OUTPUT_TOKENS_PER_SUBCHECK,
        )
        parsed = _parse_llm_validation_response(raw, "unsupported_claims")
        return _llm_response_to_validation_result(parsed, "unsupported_claims", attempt)
    except Exception as exc:
        logger.error("Unsupported claims check failed with exception: %s", exc)
        return ValidationResult(
            layer=ValidationLayer.SEMANTIC,
            passed=False,
            attempt=attempt,
            violations=[Violation(
                rule="unsupported_claims",
                description=f"Unsupported claims check failed: {exc}",
                severity=ViolationSeverity.ERROR,
            )],
        )


# ---------------------------------------------------------------------------
# Aggregate Layer 3 validation (§12.3)
# ---------------------------------------------------------------------------

def validate_layer3(
    output: SectionOutput,
    tone_register: str,
    upstream_claim_tables: Dict[str, ClaimTable],
    retrieved_chunks: List[RankedChunk],
    llm_client: LLMClient,
    attempt: int = 1,
) -> ValidationResult:
    """Run all three Layer 3 semantic sub-checks (§12.3, FR-18).

    All three sub-checks must pass for Layer 3 to pass. Sub-check
    results are aggregated into a single ValidationResult.

    §12.3 retry scope: On any sub-check failure, the entire section
    is re-generated (not just the failing sub-check).

    Parameters
    ----------
    output : SectionOutput
        Parsed section output (already passed L1 and L2).
    tone_register : str
        Expected tone from StyleSheet.
    upstream_claim_tables : dict
        Maps upstream section_id → ClaimTable for content dependencies.
    retrieved_chunks : list of RankedChunk
        Evidence chunks used during generation.
    llm_client : LLMClient
        LLM client for semantic evaluation. DR-16: model configurable.
    attempt : int
        Current attempt number.

    Returns
    -------
    ValidationResult
        Aggregated Layer 3 result. Passes only if all sub-checks pass.
    """
    sub_results: List[ValidationResult] = []

    # Sub-check A: Tone compliance
    tone_result = check_tone_compliance(
        output.content_markdown, tone_register, llm_client, attempt
    )
    sub_results.append(tone_result)

    # Sub-check B: Dependency contract
    dep_result = check_dependency_contract(
        output.content_markdown, upstream_claim_tables, llm_client, attempt
    )
    sub_results.append(dep_result)

    # Sub-check C: Unsupported claims
    claims_result = check_unsupported_claims(
        output.content_markdown, retrieved_chunks,
        upstream_claim_tables, llm_client, attempt
    )
    sub_results.append(claims_result)

    # Aggregate: all three must pass
    all_passed = all(r.passed for r in sub_results)
    all_violations: List[Violation] = []
    suggested_fixes: List[str] = []

    for r in sub_results:
        all_violations.extend(r.violations)
        if r.suggested_fix:
            suggested_fixes.append(r.suggested_fix)

    combined_fix = "\n".join(suggested_fixes) if suggested_fixes else None

    return ValidationResult(
        layer=ValidationLayer.SEMANTIC,
        passed=all_passed,
        attempt=attempt,
        violations=all_violations,
        suggested_fix=combined_fix,
    )


def format_layer3_errors(result: ValidationResult) -> List[str]:
    """Format Layer 3 violations for inclusion in a retry prompt (FR-19).

    Parameters
    ----------
    result : ValidationResult
        A failed Layer 3 result.

    Returns
    -------
    list of str
        Human-readable violation descriptions.
    """
    errors = [
        f"[{v.rule}] {v.description}"
        for v in result.violations
        if v.severity == ViolationSeverity.ERROR
    ]
    if result.suggested_fix:
        errors.append(f"Suggested fix: {result.suggested_fix}")
    return errors
```

### `synthesizer/validation/coordinator.py`
```python
# synthesizer/validation/coordinator.py
"""Validation coordinator — sequential L1 → L2 → L3 pipeline (§12).

Runs all three validation layers in order, short-circuiting on failure.
Does NOT manage retries — that is the retry module's responsibility.

The coordinator is a pure function: given inputs, it runs validation
and returns results. State mutation (retry counters, validation history)
is handled by the caller or the retry module.
"""

from __future__ import annotations

from