# synthesizer/__main__.py
"""CLI entry point for the Report Synthesizer Agent (§6, §16).

Usage:
    python -m synthesizer --report-plan <path> --style-sheet <path> [options]

Governing spec sections: §6, §16
Functional requirements: FR-01, FR-04
Non-functional requirements: NFR-05
Open decisions preserved: DR-16 (model selection), DR-17 (token budget)
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from synthesizer.config import SYNTHESIZER_MODEL, SYNTHESIZER_OUTPUT_DIR


def main() -> int:
    """Parse CLI arguments and execute the synthesis run.

    Returns
    -------
    int
        Exit code: 0 on success, 1 on failure.

    Supports
    --------
    FR-01 : Report plan path from CLI.
    FR-04 : Style sheet path from CLI.
    NFR-05 : Deterministic output directory.
    DR-16 : Model override via --model.
    """
    parser = argparse.ArgumentParser(
        prog="synthesizer",
        description="Report Synthesizer Agent — generates structured literature review sections.",
    )
    parser.add_argument(
        "--report-plan",
        type=Path,
        required=True,
        help="Path to the report plan JSON file (FR-01).",
    )
    parser.add_argument(
        "--style-sheet",
        type=Path,
        required=True,
        help="Path to the style sheet JSON file (FR-04).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=f"Output directory (default: {SYNTHESIZER_OUTPUT_DIR}).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help=f"Model identifier override (default: {SYNTHESIZER_MODEL}). DR-16.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=False,
        help="Resume from checkpoint (accepted but no-op in this sprint — completion_3).",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO).",
    )

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )

    logger = logging.getLogger("synthesizer")

    # Validate paths exist
    if not args.report_plan.exists():
        logger.error("Report plan file not found: %s", args.report_plan)
        return 1
    if not args.style_sheet.exists():
        logger.error("Style sheet file not found: %s", args.style_sheet)
        return 1

    try:
        from synthesizer.orchestrator.run import run

        # Attempt to load Stage 05 retriever
        retriever = None
        try:
            from pathlib import Path as _Path
            pipeline_dir = _Path(__file__).resolve().parent.parent / 'lit_review_pipeline'
            if pipeline_dir.is_dir() and str(pipeline_dir) not in sys.path:
                sys.path.insert(0, str(pipeline_dir))
            from synthesizer.retrieval.adapter import load_hybrid_retriever
            RetrieverClass = load_hybrid_retriever()
            if RetrieverClass is not None:
                retriever = RetrieverClass()
                print(f'RETRIEVER OK: {type(retriever)}', flush=True); logger.info('Stage 05 HybridRetriever loaded successfully.')
            else:
                print('RETRIEVER: Class was None', flush=True); logger.warning('HybridRetriever not available. Proceeding without retrieval.')
        except Exception as e:
            import traceback; print(f'RETRIEVER ERROR: {type(e).__name__}: {e}', flush=True); traceback.print_exc()

        run_state = run(
            report_plan_path=args.report_plan,
            style_sheet_path=args.style_sheet,
            output_dir=args.output_dir,
            model=args.model,
            resume=args.resume,
            retriever=retriever,
        )

        # Report summary
        finalized = sum(
            1 for ss in run_state.section_states.values()
            if ss.state.value == "finalized"
        )
        escalated = sum(
            1 for ss in run_state.section_states.values()
            if ss.state.value == "escalated"
        )
        logger.info(
            "Synthesis complete: %d finalized, %d escalated, %d total tokens.",
            finalized,
            escalated,
            run_state.cumulative_input_tokens + run_state.cumulative_output_tokens,
        )
        return 0

    except KeyboardInterrupt:
        logger.warning("Run interrupted by user.")
        return 130

    except Exception as exc:
        logger.error("Synthesis run failed: %s", exc, exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())