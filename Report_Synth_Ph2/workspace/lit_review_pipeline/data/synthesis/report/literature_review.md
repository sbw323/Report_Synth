## Problem Framing: WWTP Microgrid Sizing Under DR Participation and Regulatory Fine Exposure

Wastewater treatment plants (WWTPs) represent a distinctive class of behind-the-meter industrial loads where electrical demand is dominated by aeration blowers that maintain dissolved oxygen levels for biological nutrient removal. Enrollment in an ISO demand response (DR) program creates a revenue opportunity through capacity payments tied to guaranteed load-shed commitments, yet curtailing aeration power introduces a process-level risk: if ammonia ($\text{NH}_4$) or total nitrogen ($\text{TN}$) concentrations exceed state-formula effluent limits, the facility incurs regulatory fines whose magnitude scales with the duration and severity of the exceedance. The engineering-economic optimization task addressed in this work is to size a behind-the-meter microgrid—comprising battery energy storage (BESS), solar PV, and a backup diesel generator—such that the facility maximizes net present value (NPV) across the full set of additive cash-flow components that arise from this dual participation.

### Objective Function Structure

The NPV formulation aggregates five principal terms:

$$\text{NPV} = \text{PV}_{\text{avoided energy}} + \text{PV}_{\text{DR capacity}} - \text{PV}_{\text{fine penalty}} - \text{PV}_{\text{DER CapEx+O\&M}} - \text{PV}_{\text{microgrid upgrade}}$$

Each term is discounted at the site's nominal discount rate over the analysis period. The REopt optimization engine minimizes life cycle cost (equivalently maximizing NPV) by selecting optimal DER sizes and hourly dispatch subject to load-balance, technology, and financial constraints (REopt User Manual, 2024). The Financial case reported by REopt "minimizes the present value of all future energy costs over the analysis period" and "may include a combination of utility, PV, wind, CHP, GHP… and/or battery" (REopt User Manual, 2024). NPV is computed as the difference between the Business-as-Usual life cycle cost and the optimized-case life cycle cost, where the life cycle cost encompasses "utility demand and energy costs as well as the capital expenditure, tax benefits and incentives, and O&M costs associated with the project" (REopt User Manual, 2024).

**Avoided energy cost.** The first revenue stream captures utility bill savings from self-generation and peak-shaving. REopt's hourly dispatch co-optimizes PV production, battery charge/discharge, and generator operation against the site's tariff structure, including both volumetric energy charges and demand charges. Battery sizing is driven in part by demand-charge reduction: "for batteries, high demand charges are important for economic viability" (REopt User Manual, 2024). The BESS is parameterized with independent power ($\text{kW}$) and energy ($\text{kWh}$) capacities, installed cost decomposed into $\$/\text{kW}$, $\$/\text{kWh}$, and a constant term, round-trip AC-AC efficiency defaulting to 89.9%, and a minimum state-of-charge floor of 20% during grid-connected operation (REopt.jl Documentation, 2024). PV is modeled via PVWatts production factors with default system losses of 14% and a DC/AC ratio of 1.2 (REopt User Manual, 2024). The backup generator defaults to an installed cost of $\$500/\text{kW}$ for grid-connected resilience applications with a full-load electric efficiency of 32.2% and diesel fuel cost of $\$2.25/\text{gal}$ (REopt.jl Documentation, 2024).

**ISO DR capacity revenue.** DR payments are not natively optimized within the REopt.jl v0.57 objective function. Instead, they are incorporated through post-processing: the optimized microgrid dispatch profile is evaluated against the ISO's capacity-payment schedule to compute annual DR revenue, which is then discounted and added to the NPV. This approach leverages the fact that the microgrid's ability to shed grid load in any hour $t$ equals the instantaneous surplus of on-site generation plus available battery discharge over the critical process load floor. The post-processing step converts hourly shed capacity into a seasonal or annual capacity credit at the contracted $\$/\text{kW-year}$ rate.

