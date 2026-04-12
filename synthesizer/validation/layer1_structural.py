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