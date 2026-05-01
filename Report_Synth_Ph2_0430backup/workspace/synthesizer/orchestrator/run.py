# synthesizer/orchestrator/run.py
"""Main orchestrator run loop with retry and escalation (§6, §11, §12).

Chains all existing components — loaders, DAG builder, retrieval adapter,
prompt assembler, generator, validator coordinator, claim extractor,
summary abstractifier, and lifecycle module — into a sequential pipeline.

Implements:
  - Phase 1: Initialization (load plan, style, build DAGs, init state)
  - Phase 2: Section processing loop in topological order
  - Per-layer retry-with-feedback inner loop
  - Escalation on retry exhaustion (FR-19)
  - Post-validation claim extraction and summary abstraction (FR-20, FR-22)
  - Token tracking and budget enforcement (NFR-02)
  - Structured event emission at every state transition (NFR-06)
  - Phase 3: Completion — metrics computation and report assembly (NFR-07)

Governing spec sections: §6, §11, §12, §13, §14, §17
Functional requirements: FR-06, FR-08, FR-09, FR-10, FR-11, FR-12, FR-13,
    FR-14, FR-15, FR-16, FR-17, FR-18, FR-19, FR-20, FR-21, FR-22,
    FR-26, FR-27
Non-functional requirements: NFR-01, NFR-02, NFR-05, NFR-06, NFR-07
Open decisions preserved: DR-15, DR-16, DR-17, DR-18
"""

from __future__ import annotations

import json
import logging
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from synthesizer.config import (
    CLAIM_EXTRACTION_RETRY_LIMIT,
    LAYER1_RETRY_LIMIT,
    LAYER2_RETRY_LIMIT,
    LAYER3_RETRY_LIMIT,
    SYNTHESIZER_MODEL,
    SYNTHESIZER_OUTPUT_DIR,
    TOKEN_BUDGET_CEILING,
)
from synthesizer.dag import (
    DAG,
    build_finalization_dag,
    build_generation_dag,
    iter_topological,
)
from synthesizer.extraction.claim_extractor import extract_claim_table
from synthesizer.extraction.claim_validator import validate_claim_table
from synthesizer.extraction.summary_abstractifier import generate_summary_abstract
from synthesizer.loaders.plan_loader import load_report_plan
from synthesizer.loaders.style_loader import load_style_sheet
from synthesizer.models.enums import (
    SectionLifecycleState,
    ValidationLayer,
)
from synthesizer.models.provenance import ProvenanceRecord
from synthesizer.models.report_plan import ReportPlan, SectionNode
from synthesizer.models.state import RunState, SectionState
from synthesizer.models.style_sheet import StyleSheet
from synthesizer.observability.events import (
    emit_escalation_triggered,
    emit_run_completed,
    emit_run_failed,
    emit_run_started,
    emit_state_transition,
)
from synthesizer.observability.metrics import (
    compute_all_metrics,
    write_run_metrics,
)
from synthesizer.observability.tokens import (
    TokenBudgetExceededError,
    TokenTracker,
)
from synthesizer.orchestrator.lifecycle import (
    check_assembly_readiness,
    check_generation_prerequisites,
    transition_section_state,
)
from synthesizer.prompt.assembly import assemble_generation_prompt
from synthesizer.retrieval.adapter import (
    RankedChunk,
    RetrievalResult,
    RetrieverProtocol,
    retrieve_for_section,
)
from synthesizer.validation.coordinator import (
    ValidationPipelineResult,
    run_validation_pipeline,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Layer name constants for retry counter keys
# ---------------------------------------------------------------------------

_LAYER_KEY_MAP = {
    ValidationLayer.STRUCTURAL: "layer1",
    ValidationLayer.RULE_BASED: "layer2",
    ValidationLayer.SEMANTIC: "layer3",
}

_LAYER_RETRY_LIMITS = {
    "layer1": LAYER1_RETRY_LIMIT,
    "layer2": LAYER2_RETRY_LIMIT,
    "layer3": LAYER3_RETRY_LIMIT,
}

_LAYER_DISPLAY_NAMES = {
    "layer1": "Layer 1 (structural)",
    "layer2": "Layer 2 (rule-based)",
    "layer3": "Layer 3 (semantic)",
}


# ---------------------------------------------------------------------------
# LLM client protocol for the Generator role (§9.2.1, DR-16)
# ---------------------------------------------------------------------------

@runtime_checkable
class GeneratorLLMClient(Protocol):
    """Protocol for the Generator LLM client (§9.2.1, DR-16).

    The orchestrator injects this client for section content generation.
    Concrete implementations wrap the Anthropic SDK.
    """

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int,
    ) -> str:
        """Invoke the LLM and return the raw response text."""
        ...


# ---------------------------------------------------------------------------
# Anthropic-based Generator client (concrete implementation)
# ---------------------------------------------------------------------------

