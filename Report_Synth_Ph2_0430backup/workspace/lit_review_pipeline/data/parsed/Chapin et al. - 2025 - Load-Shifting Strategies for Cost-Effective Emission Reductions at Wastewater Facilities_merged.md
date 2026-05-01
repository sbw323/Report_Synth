Article 

**==> picture [177 x 69] intentionally omitted <==**

pubs.acs.org/est 

## **Load-Shifting Strategies for Cost-Effective Emission Reductions at Wastewater Facilities** 

Fletcher T. Chapin, Daly Wettermark, Jose Bolorinos, and Meagan S. Mauter* 

**Cite This:** _Environ. Sci. Technol._ 2025, 59, 2285−2294 **Read Online** 

ACCESS Metrics & More Article Recommendations * **sı** Supporting Information 

ABSTRACT: Significant hourly variation in the carbon intensity of electricity supplied to wastewater facilities introduces an opportunity to lower emissions by shifting the timing of their energy demand. This shift could be accomplished by storing wastewater, biogas from sludge digestion, or electricity from on-site biogas generation. However, the life cycle emissions and cost implications of these options are not clear. We present a multiobjective optimization framework for comparing cost- and emission-minimizing loadshifting strategies at a California case study facility with a relatively low carbon intensity grid and high spread in peak and off-peak electricity prices. We evaluate cost and emission trade-offs from the optimal flexible operation of both existing infrastructure and optimally sized energy flexibility upgrades. We estimate energy- 

**==> picture [236 x 135] intentionally omitted <==**

related emission reductions of up to 9.0% with flexible operation of existing infrastructure and up to 16.8% with optimally sized storage upgrades. Only a fraction of these potential savings are realized under actual industrial energy tariffs and the EPA’s recommended social cost of carbon. Energy flexibility may hold promise as a short-term emission-saving solution for the wastewater sector, but the extent of savings is heavily dependent on the cost of carbon, electricity tariffs, and emission intensity of the regional electricity grid. 

KEYWORDS: _wastewater, energy flexibility, electricity, climate, multiobjective optimization, load shifting_ 

## ■ **[INTRODUCTION]** 

Wastewater facilities account for 1−3% of life cycle US greenhouse gas (GHG) emissions (Section S.1), a figure that is expected to increase with more stringent nutrient removal requirements and enhanced demand for water reuse.[1] A wastewater facility’s total life cycle GHG emissions are − typically composed of 22 80% Scope 1[2][−][7] (i.e., direct gaseous emissions), 4−42% Scope 2[6][,][8][−][10] (i.e., emissions from purchased electricity), and 12−65% Scope 3[11][−][18] (i.e., embodied emissions from manufacturing and biosolid disposal) emissions. Meaningful Scope 1 emission reduction typically requires a full treatment system overhaul,[19][,][20] which includes substantial capital investment. Scope 2 emissions can be mitigated by generating electricity through biogas combustion[21] or on-site renewables,[22] but most facilities purchase electricity from the grid. Scope 3 emissions are outside the direct control of the facility but can be mitigated through the supply chain or other operational decisions. 

Energy flexibility, or the ability of a facility to shift the timing of energy consumption, may offer a cost-effective and rapidly implementable solution for reducing Scope 2 emissions. Since grid emissions vary significantly through the day,[6] past work has proposed modulating biological treatment processes,[23][−][25] pumps,[26][−][31] and aeration systems[27][,][30][,][32][−][34] to reduce load 

when emissions are high and increase load when emissions are low. One recent case study at a German facility estimates that load shifting could reduce Scope 2 emissions by 5−7% annually.[26] Generally, these prior studies have not fully incorporated the daily, weekly, and seasonable variability of emission intensity and electricity tariffs. Past work has rarely incorporated the effect of energy flexibility interventions on minimizing biogas flaring and associated Scope 1 emission reductions with cogeneration. Finally, existing studies have underexplored the potential for capital upgrades to wastewater,[35] biogas,[35] and Li-ion battery[35][,][36] storage to enhance latent facility flexibility. 

In addition to better understanding the potential for energy flexibility to reduce Scope 2 emissions, there is significant uncertainty around the impact of load shifting on energy costs. Local electricity tariffs often include both fixed and variable costs that change on hourly and seasonal time scales to reflect 

**==> picture [39 x 59] intentionally omitted <==**

Received: September 13, 2024 Revised: January 8, 2025 Accepted: January 9, 2025 Published: January 17, 2025 

https://doi.org/10.1021/acs.est.4c09773 _Environ. Sci. Technol._ 2025, 59, 2285−2294 

© 2025 American Chemical Society 

**2285** 

**Environmental Science & Technology** 

**pubs.acs.org/est** 

Article 

**==> picture [361 x 202] intentionally omitted <==**

Figure 1. Diagram represents the data sources, models, and outputs of our analysis of wastewater facility energy-related emissions and costs. Energy tariffs are sourced from Chapin et al.,[40] with grid emission intensities from de Chalendar et al.,[41][,][42] operational data from our case study facility in California, and literature review of embodied emissions (Tables S.3.2, S.3.5, and S.3.6). Bolorinos et al. developed the digital twin and control optimization for cost optimization.[35] We extend the framework to include emissions accounting in a multiobjective optimization problem that balances energy-related costs and emissions. 

the underlying costs of generation and transmission. Peak wastewater treatment demand typically exhibits substantial overlap with peak electricity tariffs, suggesting benefits from shifting demand away from these peaks,[28][,][37][−][39] but spatial and temporal analysis over several years of operational data is essential to quantitatively evaluate trade-offs in cost and emission incentives. High-resolution, site-specific analysis is also critical to the optimal design (e.g., type and size) and operation of storage resources that enhance energy flexibility. In conclusion, the trade-offs between cost and emission incentives have not been adequately investigated for long-term operation under electricity tariffs and carbon intensities that vary geographically, seasonally, and hourly. 

This paper presents the first comprehensive methodology for analyzing trade-offs in costs and emissions from flexibly operated wastewater facilities. First, we develop a real-time emission-accounting tool for quantifying the short- and longterm costs and emission trade-offs of flexible operation of wastewater facilities. We then formulate a multiobjective optimization problem that solves the cost- and emissionoptimal operation of a wastewater facility under diverse tariff structures, grid emission intensities, and assumed social cost of carbon (SCC). We demonstrate our framework by sizing and selecting energy flexibility upgrades at a case study facility. 

