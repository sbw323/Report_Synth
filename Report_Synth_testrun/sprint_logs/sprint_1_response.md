I'll implement Sprint 1 systematically, following the governing specification and sprint instructions precisely.

### `synthesizer/__init__.py`
```python
# synthesizer/__init__.py
"""Report Synthesizer Agent — top-level package."""
```

### `synthesizer/models/__init__.py`
```python
# synthesizer/models/__init__.py
"""Pydantic models and enumerations for the Report Synthesizer (§10)."""

from synthesizer.models.enums import (
    ConfidenceTag,
    DependencyKind,
    SectionLifecycleState,
    SectionType,
    ValidationLayer,
    ViolationSeverity,
)
from synthesizer.models.report_plan import (
    DependencyEdge,
    ReportPlan,
    SectionNode,
)
from synthesizer.models.style_sheet import (
    EquationDelimiters,
    LevelConstraint,
    StyleSheet,
)

__all__ = [
    "ConfidenceTag",
    "DependencyKind",
    "DependencyEdge",
    "EquationDelimiters",
    "LevelConstraint",
    "ReportPlan",
    "SectionLifecycleState",
    "SectionNode",
    "SectionType",
    "StyleSheet",
    "ValidationLayer",
    "ViolationSeverity",
]
```

### `synthesizer/models/enums.py`
```python
# synthesizer/models/enums.py
"""Enumerations for the Report Synthesizer (§10.1).

All six enums are defined exactly per the governing specification §10.1.
"""

from enum import Enum


class DependencyKind(str, Enum):
    """Type of dependency between sections. See §8 for enforcement rules.

    - CONTENT: Hard — blocks generation (DR-07)
    - REFERENCE: Medium — blocks finalization (DR-08)
    - THEMATIC: Soft — coherence check only (DR-09)
    - SOURCE: Informational — consistency check only (DR-10)
    """

    CONTENT = "content"
    REFERENCE = "reference"
    THEMATIC = "thematic"
    SOURCE = "source"


class SectionType(str, Enum):
    """Classification of section generation behavior. See §9 for prompt contracts."""

    NARRATIVE_SYNTHESIS = "narrative_synthesis"
    EVIDENCE_TABLE = "evidence_table"
    CROSS_REFERENCE = "cross_reference"
    METHODOLOGY_DESCRIPTION = "methodology_description"


class SectionLifecycleState(str, Enum):
    """Lifecycle state of a section. See §11 for transition table."""

    QUEUED = "queued"
    GENERATING = "generating"
    DRAFTED = "drafted"
    DRAFTED_PENDING_VALIDATION = "drafted_pending_validation"
    VALIDATED = "validated"
    FINALIZED = "finalized"
    STABLE = "stable"
    INVALIDATED = "invalidated"
    ESCALATED = "escalated"


class ValidationLayer(str, Enum):
    """Validation layer identifier. See §12 for semantics."""

    STRUCTURAL = "structural"       # Layer 1
    RULE_BASED = "rule_based"       # Layer 2
    SEMANTIC = "semantic"           # Layer 3
    CLAIM_TABLE = "claim_table"     # Post-finalization


class ConfidenceTag(str, Enum):
    """Confidence classification for extracted claims."""

    DIRECTLY_STATED = "directly_stated"
    INFERRED = "inferred"
    SYNTHESIZED = "synthesized"


class ViolationSeverity(str, Enum):
    """Severity of a validation violation."""

    ERROR = "error"
    WARNING = "warning"
```

### `synthesizer/models/report_plan.py`
```python
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
```

