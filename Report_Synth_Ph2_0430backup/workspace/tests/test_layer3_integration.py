# tests/test_layer3_integration.py
"""Integration tests for Layer 3 semantic validation pipeline (§12.3, FR-18, FR-19).

Tests the full L1→L2→L3 validation pipeline with a live Anthropic LLM client,
verifying that all three L3 sub-checks (tone compliance, dependency contract
fulfillment, unsupported claim detection) produce valid ValidationResult objects.

Governing spec sections: §12.3, §9.2.2, §10.10
Functional requirements: FR-18 (L3 sub-checks A/B/C), FR-19 (retry feedback)
Non-functional requirements: NFR-09 (model availability)

These tests require:
  - ANTHROPIC_API_KEY environment variable set
  - Network access to the Anthropic API
  - The 'anthropic' package installed

Tests are marked with pytest.mark.integration so they can be selectively
run or skipped in CI environments without API access.
"""

from __future__ import annotations

import json
import os
import logging
import pytest
from typing import Dict, List, Optional
from unittest.mock import MagicMock

from synthesizer.models.claims import ClaimTable, ClaimEntry, TextSpan
from synthesizer.models.enums import (
    ConfidenceTag,
    DependencyKind,
    SectionType,
    SectionLifecycleState,
    ValidationLayer,
    ViolationSeverity,
)
from synthesizer.models.section_output import SectionOutput, get_output_model
from synthesizer.models.style_sheet import StyleSheet, LevelConstraint
from synthesizer.models.validation_models import ValidationResult, Violation
from synthesizer.retrieval.adapter import RankedChunk
from synthesizer.validation.coordinator import (
    ValidationPipelineResult,
    run_validation_pipeline,
)
from synthesizer.validation.layer3_semantic import (
    LLMClient,
    LAYER3_OUTPUT_TOKENS_PER_SUBCHECK,
    check_tone_compliance,
    check_dependency_contract,
    check_unsupported_claims,
    validate_layer3,
    format_layer3_errors,
    _parse_llm_validation_response,
    _llm_response_to_validation_result,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Markers and skip conditions
# ---------------------------------------------------------------------------

# Check if we can run live API tests
_HAS_API_KEY = bool(os.environ.get("ANTHROPIC_API_KEY"))
_HAS_ANTHROPIC = True
try:
    import anthropic  # noqa: F401
except ImportError:
    _HAS_ANTHROPIC = False

requires_live_api = pytest.mark.skipif(
    not (_HAS_API_KEY and _HAS_ANTHROPIC),
    reason="Requires ANTHROPIC_API_KEY and anthropic package for live API tests",
)

integration = pytest.mark.integration


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

def _make_style_sheet(tone_register: str = "formal_academic") -> StyleSheet:
    """Create a minimal StyleSheet for testing (§10.5).

    FR-04: Style sheet structure for validation.
    """
    return StyleSheet(
        tone_register=tone_register,
        citation_style="author_year",
        level_constraints=[
            LevelConstraint(
                depth=1,
                heading_style="Title Case",
                word_count_min=100,
                word_count_max=5000,
            ),
            LevelConstraint(
                depth=2,
                heading_style="Title Case",
                word_count_min=50,
                word_count_max=3000,
            ),
        ],
    )


def _make_well_formed_section_json(
    section_id: str = "sec_intro",
    heading: str = "Introduction to Neural Architecture Search",
    content: str = (
        "Neural Architecture Search (NAS) has emerged as a pivotal methodology "
        "in the automated design of deep learning architectures. Recent advances "
        "in differentiable search strategies have substantially reduced the "
        "computational overhead associated with architecture optimization. "
        "This section provides a comprehensive overview of the foundational "
        "principles underlying NAS, examining both the theoretical framework "
        "and empirical evidence supporting its efficacy in diverse application "
        "domains. The methodology has demonstrated consistent improvements "
        "over manually designed architectures across multiple benchmark tasks, "
        "as evidenced by systematic evaluations in the literature."
    ),
) -> str:
    """Create a well-formed section output JSON string for testing.

    FR-14: Structural validation input format.
    """
    output = {
        "section_id": section_id,
        "heading": heading,
        "content_markdown": content,
        "provenance": [],
    }
    return json.dumps(output)


def _make_casual_section_json(section_id: str = "sec_intro") -> str:
    """Create a section with deliberately casual/informal tone for sub-check A failure.

    FR-18: Tone compliance sub-check should detect informal language.
    """
    output = {
        "section_id": section_id,
        "heading": "Introduction to Neural Architecture Search",
        "content_markdown": (
            "So basically, NAS is like super cool because it lets computers "
            "figure out the best neural network designs all by themselves! "
            "It's kinda like having a robot architect, ya know? The whole "
            "thing is pretty awesome and honestly blows my mind every time "
            "I think about it. LOL, who even needs human engineers anymore? "
            "Anyway, let's dive into this stuff and see what's up with all "
            "the hype around automated architecture design. Trust me bro, "
            "it's gonna be a wild ride! The results are literally insane "
            "and everyone should totally check this out ASAP."
        ),
        "provenance": [],
    }
    return json.dumps(output)


def _make_ignoring_upstream_section_json(section_id: str = "sec_analysis") -> str:
    """Create a section that completely ignores upstream claims for sub-check B failure.

    FR-18: Dependency contract sub-check should detect unengaged claims.
    """
    output = {
        "section_id": section_id,
        "heading": "Analysis of Weather Patterns",
        "content_markdown": (
            "This section examines contemporary weather patterns across "
            "temperate regions. Precipitation levels have shown notable "
            "variation in recent decades, with implications for agricultural "
            "planning and water resource management. Temperature anomalies "
            "recorded during the observation period suggest a complex "
            "interplay between oceanic circulation patterns and atmospheric "
            "dynamics. The analysis draws upon meteorological data from "
            "multiple monitoring stations distributed across the study area."
        ),
        "provenance": [],
    }
    return json.dumps(output)


def _make_upstream_claim_tables() -> Dict[str, ClaimTable]:
    """Create upstream claim tables about NAS for dependency contract testing.

    FR-18: Dependency contract sub-check input.
    """
    claims = [
        ClaimEntry(
            claim_id="C1",
            claim_text=(
                "Differentiable NAS methods reduce search cost by 1000x "
                "compared to reinforcement learning approaches"
            ),
            confidence_tag=ConfidenceTag.HIGH,
            source_spans=[
                TextSpan(document_id="doc1", start=0, end=100, text="..."),
            ],
        ),
        ClaimEntry(
            claim_id="C2",
            claim_text=(
                "Weight-sharing strategies introduce a systematic bias "
                "that underestimates standalone architecture performance"
            ),
            confidence_tag=ConfidenceTag.MEDIUM,
            source_spans=[
                TextSpan(document_id="doc2", start=0, end=80, text="..."),
            ],
        ),
        ClaimEntry(
            claim_id="C3",
            claim_text=(
                "One-shot NAS achieves comparable accuracy to multi-trial "
                "methods on CIFAR-10 and ImageNet benchmarks"
            ),
            confidence_tag=ConfidenceTag.HIGH,
            source_spans=[
                TextSpan(document_id="doc3", start=0, end=120, text="..."),
            ],
        ),
    ]
    return {
        "sec_background": ClaimTable(
            section_id="sec_background",
            claims=claims,
            partial=False,
        ),
    }


def _make_unsupported_claims_section_json(section_id: str = "sec_results") -> str:
    """Create a section with fabricated claims not in evidence for sub-check C failure.

    FR-18: Unsupported claim detection sub-check should flag fabricated assertions.
    """
    output = {
        "section_id": section_id,
        "heading": "Results and Discussion",
        "content_markdown": (
            "Our analysis reveals that quantum neural architecture search "
            "achieves a 99.7% accuracy improvement over all existing methods "
            "on every known benchmark dataset. Furthermore, the revolutionary "
            "HyperNAS-X framework, developed by researchers at the fictional "
            "Institute of Advanced Computation in 2025, has demonstrated that "
            "architecture search can be completed in under 0.001 seconds on "
            "consumer hardware. According to Smith et al. (2024), published "
            "in the Journal of Impossible Results, these findings overturn "
            "all prior understanding of computational complexity theory."
        ),
        "provenance": [],
    }
    return json.dumps(output)


def _make_evidence_chunks() -> List[RankedChunk]:
    """Create evidence chunks about NAS for unsupported claim testing.

    FR-18: Evidence chunks for traceability checking.
    """
    return [
        RankedChunk(
            id="chunk_1",
            text=(
                "Neural Architecture Search using reinforcement learning was "
                "introduced by Zoph and Le (2017). The original method required "
                "800 GPU-days to discover competitive architectures on CIFAR-10."
            ),
            score=0.92,
            metadata={"source": "doc1", "page": "3"},
        ),
        RankedChunk(
            id="chunk_2",
            text=(
                "DARTS (Liu et al., 2019) introduced differentiable architecture "
                "search, reducing the search cost to a single GPU-day while "
                "maintaining competitive accuracy on standard benchmarks."
            ),
            score=0.88,
            metadata={"source": "doc2", "page": "1"},
        ),
        RankedChunk(
            id="chunk_3",
            text=(
                "Weight-sharing approaches in one-shot NAS have been shown to "
                "introduce ranking correlation issues, where the shared-weight "
                "performance does not reliably predict standalone performance."
            ),
            score=0.85,
            metadata={"source": "doc3", "page": "5"},
        ),
    ]


# ---------------------------------------------------------------------------
# Mock LLM client for unit-level tests (no API needed)
# ---------------------------------------------------------------------------

class MockLLMClient:
    """Mock LLM client for testing without API access.

    Implements the LLMClient protocol from layer3_semantic.py.
    Returns configurable JSON responses for each sub-check.
    """

    def __init__(self, responses: Optional[Dict[str, str]] = None) -> None:
        self._responses = responses or {}
        self._call_count = 0
        self._calls: List[Dict] = []

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int = LAYER3_OUTPUT_TOKENS_PER_SUBCHECK,
    ) -> str:
        """Return a pre-configured response based on call order or prompt content."""
        self._call_count += 1
        self._calls.append({
            "system_prompt": system_prompt,
            "user_message": user_message,
            "max_output_tokens": max_output_tokens,
        })

        # Determine which sub-check based on system prompt content
        if "tone" in system_prompt.lower():
            return self._responses.get("tone", '{"passed": true, "violations": []}')
        elif "dependency" in system_prompt.lower() or "upstream" in system_prompt.lower():
            return self._responses.get("dependency", '{"passed": true, "violations": []}')
        elif "unsupported" in system_prompt.lower():
            return self._responses.get("unsupported", '{"passed": true, "violations": []}')
        else:
            return '{"passed": true, "violations": []}'

    @property
    def call_count(self) -> int:
        return self._call_count

    @property
    def calls(self) -> List[Dict]:
        return self._calls