This framework and subsequent analysis address several critical research questions for the wastewater community. We elucidate the magnitude and variance of wastewater treatment emission intensity as a function of time and grid mix as well as the degree to which flexible operation of existing facilities can reduce those emissions. Next, we assess the emission benefits of optimally sized storage infrastructure and elucidate the trade-offs between cost and life cycle emissions when designing and operating that storage. Finally, we apply our framework nationally to evaluate the sensitivity of these results to the tariff structure, grid mix, and assumed SCC. 

## ■ **[METHODS]** 

**Scope of Analysis.** We summarize the framework’s data sources and models in Figure 1. We develop a dynamic emissions model for a wastewater facility that explicitly calculates Scope 1, 2, and 3 emissions and accounts for any changes resulting from the storage of raw wastewater, biogas from sludge digestion, or electricity produced by the on-site cogenerator. Scope 1 emissions from biological processes are included in our estimates of total facility emissions but excluded from our dynamic model because of the uncertainty in how emissions might change when storing wastewater for up to 12 h under well-mixed conditions. The impacts of assuming fixed Scope 1 emission factors are further explored in Section S.2.5. The subsequent cost and emission minimization optimizes the operation of existing and hypothetical storage resources at the facility to identify optimal storage design and operational parameters. Throughout, we account for stochastic variation in facility operation, temporal variation in emission factors, and mechanisms by which constructing and operating storage resources would change capital and operational costs and emissions at the facility. Finally, we conduct scenario and sensitivity analysis using representative grid emission profiles, electricity tariffs, fossil natural gas (FNG) tariffs, and assumed SCCs from across the United States. 

**Dynamic Energy Model.** Bolorinos et al. developed a hybrid physics and data-driven model of wastewater energy generation and consumption.[35] Their regularized linear model simulates how storage modulates a facility’s gross and net electricity demand and biogas production on a 15 min time scale, using historical mass and fluid flow data along with hour, weekday, and season covariates to understand temporal trends. We use a 24 h moving average of mass flow data and 6 lagged samples (1.5 h on 15 min intervals) of raw influent wastewater data since the digesters respond more slowly to changes in feed than the primary and secondary treatment trains. We assume that sludge production and the resulting biogas production change minimally under the 12 h maximum retention time constraint for wastewater storage and exclude changes to 

**2286** 

https://doi.org/10.1021/acs.est.4c09773 _Environ. Sci. Technol._ 2025, 59, 2285−2294 

**Environmental Science & Technology** 

**pubs.acs.org/est** 

Article 

sludge production from the dynamic model. We selecte hyperparameters through cross-validation that randomly assigns segments to training and test sets. 

The Bolorinos et al. model accounts for electricity consumption and generation but does not include the heating demand for anaerobic digestion. Operational changes could shift the heat generation from the cogenerator to the boiler and vice versa. Consequently, we extend the Bolorinos et al. model to account for fluctuating heat generation (Section S.4.1.1). Under the new heat constraints, we assume that the digester heat demand is supplemented by backup FNG boilers when heat production from the biogas cogenerator is insufficient. 

**Dynamic Emission Model.** The electricity and heat calculations from the dynamic energy model are inputs into our life cycle emission-accounting framework. The control optimization focuses on the subset of Scope 1 and Scope 2 emissions directly influenced by flexible operation over the lifetime of an upgrade. We use historical facility operational data both as a baseline for the emission calculations and to train the dynamic energy model used to simulate operation. 

_Scope 1 Emissions._ Direct gaseous emissions of N2O, CH4, and CO2 are converted to CO2-eq using their 100-year global warming potential (GWP), although we note that the total emissions are highly sensitive to the GWP time horizon (see Section S.2.5). We assume no change to fugitive emission factors from the biological processes within the treatment work due to uncertainty in the magnitude and direction of emission changes under dynamic operation[2][−][4] (Section S.3.4.1). Changes in Scope 1 emissions in our model are limited to changes in the volume of FNG combusted on-site and leakage of CH4 from the biogas holder and cogenerator. 

We apply constant emission factors to the volume of FNG purchased and the volume of wastewater or biogas stored in the problem formulation. Equation 1 computes _R_ Scope1; the reduction in Scope 1 emissions due to flexible operation in ton CO2-eq. _Y_ base and _Y_ opt are the baseline and optimized FNG combustion time series (in m[3] ), respectively. EIFNG is the emission intensity of FNG combustion (ton CO2-eq/m[3] ). 

**==> picture [229 x 32] intentionally omitted <==**

We then use eq S10 to calculate the change in Scope 1 emissions using a functional unit of 1 m[3] wastewater treated. Equation 1 is used with different baselines ( _Y_ base) at different stages of the framework. 

_Scope 2 Emissions._ We integrate the facility energy consumption model with electric grid emission data to calculate the change in Scope 2 emissions resulting from shifting and shedding the electricity load. We average grid emission data from de Chalendar et al. by hour and month during the study period (2018−2020)[41][,][42] (Section S.2.2). These monthly hourly averaged emission factors exhibit less volatility than 15 min marginal emission factors and ensure stability when deploying control algorithms.[43] 

Equation 2 is used to compute _R_ Scope2; the reduction in Scope 2 emissions due to flexible operation in ton CO2-eq. EIgrid(month _t_ , hour _t_ ) is the average grid emission intensity (ton CO2-eq/kWh) for hour _t_ during month _t_ . month _t_ and hour _t_ are the month and the hour at time _t_ , respectively. _X_ base( _t_ ) and _X_ opt( _t_ ) are the baseline and optimized electric grid purchase time series (in kWh), respectively. 

**==> picture [229 x 49] intentionally omitted <==**

We then use eq S13 to compute the change in Scope 2 emissions using a functional unit of 1 m[3] wastewater treated. Again, different baselines ( _X_ base) are used at different stages of the framework. 

_Scope 3 Emissions._ To account for the full life cycle impact of flexible operation, we incorporate Scope 3 emissions from three forms of storage: raw wastewater storage, biogas storage, and Li-ion battery storage. We estimate the average embodied emissions associated with the manufacturing and construction of energy storage systems through a literature review including national-scale and site-specific examples (Tables S.3.2, S.3.5, and S.3.6). Equation S14 uses these emissions factors to calculate ΔScope3 _i_ , the Scope 3 emissions equivalent per unit of treated wastewater over the lifetime of the upgrade “ _i_ ” in ton CO2-eq/m[3] (Section S.3). 

_Life Cycle Emissions._ We quantify the net change in emissions, Δ _Ei_ (eq 3), from facilities under various operating schema and upgrade scenarios (“ _i_ ”) in terms of emission equivalent per unit of treated wastewater [ton CO2-eq/m[3] ] by summing the change in emissions from Scope 1, 2, and 3 sources (eqs S10, S13, and S14) over the study period _T_ . 

