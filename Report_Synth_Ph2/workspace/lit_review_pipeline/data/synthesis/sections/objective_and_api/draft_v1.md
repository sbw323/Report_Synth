## Multi-Term NPV Objective Function and REopt.jl API Surface

REopt.jl formulates distributed energy resource (DER) sizing and dispatch as a single-objective mixed-integer linear program (MILP) whose scalar objective minimizes the life-cycle cost (LCC) of energy over a user-specified analysis horizon. Because the net present value (NPV) is defined as the difference between the business-as-usual (BAU) LCC and the optimized-case LCC, minimizing LCC and maximizing NPV are algebraically equivalent; no Pareto multi-objective frontier is constructed (REopt User Manual, 2024). The subsections below formalize the additive cost and benefit terms that compose this objective, specify the minimax structure of the expected outage cost term, and catalog the Julia API calls required to execute and post-process an optimization.

### Additive Cost Terms in the Objective Function

The objective function assembles the following additive cost terms, each discounted to present value using the off-taker's nominal discount rate over `analysis_years` (default 25 years) (REopt User Manual, 2024):

1. **Capital expenditure (CAPEX).** For each technology $t$ in subdivision $k$, segment $s$, the capital cost is represented by a piecewise-linear function with slope $c^{cm}_{ts}$ [\$/kW] and intercept $c^{cb}_{ts}$ [\$]. Storage systems contribute two independent terms: $c^{kW}_b$ [\$/kW] for power capacity and $c^{kWh}_b$ [\$/kWh] for energy capacity (REopt Mathematical Formulation, Appendix D). Battery replacement or augmentation costs $C_{\text{repl}}$ or $C_{\text{aug}}$ are added to the objective when `model_degradation` is enabled (REopt.jl Documentation, Inputs).

2. **Operations and maintenance (O\&M).** Both fixed O\&M per unit of power rating ($c^{om\sigma}_t$ [\$/kW], which includes standby charges for CHP) and variable O\&M per unit of production ($c^{omp}_t$ [\$/kWh]) are discounted over the analysis period using the present worth factor $f_{om}$ (REopt Mathematical Formulation, Appendix D).

3. **Grid energy procurement.** Electricity purchases are valued at time-of-use energy prices $c^{g}_{uh}$ [\$/kWh] across tiered demand structures. Demand charges enter via monthly peak demand tiers ($c^{rm}_{mn}$ [\$/kW]) and time-of-use demand periods ($c^{r}_{de}$ [\$/kW]), with ratchet provisions over look-back months (REopt Mathematical Formulation, Appendix D). Fuel costs for on-site generation enter at $c^{u}_f$ [\$/MMBTU] discounted by technology-specific present worth factors $f^{pf}_t$.

4. **Emissions costs.** When enabled, marginal costs of pollutant $p$ from on-site fuel burn ($c^{f}_p$ [\$/ton]) and from grid-purchased electricity ($\bar{c}^{g}_p$ [\$/ton]) are included, each with their own present worth factors $f^{fc}_p$ and $f^{gc}_p$ (REopt Mathematical Formulation, Appendix D).

5. **Expected outage cost.** Weighted by `value_of_lost_load_per_kwh` (VoLL) and `outage_probabilities`, this term penalizes unserved energy during stochastic outage scenarios. Its structure is detailed below.

Benefit terms that enter the objective natively (i.e., are subtracted from cost) include:

- **Energy export revenues** at rates $c^{e}_{uh}$ [\$/kWh] across net-metering and wholesale tiers.
- **Production incentives** $X^{pi}_t$ [\$], bounded by technology-specific caps $\bar{\imath}_t$ and power limits $\bar{\imath}^{\sigma}_t$ (REopt Mathematical Formulation, Appendix D).
- **Investment Tax Credit (ITC)** and **Modified Accelerated Cost Recovery System (MACRS)** depreciation benefits. The ITC reduces CAPEX directly (e.g., 30% for PV and storage meeting prevailing wage requirements), while MACRS bonus depreciation (up to 100% first-year under current law) reduces the depreciation basis by half the ITC value (REopt User Manual, 2024). Both are embedded in the present-value capital cost computation within the objective.
- **Battery residual value** $C_{\text{residual}}$, computed as the present worth of remaining useful life at the end of the analysis period, is subtracted from total cost (REopt.jl Documentation, Inputs).

Revenue streams that are **not** native to the objective but are computed in post-processing include ISO demand response (DR) capacity revenue. This value is derived from the solved `ElectricStorage.size_kw` and `Generator.size_kw` capacities after the optimization terminates, and is reported as an ancillary economic metric rather than influencing DER sizing directly (REopt User Manual, 2024).

### NPV Computation via BAU Comparison

NPV is calculated as:

$$\text{NPV} = \text{LCC}_{\text{BAU}} - \text{LCC}_{\text{Optimal}}$$

