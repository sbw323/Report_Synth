import sys, json
sys.path.insert(0, 'lit_review_pipeline')

from pathlib import Path
from anthropic import Anthropic
from synthesizer.loaders import load_report_plan, load_style_sheet
from synthesizer.retrieval.adapter import retrieve_for_section, load_hybrid_retriever
from synthesizer.prompt.assembly import assemble_generation_prompt
from synthesizer.config import SYNTHESIZER_MODEL

plan  = load_report_plan(Path('/home/highview-home/Documents/Report_Synth_testrun/data/example_report_plan.json'))
style = load_style_sheet(Path('/home/highview-home/Documents/Report_Synth_testrun/data/example_style_sheet.json'))

RetrieverClass = load_hybrid_retriever()
if RetrieverClass is None:
    print("ERROR: Could not import HybridRetriever from 05_query.py")
    raise SystemExit(1)
retriever = RetrieverClass()
client = Anthropic()

section = plan.sections[0]  # introduction

# Retrieve
result = retrieve_for_section(section, retriever)

# Assemble prompt
prompt = assemble_generation_prompt(
    section=section,
    style=style,
    retrieved_chunks=result.chunks,
)

print(f'Calling {SYNTHESIZER_MODEL} for section: {section.section_id}')
print(f'Prompt tokens (approx): system={len(prompt.system_prompt)//4}, '
      f'user={len(prompt.user_message)//4}')

# LLM call
response = client.messages.create(
    model=SYNTHESIZER_MODEL,
    max_tokens=prompt.max_output_tokens,
    system=prompt.system_prompt,
    messages=[{'role': 'user', 'content': prompt.user_message}],
)

raw_text = response.content[0].text
print(f'Response length: {len(raw_text)} chars')
print(f'Stop reason:     {response.stop_reason}')
print(f'Input tokens:    {response.usage.input_tokens}')
print(f'Output tokens:   {response.usage.output_tokens}')
print()

# Attempt JSON parse (Layer 1 precursor)
try:
    parsed = json.loads(raw_text)
    print('JSON parse: SUCCESS')
    print(f'Top-level keys: {list(parsed.keys())}')
    if 'content_markdown' in parsed:
        wc = len(parsed['content_markdown'].split())
        print(f'content_markdown word count: {wc}')
    if 'heading_level' in parsed:
        print(f'heading_level: {parsed["heading_level"]}')
except json.JSONDecodeError as e:
    print(f'JSON parse: FAILED — {e}')
    print('Raw output (first 500 chars):')
    print(raw_text[:500])

# Save raw output for downstream steps
output_dir = Path('data/synthesis/sections/introduction')
output_dir.mkdir(parents=True, exist_ok=True)
draft_path = output_dir / 'draft_v1.md'
draft_path.write_text(raw_text, encoding='utf-8')
print(f'Draft saved to: {draft_path}')