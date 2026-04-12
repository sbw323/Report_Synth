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