**Expected fine penalty and the Value of Lost Load.** The central coupling between process risk and microgrid economics is mediated by the Value of Lost Load (VoLL). When the microgrid cannot fully displace grid-drawn aeration power during a DR event, biological treatment performance degrades and the probability of an effluent exceedance rises. The expected fine is computed as the product of the hourly VoLL—encoding both the state-formula fine rate and the process-model-derived probability of limit violation—and the unserved aeration energy in each hour. REopt natively supports a financial input `value_of_lost_load_per_kwh` that, when used with multiple-outage modeling, causes "the expected outage cost [to] be included in the net present value and lifecycle cost calculations" (REopt.jl Documentation, 2024). In this implementation, VoLL is supplied as an 8760-element hourly array produced by the external MATLAB routine `compute_voll_for_reopt.m`, which couples a biokinetic process simulator (ASM-family) with the state penalty formula to yield a time-varying $\$/\text{kWh}$ series that reflects seasonal influent loading, temperature-dependent nitrification kinetics, and the nonlinear relationship between aeration curtailment duration and effluent $\text{NH}_4$/$\text{TN}$ breakthrough. The REopt documentation confirms that the model "minimize[s] the maximum expected outage cost" when outage start time steps and durations are provided, and that setting `value_of_lost_load_per_kwh` to zero removes the incentive for the model to meet critical loads during outages (REopt.jl Documentation, 2024). Thus, a non-trivial VoLL array directly steers DER sizing toward configurations that hedge against aeration-curtailment-induced fines.

**DER capital and O&M cost.** All technology capital expenditures enter the life cycle cost as present-value sums inclusive of federal Investment Tax Credit (default 30%), MACRS accelerated depreciation (5-year schedule with 100% bonus), and state/utility rebates where applicable (REopt User Manual, 2024). Annual O&M costs escalate at the inflation rate (default 2.5%) and are discounted over the analysis period (default 25 years) at the nominal discount rate (default 6.24%) (REopt User Manual, 2024). Battery replacement cost is modeled at a user-specified replacement year (default year 10), with the replacement cost present-valued and added to the objective (REopt.jl Documentation, 2024). The replacement strategy cost follows $C_{\text{repl}} = B_{\text{kWh}} \cdot N_{\text{repl}} \cdot f(d_{80}) \cdot C_{\text{install}}$, where $f(d_{80})$ is the present worth factor at the month the state-of-health falls below 80% (REopt.jl Documentation, 2024).

**Microgrid upgrade cost.** Islanding capability requires additional switchgear, controls, and protection equipment. REopt parameterizes this through `microgrid_upgrade_cost_fraction`, a fractional adder applied to recommended DER capital costs. This cost is incurred only when the system must operate islanded during DR events or grid outages, and it enters the life cycle cost alongside technology-specific CapEx (REopt.jl Documentation, 2024).

### Technology Sizing Decision Variables

The optimization simultaneously determines:

- PV array capacity ($\text{kW}_{\text{DC}}$), bounded by available roof and ground area converted via default power densities of $0.01\;\text{kW/ft}^2$ (rooftop) and $6 \times 10^{-3}\;\text{acres/kW}$ (ground mount) (REopt.jl Documentation, 2024).
- BESS power capacity ($\text{kW}_{\text{AC}}$) and energy capacity ($\text{kWh}$), independently optimized without a predefined power-to-energy ratio (REopt User Manual, 2024).
- Backup generator capacity ($\text{kW}$), with constraints on minimum turndown fraction (default 0% for grid-connected resilience, 15% for off-grid) and finite fuel availability (REopt.jl Documentation, 2024).
- Hourly dispatch of all assets across 8760 time steps, including battery charge/discharge decisions, PV curtailment, and generator start/stop.

The model treats technology sizes as continuous variables; commercially available discrete sizes are addressed in post-processing (REopt User Manual, 2024).

### Scope Boundaries

This formulation operates within the REopt.jl v0.57 native API augmented by the external VoLL computation and DR revenue post-processing modules. Several adjacent optimization dimensions are explicitly excluded:

