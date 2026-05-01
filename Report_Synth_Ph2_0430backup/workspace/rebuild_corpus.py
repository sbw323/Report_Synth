#!/usr/bin/env python3
"""
Rebuild the corpus pipeline for a new set of PDFs.

Cleans stale artifacts from prior runs, then executes stages 01–04
of the lit_review_pipeline in sequence:

    01_ingest  → manifest.json
    02_parse   → *_merged.md per paper
    03_chunk   → *_chunks.json + all_chunks.json
    04_index   → ChromaDB collection + BM25 index

Run from the project root:

    python3 rebuild_corpus.py

Prerequisites:
    - New PDFs are already in lit_review_pipeline/data/pdfs/
    - ANTHROPIC_API_KEY is set (stage 02 needs it for equation handling)
    - Python dependencies installed per lit_review_pipeline/requirements.txt
"""

import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
PIPELINE_DIR = PROJECT_ROOT / "lit_review_pipeline"
PIPELINE_DATA = PIPELINE_DIR / "data"

# Stale root-level duplicates (safe to remove)
ROOT_DATA = PROJECT_ROOT / "data"
ROOT_VECTORSTORE = PROJECT_ROOT / "vectorstore"

# Pipeline artifacts that must be rebuilt
PARSED_DIR = PIPELINE_DATA / "parsed"
VECTORSTORE_DIR = PIPELINE_DIR / "vectorstore"
SUMMARIES_DIR = PIPELINE_DATA / "summaries"
SYNTHESIS_DIR = PIPELINE_DATA / "synthesis"
MANIFEST = PIPELINE_DATA / "manifest.json"

STAGES = ["01_ingest.py", "02_parse.py", "03_chunk.py", "04_index.py"]


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

def clean_stale_artifacts():
    """Remove artifacts from prior runs so the pipeline rebuilds from scratch."""

    # 1. Root-level duplicates
    for stale in (ROOT_DATA, ROOT_VECTORSTORE):
        if stale.exists():
            print(f"  Removing stale root-level copy: {stale}")
            shutil.rmtree(stale)

    # 2. Old parsed files and chunks (but NOT the pdfs/ directory)
    if PARSED_DIR.exists():
        print(f"  Clearing parsed artifacts:      {PARSED_DIR}")
        shutil.rmtree(PARSED_DIR)
    PARSED_DIR.mkdir(parents=True, exist_ok=True)

    # 3. Old vectorstore
    if VECTORSTORE_DIR.exists():
        print(f"  Clearing vectorstore:           {VECTORSTORE_DIR}")
        shutil.rmtree(VECTORSTORE_DIR)
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    # 4. Old manifest
    if MANIFEST.exists():
        print(f"  Removing old manifest:          {MANIFEST}")
        MANIFEST.unlink()

    # 5. Old synthesis output (will be invalid against new corpus)
    if SYNTHESIS_DIR.exists():
        print(f"  Clearing old synthesis output:  {SYNTHESIS_DIR}")
        shutil.rmtree(SYNTHESIS_DIR)

    # 6. Old summaries (stage 06 output, will be stale)
    if SUMMARIES_DIR.exists():
        print(f"  Clearing old summaries:         {SUMMARIES_DIR}")
        shutil.rmtree(SUMMARIES_DIR)
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------

def run_stage(script_name: str):
    """Run a single pipeline stage as a subprocess from lit_review_pipeline/."""
    script_path = PIPELINE_DIR / script_name
    if not script_path.exists():
        print(f"  ERROR: {script_path} not found — skipping")
        return False

    print(f"\n{'='*60}")
    print(f"  Running {script_name}")
    print(f"{'='*60}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(PIPELINE_DIR),
        capture_output=False,       # let output stream to terminal
    )

    if result.returncode != 0:
        print(f"\n  FAILED: {script_name} exited with code {result.returncode}")
        return False

    print(f"  OK: {script_name} completed")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Confirm PDFs exist
    pdf_dir = PIPELINE_DATA / "pdfs"
    pdfs = list(pdf_dir.glob("*.pdf")) if pdf_dir.exists() else []
    if not pdfs:
        print(f"No PDFs found in {pdf_dir}")
        print("Add your source PDFs there before running this script.")
        sys.exit(1)

    print(f"Found {len(pdfs)} PDFs in {pdf_dir}:")
    for p in sorted(pdfs):
        print(f"  - {p.name}")

    # Clean
    print(f"\nCleaning stale artifacts...")
    clean_stale_artifacts()
    print("Done.\n")

    # Run stages 01–04
    for stage in STAGES:
        success = run_stage(stage)
        if not success:
            print(f"\nPipeline halted at {stage}.")
            print("Fix the error above, then re-run this script.")
            sys.exit(1)

    # Summary
    print(f"\n{'='*60}")
    print("  Corpus rebuild complete")
    print(f"{'='*60}")

    chunks_file = PARSED_DIR / "all_chunks.json"
    chroma_db = VECTORSTORE_DIR / "chroma.sqlite3"
    bm25_index = VECTORSTORE_DIR / "bm25_index.pkl"

    for artifact, label in [
        (MANIFEST,     "Manifest"),
        (chunks_file,  "Chunks"),
        (chroma_db,    "ChromaDB"),
        (bm25_index,   "BM25 index"),
    ]:
        status = "OK" if artifact.exists() else "MISSING"
        size = f"({artifact.stat().st_size:,} bytes)" if artifact.exists() else ""
        print(f"  {label:12s}: {status} {size}")

    print(f"\nThe vectorstore is ready. You can now run the synthesizer")
    print(f"with your new report plan.")


if __name__ == "__main__":
    main()
    print(f"Script file:    {Path(__file__).resolve()}")
    print(f"Project root:   {PROJECT_ROOT}")
    print(f"Invocation cwd: {Path.cwd()}")
    print(f"PDF directory:  {pdf_dir}")