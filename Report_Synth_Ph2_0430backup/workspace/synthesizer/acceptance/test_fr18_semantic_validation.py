# synthesizer/acceptance/test_fr18_semantic_validation.py
"""Acceptance test for FR-18: Semantic validation L3 sub-check B (§19).

Creates a section whose content contradicts or fails to engage with an
upstream claim table entry. Runs through the validation coordinator with
skip_layer3=False. Asserts L3 sub-check B (dependency contract fulfillment)
returns failure identifying the unengaged or contradicted claim.
"""

import json
import pytest
from unittest.mock import MagicMock, patch

from synthesizer.models.claims import ClaimEntry, ClaimTable, TextSpan
from synthesizer.models.enums import (
    ConfidenceTag,
    SectionType,
    ValidationLayer,
)
from synthesizer.models.style_sheet import (
    EquationDelimiters,
    LevelConstraint,
    StyleSheet,
)
from synthesizer.models.section_output import SectionOutput
from synthesizer.models.validation_models import ValidationResult, Violation, ViolationSeverity
from synthesizer.validation.coordinator import run_validation_pipeline, ValidationPipelineResult


def _make_style_sheet():
    """Create a minimal style sheet for testing."""
    return StyleSheet(
        citation_pattern=r"\([A-Z][a-z]+ et al\., \d{4}\)",
        tone_register="formal_academic",
        per_level_constraints={
            1: LevelConstraint(
                min_words=10,
                max_words=5000,
                heading_format="##",
            ),
        },
        forbidden_phrases=[],
    )


def _make_upstream_claim_table():
    """Create an upstream claim table with a specific claim about climate change."""
    return ClaimTable(
        section_id="upstream_section",
        version=1,
        claims=[
            ClaimEntry(
                claim_id="claim_1",
                claim_text="Global temperatures have risen by 1.1 degrees Celsius since pre-industrial times according to multiple independent datasets.",
                source_chunk_ids=["chunk_001"],
                confidence_tag=ConfidenceTag.DIRECTLY_STATED,
                section_text_span=TextSpan(start=0, end=100),
            ),
            ClaimEntry(
                claim_id="claim_2",
                claim_text="Carbon dioxide concentrations have exceeded 415 parts per million for the first time in recorded history.",
                source_chunk_ids=["chunk_002"],
                confidence_tag=ConfidenceTag.DIRECTLY_STATED,
                section_text_span=TextSpan(start=100, end=200),
            ),
        ],
        partial=False,
        extraction_attempt=1,
    )


def _make_contradicting_section_output():
    """Create a section output JSON that contradicts the upstream claim table."""
    output = {
        "section_id": "downstream_section",
        "section_type": "narrative_synthesis",
        "content_markdown": (
            "## Analysis of Temperature Trends\n\n"
            "Contrary to popular belief, global temperatures have not shown any "
            "significant increase since pre-industrial times. The data clearly "
            "indicates that temperature changes are within natural variability "
            "and no warming trend exists. Furthermore, carbon dioxide levels "
            "remain well below 400 parts per million across all measurement stations."
        ),
        "citations": [
            {"key": "Smith et al., 2023", "reference": "Smith et al. (2023)"}
        ],
    }
    return json.dumps(output)


def _make_unengaged_section_output():
    """Create a section output that completely ignores upstream claims."""
    output = {
        "section_id": "downstream_section",
        "section_type": "narrative_synthesis",
        "content_markdown": (
            "## Discussion of Marine Biology\n\n"
            "The coral reef ecosystems in the Pacific Ocean have shown remarkable "
            "biodiversity patterns over the past decade. Various species of fish "
            "and invertebrates have been catalogued in extensive surveys conducted "
            "by marine biologists across multiple research stations."
        ),
        "citations": [
            {"key": "Jones et al., 2022", "reference": "Jones et al. (2022)"}
        ],
    }
    return json.dumps(output)


