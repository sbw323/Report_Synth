# synthesizer/observability/tokens.py
"""Token accounting and budget enforcement (§5, §16, §17, NFR-02).

Tracks cumulative input and output tokens across all LLM calls within a
run. Enforces TOKEN_BUDGET_CEILING (DR-17: open, defaults to None).

Also provides per-section generation latency tracking with alert
on >120s (NFR-01).

Supports: NFR-01, NFR-02.
DR-17 (open): TOKEN_BUDGET_CEILING defaults to None (no limit).
DR-18 (open): Per-role input token budgets remain open.
"""

from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Generator, List, Optional

from synthesizer.config import TOKEN_BUDGET_CEILING

logger = logging.getLogger(__name__)

# NFR-01: Maximum generation latency per section (seconds)
DEFAULT_LATENCY_THRESHOLD_SECONDS = 120.0


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class TokenBudgetExceededError(Exception):
    """Raised when cumulative tokens exceed TOKEN_BUDGET_CEILING (NFR-02).

    Attributes
    ----------
    cumulative_tokens : int
        Total tokens consumed at the time of the error.
    ceiling : int
        The configured budget ceiling.
    """

    def __init__(
        self,
        cumulative_tokens: int,
        ceiling: int,
        *,
        message: Optional[str] = None,
    ) -> None:
        self.cumulative_tokens = cumulative_tokens
        self.ceiling = ceiling
        msg = message or (
            f"Token budget exceeded: {cumulative_tokens} tokens consumed, "
            f"ceiling is {ceiling}. Generation halted per NFR-02."
        )
        super().__init__(msg)


# ---------------------------------------------------------------------------
# Per-call record
# ---------------------------------------------------------------------------

@dataclass
class LLMCallRecord:
    """Record of a single LLM invocation for accounting purposes."""

    role: str  # e.g., "generator", "validator", "claim_extractor", "summary_abstractifier"
    section_id: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""
    latency_seconds: float = 0.0
    timestamp: str = ""


# ---------------------------------------------------------------------------
# Section latency timer
# ---------------------------------------------------------------------------

@dataclass
class SectionLatencyRecord:
    """Latency record for a single section generation (NFR-01)."""

    section_id: str
    start_time: float = 0.0
    end_time: float = 0.0
    latency_seconds: float = 0.0
    threshold_exceeded: bool = False


# ---------------------------------------------------------------------------
# Token tracker (NFR-02)
# ---------------------------------------------------------------------------

