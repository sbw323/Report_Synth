import json
from pathlib import Path
from synthesizer.models.section_output import get_output_model
from synthesizer.models.enums import SectionType

draft_path = Path('data/synthesis/sections/introduction/draft_v1.md')
raw = draft_path.read_text(encoding='utf-8')

# Strip markdown fences if present
if raw.startswith('```'):
    raw = raw.split('\n', 1)[1].rsplit('```', 1)[0]

try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    print(f'LAYER 1 FAIL — not valid JSON: {e}')
    print(f'First 200 chars of raw content:')
    print(repr(raw[:200]))
    raise SystemExit(1)

OutputModel = get_output_model(SectionType.NARRATIVE_SYNTHESIS)
print(f'Validating against: {OutputModel.__name__}')

try:
    output = OutputModel.model_validate(data)
    print('LAYER 1 PASS — structural validation succeeded')
    print(f'  section_id:              {output.section_id}')
    print(f'  content_markdown length: {len(output.content_markdown)} chars')
    print(f'  heading_level:           {output.heading_level}')
    print(f'  word_count:              {output.word_count}')
    print(f'  themes_addressed:        {output.themes_addressed}')
    print(f'  cross_references:        {output.cross_references}')
    print(f'  metadata keys:           {list(output.metadata.keys())}')
except Exception as e:
    print(f'LAYER 1 FAIL — schema validation error:')
    print(e)