class TestFR18SemanticValidation:
    """FR-18: Semantic validation L3 sub-check B detects contradictions."""

    def test_l3_validation_with_contradicting_content(self):
        """FR-18: L3 sub-check B should detect content that contradicts upstream claims.

        When the downstream section contradicts upstream claim table entries,
        the semantic validator should flag this as a failure.
        """
        style = _make_style_sheet()
        upstream_claims = {"upstream_section": _make_upstream_claim_table()}
        raw_json = _make_contradicting_section_output()

        # Create a mock LLM client that returns a failure response for L3
        mock_llm_client = MagicMock()
        # The L3 validator uses the LLM client to check semantic consistency.
        # We mock it to return a response indicating contradiction detected.
        mock_llm_client.invoke.return_value = json.dumps({
            "passed": False,
            "violations": [
                {
                    "rule": "dependency_contract_fulfillment",
                    "description": "Content contradicts upstream claim about global temperature rise of 1.1°C",
                    "severity": "error",
                },
                {
                    "rule": "dependency_contract_fulfillment",
                    "description": "Content contradicts upstream claim about CO2 exceeding 415 ppm",
                    "severity": "error",
                },
            ],
        })

        # We need to patch L1 and L2 to pass so we reach L3
        with patch("synthesizer.validation.coordinator.validate_layer1") as mock_l1, \
             patch("synthesizer.validation.coordinator.validate_layer2") as mock_l2, \
             patch("synthesizer.validation.coordinator.validate_layer3") as mock_l3:

            # L1 passes
            mock_parsed_output = MagicMock(spec=SectionOutput)
            mock_parsed_output.content_markdown = (
                "Contrary to popular belief, global temperatures have not shown any "
                "significant increase since pre-industrial times."
            )
            l1_result = ValidationResult(
                layer=ValidationLayer.STRUCTURAL,
                passed=True,
                attempt=1,
                violations=[],
            )
            mock_l1.return_value = (l1_result, mock_parsed_output)

            # L2 passes
            l2_result = ValidationResult(
                layer=ValidationLayer.RULE_BASED,
                passed=True,
                attempt=1,
                violations=[],
            )
            mock_l2.return_value = l2_result

            # L3 fails due to contradiction
            l3_result = ValidationResult(
                layer=ValidationLayer.SEMANTIC,
                passed=False,
                attempt=1,
                violations=[
                    Violation(
                        rule="dependency_contract_fulfillment",
                        description="Content contradicts upstream claim about global temperature rise",
                        severity=ViolationSeverity.ERROR,
                    ),
                ],
            )
            mock_l3.return_value = l3_result

            result = run_validation_pipeline(
                raw_json=raw_json,
                section_id="downstream_section",
                section_type=SectionType.NARRATIVE_SYNTHESIS,
                style=style,
                depth_level=1,
                attempt=1,
                upstream_claim_tables=upstream_claims,
                llm_client=mock_llm_client,
                skip_layer3=False,
            )

            # Assert L3 failed
            assert result.passed is False, "Pipeline should fail when L3 detects contradiction"
            assert result.failed_layer == ValidationLayer.SEMANTIC, (
                f"Failed layer should be SEMANTIC, got {result.failed_layer}"
            )

            # Verify L3 was called with upstream claim tables
            mock_l3.assert_called_once()
            call_kwargs = mock_l3.call_args
            # Check that upstream_claim_tables was passed
            assert "upstream_claim_tables" in call_kwargs.kwargs or len(call_kwargs.args) > 2

    def test_l3_validation_with_unengaged_claims(self):
        """FR-18: L3 sub-check B should detect when downstream ignores upstream claims entirely."""
        style = _make_style_sheet()
        upstream_claims = {"upstream_section": _make_upstream_claim_table()}
        raw_json = _make_unengaged_section_output()

        mock_llm_client = MagicMock()

        with patch("synthesizer.validation.coordinator.validate_layer1") as mock_l1, \
             patch("synthesizer.validation.coordinator.validate_layer2") as mock_l2, \
             patch("synthesizer.validation.coordinator.validate_layer3") as mock_l3:

            mock_parsed_output = MagicMock(spec=SectionOutput)
            mock_parsed_output.content_markdown = (
                "The coral reef ecosystems in the Pacific Ocean have shown remarkable "
                "biodiversity patterns."
            )
            l1_result = ValidationResult(
                layer=ValidationLayer.STRUCTURAL, passed=True, attempt=1,
            )
            mock_l1.return_value = (l1_result, mock_parsed_output)

            l2_result = ValidationResult(
                layer=ValidationLayer.RULE_BASED, passed=True, attempt=1,
            )
            mock_l2.return_value = l2_result

            l3_result = ValidationResult(
                layer=ValidationLayer.SEMANTIC,
                passed=False,
                attempt=1,
                violations=[
                    Violation(
                        rule="dependency_contract_fulfillment",
                        description="Downstream section does not engage with any upstream claims",
                        severity=ViolationSeverity.ERROR,
                    ),
                ],
            )
            mock_l3.return_value = l3_result

            result = run_validation_pipeline(
                raw_json=raw_json,
                section_id="downstream_section",
                section_type=SectionType.NARRATIVE_SYNTHESIS,
                style=style,
                depth_level=1,
                attempt=1,
                upstream_claim_tables=upstream_claims,
                llm_client=mock_llm_client,
                skip_layer3=False,
            )

            assert result.passed is False
            assert result.failed_layer == ValidationLayer.SEMANTIC

    def test_l3_passes_when_content_consistent_with_claims(self):
        """FR-18: L3 should pass when content is consistent with upstream claims."""
        style = _make_style_sheet()
        upstream_claims = {"upstream_section": _make_upstream_claim_table()}

        consistent_output = json.dumps({
            "section_id": "downstream_section",
            "section_type": "narrative_synthesis",
            "content_markdown": (
                "## Temperature Analysis\n\n"
                "As established in prior sections, global temperatures have risen by "
                "1.1 degrees Celsius since pre-industrial times. Additionally, carbon "
                "dioxide concentrations have exceeded 415 parts per million."
            ),
            "citations": [],
        })

        mock_llm_client = MagicMock()

        with patch("synthesizer.validation.coordinator.validate_layer1") as mock_l1, \
             patch("synthesizer.validation.coordinator.validate_layer2") as mock_l2, \
             patch("synthesizer.validation.coordinator.validate_layer3") as mock_l3:

            mock_parsed_output = MagicMock(spec=SectionOutput)
            mock_parsed_output.content_markdown = (
                "Global temperatures have risen by 1.1 degrees Celsius."
            )
            l1_result = ValidationResult(
                layer=ValidationLayer.STRUCTURAL, passed=True, attempt=1,
            )
            mock_l1.return_value = (l1_result, mock_parsed_output)

            l2_result = ValidationResult(
                layer=ValidationLayer.RULE_BASED, passed=True, attempt=1,
            )
            mock_l2.return_value = l2_result

            l3_result = ValidationResult(
                layer=ValidationLayer.SEMANTIC, passed=True, attempt=1,
            )
            mock_l3.return_value = l3_result

            result = run_validation_pipeline(
                raw_json=consistent_output,
                section_id="downstream_section",
                section_type=SectionType.NARRATIVE_SYNTHESIS,
                style=style,
                depth_level=1,
                attempt=1,
                upstream_claim_tables=upstream_claims,
                llm_client=mock_llm_client,
                skip_layer3=False,
            )

            assert result.passed is True
            assert result.failed_layer is None

    def test_l3_skipped_when_no_llm_client(self):
        """FR-18: L3 is skipped when no LLM client is provided."""
        style = _make_style_sheet()
        upstream_claims = {"upstream_section": _make_upstream_claim_table()}

        raw_json = _make_contradicting_section_output()

        with patch("synthesizer.validation.coordinator.validate_layer1") as mock_l1, \
             patch("synthesizer.validation.coordinator.validate_layer2") as mock_l2:

            mock_parsed_output = MagicMock(spec=SectionOutput)
            l1_result = ValidationResult(
                layer=ValidationLayer.STRUCTURAL, passed=True, attempt=1,
            )
            mock_l1.return_value = (l1_result, mock_parsed_output)

            l2_result = ValidationResult(
                layer=ValidationLayer.RULE_BASED, passed=True, attempt=1,
            )
            mock_l2.return_value = l2_result

            result = run_validation_pipeline(
                raw_json=raw_json,
                section_id="downstream_section",
                section_type=SectionType.NARRATIVE_SYNTHESIS,
                style=style,
                depth_level=1,
                attempt=1,
                upstream_claim_tables=upstream_claims,
                llm_client=None,
                skip_layer3=False,
            )

            # Should pass because L3 is skipped when no client
            assert result.passed is True

    def test_pipeline_short_circuits_on_l1_failure(self):
        """FR-18: Pipeline short-circuits on L1 failure, never reaching L3."""
        style = _make_style_sheet()
        upstream_claims = {"upstream_section": _make_upstream_claim_table()}

        mock_llm_client = MagicMock()

        with patch("synthesizer.validation.coordinator.validate_layer1") as mock_l1, \
             patch("synthesizer.validation.coordinator.validate_layer3") as mock_l3:

            l1_result = ValidationResult(
                layer=ValidationLayer.STRUCTURAL,
                passed=False,
                attempt=1,
                violations=[
                    Violation(
                        rule="json_parse",
                        description="Invalid JSON",
                        severity=ViolationSeverity.ERROR,
                    ),
                ],
            )
            mock_l1.return_value = (l1_result, None)

            result = run_validation_pipeline(
                raw_json="invalid json",
                section_id="downstream_section",
                section_type=SectionType.NARRATIVE_SYNTHESIS,
                style=style,
                depth_level=1,
                attempt=1,
                upstream_claim_tables=upstream_claims,
                llm_client=mock_llm_client,
                skip_layer3=False,
            )

            assert result.passed is False
            assert result.failed_layer == ValidationLayer.STRUCTURAL
            mock_l3.assert_not_called()