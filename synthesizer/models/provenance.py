# synthesizer/models/provenance.py
"""Provenance record Pydantic model (§10.11).

Audit trail for a finalized section. Written once on finalization.
See Appendix D of the governing specification for an example.

Supports: FR-26.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.validation_models import ValidationResult


class ProvenanceRecord(BaseModel):
    """Audit trail for a finalized section (§10.11).

    Written once on finalization. Contains full generation and
    validation history for traceability.

    Supports: FR-26.
    """

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(
        ...,
        description="Section identifier.",
    )
    finalized_at: str = Field(
        ...,
        description="ISO 8601 timestamp of finalization.",
    )
    generation_model: str = Field(
        ...,
        description="Model identifier used for generation.",
    )
    generation_attempts: int = Field(
        ...,
        ge=1,
        description="Total generation attempts.",
    )
    validation_history: List[ValidationResult] = Field(
        ...,
        description="All validation results across all attempts.",
    )
    claim_table_version: Optional[int] = Field(
        default=None,
        description="Version of the extracted claim table.",
    )
    claim_table_partial: bool = Field(
        default=False,
        description="Whether claim table is partial.",
    )
    source_chunk_ids: List[str] = Field(
        ...,
        description="All chunk IDs used as evidence.",
    )
    upstream_dependencies_consumed: Dict[str, List[str]] = Field(
        ...,
        description="Maps DependencyKind → list of section_ids.",
    )
    cascade_triggers_received: int = Field(
        default=0,
        ge=0,
        description="Number of cascade invalidations received.",
    )
    word_count: int = Field(
        ...,
        ge=1,
        description="Final word count.",
    )
    heading_level: int = Field(
        ...,
        ge=1,
        le=6,
        description="Final heading level.",
    )


def write_provenance_record(
    record: ProvenanceRecord,
    output_dir: Path,
) -> Path:
    """Write a ProvenanceRecord to disk as JSON (§15.1).

    Writes to ``{output_dir}/sections/{section_id}/provenance.json``.

    Parameters
    ----------
    record : ProvenanceRecord
        The provenance record to persist.
    output_dir : Path
        Root synthesizer output directory (SYNTHESIZER_OUTPUT_DIR).

    Returns
    -------
    Path
        Path to the written provenance.json file.
    """
    section_dir = output_dir / "sections" / record.section_id
    section_dir.mkdir(parents=True, exist_ok=True)
    provenance_path = section_dir / "provenance.json"
    provenance_path.write_text(
        record.model_dump_json(indent=2),
        encoding="utf-8",
    )
    return provenance_path