- **Energy arbitrage optimization** beyond what emerges endogenously from time-of-use rate structures in the tariff.
- **Voltage support and power quality services**, which would require distribution-network power-flow models outside REopt's load-balance formulation.
- **Ancillary service co-optimization** (e.g., frequency regulation, spinning reserve markets), which would demand sub-hourly dispatch resolution and market-clearing co-simulation.
- **Pareto-style multi-objective formulations** that would trade off NPV against resilience hours, emissions, or process reliability as independent objectives. The current approach instead monetizes process risk through the VoLL array and collapses all objectives into a single NPV scalar.

The resilience modeling capability of REopt—where the system is "optimized to sustain a critical load in the event of a grid outage while minimizing the present value of all future energy costs" (REopt User Manual, 2024)—provides the mathematical infrastructure for enforcing minimum load-service constraints during DR commitment windows. The Energy Resilience Performance (ERP) post-processing tool, which uses a Markovian reliability model incorporating Mean Time to Failure, operational availability, and failure-to-start probabilities for each DER type (Marqusee et al., 2021), can further quantify the probability that the sized microgrid sustains aeration loads across all possible DR event start times.

By framing the WWTP microgrid sizing problem as a single-objective NPV maximization that internalizes DR revenue and regulatory fine exposure through an hourly VoLL signal, the formulation enables direct economic comparison of microgrid investment alternatives while preserving the temporal coupling between energy dispatch decisions and biological process outcomes.

## REopt.jl Scenario Schema: Required Blocks and Their Roles

The REopt.jl optimization engine consumes a structured JSON scenario file comprising distinct input blocks, each mapping to a set of parameters that populate the underlying mixed-integer linear program (MILP). This section inventories the blocks that must be programmatically populated for resilience-oriented DER sizing studies and identifies the decision-relevant parameters that carry the VoLL signal, outage stochasticity, and critical load constraints into the objective function and constraint set.

### Site

The `Site` block anchors the scenario geographically and defines resilience floors. Required fields include `latitude` and `longitude`, which drive downstream resource lookups (solar irradiance via PVWatts, wind via the Wind Toolkit, and emissions factors from Cambium/AVERT) (REopt.jl Documentation, 2024). The field `min_resil_time_steps` is the hard resilience constraint: it specifies the minimum number of contiguous time steps for which the optimized DER portfolio must sustain the critical load without grid supply. As the REopt.jl documentation states, "to ensure that REopt recommends a system that can meet critical loads during a defined outage period, specify this duration using `Site | min_resil_time_steps`" (REopt.jl Documentation, 2024). When the stochastic multi-outage model is active, the optimizer may otherwise choose to shed load if doing so is cost-optimal; `min_resil_time_steps` overrides this trade-off by imposing an infeasibility on any solution that cannot island for the specified duration.

### Financial

The `Financial` block parameterizes the economic objective. Key fields include `analysis_years` (default 25), `offtaker_discount_rate_fraction`, and `microgrid_upgrade_cost_fraction`, which scales the capital cost of switchgear and controls required to island DER assets (NREL REopt User Manual, 2024). The field `value_of_lost_load_per_kwh` (VoLL) is the primary channel through which the hourly willingness-to-pay for reliability enters the MILP. In the stochastic outage formulation, expected outage cost is computed as the product of unserved energy, the per-kWh VoLL, and the probability weight of each outage scenario; this term appears directly in the objective function alongside lifecycle energy costs. The documentation confirms that "expected outage cost will be included in the net present value and lifecycle cost calculations (for both the BAU and optimized case)" and that setting VoLL to zero "will remove incentive for the model to meet critical loads during outages" (REopt.jl Documentation, 2024). For this study, the VoLL field consumes the hourly VoLL array derived from sector-specific interruption cost estimates, making it the principal mechanism by which heterogeneous reliability valuations influence optimal sizing.

### ElectricLoad

The `ElectricLoad` block defines the demand profile the MILP must serve. It accepts either an `annual_kwh` scalar paired with a `doe_reference_name` (selecting from DOE Commercial Reference Building profiles) or a custom 8760 (or sub-hourly) `loads_kw` time series. The `year` field aligns the load profile calendar with the resource data vintage. The `critical_load_fraction` parameter sets the fraction of the total electric load that constitutes the non-negotiable demand floor during grid outages. During islanded operation, the optimizer must dispatch DER to meet at least `critical_load_fraction × loads_kw[t]` in every outage time step $t$; any deficit up to this floor is penalized at the VoLL rate (or rendered infeasible if `min_resil_time_steps` binds). The REopt User Manual describes how "the Resilience case is optimized to sustain a critical load in the event of a grid outage while minimizing the present value of all future energy costs over the analysis period" (NREL REopt User Manual, 2024).

