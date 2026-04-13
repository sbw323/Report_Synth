# synthesizer/validation/coordinator.py
"""Validation coordinator — sequential L1 → L2 → L3 pipeline (§12).

Runs all three validation layers in order, short-circuiting on failure.
Does NOT manage retries — that is the orchestrator's responsibility.

The coordinator is a pure function: given inputs, it runs validation
and returns results. State mutation (retry counters, validation history)
is handled by the caller.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from synthesizer.models.claims import ClaimTable
from synthesizer.models.enums import SectionType, ValidationLayer
from synthesizer.models.section_output import SectionOutput
from synthesizer.models.style_sheet import StyleSheet
from synthesizer.models.validation_models import ValidationResult
from synthesizer.retrieval.adapter import RankedChunk
from synthesizer.validation.layer1_structural import validate_layer1, format_layer1_errors
from synthesizer.validation.layer2_rules import validate_layer2, format_layer2_errors
from synthesizer.validation.layer3_semantic import validate_layer3, format_layer3_errors

logger = logging.getLogger(__name__)


@dataclass
class ValidationPipelineResult:
    """Aggregated result from the L1 → L2 → L3 validation pipeline.

    Attributes
    ----------
    passed : bool
        True only if all executed layers passed.
    failed_layer : Optional[ValidationLayer]
        The layer that failed, or None if all passed.
    results : list of ValidationResult
        Results from each layer that was executed (in order).
    parsed_output : Optional[SectionOutput]
        The validated SectionOutput from Layer 1, or None if L1 failed.
    error_messages : list of str
        Formatted error messages from the failing layer, suitable for
        inclusion in a retry prompt.
    """

    passed: bool = False
    failed_layer: Optional[ValidationLayer] = None
    results: List[ValidationResult] = field(default_factory=list)
    parsed_output: Optional[SectionOutput] = None
    error_messages: List[str] = field(default_factory=list)


def run_validation_pipeline(
    raw_json: str,
    section_id: str,
    section_type: SectionType,
    style: StyleSheet,
    depth_level: int,
    attempt: int = 1,
    tone_register: Optional[str] = None,
    upstream_claim_tables: Optional[Dict[str, ClaimTable]] = None,
    retrieved_chunks: Optional[List[RankedChunk]] = None,
    llm_client: Optional[object] = None,
    skip_layer3: bool = False,
) -> ValidationPipelineResult:
    """Run the sequential L1 → L2 → L3 validation pipeline (§12).

    Short-circuits on the first failing layer. Layer 3 is skipped
    if ``skip_layer3`` is True or if no ``llm_client`` is provided.

    Parameters
    ----------
    raw_json : str
        Raw JSON string from the Generator LLM call.
    section_id : str
        Expected section_id for consistency checking.
    section_type : SectionType
        Section type — determines the output schema for L1.
    style : StyleSheet
        Style sheet for L2 rule-based checks.
    depth_level : int
        Section depth level for heading/word-count constraint resolution.
    attempt : int
        Current attempt number (passed through to each layer).
    tone_register : str, optional
        Expected tone for L3 sub-check A. Defaults to style.tone_register.
    upstream_claim_tables : dict, optional
        Maps upstream section_id → ClaimTable for L3 sub-check B.
    retrieved_chunks : list of RankedChunk, optional
        Evidence chunks for L3 sub-check C.
    llm_client : object, optional
        LLM client for Layer 3 semantic checks. If None, L3 is skipped.
    skip_layer3 : bool
        If True, skip Layer 3 entirely (useful for component testing).

    Returns
    -------
    ValidationPipelineResult
        Aggregated result with pass/fail, failing layer, all results,
        parsed output (if L1 passed), and formatted error messages.
    """
    pipeline_result = ValidationPipelineResult()

    # --- Layer 1: Structural validation (deterministic) ---
    logger.info("Running Layer 1 (structural) validation for '%s'", section_id)
    l1_result, parsed_output = validate_layer1(
        raw_json=raw_json,
        section_type=section_type,
        section_id=section_id,
        attempt=attempt,
    )
    pipeline_result.results.append(l1_result)

    if not l1_result.passed:
        logger.warning("Layer 1 FAILED for '%s' (attempt %d)", section_id, attempt)
        pipeline_result.failed_layer = ValidationLayer.STRUCTURAL
        pipeline_result.error_messages = format_layer1_errors(l1_result)
        return pipeline_result

    pipeline_result.parsed_output = parsed_output
    logger.info("Layer 1 PASSED for '%s'", section_id)

    # --- Layer 2: Rule-based validation (deterministic) ---
    logger.info("Running Layer 2 (rule-based) validation for '%s'", section_id)
    l2_result = validate_layer2(
        output=parsed_output,
        style=style,
        section_type=section_type,
        depth_level=depth_level,
        attempt=attempt,
    )
    pipeline_result.results.append(l2_result)

    if not l2_result.passed:
        logger.warning("Layer 2 FAILED for '%s' (attempt %d)", section_id, attempt)
        pipeline_result.failed_layer = ValidationLayer.RULE_BASED
        pipeline_result.error_messages = format_layer2_errors(l2_result)
        return pipeline_result

    logger.info("Layer 2 PASSED for '%s'", section_id)

    # --- Layer 3: Semantic validation (LLM-based) ---
    if skip_layer3 or llm_client is None:
        logger.info("Layer 3 skipped for '%s' (skip_layer3=%s, llm_client=%s)",
                     section_id, skip_layer3, type(llm_client).__name__ if llm_client else "None")
        pipeline_result.passed = True
        return pipeline_result

    logger.info("Running Layer 3 (semantic) validation for '%s'", section_id)
    l3_result = validate_layer3(
        output=parsed_output,
        tone_register=tone_register or style.tone_register,
        upstream_claim_tables=upstream_claim_tables or {},
        retrieved_chunks=retrieved_chunks or [],
        llm_client=llm_client,
        attempt=attempt,
    )
    pipeline_result.results.append(l3_result)

    if not l3_result.passed:
        logger.warning("Layer 3 FAILED for '%s' (attempt %d)", section_id, attempt)
        pipeline_result.failed_layer = ValidationLayer.SEMANTIC
        pipeline_result.error_messages = format_layer3_errors(l3_result)
        return pipeline_result

    logger.info("Layer 3 PASSED for '%s'", section_id)
    pipeline_result.passed = True
    return pipeline_result