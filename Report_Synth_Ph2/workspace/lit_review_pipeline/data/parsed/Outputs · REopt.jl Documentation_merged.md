Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

 

 GitHub  ⚙  

REopt / Outputs 

## **Outputs** 

## **Financial outputs** 

- `REopt.add_financial_results` — Func!on 

`Financial` results keys: 

- `lcc` Op!mal lifecycle cost 

- `lifecycle_generation_tech_capital_costs` LCC component. Net capital costs for all genera!on technologies, in present value, including replacement costs and incen!ves. This value does not include offgrid _other_ capital_costs. 

- `lifecycle_storage_capital_costs` LCC component. Net capital costs for all storage 

- technologies, in present value, including replacement costs and incen!ves. This value does not include offgrid _other_ capital_costs. 

- `lifecycle_om_costs_after_tax` LCC component. Present value of all O&M costs, a#er tax. (does not include fuel costs) 

- `lifecycle_fuel_costs_after_tax` LCC component. Present value of all fuel costs over the analysis period, a#er tax. 

- `lifecycle_chp_standby_cost_after_tax` LCC component. Present value of all CHP standby charges, a#er tax. 

- `lifecycle_elecbill_after_tax` LCC component. Present value of all electric u!lity charges, including compensa!on for exports, a#er tax. 

- `lifecycle_production_incentive_after_tax` LCC component. Present value of all produc!on-based incen!ves, a#er tax. 

- `lifecycle_offgrid_other_annual_costs_after_tax` LCC component. Present value of offgrid _other_ annual_costs over the analysis period, a#er tax. 

- `lifecycle_offgrid_other_capital_costs` LCC component. Equal to 

- _other_ capital_costs with straight line deprecia!on applied over analysis period. The 

- deprecia!on expense is assumed to reduce the owner's taxable income. 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 1 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

- `lifecycle_outage_cost` LCC component. Expected outage cost. `lifecycle_MG_upgrade_and_fuel_cost` LCC component. Cost to upgrade genera!on and storage technologies to be included in microgrid, plus expected microgrid fuel costs, assuming outages occur in first year with specified probabili!es. `lifecycle_om_costs_before_tax` Present value of all O&M costs, before tax. `year_one_total_operating_cost_before_tax` Year one total opera!ng costs, before tax. Includes energy costs, export value, O&M, fuel, and standby costs. 

- `year_one_total_operating_cost_after_tax` Year one total opera!ng costs, a#er tax. Includes energy costs, export value, O&M, fuel, and standby costs. 

- `year_one_fuel_cost_before_tax` Year one fuel costs, before tax. Does not include fuel use during outages if using mul!ple outage modeling. `year_one_fuel_cost_after_tax` Year one fuel costs, a#er tax. Does not include fuel use during outages if using mul!ple outage modeling. `year_one_om_costs_before_tax` Year one O&M costs, before tax. `year_one_om_costs_after_tax` Year one O&M costs, a#er tax. `year_one_chp_standby_cost_after_tax` Year one CHP standby costs, a#er tax. `year_one_chp_standby_cost_before_tax` Year one CHP standby costs, before tax. `lifecycle_capital_costs_plus_om_after_tax` Capital cost for all technologies plus present value of opera!ons and maintenance over anlaysis period. 

- `lifecycle_capital_costs` Net capital costs for all technologies, in present value, including replacement costs and incen!ves. 

- `initial_capital_costs` Up-front capital costs for all technologies, in present value, excluding replacement costs and incen!ves. If third party ownership, represents cost to third party. 

- `initial_capital_costs_after_incentives` Up-front capital costs for all technologies, in present value, excluding replacement costs, and accoun!ng for incen!ves. Note: the ITC and MACRS are discounted by 1 year, and 1-7 years, respec!vely, to obtain the present value. If third party ownership, represents cost to third party. `replacements_future_cost_after_tax` Future cost of replacing storage and/or generator systems, a#er tax. 

- `replacements_present_cost_after_tax` Present value cost of replacing storage and/or generator systems, a#er tax. 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 2 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

- `om_and_replacement_present_cost_after_tax` Present value of all O&M and replacement costs, a#er tax. 

- `developer_om_and_replacement_present_cost_after_tax` Present value of all O&M and replacement costs incurred by developer, a#er tax. 

- `offgrid_microgrid_lcoe_dollars_per_kwh` grid system. 

- `lifecycle_emissions_cost_climate` LCC component if Se$ngs input 

- include _climate_ in_objec!ve is true. Present value of CO2 emissions cost over the analysis period. 

- `lifecycle_emissions_cost_health` LCC component if Se$ngs input 

- include _health_ in_objec!ve is true. Present value of NOx, SO2, and PM2.5 emissions cost over the analysis period. 

calculated in combine_results func!on if BAU scenario is run: 

```
breakeven_cost_of_emissions_reduction_per_tonne_CO2
```

- **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

- **Two Methods for Simple Payback** 

REopt Financial outputs include a comprehensive `simple_payback_years` calcula!on. This is the year in which cumula!ve net free cashflows become posi!ve. For a third party analysis, the SPP is for the developer. A simplified payback period can also be calculated as: 

`capital_costs_after_non_discounted_incentives` divided by 

`year_one_total_operating_cost_savings_after_tax` . 