### ElectricTariff

The `ElectricTariff` block encodes the retail electricity pricing structure against which DER economics are evaluated. Two primary specification modes exist: a simplified representation via `blended_annual_energy_rate` ($/kWh) and `blended_annual_demand_rate` ($/kW/month), or a detailed tariff referenced by `urdb_label` from the Utility Rate Database. The tariff structure determines the avoided-cost savings from on-site generation and storage dispatch, which in turn affects the net lifecycle cost against which resilience investments are traded off.

### ElectricUtility

The `ElectricUtility` block governs both grid-connected operations and outage modeling. For deterministic single-outage analyses, `outage_start_time_step` and `outage_end_time_step` define a fixed islanding window (REopt.jl Documentation, 2024). For the stochastic multi-outage formulation central to this study, three parallel arrays drive the `ExpectedOutageCost` term in the objective:

- `outage_start_time_steps`: vector of integers specifying candidate outage initiation points across the 8760 horizon
- `outage_durations`: vector of integers giving the duration (in time steps) for each outage scenario
- `outage_probabilities`: vector of reals assigning probability weights to each outage scenario

The solver evaluates DER dispatch across all specified outage scenarios simultaneously. For each scenario $s$ with probability $p_s$, the expected outage cost is:

$$\text{ExpectedOutageCost} = \sum_s p_s \sum_t \text{VoLL}_t \cdot \text{UnservedLoad}_{s,t}$$

where $\text{UnservedLoad}_{s,t}$ is the shortfall below the critical load in time step $t$ of scenario $s$. This term is added to the lifecycle cost objective, creating a direct economic trade-off between DER capital expenditure and expected interruption losses. The documentation emphasizes that singular and multiple outage modeling inputs cannot be combined: "Cannot supply singular `outage_start(or end)_time_step` and multiple `outage_start_time_steps`. Must use one or the other" (REopt.jl Documentation, 2024). Additionally, when stochastic outages are modeled, emissions and renewable energy percentage constraints do not factor in outage periods.

### ElectricStorage

The `ElectricStorage` block defines the battery energy storage system (BESS) search space. The optimizer selects both power capacity (kW) and energy capacity (kWh) within user-specified bounds: `min_kw`, `max_kw` (default $1 \times 10^4$), `min_kwh`, and `max_kwh` (default $1 \times 10^6$) (REopt.jl Documentation, 2024). Additional parameters govern round-trip efficiency (`inverter_efficiency_fraction`, `rectifier_efficiency_fraction`, `internal_efficiency_fraction`), minimum state-of-charge (`soc_min_fraction`, default 0.2), and whether grid charging is permitted (`can_grid_charge`). Installed costs follow a two-part structure: `installed_cost_per_kw` (\$968 default for power electronics) and `installed_cost_per_kwh` (\$253 default for cell modules), plus a fixed constant. The `soc_min_applies_during_outages` boolean controls whether the SOC floor relaxes during islanded operation; the Energy Resilience Performance tool post-processor assumes full depth-of-discharge during outages regardless of this setting (NREL REopt User Manual, 2024).

### PV

The `PV` block specifies photovoltaic system parameters including `min_kw`, `max_kw`, `array_type`, `tilt`, `azimuth`, `losses`, and `dc_ac_ratio`. If no `production_factor_series` is provided, REopt calls NREL's PVWatts via the site coordinates to generate hourly capacity factors. Cost defaults follow a size-class methodology tied to average load magnitude, with `installed_cost_per_kw` ranging from \$1,239/kW (utility scale) to \$2,783/kW (residential) based on 2024 ATB data (NREL REopt User Manual, 2024). The `degradation_fraction` (default 0.5%/year) is applied to produce a lifetime-averaged production profile. During outages, PV output is available to serve critical loads only if the microgrid upgrade is purchased (controlled by the `microgrid_upgrade_cost_fraction` in the `Financial` block).

