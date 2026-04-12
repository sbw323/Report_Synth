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
from typing import Protocol, runtime_checkable

logger = logging.getLogger(__name__)

# Output token cap per §9.2.4 (partially open DR-18)
SUMMARY_ABSTRACTIFIER_OUTPUT_TOKENS = 200

# Word count constraints per §9.2.4
MIN_WORDS = 20
MAX_WORDS = 100


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


def _count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def _count_sentences(text: str) -> int:
    """Approximate sentence count."""
    import re
    sentences = re.split(r'[.!?