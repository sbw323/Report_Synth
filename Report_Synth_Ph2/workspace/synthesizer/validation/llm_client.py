# synthesizer/validation/llm_client.py
"""Anthropic LLM client adapter for Layer 3 semantic validation (§12.3, DR-16).

Provides a concrete implementation of the LLMClient protocol defined in
layer3_semantic.py, wrapping the Anthropic Python SDK. This adapter is
the bridge between the validation subsystem and the Anthropic API.

Governing spec sections: §12.3, §9.2.2
Functional requirements: FR-18 (semantic validation LLM calls)
Non-functional requirements: NFR-09 (model availability)
Open decisions preserved: DR-16 (model selection per role), DR-18 (token budgets)
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from synthesizer.config import SYNTHESIZER_MODEL
from synthesizer.orchestrator.model_init import check_model_availability, model_for_role
from synthesizer.validation.layer3_semantic import LAYER3_OUTPUT_TOKENS_PER_SUBCHECK

logger = logging.getLogger(__name__)


class AnthropicLLMClient:
    """Concrete LLM client for Layer 3 semantic validation (§12.3, FR-18).

    Implements the ``LLMClient`` protocol from ``layer3_semantic.py``
    by wrapping the Anthropic Python SDK's messages API.

    Parameters
    ----------
    model : str, optional
        Model identifier. Defaults to the validator role model per DR-16.
    api_key : str, optional
        Anthropic API key. Defaults to ``ANTHROPIC_API_KEY`` env var.
    validate : bool
        If True, run ``check_model_availability()`` on construction (NFR-09).

    Raises
    ------
    synthesizer.orchestrator.model_init.ModelNotAvailableError
        If ``validate=True`` and the model/key is not available.

    Notes
    -----
    DR-16 (open): Model selection per role is supported via ``model_for_role()``.
    DR-18 (open): Output token budget defaults to ``LAYER3_OUTPUT_TOKENS_PER_SUBCHECK``.
    """

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        *,
        validate: bool = True,
    ) -> None:
        self._api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self._model = model or model_for_role("validator")

        if validate:
            # NFR-09: Verify model availability at construction time
            check_model_availability(
                model=self._model,
                api_key=self._api_key,
                probe_api=False,
            )

        import anthropic
        self._client = anthropic.Anthropic(api_key=self._api_key)
        logger.info(
            "AnthropicLLMClient initialized with model='%s'", self._model
        )

    @property
    def model(self) -> str:
        """The model identifier in use (DR-16)."""
        return self._model

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int = LAYER3_OUTPUT_TOKENS_PER_SUBCHECK,
    ) -> str:
        """Invoke the Anthropic messages API and return the response text.

        Implements the ``LLMClient`` protocol for Layer 3 semantic
        validation (§12.3, FR-18).

        Parameters
        ----------
        system_prompt : str
            System-level instructions for the LLM.
        user_message : str
            User-level message with validation context.
        max_output_tokens : int
            Maximum output tokens for this call (DR-18).

        Returns
        -------
        str
            Raw response text from the LLM.

        Raises
        ------
        Exception
            Any Anthropic API error is propagated to the caller.
            The caller (layer3_semantic sub-checks) catches exceptions
            and converts them to failure ValidationResults.
        """
        logger.debug(
            "LLM invoke: model=%s, max_output_tokens=%d, "
            "system_prompt_len=%d, user_message_len=%d",
            self._model,
            max_output_tokens,
            len(system_prompt),
            len(user_message),
        )

        response = self._client.messages.create(
            model=self._model,
            max_tokens=max_output_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        # Extract text from the response content blocks
        text_parts = []
        for block in response.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)

        result = "".join(text_parts)
        logger.debug(
            "LLM response: stop_reason=%s, response_len=%d",
            getattr(response, "stop_reason", "unknown"),
            len(result),
        )
        return result


def create_validation_llm_client(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    *,
    validate: bool = True,
) -> AnthropicLLMClient:
    """Factory function to create an LLM client for validation (§12.3, NFR-09).

    This is the recommended entry point for constructing the ``llm_client``
    parameter that ``run_validation_pipeline()`` and ``validate_layer3()``
    expect.

    Parameters
    ----------
    model : str, optional
        Model identifier. Defaults to validator role model (DR-16).
    api_key : str, optional
        Anthropic API key. Defaults to ``ANTHROPIC_API_KEY`` env var.
    validate : bool
        If True, verify model availability on construction (NFR-09).

    Returns
    -------
    AnthropicLLMClient
        A client implementing the ``LLMClient`` protocol.

    Raises
    ------
    synthesizer.orchestrator.model_init.ModelNotAvailableError
        If validation is enabled and the model/key is not available.
    """
    return AnthropicLLMClient(
        model=model,
        api_key=api_key,
        validate=validate,
    )