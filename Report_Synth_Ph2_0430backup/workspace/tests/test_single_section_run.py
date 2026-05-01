# tests/test_single_section_run.py
"""Tests for single-section run through the full orchestrator pipeline.

Covers:
  - FR-01: Report plan loading
  - FR-04: Style sheet loading
  - FR-06: Topological generation ordering
  - FR-08: Generation prerequisites
  - FR-11–FR-13: Prompt assembly
  - FR-14–FR-19: Validation pipeline
  - FR-20–FR-22: Claim extraction
  - NFR-02: Token tracking
  - NFR-05: Deterministic output structure
  - NFR-06: Structured event emission
  - NFR-07: Post-run metrics
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch, call

import pytest

from synthesizer.models.enums import SectionLifecycleState, SectionType, ValidationLayer
from synthesizer.models.state import RunState, SectionState


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def output_dir():
    """Create a temporary output directory and clean up after test."""
    d = tempfile.mkdtemp(prefix="synth_test_")
    yield Path(d)
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def single_section_plan(tmp_path):
    """Create a minimal single-section report plan JSON file."""
    plan = {
        "version": "1.0",
        "title": "Test Report",
        "sections": [
            {
                "section_id": "sec_intro",
                "title": "Introduction",
                "section_type": "narrative_synthesis",
                "depth_level": 1,
                "dependencies": [],
                "source_queries": ["What is the introduction about?"],
                "description": "An introductory section.",
            }
        ],
    }
    plan_path = tmp_path / "report_plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    return plan_path


@pytest.fixture
def style_sheet_file(tmp_path):
    """Create a minimal style sheet JSON file."""
    style = {
        "tone_register": "academic",
        "citation_style": "APA",
        "heading_format": "title_case",
        "min_words_per_section": 50,
        "max_words_per_section": 5000,
        "forbidden_phrases": [],
    }
    style_path = tmp_path / "style_sheet.json"
    style_path.write_text(json.dumps(style), encoding="utf-8")
    return style_path


def _make_mock_generator_client(raw_text: str = None):
    """Create a mock generator client that returns valid section output JSON."""
    if raw_text is None:
        raw_text = json.dumps({
            "section_id": "sec_intro",
            "section_type": "narrative_synthesis",
            "title": "Introduction",
            "content_markdown": "This is the introduction section with enough words to pass validation. " * 10,
            "citations": [],
            "cross_references": [],
            "metadata": {},
        })
    client = MagicMock()
    client.invoke_with_usage.return_value = {
        "text": raw_text,
        "input_tokens": 150,
        "output_tokens": 200,
    }
    client.invoke.return_value = raw_text
    return client


def _make_mock_llm_client():
    """Create a mock LLM client for L3 validation, claim extraction, summary."""
    client = MagicMock()
    # For L3 validation — return a passing result
    client.invoke.return_value = json.dumps({"passed": True, "issues": []})
    return client


# ---------------------------------------------------------------------------
# Helpers to build mock validation pipeline result
# ---------------------------------------------------------------------------

def _make_passing_validation_result():
    """Build a mock ValidationPipelineResult that passes all layers."""
    from synthesizer.validation.coordinator import ValidationPipelineResult
    from synthesizer.models.section_output import SectionOutput
    from synthesizer.models.validation_models import ValidationResult

    content = "This is the introduction section with enough words to pass validation. " * 10

    parsed = MagicMock()
    parsed.content_markdown = content
    parsed.section_id = "sec_intro"

    l1_result = MagicMock()
    l1_result.layer = ValidationLayer.STRUCTURAL
    l1_result.passed = True
    l1_result.attempt = 1
    l1_result.model_dump.return_value = {"layer": "structural", "passed": True, "attempt": 1}

    result = ValidationPipelineResult()
    result.passed = True
    result.failed_layer = None
    result.results = [l1_result]
    result.parsed_output = parsed
    result.error_messages = []
    return result


# ---------------------------------------------------------------------------
# Test: Single-section run produces expected artifacts (FR-01, NFR-05)
# ---------------------------------------------------------------------------

class TestSingleSectionRun:
    """Test that a single-section run produces all expected output artifacts."""

    @patch("synthesizer.orchestrator.run.extract_claim_table")
    @patch("synthesizer.orchestrator.run.generate_summary_abstract")
    @patch("synthesizer.orchestrator.run.run_validation_pipeline")
    @patch("synthesizer.orchestrator.run.assemble_generation_prompt")
    @patch("synthesizer.orchestrator.run.load_style_sheet")
    @patch("synthesizer.orchestrator.run.load_report_plan")
    @patch("synthesizer.orchestrator.run.emit_run_started")
    @patch("synthesizer.orchestrator.run.emit_run_completed")
    @patch("synthesizer.orchestrator.run.emit_state_transition")
    @patch("synthesizer.orchestrator.run.compute_all_metrics")
    @patch("synthesizer.orchestrator.run.write_run_metrics")
    def test_produces_draft_claim_table_provenance(
        self,
        mock_write_metrics,
        mock_compute_metrics,
        mock_emit_transition,
        mock_emit_completed,
        mock_emit_started,
        mock_load_plan,
        mock_load_style,
        mock_assemble_prompt,
        mock_run_validation,
        mock_gen_summary,
        mock_extract_claims,
        output_dir,
        single_section_plan,
        style_sheet_file,
    ):
        """FR-01, NFR-05: Single-section run produces draft_v1.md, claim_table_v1.json,
        validation_log.json, and provenance.json in the correct output directory."""
        from synthesizer.orchestrator.run import run
        from synthesizer.models.report_plan import ReportPlan, SectionNode
        from synthesizer.models.style_sheet import StyleSheet
        from synthesizer.models.claims import ClaimTable

        # Setup mocks
        section = MagicMock()
        section.section_id = "sec_intro"
        section.title = "Introduction"
        section.section_type = SectionType.NARRATIVE_SYNTHESIS
        section.depth_level = 1
        section.dependencies = []
        section.source_queries = ["What is the introduction about?"]

        plan = MagicMock()
        plan.sections = [section]
        plan.version = "1.0"
        mock_load_plan.return_value = plan

        style = MagicMock()
        style.tone_register = "academic"
        mock_load_style.return_value = style

        # Mock prompt assembly
        prompt = MagicMock()
        prompt.system_prompt = "You are a report writer."
        prompt.user_message = "Write the introduction."
        prompt.max_output_tokens = 4000
        mock_assemble_prompt.return_value = prompt

        # Mock validation to pass
        mock_run_validation.return_value = _make_passing_validation_result()

        # Mock claim extraction
        claim_table = MagicMock()
        claim_table.partial = False
        claim_table.claims = []
        claim_table.model_dump.return_value = {"partial": False, "claims": []}
        mock_extract_claims.return_value = claim_table

        # Mock summary
        mock_gen_summary.return_value = "This is a summary abstract."

        # Mock metrics
        mock_compute_metrics.return_value = {
            "section_completion_rate": 1.0,
            "validation_pass_rate": 1.0,
            "avg_retry_count": 0.0,
            "escalation_rate": 0.0,
            "token_efficiency": 1.0,
            "claim_coverage": 1.0,
            "dependency_completeness": 1.0,
        }

        # Mock claim validation
        with patch("synthesizer.orchestrator.run.validate_claim_table") as mock_validate_ct:
            mock_validate_ct.return_value = MagicMock(passed=True, failure_reasons=[])

            generator_client = _make_mock_generator_client()

            run_state = run(
                report_plan_path=single_section_plan,
                style_sheet_path=style_sheet_file,
                output_dir=output_dir,
                model="test-model",
                generator_client=generator_client,
                llm_client=_make_mock_llm_client(),
            )

        # Assert output artifacts exist
        section_dir = output_dir / "sections" / "sec_intro"
        assert section_dir.is_dir(), "Section output directory should exist"
        assert (section_dir / "draft_v1.md").exists(), "draft_v1.md should be produced"
        assert (section_dir / "claim_table_v1.json").exists(), "claim_table_v1.json should be produced"
        assert (section_dir / "validation_log.json").exists(), "validation_log.json should be produced"
        assert (section_dir / "provenance.json").exists(), "provenance.json should be produced"

    @patch("synthesizer.orchestrator.run.extract_claim_table")
    @patch("synthesizer.orchestrator.run.generate_summary_abstract")
    @patch("synthesizer.orchestrator.run.run_validation_pipeline")
    @patch("synthesizer.orchestrator.run.assemble_generation_prompt")
    @patch("synthesizer.orchestrator.run.load_style_sheet")
    @patch("synthesizer.orchestrator.run.load_report_plan")
    @patch("synthesizer.orchestrator.run.emit_run_started")
    @patch("synthesizer.orchestrator.run.emit_run_completed")
    @patch("synthesizer.orchestrator.run.emit_state_transition")
    @patch("synthesizer.orchestrator.run.compute_all_metrics")
    @patch("synthesizer.orchestrator.run.write_run_metrics")
    def test_run_state_checkpoint_written_with_finalized_section(
        self,
        mock_write_metrics,
        mock_compute_metrics,
        mock_emit_transition,
        mock_emit_completed,
        mock_emit_started,
        mock_load_plan,
        mock_load_style,
        mock_assemble_prompt,
        mock_run_validation,
        mock_gen_summary,
        mock_extract_claims,
        output_dir,
        single_section_plan,
        style_sheet_file,
    ):
        """NFR-03: RunState checkpoint (run_state.json) is written with at least one
        section in FINALIZED state."""
        from synthesizer.orchestrator.run import run

        section = MagicMock()
        section.section_id = "sec_intro"
        section.title = "Introduction"
        section.section_type = SectionType.NARRATIVE_SYNTHESIS
        section.depth_level = 1
        section.dependencies = []
        section.source_queries = []

        plan = MagicMock()
        plan.sections = [section]
        plan.version = "1.0"
        mock_load_plan.return_value = plan

        style = MagicMock()
        style.tone_register = "academic"
        mock_load_style.return_value = style

        prompt = MagicMock()
        prompt.system_prompt = "sys"
        prompt.user_message = "usr"
        prompt.max_output_tokens = 4000
        mock_assemble_prompt.return_value = prompt

        mock_run_validation.return_value = _make_passing_validation_result()

        claim_table = MagicMock()
        claim_table.partial = False
        claim_table.claims = []
        claim_table.model_dump.return_value = {"partial": False, "claims": []}
        mock_extract_claims.return_value = claim_table

        mock_gen_summary.return_value = "Summary."

        mock_compute_metrics.return_value = {
            "section_completion_rate": 1.0,
            "validation_pass_rate": 1.0,
            "avg_retry_count": 0.0,
            "escalation_rate": 0.0,
            "token_efficiency": 1.0,
            "claim_coverage": 1.0,
            "dependency_completeness": 1.0,
        }

        with patch("synthesizer.orchestrator.run.validate_claim_table") as mock_validate_ct:
            mock_validate_ct.return_value = MagicMock(passed=True, failure_reasons=[])

            generator_client = _make_mock_generator_client()
            run_state = run(
                report_plan_path=single_section_plan,
                style_sheet_path=style_sheet_file,
                output_dir=output_dir,
                model="test-model",
                generator_client=generator_client,
                llm_client=_make_mock_llm_client(),
            )

        # Check run_state.json exists
        run_state_path = output_dir / "run_state.json"
        assert run_state_path.exists(), "run_state.json should be written"

        # Parse and verify
        run_state_data = json.loads(run_state_path.read_text(encoding="utf-8"))
        assert "section_states" in run_state_data
        sec_state = run_state_data["section_states"]["sec_intro"]
        assert sec_state["state"] == "finalized", (
            f"Section should be FINALIZED, got {sec_state['state']}"
        )

    @patch("synthesizer.orchestrator.run.extract_claim_table")
    @patch("synthesizer.orchestrator.run.generate_summary_abstract")
    @patch("synthesizer.orchestrator.run.run_validation_pipeline")
    @patch("synthesizer.orchestrator.run.assemble_generation_prompt")
    @patch("synthesizer.orchestrator.run.load_style_sheet")
    @patch("synthesizer.orchestrator.run.load_report_plan")
    @patch("synthesizer.orchestrator.run.emit_run_started")
    @patch("synthesizer.orchestrator.run.emit_run_completed")
    @patch("synthesizer.orchestrator.run.emit_state_transition")
    @patch("synthesizer.orchestrator.run.compute_all_metrics")
    @patch("synthesizer.orchestrator.run.write_run_metrics")
    def test_token_tracker_records_usage(
        self,
        mock_write_metrics,
        mock_compute_metrics,
        mock_emit_transition,
        mock_emit_completed,
        mock_emit_started,
        mock_load_plan,
        mock_load_style,
        mock_assemble_prompt,
        mock_run_validation,
        mock_gen_summary,
        mock_extract_claims,
        output_dir,
        single_section_plan,
        style_sheet_file,
    ):
        """NFR-02: cumulative_input_tokens and cumulative_output_tokens in RunState
        are > 0 after a successful run."""
        from synthesizer.orchestrator.run import run

        section = MagicMock()
        section.section_id = "sec_intro"
        section.title = "Introduction"
        section.section_type = SectionType.NARRATIVE_SYNTHESIS
        section.depth_level = 1
        section.dependencies = []
        section.source_queries = []

        plan = MagicMock()
        plan.sections = [section]
        plan.version = "1.0"
        mock_load_plan.return_value = plan

        style = MagicMock()
        style.tone_register = "academic"
        mock_load_style.return_value = style

        prompt = MagicMock()
        prompt.system_prompt = "sys"
        prompt.user_message = "usr"
        prompt.max_output_tokens = 4000
        mock_assemble_prompt.return_value = prompt

        mock_run_validation.return_value = _make_passing_validation_result()

        claim_table = MagicMock()
        claim_table.partial = False
        claim_table.claims = []
        claim_table.model_dump.return_value = {"partial": False, "claims": []}
        mock_extract_claims.return_value = claim_table

        mock_gen_summary.return_value = "Summary."

        mock_compute_metrics.return_value = {
            "section_completion_rate": 1.0,
            "validation_pass_rate": 1.0,
            "avg_retry_count": 0.0,
            "escalation_rate": 0.0,
            "token_efficiency": 1.0,
            "claim_coverage": 1.0,
            "dependency_completeness": 1.0,
        }

        with patch("synthesizer.orchestrator.run.validate_claim_table") as mock_validate_ct:
            mock_validate_ct.return_value = MagicMock(passed=True, failure_reasons=[])

            generator_client = _make_mock_generator_client()
            run_state = run(
                report_plan_path=single_section_plan,
                style_sheet_path=style_sheet_file,
                output_dir=output_dir,
                model="test-model",
                generator_client=generator_client,
                llm_client=_make_mock_llm_client(),
            )

        assert run_state.cumulative_input_tokens > 0, (
            "cumulative_input_tokens should be > 0 after run"
        )
        assert run_state.cumulative_output_tokens > 0, (
            "cumulative_output_tokens should be > 0 after run"
        )

    @patch("synthesizer.orchestrator.run.extract_claim_table")
    @patch("synthesizer.orchestrator.run.generate_summary_abstract")
    @patch("synthesizer.orchestrator.run.run_validation_pipeline")
    @patch("synthesizer.orchestrator.run.assemble_generation_prompt")
    @patch("synthesizer.orchestrator.run.load_style_sheet")
    @patch("synthesizer.orchestrator.run.load_report_plan")
    @patch("synthesizer.orchestrator.run.emit_run_started")
    @patch("synthesizer.orchestrator.run.emit_run_completed")
    @patch("synthesizer.orchestrator.run.emit_state_transition")
    @patch("synthesizer.orchestrator.run.compute_all_metrics")
    @patch("synthesizer.orchestrator.run.write_run_metrics")
    def test_event_log_contains_state_transitions(
        self,
        mock_write_metrics,
        mock_compute_metrics,
        mock_emit_transition,
        mock_emit_completed,
        mock_emit_started,
        mock_load_plan,
        mock_load_style,
        mock_assemble_prompt,
        mock_run_validation,
        mock_gen_summary,
        mock_extract_claims,
        output_dir,
        single_section_plan,
        style_sheet_file,
    ):
        """NFR-06: Event log contains one structured event per state transition."""
        from synthesizer.orchestrator.run import run

        section = MagicMock()
        section.section_id = "sec_intro"
        section.title = "Introduction"
        section.section_type = SectionType.NARRATIVE_SYNTHESIS
        section.depth_level = 1
        section.dependencies = []
        section.source_queries = []

        plan = MagicMock()
        plan.sections = [section]
        plan.version = "1.0"
        mock_load_plan.return_value = plan

        style = MagicMock()
        style.tone_register = "academic"
        mock_load_style.return_value = style

        prompt = MagicMock()
        prompt.system_prompt = "sys"
        prompt.user_message = "usr"
        prompt.max_output_tokens = 4000
        mock_assemble_prompt.return_value = prompt

        mock_run_validation.return_value = _make_passing_validation_result()

        claim_table = MagicMock()
        claim_table.partial = False
        claim_table.claims = []
        claim_table.model_dump.return_value = {"partial": False, "claims": []}
        mock_extract_claims.return_value = claim_table

        mock_gen_summary.return_value = "Summary."

        mock_compute_metrics.return_value = {
            "section_completion_rate": 1.0,
            "validation_pass_rate": 1.0,
            "avg_retry_count": 0.0,
            "escalation_rate": 0.0,
            "token_efficiency": 1.0,
            "claim_coverage": 1.0,
            "dependency_completeness": 1.0,
        }

        with patch("synthesizer.orchestrator.run.validate_claim_table") as mock_validate_ct:
            mock_validate_ct.return_value = MagicMock(passed=True, failure_reasons=[])

            generator_client = _make_mock_generator_client()
            run_state = run(
                report_plan_path=single_section_plan,
                style_sheet_path=style_sheet_file,
                output_dir=output_dir,
                model="test-model",
                generator_client=generator_client,
                llm_client=_make_mock_llm_client(),
            )

        # Verify emit_state_transition was called for each transition:
        # QUEUED -> GENERATING -> DRAFTED -> FINALIZED = 3 transitions
        assert mock_emit_transition.call_count >= 3, (
            f"Expected at least 3 state transition events, got {mock_emit_transition.call_count}"
        )

        # Verify emit_run_started and emit_run_completed were called
        mock_emit_started.assert_called_once()
        mock_emit_completed.assert_called_once()

        # Check that transitions include the expected states
        transition_calls = mock_emit_transition.call_args_list
        to_states = [c.kwargs.get("to_state") or c[1].get("to_state", None)
                     for c in transition_calls]
        # Handle both positional and keyword args
        to_states_kw = []
        for c in transition_calls:
            kwargs = c.kwargs if c.kwargs else {}
            to_states_kw.append(kwargs.get("to_state"))

        assert "generating" in to_states_kw, "Should have transition to 'generating'"
        assert "drafted" in to_states_kw, "Should have transition to 'drafted'"
        assert "finalized" in to_states_kw, "Should have transition to 'finalized'"


class TestCLIEntryPoint:
    """Test the CLI entry point works."""

    @patch("synthesizer.orchestrator.run.run")
    def test_cli_runs_without_error(
        self,
        mock_run,
        output_dir,
        single_section_plan,
        style_sheet_file,
    ):
        """FR-01, FR-04: 'python -m synthesizer --report-plan ... --style-sheet ...'
        runs without error."""
        from synthesizer.__main__ import main

        # Mock run to return a valid RunState
        mock_state = MagicMock()
        mock_state.section_states = {
            "sec_intro": MagicMock(state=MagicMock(value="finalized"))
        }
        mock_state.cumulative_input_tokens = 100
        mock_state.cumulative_output_tokens = 200
        mock_run.return_value = mock_state

        import sys
        original_argv = sys.argv
        try:
            sys.argv = [
                "synthesizer",
                "--report-plan", str(single_section_plan),
                "--style-sheet", str(style_sheet_file),
                "--output-dir", str(output_dir),
                "--model", "test-model",
            ]
            exit_code = main()
        finally:
            sys.argv = original_argv

        assert exit_code == 0, f"CLI should exit with 0, got {exit_code}"
        mock_run.assert_called_once()

    def test_cli_missing_plan_file_returns_1(self, tmp_path, style_sheet_file):
        """CLI returns exit code 1 when report plan file doesn't exist."""
        from synthesizer.__main__ import main
        import sys

        original_argv = sys.argv
        try:
            sys.argv = [
                "synthesizer",
                "--report-plan", str(tmp_path / "nonexistent.json"),
                "--style-sheet", str(style_sheet_file),
            ]
            exit_code = main()
        finally:
            sys.argv = original_argv

        assert exit_code == 1