# synthesizer/validation/coordinator.py
"""Validation coordinator — sequential L1 → L2 → L3 pipeline (§12).

Runs all three validation layers in order, short-circuiting on failure.
Does NOT manage retries — that is the retry module's responsibility.

The coordinator is a pure function: given inputs, it runs validation
and returns results. State mutation (retry counters, validation history)
is handled by the caller or the retry module.
"""

from __future__ import annotations

from