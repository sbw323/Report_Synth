from pathlib import Path
from synthesizer.loaders import load_style_sheet
import re

style = load_style_sheet(Path('/home/highview-home/Documents/Report_Synth_testrun/data/example_style_sheet.json'))
print(f'Tone register:    {style.tone_register}')
print(f'Citation pattern: {style.citation_pattern}')
print(f'Forbidden phrases ({len(style.forbidden_phrases)}):')
for fp in style.forbidden_phrases:
    print(f'  - \"{fp}\"')
print()

# Verify citation regex compiles and matches expected format
rx = re.compile(style.citation_pattern)
test_cases = [
    ('(Stare et al., 2007)', True),
    ('(Smith, 2020)',         True),
    ('Stare et al., 2007',   False),   # no parens
    ('(stare et al., 2007)', False),   # lowercase
]
print('Citation regex spot-check:')
for text, expect_match in test_cases:
    matched = rx.search(text) is not None
    status = 'PASS' if matched == expect_match else 'FAIL'
    print(f'  [{status}] \"{text}\" -> match={matched} (expected {expect_match})')
print()

print('Per-level constraints:')
for level, constraint in style.per_level_constraints.items():
    print(f'  Level {level}: {constraint.min_words}-{constraint.max_words} words, '
          f'heading: {constraint.heading_format}')
print()

print('Per-type overrides:')
for stype, overrides in style.per_type_overrides.items():
    print(f'  {stype}: {overrides}')
