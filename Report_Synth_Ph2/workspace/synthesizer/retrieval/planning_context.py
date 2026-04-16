# synthesizer/retrieval/planning_context.py
"""Stage 06 PaperSummary loader for planning context only (§14.1, DR-06).

Loads PaperSummary objects from Stage 06's ``load_all_summaries()``
function. These summaries are used exclusively for planning purposes
(e.g., retrieval query construction) and are **never** injected into
generation prompts as source evidence.

DR-06 (decided): Stage 06 summaries are used for planning only, not as
generation evidence. PaperSummary objects inform retrieval query
construction but are never injected into generation prompts as source
material. Summaries are abstractions; generation must be grounded in
primary chunk evidence from the vector store.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lightweight representation of PaperSummary data
# ---------------------------------------------------------------------------

@dataclass
class PaperSummaryInfo:
    """Planning-only representation of a Stage 06 PaperSummary.

    This is a read-only data class that captures the fields from
    Stage 06's PaperSummary relevant to planning. It is explicitly
    NOT a prompt context channel — see DR-06.

    Attributes
    ----------
    paper_id : str
        Unique paper identifier.
    title : str
        Paper title.
    authors : str
        Author string.
    year : str
        Publication year.
    objective : str
        Paper's stated objective.
    methodology : str
        Summary of methodology.
    key_findings : str
        Key findings summary.
    limitations : str
        Noted limitations.
    relevance_tags : list of str
        Tags indicating relevance domains.
    """

    paper_id: str = ""
    title: str = ""
    authors: str = ""
    year: str = ""
    objective: str = ""
    methodology: str = ""
    key_findings: str = ""
    limitations: str = ""
    relevance_tags: List[str] = field(default_factory=list)


def _convert_paper_summary(raw: Any) -> PaperSummaryInfo:
    """Convert a Stage 06 PaperSummary object to our planning-only dataclass.

    Handles both attribute-based objects and dict-like objects.
    """
    def _get(obj: Any, attr: str, default: Any = "") -> Any:
        if hasattr(obj, attr):
            return getattr(obj, attr)
        if isinstance(obj, dict):
            return obj.get(attr, default)
        return default

    return PaperSummaryInfo(
        paper_id=str(_get(raw, "paper_id", "")),
        title=str(_get(raw, "title", "")),
        authors=str(_get(raw, "authors", "")),
        year=str(_get(raw, "year", "")),
        objective=str(_get(raw, "objective", "")),
        methodology=str(_get(raw, "methodology", "")),
        key_findings=str(_get(raw, "key_findings", "")),
        limitations=str(_get(raw, "limitations", "")),
        relevance_tags=list(_get(raw, "relevance_tags", [])),
    )


def load_planning_summaries() -> List[PaperSummaryInfo]:
    """Load PaperSummary data from Stage 06 for planning use only (DR-06).

    Calls ``load_all_summaries()`` from ``06_review.py`` and converts
    the results to ``PaperSummaryInfo`` dataclass instances.

    These summaries are used for planning (e.g., query construction)
    and must NEVER be injected into generation prompts.

    Returns
    -------
    list of PaperSummaryInfo
        Planning-only summary representations. Empty list if Stage 06
        is not importable.
    """
    try:
        from importlib import import_module
        mod = import_module("06_review")
        load_fn = getattr(mod, "load_all_summaries", None)
        if load_fn is None:
            logger.warning(
                "06_review module does not expose load_all_summaries(). "
                "No planning summaries loaded."
            )
            return []
        raw_summaries = load_fn()
        result = [_convert_paper_summary(s) for s in raw_summaries]
        logger.info("Loaded %d planning summaries from Stage 06.", len(result))
        return result
    except (ImportError, ModuleNotFoundError):
        logger.warning(
            "Stage 06 (06_review) is not importable. "
            "No planning summaries loaded."
        )
        return []
    except Exception:
        logger.exception("Failed to load planning summaries from Stage 06.")
        return []


def get_summary_by_paper_id(
    summaries: List[PaperSummaryInfo],
    paper_id: str,
) -> Optional[PaperSummaryInfo]:
    """Look up a planning summary by paper_id.

    Parameters
    ----------
    summaries : list of PaperSummaryInfo
        Loaded planning summaries.
    paper_id : str
        The paper_id to search for.

    Returns
    -------
    PaperSummaryInfo or None
    """
    for s in summaries:
        if s.paper_id == paper_id:
            return s
    return None