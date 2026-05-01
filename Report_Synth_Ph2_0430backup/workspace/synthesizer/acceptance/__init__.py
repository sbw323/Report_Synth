# synthesizer/acceptance/__init__.py
"""Acceptance test suite for the Report Synthesizer Agent (§19).

This package contains the five priority acceptance tests defined in §19
of the governing specification (report_synthesizer_v4.md):

  - FR-08: Content dependency ordering enforcement
  - FR-18: Semantic validation (L3 sub-check B) contradiction detection
  - FR-23: Cascade invalidation propagation
  - FR-26: Assembly heading level correctness
  - FR-27: Assembly readiness blocking on non-finalized sections

Each test module is self-contained and uses shared fixtures defined in
this __init__.py for common setup (e.g., creating minimal report plans,
style sheets, and section states).

Governing spec section: §19
Functional requirements: FR-08, FR-18, FR-23, FR-26, FR-27
Non-functional requirements: NFR-08 (acceptance test coverage)
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from synthesizer.models.claims import ClaimEntry, ClaimTable, TextSpan
from synthesizer.models.enums import (
    ConfidenceTag,
    DependencyKind,
    SectionLifecycleState,
    SectionType,
    ValidationLayer,
)
from synthesizer.models.report_plan import DependencyEdge, ReportPlan, SectionNode
from synthesizer.models.state import RunState, SectionState
from synthesizer.models.style_sheet import LevelConstraint, StyleSheet
from synthesizer.models.validation_models import ValidationResult


def make_section_node(
    section_id: str,
    title: str = "Test Section",
    section_type: SectionType = SectionType.NARRATIVE_SYNTHESIS,
    depth_level: int = 1,
    source_queries: Optional[List[str]] = None,
) -> SectionNode:
    """Create a minimal SectionNode for acceptance testing (§19).

    Parameters
    ----------
    section_id : str
        Unique section identifier.
    title : str
        Section title.
    section_type : SectionType
        Type of section.
    depth_level : int
        Depth level in the report hierarchy.
    source_queries : list of str, optional
        Retrieval queries for this section.

    Returns
    -------
    SectionNode
        A minimal section node suitable for testing.

    Supports
    --------
    §19 : Shared test fixture for acceptance tests.
    """
    return SectionNode(
        section_id=section_id,
        title=title,
        section_type=section_type,
        depth_level=depth_level,
        source_queries=source_queries or [],
        dependencies=[],
    )


def make_section_state(
    section_id: str,
    state: SectionLifecycleState = SectionLifecycleState.QUEUED,
    version: int = 1,
    claim_table: Optional[ClaimTable] = None,
    summary_abstract: Optional[str] = None,
    validation_history: Optional[List[ValidationResult]] = None,
) -> SectionState:
    """Create a minimal SectionState for acceptance testing (§19).

    Parameters
    ----------
    section_id : str
        Unique section identifier.
    state : SectionLifecycleState
        Current lifecycle state.
    version : int
        Draft version counter.
    claim_table : ClaimTable, optional
        Claim table for this section.
    summary_abstract : str, optional
        Summary abstract text.
    validation_history : list of ValidationResult, optional
        Validation history entries.

    Returns
    -------
    SectionState
        A minimal section state suitable for testing.

    Supports
    --------
    §19 : Shared test fixture for acceptance tests.
    """
    return SectionState(
        section_id=section_id,
        state=state,
        version=version,
        last_transition_timestamp=datetime.now(timezone.utc).isoformat(),
        validation_history=validation_history or [],
        claim_table=claim_table,
        summary_abstract=summary_abstract,
        retry_counters={},
        cascade_depth=0,
    )


def make_style_sheet(
    tone_register: str = "formal_academic",
) -> StyleSheet:
    """Create a minimal StyleSheet for acceptance testing (§19).

    Parameters
    ----------
    tone_register : str
        Tone register for the style sheet.

    Returns
    -------
    StyleSheet
        A minimal style sheet suitable for testing.

    Supports
    --------
    §19 : Shared test fixture for acceptance tests.
    FR-04 : Style sheet structure.
    """
    return StyleSheet(
        tone_register=tone_register,
        citation_style="author_year",
        level_constraints=[
            LevelConstraint(
                depth=1,
                heading_style="Title Case",
                word_count_min=50,
                word_count_max=5000,
            ),
            LevelConstraint(
                depth=2,
                heading_style="Title Case",
                word_count_min=30,
                word_count_max=3000,
            ),
        ],
    )


def make_claim_table(
    section_id: str,
    claims: Optional[List[ClaimEntry]] = None,
    partial: bool = False,
) -> ClaimTable:
    """Create a ClaimTable for acceptance testing (§19).

    Parameters
    ----------
    section_id : str
        Section this claim table belongs to.
    claims : list of ClaimEntry, optional
        Claim entries. Defaults to a single sample claim.
    partial : bool
        Whether the claim table is partial.

    Returns
    -------
    ClaimTable
        A claim table suitable for testing.

    Supports
    --------
    §19 : Shared test fixture for acceptance tests.
    FR-20 : Claim table structure.
    """
    if claims is None:
        claims = [
            ClaimEntry(
                claim_id=f"{section_id}_C1",
                claim_text="Sample claim for testing purposes.",
                confidence_tag=ConfidenceTag.HIGH,
                source_spans=[
                    TextSpan(document_id="doc1", start=0, end=50, text="sample"),
                ],
                source_chunk_ids=["chunk_1"],
            ),
        ]
    return ClaimTable(
        section_id=section_id,
        claims=claims,
        partial=partial,
    )


def make_dependency_edge(
    source_section_id: str,
    target_section_id: str,
    kind: DependencyKind = DependencyKind.CONTENT,
) -> DependencyEdge:
    """Create a DependencyEdge for acceptance testing (§19).

    Parameters
    ----------
    source_section_id : str
        The dependent section (downstream).
    target_section_id : str
        The dependency target (upstream).
    kind : DependencyKind
        Type of dependency.

    Returns
    -------
    DependencyEdge
        A dependency edge suitable for testing.

    Supports
    --------
    §19 : Shared test fixture for acceptance tests.
    """
    return DependencyEdge(
        source_section_id=source_section_id,
        target_section_id=target_section_id,
        kind=kind,
    )


__all__ = [
    "make_section_node",
    "make_section_state",
    "make_style_sheet",
    "make_claim_table",
    "make_dependency_edge",
]