### `synthesizer/models/style_sheet.py`
```python
# synthesizer/models/style_sheet.py
"""Style sheet Pydantic models (§10.5).

Supports: FR-04, FR-05, FR-16.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from synthesizer.models.enums import SectionType


class EquationDelimiters(BaseModel):
    """LaTeX equation delimiter configuration (§10.5)."""

    model_config = ConfigDict(extra="forbid")

    inline: str = Field(
        default="$",
        description="Inline equation delimiter.",
    )
    display: str = Field(
        default="$$",
        description="Display equation delimiter.",
    )


class LevelConstraint(BaseModel):
    """Per-depth-level formatting constraints (§10.5)."""

    model_config = ConfigDict(extra="forbid")

    min_words: int = Field(
        ...,
        ge=0,
        description="Minimum word count. Constraint: ≥0.",
    )
    max_words: int = Field(
        ...,
        gt=0,
        description="Maximum word count. Constraint: > min_words.",
    )
    heading_format: str = Field(
        ...,
        min_length=1,
        description='Markdown heading format (e.g., "##", "###").',
    )

    @model_validator(mode="after")
    def check_max_greater_than_min(self) -> LevelConstraint:
        """Enforce max_words > min_words as required by §10.5."""
        if self.max_words <= self.min_words:
            raise ValueError(
                f"max_words ({self.max_words}) must be greater than "
                f"min_words ({self.min_words})"
            )
        return self


class StyleSheet(BaseModel):
    """Formatting and tone rules applied during generation and validation (§10.5).

    Tier 2 source of truth (§7).
    Supports: FR-04, FR-05, FR-16.
    """

    model_config = ConfigDict(extra="forbid")

    citation_pattern: str = Field(
        ...,
        description=(
            "Regex pattern for valid citations "
            '(e.g., r"\\([A-Z][a-z]+ et al\\., \\d{4}\\)").'
        ),
    )
    tone_register: str = Field(
        ...,
        min_length=1,
        description='Tone descriptor (e.g., "formal_academic", "technical_review").',
    )
    per_level_constraints: Dict[int, LevelConstraint] = Field(
        ...,
        description="Maps depth_level → constraints.",
    )
    per_type_overrides: Dict[SectionType, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Type-specific rule overrides.",
    )
    forbidden_phrases: List[str] = Field(
        default_factory=list,
        description="Phrases that must not appear in generated text.",
    )
    equation_delimiters: EquationDelimiters = Field(
        default_factory=EquationDelimiters,
        description="LaTeX delimiter config.",
    )

    @field_validator("citation_pattern")
    @classmethod
    def validate_citation_pattern_is_compilable(cls, v: str) -> str:
        """FR-04: Validate that citation_pattern is a compilable regex."""
        try:
            re.compile(v)
        except re.error as exc:
            raise ValueError(
                f"citation_pattern is not a valid regex: {exc}"
            ) from exc
        return v
```

### `synthesizer/config.py`
```python
# synthesizer/config.py
"""Synthesizer configuration surface (§16).

Adds synthesizer-specific keys per §16 table. Does not modify existing
pipeline keys. Reads from environment variables where set; falls back
to documented defaults.

Open decisions preserved as configurable:
  - DR-16: SYNTHESIZER_MODEL defaults to PIPELINE_MODEL (open — may differ per role)
  - DR-17: TOKEN_BUDGET_CEILING defaults to None (open — no limit)
  - DR-18: Per-role input token budgets remain open (not defined here)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Import pipeline-level constants from existing config, with safe fallbacks.
# The synthesizer wraps (never refactors) the existing pipeline (§14.2).
# ---------------------------------------------------------------------------
try:
    from config import DATA_DIR as _PIPELINE_DATA_DIR  # type: ignore[import-untyped]
except ImportError:
    _PIPELINE_DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))

try:
    from config import PIPELINE_MODEL as _PIPELINE_MODEL  # type: ignore[import-untyped]
except ImportError:
    _PIPELINE_MODEL = os.environ.get("PIPELINE_MODEL", "claude-sonnet-4-20250514")


# ---------------------------------------------------------------------------
# §16  Synthesizer configuration keys
# ---------------------------------------------------------------------------

# Required — no default; None signals "not yet configured".
REPORT_PLAN_PATH: Optional[Path] = (
    Path(os.environ["REPORT_PLAN_PATH"])
    if "REPORT_PLAN_PATH" in os.environ
    else None
)

STYLE_SHEET_PATH: Optional[Path] = (
    Path(os.environ["STYLE_SHEET_PATH"])
    if "STYLE_SHEET_PATH" in os.environ
    else None
)

# Optional — documented defaults from §16.
SYNTHESIZER_OUTPUT_DIR: Path = Path(
    os.environ.get(
        "SYNTHESIZER_OUTPUT_DIR",
        str(_PIPELINE_DATA_DIR / "synthesis"),
    )
)

CASCADE_DEPTH_LIMIT: int = int(
    os.environ.get("CASCADE_DEPTH_LIMIT", "3")
)

LAYER1_RETRY_LIMIT: int = int(
    os.environ.get("LAYER1_RETRY_LIMIT", "3")
)

LAYER2_RETRY_LIMIT: int = int(
    os.environ.get("LAYER2_RETRY_LIMIT", "3")
)

LAYER3_RETRY_LIMIT: int = int(
    os.environ.get("LAYER3_RETRY_LIMIT", "2")
)

CLAIM_EXTRACTION_RETRY_LIMIT: int = int(
    os.environ.get("CLAIM_EXTRACTION_RETRY_LIMIT", "1")
)

# DR-16 (open): Model selection per role. Currently a single configurable
# key. May be split per-role in a future sprint after benchmarking.
SYNTHESIZER_MODEL: str = os.environ.get(
    "SYNTHESIZER_MODEL", _PIPELINE_MODEL
)

# DR-17 (open): Token budget ceiling per run. None = no limit.
TOKEN_BUDGET_CEILING: Optional[int] = (
    int(os.environ["TOKEN_BUDGET_CEILING"])
    if "TOKEN_BUDGET_CEILING" in os.environ
    else None
)
```

