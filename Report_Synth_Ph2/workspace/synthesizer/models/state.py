# synthesizer/models/state.py
"""Section and run state Pydantic models (§10.12, §10.13).

Supports: FR-08, FR-19, FR-23, FR-24, FR-27, NFR-03.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.claims import ClaimTable
from synthesizer.models.enums import SectionLifecycleState
from synthesizer.models.report_plan import DependencyEdge
from synthesizer.models.validation_models import ValidationResult


def _now_iso() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


class SectionState(BaseModel):
    """Per-section lifecycle state tracked by the orchestrator (§10.12).

    See §11 for state transitions.
    Supports: FR-08, FR-19, FR-23, FR-27.
    """

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(
        ...,
        description="Unique section identifier.",
    )
    state: SectionLifecycleState = Field(
        ...,
        description="Current lifecycle state.",
    )
    version: int = Field(
        default=1,
        ge=1,
        description="Draft version counter. Increments on each re-generation.",
    )
    last_transition_timestamp: str = Field(
        default_factory=_now_iso,
        description="ISO 8601 timestamp of last state change.",
    )
    validation_history: List[ValidationResult] = Field(
        default_factory=list,
        description="Cumulative validation results.",
    )
    claim_table: Optional[ClaimTable] = Field(
        default=None,
        description="Current claim table (None until extraction).",
    )
    summary_abstract: Optional[str] = Field(
        default=None,
        description="2-3 sentence summary (None until abstraction).",
    )
    retry_counters: Dict[str, int] = Field(
        default_factory=dict,
        description="Maps layer name → current retry count.",
    )
    cascade_depth: int = Field(
        default=0,
        ge=0,
        description="Current cascade depth for this section.",
    )


class RunState(BaseModel):
    """Checkpoint object for the full orchestrator run (§10.13).

    Persisted to disk after every checkpoint-worthy state transition (§11).
    Supports: NFR-03, FR-24.
    """

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(
        ...,
        description="Unique run identifier (UUID).",
    )
    report_plan_version: str = Field(
        ...,
        description="Version of the report plan being executed.",
    )
    section_states: Dict[str, SectionState] = Field(
        ...,
        description="Maps section_id → SectionState.",
    )
    generation_dag_edges: List[DependencyEdge] = Field(
        ...,
        description="Content-dependency edges for generation ordering.",
    )
    finalization_dag_edges: List[DependencyEdge] = Field(
        ...,
        description="Content + reference edges for finalization ordering.",
    )
    started_at: str = Field(
        ...,
        description="ISO 8601 timestamp.",
    )
    last_checkpoint_at: str = Field(
        ...,
        description="ISO 8601 timestamp of last checkpoint write.",
    )
    cumulative_input_tokens: int = Field(
        default=0,
        ge=0,
        description="Total input tokens consumed across all LLM calls.",
    )
    cumulative_output_tokens: int = Field(
        default=0,
        ge=0,
        description="Total output tokens consumed across all LLM calls.",
    )