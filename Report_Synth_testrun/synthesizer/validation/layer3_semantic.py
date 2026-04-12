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