### `synthesizer/loaders/__init__.py`
```python
# synthesizer/loaders/__init__.py
"""Loader modules for report plans and style sheets."""

from synthesizer.loaders.plan_loader import load_report_plan
from synthesizer.loaders.style_loader import load_style_sheet

__all__ = ["load_report_plan", "load_style_sheet"]
```

### `synthesizer/loaders/plan_loader.py`
```python
# synthesizer/loaders/plan_loader.py
"""Report plan loader (§7, §10.2–10.4).

Loads a JSON report plan from disk, parses it into a validated ReportPlan
object, and runs cross-section validations (FR-01, FR-02, FR-03).

Source-of-truth hierarchy (§7):
  Tier 1 — Report Plan (highest authority)
  Tier 2 — Style Sheet
  Tier 3 — Directory Tree (derived, never canonical)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from synthesizer.config import REPORT_PLAN_PATH
from synthesizer.models.report_plan import ReportPlan
from synthesizer.validation.graph_validation import (
    validate_dependency_references,
    validate_depth_levels,
    validate_no_content_cycles,
)


class ReportPlanLoadError(Exception):
    """Raised when report plan loading or validation fails.

    Wraps Pydantic ValidationError, JSON decode errors, and
    graph-validation errors with descriptive context.
    """


def load_report_plan(path: Optional[Path] = None) -> ReportPlan:
    """Load and fully validate a report plan from a JSON file.

    Performs, in order:
      1. File read and JSON parse
      2. Pydantic schema validation (FR-01)
      3. Dependency-reference validation — all section_ids in
         dependency_edges must exist (FR-02)
      4. Content-cycle detection — no cycles among CONTENT edges (FR-03)
      5. Depth-level consistency — each section's depth_level must match
         its ancestor-chain length

    Parameters
    ----------
    path : Path, optional
        Explicit path to the report plan JSON. If *None*, falls back to
        ``REPORT_PLAN_PATH`` from the synthesizer config (§16).

    Returns
    -------
    ReportPlan
        Fully validated report plan.

    Raises
    ------
    ReportPlanLoadError
        On any validation or I/O failure, with a descriptive message.
    """
    resolved_path = path or REPORT_PLAN_PATH
    if resolved_path is None:
        raise ReportPlanLoadError(
            "No report plan path provided and REPORT_PLAN_PATH is not "
            "configured. Set the REPORT_PLAN_PATH environment variable "
            "or pass an explicit path."
        )

    resolved_path = Path(resolved_path)

    # 1. File read + JSON parse
    try:
        raw_text = resolved_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ReportPlanLoadError(
            f"Report plan file not found: {resolved_path}"
        ) from exc
    except OSError as exc:
        raise ReportPlanLoadError(
            f"Failed to read report plan file {resolved_path}: {exc}"
        ) from exc

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ReportPlanLoadError(
            f"Report plan is not valid JSON: {exc}"
        ) from exc

    # 2. Pydantic schema validation (FR-01)
    try:
        plan = ReportPlan.model_validate(data)
    except ValidationError as exc:
        raise ReportPlanLoadError(
            f"Report plan schema validation failed:\n{exc}"
        ) from exc

    # 3. Dependency-reference validation (FR-02)
    try:
        validate_dependency_references(plan)
    except ValueError as exc:
        raise ReportPlanLoadError(str(exc)) from exc

    # 4. Content-cycle detection (FR-03)
    try:
        validate_no_content_cycles(plan)
    except ValueError as exc:
        raise ReportPlanLoadError(str(exc)) from exc

    # 5. Depth-level consistency
    try:
        validate_depth_levels(plan)
    except ValueError as exc:
        raise ReportPlanLoadError(str(exc)) from exc

    return plan
```

