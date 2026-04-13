from pathlib import Path
from synthesizer.loaders import load_report_plan
from synthesizer.dag import build_generation_dag, build_finalization_dag, iter_topological

plan = load_report_plan(Path('/home/highview-home/Documents/Report_Synth_testrun/data/example_report_plan.json'))

gen_dag = build_generation_dag(plan)
fin_dag = build_finalization_dag(plan)

print('=== Generation DAG (content edges only) ===')
print(f'Topological order: {iter_topological(gen_dag)}')
for sid in gen_dag.nodes:
    preds = gen_dag.predecessors(sid)
    succs = gen_dag.successors(sid)
    print(f'  {sid:30s}  preds={preds}  succs={succs}')

print()
print('=== Finalization DAG (content + reference edges) ===')
print(f'Topological order: {iter_topological(fin_dag)}')
for sid in fin_dag.nodes:
    preds = fin_dag.predecessors(sid)
    succs = fin_dag.successors(sid)
    print(f'  {sid:30s}  preds={preds}  succs={succs}')