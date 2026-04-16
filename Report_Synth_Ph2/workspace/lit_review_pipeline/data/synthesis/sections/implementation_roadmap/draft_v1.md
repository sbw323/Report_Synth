## File-by-File Julia Implementation Roadmap

This section synthesizes the scenario component inventory, decision matrix, and objective specification from the upstream analysis into a concrete set of `.jl` files that the agent must author. Each file's responsibilities, inputs, outputs, and inter-file dependencies are stated explicitly, grounded in the REopt.jl API patterns documented in the evidence base.

### 1. `utils_to_dict.jl` — Recursive Type Conversion Utilities

**Responsibility.** Provide two shared utility functions: `to_dict(obj)` and `make_serializable(d::Dict)`. The first recursively converts `JSON.Object` instances returned by `JSON.parsefile` into native Julia `Dict{String,Any}` structures, addressing the documented requirement that REopt internals expect native dictionary types rather than `JSON.Object` wrappers (REopt API Wiki, 2024). The second traverses a results dictionary and converts every `JuMP.Containers.DenseAxisArray` to a standard `Array`, enabling downstream `JSON.print` serialization (REopt.jl Documentation, 2024).

**Inputs.** Any nested `JSON.Object` or results `Dict` containing non-serializable JuMP container types.

**Outputs.** Clean `Dict{String,Any}` structures suitable for REopt scenario construction or JSON export.

**Dependencies.** Requires `import JSON` and `import JuMP`. This file is consumed by all other files via `include("utils_to_dict.jl")`.

### 2. `scenario_builder.jl` — Scenario Ingestion, Override, and Validation

**Responsibility.** Read the baseline `reopt_wwtp_scenario.json` produced by the upstream MATLAB stage (`compute_voll_for_reopt.m`), apply programmatic overrides to selected fields, and validate the resulting dictionary against REopt.jl field expectations. The override mechanism must support at minimum the following keys: `Financial.value_of_lost_load_per_kwh` (scalar or 8760-element vector per upstream claim_33), `ElectricUtility.outage_durations`, `ElectricUtility.outage_start_time_steps`, and `ElectricUtility.outage_probabilities`. Validation should confirm field types, min/max bounds, and time-series length alignment with `Settings.time_steps_per_hour`, mirroring the `InputValidator.clean_fields()` and `cross_clean()` logic documented in the Django v3 API architecture (REopt API Wiki, 2024).

**Inputs.** Path to `reopt_wwtp_scenario.json`; a keyword-argument dictionary of overrides.

**Outputs.** A validated `Dict{String,Any}` scenario dictionary ready for `run_reopt`.

**Dependencies.** Calls `to_dict` from `utils_to_dict.jl`. Consumed by `run_wwdr.jl`, `run_voll_sweep.jl`, and `run_outage_sweep.jl`.

**Exported function signature:**
```julia
function build_scenario(json_path::String; overrides::Dict=Dict()) -> Dict{String,Any}
```

### 3. `dr_revenue_model.jl` — ISO Demand Response Capacity Revenue Post-Processor

**Responsibility.** Compute ISO DR capacity revenue from solved DER capacities using an input capacity-payment rate $r_{\text{DR}}$ in dollars per kW-month. Per upstream claim_15, ISO DR revenue is not native to the REopt objective but is computed in post-processing from the solved `ElectricStorage.size_kw` and `Generator.size_kw` values. The function extracts these capacities from the results dictionary, applies the payment rate over the 12-month annual cycle, and returns a revenue line-item dictionary for inclusion in the NPV decomposition report.

**Revenue computation:**

$$R_{\text{DR}} = r_{\text{DR}} \times \left( P_{\text{batt}} + P_{\text{gen}} \right) \times 12$$

where $P_{\text{batt}}$ is `ElectricStorage.size_kw` and $P_{\text{gen}}$ is `Generator.size_kw` from the results dictionary.

**Inputs.** Results `Dict` from `run_reopt`; scalar `capacity_payment_per_kw_month::Float64`; `Financial.analysis_years` and `Financial.offtaker_discount_rate_fraction` for present-worth discounting.

**Outputs.** A `Dict` containing `annual_dr_revenue`, `lifecycle_dr_revenue_pv`, and the adjusted NPV that adds DR revenue to the baseline $\text{NPV} = \text{LCC}_{\text{BAU}} - \text{LCC}_{\text{Optimal}}$ (upstream claim_16).

