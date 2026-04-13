from synthesizer.models.enums import SectionLifecycleState
from synthesizer.models.state import SectionState
from synthesizer.dag import build_generation_dag, build_finalization_dag
from synthesizer.loaders import load_report_plan
from synthesizer.orchestrator.lifecycle import (
    check_generation_prerequisites,
    check_finalization_prerequisites,
)
from pathlib import Path

plan = load_report_plan(Path('/home/highview-home/Documents/Report_Synth_testrun/data/example_report_plan.json'))
gen_dag = build_generation_dag(plan)
fin_dag = build_finalization_dag(plan)

# Simulate section states
states = {}
for s in plan.sections:
    states[s.section_id] = SectionState(
        section_id=s.section_id,
        state=SectionLifecycleState.QUEUED,
    )

# Check: introduction should be ready to generate (no content deps)
can_gen_intro = check_generation_prerequisites('introduction', states, gen_dag)
print(f'introduction can generate (no deps):     {can_gen_intro}')  # True

# Check: methodology_comparison should NOT be ready (needs control_strategies)
can_gen_meth = check_generation_prerequisites('methodology_comparison', states, gen_dag)
print(f'methodology_comparison can generate:      {can_gen_meth}')  # False

# Simulate: finalize introduction and control_strategies
states['introduction'].state = SectionLifecycleState.FINALIZED
states['control_strategies'].state = SectionLifecycleState.FINALIZED

can_gen_meth2 = check_generation_prerequisites('methodology_comparison', states, gen_dag)
print(f'methodology_comparison can generate now:  {can_gen_meth2}')  # True

# Check finalization of cross_cutting_findings (needs methodology_comparison ref dep)
states['economic_analysis'].state = SectionLifecycleState.FINALIZED
can_fin_ccf = check_finalization_prerequisites('cross_cutting_findings', states, fin_dag)
print(f'cross_cutting_findings can finalize:      {can_fin_ccf}')  # False (meth not finalized)

states['methodology_comparison'].state = SectionLifecycleState.FINALIZED
can_fin_ccf2 = check_finalization_prerequisites('cross_cutting_findings', states, fin_dag)
print(f'cross_cutting_findings can finalize now:  {can_fin_ccf2}')  # True