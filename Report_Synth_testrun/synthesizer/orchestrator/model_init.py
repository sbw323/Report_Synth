# synthesizer/orchestrator/model_init.py
"""Model availability check with graceful degradation (§5, NFR-09).

Verifies at initialization time that the configured SYNTHESIZER_MODEL
is likely available. Raises a descriptive error if not, preventing
silent failures mid-generation.

DR-16 (open): Model selection per role remains configurable.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from synthesizer.config import SYNTHESIZER_MODEL

logger = logging.getLogger(__name__)


class ModelNotAvailableError(Exception):
    """Raised when the configured model is not available (NFR-09).

    Provides a descriptive error message to help diagnose the issue.

    Attributes
    ----------
    model : str
        The model identifier that was checked.
    reason : str
        Human-readable reason for unavailability.
    """

    def __init__(self, model: str, reason: str) -> None:
        self.model = model
        self.reason = reason
        super().__init__(
            f"Model '{model}' is not available: {reason}. "
            f"Please check your SYNTHESIZER_MODEL configuration and "
            f"ANTHROPIC_API_KEY environment variable."
        )


def check_model_availability(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    *,
    probe_api: bool = False,
) -> str:
    """Verify that the configured model is available before generation (NFR-09).

    Performs checks in order:
      1. Model string is non-empty and valid
      2. ``anthropic`` package is importable
      3. ``ANTHROPIC_API_KEY`` is configured
      4. Anthropic client can be instantiated
      5. (Optional) Lightweight API probe if ``probe_api=True``

    Parameters
    ----------
    model : str, optional
        Model identifier to check. Defaults to SYNTHESIZER_MODEL from
        config. DR-16: this is configurable per role.
    api_key : str, optional
        API key to use. Defaults to ANTHROPIC_API_KEY env var.
    probe_api : bool
        If True, attempt a minimal API call to verify connectivity.
        Default False to avoid unnecessary API usage during testing.

    Returns
    -------
    str
        The validated model identifier.

    Raises
    ------
    ModelNotAvailableError
        If any check fails, with a descriptive error message indicating
        the specific failure point.
    """
    resolved_model = model or SYNTHESIZER_MODEL
    resolved_key = api_key or os.environ.get("ANTHROPIC_API_KEY")

    # Check 1: Model string validity
    if not resolved_model or not isinstance(resolved_model, str):
        raise ModelNotAvailableError(
            model=str(resolved_model),
            reason="Model identifier is empty or not a string",
        )

    if len(resolved_model.strip()) == 0:
        raise ModelNotAvailableError(
            model=resolved_model,
            reason="Model identifier is blank",
        )

    # Check 2: anthropic package importable
    try:
        import anthropic  # noqa: F401
    except ImportError:
        raise ModelNotAvailableError(
            model=resolved_model,
            reason=(
                "The 'anthropic' Python package is not installed. "
                "Install it with: pip install anthropic"
            ),
        )

    # Check 3: API key configured
    if not resolved_key:
        raise ModelNotAvailableError(
            model=resolved_model,
            reason=(
                "ANTHROPIC_API_KEY environment variable is not set. "
                "Set it to a valid API key."
            ),
        )

    # Check 4: Client instantiation
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=resolved_key)
    except Exception as exc:
        raise ModelNotAvailableError(
            model=resolved_model,
            reason=f"Failed to instantiate Anthropic client: {exc}",
        )

    # Check 5: Optional API probe
    if probe_api:
        try:
            # Minimal call to verify connectivity and model access
            response = client.messages.create(
                model=resolved_model,
                max_tokens=10,
                messages=[{"role": "user", "content": "ping"}],
            )
            logger.info(
                "Model probe successful: %s (stop_reason=%s)",
                resolved_model,
                getattr(response, "stop_reason", "unknown"),
            )
        except Exception as exc:
            raise ModelNotAvailableError(
                model=resolved_model,
                reason=f"API probe failed: {exc}",
            )

    logger.info("Model availability check passed: %s", resolved_model)
    return resolved_model


def model_for_role(
    role: str,
    *,
    model_override: Optional[str] = None,
) -> str:
    """Return the model identifier for a given LLM role (DR-16).

    DR-16 (open): Model selection per role remains configurable. Currently
    all roles use SYNTHESIZER_MODEL. This function provides the extension
    point for future per-role model differentiation.

    Parameters
    ----------
    role : str
        LLM role name: "generator", "validator", "claim_extractor",
        "summary_abstractifier".
    model_override : str, optional
        Override model for this specific role.

    Returns
    -------
    str
        Model identifier to use for this role.
    """
    if model_override:
        return model_override

    # DR-16: Currently all roles use the same model.
    # Future: read per-role config (e.g., SYNTHESIZER_VALIDATOR_MODEL)
    role_env_key = f"SYNTHESIZER_{role.upper()}_MODEL"
    env_value = os.environ.get(role_env_key)
    if env_value:
        return env_value

    return SYNTHESIZER_MODEL