import sys
sys.path.insert(0, 'lit_review_pipeline')

from pathlib import Path
from synthesizer.loaders import load_report_plan
from synthesizer.retrieval.adapter import (
    retrieve_for_section,
    load_hybrid_retriever,
)

plan = load_report_plan(Path('/home/highview-home/Documents/Report_Synth_testrun/data/example_report_plan.json'))
section = plan.sections[0]  # introduction

# Load the real Stage 05 retriever
RetrieverClass = load_hybrid_retriever()
if RetrieverClass is None:
    print("ERROR: Could not import HybridRetriever from 05_query.py")
    print("Check that lit_review_pipeline/ is on sys.path and 05_query.py exists.")
    raise SystemExit(1)

retriever = RetrieverClass()
print(f"HybridRetriever loaded: {type(retriever).__name__}")

# Execute retrieval for the introduction section
result = retrieve_for_section(section, retriever)
print(f"Section:          {result.section_id}")
print(f"Queries executed: {result.queries_executed}")
print(f"Chunks returned:  {len(result.chunks)}")
print()

for i, chunk in enumerate(result.chunks[:3]):
    print(f"  Chunk {i+1}:")
    print(f"    ID:         {chunk.id}")
    print(f"    RRF score:  {chunk.rrf_score:.4f}")
    print(f"    Method:     {chunk.method}")
    print(f"    Text:       {chunk.text[:100]}...")
    print()

print("answer_text discarded (FR-10) — not present on RetrievalResult.")