The BAU case includes only utility demand and energy costs, existing boiler fuel costs, and O\&M for any existing PV or generator. The optimized case adds CAPEX, tax benefits, incentives, and O\&M for all recommended DER. Fixed utility fees cancel in the NPV calculation because they cannot be offset by DER (REopt User Manual, 2024). For financial analyses, NPV is guaranteed non-negative unless the user forces a minimum technology size; for resilience analyses, NPV may be negative, indicating that the resilience premium exceeds the economic benefit. Avoided outage costs are not included in the NPV calculation by default, though adding them may increase NPV.

### ExpectedOutageCost Minimax Structure

The stochastic outage formulation evaluates resilience across a combinatorial grid of `outage_start_time_steps` and `outage_durations`, each weighted by `outage_probabilities` (REopt.jl Documentation, Inputs). As established in the upstream scenario overview, the expected outage cost takes the form:

$$\text{ExpectedOutageCost} = \sum_{s \in S} p_s \sum_{t \in T_s} \text{VoLL}_t \cdot \text{UnservedLoad}_{s,t}$$

where $p_s$ is the probability of outage scenario $s$ and the inner summation runs over the time steps $t$ within that scenario's duration. The critical structural feature is a **minimax** arrangement: the **maximum** is taken over `outage_start_time_steps` (the optimizer must hedge against the worst-case start time), while the **expectation** is taken over `outage_durations` weighted by `outage_probabilities`. This ensures the solver provisions sufficient DER capacity for the most challenging initiation hour while weighting costs proportionally to the likelihood of each duration (REopt.jl Documentation, Outputs). Outage time-series results are stored as three-dimensional arrays indexed by `[duration_scenario, start_time_step, timestep_within_outage]`.

### Julia API Surface: Required Calls and Patterns

The `.jl` scripts that drive REopt optimization follow a well-defined API surface. The core calls and their associated patterns are catalogued below.

**1. Scenario Ingestion.**
The scenario JSON is loaded via `JSON.parsefile("path/to/scenario.json")`, which returns a nested `JSON.Object`. A documented bug requires recursive conversion of these objects to native Julia `Dict` types before passing them to REopt internals. The canonical workaround is a `to_dict` utility that walks the parse tree, converting every `JSON.Object` node to `Dict{String, Any}` (REopt API Wiki, Structure).

**2. Solver Instantiation.**
The JuMP model is constructed with:

```julia
using REopt, HiGHS, JuMP
m = Model(HiGHS.Optimizer)
```

Solver-level attributes—most critically the time limit—are configured via `set_attribute(m, "time_limit", seconds)`. The REopt User Manual specifies default optimality tolerances of 0.1% for general cases, 1% for CHP scenarios, and 5% for off-grid analyses (REopt User Manual, 2024).

**3. Optimization Execution.**
`run_reopt` supports two calling signatures:

- **Single-model signature:** `results = run_reopt(m, scenario_dict)` solves the optimized case only.
- **Two-model signature:** `results = run_reopt(m1, m2, scenario_dict)` solves both the BAU and optimized cases in the same invocation, enabling automatic NPV calculation as $\text{LCC}_{\text{BAU}} - \text{LCC}_{\text{Optimal}}$ (REopt API Wiki, Structure). The v3 architecture runs BAU and optimal scenarios in parallel within the Julia process, consolidating what were previously four separate Celery tasks into one.

**4. Result Serialization.**
REopt returns results containing `JuMP.Containers.DenseAxisArray` objects, which are not directly JSON-serializable. A recursive `make_serializable` function must traverse the results dictionary, converting every `DenseAxisArray` to a standard Julia `Array` before calling `JSON.print(io, results)` (REopt.jl Documentation, Outputs).

### Sensitivity Sweep Workflow Pattern

Parametric studies—such as sweeping `Financial.value_of_lost_load_per_kwh` across a range of reliability valuations—follow a standardized pattern:

1. **Deep copy the base scenario:** `scenario_i = deepcopy(base_scenario)` to avoid mutating the template dictionary across iterations.
2. **Override the target parameter:** For VoLL sweeps, assign a scaled profile to `scenario_i["Financial"]["value_of_lost_load_per_kwh"]`. The value may be a scalar or an 8,760-element (or sub-hourly) vector reflecting time-varying willingness-to-pay.
3. **Instantiate a fresh solver model** per iteration: `m = Model(HiGHS.Optimizer)` with appropriate `set_attribute` calls.
4. **Execute:** `results_i = run_reopt(m1, m2, scenario_i)` using the two-model signature to obtain both LCC and NPV.
5. **Collect and serialize:** Apply `make_serializable` to `results_i`, then aggregate across the sweep parameter for downstream analysis.

This `deepcopy`-override-solve-collect loop ensures each iteration operates on an independent scenario state, preventing cross-contamination of mutable dictionary references across parameter grid points. The pattern extends naturally to multi-dimensional sweeps (e.g., jointly varying VoLL and `outage_durations`) by nesting loops over the respective parameter vectors.