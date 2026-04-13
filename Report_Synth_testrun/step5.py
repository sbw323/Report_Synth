import sys, json
sys.path.insert(0, 'lit_review_pipeline')

from pathlib import Path
from synthesizer.loaders import load_report_plan, load_style_sheet
from synthesizer.retrieval.adapter import retrieve_for_section, load_hybrid_retriever
from synthesizer.prompt.assembly import assemble_generation_prompt

plan  = load_report_plan(Path('/home/highview-home/Documents/Report_Synth_testrun/data/example_report_plan.json'))
style = load_style_sheet(Path('/home/highview-home/Documents/Report_Synth_testrun/data/example_style_sheet.json'))

RetrieverClass = load_hybrid_retriever()
if RetrieverClass is None:
    print("ERROR: Could not import HybridRetriever from 05_query.py")
    raise SystemExit(1)
retriever = RetrieverClass()

# Pick the first section (introduction — no upstream deps)
section = plan.sections[0]
print(f'Assembling prompt for: {section.section_id} ({section.section_type.value})')

# Retrieve evidence using the function-based API
result = retrieve_for_section(section, retriever)
print(f'Retrieved {len(result.chunks)} unique chunks across {len(result.queries_executed)} queries')

# Assemble (no upstream claim tables or abstracts for introduction)
prompt = assemble_generation_prompt(
    section=section,
    style=style,
    retrieved_chunks=result.chunks,
    upstream_claim_tables=None,
    upstream_summary_abstracts=None,
)

print(f'Section type:          {prompt.section_type.value}')
print(f'Expected output model: {prompt.expected_output_model_name}')
print(f'Max output tokens:     {prompt.max_output_tokens}')
print()
print(f'System prompt length:  {len(prompt.system_prompt)} chars')
print(f'User message length:   {len(prompt.user_message)} chars')
print()
print('--- System prompt (first 500 chars) ---')
print(prompt.system_prompt[:500])
print('...')
print()
print('--- User message (first 800 chars) ---')
print(prompt.user_message[:800])
print('...')