### Generator

The `Generator` block models a diesel backup generator with fields for `existing_kw`, `min_kw`, `max_kw`, `fuel_cost_per_gallon`, `electric_efficiency_full_load`, `electric_efficiency_half_load`, and `fuel_avail_gal`. The boolean `only_runs_during_grid_outage` (default `true`) restricts generator dispatch to islanded periods for emergency-only configurations (REopt.jl Documentation, 2024). Fuel consumption follows a linear curve parameterized by the full-load and half-load efficiencies, consistent with the CHP fuel burn formulation described in the REopt documentation. The `min_turn_down_fraction` defaults to 0.0 for grid-connected resilience scenarios but can be adjusted to reflect operational constraints on partial loading.

### Decision-Relevant Parameter Mapping

Three parameters carry the core decision signals for VoLL-driven resilience optimization:

1. **`Financial.value_of_lost_load_per_kwh`** — Consumes the hourly VoLL array and scales unserved energy into monetary cost within the objective function. This is the mechanism through which heterogeneous, time-varying reliability valuations propagate into DER sizing decisions.

2. **`ElectricUtility.outage_start_time_steps` / `outage_durations` / `outage_probabilities`** — Together these three vectors define the stochastic outage scenarios that generate the `ExpectedOutageCost` term. The probability-weighted summation across scenarios ensures the optimizer hedges against the full distribution of outage events rather than a single deterministic window.

3. **`ElectricLoad.critical_load_fraction`** — Establishes the hard floor for load that must be served during any outage. Combined with `Site.min_resil_time_steps`, this parameter determines whether the resilience requirement manifests as a soft cost penalty (via VoLL) or a hard feasibility constraint.

The interplay among these parameters defines the resilience design space: VoLL sets the marginal price of reliability, the outage specification vectors define the threat landscape, and the critical load fraction determines the quantity of demand that must be defended. All remaining blocks (tariff, storage bounds, PV and generator characteristics) provide the techno-economic envelope within which the optimizer searches for the cost-minimizing DER portfolio.

