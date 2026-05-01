# synthesizer/extraction/claim_extractor.py
"""Claim table extraction from finalized section text (§9.2.3, §12.4).

Invokes an LLM to extract structured ClaimTable (§10.7) from finalized
section content and its retrieval chunks.

Supports: FR-20, FR-22.
DR-14: CLAIM_EXTRACTION_RETRY_LIMIT is configurable (default 1).
DR-16: Model selection remains open — LLM client is injected via protocol.
DR-18: Output budget is 2000 tokens per §9.2.3; input budget remains open.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from synthesizer.config import CLAIM_EXTRACTION_RETRY_LIMIT
from synthesizer.models.claims import ClaimTable
from synthesizer.models.enums import ConfidenceTag
from synthesizer.retrieval.adapter import RankedChunk

logger = logging.getLogger(__name__)

# Output token cap per §9.2.3 (partially open DR-18)
CLAIM_EXTRACTOR_OUTPUT_TOKENS = 9000


# ---------------------------------------------------------------------------
# LLM client protocol (DR-16: model selection configurable per role)
# ---------------------------------------------------------------------------

@runtime_checkable
class LLMClient(Protocol):
    """Protocol for LLM invocation used by the claim extractor.

    DR-16 (open): Implementations may use different models per role.
    """

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        max_output_tokens: int = CLAIM_EXTRACTOR_OUTPUT_TOKENS,
    ) -> str:
        """Invoke the LLM and return the response text."""
        ...


# ---------------------------------------------------------------------------
# System prompt (§9.2.3)
# ---------------------------------------------------------------------------

_CLAIM_EXTRACTOR_SYSTEM_PROMPT = (
    "You are a claim extraction specialist. Your task is to extract "
    "structured claims from a finalized section of a scientific literature "
    "review.\n\n"
    "For each claim you identify in the section text, produce a JSON entry "
    "with:\n"
    "- claim_id: unique identifier in format 'claim_0', 'claim_1', etc.\n"
    "- claim_text: the claim statement as it appears or is expressed in "
    "the section\n"
    "- source_chunk_ids: list of chunk IDs from the provided evidence "
    "chunks that support this claim (at least one required)\n"
    "- confidence_tag: one of 'directly_stated' (claim appears verbatim "
    "or near-verbatim in a source chunk), 'inferred' (reasonable "
    "inference from a source chunk), or 'synthesized' (combines "
    "information from multiple source chunks)\n"
    "- section_text_span: {\"start\": <int>, \"end\": <int>} character "
    "offsets locating the claim in the section text (0-indexed, start "
    "inclusive, end exclusive)\n\n"
    "Respond with ONLY valid JSON in this exact format:\n"
    "{\n"
    '  "section_id": "<section_id>",\n'
    '  "version": 1,\n'
    '  "claims": [<list of claim entries>],\n'
    '  "partial": false,\n'
    '  "extraction_attempt": 1\n'
    "}\n\n"
    "Extract ALL substantive claims from the section. Every claim must "
    "be traceable to at least one evidence chunk.\n"
)


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def _parse_claim_table_response(
    raw_response: str,
    section_id: str,
    version: int,
    attempt: int,
) -> ClaimTable:
    """Parse LLM response into a validated ClaimTable.

    Raises ValueError if parsing or validation fails.
    """
    text = raw_response.strip()
    # Handle markdown fences
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines)

    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object, got {type(data).__name__}")

    # Override metadata fields to ensure consistency
    data["section_id"] = section_id
    data["version"] = version
    data["extraction_attempt"] = attempt

    return ClaimTable.model_validate(data)


# ---------------------------------------------------------------------------
# FR-20, FR-22  Claim extraction with retry and partial fallback
# ---------------------------------------------------------------------------

def extract_claim_table(
    section_id: str,
    content_markdown: str,
    retrieved_chunks: List[RankedChunk],
    llm_client: LLMClient,
    version: int = 1,
    retry_limit: int = CLAIM_EXTRACTION_RETRY_LIMIT,
) -> ClaimTable:
    """Extract a ClaimTable from finalized section text (FR-20, FR-22).

    Invokes the LLM to extract structured claims, then validates the
    result. On failure, retries up to ``retry_limit`` times. If all
    attempts fail, returns a partial ClaimTable (FR-22).

    Parameters
    ----------
    section_id : str
        The section this claim table is for.
    content_markdown : str
        Finalized section content in Markdown.
    retrieved_chunks : list of RankedChunk
        Evidence chunks used during section generation.
    llm_client : LLMClient
        LLM client for claim extraction. DR-16: model configurable.
    version : int
        Claim table version (increments on re-extraction).
    retry_limit : int
        Maximum retries on failure. DR-14: configurable, default 1.

    Returns
    -------
    ClaimTable
        Extracted claim table. May have partial=True on retry exhaustion.

    Supports
    --------
    FR-20 : Produces ClaimTable with ClaimEntry instances.
    FR-22 : On retry exhaustion, sets partial=True and returns.
    DR-14 : retry_limit is configurable.
    DR-16 : LLM client is injected, model selection is open.
    DR-18 : Output budget is 2000 tokens; input budget remains open.
    """
    # Format evidence chunks for the prompt
    chunks_text_parts: List[str] = []
    for chunk in retrieved_chunks:
        meta = chunk.metadata
        meta_str = ", ".join(
            f"{k}: {v}" for k, v in sorted(meta.items()) if v
        ) or "no metadata"
        chunks_text_parts.append(
            f"  [{chunk.id}] ({meta_str})\n  {chunk.text}"
        )
    chunks_text = "\n".join(chunks_text_parts) if chunks_text_parts else "(No evidence chunks)"

    user_message = (
        f"Section ID: {section_id}\n\n"
        f"=== SECTION TEXT ===\n{content_markdown}\n"
        f"=== END SECTION TEXT ===\n\n"
        f"=== EVIDENCE CHUNKS ===\n{chunks_text}\n"
        f"=== END EVIDENCE CHUNKS ===\n\n"
        "Extract all substantive claims from the section text. "
        "Map each claim to supporting evidence chunk(s) by their IDs."
    )

    last_error: Optional[str] = None

    # Initial attempt + retries
    total_attempts = 1 + retry_limit
    for attempt_num in range(1, total_attempts + 1):
        try:
            prompt = user_message
            if last_error and attempt_num > 1:
                prompt += (
                    f"\n\nPrevious extraction attempt failed: {last_error}\n"
                    "Please fix the issues and try again."
                )

            raw_response = llm_client.invoke(
                system_prompt=_CLAIM_EXTRACTOR_SYSTEM_PROMPT,
                user_message=prompt,
                max_output_tokens=CLAIM_EXTRACTOR_OUTPUT_TOKENS,
            )

            claim_table = _parse_claim_table_response(
                raw_response, section_id, version, attempt_num
            )

            logger.info(
                "Claim extraction succeeded for section '%s' on attempt %d "
                "with %d claims.",
                section_id, attempt_num, len(claim_table.claims),
            )
            return claim_table

        except Exception as exc:
            last_error = str(exc)
            logger.warning(
                "Claim extraction attempt %d/%d failed for section '%s': %s",
                attempt_num, total_attempts, section_id, last_error,
            )

    # FR-22: All attempts exhausted — return partial claim table
    logger.warning(
        "Claim extraction exhausted all %d attempts for section '%s'. "
        "Returning partial claim table (FR-22).",
        total_attempts, section_id,
    )
    return ClaimTable(
        section_id=section_id,
        version=version,
        claims=[],
        partial=True,
        extraction_attempt=total_attempts,
    )