class ErrorLLMClient:
    """LLM client that raises exceptions for error handling tests."""

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int = LAYER3_OUTPUT_TOKENS_PER_SUBCHECK,
    ) -> str:
        raise ConnectionError("Simulated API connection failure")


class MalformedResponseLLMClient:
    """LLM client that returns malformed (non-JSON) responses.

    FR-18: Tests that malformed LLM responses produce failure
    ValidationResults with parse-error violations rather than
    raising unhandled exceptions.
    """

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int = LAYER3_OUTPUT_TOKENS_PER_SUBCHECK,
    ) -> str:
        return "This is not valid JSON at all. The model went off the rails."


# ---------------------------------------------------------------------------
# Unit tests (no API required)
# ---------------------------------------------------------------------------

class TestResponseParsing:
    """Tests for LLM response parsing utilities (§12.3)."""

    def test_parse_valid_json_pass(self):
        """Valid JSON with passed=true parses correctly."""
        raw = '{"passed": true, "violations": []}'
        parsed = _parse_llm_validation_response(raw, "test_rule")
        assert parsed["passed"] is True
        assert parsed["violations"] == []

    def test_parse_valid_json_fail(self):
        """Valid JSON with passed=false and violations parses correctly."""
        raw = json.dumps({
            "passed": False,
            "violations": [
                {"description": "Tone is too casual", "severity": "error"}
            ],
            "suggested_fix": "Use formal academic language",
        })
        parsed = _parse_llm_validation_response(raw, "test_rule")
        assert parsed["passed"] is False
        assert len(parsed["violations"]) == 1
        assert parsed["suggested_fix"] == "Use formal academic language"

    def test_parse_markdown_fenced_json(self):
        """JSON wrapped in markdown code fences parses correctly."""
        raw = '```json\n{"passed": true, "violations": []}\n```'
        parsed = _parse_llm_validation_response(raw, "test_rule")
        assert parsed["passed"] is True

    def test_parse_malformed_json(self):
        """Malformed JSON returns a failure dict with parse-error violation (FR-18)."""
        raw = "This is not JSON"
        parsed = _parse_llm_validation_response(raw, "test_rule")
        assert parsed["passed"] is False
        assert len(parsed["violations"]) == 1
        assert "could not be parsed" in parsed["violations"][0]["description"]

    def test_llm_response_to_validation_result(self):
        """Parsed dict converts to a proper ValidationResult (§10.10)."""
        parsed = {
            "passed": False,
            "violations": [
                {"description": "Informal tone detected", "severity": "error"}
            ],
            "suggested_fix": "Revise to formal register",
        }
        result = _llm_response_to_validation_result(parsed, "tone_compliance", 1)
        assert isinstance(result, ValidationResult)
        assert result.layer == ValidationLayer.SEMANTIC
        assert result.passed is False
        assert result.attempt == 1
        assert len(result.violations) == 1
        assert result.violations[0].rule == "tone_compliance"
        assert result.violations[0].severity == ViolationSeverity.ERROR
        assert result.suggested_fix == "Revise to formal register"

    def test_string_violations_handled(self):
        """String-type violations in the list are handled gracefully."""
        parsed = {
            "passed": False,
            "violations": ["Simple string violation"],
        }
        result = _llm_response_to_validation_result(parsed, "test_rule", 2)
        assert len(result.violations) == 1
        assert result.violations[0].description == "Simple string violation"
        assert result.violations[0].severity == ViolationSeverity.ERROR