**Dependencies.** None beyond standard library. Consumed by `run_wwdr.jl` and `postprocess.jl`.

**Open decision point 1:** Whether the ISO capacity commitment should enforce a floor constraint on `ElectricStorage.size_kw` (e.g., `min_kw >= committed_capacity`) as a JuMP constraint added before calling `run_reopt`. Doing so would depart from pure post-processing and would require `dr_revenue_model.jl` to expose a pre-solve constraint-injection function in addition to the post-solve revenue calculator. The tradeoff is between fidelity to the DR program's firm capacity obligation and the simplicity of treating DR revenue as an exogenous adder.

### 4. `run_wwdr.jl` — Primary Driver Script

**Responsibility.** Orchestrate the full WWTP wastewater demand response analysis. This script instantiates two `JuMP.Model` instances for the BAU comparison pattern documented in the v3 architecture, where BAU and optimal scenarios run in parallel within the Julia process (upstream claim_30). It calls `build_scenario` from `scenario_builder.jl`, invokes the two-model `run_reopt(m1, m2, scenario_dict)` signature (upstream claim_29), applies `make_serializable` from `utils_to_dict.jl`, computes DR revenue via `dr_revenue_model.jl`, and writes the combined results JSON plus the adjusted NPV.

**Execution flow:**
1. `include("utils_to_dict.jl")`
2. `include("scenario_builder.jl")`
3. `include("dr_revenue_model.jl")`
4. `scenario = build_scenario("reopt_wwtp_scenario.json")`
5. `m1 = Model(HiGHS.Optimizer); m2 = Model(HiGHS.Optimizer)` with `set_attribute(m, "time_limit", 600.0)` per upstream claim_27
6. `results = run_reopt(m1, m2, scenario)`
7. `results = make_serializable(results)`
8. `dr = compute_dr_revenue(results; capacity_payment_per_kw_month=X)`
9. Merge `dr` into `results["Financial"]`
10. `open(io -> JSON.print(io, results, 2), "results_wwdr.json", "w")`

**Inputs.** `reopt_wwtp_scenario.json` on disk; solver configuration parameters.

**Outputs.** `results_wwdr.json` containing full REopt results plus DR revenue line items and adjusted NPV.

**Dependencies.** `utils_to_dict.jl`, `scenario_builder.jl`, `dr_revenue_model.jl`; packages `REopt`, `JuMP`, `HiGHS`, `JSON`.

### 5. `run_voll_sweep.jl` — Parametric VoLL Sensitivity Sweep

**Responsibility.** Execute a parametric sweep over VoLL scalar multipliers ranging from $0.1\times$ to $10\times$ the marginal VoLL baseline. Each iteration follows the `deepcopy`-override-solve-collect pattern (upstream claim_34): deep-copy the base scenario, override `Financial.value_of_lost_load_per_kwh`, instantiate a fresh solver model per iteration, execute using the two-model signature, and serialize results. VoLL may be a scalar or an 8760-element vector (upstream claim_33); the multiplier scales whichever form is present.

**Sweep grid:** `multipliers = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 7.5, 10.0]`

**Inputs.** Base scenario JSON path; VoLL multiplier array.

**Outputs.** Directory of per-multiplier result JSONs plus a summary CSV mapping multiplier to NPV, `ElectricStorage.size_kw`, `ElectricStorage.size_kwh`, `Generator.size_kw`, and expected outage cost.

**Dependencies.** `utils_to_dict.jl`, `scenario_builder.jl`, `dr_revenue_model.jl`.

**Open decision point 2:** The hourly VoLL profile's time-varying magnitude creates an asymmetry with the coarser `outage_durations` scenario granularity. When a VoLL vector is scaled by a uniform multiplier, the relative weighting across hours is preserved, but the interaction with discrete outage duration bins may produce non-monotonic expected-outage-cost responses. The implementer must decide whether to (a) retain uniform multiplier scaling, (b) apply duration-weighted averaging of the VoLL vector to match the outage granularity, or (c) construct duration-specific VoLL sub-vectors that align with each `outage_durations` entry.

### 6. `run_outage_sweep.jl` — Outage Duration and Probability Sweep