**==> picture [222 x 13] intentionally omitted <==**

**Optimized Operation with Existing Infrastructure.** We first optimize electricity and FNG consumption (eq 4) with the existing infrastructure based on the market conditions (i.e., grid emission intensity profile, electricity and FNG tariffs, and SCC). For our case study facility with existing infrastructure, the only optimization variable is the cogenerator’s FNG usage. This initial optimization helps to disentangle the operational benefits of upgrades from the altered behavior incentivized by the changes in market conditions. 

**==> picture [207 x 62] intentionally omitted <==**

**==> picture [13 x 9] intentionally omitted <==**

where EIFNG and EIgrid (month _t_ , hour _t_ ) are as defined in eqs 1 and 2, _G_ ( _t_ ) = FNG cost ($/m[3] ), _k_ = SCC ($/ton CO2-eq), _E_ ( _t_ ) = electricity cost ($/kWh), _X_ ( _t_ ) = electric grid consumption (kWh), and _Y_ ( _t_ ) = FNG consumption (m[3] ). 

The change in emission intensity is calculated from time series data of historical electricity consumption, _X_ hist as _X_ base; historical FNG consumption, _Y_ hist as _Y_ base; electricity consumption optimized with existing infrastructure, _X_ opt,ex as _X_ opt; and FNG consumption optimized for existing infrastructure, _Y_ opt,ex as _Y_ opt. We plugged ΔScope1 and ΔScope2 into eq 3 with ΔScope3 _i_ set to zero when optimizing the existing infrastructure. 

**Optimized Operation with Energy Flexibility Upgrades.** We model and optimize the addition of storage to enhance energy flexibility and maximize reduction in wastewater facility emissions. While we account for Scope 3 emission implications of storage upgrades, we do not consider 

**2287** 

https://doi.org/10.1021/acs.est.4c09773 _Environ. Sci. Technol._ 2025, 59, 2285−2294 

**Environmental Science & Technology pubs.acs.org/est** Article 

**==> picture [503 x 326] intentionally omitted <==**

Figure 2. Representative historical time series data and storage-optimized facility operation from October 22nd-23rd, 2019 for our case study facility, Silicon Valley Clean Water. In the historical scenario, the facility has a cogenerator and no raw wastewater (RW), gas holder (GH), or battery (BY) storage capacity. For both the energy bill minimization (dashed line) and emission minimization scenarios (dotted line), the facility has an equivalently sized cogenerator, but the sizes of the RW, GH, and BY storage systems are optimally sized for each scenario. Cost-optimal and emission-optimal capacities are reported in Figure 3B. The sleeves represent 95% confidence intervals for the optimized simulations. (A) Historical − raw wastewater influent in m[3] /day. (B) CAISO average emission profile for October from 2018 2020 and the 2021 Pacific Gas & Electric (PG&E) energy charge ($/kWh). There is a monthly demand charge of 1.78 $/kW with the same peak hours that is not shown. (C) Net electricity demand in kW (i.e., grid electricity purchases) under historical, cost-optimized, and emission-optimized operation. (D) Electricity generation under historical, cost-optimized, and emission-optimized operation. (E) Biogas flaring rate in m[3] /day under historical, cost-optimized, and emissionoptimized operation. (F) State of storage for RW in m[3] for emission-optimized and cost-optimized operation. (G) State of storage for GH in m[3] for emission-optimized and cost-optimized operation. (H) State of storage for RW in kWh for emission-optimized and cost-optimized operation. 

other constraints (e.g., footprint) that might limit storage deployment. 

We identify cost- and emission-optimal storage types (raw wastewater storage, biogas storage, or battery storage) and sizes for a facility using grid search techniques (Section S.5). The objective function matches eq 4 with additional mass balance and upper bound constraints (Section S.4). Finally, we use the electricity and FNG consumption time series optimized with energy flexibility upgrades, _X_ opt,up and _Y_ opt,up respectively, to calculate the change in emissions from optimized operation with the upgrade. During sensitivity and scenario analysis, we standardize results in terms of load hour equivalents (LHEs) of storage capacity to ease comparison across diverse forms of energy storage. LHE is calculated using methods detailed in Bolorinos et al.[35] 

We differentiate between the cost-optimal and the emissionoptimal operating conditions by setting the SCC, _k_ = 0 for the cost-optimized case and setting the energy cost _E_ ( _X_ ) = 0 for the emission-optimized case. Costs and emissions can be cooptimized by using the true electricity tariff for _E_ ( _X_ ) and setting _k_ to the desired SCC. Unless otherwise noted, the cost 

of carbon used for co-optimization throughout the study is _k_ = $120 ton of CO2-eq.[46] 

**Case Study Facility Parameters.** We demonstrate this workflow for Silicon Valley Clean Water in Redwood City, CA. The case study facility is a publicly owned treatment work serving 200,000 customers with a treatment capacity of 29 million gallons per day (MGD) and an average flow of 13.5 MGD (51.1 megaliters/day).[44] While the municipality operates a separate stormwater system, it experiences a significant amount of inflow and infiltration, with wet weather − peak flows of 2 3 times normal flow. The facility is located in the PG&E service area with the B-20 tariff structure in which − there is a time of use charge from 4 9 PM, a concurrent peak hour demand charge of $1.78/kW during winter and $26.8/ kW during summer, and an all-day demand charge of $20.7/ kW. All demand charges are based on monthly energy demand maxima. The energy model uses 15 min operational data from September 2018 to December 2020. These data include metered energy consumption, wastewater volumetric flow, and sludge mass flow rates, biogas production, and heat and electricity generation from a 1.266 MW cogenerator. During 

**2288** 

https://doi.org/10.1021/acs.est.4c09773 _Environ. Sci. Technol._ 2025, 59, 2285−2294 

**==> picture [505 x 12] intentionally omitted <==**

**----- Start of picture text -----**<br>
Environmental Science & Technology pubs.acs.org/est Article<br>**----- End of picture text -----**<br>


**==> picture [503 x 241] intentionally omitted <==**

Figure 3. Greenhouse gas emission change when deploying and optimizing the use of energy storage for cost and emission reductions. (A) Emissions are broken down into direct fugitive emissions from methane leakage and FNG combustion (Scope 1), electric grid emissions (Scope 2), and embodied emissions of the energy flexibility upgrade (Scope 3). Four storage systems are modeled: raw wastewater (RW) storage tank, lowpressure biogas holder (GH), Li-ion battery (BY), and a combination of the three (RW + GH + BY). For each storage system, two scenarios are considered: cost-optimized (SCC = $0/ton CO2-eq) and emission-optimized (electricity cost = $0/kWh). The cost implications are shown in red. (B) Optimal storage capacities sized using a grid search in each scenario, with the sizes normalized to load hour equivalents (LHEs). 

