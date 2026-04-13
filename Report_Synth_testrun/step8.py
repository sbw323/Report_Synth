import json, re
from pathlib import Path
from synthesizer.loaders import load_report_plan, load_style_sheet
from synthesizer.models.section_output import get_output_model
from synthesizer.models.enums import SectionType

plan  = load_report_plan(Path('/home/highview-home/Documents/Report_Synth_testrun/data/example_report_plan.json'))
style = load_style_sheet(Path('/home/highview-home/Documents/Report_Synth_testrun/data/example_style_sheet.json'))
section = plan.sections[0]  # introduction, depth_level=0

draft_path = Path('data/synthesis/sections/introduction/draft_v1.md')
raw = draft_path.read_text(encoding='utf-8')
if raw.startswith('```'):
    raw = raw.split('\n', 1)[1].rsplit('```', 1)[0]
data = json.loads(raw)
OutputModel = get_output_model(SectionType.NARRATIVE_SYNTHESIS)
output = OutputModel.model_validate(data)

violations = []

# --- Check 1: Word count ---
level_key = str(section.depth_level)
constraints = style.per_level_constraints.get(level_key)
type_override = style.per_type_overrides.get(section.section_type.value, {})

min_w = type_override.get('min_words', constraints.min_words if constraints else 0)
max_w = type_override.get('max_words', constraints.max_words if constraints else 99999)
actual_wc = len(output.content_markdown.split())

if actual_wc < min_w:
    violations.append(f'Word count {actual_wc} < min {min_w}')
elif actual_wc > max_w:
    violations.append(f'Word count {actual_wc} > max {max_w}')
else:
    print(f'[PASS] Word count: {actual_wc} (range {min_w}-{max_w})')

# --- Check 2: Heading level ---
expected_heading = constraints.heading_format if constraints else '##'
heading_str = '#' * output.heading_level
if heading_str == expected_heading:
    print(f'[PASS] Heading level: {heading_str} == {expected_heading}')
else:
    violations.append(f'Heading {heading_str} != expected {expected_heading}')

# --- Check 3: Citation format ---
citation_rx = re.compile(style.citation_pattern)
year_parens = re.findall(r'\([^)]*\d{4}[^)]*\)', output.content_markdown)
bad_cites = [c for c in year_parens if not citation_rx.search(c)]
if bad_cites:
    violations.append(f'Bad citations: {bad_cites}')
else:
    print(f'[PASS] Citation format: {len(year_parens)} citation(s) match pattern')

# --- Check 4: Forbidden phrases ---
content_lower = output.content_markdown.lower()
found_forbidden = [fp for fp in style.forbidden_phrases if fp.lower() in content_lower]
if found_forbidden:
    violations.append(f'Forbidden phrases found: {found_forbidden}')
else:
    print(f'[PASS] No forbidden phrases detected')

# --- Check 5: Equation delimiters ---
non_standard = []
if r'\[' in output.content_markdown or r'\]' in output.content_markdown:
    non_standard.append(r'\[...\]')
if r'\begin{equation}' in output.content_markdown:
    non_standard.append(r'\begin{equation}')
if non_standard:
    violations.append(f'Non-standard equation delimiters: {non_standard}')
else:
    print(f'[PASS] Equation delimiters OK (or none present)')

print()
if violations:
    print(f'LAYER 2 RESULT: FAIL — {len(violations)} violation(s)')
    for v in violations:
        print(f'  ERROR: {v}')
else:
    print('LAYER 2 RESULT: PASS — all style checks satisfied')