class AnthropicGeneratorClient:
    """Concrete Generator LLM client wrapping the Anthropic SDK (§9.2.1, DR-16).

    Parameters
    ----------
    model : str
        Model identifier (DR-16: configurable per role).
    api_key : str, optional
        Anthropic API key. Defaults to ANTHROPIC_API_KEY env var.

    Supports
    --------
    DR-16 : Model selection is configurable.
    """

    def __init__(self, model: str, api_key: Optional[str] = None) -> None:
        self._model = model
        self._api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        import anthropic
        self._client = anthropic.Anthropic(api_key=self._api_key)

    @property
    def model(self) -> str:
        """The model identifier in use."""
        return self._model

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int = 4000,
    ) -> str:
        """Invoke the Anthropic messages API (§9.2.1).

        Returns
        -------
        str
            Raw response text from the LLM.
        """
        response = self._client.messages.create(
            model=self._model,
            max_tokens=max_output_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        text_parts = []
        for block in response.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)
        return "".join(text_parts)

    def invoke_with_usage(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int = 4000,
    ) -> dict:
        """Invoke the Anthropic messages API and return response with usage info.

        Returns
        -------
        dict
            Keys: 'text', 'input_tokens', 'output_tokens'.
        """
        response = self._client.messages.create(
            model=self._model,
            max_tokens=max_output_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        text_parts = []
        for block in response.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)
        usage = getattr(response, "usage", None)
        return {
            "text": "".join(text_parts),
            "input_tokens": getattr(usage, "input_tokens", 0) if usage else 0,
            "output_tokens": getattr(usage, "output_tokens", 0) if usage else 0,
        }


# ---------------------------------------------------------------------------
# Helper: build section lookup from plan
# ---------------------------------------------------------------------------



def _strip_code_fences(text: str) -> str:
    """Strip markdown code fences from LLM responses."""
    s = text.strip()
    fence = chr(96) * 3
    if s.startswith(fence):
        first_nl = s.find(chr(10))
        s = s[first_nl + 1:] if first_nl >= 0 else s[3:]
    if s.endswith(fence):
        s = s[:-3]
    return s.strip()

def _build_section_lookup(plan: ReportPlan) -> Dict[str, SectionNode]:
    """Build a section_id → SectionNode lookup from the report plan.

    Parameters
    ----------
    plan : ReportPlan
        Validated report plan.

    Returns
    -------
    dict
        Maps section_id → SectionNode.
    """
    return {section.section_id: section for section in plan.sections}


# ---------------------------------------------------------------------------
# Helper: initialize RunState with all sections QUEUED
# ---------------------------------------------------------------------------

def _initialize_run_state(
    plan: ReportPlan,
    gen_dag: DAG,
    fin_dag: DAG,
    run_id: str,
) -> RunState:
    """Initialize RunState with all sections in QUEUED state (§10.13, FR-08).

    Parameters
    ----------
    plan : ReportPlan
        Validated report plan.
    gen_dag : DAG
        Generation DAG (content edges only).
    fin_dag : DAG
        Finalization DAG (content + reference edges).
    run_id : str
        Unique run identifier.

    Returns
    -------
    RunState
        Initialized run state with all sections QUEUED.
    """
    now = datetime.now(timezone.utc).isoformat()
    section_states: Dict[str, SectionState] = {}
    for section in plan.sections:
        section_states[section.section_id] = SectionState(
            section_id=section.section_id,
            state=SectionLifecycleState.QUEUED,
            version=1,
            last_transition_timestamp=now,
            validation_history=[],
            claim_table=None,
            summary_abstract=None,
            retry_counters={},
            cascade_depth=0,
        )
    return RunState(
        run_id=run_id,
        report_plan_version=getattr(plan, "version", "1.0"),
        section_states=section_states,
        generation_dag_edges=gen_dag.edges,
        finalization_dag_edges=fin_dag.edges,
        started_at=now,
        last_checkpoint_at=now,
        cumulative_input_tokens=0,
        cumulative_output_tokens=0,
    )


# ---------------------------------------------------------------------------
# Helper: scaffold output directories
# ---------------------------------------------------------------------------

def _scaffold_output_dirs(
    output_dir: Path,
    section_ids: List[str],
) -> None:
    """Create output directory structure for each section (§16).

    Creates: output_dir/sections/{section_id}/ for each section.

    Parameters
    ----------
    output_dir : Path
        Root output directory.
    section_ids : list of str
        All section IDs from the report plan.
    """
    for section_id in section_ids:
        section_dir = output_dir / "sections" / section_id
        os.makedirs(section_dir, exist_ok=True)
    logger.info(
        "Scaffolded output directories for %d sections under %s",
        len(section_ids),
        output_dir,
    )


# ---------------------------------------------------------------------------
# Helper: emit state transition with event logging
# ---------------------------------------------------------------------------

