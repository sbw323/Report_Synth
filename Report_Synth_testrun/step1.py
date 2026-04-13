from pathlib import Path
from synthesizer.loaders import load_report_plan
from synthesizer.validation.graph_validation import build_generation_dag

# --- 1a. Load + validate ---
plan = load_report_plan(Path('/home/highview-home/Documents/Report_Synth_testrun/data/example_report_plan.json'))
print(f'Plan loaded: {plan.plan_id}  v{plan.version}')
print(f'Title:       {plan.title}')
print(f'Sections:    {len(plan.sections)}')
print()

for s in plan.sections:
    deps = [(e.target_section_id, e.kind.value) for e in s.dependency_edges]
    print(f'  {s.section_id:30s}  type={s.section_type.value:25s}  '
          f'depth={s.depth_level}  deps={deps}')

# --- 1b. Build generation DAG ---
dag = build_generation_dag(plan)
print()
print(f'Generation DAG topological order:')
for i, sid in enumerate(dag.topological_order, 1):
    print(f'  {i}. {sid}')
print(f'Content edges: {len(dag.edges)}')