the study period, the facility generated 60% of its electricity from biogas. Approximately 10% of biogas was flared due to cogenerator outages and misalignment of electricity demand and biogas production. The optimization framework is adaptable to different facility configurations, as the underlying linear models can be retrained using facility-specific historical data. 

**Scenario and Sensitivity Analysis.** We assess the generalizability of our findings by performing scenario analyses for fixed energy storage sizes of 1 and 2 LHE for each of the three storage types, a total of 12 upgrade scenarios. We also perform sensitivity analysis using electricity and FNG tariffs from the 100 largest wastewater facilities in the US[40] and emission intensities from 15 different US electric grid areas.[41][,][42] Finally, we vary the assumed SCC between $0 and $525/metric ton[45] (i.e., _k_ was varied in eq 4) to inform a marginal cost of carbon analysis (Section S.6). While varying the tariff structure and grid emission profiles, we use a constant SCC of $120/ton based on the EPA’s 2023 recommendation.[46] For sensitivity analysis of emission factors used throughout the model, see Section S.2.5. 

## ■ **[RESULTS]** 

**Dynamic Emission Model.** We observe a high variance in real-time carbon emissions from our case study facility. This results from variations in wastewater flow rate (Figure 2A), the emission intensity of the grid (Figure 2B), the price incentive for shifting load to off-peak hours (Figure 2B), and the instantaneous balance between facility energy demand (Figure 2C) and on-site energy generation (Figure 2D). Influent wastewater flow varies from 13,700 m[3] /day (3.62 MGD) to 95,500 m[3] /day (25.2 MGD). The emission intensity of the California Independent System Operator (CAISO) grid has 

seasonal and daily variation of up to 100 kg CO2/MWh and 125 kg CO2/MWh, respectively. In October, the PG&E tariff energy charge is 29.6% higher during peak periods, while the demand charge is 8.6% higher, incentivizing load shifting. Peak hour charges are higher during summer months and lower during winter months. The emissions and energy profiles are not aligned (e.g., at night the electricity price is lowest, while emissions are highest), so the optimization problem must account for trade-offs between the two incentive signals. 

Given this operating environment, we estimate a treatment emission intensity of 0.75 kg of CO2-eq/m[3] of water treated, for a total of 14 kiloton of CO2-eq/year. Of that annual total, Scope 1 is 7.4 kton of CO2-eq, Scope 2 is 1.0 kton of CO2-eq, and Scope 3 is 5.6 kton of CO2-eq Approximately 70% of the Scope 1 emissions are biological process-related rather than energy-related (Section S.2.4). Scope 2 emissions would be 3% higher if we did not account for the hourly and monthly variation in the emission intensity of the grid. The low Scope 2 baseline emissions for this case study facility stem from 65% of the electricity demand being generated via on-site cogeneration, with up to 9% FNG blended with biogas, and the remainder coming from California’s relatively low-emission grid (250 kg CO2-eq/MWh in CA versus 375 kg CO2-eq/ MWh national average). As a result, this case study represents a conservative estimate of the emission impact of flexible operation. Our results focus on changes to _energy-related emissions_ , which include Scope 2 emissions and 30% of Scope 1 emissions related to cogeneration. 

**Optimized Operation with Existing Infrastructure.** The operational objective function has a significant effect on the energy costs and Scope 2 emissions of the case study facility. In the absence of energy flexibility upgrades at the case study facility, optimizing the timing of electricity consumption could reduce energy costs by up to 2.6% (i.e., SCC = $0/ton 

**2289** 

https://doi.org/10.1021/acs.est.4c09773 _Environ. Sci. Technol._ 2025, 59, 2285−2294 

**Environmental Science & Technology** 

**pubs.acs.org/est** 

Article 

CO2-eq). An objective function seeking to minimize carbon emissions, without regard for electricity costs (i.e., electricity cost = $0/kWh), is expected to reduce facility emissions by 9.0%. This decrease primarily stems from a substitution of electricity sources, namely, decreased reliance on electricity generation from FNG and increased electricity purchase from the relatively low-emission intensity CAISO grid. 

**Optimized Operation with Energy Flexibility Upgrades.** Next, we explore the potential for further reductions in cost and emission intensity achievable through expanded onsite storage of raw wastewater, biogas, and electricity. To facilitate direct comparison between storage technologies, we evaluate the cost and emission benefits of capacity upgrades for the combination of storage types and each standalone storage type (Figure 3A). For each scenario, we identify the costoptimal and emission-optimal storage types and sizes (Figure 3B). The optimal storage capacity is very sensitive to the objective function, with optimal storage sizes varying by up to an order of magnitude between the emissions and cost-optimal cases. 

A 2-day period (October 22nd−23rd, 2019) of optimized operation using the optimized combination of storage capacities is shown in Figure 2C−H. On October 22nd, the net electricity demand did not follow the typical diurnal profile peaks in the early afternoon and evening due to a cogenerator outage in the middle of the day (Figure 2D). We intentionally selected this abnormal day to visualize the ability of flexible operation to manage fluctuations in biogas generation and demand and reduce flared gas and Scope 1 emissions. Besides a brief cogenerator outage, the facility operation was more typical on October 23rd. When the energy storage capacity and operation of the facility are optimized for costs on a typical day, the net demand is kept flat throughout the day to avoid demand charges (Figure 2C). By contrast, the facility has a large demand peak during minimum emission hours in the emission-optimized scenario. 

The state of storage in Figure 2F−H highlights the operational differences between the cost- and emissionoptimized scenarios. In the cost-optimized scenario, the battery is charged earlier on October 22nd and discharged during the cogenerator outage to decrease peak demand (Figure 2H). By contrast, the battery in the emissionoptimized scenario is charged later in the day when the emission intensity of electricity is lower. The timing of raw wastewater storage use is similar across the two scenarios, but the storage utilization is higher in the emission-optimized scenario (Figure 2F). While both cost-optimal and emissionoptimal operations involve storing biogas during the cogenerator outage to minimize flaring and maximize energy recovery (Figure 2G), biogas flaring is more successfully mitigated in the emission-optimal scenario due to the larger storage capacity (Figure 2E). 

