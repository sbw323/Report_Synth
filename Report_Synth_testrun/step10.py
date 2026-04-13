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

response = client.messages.create(
    model=SYNTHESIZER_MODEL,
    max_tokens=200,
    system=(
        'You are a scientific summarizer. Produce a concise 2-3 sentence '
        'summary abstract of the section below. Stay within 50-100 words. '
        'Use formal academic tone. No citations. Return ONLY the summary text.'
    ),
    messages=[{'role': 'user', 'content': content}],
)

abstract = response.content[0].text.strip()
wc = len(abstract.split())
print(f'Summary abstract ({wc} words):')
print(f'  {abstract}')
print()
if 50 <= wc <= 100:
    print('[PASS] Word count within 50-100 range')
else:
    print(f'[WARN] Word count {wc} outside 50-100 target')