### `synthesizer/loaders/style_loader.py`
```python
# synthesizer/loaders/style_loader.py
"""Style sheet loader (§7, §10.5).

Loads a JSON style sheet from disk, parses it into a validated StyleSheet
object (FR-04). Citation pattern regex compilation is enforced by the
StyleSheet model's field validator.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from synthesizer.config import STYLE_SHEET_PATH
from synthesizer.models.style_sheet import StyleSheet


class StyleSheetLoadError(Exception):
    """Raised when style sheet loading or validation fails.

    Wraps Pydantic ValidationError, JSON decode errors, and
    regex-compilation errors with descriptive context.
    """


def load_style_sheet(path: Optional[Path] = None) -> StyleSheet:
    """Load and validate a style sheet from a JSON file.

    Performs, in order:
      1. File read and JSON parse
      2. Pydantic schema validation, including citation_pattern regex
         compilation check (FR-04)

    Parameters
    ----------
    path : Path, optional
        Explicit path to the style sheet JSON. If *None*, falls back to
        ``STYLE_SHEET_PATH`` from the synthesizer config (§16).

    Returns
    -------
    StyleSheet
        Fully validated style sheet.

    Raises
    ------
    StyleSheetLoadError
        On any validation or I/O failure, with a descriptive message.
    """
    resolved_path = path or STYLE_SHEET_PATH
    if resolved_path is None:
        raise StyleSheetLoadError(
            "No style sheet path provided and STYLE_SHEET_PATH is not "
            "configured. Set the STYLE_SHEET_PATH environment variable "
            "or pass an explicit path."
        )

    resolved_path = Path(resolved_path)

    # 1. File read + JSON parse
    try:
        raw_text = resolved_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise StyleSheetLoadError(
            f"Style sheet file not found: {resolved_path}"
        ) from exc
    except OSError as exc:
        raise StyleSheetLoadError(
            f"Failed to read style sheet file {resolved_path}: {exc}"
        ) from exc

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise StyleSheetLoadError(
            f"Style sheet is not valid JSON: {exc}"
        ) from exc

    # 2. Pydantic schema validation (FR-04)
    #    citation_pattern regex compilation is enforced by the
    #    StyleSheet model's field_validator.
    try:
        style_sheet = StyleSheet.model_validate(data)
    except ValidationError as exc:
        raise StyleSheetLoadError(
            f"Style sheet schema validation failed:\n{exc}"
        ) from exc

    return style_sheet
```

### `synthesizer/validation/__init__.py`
```python
# synthesizer/validation/__init__.py
"""Validation modules for the Report Synthesizer."""

from synthesizer.validation.graph_validation import (
    build_generation_dag,
    collect_all_edges,
    validate_dependency_references,
    validate_depth_levels,
    validate_no_content_cycles,
)

__all__ = [
    "build_generation_dag",
    "collect_all_edges",
    "validate_dependency_references",
    "validate_depth_levels",
    "validate_no_content_cycles",
]
```