**Life Cycle Emission Trade-offs from Energy Flexibility Upgrades.** We compare the annual average life cycle emission impacts of cost-optimal and emission-optimal design and operation of facilities with expanded energy flexibility in Figure 3A. Cost-optimal operation using existing storage infrastructure increases energy-related emissions by 10.7% (or 7.61 g CO2-eq/m[3] wastewater treated) compared to historical emissions. When flexibility directly reduces flaring (i.e., the gas holder scenario), the cost-optimal operation also reduces emissions due to an increase in gross on-site electricity generation. In other scenarios, the cost-optimal operation with 

expanded storage further increases emissions because PG&E electricity tariffs are not aligned with CAISO emission intensity for this case study facility. For example, cost-optimized operation with a battery reduces Scope 2 but increases Scope 1 emissions by importing FNG to produce lower cost electricity with the cogenerator. This increase is further exacerbated by Scope 3 emissions of the battery. 

In contrast to cost-optimized upgrades and operational strategies, emission-optimized energy flexibility upgrades offer significant additional benefits for emission reduction benefits. Optimized energy flexibility upgrades yield an additional 2−8% energy-related emission reduction on top of the 9% reduction without infrastructure upgrades. The largest life cycle emission decreases are achieved using raw wastewater storage (16.8% or 12.0 g CO2-eq/m[3] wastewater treated). 

In all the emission-optimized cases, however, the resulting emission decreases incurred large financial losses from increased energy bills. The emission-optimal raw wastewater storage scenario incurred an 87.9% increase in the facility’s energy bill compared to historical operation. This is equivalent to an average marginal cost of $7,100/ton CO2-eq, suggesting a low likelihood of achieving this degree of carbon emissions in practice. A more realistic scenario with a flat tariff and $120/ ton CO2-eq SCC is investigated in Section S.7. 

Finally, we consider the trade-offs in cost and emission intensity using a multiobjective optimization formulation with SCC ranging from $0 to $525/ton CO2-eq (Figure 4A). The three storage systems are compared at 1 and 2 LHE capacities (as opposed to the cost- or emission-optimized capacities from Figures 2 and 3) to fairly compare the impact of optimization across SCCs. Despite being equivalently sized, the energy flexibility upgrades have different trade-off curves due to the different ways in which they interact with system dynamics. For example, operating the 2 LHE gas holder under a SCC of $120/ton CO2-eq achieves nearly all the reduction that would be achieved at $525/ton CO2-eq. Battery operation does not reduce emissions as much at $120/CO2-eq, but it has the largest range in its trade-off curve, indicating that it is more sensitive to the SCC. Flexible operation of raw wastewater storage has the least potential for emission reduction for the SCCs analyzed, a stark contrast to the 100% emissionoptimized result in Figure 3A, when raw wastewater showed the largest emission reduction potential. 

**Scenario and Sensitivity Analysis.** Given the sensitivity of the facility’s optimal emissions to both grid emission intensity and tariffs, we perform sensitivity analysis by simulating operation in other markets. We apply electricity and FNG tariffs from the 100 largest wastewater facilities in the US with CAISO grid emissions and 15 grid emission profiles across the US with PG&E tariffs with a 2 LHE battery. We compare the percent emission reduction for optimized operation versus unoptimized operation in the same market (Figure 4B). We chose a 2 LHE battery since it has the largest range of emissions in Figure 4A. 

When optimizing with a $120/ton CO2-eq SCC, there is always a cost reduction versus unoptimized operation. Conversely, there is a wide variation in the percent change in energy-related emissions from negative to positive. As seen from the star representing our case study, California is near the median in terms of percent change in energy-related costs and emissions, indicating that some markets have more and some less potential for cost-effective emission reductions through flexible operation. For example, maintaining the CAISO grid 

**2290** 

https://doi.org/10.1021/acs.est.4c09773 _Environ. Sci. Technol._ 2025, 59, 2285−2294 

**Environmental Science & Technology** 

**pubs.acs.org/est** 

Article 

**==> picture [239 x 613] intentionally omitted <==**

Figure 4. Annual energy-related costs and emissions at a wastewater facility under different storage, rate, and grid emission intensity values. (A) Trade-off curve between energy-related emissions and costs resulting from energy flexibility in a wastewater facility in the San Francisco Bay Area. 1 and 2 load hour equivalents (LHEs) of different energy storage systems (raw wastewater storage (RW), low-pressure biogas holder (GH), and Li-ion battery (BY)) are compared to 

## Figure 4. continued 

optimization of existing infrastructure (EX) under the actual Pacific Gas & Electric (PG&E) rate structure as of November 2021.[40] Each curve represents the results of optimizing both electricity and fossil natural gas (FNG) consumption using a social cost of carbon (SCC) ranging from $0 to $525. The points on each curve represent a SCC of $120/ton CO2-eq. The triangle indicates energy-related emissions and costs for historical operation. (B) Impact of market forces on optimal energy-related emissions and costs is represented as a percentage compared to unoptimized operation examined by (i) simulating the case study facility with a 2 LHE battery under the rate structures for the largest 100 wastewater facilities in the US with a SCC of $120/ton CO2-eq and CAISO emission intensities and (ii) simulating the case study facility with a 2 LHE battery, the emission intensities of 15 different grids across the US, PG&E tariffs, and a $120/ton CO2-eq SCC. The star indicates the optimized operation under the real-life energy tariffs and grid emission intensity of the case study facility (PG&E and CAISO) with a $120/ton CO2-eq SCC. Two examples are highlighted, Nashville Electric Service (NES) and CAISO from varying tariffs and PG&E and Louisville Gas & Electric and Kentucky Utilities Energy (LGEE) from varying grid mix. (C) Marginal cost curves for BY, GH, and RW in both 1 and 2 LHE capacities compared to a $120/ton CO2-eq SCC. Due to the fitting procedure, marginal costs are only valid for the domain of the raw data ($0-$525/ton CO2-eq). 

mix but using the Nashville Electric Service (NES) tariff achieves an additional 7.9% emission reduction (104 tons CO2-eq/year) with only a 5.6% increase in costs ($57,000/ year) compared to the optimized operation under the PG&E tariff. Optimizing the Louisville Gas & Electric and Kentucky Utilities Energy (LGEE) grid mix with PG&E rates leads to a 3.4% increase in emissions (45 tons CO2-eq/year) with virtually no change in costs. For context, the average CAISO power plant has an emission intensity of 245 kg CO2-eq/ MWh. 

Finally, we reformulate the results from the trade-off curve to examine the average marginal cost of CO2 reductions between cost-optimal and emission-optimal operation (Figure 4C). Over the sweep between a SCC of $0 and $525/ton CO2eq, the average marginal costs are $254/ton CO2-eq, $80/ton CO2-eq, and $102/ton CO2-eq for the 1 LHE raw wastewater storage tank, gas holder, and battery, respectively. 