@dataclass
class TokenTracker:
    """Cumulative token accounting with budget ceiling enforcement (NFR-02).

    Tracks input and output tokens across all LLM calls in a run.
    Raises TokenBudgetExceededError when TOKEN_BUDGET_CEILING is reached.

    DR-17 (open): ceiling defaults to None (no limit).
    DR-18 (open): Per-role input budgets are not enforced here.

    Attributes
    ----------
    ceiling : int or None
        Maximum cumulative tokens (input + output). None = no limit.
    cumulative_input_tokens : int
        Total input tokens consumed.
    cumulative_output_tokens : int
        Total output tokens consumed.
    call_records : list of LLMCallRecord
        Individual call records for auditing.
    latency_records : list of SectionLatencyRecord
        Per-section latency records (NFR-01).
    latency_threshold : float
        Threshold in seconds for latency alerts (NFR-01, default 120s).
    """

    ceiling: Optional[int] = None
    cumulative_input_tokens: int = 0
    cumulative_output_tokens: int = 0
    call_records: List[LLMCallRecord] = field(default_factory=list)
    latency_records: List[SectionLatencyRecord] = field(default_factory=list)
    latency_threshold: float = DEFAULT_LATENCY_THRESHOLD_SECONDS

    def __post_init__(self) -> None:
        # If ceiling not explicitly provided, use config default
        if self.ceiling is None:
            self.ceiling = TOKEN_BUDGET_CEILING

    @property
    def cumulative_total_tokens(self) -> int:
        """Total tokens consumed (input + output)."""
        return self.cumulative_input_tokens + self.cumulative_output_tokens

    def record_call(
        self,
        role: str,
        input_tokens: int,
        output_tokens: int,
        *,
        section_id: Optional[str] = None,
        model: str = "",
        latency_seconds: float = 0.0,
    ) -> LLMCallRecord:
        """Record an LLM call and enforce budget ceiling (NFR-02).

        Parameters
        ----------
        role : str
            LLM role (e.g., "generator", "validator").
        input_tokens : int
            Input tokens consumed.
        output_tokens : int
            Output tokens consumed.
        section_id : str, optional
            Associated section ID.
        model : str
            Model identifier used.
        latency_seconds : float
            Call latency in seconds.

        Returns
        -------
        LLMCallRecord
            The recorded call.

        Raises
        ------
        TokenBudgetExceededError
            If cumulative tokens exceed the ceiling after this call.
        """
        self.cumulative_input_tokens += input_tokens
        self.cumulative_output_tokens += output_tokens

        record = LLMCallRecord(
            role=role,
            section_id=section_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model=model,
            latency_seconds=latency_seconds,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.call_records.append(record)

        logger.debug(
            "LLM call recorded: role=%s section=%s in=%d out=%d cumulative=%d",
            role, section_id, input_tokens, output_tokens,
            self.cumulative_total_tokens,
        )

        # NFR-02: Enforce budget ceiling
        self._check_ceiling()

        return record

    def _check_ceiling(self) -> None:
        """Check if cumulative tokens exceed the ceiling. Raise if so."""
        if self.ceiling is not None and self.cumulative_total_tokens >= self.ceiling:
            from synthesizer.observability.events import emit_budget_exceeded
            emit_budget_exceeded(
                run_id="",  # Caller should set context; this is a safety net
                cumulative_tokens=self.cumulative_total_tokens,
                ceiling=self.ceiling,
            )
            raise TokenBudgetExceededError(
                cumulative_tokens=self.cumulative_total_tokens,
                ceiling=self.ceiling,
            )

    def check_budget_before_call(self, estimated_tokens: int = 0) -> bool:
        """Pre-check whether there's budget remaining for another call.

        Parameters
        ----------
        estimated_tokens : int
            Estimated tokens for the upcoming call.

        Returns
        -------
        bool
            True if budget is sufficient, False if it would be exceeded.
        """
        if self.ceiling is None:
            return True
        return (self.cumulative_total_tokens + estimated_tokens) < self.ceiling

    @contextmanager
    def track_section_latency(
        self,
        section_id: str,
    ) -> Generator[SectionLatencyRecord, None, None]:
        """Context manager to track per-section generation latency (NFR-01).

        Usage::

            with tracker.track_section_latency("my_section") as record:
                # ... generation code ...
            # record.latency_seconds is now set

        If latency exceeds the threshold, a latency_alert event is emitted
        and a warning is logged (NFR-01).
        """
        record = SectionLatencyRecord(
            section_id=section_id,
            start_time=time.monotonic(),
        )
        try:
            yield record
        finally:
            record.end_time = time.monotonic()
            record.latency_seconds = record.end_time - record.start_time

            if record.latency_seconds > self.latency_threshold:
                record.threshold_exceeded = True
                from synthesizer.observability.events import emit_latency_alert
                emit_latency_alert(
                    section_id=section_id,
                    latency_seconds=record.latency_seconds,
                    threshold_seconds=self.latency_threshold,
                )

            self.latency_records.append(record)

    def get_summary(self) -> Dict[str, Any]:
        """Return a summary of token accounting for reporting."""
        return {
            "cumulative_input_tokens": self.cumulative_input_tokens,
            "cumulative_output_tokens": self.cumulative_output_tokens,
            "cumulative_total_tokens": self.cumulative_total_tokens,
            "ceiling": self.ceiling,
            "total_calls": len(self.call_records),
            "calls_by_role": self._calls_by_role(),
            "sections_exceeding_latency": [
                r.section_id for r in self.latency_records
                if r.threshold_exceeded
            ],
        }

    def _calls_by_role(self) -> Dict[str, int]:
        """Count calls grouped by role."""
        counts: Dict[str, int] = {}
        for rec in self.call_records:
            counts[rec.role] = counts.get(rec.role, 0) + 1
        return counts