### `synthesizer/validation/graph_validation.py`
```python
# synthesizer/validation/graph_validation.py
"""Graph-level validation for report plans (§10.2–10.4, §8).

Provides:
  - Dangling dependency-reference detection (FR-02)
  - Content-dependency cycle detection via topological sort (FR-03)
  - Depth-level consistency validation
  - Generation DAG construction (FR-06)
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

from synthesizer.models.enums import DependencyKind
from synthesizer.models.report_plan import DependencyEdge, ReportPlan


@dataclass
class GenerationDAG:
    """Result of DAG construction (FR-06).

    Attributes
    ----------
    adjacency : dict
        Maps each section_id to the list of section_ids that depend on it
        (i.e., successors in generation order). If A must be generated
        before B, then B is in adjacency[A].
    topological_order : list
        A valid topological ordering of section_ids for generation.
    nodes : set
        All section_ids present in the DAG (including isolated nodes).
    edges : list
        The content-type DependencyEdge objects used to build the DAG.
    """

    adjacency: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))
    topological_order: List[str] = field(default_factory=list)
    nodes: Set[str] = field(default_factory=set)
    edges: List[DependencyEdge] = field(default_factory=list)


def collect_all_edges(plan: ReportPlan) -> List[DependencyEdge]:
    """Collect every DependencyEdge from every section in the plan.

    Parameters
    ----------
    plan : ReportPlan
        Validated report plan.

    Returns
    -------
    list of DependencyEdge
        Flat list of all edges across all sections.
    """
    all_edges: List[DependencyEdge] = []
    for section in plan.sections:
        all_edges.extend(section.dependency_edges)
    return all_edges


def _get_section_id_set(plan: ReportPlan) -> Set[str]:
    """Return the set of all declared section_ids."""
    return {section.section_id for section in plan.sections}


# ---------------------------------------------------------------------------
# FR-02  Dangling dependency-reference detection
# ---------------------------------------------------------------------------

def validate_dependency_references(plan: ReportPlan) -> None:
    """Validate that every section_id in dependency_edges exists (FR-02).

    Checks both ``source_section_id`` and ``target_section_id`` for every
    edge on every section.

    Parameters
    ----------
    plan : ReportPlan
        Parsed (but not yet cross-validated) report plan.

    Raises
    ------
    ValueError
        If any referenced section_id does not exist as a declared section,
        with a message naming the dangling reference(s).
    """
    declared_ids = _get_section_id_set(plan)
    dangling: List[str] = []

    for section in plan.sections:
        for edge in section.dependency_edges:
            if edge.source_section_id not in declared_ids:
                dangling.append(
                    f"source_section_id '{edge.source_section_id}' "
                    f"(in edge on section '{section.section_id}')"
                )
            if edge.target_section_id not in declared_ids:
                dangling.append(
                    f"target_section_id '{edge.target_section_id}' "
                    f"(in edge on section '{section.section_id}')"
                )

    if dangling:
        details = "; ".join(dangling)
        raise ValueError(
            f"Dangling dependency reference(s) — the following section_ids "
            f"are referenced in dependency_edges but do not exist as "
            f"declared sections: {details}"
        )


# ---------------------------------------------------------------------------
# FR-03  Content-dependency cycle detection
# ---------------------------------------------------------------------------

def validate_no_content_cycles(plan: ReportPlan) -> None:
    """Validate that CONTENT-type edges contain no cycles (FR-03).

    Uses Kahn's algorithm (BFS topological sort) on content-type edges
    only. Non-content edge types (REFERENCE, THEMATIC, SOURCE) are
    excluded — they do not impose generation-ordering constraints (§8).

    Parameters
    ----------
    plan : ReportPlan
        Report plan that has already passed reference validation (FR-02).

    Raises
    ------
    ValueError
        If a cycle is detected among content-type edges, with a message
        identifying the section_ids involved in the cycle.
    """
    all_edges = collect_all_edges(plan)
    content_edges = [e for e in all_edges if e.kind == DependencyKind.CONTENT]

    if not content_edges:
        return  # No content edges → no cycle possible.

    declared_ids = _get_section_id_set(plan)

    # Build adjacency for content edges:
    #   target → source  (upstream → downstream in generation order)
    # i.e., target_section_id must be generated before source_section_id.
    adjacency: Dict[str, List[str]] = defaultdict(list)
    in_degree: Dict[str, int] = {sid: 0 for sid in declared_ids}

    for edge in content_edges:
        adjacency[edge.target_section_id].append(edge.source_section_id)
        in_degree[edge.source_section_id] = (
            in_degree.get(edge.source_section_id, 0) + 1
        )

    # Kahn's algorithm
    queue: deque[str] = deque(
        sid for sid, deg in in_degree.items() if deg == 0
    )
    visited_count = 0

    while queue:
        node = queue.popleft()
        visited_count += 1
        for successor in adjacency.get(node, []):
            in_degree[successor] -= 1
            if in_degree[successor] == 0:
                queue.append(successor)

    if visited_count < len(declared_ids):
        # Some nodes were never visited → cycle exists among them.
        cycle_members = sorted(
            sid for sid, deg in in_degree.items() if deg > 0
        )
        raise ValueError(
            f"Content-dependency cycle detected among sections: "
            f"{cycle_members}. The dependency graph must be acyclic for "
            f"content-type edges (§8.1, FR-03)."
        )


# ---------------------------------------------------------------------------
# Depth-level consistency
# ---------------------------------------------------------------------------

def validate_depth_levels(plan: ReportPlan) -> None:
    """Validate that each section's depth_level equals its ancestor chain length.

    The ancestor chain is computed by following parent_id links.
    A top-level section (parent_id is None) must have depth_level 0.

    Parameters
    ----------
    plan : ReportPlan
        Report plan to validate.

    Raises
    ------
    ValueError
        If any section's depth_level does not match its computed ancestor
        chain length, or if a parent_id references a non-existent section.
    """
    id_to_section = {s.section_id: s for s in plan.sections}
    errors: List[str] = []

    for section in plan.sections:
        # Compute ancestor chain length
        depth = 0
        current_parent = section.parent_id
        visited: Set[str] = {section.section_id}

        while current_parent is not None:
            if current_parent not in id_to_section:
                errors.append(
                    f"Section '{section.section_id}' references "
                    f"parent_id '{current_parent}' which does not exist."
                )
                break
            if current_parent in visited:
                errors.append(
                    f"Section '{section.section_id}' has a circular "
                    f"parent chain involving '{current_parent}'."
                )
                break
            visited.add(current_parent)
            depth += 1
            current_parent = id_to_section[current_parent].parent_id

        if section.depth_level != depth and not errors:
            errors.append(
                f"Section '{section.section_id}' has depth_level="
                f"{section.depth_level} but its ancestor chain length is "
                f"{depth}."
            )

    if errors:
        raise ValueError(
            "Depth-level consistency check failed: " + "; ".join(errors)
        )


# ---------------------------------------------------------------------------
# FR-06  Generation DAG construction
# ---------------------------------------------------------------------------

def build_generation_dag(plan: ReportPlan) -> GenerationDAG:
    """Build the generation DAG from content-type dependency edges (FR-06).

    The DAG encodes generation ordering: if section B has a content
    dependency on section A, then A must be generated (and finalized)
    before B. In the adjacency representation, A → B means "A is a
    prerequisite of B".

    Parameters
    ----------
    plan : ReportPlan
        Report plan that has already passed validation (FR-02, FR-03).

    Returns
    -------
    GenerationDAG
        DAG with adjacency, topological order, node set, and edge list.
    """
    declared_ids = _get_section_id_set(plan)
    all_edges = collect_all_edges(plan)
    content_edges = [e for e in all_edges if e.kind == DependencyKind.CONTENT]

    adjacency: Dict[str, List[str]] = defaultdict(list)
    in_degree: Dict[str, int] = {sid: 0 for sid in declared_ids}

    for edge in content_edges:
        # target (upstream) → source (downstream)
        adjacency[edge.target_section_id].append(edge.source_section_id)
        in_degree[edge.source_section_id] = (
            in_degree.get(edge.source_section_id, 0) + 1
        )

    # Topological sort (Kahn's algorithm) — deterministic via sorted queue
    queue: deque[str] = deque(
        sorted(sid for sid, deg in in_degree.items() if deg == 0)
    )
    topo_order: List[str] = []

    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for successor in sorted(adjacency.get(node, [])):
            in_degree[successor] -= 1
            if in_degree[successor] == 0:
                queue.append(successor)

    dag = GenerationDAG(
        adjacency=dict(adjacency),
        topological_order=topo_order,
        nodes=declared_ids,
        edges=content_edges,
    )

    return dag


def build_finalization_dag(
    plan: ReportPlan,
) -> Tuple[Dict[str, List[str]], List[str]]:
    """Build the finalization DAG (FR-07) — content + reference edges.

    The finalization DAG includes both CONTENT and REFERENCE edges.
    A section cannot finalize until all of its content *and* reference
    predecessors have finalized.

    Returns
    -------
    (adjacency, topological_order)
        Same structure as GenerationDAG, but covering more edge kinds.
    """
    declared_ids = _get_section_id_set(plan)
    all_edges = collect_all_edges(plan)
    fin_edges = [
        e
        for e in all_edges
        if e.kind in (DependencyKind.CONTENT, DependencyKind.REFERENCE)
    ]

    adjacency: Dict[str, List[str]] = defaultdict(list)
    in_degree: Dict[str, int] = {sid: 0 for sid in declared_ids}

    for edge in fin_edges:
        adjacency[edge.target_section_id].append(edge.source_section_id)
        in