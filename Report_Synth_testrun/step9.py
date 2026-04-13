import sys, json
sys.path.insert(0, 'lit_review_pipeline')

from pathlib import Path
from anthropic import Anthropic
from synthesizer.config import SYNTHESIZER_MODEL

client = Anthropic()

draft_path = Path('data/synthesis/sections/introduction/draft_v1.md')
raw = draft_path.read_text(encoding='utf-8')
if raw.startswith('```'):
    raw = raw.split('\n', 1)[1].rsplit('```', 1)[0]
data = json.loads(raw)
content = data.get('content_markdown', '')

system_prompt = (
    'You are a claim extractor for a scientific literature review.\n'
    'Extract the key factual claims from the section text below.\n\n'
    'Return a JSON object with this structure:\n'
    '{\n'
    '  "claims": [\n'
    '    {\n'
    '      "claim_id": "claim_001",\n'
    '      "claim_text": "The claim statement.",\n'
    '      "source_chunk_ids": ["chunk_id_1"],\n'
    '      "confidence_tag": "directly_stated | inferred | synthesized"\n'
    '    }\n'
    '  ]\n'
    '}\n\n'
    'Rules:\n'
    '- Every claim must be traceable to at least one source chunk ID referenced in the text.\n'
    '- Use confidence tags accurately: directly_stated, inferred, or synthesized.\n'
    '- Extract 3-8 claims that capture the sections key assertions.\n'
    '- Return ONLY valid JSON, no markdown fences.'
)

response = client.messages.create(
    model=SYNTHESIZER_MODEL,
    max_tokens=2000,
    system=system_prompt,
    messages=[{'role': 'user', 'content': f'Section text:\n\n{content}'}],
)

claim_text = response.content[0].text
print(f'Claim extraction response: {len(claim_text)} chars')

try:
    claims = json.loads(claim_text)
    n = len(claims.get('claims', []))
    print(f'Extracted {n} claims:')
    for c in claims['claims']:
        tag = c.get('confidence_tag', '?')
        cid = c.get('claim_id', '?')
        txt = c.get('claim_text', '')[:80]
        print(f'  [{tag:17s}] {cid}: {txt}...')

    # Save claim table
    ct_path = Path('data/synthesis/sections/introduction/claim_table_v1.json')
    ct_path.write_text(json.dumps(claims, indent=2), encoding='utf-8')
    print(f'Claim table saved to: {ct_path}')
except json.JSONDecodeError as e:
    print(f'Claim extraction JSON parse FAILED: {e}')
    print(claim_text[:500])