# synthesizer/extraction/summary_abstractifier.py
"""Summary abstractifier — generates 2-3 sentence section summaries (§9.2.4).

Generates summary abstracts from finalized section text for use as
thematic context in downstream generation prompts (§13.2).

Supports: FR-20 (post-finalization processing).
DR-16: Model selection remains open — LLM client is injected via protocol.
DR-18: Output budget is 200 tokens per §9.2.4; input budget remains open.
"""

from __future__ import annotations

import logging
import re
from typing import Optional, Protocol, runtime_checkable

logger = logging.getLogger(__name__)

# Output token cap per §9.2.4 (partially open DR-18)
SUMMARY_ABSTRACTIFIER_OUTPUT_TOKENS = 200

# Word count constraints per §9.2.4
MIN_WORDS = 20
MAX_WORDS = 100

# Retry limit for word-count compliance
_MAX_RETRIES = 2


# ---------------------------------------------------------------------------
# LLM client protocol (DR-16: model selection configurable per role)
# ---------------------------------------------------------------------------

@runtime_checkable
class LLMClient(Protocol):
    """Protocol for LLM invocation used by the summary abstractifier.

    DR-16 (open): May use a lighter model than the Generator.
    """

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int = SUMMARY_ABSTRACTIFIER_OUTPUT_TOKENS,
    ) -> str:
        """Invoke the LLM and return the response text."""
        ...


# ---------------------------------------------------------------------------
# System prompts (§9.2.4)
# ---------------------------------------------------------------------------

_SUMMARY_SYSTEM_PROMPT = (
    "You are a scientific summarizer. Your task is to produce a concise "
    "summary abstract of a finalized section from a scientific literature "
    "review.\n\n"
    "Requirements:\n"
    "- Produce exactly 2-3 sentences\n"
    "- Stay within 50-100 words\n"
    "- Capture the section's key points and conclusions\n"
    "- Use formal academic tone\n"
    "- Do NOT include citations or references\n"
    "- Respond with ONLY the summary text, no JSON or formatting\n"
)

_TIGHTER_SUMMARY_SYSTEM_PROMPT = (
    "You are a scientific summarizer. Your previous summary was too "
    "long or too short. Please produce a concise summary abstract.\n\n"
    "STRICT requirements:\n"
    "- Produce EXACTLY 2-3 sentences\n"
    "- MUST be between 50 and 100 words (count carefully)\n"
    "- Capture only the most important point(s)\n"
    "- Use formal academic tone\n"
    "- Respond with ONLY the summary text\n"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def _count_sentences(text: str) -> int:
    """Approximate sentence count by splitting on sentence-ending punctuation."""
    sentences = re.split(r'[.!?]+\s+', text.strip())
    return len([s for s in sentences if s])


def _is_valid_summary(text: str) -> bool:
    """Check whether a summary meets the §9.2.4 word and sentence constraints.

    Returns True if the summary has 2-3 sentences and between
    MIN_WORDS and MAX_WORDS words (inclusive).
    """
    word_count = _count_words(text)
    sentence_count = _count_sentences(text)
    return (
        MIN_WORDS <= word_count <= MAX_WORDS
        and 2 <= sentence_count <= 3
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_summary_abstract(
    section_id: str,
    content_markdown: str,
    llm_client: LLMClient,
    max_retries: int = _MAX_RETRIES,
) -> Optional[str]:
    """Generate a 2-3 sentence summary abstract for a finalized section.

    Uses the injected LLM client to produce a concise summary of the
    section content.  If the first attempt doesn't meet word/sentence
    constraints, retries with a tighter prompt up to *max_retries* times.

    Parameters
    ----------
    section_id : str
        Identifier for the section being summarized (for logging).
    content_markdown : str
        The finalized section text in markdown format.
    llm_client : LLMClient
        An object satisfying the LLMClient protocol (DR-16).
    max_retries : int, optional
        Maximum number of retry attempts for constraint compliance.
        Defaults to ``_MAX_RETRIES``.

    Returns
    -------
    str or None
        The summary abstract text if successfully generated, or None
        if all attempts failed or an error occurred.

    Supports
    --------
    FR-20 : Post-finalization summary generation.
    DR-16 : Model selection via injected client.
    DR-18 : Output budget capped at SUMMARY_ABSTRACTIFIER_OUTPUT_TOKENS.
    """
    if not content_markdown or not content_markdown.strip():
        logger.warning(
            "Section %s has empty content — skipping summary generation.",
            section_id,
        )
        return None

    user_message = (
        f"Produce a summary abstract for the following section "
        f"(section_id: {section_id}):\n\n"
        f"{content_markdown}"
    )

    # --- First attempt with standard prompt --------------------------------
    try:
        summary = llm_client.invoke(
            system_prompt=_SUMMARY_SYSTEM_PROMPT,
            user_message=user_message,
            max_output_tokens=SUMMARY_ABSTRACTIFIER_OUTPUT_TOKENS,
        ).strip()
    except Exception as exc:
        logger.error(
            "LLM invocation failed for section %s summary: %s",
            section_id, exc,
        )
        return None

    if _is_valid_summary(summary):
        logger.info(
            "Section %s summary generated: %d words, %d sentences.",
            section_id, _count_words(summary), _count_sentences(summary),
        )
        return summary

    # --- Retry with tighter prompt if constraints not met ------------------
    for attempt in range(1, max_retries + 1):
        logger.info(
            "Section %s summary attempt %d did not meet constraints "
            "(%d words, %d sentences). Retrying with tighter prompt.",
            section_id, attempt,
            _count_words(summary), _count_sentences(summary),
        )

        retry_message = (
            f"Your previous summary was {_count_words(summary)} words "
            f"and {_count_sentences(summary)} sentences. It must be "
            f"2-3 sentences and {MIN_WORDS}-{MAX_WORDS} words.\n\n"
            f"Section content:\n\n{content_markdown}"
        )

        try:
            summary = llm_client.invoke(
                system_prompt=_TIGHTER_SUMMARY_SYSTEM_PROMPT,
                user_message=retry_message,
                max_output_tokens=SUMMARY_ABSTRACTIFIER_OUTPUT_TOKENS,
            ).strip()
        except Exception as exc:
            logger.error(
                "LLM retry %d failed for section %s summary: %s",
                attempt, section_id, exc,
            )
            return None

        if _is_valid_summary(summary):
            logger.info(
                "Section %s summary generated on retry %d: %d words, "
                "%d sentences.",
                section_id, attempt,
                _count_words(summary), _count_sentences(summary),
            )
            return summary

    # --- All retries exhausted — return best effort -----------------------
    logger.warning(
        "Section %s summary did not meet constraints after %d retries "
        "(%d words, %d sentences). Returning best-effort result.",
        section_id, max_retries,
        _count_words(summary), _count_sentences(summary),
    )
    return summary