## ■ **[DISCUSSION]** 

Wastewater treatment accounts for 75% of air emission damages from the US water sector for an estimated value of $1.63 billion in the Clean Watershed Needs Survey from 2012.[21][,][47] A significant fraction of these emissions are Scope 2 emissions stemming from electricity consumed in facility processes, especially pumping and aeration. While processbased efficiency audits commonly yield Scope 2 emission reductions at wastewater facilities, the magnitude of these emission reduction benefits is likely to be modest compared to those available through load shifting. Further, we expect the variability in the emission intensity of regional grids across the US and the rest of the world to increase with an increase in renewable capacity. 

Our reported results for optimizing the flexible operation of existing infrastructure are comparable to those of the previous literature. Reifsnyder et al. found potential for up to 8.5 and 4.5% reduction in operating costs and electricity-related emissions, respectively.[29] Sweetapple et al. found the potential 

**2291** 

https://doi.org/10.1021/acs.est.4c09773 _Environ. Sci. Technol._ 2025, 59, 2285−2294 

**Environmental Science & Technology** 

**pubs.acs.org/est** 

Article 

for 10.0% reduction in electricity-related emissions without increasing operating costs.[23] We find 2.6% energy bill savings optimizing costs and 9.0% energy-related emission reduction optimizing the existing cogeneration infrastructure for our specific case study facility. 

We find additional opportunity for reducing emissions and operating costs through optimized infrastructure upgrades. Reductions of up to 20.7% in energy costs and 16.8% in energy-related emissions can be achieved at our case study facility in the CAISO/PG&E service areas when the timing of grid electricity purchases is optimized separately. Were our case study facility to be located in the LGEE service area, these emission saving opportunities grow to between 13.0% (existing infrastructure) and 24.3% (upgraded energy flexibility infrastructure). These reductions are greatly diminished when cooptimizing for both cost and emissions, even when accounting for reasonable SCCs. 

Despite the physical potential for carbon savings through energy flexibility, we identify serious financial barriers under PG&E tariff structures and current values for the SCC. Realizing the maximum 16.8% emission reduction at our case study facility was associated with an 87.9% increase in electricity costs. This tension is a direct result of the misalignment of the electric grid emission profile and electricity tariffs in the CAISO/PG&E service area, but similar conditions exist whenever there are large spreads in peak and off-peak hours that do not track the emission intensity of the grid. In service areas where tariffs are flat, and/or there is no demand charge, these trade-offs would be substantially reduced or eliminated. Where grid electricity is more emission-intensive than combusting FNG on-site, there is the potential for increased FNG imports to reduce facility emissions. 

Our multiobjective optimization framework helps facility operators balance GHG emission reductions and energy costs by leveraging energy storage. Additional work is needed to incorporate other key operational objectives, like treatment reliability or effluent water quality, and include the contributions of both energy flexibility mechanisms and process efficiency from the wastewater treatment process itself (e.g., aeration controls). Scope 2 reductions also offer air quality benefits that could be incorporated into a broader framework for evaluating the benefits of energy flexibility.[21][,][48] A growing number of cities in the US are developing climate action plans, and energy-flexible operation provides a lowinvestment option for modest Scope 2 emission reductions. Digital solutions, such as our optimization framework coupled with reliable automated controls, provide an opportunity for cities to meet those goals with minimal capital upgrades or burden on operators. 

## ■ **[ASSOCIATED][CONTENT]** 

## * **sı Supporting Information** 

The Supporting Information is available free of charge at https://pubs.acs.org/doi/10.1021/acs.est.4c09773. 

Wastewater sector emissions in the US, existing facility emission parameters, added storage system emission parameters, optimization problem formulation, grid search for optimal storage capacity, marginal cost calculation, and optimization with flat tariff (PDF) 

## ■ **[AUTHOR][INFORMATION]** 

## **Corresponding Author** 

- Meagan S. Mauter − _Department of Civil and Environmental Engineering, Stanford University, Stanford, California 94305, United States; Environmental Social Sciences, Senior Fellow, Woods Institute for the Environment, and Senior Fellow, Precourt Institute for Energy, Stanford University, Stanford, California 94305, United States; Photon Science, SLAC National Accelerator Laboratory, Menlo Park, California 94025, United States;_ orcid.org/0000-0002-4932-890X; Email: mauter@stanford.edu 

## **Authors** 

- Fletcher T. Chapin − _Department of Civil and Environmental Engineering, Stanford University, Stanford, California 94305, United States;_ orcid.org/0000-0002-2165-7963 

- Daly Wettermark − _Department of Civil and Environmental Engineering, Stanford University, Stanford, California 94305, United States;_ orcid.org/0000-0001-7151-2765 

- Jose Bolorinos − _Department of Civil and Environmental Engineering, Stanford University, Stanford, California 94305, United States;_ orcid.org/0000-0002-3741-5483 

Complete contact information is available at: https://pubs.acs.org/10.1021/acs.est.4c09773 

## **Author Contributions** 

All authors have given approval to the final version of the manuscript. F.T.C.: conceptualization, methodology, software, and writing (original draft). D.W.: methodology, writing (original draft), and writing (review and editing). J.B.: conceptualization, methodology, software, writing (review and editing), and supervision. M.S.M.: conceptualization, methodology, writing (review and editing), funding acquisition, and supervision. 

## **Notes** 

The authors declare no competing financial interest. 

## ■ **[ACKNOWLEDGMENTS]** 

We thank the staff at our case study facility Silicon Valley Clean Water, especially Alexandre Miot and Gurpal Sandhu for their help in collecting data and explaining facility operation. We also thank Jacques de Chalendar for his responsiveness to inquiries and Corisa Wong for her feedback. This material is based upon work supported by the US Department of Energy, Office of Energy Efficiency and Renewable Energy, Advanced Manufacturing Office under Award Number DE-EE0009499. 

## ■ **[ABBREVIATIONS]** 

GHG, greenhouse gas; LCA, life cycle assessment; FNG, fossil natural gas; SCC, social cost of carbon; LHE, load hour equivalent; MGD, million gallons per day; CAISO, California Independent System Operator; PG&E, Pacific Gas & Electric; NES, Nashville Electric Service; LGEE, Louisville Gas & Electric and Kentucky Utilities Energy 

## ■ **[REFERENCES]** 

(1) Neethling, J. B.; Kennedy, H. _Nutrient Reduction Study: Potential Nutrient Reduction by Treatment Optimization, Sidestream Treatment, Treatment Upgrades, and Other Means_ Bay Area Clean Water Agencies: Walnut Creek, CA; 2018. 