## **Financial outputs adders with BAU Scenario** 

- `REopt.combine_results` — Method 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 3 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

`combine_results(bau::Dict, opt::Dict)`  

added to the Financial output/results: 

- `npv` : Net Present Value of the op!mal scenario 

- `year_one_total_operating_cost_savings_before_tax` : Total opera!ng cost savings in year 1 before tax 

- `year_one_total_operating_cost_savings_after_tax` : Total opera!ng cost savings in year 1 a#er tax 

- `breakeven_cost_of_emissions_reduction_per_tonne_CO2` : Breakeven cost of CO2 (usd per tonne) that would yield an npv of 0, holding all other inputs constant 

- `lifecycle_emissions_reduction_CO2_fraction` : Frac!on of CO2 emissions reduced in the op!mal scenario compared to the BAU scenario 

## **ElectricTarif outputs** 

- `REopt.add_electric_tariff_results` — Method 

`ElectricTariff` results keys: 

- `lifecycle_energy_cost_after_tax` lifecycle cost of energy from the grid in present value, a#er tax 

- `year_one_energy_cost_before_tax` considering tax benefits 

- `lifecycle_demand_cost_after_tax` lifecycle cost of power from the grid in present value, a#er tax 

- `year_one_demand_cost_before_tax` considering tax benefits 

- `lifecycle_fixed_cost_after_tax` 

- `year_one_fixed_cost_before_tax` benefits 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 4 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

- `lifecycle_min_charge_adder_after_tax` lifecycle minimum charge in present value, a#er tax 

- `year_one_min_charge_adder_before_tax` considering tax benefits 

- `year_one_bill_before_tax` sum of `year_one_energy_cost_before_tax` , `year_one_demand_cost_before_tax` , `year_one_fixed_cost_before_tax` , `year_one_min_charge_adder_before_tax` , and `year_one_coincident_peak_cost_before_tax lifecycle_export_benefit_after_tax` lifecycle export credits in present value, a#er tax `year_one_export_benefit_before_tax` export credits over the first year, before considering tax benefits. A posi!ve value indicates a benefit. 

- `lifecycle_coincident_peak_cost_after_tax` lifecycle coincident peak charge in present value, a#er tax 

- `year_one_coincident_peak_cost_before_tax` 

- `monthly_fixed_cost_series_before_tax` meter per chosen electric tariff in $/month `energy_rate_series` dic!onary for cost of electricity, each key corresponds to a !er with value being $/kWh !meseries 

- `energy_rate_tier_limits` dic!onary for energy rate !er limits, each key corresponds to a !er with value being kWh limit 

- `energy_rate_average_series` average energy rate across all !ers as $/kWh !meseries `facility_demand_monthly_rate_series` facility demand charge in $/kW/month (keys = !ers, values = demand charge for each month) `facility_demand_monthly_rate_tier_limits` facility demand charge limits in kW (keys = !ers, values = demand limit for each month) `tou_demand_rate_series` is a dic!onary with TOU demand charges in $/kW as !meseries for each !mestep 

- `demand_rate_average_series` average TOU demand rate across all !ers as $/kW !meseries `tou_demand_rate_tier_limits` TOU demand charge limits in kW 

Outputs related to REopt calculated costs of electricity (year-one rates and costs not escalated): 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 5 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

- `energy_cost_series_before_tax` !meseries of cost of electricity purchases from the grid (grid to total net load) in $ 

- `monthly_energy_cost_series_before_tax` Monthly energy costs, summed across all !ers in $ 

- `monthly_facility_demand_cost_series_before_tax` Monthly facility demand cost, dic!onary by Tier number in $/month 

- `tou_demand_metrics` -> month: Month this TOU period applies to 

- `tou_demand_metrics` -> !er: Tier of TOU period 

- `tou_demand_metrics` -> demand_rate: $/kW TOU demand charge 

- `tou_demand_metrics` -> measured _tou_ peak_demand: measured peak kW load in TOU period in kW 