**Responsibility.** Execute a parametric sweep over `outage_durations` and `outage_probabilities` scenarios. The stochastic outage formulation evaluates resilience across a combinatorial grid of start times and durations, each weighted by probability (upstream claim_22). This script varies the duration vector (e.g., `[4, 8, 16, 24, 48, 72, 168]` hours) and the associated probability weights.

**Inputs.** Base scenario JSON path; arrays of outage duration vectors and corresponding probability vectors.

**Outputs.** Per-scenario result JSONs; summary CSV mapping scenario parameters to NPV, DER sizes, `expected_outage_cost`, `resilience_hours_min`, `resilience_hours_avg`, and `probs_of_surviving` (REopt.jl Methods Documentation, 2024).

**Dependencies.** `utils_to_dict.jl`, `scenario_builder.jl`.

**Open decision point 3:** Whether seasonal outage probability weighting should replace the default uniform weighting. REopt's `outage_probabilities` input accepts a vector aligned with `outage_durations`, but seasonal variation (e.g., higher storm probability in summer, higher ice-storm probability in winter) would require constructing month-specific probability distributions and potentially running separate optimizations per season. The implementer must decide between (a) a single annual probability vector, (b) a monthly-weighted composite probability, or (c) a seasonal decomposition that solves multiple scenarios and aggregates expected costs.

### 7. `postprocess.jl` — NPV Decomposition, DER Sizing Summary, and Resilience Metrics

**Responsibility.** Consume the results JSON(s) produced by the driver scripts and generate three report artifacts:

1. **NPV decomposition** into component terms: capital expenditure (net of ITC and MACRS per upstream claim_13), O&M lifecycle costs (upstream claim_6), grid energy and demand charges (upstream claim_7), fuel costs (upstream claim_8), export revenues (upstream claim_11), production incentives (upstream claim_12), battery replacement or augmentation costs (upstream claim_5), battery residual value (upstream claim_14), expected outage costs (upstream claim_10), and DR capacity revenue from `dr_revenue_model.jl`. The decomposition must satisfy the identity:

$$\text{NPV}_{\text{adjusted}} = \text{LCC}_{\text{BAU}} - \text{LCC}_{\text{Optimal}} + R_{\text{DR,lifecycle}}$$

2. **DER sizing summary** table: `PV.size_kw`, `ElectricStorage.size_kw`, `ElectricStorage.size_kwh`, `Generator.size_kw`, and any CHP or thermal storage capacities.

3. **Resilience metrics report**: `resilience_hours_min`, `resilience_hours_max`, `resilience_hours_avg`, `probs_of_surviving`, and `probs_of_surviving_by_month` as returned by `simulate_outages` (REopt.jl Methods Documentation, 2024).

**Inputs.** One or more results JSON files.

**Outputs.** Markdown-formatted report; CSV summary tables.

**Dependencies.** `dr_revenue_model.jl` for revenue recalculation if needed.

### Inter-File Dependency Graph

```
utils_to_dict.jl
    <- scenario_builder.jl
        <- run_wwdr.jl
        <- run_voll_sweep.jl
        <- run_outage_sweep.jl
    <- run_wwdr.jl (make_serializable)

dr_revenue_model.jl
    <- run_wwdr.jl
    <- run_voll_sweep.jl
    <- postprocess.jl

postprocess.jl (terminal; no downstream consumers)
```

### Summary of Open Decision Points

| # | Question | Design Alternatives |
|---|----------|--------------------|
| 1 | Should ISO capacity commitment enforce a `min_kw` floor on `ElectricStorage.size_kw` as a JuMP constraint? | (a) Pure post-processing adder; (b) Pre-solve constraint injection via `set_lower_bound` |
| 2 | How to reconcile hourly VoLL vector granularity with coarser `outage_durations` bins? | (a) Uniform scalar multiplier; (b) Duration-weighted VoLL averaging; (c) Duration-specific sub-vectors |
| 3 | Should seasonal outage probability weighting replace uniform weighting? | (a) Single annual vector; (b) Monthly-weighted composite; (c) Seasonal decomposition with scenario aggregation |

These decision points should be resolved by the implementing author based on the specific ISO program rules, WWTP operational context, and computational budget available for the parametric sweeps.