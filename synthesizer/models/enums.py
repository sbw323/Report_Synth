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