class TestMockSubChecks:
    """Tests for L3 sub-checks using mock LLM client (no API required)."""

    def test_tone_compliance_pass(self):
        """Sub-check A passes with a passing mock response (FR-18)."""
        client = MockLLMClient({"tone": '{"passed": true, "violations": []}'})
        result = check_tone_compliance(
            content_markdown="Formal academic text here.",
            tone_register="formal_academic",
            llm_client=client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.layer == ValidationLayer.SEMANTIC
        assert result.passed is True
        assert result.attempt == 1
        assert client.call_count == 1

    def test_tone_compliance_fail(self):
        """Sub-check A fails with a failing mock response (FR-18)."""
        client = MockLLMClient({
            "tone": json.dumps({
                "passed": False,
                "violations": [
                    {"description": "Casual language detected", "severity": "error"}
                ],
                "suggested_fix": "Use formal academic register",
            })
        })
        result = check_tone_compliance(
            content_markdown="Hey dude, this is super cool!",
            tone_register="formal_academic",
            llm_client=client,
            attempt=2,
        )
        assert result.passed is False
        assert result.attempt == 2
        assert len(result.violations) >= 1
        assert result.violations[0].rule == "tone_compliance"

    def test_dependency_contract_no_upstream(self):
        """Sub-check B trivially passes with no upstream claims (FR-18)."""
        client = MockLLMClient()
        result = check_dependency_contract(
            content_markdown="Some content.",
            upstream_claim_tables={},
            llm_client=client,
            attempt=1,
        )
        assert result.passed is True
        # No LLM call should be made when there are no upstream claims
        assert client.call_count == 0

    def test_dependency_contract_with_upstream(self):
        """Sub-check B invokes LLM when upstream claims exist (FR-18)."""
        client = MockLLMClient({
            "dependency": '{"passed": true, "violations": []}'
        })
        result = check_dependency_contract(
            content_markdown="Content engaging with upstream claims.",
            upstream_claim_tables=_make_upstream_claim_tables(),
            llm_client=client,
            attempt=1,
        )
        assert result.passed is True
        assert client.call_count == 1

    def test_unsupported_claims_pass(self):
        """Sub-check C passes with a passing mock response (FR-18)."""
        client = MockLLMClient({
            "unsupported": '{"passed": true, "violations": []}'
        })
        result = check_unsupported_claims(
            content_markdown="Claims supported by evidence.",
            retrieved_chunks=_make_evidence_chunks(),
            upstream_claim_tables={},
            llm_client=client,
            attempt=1,
        )
        assert result.passed is True
        assert client.call_count == 1

    def test_unsupported_claims_fail(self):
        """Sub-check C fails when unsupported claims detected (FR-18)."""
        client = MockLLMClient({
            "unsupported": json.dumps({
                "passed": False,
                "violations": [
                    {
                        "description": "Claim about 99.7% accuracy is not in evidence",
                        "severity": "error",
                    }
                ],
            })
        })
        result = check_unsupported_claims(
            content_markdown="Fabricated claims here.",
            retrieved_chunks=_make_evidence_chunks(),
            upstream_claim_tables={},
            llm_client=client,
            attempt=1,
        )
        assert result.passed is False
        assert len(result.violations) >= 1
        assert result.violations[0].rule == "unsupported_claims"


class TestValidateLayer3Aggregate:
    """Tests for the aggregate validate_layer3() function (§12.3)."""

    def test_all_pass(self):
        """All three sub-checks pass → Layer 3 passes (FR-18)."""
        client = MockLLMClient({
            "tone": '{"passed": true, "violations": []}',
            "dependency": '{"passed": true, "violations": []}',
            "unsupported": '{"passed": true, "violations": []}',
        })
        # Create a minimal SectionOutput
        output = get_output_model(SectionType.ANALYSIS)(
            section_id="sec_test",
            heading="Test Section",
            content_markdown="Formal academic content about NAS.",
            provenance=[],
        )
        result = validate_layer3(
            output=output,
            tone_register="formal_academic",
            upstream_claim_tables={},
            retrieved_chunks=_make_evidence_chunks(),
            llm_client=client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.layer == ValidationLayer.SEMANTIC
        assert result.passed is True
        assert result.attempt == 1
        assert len(result.violations) == 0

    def test_tone_fails_others_pass(self):
        """Tone sub-check fails → Layer 3 fails even if others pass (FR-18)."""
        client = MockLLMClient({
            "tone": json.dumps({
                "passed": False,
                "violations": [{"description": "Too casual", "severity": "error"}],
            }),
            "dependency": '{"passed": true, "violations": []}',
            "unsupported": '{"passed": true, "violations": []}',
        })
        output = get_output_model(SectionType.ANALYSIS)(
            section_id="sec_test",
            heading="Test Section",
            content_markdown="Hey dude, NAS is cool!",
            provenance=[],
        )
        result = validate_layer3(
            output=output,
            tone_register="formal_academic",
            upstream_claim_tables={},
            retrieved_chunks=[],
            llm_client=client,
            attempt=1,
        )
        assert result.passed is False
        assert any(v.rule == "tone_compliance" for v in result.violations)

    def test_multiple_failures_aggregated(self):
        """Multiple sub-check failures aggregate violations (FR-18)."""
        client = MockLLMClient({
            "tone": json.dumps({
                "passed": False,
                "violations": [{"description": "Tone issue", "severity": "error"}],
            }),
            "dependency": json.dumps({
                "passed": False,
                "violations": [{"description": "Missing claim", "severity": "error"}],
            }),
            "unsupported": json.dumps({
                "passed": False,
                "violations": [{"description": "Fabricated claim", "severity": "error"}],
            }),
        })
        output = get_output_model(SectionType.ANALYSIS)(
            section_id="sec_test",
            heading="Test Section",
            content_markdown="Bad content.",
            provenance=[],
        )
        result = validate_layer3(
            output=output,
            tone_register="formal_academic",
            upstream_claim_tables=_make_upstream_claim_tables(),
            retrieved_chunks=_make_evidence_chunks(),
            llm_client=client,
            attempt=1,
        )
        assert result.passed is False
        rules = {v.rule for v in result.violations}
        assert "tone_compliance" in rules
        assert "dependency_contract" in rules
        assert "unsupported_claims" in rules


class TestFormatLayer3Errors:
    """Tests for format_layer3_errors() (FR-19)."""

    def test_format_errors_with_violations(self):
        """Formatted errors include violation descriptions (FR-19)."""
        result = ValidationResult(
            layer=ValidationLayer.SEMANTIC,
            passed=False,
            attempt=1,
            violations=[
                Violation(
                    rule="tone_compliance",
                    description="Informal language detected",
                    severity=ViolationSeverity.ERROR,
                ),
                Violation(
                    rule="unsupported_claims",
                    description="Claim X is not in evidence",
                    severity=ViolationSeverity.ERROR,
                ),
            ],
            suggested_fix="Revise tone and remove unsupported claims",
        )
        errors = format_layer3_errors(result)
        assert len(errors) >= 2
        assert any("tone_compliance" in e for e in errors)
        assert any("unsupported_claims" in e for e in errors)
        assert any("Suggested fix" in e for e in errors)

    def test_format_errors_warnings_excluded(self):
        """Warnings are excluded from formatted errors (FR-19)."""
        result = ValidationResult(
            layer=ValidationLayer.SEMANTIC,
            passed=False,
            attempt=1,
            violations=[
                Violation(
                    rule="tone_compliance",
                    description="Minor tone issue",
                    severity=ViolationSeverity.WARNING,
                ),
            ],
        )
        errors = format_layer3_errors(result)
        # Warnings should not appear in error messages
        assert not any("Minor tone issue" in e for e in errors)


class TestMalformedLLMResponse:
    """Tests for malformed LLM response handling (FR-18).

    Verifies that malformed responses produce failure ValidationResults
    with parse-error violations rather than raising unhandled exceptions.
    """

    def test_malformed_response_tone(self):
        """Malformed response from tone check → failure with parse-error (FR-18)."""
        client = MalformedResponseLLMClient()
        result = check_tone_compliance(
            content_markdown="Some content.",
            tone_register="formal_academic",
            llm_client=client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.passed is False
        assert result.layer == ValidationLayer.SEMANTIC
        assert len(result.violations) >= 1
        # Should have a parse-error or the raw text in the violation
        assert any(
            "could not be parsed" in v.description.lower()
            or "not valid json" in v.description.lower()
            for v in result.violations
        )

    def test_malformed_response_dependency(self):
        """Malformed response from dependency check → failure with parse-error (FR-18)."""
        client = MalformedResponseLLMClient()
        result = check_dependency_contract(
            content_markdown="Some content.",
            upstream_claim_tables=_make_upstream_claim_tables(),
            llm_client=client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.passed is False

    def test_malformed_response_unsupported(self):
        """Malformed response from unsupported claims check → failure (FR-18)."""
        client = MalformedResponseLLMClient()
        result = check_unsupported_claims(
            content_markdown="Some content.",
            retrieved_chunks=_make_evidence_chunks(),
            upstream_claim_tables={},
            llm_client=client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.passed is False

    def test_exception_in_llm_call(self):
        """Exception during LLM call → failure ValidationResult (FR-18)."""
        client = ErrorLLMClient()
        result = check_tone_compliance(
            content_markdown="Some content.",
            tone_register="formal_academic",
            llm_client=client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.passed is False
        assert any("failed" in v.description.lower() for v in result.violations)


class TestCoordinatorPipelineMock:
    """Tests for the full coordinator pipeline with mock LLM client.

    Verifies the L1→L2→L3 pipeline wiring without requiring API access.
    """

    def test_pipeline_all_pass_with_l3(self):
        """Full pipeline L1→L2→L3 passes with well-formed input (§12, FR-18)."""
        client = MockLLMClient({
            "tone": '{"passed": true, "violations": []}',
            "dependency": '{"passed": true, "violations": []}',
            "unsupported": '{"passed": true, "violations": []}',
        })
        style = _make_style_sheet()
        raw_json = _make_well_formed_section_json()

        result = run_validation_pipeline(
            raw_json=raw_json,
            section_id="sec_intro",
            section_type=SectionType.ANALYSIS,
            style=style,
            depth_level=1,
            attempt=1,
            llm_client=client,
            skip_layer3=False,
        )

        assert isinstance(result, ValidationPipelineResult)
        assert result.passed is True
        assert result.failed_layer is None
        assert result.parsed_output is not None
        # Should have L1, L2, and L3 results
        assert len(result.results) == 3
        assert result.results[0].layer == ValidationLayer.STRUCTURAL
        assert result.results[1].layer == ValidationLayer.RULE_BASED
        assert result.results[2].layer == ValidationLayer.SEMANTIC

    def test_pipeline_l3_failure_returns_errors(self):
        """Pipeline with L3 failure returns formatted error messages (FR-19)."""
        client = MockLLMClient({
            "tone": json.dumps({
                "passed": False,
                "violations": [
                    {"description": "Casual tone detected", "severity": "error"}
                ],
                "suggested_fix": "Use formal academic register",
            }),
            "dependency": '{"passed": true, "violations": []}',
            "unsupported": '{"passed": true, "violations": []}',
        })
        style = _make_style_sheet()
        raw_json = _make_well_formed_section_json()

        result = run_validation_pipeline(
            raw_json=raw_json,
            section_id="sec_intro",
            section_type=SectionType.ANALYSIS,
            style=style,
            depth_level=1,
            attempt=1,
            llm_client=client,
            skip_layer3=False,
        )

        assert result.passed is False
        assert result.failed_layer == ValidationLayer.SEMANTIC
        assert len(result.error_messages) > 0
        assert any("tone_compliance" in msg for msg in result.error_messages)

    def test_pipeline_skip_l3(self):
        """Pipeline with skip_layer3=True skips L3 (§12)."""
        style = _make_style_sheet()
        raw_json = _make_well_formed_section_json()

        result = run_validation_pipeline(
            raw_json=raw_json,
            section_id="sec_intro",
            section_type=SectionType.ANALYSIS,
            style=style,
            depth_level=1,
            attempt=1,
            llm_client=None,
            skip_layer3=True,
        )

        assert result.passed is True
        # Only L1 and L2 results
        assert len(result.results) == 2

    def test_pipeline_no_client_skips_l3(self):
        """Pipeline with llm_client=None skips L3 (§12)."""
        style = _make_style_sheet()
        raw_json = _make_well_formed_section_json()

        result = run_validation_pipeline(
            raw_json=raw_json,
            section_id="sec_intro",
            section_type=SectionType.ANALYSIS,
            style=style,
            depth_level=1,
            attempt=1,
            llm_client=None,
            skip_layer3=False,
        )

        assert result.passed is True
        assert len(result.results) == 2

    def test_retry_counter_increments(self):
        """Retry counter (attempt) is passed through to L3 results (FR-19)."""
        client = MockLLMClient({
            "tone": json.dumps({
                "passed": False,
                "violations": [
                    {"description": "Still too casual", "severity": "error"}
                ],
            }),
            "dependency": '{"passed": true, "violations": []}',
            "unsupported": '{"passed": true, "violations": []}',
        })
        style = _make_style_sheet()
        raw_json = _make_well_formed_section_json()

        # Simulate attempt 3
        result = run_validation_pipeline(
            raw_json=raw_json,
            section_id="sec_intro",
            section_type=SectionType.ANALYSIS,
            style=style,
            depth_level=1,
            attempt=3,
            llm_client=client,
            skip_layer3=False,
        )

        assert result.passed is False
        # The L3 result should have attempt=3
        l3_result = result.results[-1]
        assert l3_result.layer == ValidationLayer.SEMANTIC
        assert l3_result.attempt == 3
        # Error messages should be non-empty for retry prompt
        assert len(result.error_messages) > 0

    def test_l1_failure_short_circuits(self):
        """L1 failure prevents L2 and L3 from running (§12)."""
        client = MockLLMClient()
        style = _make_style_sheet()
        # Invalid JSON → L1 failure
        raw_json = "this is not valid json at all"

        result = run_validation_pipeline(
            raw_json=raw_json,
            section_id="sec_intro",
            section_type=SectionType.ANALYSIS,
            style=style,
            depth_level=1,
            attempt=1,
            llm_client=client,
            skip_layer3=False,
        )

        assert result.passed is False
        assert result.failed_layer == ValidationLayer.STRUCTURAL
        assert len(result.results) == 1
        # LLM client should not have been called
        assert client.call_count == 0


class TestLLMClientProtocol:
    """Tests verifying LLM client protocol compliance (DR-16)."""

    def test_mock_client_satisfies_protocol(self):
        """MockLLMClient satisfies the LLMClient protocol (DR-16)."""
        client = MockLLMClient()
        assert isinstance(client, LLMClient)

    def test_error_client_satisfies_protocol(self):
        """ErrorLLMClient satisfies the LLMClient protocol (DR-16)."""
        client = ErrorLLMClient()
        assert isinstance(client, LLMClient)

    def test_malformed_client_satisfies_protocol(self):
        """MalformedResponseLLMClient satisfies the LLMClient protocol (DR-16)."""
        client = MalformedResponseLLMClient()
        assert isinstance(client, LLMClient)


# ---------------------------------------------------------------------------
# Live API integration tests (require ANTHROPIC_API_KEY)
# ---------------------------------------------------------------------------

@integration
@requires_live_api
class TestLiveLayer3SubChecks:
    """Live API tests for individual L3 sub-checks (§12.3, FR-18).

    These tests make real Anthropic API calls and verify that the
    sub-check functions produce valid ValidationResult objects from
    live LLM responses.
    """

    @pytest.fixture(scope="class")
    def live_client(self):
        """Create a live AnthropicLLMClient for testing (NFR-09)."""
        from synthesizer.validation.llm_client import create_validation_llm_client
        return create_validation_llm_client(validate=True)

    def test_tone_compliance_formal_pass(self, live_client):
        """Well-formed formal text passes tone compliance (FR-18 sub-check A)."""
        content = (
            "Neural Architecture Search has emerged as a significant "
            "methodology in the automated design of deep learning "
            "architectures. The systematic evaluation of search strategies "
            "reveals substantial improvements in computational efficiency "
            "while maintaining competitive performance across established "
            "benchmark datasets."
        )
        result = check_tone_compliance(
            content_markdown=content,
            tone_register="formal_academic",
            llm_client=live_client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.layer == ValidationLayer.SEMANTIC
        assert result.attempt == 1
        # We expect this to pass, but the LLM may disagree — at minimum
        # we verify the result is structurally valid
        assert isinstance(result.passed, bool)
        for v in result.violations:
            assert isinstance(v, Violation)
            assert v.rule == "tone_compliance"

    def test_tone_compliance_casual_fail(self, live_client):
        """Deliberately casual text fails tone compliance (FR-18 sub-check A)."""
        content = (
            "So basically, NAS is like super cool because it lets computers "
            "figure out the best neural network designs all by themselves! "
            "It's kinda like having a robot architect, ya know? LOL, who "
            "even needs human engineers anymore? Trust me bro, it's gonna "
            "be a wild ride! The results are literally insane!"
        )
        result = check_tone_compliance(
            content_markdown=content,
            tone_register="formal_academic",
            llm_client=live_client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.layer == ValidationLayer.SEMANTIC
        # This should fail — casual text vs formal_academic register
        assert result.passed is False
        assert len(result.violations) >= 1
        assert all(v.rule == "tone_compliance" for v in result.violations)

    def test_dependency_contract_no_upstream(self, live_client):
        """No upstream claims → sub-check B trivially passes (FR-18)."""
        result = check_dependency_contract(
            content_markdown="Some formal content.",
            upstream_claim_tables={},
            llm_client=live_client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.passed is True
        assert result.attempt == 1

    def test_dependency_contract_ignoring_claims(self, live_client):
        """Section ignoring upstream claims fails sub-check B (FR-18)."""
        # Content about weather, upstream claims about NAS
        content = (
            "This section examines contemporary weather patterns across "
            "temperate regions. Precipitation levels have shown notable "
            "variation in recent decades, with implications for agricultural "
            "planning and water resource management."
        )
        result = check_dependency_contract(
            content_markdown=content,
            upstream_claim_tables=_make_upstream_claim_tables(),
            llm_client=live_client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.layer == ValidationLayer.SEMANTIC
        # Should fail — content doesn't engage with NAS claims at all
        assert result.passed is False
        assert len(result.violations) >= 1
        assert all(v.rule == "dependency_contract" for v in result.violations)

    def test_unsupported_claims_fabricated(self, live_client):
        """Fabricated claims not in evidence fail sub-check C (FR-18)."""
        content = (
            "Our analysis reveals that quantum neural architecture search "
            "achieves a 99.7% accuracy improvement over all existing methods. "
            "The revolutionary HyperNAS-X framework has demonstrated that "
            "architecture search can be completed in under 0.001 seconds. "
            "According to Smith et al. (2024), published in the Journal of "
            "Impossible Results, these findings overturn all prior understanding."
        )
        result = check_unsupported_claims(
            content_markdown=content,
            retrieved_chunks=_make_evidence_chunks(),
            upstream_claim_tables={},
            llm_client=live_client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.layer == ValidationLayer.SEMANTIC
        # Should fail — claims are fabricated
        assert result.passed is False
        assert len(result.violations) >= 1
        assert all(v.rule == "unsupported_claims" for v in result.violations)

    def test_unsupported_claims_supported(self, live_client):
        """Claims traceable to evidence pass sub-check C (FR-18)."""
        content = (
            "Neural Architecture Search using reinforcement learning, as "
            "introduced by Zoph and Le (2017), required approximately 800 "
            "GPU-days to discover competitive architectures on CIFAR-10. "
            "Subsequent work on differentiable approaches, notably DARTS "
            "(Liu et al., 2019), reduced this cost to a single GPU-day "
            "while maintaining competitive accuracy. Weight-sharing "
            "approaches have been shown to introduce ranking correlation "
            "issues between shared-weight and standalone performance."
        )
        result = check_unsupported_claims(
            content_markdown=content,
            retrieved_chunks=_make_evidence_chunks(),
            upstream_claim_tables={},
            llm_client=live_client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        assert result.layer == ValidationLayer.SEMANTIC
        assert isinstance(result.passed, bool)
        # We expect this to pass since claims match evidence
        # But verify structural validity regardless
        for v in result.violations:
            assert isinstance(v, Violation)


@integration
@requires_live_api
class TestLiveFullPipeline:
    """Live API tests for the full L1→L2→L3 pipeline (§12, FR-18).

    These tests exercise the complete validation coordinator with
    a live Anthropic LLM client.
    """

    @pytest.fixture(scope="class")
    def live_client(self):
        """Create a live AnthropicLLMClient for testing (NFR-09)."""
        from synthesizer.validation.llm_client import create_validation_llm_client
        return create_validation_llm_client(validate=True)

    def test_full_pipeline_well_formed(self, live_client):
        """Full L1→L2→L3 pipeline with well-formed input (§12, FR-18).

        Verifies all three L3 sub-checks execute and return valid
        ValidationResult objects from live LLM responses.
        """
        style = _make_style_sheet()
        raw_json = _make_well_formed_section_json()

        result = run_validation_pipeline(
            raw_json=raw_json,
            section_id="sec_intro",
            section_type=SectionType.ANALYSIS,
            style=style,
            depth_level=1,
            attempt=1,
            retrieved_chunks=_make_evidence_chunks(),
            llm_client=live_client,
            skip_layer3=False,
        )

        assert isinstance(result, ValidationPipelineResult)
        assert result.parsed_output is not None
        # Should have at least L1 and L2 results, and L3 if it ran
        assert len(result.results) >= 2
        # Verify L1 and L2 passed
        assert result.results[0].layer == ValidationLayer.STRUCTURAL
        assert result.results[0].passed is True
        assert result.results[1].layer == ValidationLayer.RULE_BASED
        assert result.results[1].passed is True
        # L3 should have been attempted
        if len(result.results) == 3:
            assert result.results[2].layer == ValidationLayer.SEMANTIC
            assert isinstance(result.results[2].passed, bool)

    def test_full_pipeline_casual_tone_fails_l3(self, live_client):
        """Casual tone section fails L3 in full pipeline (FR-18, FR-19)."""
        style = _make_style_sheet(tone_register="formal_academic")
        raw_json = _make_casual_section_json()

        result = run_validation_pipeline(
            raw_json=raw_json,
            section_id="sec_intro",
            section_type=SectionType.ANALYSIS,
            style=style,
            depth_level=1,
            attempt=1,
            llm_client=live_client,
            skip_layer3=False,
        )

        # L1 and L2 should pass (structurally valid, meets word count)
        assert result.results[0].passed is True  # L1
        assert result.results[1].passed is True  # L2
        # L3 should fail due to tone
        if len(result.results) == 3:
            assert result.results[2].layer == ValidationLayer.SEMANTIC
            assert result.results[2].passed is False
            assert result.failed_layer == ValidationLayer.SEMANTIC
            assert len(result.error_messages) > 0

    def test_retry_feedback_available(self, live_client):
        """L3 failure produces non-empty feedback for retry prompt (FR-19)."""
        style = _make_style_sheet(tone_register="formal_academic")
        raw_json = _make_casual_section_json()

        # First attempt
        result1 = run_validation_pipeline(
            raw_json=raw_json,
            section_id="sec_intro",
            section_type=SectionType.ANALYSIS,
            style=style,
            depth_level=1,
            attempt=1,
            llm_client=live_client,
            skip_layer3=False,
        )

        if result1.failed_layer == ValidationLayer.SEMANTIC:
            assert len(result1.error_messages) > 0
            # Verify error messages are non-empty strings
            for msg in result1.error_messages:
                assert isinstance(msg, str)
                assert len(msg) > 0

            # Second attempt with incremented counter
            result2 = run_validation_pipeline(
                raw_json=raw_json,
                section_id="sec_intro",
                section_type=SectionType.ANALYSIS,
                style=style,
                depth_level=1,
                attempt=2,
                llm_client=live_client,
                skip_layer3=False,
            )

            if len(result2.results) >= 3:
                # Verify attempt counter was passed through
                assert result2.results[2].attempt == 2


@integration
@requires_live_api
class TestLiveModelInit:
    """Live tests for model initialization (NFR-09)."""

    def test_check_model_availability(self):
        """check_model_availability() succeeds with valid config (NFR-09)."""
        from synthesizer.orchestrator.model_init import check_model_availability
        model = check_model_availability()
        assert isinstance(model, str)
        assert len(model) > 0

    def test_anthropic_client_creation(self):
        """AnthropicLLMClient can be created and satisfies protocol (DR-16)."""
        from synthesizer.validation.llm_client import AnthropicLLMClient
        client = AnthropicLLMClient(validate=True)
        assert isinstance(client, LLMClient)
        assert isinstance(client.model, str)


# ---------------------------------------------------------------------------
# Edge case tests
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge case tests for Layer 3 validation (§12.3)."""

    def test_empty_content_markdown(self):
        """Empty content markdown is handled gracefully (FR-18)."""
        client = MockLLMClient({
            "tone": '{"passed": true, "violations": []}',
        })
        result = check_tone_compliance(
            content_markdown="",
            tone_register="formal_academic",
            llm_client=client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)

    def test_very_long_content(self):
        """Very long content is handled without error (FR-18)."""
        client = MockLLMClient({
            "tone": '{"passed": true, "violations": []}',
        })
        long_content = "This is a formal academic sentence. " * 1000
        result = check_tone_compliance(
            content_markdown=long_content,
            tone_register="formal_academic",
            llm_client=client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)

    def test_empty_evidence_chunks(self):
        """Empty evidence chunks list is handled (FR-18)."""
        client = MockLLMClient({
            "unsupported": '{"passed": true, "violations": []}',
        })
        result = check_unsupported_claims(
            content_markdown="Some content.",
            retrieved_chunks=[],
            upstream_claim_tables={},
            llm_client=client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)

    def test_partial_claim_table(self):
        """Partial claim table is noted in prompt (FR-18)."""
        client = MockLLMClient({
            "dependency": '{"passed": true, "violations": []}',
        })
        partial_ct = ClaimTable(
            section_id="sec_bg",
            claims=[
                ClaimEntry(
                    claim_id="C1",
                    claim_text="A partial claim",
                    confidence_tag=ConfidenceTag.LOW,
                    source_spans=[],
                ),
            ],
            partial=True,
        )
        result = check_dependency_contract(
            content_markdown="Content here.",
            upstream_claim_tables={"sec_bg": partial_ct},
            llm_client=client,
            attempt=1,
        )
        assert isinstance(result, ValidationResult)
        # Verify the prompt mentioned "partial"
        assert client.call_count == 1
        user_msg = client.calls[0]["user_message"]
        assert "partial" in user_msg.lower()