# synthesizer/models/report_plan.py
"""Report plan Pydantic models (§10.2, §10.3, §10.4).

Supports: FR-01, FR-02, FR-03, FR-06, FR-08, FR-09, FR-26.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from synthesizer.models.enums import DependencyKind, SectionType


class DependencyEdge(BaseModel):
    """Typed relationship between two sections (§10.4).

    See §8 for enforcement rules per DependencyKind.
    Supports: FR-02, FR-03, FR-06, FR-07, FR-08, FR-23, FR-25.

    Uses extra='forbid' to reject unknown fields per sprint guardrails.
    Only canonical field names (source_section_id, target_section_id, kind)
    are accepted.
    """

    model_config = ConfigDict(extra="forbid")

    source_section_id: str = Field(
        ...,
        description="The section that depends (the downstream consumer).",
    )
    target_section_id: str = Field(
        ...,
        description="The section depended upon (the upstream provider).",
    )
    kind: DependencyKind = Field(
        ...,
        description="Type of dependency relationship.",
    )


class SectionNode(BaseModel):
    """One section in the report plan (§10.3).

    Defines structure, type, and dependencies.
    Supports: FR-01, FR-02, FR-06, FR-08, FR-09.
    """

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(
        ...,
        pattern=r"^[a-z0-9_]+$",
        max_length=64,
        description="Unique within plan. Pattern: [a-z0-9_]+, max 64 chars.",
    )
    title: str = Field(
        ...,
        min_length=1,
        description="Human-readable section title.",
    )
    parent_id: Optional[str] = Field(
        default=None,
        description="section_id of parent for hierarchy. None = top-level.",
    )
    section_type: SectionType = Field(
        ...,
        description="Determines prompt contract and output schema.",
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Prose guidance for generation (2-5 sentences).",
    )
    source_queries: List[str] = Field(
        ...,
        min_length=1,
        description="Queries for Stage 05 retrieval. At least one required.",
    )
    dependency_edges: List[DependencyEdge] = Field(
        default_factory=list,
        description="Dependencies on other sections.",
    )
    depth_level: int = Field(
        ...,
        ge=0,
        description=(
            "Nesting depth (0 = top-level). "
            "Must equal len(ancestor chain)."
        ),
    )


class ReportPlan(BaseModel):
    """Top-level container for the report structure (§10.2).

    Tier 1 source of truth (§7).
    Supports: FR-01, FR-02, FR-03, FR-06, FR-26.
    """

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(
        ...,
        min_length=1,
        description="Unique identifier for this plan.",
    )
    title: str = Field(
        ...,
        min_length=1,
        description="Report title.",
    )
    version: str = Field(
        ...,
        min_length=1,
        description="Plan version string (semver recommended).",
    )
    sections: List[SectionNode] = Field(
        ...,
        min_length=1,
        description="Ordered list of top-level and nested sections.",
    )
    global_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary metadata (e.g., target audience, domain).",
    )