def _transition_and_emit(
    section_state: SectionState,
    new_state: SectionLifecycleState,
    *,
    trigger_event: Optional[str] = None,
    attempt: Optional[int] = None,
    model: Optional[str] = None,
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> SectionState:
    """Transition a section state and emit a structured event (§11, NFR-06).

    Combines lifecycle.transition_section_state() with
    events.emit_state_transition() to ensure every transition is logged.

    Parameters
    ----------
    section_state : SectionState
        The section state to transition.
    new_state : SectionLifecycleState
        Target lifecycle state.
    trigger_event : str, optional
        Event that triggered the transition.
    attempt : int, optional
        Current attempt number.
    model : str, optional
        Model identifier used.
    input_tokens : int, optional
        Input tokens consumed.
    output_tokens : int, optional
        Output tokens consumed.
    extra_metadata : dict, optional
        Additional metadata for the event.

    Returns
    -------
    SectionState
        The updated section state.
    """
    from_state = section_state.state.value
    transition_section_state(section_state, new_state)
    emit_state_transition(
        section_id=section_state.section_id,
        from_state=from_state,
        to_state=new_state.value,
        trigger_event=trigger_event,
        attempt=attempt,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        extra_metadata=extra_metadata,
    )
    return section_state


# ---------------------------------------------------------------------------
# Helper: write section artifacts to disk
# ---------------------------------------------------------------------------

def _write_section_artifacts(
    output_dir: Path,
    section_id: str,
    version: int,
    draft_content: str,
    claim_table_dict: Optional[dict],
    validation_log: List[dict],
    provenance: dict,
) -> None:
    """Write section output artifacts to the section's output directory.

    Writes:
      - draft_v{version}.md
      - claim_table_v{version}.json
      - validation_log.json
      - provenance.json

    Parameters
    ----------
    output_dir : Path
        Root output directory.
    section_id : str
        Section identifier.
    version : int
        Draft version number.
    draft_content : str
        Markdown content of the section draft.
    claim_table_dict : dict or None
        Serialized claim table, or None if extraction failed.
    validation_log : list of dict
        Serialized validation results.
    provenance : dict
        Provenance record.
    """
    section_dir = output_dir / "sections" / section_id

    # Draft
    draft_path = section_dir / f"draft_v{version}.md"
    draft_path.write_text(draft_content, encoding="utf-8")

    # Claim table
    ct_path = section_dir / f"claim_table_v{version}.json"
    ct_data = claim_table_dict if claim_table_dict is not None else {"partial": True, "claims": []}
    ct_path.write_text(json.dumps(ct_data, indent=2, default=str), encoding="utf-8")

    # Validation log
    vlog_path = section_dir / "validation_log.json"
    vlog_path.write_text(json.dumps(validation_log, indent=2, default=str), encoding="utf-8")

    # Provenance
    prov_path = section_dir / "provenance.json"
    prov_path.write_text(json.dumps(provenance, indent=2, default=str), encoding="utf-8")

    logger.info(
        "Wrote artifacts for section '%s' v%d to %s",
        section_id, version, section_dir,
    )


# ---------------------------------------------------------------------------
# Core: process a single section through generation → validation → finalization
# ---------------------------------------------------------------------------

def _process_section(
    section: SectionNode,
    section_state: SectionState,
    section_states: Dict[str, SectionState],
    style: StyleSheet,
    gen_dag: DAG,
    fin_dag: DAG,
    retriever: Optional[RetrieverProtocol],
    generator_client: GeneratorLLMClient,
    llm_client: Any,
    token_tracker: TokenTracker,
    output_dir: Path,
    model_name: str,
    section_lookup: Dict[str, SectionNode],
) -> None:
    """Process a single section through the full pipeline (§6, §11).

    Steps:
      1. Check generation prerequisites (FR-08)
      2. Transition to GENERATING
      3. Retrieve evidence chunks (FR-09, FR-10)
      4. Assemble generation prompt (FR-11, FR-12, FR-13)
      5. Call Generator LLM
      6. Transition to DRAFTED
      7. Validate via coordinator (L1→L2→L3) with retry loop (FR-14–FR-19)
      8. On validation pass: extract claims, generate summary, write artifacts
      9. Transition to FINALIZED
      10. On retry exhaustion: escalate (FR-19)

    Parameters
    ----------
    section : SectionNode
        The section to process.
    section_state : SectionState
        Current state of this section.
    section_states : dict
        All section states (for prerequisite checks).
    style : StyleSheet
        Loaded style sheet.
    gen_dag : DAG
        Generation DAG.
    fin_dag : DAG
        Finalization DAG.
    retriever : RetrieverProtocol or None
        Stage 05 retriever (None if unavailable).
    generator_client : GeneratorLLMClient
        LLM client for content generation.
    llm_client : object
        LLM client for L3 validation, claim extraction, summary abstraction.
    token_tracker : TokenTracker
        Token accounting tracker.
    output_dir : Path
        Root output directory.
    model_name : str
        Model identifier for event metadata.
    section_lookup : dict
        Maps section_id → SectionNode.

    Supports
    --------
    FR-06 : Topological ordering (caller ensures order).
    FR-08 : Generation prerequisites checked.
    FR-09, FR-10 : Retrieval with answer text exclusion.
    FR-11, FR-12, FR-13 : Prompt assembly with context channels.
    FR-14, FR-16, FR-18 : Three-layer validation.
    FR-15, FR-17, FR-19 : Retry with feedback and escalation.
    FR-20, FR-21, FR-22 : Claim extraction and validation.
    NFR-01 : Latency tracking.
    NFR-02 : Token budget enforcement.
    NFR-06 : Structured event emission.
    """
    sid = section.section_id

    # --- Step 1: Check generation prerequisites (FR-08) ---
    if not check_generation_prerequisites(sid, section_states, gen_dag):
        logger.info(
            "Section '%s' prerequisites not met — skipping (stays QUEUED).",
            sid,
        )
        return

    # --- Step 2: Transition to GENERATING ---
    _transition_and_emit(
        section_state,
        SectionLifecycleState.GENERATING,
        trigger_event="prerequisites_met",
    )

    # --- Step 3: Retrieve evidence chunks (FR-09, FR-10) ---
    retrieved_chunks: List[RankedChunk] = []
    if retriever is not None:
        try:
            retrieval_result = retrieve_for_section(section, retriever)
            retrieved_chunks = retrieval_result.chunks
        except Exception as exc:
            logger.warning(
                "Retrieval failed for section '%s': %s. Proceeding with no chunks.",
                sid, exc,
            )
    else:
        logger.info(
            "No retriever available for section '%s'. Proceeding with no chunks.",
            sid,
        )

    # --- Gather upstream context for prompt assembly ---
    upstream_claim_tables = {}
    upstream_summary_abstracts = {}
    for pred_id in gen_dag.predecessors(sid):
        pred_state = section_states.get(pred_id)
        if pred_state is not None:
            if pred_state.claim_table is not None:
                upstream_claim_tables[pred_id] = pred_state.claim_table
            if pred_state.summary_abstract is not None:
                upstream_summary_abstracts[pred_id] = pred_state.summary_abstract

    # --- Step 4 & 5: Generate section content with retry loop ---
    retry_errors: Optional[List[str]] = None
    retry_layer: Optional[str] = None
    raw_json: Optional[str] = None
    validation_result: Optional[ValidationPipelineResult] = None
    all_validation_results: List[dict] = []

    # Reset retry counters for this processing pass
    section_state.retry_counters = {}

    # Track section latency (NFR-01)
    with token_tracker.track_section_latency(sid):
        # Outer retry loop: generate → validate → retry on failure
        max_total_attempts = 1 + LAYER1_RETRY_LIMIT + LAYER2_RETRY_LIMIT + LAYER3_RETRY_LIMIT
        attempt = 0
        escalated = False

        while attempt < max_total_attempts and not escalated:
            attempt += 1

            # --- Assemble generation prompt (FR-11, FR-12, FR-13) ---
            prompt = assemble_generation_prompt(
                section=section,
                style=style,
                retrieved_chunks=retrieved_chunks,
                upstream_claim_tables=upstream_claim_tables if upstream_claim_tables else None,
                upstream_summary_abstracts=upstream_summary_abstracts if upstream_summary_abstracts else None,
                retry_errors=retry_errors,
                retry_layer=retry_layer,
            )

            # --- Call Generator LLM (§9.2.1) ---
            call_start = time.monotonic()
            try:
                gen_response = generator_client.invoke_with_usage(
                    system_prompt=prompt.system_prompt,
                    user_message=prompt.user_message,
                    max_output_tokens=prompt.max_output_tokens,
                )
                raw_json = gen_response["text"]
                raw_json = _strip_code_fences(raw_json)
                gen_input_tokens = gen_response["input_tokens"]
                gen_output_tokens = gen_response["output_tokens"]
            except AttributeError:
                # Fallback for clients without invoke_with_usage
                raw_json = generator_client.invoke(
                    system_prompt=prompt.system_prompt,
                    user_message=prompt.user_message,
                    max_output_tokens=prompt.max_output_tokens,
                )
                raw_json = _strip_code_fences(raw_json)
                gen_input_tokens = 0
                gen_output_tokens = 0
            call_latency = time.monotonic() - call_start

            # Record token usage (NFR-02)
            token_tracker.record_call(
                role="generator",
                input_tokens=gen_input_tokens,
                output_tokens=gen_output_tokens,
                section_id=sid,
                model=model_name,
                latency_seconds=call_latency,
            )

            # Transition to DRAFTED on first generation
            if section_state.state == SectionLifecycleState.GENERATING:
                _transition_and_emit(
                    section_state,
                    SectionLifecycleState.DRAFTED,
                    trigger_event="generation_complete",
                    attempt=attempt,
                    model=model_name,
                    input_tokens=gen_input_tokens,
                    output_tokens=gen_output_tokens,
                )

            # --- Step 7: Validate via coordinator (L1→L2→L3) ---
            validation_result = run_validation_pipeline(
                raw_json=raw_json,
                section_id=sid,
                section_type=section.section_type,
                style=style,
                depth_level=section.depth_level,
                attempt=attempt,
                tone_register=style.tone_register,
                upstream_claim_tables=upstream_claim_tables if upstream_claim_tables else None,
                retrieved_chunks=retrieved_chunks if retrieved_chunks else None,
                llm_client=llm_client,
                skip_layer3=os.environ.get("SKIP_LAYER3", "").lower() in ("1", "true", "yes"),
            )

            # Record L3 validation token usage if applicable
            # (L3 uses LLM calls; we approximate since coordinator doesn't return usage)
            # Token tracking for L3 is handled by the llm_client if it's tracked externally

            # Store validation results for the log
            for vr in validation_result.results:
                all_validation_results.append(vr.model_dump() if hasattr(vr, "model_dump") else {"layer": str(vr.layer), "passed": vr.passed, "attempt": vr.attempt})

            section_state.validation_history.extend(validation_result.results)

            if validation_result.passed:
                logger.info(
                    "Section '%s' passed all validation layers on attempt %d.",
                    sid, attempt,
                )
                break

            # --- Validation failed: determine retry or escalation ---
            failed_layer = validation_result.failed_layer
            if failed_layer is None:
                # Should not happen if passed is False, but handle gracefully
                logger.error(
                    "Section '%s' validation failed but no failed_layer set. Escalating.",
                    sid,
                )
                escalated = True
                break

            layer_key = _LAYER_KEY_MAP.get(failed_layer, "unknown")
            layer_limit = _LAYER_RETRY_LIMITS.get(layer_key, 0)
            layer_display = _LAYER_DISPLAY_NAMES.get(layer_key, layer_key)

            # Increment retry counter for this layer
            current_retries = section_state.retry_counters.get(layer_key, 0)
            section_state.retry_counters[layer_key] = current_retries + 1

            logger.info(
                "Section '%s' failed %s (attempt %d, retry %d/%d).",
                sid, layer_display, attempt, current_retries + 1, layer_limit,
            )

            if current_retries + 1 > layer_limit:
                # Retry limit exceeded → escalate (FR-19)
                logger.warning(
                    "Section '%s' exceeded retry limit for %s (%d/%d). Escalating.",
                    sid, layer_display, current_retries + 1, layer_limit,
                )
                escalated = True
                break

            # Prepare retry feedback for next generation attempt (FR-15, FR-17)
            retry_errors = validation_result.error_messages
            retry_layer = layer_display

            # Transition back to GENERATING for retry
            _transition_and_emit(
                section_state,
                SectionLifecycleState.GENERATING,
                trigger_event=f"{layer_key}_retry",
                attempt=attempt,
                extra_metadata={
                    "failed_layer": layer_key,
                    "retry_count": current_retries + 1,
                    "error_count": len(validation_result.error_messages),
                },
            )

    # --- Handle escalation ---
    if escalated:
        _transition_and_emit(
            section_state,
            SectionLifecycleState.ESCALATED,
            trigger_event="retry_exhaustion",
            extra_metadata={
                "retry_counters": dict(section_state.retry_counters),
                "failed_layer": _LAYER_KEY_MAP.get(
                    validation_result.failed_layer, "unknown"
                ) if validation_result and validation_result.failed_layer else "unknown",
            },
        )
        emit_escalation_triggered(
            section_id=sid,
            reason=f"Retry limit exceeded for {_LAYER_DISPLAY_NAMES.get(_LAYER_KEY_MAP.get(validation_result.failed_layer, 'unknown'), 'unknown') if validation_result and validation_result.failed_layer else 'unknown'}",
            from_state="drafted",
        )

        # Write whatever artifacts we have even for escalated sections
        if raw_json is not None:
            _write_section_artifacts(
                output_dir=output_dir,
                section_id=sid,
                version=section_state.version,
                draft_content=raw_json,
                claim_table_dict=None,
                validation_log=all_validation_results,
                provenance={
                    "section_id": sid,
                    "state": "escalated",
                    "retry_counters": dict(section_state.retry_counters),
                },
            )
        return

    # --- Validation passed: post-processing (FR-20, FR-21, FR-22) ---
    if validation_result is None or not validation_result.passed:
        # Should not reach here, but guard
        return

    parsed_output = validation_result.parsed_output
    if parsed_output is None:
        logger.error("Section '%s' passed validation but parsed_output is None.", sid)
        return

    content_markdown = parsed_output.content_markdown

    # --- Step 7a: Extract claim table (FR-20, FR-22) ---
    claim_table = None
    try:
        claim_table = extract_claim_table(
            section_id=sid,
            content_markdown=content_markdown,
            retrieved_chunks=retrieved_chunks,
            llm_client=llm_client,
            version=section_state.version,
            retry_limit=CLAIM_EXTRACTION_RETRY_LIMIT,
        )
        # Record approximate token usage for claim extraction
        token_tracker.record_call(
            role="claim_extractor",
            input_tokens=0,  # Approximation — actual usage tracked by client
            output_tokens=0,
            section_id=sid,
            model=model_name,
        )
    except TokenBudgetExceededError:
        raise
    except Exception as exc:
        logger.warning(
            "Claim extraction failed for section '%s': %s. "
            "Marking claim table as partial (FR-22).",
            sid, exc,
        )

    # --- Step 7b: Validate claim table (FR-21) ---
    if claim_table is not None and not claim_table.partial:
        available_chunk_ids = {c.id for c in retrieved_chunks}
        chunk_texts = {c.id: c.text for c in retrieved_chunks}
        claim_validation = validate_claim_table(
            claim_table=claim_table,
            section_text=content_markdown,
            available_chunk_ids=available_chunk_ids,
            chunk_texts=chunk_texts,
        )
        if not claim_validation.passed:
            logger.warning(
                "Claim table validation failed for section '%s': %s",
                sid, claim_validation.failure_reasons,
            )
            # Mark as partial if validation fails
            claim_table.partial = True

    section_state.claim_table = claim_table

    # --- Step 7c: Generate summary abstract (FR-20) ---
    summary_abstract = None
    try:
        summary_abstract = generate_summary_abstract(
            section_id=sid,
            content_markdown=content_markdown,
            llm_client=llm_client,
        )
        # Record approximate token usage for summary abstraction
        token_tracker.record_call(
            role="summary_abstractifier",
            input_tokens=0,
            output_tokens=0,
            section_id=sid,
            model=model_name,
        )
    except TokenBudgetExceededError:
        raise
    except Exception as exc:
        logger.warning(
            "Summary abstraction failed for section '%s': %s",
            sid, exc,
        )

    section_state.summary_abstract = summary_abstract

    # --- Step 7d: Write artifacts ---
    claim_table_dict = claim_table.model_dump() if claim_table is not None else None
    provenance = {
        "section_id": sid,
        "version": section_state.version,
        "model": model_name,
        "state": "finalized",
        "retrieval_queries": [q for q in section.source_queries] if hasattr(section, "source_queries") else [],
        "chunk_count": len(retrieved_chunks),
        "validation_attempts": attempt,
        "retry_counters": dict(section_state.retry_counters),
        "claim_count": len(claim_table.claims) if claim_table else 0,
        "claim_partial": claim_table.partial if claim_table else True,
        "has_summary_abstract": summary_abstract is not None,
    }

    _write_section_artifacts(
        output_dir=output_dir,
        section_id=sid,
        version=section_state.version,
        draft_content=content_markdown,
        claim_table_dict=claim_table_dict,
        validation_log=all_validation_results,
        provenance=provenance,
    )

    # --- Step 7e: Transition to FINALIZED ---
    _transition_and_emit(
        section_state,
        SectionLifecycleState.FINALIZED,
        trigger_event="validation_passed",
        attempt=attempt,
        model=model_name,
        extra_metadata={
            "claim_count": len(claim_table.claims) if claim_table else 0,
            "claim_partial": claim_table.partial if claim_table else True,
            "has_summary": summary_abstract is not None,
        },
    )

    logger.info("Section '%s' finalized (v%d).", sid, section_state.version)


# ---------------------------------------------------------------------------
# Helper: compute and write run metrics (§17.2, NFR-07)
# ---------------------------------------------------------------------------

def _compute_and_write_metrics(
    run_state: RunState,
    output_dir: Path,
) -> Dict[str, float]:
    """Compute all §17.2 metrics and write run_metrics.json (NFR-07).

    Calls ``compute_all_metrics()`` from ``observability.metrics`` to
    compute the seven metrics from the final RunState, then calls
    ``write_run_metrics()`` to persist them.

    This function runs unconditionally in the completion phase — even if
    assembly was skipped (e.g., some sections escalated) — because metrics
    are computed from the RunState, not from the assembled report.

    Parameters
    ----------
    run_state : RunState
        The final run state after all section processing.
    output_dir : Path
        Root output directory for writing run_metrics.json.

    Returns
    -------
    dict
        Maps metric key → float value. All seven keys are present.

    Supports
    --------
    NFR-07 : Post-run metrics computation and persistence.
    §17.2 : All seven metric definitions.
    """
    logger.info("Computing run metrics (§17.2, NFR-07)...")

    # Collect section contents from disk for dependency completeness metric
    section_contents: Dict[str, str] = {}
    for section_id, ss in run_state.section_states.items():
        if ss.state in (
            SectionLifecycleState.FINALIZED,
            SectionLifecycleState.STABLE,
        ):
            # Try to read the latest draft from disk
            section_dir = output_dir / "sections" / section_id
            if section_dir.is_dir():
                import re as _re
                draft_pattern = _re.compile(r"^draft_v(\d+)\.md$")
                max_version = -1
                latest_path = None
                for entry in section_dir.iterdir():
                    match = draft_pattern.match(entry.name)
                    if match:
                        version = int(match.group(1))
                        if version > max_version:
                            max_version = version
                            latest_path = entry
                if latest_path is not None:
                    try:
                        section_contents[section_id] = latest_path.read_text(
                            encoding="utf-8"
                        )
                    except Exception as exc:
                        logger.warning(
                            "Could not read draft for section '%s': %s",
                            section_id, exc,
                        )

    metrics = compute_all_metrics(
        run_state=run_state,
        section_contents=section_contents if section_contents else None,
    )

    write_run_metrics(metrics, output_dir)

    logger.info(
        "Run metrics computed and written: %s",
        {k: f"{v:.4f}" for k, v in metrics.items()},
    )

    return metrics


# ---------------------------------------------------------------------------
# Helper: attempt report assembly (§9.2.5, FR-26, FR-27)
# ---------------------------------------------------------------------------

def _attempt_assembly(
    run_state: RunState,
    plan: ReportPlan,
    output_dir: Path,
) -> Optional[Path]:
    """Attempt to assemble the final report if all sections are ready (FR-26, FR-27).

    Checks assembly readiness via ``check_assembly_readiness()``. If ready,
    calls the assembler. If not ready (e.g., some sections still in DRAFTED
    or QUEUED state), logs a warning and returns None.

    Parameters
    ----------
    run_state : RunState
        The final run state.
    plan : ReportPlan
        The report plan for section ordering.
    output_dir : Path
        Root output directory.

    Returns
    -------
    Path or None
        Path to the assembled report, or None if assembly was skipped.

    Supports
    --------
    FR-26 : Heading hierarchy in assembled report.
    FR-27 : Assembly readiness pre-check.
    """
    from synthesizer.orchestrator.lifecycle import AssemblyNotReadyError

    try:
        check_assembly_readiness(run_state.section_states)
    except AssemblyNotReadyError as exc:
        logger.warning(
            "Assembly skipped: %s", exc,
        )
        return None

    try:
        from synthesizer.assembly.assembler import assemble_report
        report_path = assemble_report(
            report_plan=plan,
            output_dir=output_dir,
        )
        logger.info("Report assembled at %s", report_path)
        return report_path
    except Exception as exc:
        logger.error("Assembly failed: %s", exc, exc_info=True)
        return None


# ---------------------------------------------------------------------------
# Main entry point: run()
# ---------------------------------------------------------------------------

def run(
    report_plan_path: Path,
    style_sheet_path: Path,
    output_dir: Optional[Path] = None,
    model: Optional[str] = None,
    resume: bool = False,
    retriever: Optional[RetrieverProtocol] = None,
    generator_client: Optional[GeneratorLLMClient] = None,
    llm_client: Optional[Any] = None,
) -> RunState:
    """Execute the report synthesis pipeline (§6).

    Chains all components into a sequential pipeline:
      Phase 1 — Initialization: load plan, style, build DAGs, init state
      Phase 2 — Section processing: iterate topological order, generate,
                validate with retry, extract claims, finalize
      Phase 3 — Completion: compute metrics, assemble report, write checkpoint

    Parameters
    ----------
    report_plan_path : Path
        Path to the report plan JSON file (FR-01).
    style_sheet_path : Path
        Path to the style sheet JSON file (FR-04).
    output_dir : Path, optional
        Output directory. Defaults to SYNTHESIZER_OUTPUT_DIR from config.
    model : str, optional
        Model identifier. Overrides SYNTHESIZER_MODEL from config (DR-16).
    resume : bool, optional
        If True, attempt to resume from checkpoint. **Accepted but ignored
        in this sprint** — completion_3 implements checkpoint/resume.
    retriever : RetrieverProtocol, optional
        Stage 05 retriever instance. If None, retrieval is skipped.
    generator_client : GeneratorLLMClient, optional
        LLM client for content generation. If None, creates an
        AnthropicGeneratorClient with the configured model.
    llm_client : object, optional
        LLM client for L3 validation, claim extraction, and summary
        abstraction. If None, creates one via the validation llm_client
        factory.

    Returns
    -------
    RunState
        Final run state with all section states.

    Raises
    ------
    TokenBudgetExceededError
        If cumulative token usage exceeds TOKEN_BUDGET_CEILING (NFR-02).

    Supports
    --------
    FR-01 : Report plan loading.
    FR-04 : Style sheet loading.
    FR-06 : Topological generation ordering.
    FR-08 : Generation prerequisites.
    FR-09, FR-10 : Retrieval with answer text exclusion.
    FR-11–FR-13 : Prompt assembly.
    FR-14–FR-19 : Three-layer validation with retry and escalation.
    FR-20–FR-22 : Claim extraction and validation.
    FR-26 : Heading hierarchy in assembled report.
    FR-27 : Assembly readiness pre-check.
    NFR-01 : Per-section latency tracking.
    NFR-02 : Token budget enforcement.
    NFR-05 : Deterministic output structure.
    NFR-06 : Structured event emission.
    NFR-07 : Post-run metrics computation and persistence.
    DR-15, DR-16, DR-17, DR-18 : Open decisions preserved as configurable.
    """
    run_id = str(uuid.uuid4())
    resolved_output_dir = output_dir or SYNTHESIZER_OUTPUT_DIR
    resolved_model = model or SYNTHESIZER_MODEL
    start_time = time.monotonic()

    logger.info(
        "Starting synthesis run %s (model=%s, output=%s)",
        run_id, resolved_model, resolved_output_dir,
    )

    # ===================================================================
    # Phase 1 — Initialization
    # ===================================================================

    # 1a. Load report plan (FR-01, FR-02, FR-03)
    plan = load_report_plan(report_plan_path)
    logger.info(
        "Loaded report plan: %d sections, version=%s",
        len(plan.sections),
        getattr(plan, "version", "unknown"),
    )

    # 1b. Load style sheet (FR-04)
    style = load_style_sheet(style_sheet_path)
    logger.info("Loaded style sheet: tone=%s", style.tone_register)

    # 1c. Build DAGs (FR-06, FR-07)
    gen_dag = build_generation_dag(plan)
    fin_dag = build_finalization_dag(plan)

    # 1d. Get topological order (FR-06)
    topo_order = iter_topological(gen_dag)
    logger.info("Topological generation order: %s", topo_order)

    # 1e. Initialize RunState
    run_state = _initialize_run_state(plan, gen_dag, fin_dag, run_id)

    # 1f. Scaffold output directories
    section_ids = [s.section_id for s in plan.sections]
    _scaffold_output_dirs(resolved_output_dir, section_ids)

    # Build section lookup
    section_lookup = _build_section_lookup(plan)

    # Initialize token tracker (NFR-02)
    token_tracker = TokenTracker(ceiling=TOKEN_BUDGET_CEILING)

    # Emit run_started event (NFR-06)
    emit_run_started(
        run_id=run_id,
        report_plan_version=getattr(plan, "version", "1.0"),
        section_count=len(plan.sections),
    )

    # --- Create LLM clients if not injected ---
    if generator_client is None:
        try:
            generator_client = AnthropicGeneratorClient(
                model=resolved_model,
            )
        except Exception as exc:
            logger.error("Failed to create generator client: %s", exc)
            emit_run_failed(run_id=run_id, error=str(exc))
            raise

    if llm_client is None:
        try:
            from synthesizer.validation.llm_client import create_validation_llm_client
            llm_client = create_validation_llm_client(
                model=resolved_model,
                validate=True,
            )
        except Exception as exc:
            logger.warning(
                "Failed to create validation LLM client: %s. "
                "L3 validation and claim extraction will be skipped.",
                exc,
            )
            llm_client = None

    # ===================================================================
    # Phase 2 — Section Processing Loop
    # ===================================================================

    try:
        for section_id in topo_order:
            section = section_lookup.get(section_id)
            if section is None:
                logger.warning("Section '%s' in topo order but not in plan. Skipping.", section_id)
                continue

            section_state = run_state.section_states.get(section_id)
            if section_state is None:
                logger.warning("Section '%s' has no state entry. Skipping.", section_id)
                continue

            # Only process sections that are QUEUED
            if section_state.state != SectionLifecycleState.QUEUED:
                logger.info(
                    "Section '%s' is in state '%s', not QUEUED. Skipping.",
                    section_id, section_state.state.value,
                )
                continue

            _process_section(
                section=section,
                section_state=section_state,
                section_states=run_state.section_states,
                style=style,
                gen_dag=gen_dag,
                fin_dag=fin_dag,
                retriever=retriever,
                generator_client=generator_client,
                llm_client=llm_client,
                token_tracker=token_tracker,
                output_dir=resolved_output_dir,
                model_name=resolved_model,
                section_lookup=section_lookup,
            )

    except TokenBudgetExceededError as exc:
        logger.error("Token budget exceeded: %s", exc)
        emit_run_failed(run_id=run_id, error=str(exc))
        # Update run state with token counts before re-raising
        run_state.cumulative_input_tokens = token_tracker.cumulative_input_tokens
        run_state.cumulative_output_tokens = token_tracker.cumulative_output_tokens
        run_state.last_checkpoint_at = datetime.now(timezone.utc).isoformat()
        _write_run_state(resolved_output_dir, run_state)
        # Still compute metrics even on budget exceeded (NFR-07)
        _compute_and_write_metrics(run_state, resolved_output_dir)
        raise

    except Exception as exc:
        logger.error("Run failed with unexpected error: %s", exc, exc_info=True)
        emit_run_failed(run_id=run_id, error=str(exc))
        run_state.cumulative_input_tokens = token_tracker.cumulative_input_tokens
        run_state.cumulative_output_tokens = token_tracker.cumulative_output_tokens
        run_state.last_checkpoint_at = datetime.now(timezone.utc).isoformat()
        _write_run_state(resolved_output_dir, run_state)
        # Still compute metrics even on failure (NFR-07)
        try:
            _compute_and_write_metrics(run_state, resolved_output_dir)
        except Exception as metrics_exc:
            logger.warning("Metrics computation failed during error handling: %s", metrics_exc)
        raise

    # ===================================================================
    # Phase 3 — Completion: metrics, assembly, and checkpoint
    # ===================================================================

    wall_clock = time.monotonic() - start_time
    run_state.cumulative_input_tokens = token_tracker.cumulative_input_tokens
    run_state.cumulative_output_tokens = token_tracker.cumulative_output_tokens
    run_state.last_checkpoint_at = datetime.now(timezone.utc).isoformat()

    # 3a. Compute and write run metrics (§17.2, NFR-07)
    # This runs unconditionally — metrics are computed from RunState,
    # not from the assembled report.
    _compute_and_write_metrics(run_state, resolved_output_dir)

    # 3b. Attempt report assembly (FR-26, FR-27)
    _attempt_assembly(run_state, plan, resolved_output_dir)

    # 3c. Write run_state.json
    _write_run_state(resolved_output_dir, run_state)

    # Count outcomes
    finalized_count = sum(
        1 for ss in run_state.section_states.values()
        if ss.state == SectionLifecycleState.FINALIZED
    )
    escalated_count = sum(
        1 for ss in run_state.section_states.values()
        if ss.state == SectionLifecycleState.ESCALATED
    )

    emit_run_completed(
        run_id=run_id,
        sections_finalized=finalized_count,
        sections_escalated=escalated_count,
        total_input_tokens=token_tracker.cumulative_input_tokens,
        total_output_tokens=token_tracker.cumulative_output_tokens,
        wall_clock_seconds=wall_clock,
    )

    logger.info(
        "Run %s completed: %d finalized, %d escalated, %.1fs wall clock, "
        "%d total tokens.",
        run_id,
        finalized_count,
        escalated_count,
        wall_clock,
        token_tracker.cumulative_total_tokens,
    )

    return run_state


def _write_run_state(output_dir: Path, run_state: RunState) -> None:
    """Write RunState to run_state.json in the output directory.

    Parameters
    ----------
    output_dir : Path
        Root output directory.
    run_state : RunState
        Current run state to serialize.
    """
    path = output_dir / "run_state.json"
    os.makedirs(output_dir, exist_ok=True)
    path.write_text(
        run_state.model_dump_json(indent=2),
        encoding="utf-8",
    )
    logger.info("Wrote run state to %s", path)