- `tou_demand_metrics` -> demand _charge_ before_tax`: calculated demand charge in $ 

- `monthly_tou_demand_cost_series_before_tax` Monthly TOU demand costs, dic!onary by Tier number in $/month 

- `monthly_demand_cost_series_before_tax` Monthly total facility plus TOU demand costs, summed across all !ers in $/month 

Prefix net _metering, wholesale, or net_ metering_excess (export categories) for following outputs, all can be in results if relevant inputs are provided. 

- `_export_rate_series` export rate !meseries for type of export category in $/kWh 

- `_electric_to_grid_series_kw` exported electricity !meseries for type of export category in kW 

- `_monthly_export_series_kwh` monthly exported energy totals by export category in kWh 

- `_monthly_export_cost_benefit_before_tax` $ 

##  **Handling of !ered rates** 

Energy and demand charges costs are returned as a dic!onary with each key corresponding to a cost !er. REopt assumes all TOU periods have the same !er limits 

## **ElectricLoad out uts p** 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 6 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

##  `REopt.add_electric_load_results` — Func!on 

## `ElectricLoad` results keys: 

   - `load_series_kw` # vector of BAU site load in every !me step. Does not include electric load for any new hea!ng or cooling techs. 

   - `critical_load_series_kw` # vector of site cri!cal load in every !me step 

   - `annual_calculated_kwh` # sum of the `load_series_kw` . Does not include electric load for any new hea!ng or cooling techs. 

   - `annual_electric_load_with_thermal_conversions_kwh` # Total end-use electrical load, including electrified hea!ng and cooling end-use load 

   - `offgrid_load_met_series_kw` scenarios only 

   - `offgrid_load_met_fraction` # percentage of total electric load met on an annual basis, for off-grid scenarios only 

   - `offgrid_annual_oper_res_required_series_kwh` # total opera!ng reserves required (for load and techs) on an annual basis, for off-grid scenarios only 

   - `offgrid_annual_oper_res_provided_series_kwh` # total opera!ng reserves provided on an annual basis, for off-grid scenarios only 

   - `monthly_calculated_kwh` # vector of monthly energy consump!on at a site 

   - `monthly_peaks_kw` # vector of monthly peak demand 

   - `annual_peak_kw` # annual peak electricity demand 

- **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

## **ElectricU!lity outputs** 

- `REopt.add_electric_utility_results` — Method 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 7 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

## `ElectricUtility` results keys: 

- `annual_energy_supplied_kwh` # Total energy supplied from the grid in an average year. `electric_to_load_series_kw` # Vector of power drawn from the grid to serve load. `electric_to_storage_series_kw` # Vector of power drawn from the grid to charge the ba%ery. 

- `annual_renewable_electricity_supplied_kwh` # Total renewable electricity supplied from the grid in an average year. 

- `annual_emissions_tonnes_CO2` # Average annual total tons of CO2 emissions associated with the site's grid-purchased electricity. If include _exported_ elec _emissions_ in_total is False, this value only reflects grid purchases. Otherwise, it accounts for emissions offset from any export to the grid. 

- `annual_emissions_tonnes_NOx` # Average annual total tons of NOx emissions associated with the site's grid-purchased electricity. If include _exported_ elec _emissions_ in_total is False, this value only reflects grid purchases. Otherwise, it accounts for emissions offset from any export to the grid. 

- `annual_emissions_tonnes_SO2` # Average annual total tons of SO2 emissions associated with the site's grid-purchased electricity. If include _exported_ elec _emissions_ in_total is False, this value only reflects grid purchases. Otherwise, it accounts for emissions offset from any export to the grid. 

- `annual_emissions_tonnes_PM25` # Average annual total tons of PM25 emissions associated with the site's grid-purchased electricity. If include _exported_ elec _emissions_ in_total is False, this value only reflects grid purchsaes. Otherwise, it accounts for emissions offset from any export to the grid. 

- `lifecycle_emissions_tonnes_CO2` # Total tons of CO2 emissions associated with the site's grid-purchased electricity over the analysis period. If include _exported_ elec _emissions_ in_total is False, this value only reflects grid purchaes. Otherwise, it accounts for emissions offset from any export to the grid. `lifecycle_emissions_tonnes_NOx` # Total tons of NOx emissions associated with the site's grid-purchased electricity over the analysis period. If include _exported_ elec _emissions_ in_total is False, this value only reflects grid purchaes. Otherwise, it accounts for emissions offset from any export to the grid. 

- `lifecycle_emissions_tonnes_SO2` # Total tons of SO2 emissions associated with the site's grid-purchased electricity over the analysis period. If include _exported_ elec _emissions_ in_total is 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 8 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

any export to the grid. 

   - `lifecycle_emissions_tonnes_PM25` # Total tons of PM2.5 emissions associated with the site's grid-purchased electricity over the analysis period. If 

   - include _exported_ elec _emissions_ it accounts for emissions offset from any export to the grid. 

   - `avert_emissions_region` # EPA AVERT region of the site. Used for health-related emissions from grid electricity (populated if default emissions values are used) and climate emissions if "co2 _from_ avert" is set to true. 

   - `distance_to_avert_emissions_region_meters` # Distance in meters from the site to the nearest AVERT emissions region. 

   - `cambium_region` # NLR Cambium region of the site. Used for climate-related emissions from grid electricity (populated only if default (Cambium) climate emissions values are used) 

- **'Series' and 'Annual' energy and emissions outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy and emissions outputs averaged over the analysis period. 

##  **Emissions outputs** 

By default, REopt uses marginal emissions rates for grid-purchased electricity. Marginal emissions rates are most appropriate for repor!ng a change in emissions (avoided or increased) rather than emissions totals. It is therefore recommended that emissions results from REopt (using default marginal emissions rates) be reported as the difference in emissions between the op!mized and BAU case. Note also that the annual_emissions metrics are average annual emissions over the analysis period, accoun!ng for expected changes in future grid emissions. 

## **PV outputs** 

##  `REopt.add_pv_results` — Method 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 9 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

## `PV` results keys: 

- `size_kw` Op!mal PV DC capacity 

- `lifecycle_om_cost_after_tax` Lifecycle opera!ons and maintenance cost in present value, a#er tax 

- `year_one_energy_produced_kwh` 

- `annual_energy_produced_kwh` Average annual energy produced, accoun!ng for degrada!on. Includes curtailed energy. 

- `lcoe_per_kwh` Levelized Cost of Energy produced by the PV system 

- `electric_to_load_series_kw` Vector of power used to meet load over an average year 

- `electric_to_storage_series_kw` Vector of power used to charge the ba%ery over an average year 

- `electric_to_grid_series_kw` Vector of power exported to the grid over an average year `electric_curtailed_series_kw` Vector of power curtailed over an average year 

- `annual_energy_exported_kwh` Average annual energy exported to the grid 

- `production_factor_series` PV produc!on factor in each !me step, either provided by user or obtained from PVWa%s 

##  **Warn** 

The key(s) used to access PV outputs in the results dic!onary is determined by the `PV.name` value to allow for modeling mul!ple PV op!ons. (The default `PV.name` is "PV".) 

##  **Exis!ng PV** 

All outputs account for any exis!ng PV. E.g., `size_kw` includes exis!ng capacity and the REopt-recommended addi!onal capacity. 

##  **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 10 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

**==> picture [576 x 12] intentionally omitted <==**

## **Wind outputs** 

- `REopt.add_wind_results` — Func!on 

`Wind` results keys: 

- `size_kw` Op!mal Wind capacity [kW] 

- `lifecycle_om_cost_after_tax` Lifecycle opera!ons and maintenance cost in present value, a#er tax 

- `year_one_om_cost_before_tax` benefits 

- `electric_to_storage_series_kw` Vector of power used to charge the ba%ery over an average year 

- `electric_to_grid_series_kw` Vector of power exported to the grid over an average year `annual_energy_exported_kwh` Average annual energy exported to the grid 

- `electric_to_load_series_kw` Vector of power used to meet load over an average year 

- `annual_energy_produced_kwh` Average annual energy produced, accoun!ng for degrada!on. Includes curtailed energy. 

- `lcoe_per_kwh` Levelized Cost of Energy produced by the PV system 

- `electric_curtailed_series_kw` Vector of power curtailed over an average year 

- `production_factor_series` Wind produc!on factor in each !me step, either provided by user or obtained from SAM 

 **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

## **ElectricStorage outputs** 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 11 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

 `REopt.add_electric_storage_results` — Method 

`ElectricStorage` results keys: 

- `size_kw` Op!mal inverter capacity 

- `size_kwh` Op!mal storage capacity 

- `soc_series_fraction` Vector of normalized (0-1) state of charge values over the first year 

- `storage_to_load_series_kw` 

- `initial_capital_cost` Upfront capital cost for storage and inverter 

## **The following results are reported if storage degrada!on is modeled:** 

   - `state_of_health` 

   - `maintenance_cost` 

   - `replacement_month` # only applies is maintenance_strategy = "replacement" 

   - `residual_value` 

   - `total_residual_kwh` # only applies is maintenance_strategy = "replacement" 

- **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

## **HotThermalStorage outputs** 

- `REopt.add_hot_storage_results` — Method 

`HotThermalStorage` results keys: 

- `size_kwh` Op!mal TES capacity, by energy [kWh] 

- `size_gal` Op!mal TES capacity, by volume [gal] 

```
soc_series_fraction
```

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 12 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

   - `storage_to_steamturbine_series_mmbtu_per_hour` Vector of heat sent to steam turbine over the first year [MMBTU/hr] 

   - `storage_to_absorption_chiller_series_mmbtu_per_hour` Vector of heat sent to absorp!on chiller over the first year [MMBTU/hr] 

   - `storage_to_load_series_mmbtu_per_hour` Vector of thermal power used to meet load over the first year [MMBTU/hr] 

   - `storage_to_space_heating_load_series_mmbtu_per_hour` Vector of heat sent to space hea!ng load over the first year [MMBTU/hr] 

   - `storage_to_dhw_load_series_mmbtu_per_hour` Vector of heat sent to domes!c hot water load over the first year [MMBTU/hr] 

   - `storage_to_process_heat_load_series_mmbtu_per_hour` Vector of heat sent to process heat load over the first year [MMBTU/hr] 

- **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

## **HighTempThermalStorage outputs** 

- `REopt.add_high_temp_thermal_storage_results` — Method 

`HighTempThermalStorage` results keys: 

- `size_kwh` Op!mal TES capacity, by energy [kWh] 

- `soc_series_fraction` 

- `storage_to_steamturbine_series_mmbtu_per_hour` Vector of heat sent to steam turbine over the first year [MMBTU/hr] 

- `storage_to_absorption_chiller_series_mmbtu_per_hour` Vector of heat sent to absorp!on chiller over the first year [MMBTU/hr] 

- `storage_to_load_series_mmbtu_per_hour` Vector of thermal power used to meet load over the first year [MMBTU/hr] 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 13 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

   - `storage_to_space_heating_load_series_mmbtu_per_hour` Vector of heat sent to space hea!ng load over the first year [MMBTU/hr] 

   - `storage_to_dhw_load_series_mmbtu_per_hour` Vector of heat sent to domes!c hot water load over the first year [MMBTU/hr] 

   - `storage_to_process_heat_load_series_mmbtu_per_hour` Vector of heat sent to process heat load over the first year [MMBTU/hr] 

- **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

## **ColdThermalStorage outputs** 

- `REopt.add_cold_storage_results` — Method 

`ColdThermalStorage` results: 

- `size_gal` Op!mal TES capacity, by volume [gal] 

- `soc_series_fraction` 

- `storage_to_load_series_ton` 

## **Generator outputs** 

- `REopt.add_generator_results` — Method 

`Generator` results keys: 

- `size_kw` Op!mal generator capacity 

- `lifecycle_fixed_om_cost_after_tax` present value, a#er tax 

- `year_one_fixed_om_cost_before_tax` 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 14 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

- `lifecycle_variable_om_cost_after_tax` Lifecycle variable opera!ons and maintenance cost in present value, a#er tax 

- `year_one_variable_om_cost_before_tax` variable opera!ons and maintenance cost over the first year, before considering tax benefits 

- `lifecycle_fuel_cost_after_tax` Lifecycle fuel cost in present value, a#er tax 

- `year_one_fuel_cost_before_tax` benefits. Does not include fuel use during outages if using mul!ple outage modeling. 

- `year_one_fuel_cost_after_tax` Does not include fuel use during outages if using mul!ple outage modeling. 

- `annual_fuel_consumption_gal` Gallons of fuel used in each year 

- `electric_to_storage_series_kw` Vector of power sent to ba%ery in an average year 

- `electric_to_grid_series_kw` Vector of power sent to grid in an average year 

- `electric_to_load_series_kw` Vector of power sent to load in an average year 

- `annual_energy_produced_kwh` Average annual energy produced over analysis period 

 **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

## **Exis!ngBoiler outputs** 

- `REopt.add_existing_boiler_results` — Func!on 

## `ExistingBoiler` results keys: 

- `size_mmbtu_per_hour` # Thermal produc!on capacity size of the Boiler [MMBtu/hr] 

- `fuel_consumption_series_mmbtu_per_hour` # Fuel consump!on series [MMBtu/hr] 

- `annual_fuel_consumption_mmbtu` # Fuel consumed in a year [MMBtu] 

- `thermal_production_series_mmbtu_per_hour` # Thermal energy produc!on series 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 15 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

## [MMBtu/hr] 

   - `annual_thermal_production_mmbtu` # Thermal power produc!on in a year [MMBtu] 

   - `thermal_to_storage_series_mmbtu_per_hour` # Thermal power produc!on to TES (HotThermalStorage) series [MMBtu/hr] 

   - `thermal_to_steamturbine_series_mmbtu_per_hour` # Thermal power produc!on to SteamTurbine series [MMBtu/hr] 

   - `thermal_to_load_series_mmbtu_per_hour` # Thermal power produc!on to serve the hea!ng load series [MMBtu/hr] (superset of "to _absorp!on_ chiller", "to _space_ hea!ng _load", "to_ dhw _load", and "to_ process _heat_ load") 

   - `thermal_to_absorption_chiller_series_mmbtu_per_hour` # Thermal power produc!on to serve absorp!on chiller load series [MMBtu/hr] 

   - `thermal_to_dhw_load_series_mmbtu_per_hour` # Thermal power produc!on to serve domes!c hot water load series [MMBtu/hr] 

   - `thermal_to_space_heating_load_series_mmbtu_per_hour` # Thermal power produc!on to serve space hea!ng load series [MMBtu/hr] 

   - `thermal_to_process_heat_load_series_mmbtu_per_hour` # Thermal power produc!on to serve process heat load series [MMBtu/hr] 

   - `lifecycle_fuel_cost_after_tax` # Life cycle fuel cost [$] 

   - `year_one_fuel_cost_before_tax` # Year one fuel cost, before tax [$] 

   - `year_one_fuel_cost_after_tax` # Year one fuel cost, a#er tax [$] 

- **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

## **CHP outputs** 

- `REopt.add_chp_results` — Func!on 

`CHP` results keys: 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 16 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

- `size_kw` Power capacity size of the CHP system [kW] 

- `size_supplemental_firing_kw` Power capacity of CHP supplementary firing system [kW] `annual_fuel_consumption_mmbtu` Fuel consumed in a year [MMBtu] `annual_electric_production_kwh` Electric energy produced in a year [kWh] `annual_thermal_production_mmbtu` Thermal energy produced in a year (not including curtailed thermal) [MMBtu] 

- `electric_production_series_kw` Electric power produc!on !me-series array [kW] `electric_to_grid_series_kw` Electric power exported !me-series array [kW] `electric_to_storage_series_kw` Electric power to charge the ba%ery storage !me-series array [kW] 

- `electric_to_load_series_kw` Electric power to serve the electric load !me-series array [kW] 

- `thermal_to_storage_series_mmbtu_per_hour` Thermal power to TES (HotThermalStorage) !me-series array [MMBtu/hr] 

- `thermal_curtailed_series_mmbtu_per_hour` Thermal power wasted/unused/vented !meseries array [MMBtu/hr] 

- `thermal_to_steamturbine_series_mmbtu_per_hour` Thermal (steam) power to steam turbine !me-series array [MMBtu/hr] `thermal_to_load_series_mmbtu_per_hour` Thermal power to serve the hea!ng load !meseries array [MMBtu/hr] (superset of "to _absorp!on_ chiller", "to _space_ hea!ng _load", "to_ dhw _load", and "to_ process _heat_ load") 

- `thermal_to_absorption_chiller_series_mmbtu_per_hour` Thermal power to serve absorp!on chiller load [MMBtu/hr] 

- `thermal_to_dhw_load_series_mmbtu_per_hour` Thermal power to serve domes!c hot water load [MMBtu/hr] 

- `thermal_to_space_heating_load_series_mmbtu_per_hour` Thermal power to serve space hea!ng load [MMBtu/hr] 

- `thermal_to_process_heat_load_series_mmbtu_per_hour` Thermal power to serve process heat load [MMBtu/hr] 

- `year_one_fuel_cost_before_tax` Cost of fuel consumed by the CHP system in year one, before tax [$] 

- `year_one_fuel_cost_after_tax` Cost of fuel consumed by the CHP system in year one, a#er 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 17 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

## tax 

   - `lifecycle_fuel_cost_after_tax` Present value of cost of fuel consumed by the CHP system, a#er tax [$] 

   - `year_one_standby_cost_before_tax` CHP standby charges in year one, before tax [$] 

   - `year_one_standby_cost_after_tax` CHP standby charges in year one, a#er tax 

   - `lifecycle_standby_cost_after_tax` Present value of all CHP standby charges, a#er tax. 

   - `thermal_production_series_mmbtu_per_hour` 

   - `initial_capital_costs` Ini!al capital costs of the CHP system, before incen!ves [$] 

- **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

## **Boiler outputs** 

- `REopt.add_boiler_results` — Func!on 

## `Boiler` results keys: 

- `size_mmbtu_per_hour` # Thermal produc!on capacity size of the Boiler [MMBtu/hr] 

- `fuel_consumption_series_mmbtu_per_hour` # Fuel consump!on series [MMBtu/hr] 

- `annual_fuel_consumption_mmbtu` # Fuel consumed in a year [MMBtu] 

- `thermal_production_series_mmbtu_per_hour` # Thermal energy produc!on series [MMBtu/hr] 

- `annual_thermal_production_mmbtu` # Thermal energy produced in a year [MMBtu] 

- `thermal_to_storage_series_mmbtu_per_hour` # Thermal power produc!on to TES (HotThermalStorage) series [MMBtu/hr] 

- `thermal_to_steamturbine_series_mmbtu_per_hour` # Thermal power produc!on to SteamTurbine series [MMBtu/hr] 

- `thermal_to_load_series_mmbtu_per_hour` # Thermal power produc!on to serve the 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 18 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

   - hea!ng load series [MMBtu/hr] (superset of "to _absorp!on_ chiller", "to _space_ hea!ng _load", "to_ dhw _load", and "to_ process _heat_ load") 

   - `thermal_to_absorption_chiller_series_mmbtu_per_hour` # Thermal power produc!on to serve absorp!on chiller load series [MMBtu/hr] 

   - `thermal_to_dhw_load_series_mmbtu_per_hour` # Thermal power produc!on to serve domes!c hot water load series [MMBtu/hr] 

   - `thermal_to_space_heating_load_series_mmbtu_per_hour` # Thermal power produc!on to serve space hea!ng load series [MMBtu/hr] 

   - `thermal_to_process_heat_load_series_mmbtu_per_hour` # Thermal power produc!on to serve process heat load series [MMBtu/hr] 

   - `lifecycle_fuel_cost_after_tax` # Life cycle fuel cost [$] 

   - `year_one_fuel_cost_before_tax` # Year one fuel cost, before tax [$] 

   - `year_one_fuel_cost_after_tax` # Year one fuel cost, a#er tax [$] 

   - `lifecycle_per_unit_prod_om_costs` # Life cycle produc!on-based O&M cost [$] 

- **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

## **Hea!ngLoad outputs** 

- `REopt.add_heating_load_results` — Func!on 

## `HeatingLoad` results keys: 

- `dhw_thermal_load_series_mmbtu_per_hour` vector of site thermal domes!c hot water load in every !me step 

- `space_heating_thermal_load_series_mmbtu_per_hour` vector of site thermal space hea!ng load in every !me step 

`process_heat_thermal_load_series_mmbtu_per_hour` vector of site thermal process heat load in every !me step 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 19 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

- `total_heating_thermal_load_series_mmbtu_per_hour` vector of sum thermal hea!ng load in every !me step 

- `dhw_boiler_fuel_load_series_mmbtu_per_hour` vector of site fuel domes!c hot water load in every !me step 

- `space_heating_boiler_fuel_load_series_mmbtu_per_hour` vector of site fuel space hea!ng load in every !me step 

- `process_heat_boiler_fuel_load_series_mmbtu_per_hour` vector of site fuel process heat load in every !me step 

- `total_heating_thermal_load_series_mmbtu_per_hour` vector of sum fuel hea!ng load in every !me step 

- `annual_calculated_dhw_thermal_load_mmbtu` sum of the 

- `dhw_thermal_load_series_mmbtu_per_hour` 

- `annual_calculated_space_heating_thermal_load_mmbtu` sum of the 

- `space_heating_thermal_load_series_mmbtu_per_hour` 

- `annual_calculated_process_heat_thermal_load_mmbtu` sum of the 

- `process_heat_thermal_load_series_mmbtu_per_hour` 

- `annual_calculated_total_heating_thermal_load_mmbtu` sum of the 

- `total_heating_thermal_load_series_mmbtu_per_hour` 

- `annual_calculated_dhw_boiler_fuel_load_mmbtu` sum of the 

- `dhw_boiler_fuel_load_series_mmbtu_per_hour` 

- `annual_calculated_space_heating_boiler_fuel_load_mmbtu` sum of the `space_heating_boiler_fuel_load_series_mmbtu_per_hour` 

- `annual_calculated_process_heat_boiler_fuel_load_mmbtu` sum of the `process_heat_boiler_fuel_load_series_mmbtu_per_hour` 

- `annual_calculated_total_heating_boiler_fuel_load_mmbtu` sum of the `total_heating_boiler_fuel_load_series_mmbtu_per_hour` 

## **CoolingLoad outputs** 

- `REopt.add_cooling_load_results` — Func!on 

`CoolingLoad` results keys: 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 20 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

   - `load_series_ton` # vector of site cooling load in every !me step 

   - `annual_calculated_tonhour` # sum of the `load_series_ton` . Annual site total cooling load [tonhr] 

   - `electric_chiller_base_load_series_kw` # Hourly total base load drawn from chiller [kWelectric] 

   - `annual_electric_chiller_base_load_kwh` # Annual total base load drawn from chiller [kWh-electric] 

- **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

## **Outages outputs** 

- `REopt.add_outage_results` — Func!on 

## `Outages` results keys: 

- `expected_outage_cost` The expected outage cost over the random outages modeled. 

- `max_outage_cost_per_outage_duration` The maximum outage cost in every outage dura!on modeled. 

- `unserved_load_series_kw` The amount of unserved load in each outage and each !me step. `unserved_load_per_outage_kwh` The total unserved load in each outage. 

- `storage_microgrid_upgrade_cost` The cost to include the storage system in the microgrid. 

- `storage_discharge_series_kw` Array of storage power discharged in every outage modeled. 

- `pv_microgrid_size_kw` Op!mal microgrid PV capacity. Note that the name `PV` can change based on user provided `PV.name` . 

- `pv_microgrid_upgrade_cost` The cost to include the PV system in the microgrid. 

- `pv_to_storage_series_kw` Array of PV power sent to the ba%ery in every outage modeled. 

- `pv_curtailed_series_kw` Array of PV curtailed in every outage modeled. 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 21 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

- `pv_to_load_series_kw` Array of PV power used to meet load in every outage modeled. `wind_microgrid_size_kw` Op!mal microgrid Wind capacity. `wind_microgrid_upgrade_cost` The cost to include the Wind system in the microgrid. `wind_to_storage_series_kw` Array of Wind power sent to the ba%ery in every outage modeled. 

- `wind_curtailed_series_kw` Array of Wind curtailed in every outage modeled. `wind_to_load_series_kw` Array of Wind power used to meet load in every outage modeled. `generator_microgrid_size_kw` Op!mal microgrid Generator capacity. Note that the name `Generator` can change based on user provided `Generator.name` . `generator_microgrid_upgrade_cost` The cost to include the Generator system in the microgrid. `generator_to_storage_series_kw` Array of Generator power sent to the ba%ery in every outage modeled. `generator_curtailed_series_kw` Array of Generator curtailed in every outage modeled. `generator_to_load_series_kw` Array of Generator power used to meet load in every outage modeled. 

- `generator_fuel_used_per_outage_gal` Array of fuel used in every outage modeled, summed over all Generators. 

- `chp_microgrid_size_kw` Op!mal microgrid CHP capacity. `chp_microgrid_upgrade_cost` The cost to include the CHP system in the microgrid. `chp_to_storage_series_kw` Array of CHP power sent to the ba%ery in every outage modeled. 

- `chp_curtailed_series_kw` Array of CHP curtailed in every outage modeled. `chp_to_load_series_kw` Array of CHP power used to meet load in every outage modeled. `chp_fuel_used_per_outage_mmbtu` Array of fuel used in every outage modeled, summed over all CHPs. `microgrid_upgrade_capital_cost` Total capital cost of including technologies in the microgrid `critical_loads_per_outage_series_kw` Cri!cal load series in every outage modeled `soc_series_fraction` ElectricStorage state of charge series in every outage modeled 

 **Warn** 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 22 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

The output keys for `Outages` are subject to change. 

##  **Note** 

This `Outages` sec!on is only added to results when outages are modeled via the 

`ElectricUtility.outage_start_time_steps` and `ElectricUtility.outage_durations` 

inputs. If the single outage model is used, the outage is included in all !me series outputs. See `ElectricUtility` for an explana!on of these outage modeling op!ons. 

##  **Warn** 

The `Outages` results can be very large when many outages are modeled and can take a long !me to generate. 

##  **Accessing outage results** 

Outage !meseries results are 3-dimensional arrays with dimensions corresponding to the outage dura!ons, the outage start !me, and the !me step in the outage. For example, 

`results["Outages"]["pv_to_load_series_kw"][s,t,ts]` is the PV power used to meet load in outage scenario (dura!on) `s` , star!ng at !me step `t` , at !me step `ts` in that outage. 

## **Absorp!onChiller outputs** 

 `REopt.add_absorption_chiller_results` — Func!on 

## `AbsorptionChiller` results keys: 

`size_kw` # Op!mal power capacity size of the absorp!on chiller system [kW] 

```
size_ton
```

`thermal_to_storage_series_ton` # Thermal produc!on to ColdThermalStorage 

`thermal_to_load_series_ton` # Thermal produc!on to cooling load 

```
thermal_consumption_series_mmbtu_per_hour
```

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 23 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

```
annual_thermal_consumption_mmbtu
```

```
annual_thermal_production_tonhour
```

- `electric_consumption_series_kw` 

- `annual_electric_consumption_kwh` 

## **FlexibleHVAC outputs** 

- `REopt.add_flexible_hvac_results` — Func!on 

## `FlexibleHVAC` results keys: 

- `purchased` 

- `temperatures_degC_node_by_time` 

- `upgrade_cost` 

## **SteamTurbine outputs** 

- `REopt.add_steam_turbine_results` — Func!on 

## `SteamTurbine` results keys: 

- `size_kw` Power capacity size [kW] 

- `annual_thermal_consumption_mmbtu` Thermal (steam) consump!on [MMBtu] 

- `annual_electric_production_kwh` Electric energy produced in a year [kWh] 

- `annual_thermal_production_mmbtu` Thermal energy produced in a year [MMBtu] 

- `thermal_consumption_series_mmbtu_per_hour` Thermal (steam) energy consump!on series [MMBtu/hr] 

- `electric_production_series_kw` Electric power produc!on series [kW] 

- `electric_to_grid_series_kw` Electric power exported to grid series [kW] 

- `electric_to_storage_series_kw` Electric power to charge the ba%ery series [kW] 

- `electric_to_load_series_kw` Electric power to serve load series [kW] 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 24 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

   - `thermal_to_storage_series_mmbtu_per_hour` Thermal produc!on to charge the HotThermalStorage series [MMBtu/hr] 

   - `thermal_to_high_temp_thermal_storage_series_mmbtu_per_hour` 

   - `thermal_to_load_series_mmbtu_per_hour` Thermal power to serve the hea!ng load !meseries array [MMBtu/hr] (superset of "to _absorp!on_ chiller", "to _space_ hea!ng _load", "to_ dhw _load", and "to_ process _heat_ load") 

   - `thermal_to_absorption_chiller_series_mmbtu_per_hour` 

   - `thermal_to_dhw_load_series_mmbtu_per_hour` Thermal power to serve domes!c hot water load [MMBtu/hr] 

   - `thermal_to_space_heating_load_series_mmbtu_per_hour` Thermal power to serve space hea!ng load [MMBtu/hr] 

   - `thermal_to_process_heat_load_series_mmbtu_per_hour` Thermal power to serve process heat load [MMBtu/hr] 

- **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

## **CST outputs** 

- `REopt.add_concentrating_solar_results` — Func!on 

## `CST` results keys: 

- `size_kw` # Thermal produc!on capacity size of the CST [kW] 

- `size_mmbtu_per_hour` ` Thermal produc!on capacity size of the CST [MMBtu/hr] 