(2) Song, C.; Zhu, J.-J.; Willis, J. L.; Moore, D. P.; Zondlo, M. A.; Ren, Z. J. Methane Emissions from Municipal Wastewater Collection 

**2292** 

https://doi.org/10.1021/acs.est.4c09773 _Environ. Sci. Technol._ 2025, 59, 2285−2294 

**Environmental Science & Technology** 

**pubs.acs.org/est** 

Article 

and Treatment Systems. _Environ. Sci. Technol._ 2023, _57_ (6), 2248− 2261. 

(3) Song, C.; Zhu, J.-J.; Willis, J. L.; Moore, D. P.; Zondlo, M. A.; Ren, Z. J. Oversimplification and Misestimation of Nitrous Oxide Emissions from Wastewater Treatment Plants. _Nat. Sustainability_ 2024, _7_ , 1348. 

(4) Moore, D. P.; Li, N. P.; Wendt, L. P.; Castaneda, S. R.; Falinski, M. M.; Zhu, J.-J.; Song, C.; Ren, Z. J.; Zondlo, M. A. Underestimation of Sector-Wide Methane Emissions from United States Wastewater Treatment. _Environ. Sci. Technol._ 2023, _57_ (10), 4082−4090. 

(5) _Inventory of U.S. Greenhouse Gas Emissions and Sinks: 1990_ − _2021_ U.S. Environmental Protection Agency: 2023. 

(6) Zib, L.; Byrne, D. M.; Marston, L. T.; Chini, C. M. Operational Carbon Footprint of the U.S. Water and Wastewater Sector’s Energy Consumption. _J. Cleaner Prod._ 2021, _321_ , No. 128815. 

(7) Singh, P.; Kansal, A. Energy and GHG Accounting for Wastewater Infrastructure. _Resour. Conserv. Recycl._ 2018, _128_ , 499− 507. 

(8) McCarty, P. L.; Bae, J.; Kim, J. Domestic Wastewater Treatment as a Net Energy Producer−Can This Be Achieved? _Environ. Sci. Technol._ 2011, _45_ (17), 7100−7106. 

(9) Sanders, K. T.; Webber, M. E. Evaluating the Energy Consumed for Water Use in the United States. _Environ. Res. Lett._ 2012, _7_ (3), No. 034034. 

(10) Copeland, C.; Carter, N. T. Energy-Water Nexus: The Water Sector’s Energy Use 2017 https://sgp.fas.org/crs/misc/R43200.pdf (accessed December 05, 2021). 

(11) Kyung, D.; Kim, M.; Chang, J.; Lee, W. Estimation of Greenhouse Gas Emissions from a Hybrid Wastewater Treatment Plant. _J. Cleaner Prod._ 2015, _95_ , 117−123. 

(12) Miller-Robbie, L.; Ulrich, B. A.; Ramey, D. F.; Spencer, K. S.; Herzog, S. P.; Cath, T. Y.; Stokes, J. R.; Higgins, C. P. Life Cycle Energy and Greenhouse Gas Assessment of the Co-Production of Biosolids and Biochar for Land Application. _J. Cleaner Prod._ 2015, _91_ , 118−127. 

(13) Raheem, A.; Sikarwar, V. S.; He, J.; Dastyar, W.; Dionysiou, D. D.; Wang, W.; Zhao, M. Opportunities and Challenges in Sustainable Treatment and Resource Reuse of Sewage Sludge: A Review. _Chem. Eng. J._ 2018, _337_ , 616−641. 

(14) Seiple, T. E.; Coleman, A. M.; Skaggs, R. L. Municipal Wastewater Sludge as a Sustainable Bioresource in the United States. _J. Environ. Manage._ 2017, _197_ , 673−680. 

(15) Chai, C.; Zhang, D.; Yu, Y.; Feng, Y.; Wong, M. Carbon Footprint Analyses of Mainstream Wastewater Treatment Technologies under Different Sludge Treatment Scenarios in China. _Water_ 2015, _7_ (3), 918−938. 

(16) Pang, C.; Luo, X.; Rong, B.; Nie, X.; Jin, Z.; Xia, X. Carbon Emission Accounting and the Carbon Neutralization Model for a Typical Wastewater Treatment Plant in China. _Int. J. Environ. Res. Public. Health_ 2023, _20_ (1), 140. 

(17) Awaitey, A. Carbon Footprint of Finnish Wastewater Treatment Plants, Masters Thesis; Aalto University School of Engineering: Epsoo, Finland, 2021. 

(18) American Society of Civil Engineers. Infrastructure Report Card 2021 https://infrastructurereportcard.org/wp-content/uploads/ 2020/12/Wastewater-2021.pdf (accessed June 24, 2024). 

(19) Duan, H.; Zhao, Y.; Koch, K.; Wells, G. F.; Zheng, M.; Yuan, Z.; Ye, L. Insights into Nitrous Oxide Mitigation Strategies in Wastewater Treatment and Challenges for Wider Implementation. _Environ. Sci. Technol._ 2021, _55_ (11), 7208−7224. 

(20) Gruber, W.; Magyar, P. M.; Mitrovic, I.; Zeyer, K.; Vogel, M.; von Känel, L.; Biolley, L.; Werner, R. A.; Morgenroth, E.; Lehmann, M. F.; Braun, D.; Joss, A.; Mohn, J. Tracing N2O Formation in FullScale Wastewater Treatment with Natural Abundance Isotopes Indicates Control by Organic Substrate and Process Settings. _Water Res. X_ 2022, _15_ , No. 100130. 

(21) Gingerich, D. B.; Mauter, M. S. Air Emission Reduction Benefits of Biogas Electricity Generation at Municipal Wastewater Treatment Plants. _Environ. Sci. Technol._ 2018, _52_ (3), 1633−1643. 

(22) Strazzabosco, A.; Kenway, S. J.; Lant, P. A. Solar PV Adoption in Wastewater Treatment Plants: A Review of Practice in California. _J. Environ. Manage._ 2019, _248_ , No. 109337. 

(23) Sweetapple, C.; Fu, G.; Butler, D. Multi-Objective Optimisation of Wastewater Treatment Plant Control to Reduce Greenhouse Gas Emissions. _Water Res._ 2014, _55_ , 52−62. 

(24) Kim, D.; Bowen, J. D.; Ozelkan, E. C. Optimization of Wastewater Treatment Plant Operation for Greenhouse Gas Mitigation. _J. Environ. Manage._ 2015, _163_ , 39−48. 

