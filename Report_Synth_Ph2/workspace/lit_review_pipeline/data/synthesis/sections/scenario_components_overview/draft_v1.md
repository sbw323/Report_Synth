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