- `electric_consumption_series_kw` # Fuel consump!on series [kW] 

- `annual_electric_consumption_kwh` # Fuel consumed in a year [kWh] 

- `thermal_production_series_mmbtu_per_hour` # Thermal energy produc!on series [MMBtu/hr] 

`annual_thermal_production_mmbtu` # Thermal energy produced in a year [MMBtu] 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 25 of 26 

Outputs · REopt.jl Documentation 

4/16/26, 10:34 AM 

   - `thermal_to_storage_series_mmbtu_per_hour` # Thermal power produc!on to TES (HotThermalStorage) series [MMBtu/hr] 

   - `thermal_to_high_temp_thermal_storage_series_mmbtu_per_hour` # Thermal power produc!on to TES (HotThermalStorage) series [MMBtu/hr] 

   - `thermal_to_steamturbine_series_mmbtu_per_hour` # Thermal power produc!on to SteamTurbine series [MMBtu/hr] 

   - `thermal_curtailed_series_mmbtu_per_hour` Thermal power wasted/unused/vented !meseries array [MMBtu/hr] 

   - `thermal_to_load_series_mmbtu_per_hour` # Thermal power produc!on to serve the hea!ng load series [MMBtu/hr] (superset of "to _absorp!on_ chiller", "to _space_ hea!ng _load", "to_ dhw _load", and "to_ process _heat_ load") 

   - `thermal_to_absorption_chiller_series_mmbtu_per_hour` # Thermal power produc!on to serve absorp!on chiller load series [MMBtu/hr] 

   - `thermal_to_dhw_load_series_mmbtu_per_hour` # Thermal power produc!on to serve domes!c hot water load series [MMBtu/hr] 

   - `thermal_to_space_heating_load_series_mmbtu_per_hour` # Thermal power produc!on to serve space hea!ng load series [MMBtu/hr] 

   - `thermal_to_process_heat_load_series_mmbtu_per_hour` # Thermal power produc!on to serve process heat load series [MMBtu/hr] 

- **'Series' and 'Annual' energy outputs are average annual** 

REopt performs load balances using average annual produc!on values for technologies that include degrada!on. Therefore, all !meseries ( `_series` ) and `annual_` results should be interpre%ed as energy outputs averaged over the analysis period. 

« Inputs 

Methods » 

Powered by Documenter.jl and the Julia Programming Language. 

https://natlabrockies.github.io/REopt.jl/dev/reopt/outputs/ 

Page 26 of 26 