(25) Liao, J.; Li, S.; Liu, Y.; Mao, S.; Tian, T.; Ma, X.; Li, B.; Qiu, Y. Multi-Objective Optimization Based on Simulation Integrated Pareto Analysis to Achieve Low-Carbon and Economical Operation of a Wastewater Treatment Plant. _Water_ 2024, _16_ (7), 995. 

(26) Topuz, N.; Alsmeyer, F.; Okutan, H. C.; Roos, H.-J. Role of Flexible Operation of a Wastewater Treatment Plant in the Reduction of Its Indirect Carbon Dioxide Emissions − A Case Study. _Water_ 2024, _16_ (3), 483. 

(27) Thompson, L.; Lekov, A. B.; McKane, A. T.; Piette, M. A.Opportunities for Open Automated Demand Response in Wastewater Treatment Facilities in California − Phase II Report. San Luis Rey Wastewater Treatment Plant Case Study, 2010. 

(28) Aghajanzadeh, A.; Wray, C.; McKane, A.Opportunities for Automated Demand Response in California Wastewater Treatment Facilities, 2015. 

(29) Reifsnyder, S.; Cecconi, F.; Rosso, D. Dynamic Load Shifting for the Abatement of GHG Emissions, Power Demand, Energy Use, and Costs in Metropolitan Hybrid Wastewater Treatment Systems. _Water Res._ 2021, _200_ , No. 117224. 

(30) Olsen, D.; Goli, S.; Faulkner, D.; McKane, A.Opportunities for Automated Demand Response in Wastewater Treatment Facilities in California - Southeast Water Pollution Control Plant Case Study, 2012. 

(31) Filipe, J.; Bessa, R. J.; Reis, M.; Alves, R.; Póvoa, P. Data-Driven Predictive Energy Optimization in a Wastewater Pumping Station. _Appl. Energy_ 2019, _252_ , No. 113423. 

(32) Póvoa, P.; Oehmen, A.; Inocencio, P.; Matos, J. S.; Frazao, A. Modelling Energy Costs for Different Operational Strategies of a Large Water Resource Recovery Facility. _Water Sci. Technol._ 2017, _75_ (9), 2139−2148. 

(33) Brok, N. B.; Munk-Nielsen, T.; Madsen, H.; Stentoft, P. A. Unlocking Energy Flexibility of Municipal Wastewater Aeration Using Predictive Control to Exploit Price Differences in Power Markets. _Appl. Energy_ 2020, _280_ , No. 115965. 

(34) Giberti, M.; Dereli, R. K.; Flynn, D.; Casey, E. Predicting Wastewater Treatment Plant Performance during Aeration Demand Shifting with a Dual-Layer Reaction Settling Model. _Water Sci. Technol._ 2020, _81_ (7), 1365−1374. 

(35) Bolorinos, J.; Mauter, M. S.; Rajagopal, R. Integrated Energy Flexibility Management at Wastewater Treatment Facilities. _Environ. Sci. Technol._ 2023, _57_ (46), 18362−18371. 

(36) Musabandesu, E.; Loge, F. Load Shifting at Wastewater Treatment Plants: A Case Study for Participating as an Energy Demand Resource. _J. Cleaner Prod._ 2021, _282_ , No. 124454. 

(37) Zohrabian, A.; Plata, S. L.; Kim, D. M.; Childress, A. E.; Sanders, K. T. Leveraging the Water-energy Nexus to Derive Benefits for the Electric Grid through Demand-side Management in the Water Supply and Wastewater Sectors. _Wiley Interdiscip. Rev.: Water_ 2021, _8_ (3), No. e1510, DOI: 10.1002/wat2.1510. 

(38) Kirchem, D.; Lynch, M. A.; Bertsch, V.; Casey, E. Modelling Demand Response with Process Models and Energy Systems Models: Potential Applications for Wastewater Treatment within the EnergyWater Nexus. _Appl. Energy_ 2020, _260_ , No. 114321. 

(39) Nakkasunchi, S.; Hewitt, N. J.; Zoppi, C.; Brandoni, C. A Review of Energy Optimization Modelling Tools for the Decarbonisation of Wastewater Treatment Plants. _J. Cleaner Prod._ 2021, _279_ , No. 123811. 

(40) Chapin, F. T.; Bolorinos, J.; Mauter, M. S. Electricity and Natural Gas Tariffs at United States Wastewater Treatment Plants. _Sci. Data_ 2024, _11_ (1), 113. 

**2293** 

https://doi.org/10.1021/acs.est.4c09773 _Environ. Sci. Technol._ 2025, 59, 2285−2294 

**Environmental Science & Technology** 

**pubs.acs.org/est** 

Article 

(41) de Chalendar, J. A.; Taggart, J.; Benson, S. M. Tracking Emissions in the US Electricity System. _Proc. Natl. Acad. Sci. U.S.A._ 2019, _116_ (51), 25497−25502. 

(42) de Chalendar, J. A.; Benson, S. M. A Physics-Informed Data Reconciliation Framework for Real-Time Electricity and Emissions Tracking. _Appl. Energy_ 2021, _304_ , No. 117761. 

(43) Siler-Evans, K.; Azevedo, I. L.; Morgan, M. G. Marginal Emissions Factors for the U.S. Electricity System. _Environ. Sci. Technol._ 2012, _46_ (9), 4742−4748. 

(44) Wolfe, B. H. Tentative Order No. R2-2018-00XX. https:// www.waterboards.ca.gov/sanfranciscobay/board_info/agendas/ 2018/February/SiliconValley/SVCW_Tentative_Order.pdf. 

(45) Tol, R. S. J. Social Cost of Carbon Estimates Have Increased over Time. _Nat. Clim. Change_ 2023, _13_ (6), 532−536. 

(46) _Report on the Social Cost of Greenhouse Gases: Estimates Incorporating Recent Scientific Advances; Technical Report EPA-HQOAR-2021-0317_ U.S. Environmental Protection Agency: Washington, DC; 2023. 

(47) Gingerich, D. B.; Mauter, M. S. Air Emissions Damages from Municipal Drinking Water Treatment Under Current and Proposed Regulatory Standards. _Environ. Sci. Technol._ 2017, _51_ (18), 10299− 10306. 

(48) Global Water Intelligence. Mapping Water’s Carbon Footprint: Our Net Zero Future Hinges on Wastewater 2022 https://my. globalwaterintel-insights.com/l/2DC/carbonfootprintwp. 

**==> picture [241 x 324] intentionally omitted <==**

**2294** 

https://doi.org/10.1021/acs.est.4c09773 _Environ. Sci. Technol._ 2025, 59, 2285−2294 