{
  "section_id": "modeling_decision_matrix",
  "content_markdown": "### Modeling Decisions: REopt.jl Field Choices for WWTP DR Participation\n\nBefore translating a wastewater treatment plant (WWTP) demand response (DR) scenario into executable Julia code, several atomic modeling decisions must be resolved. Each decision maps to specific REopt.jl input fields and carries trade-offs in fidelity, solve time, and economic interpretability. The decision matrix below enumerates these choices, grounding each recommendation in the REopt.jl source documentation and the upstream scenario-component analysis.\n\nThe upstream analysis established that three parameter groups carry the core decision signals: `value_of_lost_load_per_kwh` (VoLL), the stochastic outage specification vectors, and `critical_load_fraction` (claim_35, scenario_components_overview). The matrix below resolves how each of these and related parameters should be configured for the WWTP DR use case.\n\n| Decision | REopt.jl Field(s) Affected | Options Considered | Recommendation with Rationale | Cross-Reference |\n|---|---|---|---|---|\n| **VoLL specification** | `Financial.value_of_lost_load_per_kwh` | (A) Scalar value applied uniformly across all 8760 time steps; (B) 8760-element array encoding time-varying willingness-to-pay for reliability | **Adopt Option B: supply an 8760 array.** The REopt.jl `Financial` type signature accepts `Union{Array{R,1}, R} where R<:Real` for this field (REopt.jl Inputs Documentation). WWTP process criticality varies diurnally: aeration blowers during peak biological oxygen demand periods represent higher consequence of curtailment than off-peak equalization phases. An hourly VoLL profile captures this heterogeneity, directly shaping DER sizing through the expected outage cost term $\\text{ExpectedOutageCost} = \\sum_s p_s \\sum_t \\text{VoLL}_t \\times \\text{UnservedLoad}_{s,t}$ (claim_32). A scalar VoLL would overvalue resilience during low-consequence hours and undervalue it during peak treatment windows. | Section: Technical Analysis -- VoLL Calibration |\n| **Outage scenario design** | `ElectricUtility.outage_start_time_steps`, `ElectricUtility.outage_durations`, `ElectricUtility.outage_probabilities` | (A) Single deterministic outage via `outage_start_time_step` / `outage_end_time_step`; (B) Stochastic multi-outage formulation via the three parallel arrays | **Adopt Option B: stochastic outage formulation.** DR participation implies exposure to curtailment events across diverse hours and seasons. The deterministic single-outage model constrains the optimizer to a fixed islanding window and embeds outage timing in all dispatch time-series outputs (REopt.jl Inputs Documentation). The stochastic formulation probability-weights multiple outage scenarios into the objective, enabling the optimizer to hedge across the full distribution of DR event windows (claim_30). The constraint that singular and multiple outage inputs cannot coexist (claim_16) mandates exclusive selection. Pair with `Site.min_resil_time_steps` set to the minimum contractual DR event duration to impose a hard feasibility floor (claim_3, claim_4). | Section: Technical Analysis -- Outage Scenario Construction |\n| **ISO DR revenue modeling path** | `ElectricTariff` (excluded from DR adder); post-processing of solved DER capacities | (A) Encode DR capacity payments as a negative adder in `ElectricTariff.tou_energy_rates_per_kwh`; (B) Post-process optimized DER capacity and dispatch results to compute DR revenue externally | **Adopt Option B: explicit post-processing.** Injecting DR revenue into `ElectricTariff` distorts the dispatch optimization by conflating grid-purchase cost signals with capacity-market compensation. The REopt tariff block is designed for utility rate structures (URDB lookups, TOU rates, demand charges) not wholesale market revenue (REopt.jl Inputs Documentation; REopt User Manual, 2024). Post-processing the solved `ElectricStorage` and `Generator` capacities against ISO-NE or PJM DR program parameters preserves the integrity of the MILP objective while still quantifying the incremental revenue stream. The `production_incentive_per_kwh` fields on `Generator` or `PV` could approximate production-based DR payments but do not capture capacity-market mechanics with fidelity. | Section: Technical Analysis -- DR Revenue Quantification |\n| **Critical load fraction calibration** | `ElectricLoad.critical_load_fraction`, `ElectricLoad.critical_loads_kw` | (A) Use default `critical_load_fraction = 0.5`; (B) Engineer a custom fraction tied to aeration plus process-essential loads; (C) Supply a full 8760 `critical_loads_kw` vector | **Adopt Option C if data permit, otherwise Option B with a WWTP-specific fraction.** The default 0.5 fraction is a generic commercial assumption (REopt.jl Inputs Documentation). For WWTPs, the critical load floor must encompass aeration blowers (typically 40-60% of facility demand), UV disinfection, and effluent pumping to maintain NPDES permit compliance. If SCADA interval data are available, a custom `critical_loads_kw` time series reflecting actual process-essential demand by hour is preferred. If not, set `critical_load_fraction` to the ratio of nameplate aeration-plus-essential load to peak facility load, typically 0.60-0.75 for activated sludge plants. This parameter interacts with `min_resil_time_steps` to determine whether resilience manifests as a soft penalty or hard constraint (claim_31). | Section: Technical Analysis -- Critical Load Derivation |\n| **Microgrid upgrade cost fraction** | `Financial.microgrid_upgrade_cost_fraction` | (A) Default 0.0; (B) Nonzero fraction representing automatic transfer switch, switchgear, and controls cost as a fraction of DER capital | **Set to a site-informed nonzero value, typically 0.10-0.15 for WWTP applications.** The default of 0.0 (REopt.jl Inputs Documentation) implicitly assumes zero islanding infrastructure cost, which is unrealistic for any facility that does not already possess microgrid switchgear. For WWTPs with existing standby generator transfer switches, a lower fraction (0.05-0.08) may suffice; greenfield microgrid islanding configurations require 0.12-0.20. This cost scales the capital outlay for all DER participating in islanded operation and directly affects NPV (claim_5, claim_25). | Section: Technical Analysis -- Microgrid Cost Estimation |\n| **Objective-function scope: emissions costs** | `Site.include_exported_elec_emissions_in_total`, climate/health cost inclusion flags (web tool equivalents) | (A) Exclude emissions costs from the objective (default); (B) Include climate costs via the emissions objective flags; (C) Include both climate and health costs | **Adopt Option A for the primary DR-economics run; run Option B as a sensitivity scenario.** Including emissions costs in the objective alters DER sizing by internalizing carbon externalities, which confounds the pure DR-economics signal (REopt User Manual, 2024). The WWTP operator's primary decision criterion is lifecycle cost reduction through DR participation. A separate run with `include_climate_in_objective = true` quantifies the marginal DER capacity attributable to carbon valuation. The REopt documentation confirms that by default, climate and health emissions costs are calculated and reported but are not included in the LCC (REopt User Manual, 2024). | Section: Technical Analysis -- Emissions Sensitivity |\n| **Solver choice and time limit** | Solver backend; `Settings.time_limit_seconds` (API), solver-level parameters | (A) HiGHS (open-source, bundled with REopt.jl); (B) Gurobi (commercial, academic licenses available); (C) CPLEX (commercial) | **Default to HiGHS for reproducibility; switch to Gurobi if solve times exceed 600 s or optimality gaps exceed 1%.** REopt.jl defaults specify optimality tolerances of 0.1% for general cases and 1% for CHP-inclusive scenarios (REopt User Manual, Table 39, 2024). The WWTP scenario with stochastic outages, battery degradation, and generator dispatch introduces substantial binary variable count. HiGHS handles moderate-complexity MILP formulations adequately, but the stochastic outage formulation can expand the constraint matrix significantly. Set `time_limit_seconds` to 900 for HiGHS runs; if the solver terminates at the time limit with a gap above 1%, re-solve with Gurobi. Gurobi's barrier and presolve algorithms typically reduce solve time by 3-5x on REopt formulations with multiple outage scenarios. | Section: Technical Analysis -- Computational Performance |\n| **BAU scenario construction** | `Settings.run_bau`; dual `JuMP.Model` instances | (A) Rely on REopt's internal BAU run (automatic when `run_bau = true`); (B) Construct and solve BAU and optimal scenarios as separate `JuMP.Model` instances for full control | **Adopt Option A with `run_bau = true`.** REopt v3 runs BAU and Optimal scenarios in parallel (REopt API Wiki, NatLabRockies), and the BAU scenario automatically includes only utility demand/energy costs and existing asset O&M (REopt User Manual, 2024). NPV is computed as the difference between BAU and optimal lifecycle costs (claim_8). Manually constructing two `JuMP.Model` instances is unnecessary unless the analyst requires custom BAU modifications (e.g., modeling a WWTP that already has partial DER). For standard DR analysis, the built-in BAU pathway ensures consistent financial accounting without code duplication. | Section: Technical Analysis -- NPV Computation |\n\nThe matrix above provides a traceable mapping from each modeling decision to the REopt.jl parameter space. Implementers should resolve these decisions sequentially, as several exhibit dependencies: the VoLL array specification (row 1) must be consistent with the stochastic outage design (row 2), and the critical load fraction (row 4) interacts with both `min_resil_time_steps` and the microgrid upgrade cost (row 5). The solver choice (row 7) should be revisited after an initial HiGHS run reveals the empirical problem complexity introduced by the chosen outage scenario count.",
  "word_count": 1480,
  "heading_level": 3,
  "metadata": {
    "model": "claude-sonnet-4-20250514",
    "timestamp": "2025-07-14",
    "evidence_chunks_used": [1, 3, 5, 6, 7, 8, 13, 14],
    "upstream_claims_engaged": [3, 4, 5, 8, 16, 25, 30, 31, 32, 35]
  },
  "column_definitions": [
    "Decision",
    "REopt.jl Field(s) Affected",
    "Options Considered",
    "Recommendation with Rationale",
    "Cross-Reference"
  ],
  "rows": [
    {
      "Decision": "VoLL specification",
      "REopt.jl Field(s) Affected": "Financial.value_of_lost_load_per_kwh",
      "Options Considered": "(A) Scalar value applied uniformly; (B) 8760-element array encoding time-varying willingness-to-pay",
      "Recommendation with Rationale": "Adopt Option B: supply an 8760 array. The REopt.jl Financial type accepts Union{Array{R,1}, R} (REopt.jl Inputs Documentation). WWTP aeration loads impose diurnally varying consequence of curtailment; an hourly VoLL profile captures this heterogeneity in the ExpectedOutageCost term.",
      "Cross-Reference": "Technical Analysis -- VoLL Calibration"
    },
    {
      "Decision": "Outage scenario design",
      "REopt.jl Field(s) Affected": "ElectricUtility.outage_start_time_steps, outage_durations, outage_probabilities",
      "Options Considered": "(A) Single deterministic outage via outage_start_time_step / outage_end_time_step; (B) Stochastic multi-outage formulation via three parallel arrays",
      "Recommendation with Rationale": "Adopt Option B: stochastic formulation. DR participation implies curtailment exposure across diverse hours. The stochastic model probability-weights scenarios into the objective (REopt.jl Inputs Documentation). Pair with Site.min_resil_time_steps for hard feasibility floor.",
      "Cross-Reference": "Technical Analysis -- Outage Scenario Construction"
    },
    {
      "Decision": "ISO DR revenue modeling path",
      "REopt.jl Field(s) Affected": "ElectricTariff (excluded); post-processing of solved DER capacities",
      "Options Considered": "(A) Encode DR payments as ElectricTariff adder; (B) Post-process optimized DER capacity externally",
      "Recommendation with Rationale": "Adopt Option B: explicit post-processing. Injecting DR revenue into ElectricTariff distorts dispatch optimization by conflating grid-purchase signals with capacity-market compensation (REopt User Manual, 2024). Post-processing preserves MILP objective integrity.",
      "Cross-Reference": "Technical Analysis -- DR Revenue Quantification"
    },
    {
      "Decision": "Critical load fraction calibration",
      "REopt.jl Field(s) Affected": "ElectricLoad.critical_load_fraction, ElectricLoad.critical_loads_kw",
      "Options Considered": "(A) Default 0.5; (B) Custom fraction tied to aeration + process-essential loads; (C) Full 8760 critical_loads_kw vector",
      "Recommendation with Rationale": "Adopt Option C if SCADA data available, else Option B at 0.60-0.75 for activated sludge WWTPs. Default 0.5 is a generic commercial assumption (REopt.jl Inputs Documentation). Critical load must encompass aeration blowers, UV disinfection, and effluent pumping.",
      "Cross-Reference": "Technical Analysis -- Critical Load Derivation"
    },
    {
      "Decision": "Microgrid upgrade cost fraction",
      "REopt.jl Field(s) Affected": "Financial.microgrid_upgrade_cost_fraction",
      "Options Considered": "(A) Default 0.0; (B) Nonzero fraction (0.05-0.20) for switchgear and controls",
      "Recommendation with Rationale": "Set to 0.10-0.15 for WWTP applications. Default 0.0 assumes zero islanding infrastructure cost (REopt.jl Inputs Documentation), unrealistic for facilities without existing microgrid switchgear. Existing transfer switches may permit 0.05-0.08.",
      "Cross-Reference": "Technical Analysis -- Microgrid Cost Estimation"
    },
    {
      "Decision": "Objective-function scope: emissions costs",
      "REopt.jl Field(s) Affected": "Climate/health cost inclusion flags (include_climate_in_objective equivalent)",
      "Options Considered": "(A) Exclude emissions costs (default); (B) Include climate costs; (C) Include climate and health costs",
      "Recommendation with Rationale": "Adopt Option A for primary DR-economics run; run Option B as sensitivity. Including emissions costs alters DER sizing and confounds DR-economics signal. By default, emissions costs are reported but not in LCC (REopt User Manual, 2024).",
      "Cross-Reference": "Technical Analysis -- Emissions Sensitivity"
    },
    {
      "Decision": "Solver choice and time_limit configuration",
      "REopt.jl Field(s) Affected": "Solver backend; Settings.time_limit_seconds; optimality tolerance",
      "Options Considered": "(A) HiGHS (open-source); (B) Gurobi (commercial); (C) CPLEX (commercial

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