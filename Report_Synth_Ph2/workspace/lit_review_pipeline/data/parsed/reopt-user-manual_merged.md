## **The REopt Web Tool User Manual** 

_**Kate Anderson, Dan Olis, Bill Becker, Linda Casson, Nick Laws, Xiangkun Li, Sakshi Mishra, Ted Kwasnik, Andrew Jeffery, Emma Elgqvist, Kathleen Krah, Dylan Cutler, Alex Zolan, Nick Muerdter, Rob Eger, Andy Walker, Chris Hampel, Gregg Tomberlin, Amanda Farthing, Jeffrey Marqusee, Hallie Dunham, Byron Pullutasig**_ 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **Acknowledgments** 

We gratefully acknowledge the many people whose efforts contributed to this report. The REopt[®] web tool is based on the National Renewable Energy Laboratory’s (NREL’s) REopt[®] model, which has benefited from the expertise of many contributors and advisors over the years. We thank the vast number of current and past NREL employees on and beyond the REopt team who have contributed to data and model development, testing, and analysis, especially Nick DiOrio and Josiah Pohl. We also thank Alexandra Newman and Rob Braun of Colorado School of Mines for their contributions to optimization model development and the combined heat and power module. The model has been improved through the guidance and review provided by Nate Blair, Craig Christensen, Ben Polly, Ben Sigrin, Jie Zhang, Moncef Krarti, Rob Braun, Robert Brigantic, Tim McDowell, Mike Coddington, and Adam Warren, as well as the U.S. Department of Energy (DOE) REopt Advisory Board. We are grateful to all those who helped sponsor The REopt web tool development and analysis, especially Rachel Shepherd of the DOE Office of Energy Efficiency and Renewable Energy Federal Energy Management Program and Meegan Kelly of the DOE Industrial Technologies Office as well as DOE’s Solar Energy Technology Office and the Department of Defense’s Environmental Security Technology Certification Program. 

iii 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **List of Acronyms** 

|AC|alternating current|
|---|---|
|AMO|Advanced Manufacturing Office|
|AOP|annual operating plan|
|API|Application Programming Interface|
|AVERT|AVoided Emissions and geneRation Tool|
|CAPEX|capital expenditure|
|CBI|capital cost-based incentives|
|CHP|combined heat and power|
|CO2|carbon dioxide|
|CO2e|carbon dioxide equivalent|
|COP|coefficient of performance|
|CRB|Commercial Reference Building|
|DC|direct current|
|DER|distributed energy resource|
|DOE|Department of Energy|
|DOMHW|domestic hot water|
|EIA|Energy Information Administration|
|EPA|Environmental Protection Agency|
|ESPC|energy savings performance contract|
|GHP|geothermal heat pump|
|GHX|geothermal heat exchanger|
|HHV|higher heating value|
|IRR|internal rate of return|
|ISO|International Organization for Standardization|
|ITC|investment tax credit|
|JSON|JavaScript Object Notation|
|LID|light-induced degradation|
|MACRS|Modified Accelerated Cost Recovery System|
|NIST|National Institute of Standards and Technology|
|NREL|National Renewable Energy Laboratory|
|O&M|operations and maintenance|
|PBI|production-based incentive|
|PPA|power purchase agreement|
|PV|solar photovoltaics|
|RE|renewable energy|
|SAM|System Advisor Model|
|SOC|state of charge|
|T&D|transmission and distribution|
|TES|thermal energy storage|
|UESC|utility energy service contract|
|URDB|Utility Rate Database|
|WAHP/WSHP|Water-to-air heat pump, a.k.a. Water-sourced heat pump|
|WIND|Wind Integration National Dataset|



iv 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **Executive Summary** 

The REopt web tool evaluates the economic viability of grid-connected solar photovoltaics, wind, combined heat and power, geothermal heat pumps, and electric and thermal storage at commercial and small industrial sites. It allows facility owners to identify the system sizes and dispatch strategies that minimize the site’s life cycle cost of energy. The REopt web tool also estimates the amount of time on-site generation and storage can sustain the site's critical load during a grid outage and allows the user the choice of optimizing for energy resilience or clean energy goals. It is primarily used to inform project development decisions and to support research on the factors that drive project feasibility for market development and policy analysis. It is available through a web interface, application programing interface, and open-source code. 

This user manual provides an overview of the model, including its capabilities and typical applications; inputs and outputs; economic calculations; technology descriptions; and model parameters, variables, and equations. The model is highly flexible and is continually evolving to meet the needs of each analysis. Therefore, this report is not an exhaustive description of all capabilities, but rather a summary of the core components of the model. Tutorials that guide - users through the tool inputs and results are available here: https://reopt.nrel.gov/user guides.html. A user forum discussion board with questions and answers concerning using the REopt optimization tool can be found here: REopt Web Tool User Forum. 

v 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **Table of Contents** 

|**1**|**Introduction ......................................................................................................................................... 13**|**Introduction ......................................................................................................................................... 13**|
|---|---|---|
||1.1 Applications ................................................................................................................................ 13||
||1.1.1<br>What Questions Does The REopt Web Tool Answer? .................................................. 14||
||1.1.2<br>What Questions Does The REopt Web Tool NOT Answer? ......................................... 14||
||1.1.3<br>Who Uses The REopt Web Tool? .................................................................................. 14||
||1.1.4<br>How Does The REopt Web Tool Compare with Other Models? ................................... 15||
||1.2 Accessing The|REopt Web Tool ................................................................................................. 15|
||1.3 Citing The REopt Web Tool ....................................................................................................... 16||
||1.4 Feedback...................................................................................................................................... 16||
|**2**|**General Description ........................................................................................................................... 16**||
||2.1 Technology Models ..................................................................................................................... 17||
||2.2 Formulation ................................................................................................................................. 19||
||2.3 Temporal Resolution ................................................................................................................... 20||
|**3**|**Getting Started .................................................................................................................................... 20**||
||3.1 Logging In ................................................................................................................................... 20||
||3.1.1<br>User Dashboard .............................................................................................................. 21||
||3.1.2<br>Custom Load Profiles ..................................................................................................... 21||
||3.1.3<br>Custom Rates ................................................................................................................. 21||
||3.2 New Evaluation ........................................................................................................................... 21||
||3.2.1<br>Step 0:|Gathering Data ................................................................................................... 21|
||3.2.2<br>Step 1:|Choose Your Focus ............................................................................................ 22|
||3.2.3<br>Step 2:|Select Technologies ........................................................................................... 22|
||3.2.4<br>Step 3:|Enter Data .......................................................................................................... 22|
||3.3 International Use ......................................................................................................................... 23||
||3.3.1<br>Site Location & Utility Rate ........................................................................................... 23||
||3.3.2<br>Currency ......................................................................................................................... 24||
||3.3.3<br>Load Profile .................................................................................................................... 24||
||3.3.4<br>Financial Information ..................................................................................................... 24||
||3.3.5<br>Solar Production Data .................................................................................................... 24||
||3.3.6<br>Wind Resource Data ....................................................................................................... 24||
||3.3.7<br>Ground Thermal Conductivity Data for GHP ................................................................ 24||
||3.3.8<br>Ambient Temperature .................................................................................................... 25||
||3.3.9<br>Grid Emissions ............................................................................................................... 25||
||3.4 Solver Settings ............................................................................................................................. 25||
|**4**|**Economic Model ................................................................................................................................. 25**||
||4.1 Definitions, Inputs, and Assumptions ......................................................................................... 26||
||4.2 Ownership Models ...................................................................................................................... 27||
||4.3 Economic Incentives ................................................................................................................... 29||
||4.3.1<br>Capital Cost Based Incentives ........................................................................................ 29||
||4.3.2<br>Production Based Incentives .......................................................................................... 29||
||4.4 Tax Policies ................................................................................................................................. 30||
|**5**|**Existing Facility Infrastructure .......................................................................................................... 30**||
||5.1 Utility Services ............................................................................................................................ 30||
||5.2 Heating System ........................................................................................................................... 30||
||5.3 Cooling System ........................................................................................................................... 31||
||5.4 Land and Roof|Area Available .................................................................................................... 33|
|**6**|**Electricity and Fuel**|**Tariffs ................................................................................................................. 33**|
||6.1 Electric Rate Tariff ...................................................................................................................... 33||
||6.1.1<br>CHP Standby Charge ..................................................................................................... 35||



vi 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

||6.1.2<br>Compensation for Exported Electricity .......................................................................... 36|6.1.2<br>Compensation for Exported Electricity .......................................................................... 36|
|---|---|---|
||6.2 Fuel Costs .................................................................................................................................... 37||
|**7**|**Loads ................................................................................................................................................... 37**||
||7.1 Actual (Custom) Load Profile ..................................................................................................... 37||
||7.2 Simulated Load Profile from Models .......................................................................................... 38||
||7.2.1<br>Modeling|a Campus with Multiple Simulated Building Load Profiles .......................... 40|
||7.3 Electric Loads .............................................................................................................................. 40||
||7.3.1<br>Electric Load Adjustment ............................................................................................... 40||
||7.4 Heating Loads ............................................................................................................................. 41||
||7.5 Cooling Loads ............................................................................................................................. 42||
|**8**|**Resilience Analysis ............................................................................................................................ 42**||
||8.1 Critical Load ................................................................................................................................ 43||
||8.1.1<br>Critical Load Builder ...................................................................................................... 43||
||8.2 Outage Start Time and Duration ................................................................................................. 45||
|**9**|**Renewable Energy and Emissions ................................................................................................... 45**||
||9.1 Renewable Energy Accounting ................................................................................................... 47||
||9.2 Climate and Health Emissions .................................................................................................... 49||
||9.2.1<br>Emissions Accounting Overview ................................................................................... 49||
||9.2.1<br>Electric Grid Emissions Factors ..................................................................................... 50||
||9.2.1.1<br>Climate Emissions Factors for the Contiguous United States ...................................................... 50||
||9.2.1.2<br>Health Emissions Factors for the Contiguous United States ........................................................ 53||
||9.2.1.3<br>Climate and Health Emissions Factors for Alaska and Hawaii ...................................................... 54||
||9.2.1.4<br>Custom User-Provided Climate and Health Emissions Data ........................................................ 55||
||9.2.2<br>Fuels Emissions Factors ................................................................................................. 55||
||9.2.1<br>Emissions Costs ............................................................................................................. 56||
||9.2.1.1<br>Climate Emissions Costs ............................................................................................................... 56||
||9.2.1.2<br>Health Emissions Costs ................................................................................................................. 57||
||9.3 Clean Energy Targets .................................................................................................................. 57||
||9.3.1<br>Renewable Electricity Targets ....................................................................................... 57||
||9.3.2<br>Emissions Reductions Targets ....................................................................................... 58||
||9.3.3<br>Include climate and/or health emissions costs in the objective function ........................ 58||
|**10**|**Photovoltaics ...................................................................................................................................... 59**||
||10.1 PV Costs ...................................................................................................................................... 59||
||10.2 PV System Characteristics .......................................................................................................... 60||
||10.2.1 PV Size ........................................................................................................................... 60||
||10.2.2 Existing PV .................................................................................................................... 61||
||10.2.3 Module Type .................................................................................................................. 61||
||10.2.3.1<br>Array Type .................................................................................................................................... 62||
||10.2.3.2<br>Array Azimuth .............................................................................................................................. 62||
||10.2.3.3<br>Array Tilt ....................................................................................................................................... 63||
||10.2.3.4<br>Direct Current to Alternating Current Size Ratio .......................................................................... 63||
||10.2.3.5<br>System Losses ............................................................................................................................... 64||
||10.2.4 Custom PV Generation Profile ....................................................................................... 64||
||10.2.5 PV Resource Data and Station Search Radius ............................................................... 65||
|**11**|**Battery Storage ................................................................................................................................... 65**||
||11.1 Battery Cost ................................................................................................................................. 65||
||11.1.1 Capital Cost .................................................................................................................... 65||
||11.1.2 Operating|and Maintenance (O&M) Cost ...................................................................... 66|
||11.1.3 Replacement Cost ........................................................................................................... 66||
||11.1.4 Allowing|Grid to Charge Battery ................................................................................... 67|
||11.2 Battery Characteristics ................................................................................................................ 67||
||11.2.1 Battery Size .................................................................................................................... 67||



vii 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

||11.2.2 Battery Efficiency .......................................................................................................... 68|
|---|---|
||11.2.3 Battery State of Charge .................................................................................................. 68|
|**12**|**Wind Turbine ....................................................................................................................................... 68**|
||12.1 Wind Cost .................................................................................................................................... 69|
||12.2 Wind characteristics .................................................................................................................... 69|
||12.2.1 Size Class ....................................................................................................................... 69|
||12.2.2 Wind Size ....................................................................................................................... 70|
|**13**|**Emergency Generator & Offgrid Generator ..................................................................................... 70**|
||13.1 Emergency Generator .................................................................................................................. 71|
||13.2 Off-grid Generator ....................................................................................................................... 71|
||13.3 Generator Costs ........................................................................................................................... 71|
||13.4 Generator Size ............................................................................................................................. 72|
|**14**|**Combined Heat and Power ................................................................................................................ 72**|
||14.1 CHP Prime Mover Overview ...................................................................................................... 73|
||14.2 CHP Fuel Consumption .............................................................................................................. 74|
||14.3 CHP Available Heat Production.................................................................................................. 76|
||14.4 Modeling Multiple Ganged Units ................................................................................................ 79|
||14.5 Combustion Turbine Supplementary Duct Firing ....................................................................... 81|
||14.6 CHP Auxiliary and Parasitic Loads ............................................................................................. 82|
||14.7 CHP Operations Constraints ....................................................................................................... 82|
||14.8 Topping Cycle Default CHP Cost & Performance Parameters by Prime Mover Type & Size|
||Class<br>82|
||14.9 Back-Pressure Steam Turbine CHP ............................................................................................ 88|
||14.10 CHP Scheduled and Unscheduled Maintenance ......................................................................... 92|
|**15**|**Prime Generator.................................................................................................................................. 94**|
|**16**|**Absorption Chilling ............................................................................................................................ 94**|
|**17**|**Thermal Energy Storage .................................................................................................................... 96**|
||17.1 Chilled Water TES ...................................................................................................................... 98|
||17.2 Hot Water TES ............................................................................................................................ 98|
|**18**|**Geothermal Heat Pumps .................................................................................................................... 98**|
||18.1 Overview of the GHP Performance Model ............................................................................... 100|
||18.2 GHP Cost Model ....................................................................................................................... 101|
||18.3 Heat Pump ................................................................................................................................. 102|
||18.3.1 Distributed Heat Pumps in WAHP configuration ........................................................ 102|
||18.3.2 Central Plant Heat Pumps in WWHP configuration .................................................... 103|
||18.4 Geothermal Heat Exchanger ..................................................................................................... 107|
||18.4.1 Inputs to the GHX model ............................................................................................. 108|
||18.5 Hybrid Geothermal Heat Exchange .......................................................................................... 111|
||18.6 Efficiency Gain of Replacing VAV HVAC Equipment with GHP........................................... 116|
|**19**|**Air-Source Heat Pumps ................................................................................................................... 117**|
||19.1 Background to building HVAC systems and scope of ASHP in REopt ................................... 118|
||19.2 ASHP Cost Model ..................................................................................................................... 124|
||19.3 Considerations based on ASHP configuration .......................................................................... 124|
||19.3.1 Hybrid ASHP considerations (configurations 1 and 3) .................................................. 124|
||19.3.2 Full replacement ASHP considerations (configurations 2 and 4) .................................. 125|
||19.4 ASHP Performance Model ........................................................................................................ 125|
||19.4.1 Heat Pump COP and Capacity Dependence on Outdoor Air Temperature .................... 125|
|**20**|**Concentrating Solar Thermal (CST)................................................................................................ 127**|
||20.1 Parabolic Trough Collectors for Industrial Process Heat .......................................................... 127|
||20.2 High Temperature Thermal Energy Storage ............................................................................. 127|
||20.3 Applications for Heating Loads ................................................................................................ 127|
|**21**|**Outputs .............................................................................................................................................. 128**|



viii 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

21.1 Cases 128 21.2 System Size ............................................................................................................................... 129 21.2.1 Energy Production ........................................................................................................ 130 21.3 Dispatch Strategy ...................................................................................................................... 130 21.3.1 Electric Dispatch .......................................................................................................... 130 21.3.2 Heating Thermal Dispatch ........................................................................................... 130 21.3.3 Cooling Thermal Dispatch ........................................................................................... 131 21.4 Economics ................................................................................................................................. 131 21.5 Resilience .................................................................................................................................. 132 21.5.1 Resilience vs. Financial Comparison ........................................................................... 132 21.5.2 Energy Resilience Performance Tool ........................................................................... 132 21.5.3 Modeling Approach in Energy Resilience Performance Tool ..................................... 135 21.6 Renewable Energy Outputs ....................................................................................................... 139 21.7 Climate and Health Emissions Outputs ..................................................................................... 140 21.7.1 Emissions Outputs in Results Comparison Table ........................................................ 140 21.7.2 Renewable Energy & Emissions Metrics Table ........................................................... 140 21.7.3 Interpreting Emissions Results Based on Emissions Type........................................... 141 21.8 Caution Information .................................................................................................................. 142 21.9 Next Steps ................................................................................................................................. 144 **22 Off-grid Microgrids ........................................................................................................................... 144** 22.1 Off-grid inputs ........................................................................................................................... 145 22.2 Off-grid model ........................................................................................................................... 147 22.3 Off-grid outputs ......................................................................................................................... 147 **23 The REopt Web Tool Default Values, Typical Ranges, and Sources .......................................... 148 References ............................................................................................................................................... 181 Appendix A: CHP Cost and Performance Data by Prime Mover Type and Size Class .................... 184 Appendix B: Efficiency Gain Potential of GHP Retrofit in Facilities with Variable-Air-Volume HVAC Equipment ......................................................................................................................................... 187 Appendix C: ASHP Performance Data .................................................................................................. 192 Appendix D: Mathematical Formulation** 

ix 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **List of Figures** 

Figure 1. System diagram for REopt power, heating, and cooling technologies and loads ........................ 18 Figure 2. Cambium’s generation and emission assessment (GEA) regions, 2023 version (Gagnon P. S., 2024). This is the default geographic resolution for the long-run marginal emissions rates used in REopt. ........................................................................................................................ 51 Figure 3. Annual average of the default hourly marginal emissions factors for SO2, NOx, and PM2.5 for grid electricity in each AVERT or eGrid (for HI and AK) subregion used in REopt. ........... 55 Figure 4. Topping cycle CHP diagram to illustrate the energy flows ......................................................... 74 Figure 5. Bottoming cycle CHP: back pressure steam turbine ................................................................... 74 Figure 6. Modeling of CHP fuel burn rate .................................................................................................. 75 Figure 7. Modeling of CHP available useful heat ....................................................................................... 77 Figure 8. Heat recovery configuration for reciprocating engine CHP ........................................................ 78 Figure 9. Heat recovery configuration for microturbine CHP .................................................................... 78 Figure 10. Heat recovery configuration for combustion turbine CHP ........................................................ 79 Figure 11. Fuel consumption and electrical efficiency versus load for one 200-kW microturbine ............ 80 Figure 12. Actual and REopt-modeled fuel and electrical efficiency curves for three 200-kW generators packaged as one unit .............................................................................................................. 80 Figure 13. Back-pressure steam turbine CHP diagram (DOE CHP Fact Sheet) ......................................... 89 Figure 14. Steam turbine performance parameter diagram ......................................................................... 90 Figure 15. Example month for understanding how to build a maintenance period with respect to the year/month calendar ............................................................................................................... 93 Figure 16. TES installed cost estimates from Glazer (2019) and applying a 14°F temperature differential assumption ............................................................................................................................. 97 Figure 17. Default water-sourced heat pump performance map as a function of entering fluid temperature .............................................................................................................................................. 102 Figure 18. Default cooling WWHP performance map as a function of GHX EFT and cooling loop setpoint temperature ............................................................................................................. 105 Figure 19. Default heating WWHP performance map as a function of GHX EFT and heating loop setpoint temperature ........................................................................................................................... 105 Figure 20. GHP concept schematic for distributed water-source heat pumps (WSHP) ............................ 113 Figure 21. Diagram of two example central-plant HVAC systems for heating and cooling; on the left, the heating is provided solely in the terminal VAV boxes, while on the right, there is heating coil in the central AHU. ....................................................................................................... 119 Figure 22. Illustration of roof-top unit HVAC systems, each of which are serving specific zones .......... 119 Figure 23. Example diagram of ASHP water heater, including water storage tanks and piping. ............. 120 Figure 24. Diagram illustrating how ASHP integrates with the existing HVAC system depending on configuration. The orange boxes highlight new ASHP equipment. ..................................... 123 Figure 4. Schematic of a parabolic trough CST with molten salt tank HT-TES system (modified diagram from Alami et al 2023) ......................................................................................................... 128 Figure 25. Relationship and workflow between REopt techno-economic optimization and the Energy Resilience Performance tool accessible on the REopt results web page. ............................. 133 Figure 26. A reliability bathtub model showing a low constant failure rate during the useful life period 139 Figure 27. Obstacles to potential wind energy production ....................................................................... 143 Figure 28. ASHP coefficient of performance (COP) data for heating from which the linear curve fit is used to determine the default performance; this applies to both ASHP for space heating and ASHP Water Heater defaults. .............................................................................................. 192 Figure 29. ASHP capacity factor (CF) data for heating from which the linear curve fit is used to determine the default performance; this applies to both ASHP for space heating and ASHP Water Heater defaults. .................................................................................................................... 193 

x 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

Figure 30. ASHP coefficient of performance (COP) data for cooling from which the linear curve fit is used to determine the default performance; this applies to ASHP for space cooling defaults. .............................................................................................................................................. 193 

Figure 31. ASHP capacity factor (CF) data for cooling from which the linear curve fit is used to determine the default performance; this applies to ASHP for space cooling defaults. ........ 194 

## **List of Tables** 

Table 1. Default COPs for Existing Cooling Plant ..................................................................................... 32 Table 2. DOE Commercial Reference Building Types ............................................................................... 39 Table 3. Climate Zones ............................................................................................................................... 39 Table 4. Summary of key inputs and outputs related to renewable energy and emissions calculations in REopt. All inputs include default values that can be overridden by the user. ........................ 46 Table 5. Renewable energy contributions by technology ........................................................................... 47 Table 6. User-modifiable inputs to generate hourly levelized grid climate emissions factors from NREL’s Cambium data sets, for locations in the contiguous United States. See the Cambium Documentation for more details on each input (Gagnon P. S., 2024). ................................... 51 Table 7. EPA eGRID 2022 emission factors, EFg, for grid electricity in Alaska and Hawaii. CO2e values are used for REopt climate emissions calculations. NOx, PM2.5, and SO2 are used for REopt health emissions calculations. ................................................................................................ 54 Table 8. Default fuel-specific emissions factors used in REopt. ................................................................ 55 Table 9. PV size classes and the capital cost and O&M cost default values for each, based on roofmounted PV systems except for the Utility size class. See below for cost increases for ground-mounted PV for Residential through Large Commercial size classes. ...................... 60 Table 9. Module Types ............................................................................................................................... 61 Table 10. Azimuth Angles for Different Compass Headings ..................................................................... 62 Table 11. PV Array Tilt Angle for Different Roof Pitches ......................................................................... 63 Table 12. Default Values for the System Loss Categories .......................................................................... 64 Table 14. Wind Size Class Representative Sizes ........................................................................................ 69 Table 15. Representative Power Curves ..................................................................................................... 70 Table 16. Supplementary firing input parameters and default values ......................................................... 81 Table 17. Threshold of Average Boiler Fuel Load over which the Default Prime Mover Switches from Reciprocating Engine to Combustion Turbine ....................................................................... 83 Table 18. Reciprocating Engine Cost and Performance Parameters Included in the REopt web tool ........ 85 Table 19. Micro-Turbine Cost and Performance Parameters Included in the REopt web tool ................... 86 Table 20. Combustion Turbine Cost and Performance Parameters Included in the REopt web tool ......... 87 Table 21. Fuel Cell Cost and Performance Parameters Included in the REopt web tool ............................ 88 Table 22. Steam turbine default cost and performance parameters from DOE CHP Fact Sheets .............. 90 Table 23. Default Maintenance Periods and Unavailability Summary Metrics .......................................... 92 Table 24. Custom Uploaded CHP Maintenance Schedule Form Description ............................................ 93 Table 25. Absorption Chiller Installed Cost and O&M Cost ...................................................................... 95 Table 26. Default heat pump performance as a function of entering fluid temperature ........................... 103 Table 27. Default cooling WWHP COP (kW/kWe) as a function of GHX EFT and cooling loop setpoint temperature ........................................................................................................................... 106 Table 28. Default heating WWHP COP (kW/kWe) as a function of GHX EFT and heating loop setpoint temperature ........................................................................................................................... 106 Table 29. Geothermal heat exchanger system characteristics inputs ........................................................ 109 Table 30. Ground properties ..................................................................................................................... 110 Table 31. Default ground thermal conductivity values by climate zone ................................................... 110 Table 32. Application of ground loop temperature limits in non-hybrid and hybrid GHX design ........... 112 

xi 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

Table 33. Default values for auxiliary heat exchange units ...................................................................... 115 Table 34. Default thermal correction factors in percentage (%) by climate zone and building type ........ 117 Table 35. Default coefficient of performance (COP) and capacity factor (CF) dependence on outdoor air temperature (OAT) for heating and cooling. ........................................................................ 126 Table 36. DER modeled in ERP ............................................................................................................... 135 Table 37. Default reliability metrics by DER ........................................................................................... 138 Table 38. Simplified summary of how to interpret emissions results in the Renewable Energy & Emissions Metrics table, given the table column header and use of marginal vs. average grid emissions rates. Check mark indicates metric is appropriate to use and “X” indicates metric is not appropriate to use. ...................................................................................................... 142 Table 39. Site and Utilities Inputs, Default Values, Ranges, and Sources ................................................ 149 Table 40. Load Profile Inputs, Default Values, Ranges, and Sources ...................................................... 149 Table 41. Financial Inputs, Default Values, Ranges, and Sources ........................................................... 151 Table 42. Emissions Inputs, Default Values, Ranges, and Sources .......................................................... 154 Table 43. PV Inputs, Default Values, Ranges, and Sources ..................................................................... 155 Table 44. Battery Storage Inputs, Default Values, Ranges, and Sources ................................................. 162 Table 45. Wind Inputs, Default Values, Ranges, and Sources ................................................................. 168 Table 10. Concentrating solar thermal (CST) Inputs, Default Values, Ranges, and Sources .............. **Error! Bookmark not defined.** Table 11. High Temperature Thermal Storage Inputs, Default Values, Ranges, and Sources ............ **Error! Bookmark not defined.** Table 46. Resilience Evaluations- Load Profile Inputs, Default Values, Ranges, and Sources ................ 172 Table 47. Resilience Evaluations- Emergency and Off-Grid Generator (Diesel) Inputs, Default Values, Ranges, and Sources ............................................................................................................ 172 Table 48. Combined Heat and Power Inputs, Default Values, Ranges, and Sources ............................... 175 Table 49. Hot Water Storage Inputs, Default Values, Ranges, and Sources ............................................ 177 Table 50. Absorption Chiller Inputs, Default Values, Ranges, and Sources ............................................ 178 Table 51. Chilled Water Storage Inputs, Default Values, Ranges, and Sources ....................................... 178 Table 52. Geothermal Heat Pump Inputs, Default Values, Ranges, and Sources ..................................... 179 Table 53. Default thermal correction factors in percentage (%) by climate zone and building type (ASHRAE 90.1 1989) .......................................................................................................... 191 Table 54. Thermal correction factors in percentage (%) by climate zone and building type for ASHRAE 90.1 2007. ............................................................................................................................. 191 

xii 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **1 Introduction** 

The REopt ® web tool evaluates the economic viability of grid-connected solar photovoltaics (PV), wind, combined heat and power (CHP), geothermal heat pumps (GHP), and storage at commercial and small industrial sites. It allows facility owners to identify the system sizes and dispatch strategies that minimize the site’s life cycle cost of energy. The REopt web tool also estimates the amount of time on-site generation and storage can sustain the site's critical load during a grid outage and allows the user the choice of optimizing for energy resilience. The REopt web tool allows users to screen the technical and economic potential of distributed energy technologies on their own or in combination with each other. The user can select default performance parameters or enter user-specified performance parameters that are consistent with the model architecture and assumptions. By default, technology sizes will be determined by the model although the user can instead specify a size to be evaluated within a predetermined range. 

Users are cautioned that although this model provides an estimate of the techno-economic feasibility of PV, wind, CHP, GHP, and storage installations, this is not a design tool. The results are indicative of a potential opportunity; they do not describe a design for procurement. Investment decisions should not be made based on these results alone. 

This report primarily describes access of the REopt web tool through the web-interface, or userinterface, although some specific features only accessible via the application programming interface (API) are occasionally described. Tutorials that guide users through the tool inputs and results are available here: https://reopt.nrel.gov/user-guides.html. 

## **1.1 Applications** 

Although a variety of potential applications are possible, the REopt web tool is primarily designed to address two use cases: 

- **Project development decision support:** The REopt web tool is used to evaluate the technical and economic feasibility of PV, wind, CHP, GHP, and storage projects early in the project development process. In a typical development process, sites are qualified using an iterative analysis approach employing increasing levels of rigor and detail around key input assumptions with each successive iteration. This approach is designed to identify potential fatal flaws as quickly as possible and with a minimum of effort and expense. The REopt web tool can be used for early screenings that rely on minimal site information. The default assumptions for many parameters, such as modeled building loads and industry average cost data, are sufficient for this initial screening. Projects without obvious flaws are reanalyzed using increasing levels of actual site- and technology-specific information. In this case, many of the default assumptions may be overridden with specific values based on more detailed investigation and qualification of the site. 

- **Research-related uses:** The REopt web tool is used to research the general conditions and factors driving project feasibility for market development and policy analysis. For example, the tool can be used to explore combinations of technology cost and incentive support needed for project feasibility on different building types and under different tariff structures. 

13 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## _**1.1.1 What Questions Does The REopt Web Tool Answer?**_ 

The REopt web tool is used to evaluate the economics and resilience benefits of behind-themeter distributed energy resources (DER) at specific sites. The REopt web tool answers questions such as: 

- What type and size of DERs should I install to minimize my cost of energy? 

- How much will it cost to achieve a sustainability goal? 

- What is the most cost-effective way to survive a grid outage spanning one day? Three days? One week? 

- How much would it cost to install a completely off-grid system? 

- Where do market opportunities exist for DERs, now and in the future? 

- How do I optimize system control across multiple value streams to maximize project value? 

_**1.1.2 What Questions Does The REopt Web Tool NOT Answer?**_ The REopt web tool is not used to answer questions about: 

- **Front-of-the-meter or utility projects.** The REopt web tool is designed to model the economics of distributed energy resources (DER) at specific sites, behind the utility meter. It models opportunities to reduce utility bills through demand reduction and energy arbitrage. It does not capture front-of-the-meter value streams like demand response, frequency regulation, or ancillary services. 

- **Regional or national energy adoption.** The REopt web tool is not used to predict adoption of energy technologies across city, regional, or national-scale systems. 

- **Power flow.** The REopt web tool is an energy-balance model. It does not consider power flow characteristics. 

- **Detailed design.** REopt is not a design tool. The results are indicative of a potential opportunity; they do not describe a design for procurement. The model generates the economic outlook for potential distributed energy technologies to identify whether they may be worth further consideration with more detailed assessment and consultation with professional engineers. 

- **Building energy modeling.** Loads to be served by DER are inputs to the REopt web tool; it does not include building energy modeling. 

While the REopt web tool is not designed to answer the questions above, researchers are continually adapting the Application Programming Interface (API) and open source code as well as integrating the REopt web tool with other models to address emerging research questions. 

## _**1.1.3 Who Uses The REopt Web Tool?**_ 

The REopt web tool is accessible to users with a range of skill levels and data. Inputs are configured so that increasingly detailed input options are progressively exposed to users. Basic users, or those with minimal data, will enter minimal site-specific information to run an analysis. Results will provide an initial, high-level assessment of project feasibility at a site. Advanced analyses will use detailed site information (e.g., exact tariffs, actual load profiles, actual site area and roof space available) to produce results with a higher degree of accuracy. 

14 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

The REopt web tool is used by: 

- **Facility owners, energy managers, and energy consultants** to understand the economics and resilience benefits of DER at their site 

- **Developers** to understand the economics of DER across a range of potential sites 

- **Utilities** to understand the economics of DER at their customers’ sites 

- **Industry** to understand optimal control strategies for DER 

- **Researchers** to understand economics and resilience benefits of integrated suites of DER. 

## _**1.1.4 How Does The REopt Web Tool Compare with Other Models?**_ 

Other models that also evaluate the technical and economic viability of distributed energy at the site level include RETScreen, System Advisor Model, HOMER, DER-CAM, EnergyPro, TRNSYS, iHOGA, eSyst and ficus. The unique features of the REopt web tool include: 

- **Optimization:** The REopt web tool optimizes system size and dispatch strategy (the user does not have to enter the size/dispatch) 

- **Integration:** The REopt web tool assesses an integrated suite of electric and thermal technologies (rather than each technology individually) 

- **Accessibility:** The REopt web tool is accessible to novice users with just three required inputs while also offering over 100 optional inputs and an API and open-source code for advanced users 

- **Transparency and Extendibility:** The REopt web tool provides transparency into the model formulation and extendibility of the code through the open-source model. 

## **1.2 Accessing The REopt Web Tool** 

The REopt web tool is available in three formats: 

- Web interface: reopt.nrel.gov/tool. The web interface allows users to easily input data, run analysis, and view results for a single site in a graphical user interface. 

- API: https://developer.nrel.gov/docs/energy-optimization/reopt-v1/. The API allows users and software developers to programmatically interface with the REopt tool. The API can be used to evaluate multiple sites and perform sensitivity analyses in an efficient manner, and to integrate REopt tool capabilities into other tools. The REopt API is available on the NREL developer network. Nonprofit or commercial use of these web services is free, subject to hourly and daily limits on the number of web service requests as described at developer.nrel.gov/docs/rate-limits. 

- Open source: https://github.com/NREL/REopt_API. The open-source code allows software developers to modify the REopt tool code or host it on their own servers. It is licensed under BSD-3, a permissive license that allows for modification and distribution for private and commercial use. 

The REopt web tool is a free, publicly available web version of the more comprehensive REopt model, which is described in Cutler et al. (2017). The full REopt model is not available outside NREL. The full model includes technologies that are not yet available in the REopt web tool such as solar hot water and solar ventilation preheating. NREL is gradually transitioning capabilities from the internal version to the public REopt web tool version as time and funding 

15 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

allow. Early versions of the REopt web tool were called REopt Lite. Those versions contained a smaller subset of the full REopt model’s capabilities. 

## **1.3 Citing The REopt Web Tool** 

To cite REopt web tool analysis results for a specific site, please use: 

NREL. [Year]. “REopt Results from [Site Location], [Technologies] [Financial or Resilience] Evaluation.” REopt Web Tool. Accessed [Month Day, Year]. [URL]. 

For example: 

NREL. 2020. “REopt Results from Palmdale, CA, PV and Battery Storage Financial Evaluation.” REopt Web Tool. Accessed May 4, 2020. https://reopt.nrel.gov/tool/results/d875d523-6969-405b-9258-b428169ca42f. 

To cite the REopt web tool model in general, please use: 

S. Mishra, J. Pohl, N. Laws, D. Cutler, T. Kwasnik, W. Becker, A. Zolan, K. Anderson, D. Olis, E. Elgqvist, Computational framework for behind-the-meter DER techno-economic modeling and optimization—REopt Lite, _Energy Systems_ (2021). 

## **1.4 Feedback** 

Contact NREL at REopt@nrel.gov to offer suggestions or feedback on the REopt web tool or to explore options for more detailed modeling and project development assistance. 

## **2 General Description** 

The REopt web tool is a techno-economic decision support model used to identify potentially cost-effective investment opportunities for buildings, campuses, communities, and microgrids. Formulated as a mixed-integer linear program, the REopt web tool solves a deterministic optimization problem to determine the optimal selection, sizing, and dispatch strategy of technologies chosen from a candidate pool such that loads are met at every time step at the minimum life cycle cost. The candidate pool of technologies typically includes PV, wind power, CHP, GHP, electric and thermal energy storage (TES), absorption chillers, and the existing heating plant, cooling plant, and service connection from the electric utility. 

The REopt web tool identifies technologies and operational strategies of these technologies that might reduce the cost of energy services at a particular site. Energy services include the site’s electricity and thermal energy requirements. These services are conventionally supplied by an electric utility (the grid), a natural gas utility, and off-site fuels transported to the site by pipeline, truck, or rail. 

To identify the least-cost set of resources that can provide a site’s energy services, the model weighs the avoided utility costs (grid-purchased electricity and purchased fuels) against the cost to procure, operate, and maintain additional on-site DER. If the avoided costs are greater than the ownership costs, the system is life cycle cost effective. The REopt web tool identifies which 

16 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

technologies are life cycle cost effective, then sizes each technology[1] and determines their dispatch to maximize their economic value for the set of inputs that describe the case under consideration. 

The loads, utility costs, and renewable resources are modeled for every hour of one year. We assume the modeled year represents a typical year and that the load and resources will not change significantly over the user’s selected analysis period. Scenarios with load growth or declines over many years cannot be modeled. The REopt web tool is a time series model in which energy balances are ensured at each time step and operational constraints are upheld while minimizing the cost of energy services for a given customer. A primary modeling assumption is that decisions made by the model will not impact markets, i.e., the model is always assumed to be a price-taker. This is in contrast to price maker models in which pricing is a decision variable. The REopt web tool also does not model power flow or transient effects. 

The REopt web tool solves a single-year optimization to determine N-year cash flows, assuming constant production and consumption over all N years of the desired analysis period. The REopt web tool assumes perfect prediction of all future events, including weather and load. All costs and benefits are discounted with the user-specified discount rate to present value using standard economic functions. The user can enter constant rates of change for future costs of grid power, fuels, and operations and maintenance (O&M) for inclusion into the discounting factors to account for projected cost escalation (or de-escalation) rates. Incentives and taxes are also included in the life cycle cost analysis if the user chooses to include them. 

Because the objective function is set to minimize life cycle costs of energy services, sometimes the solution includes no new technologies because the net present value (NPV) would otherwise be negative. In this case, the baseline system is the cost-optimal result. By adjusting some inputs, the user can specify a system type and size rather than having the REopt web tool solve for this. In this case, systems are ‘forced’ into the solution whether it is cost effective or not. In some cases, the model may find that even though the addition of the new asset was forced in by the user, the model may not utilize it because the cost of operating the new asset would be greater than avoiding its use. For example, in a scenario where electricity costs are low, a CHP system, even if it had no initial capital costs, could be more costly to operate due to the cost of the fuel and maintenance than it is to purchase grid electricity and continue to provide heat through the existing heating plant. 

## **2.1 Technology Models** 

The REopt web tool models the following technologies: PV, wind power, CHP, prime generators GHP, battery energy storage, TES, absorption chillers, and emergency  diesel generators. Because the model weighs the cost-benefit tradeoff of these technologies, we also include models of the serving electrical utility rate tariff, as well as a facility’s existing heating and cooling systems as required. 

All technologies are dispatched on an hourly basis for a typical, or representative, year. There is an implicit assumption that typical meteorological power production profiles for PV and wind 

> 1 The one exception is that REopt does not size GHP for economic optimization. If selected as a technology, the GHP system is assumed to serve all of the space heating and space cooling. 

17 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

are valid over the analysis period, e.g., long-term climate change projections are not included. Furthermore, the user’s entered representative loads are assumed not to change significantly over the analysis period. 

Figure 1 illustrates an example of the general system configuration of the REopt model, including generation sources, storage devices, and loads. Within the electric load and the heating load, dashed boxes show a subset of those loads that could be dispatched by REopt if certain technologies are selected by the user for consideration. 

The assumed existing infrastructure, namely the electrical grid connection, boiler/heating system, and cooling system are shown in bold. The electrical, heating, and cooling distribution systems are also existing infrastructure that the model does not size or cost. The optional user-selected components that the model can consider for parallel operation with the existing sources are not bolded. 

**==> picture [442 x 353] intentionally omitted <==**

**Figure 1. System diagram for REopt power, heating, and cooling technologies and loads** 

The user can select to screen for all or some subset of the available technologies. If the user does not choose to consider chilled water TES or absorption chiller as an additional potential use of the CHP waste heat or GHP, then the cooling load is not a required input and an electrically 

18 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

driven cooling system is not explicitly modeled. In this case, the cooling load is assumed to be embedded within the total electrical load and is met by serving all the site’s electrical load. 

The REopt web tool automatically queries NREL databases and modeling tools, including the Utility Rate Database to gather utility rate tariffs, and PVWatts®, System Advisor Model, and Wind Toolkit to gather renewable energy resource data. PV and wind generation estimates are location-specific time-series profiles. CHP produces both electric and thermal energy. Part-load electric efficiency and heat recovery performance can be modeled as an option. An absorption chiller that produces chilled water from a supply of hot thermal energy may also be considered in conjunction with CHP. GHP can be modeled as a retrofit to replace existing heating and cooling systems to see the impacts on lifecycle costs and potential interaction with other technologies screened. The backup diesel generator is available as a power source during grid outages. Utility supply is modeled as an infinite source of energy for the site, which can be turned off by the user to explore impact of loss of grid power on DER results and economics. 

The electric load is met by the grid, any electricity-producing DER, or discharge from the battery. The modeled facility’s heating system conventionally serves the heating load, and the electric cooling system conventionally supplies the cooling load. With GHP, these loads are assumed to be met entirely by the GHP system. With CHP, absorption chiller, chilled water TES, and hot water TES, the following flows of energy are also considered: 

- The grid and optional PV, wind power, and CHP can provide electricity to the electric load, and electricity from these resources can be stored in the battery if a battery is included in the solution. 

- The battery, subject to state of charge (SOC), can supply electricity to the electrical load. 

- The boiler and CHP can supply hot thermal energy to the heating load, including an optional absorption chiller, and, for hot water systems, hot water can be stored in the hot water TES if hot water TES is included in the solution. 

- Hot water TES, subject to level of stored energy, can supply hot water to the heating load, including an absorption chiller if it is included in the solution. 

- The electric chiller and the optional absorption chiller can supply chilled water to the cooling load, and chilled water can be stored in the chilled water TES if chilled water TES is included in the solution. 

- The chilled water TES, subject to level of stored energy, can supply chilled water to the cooling load. 

- The backup diesel generator can serve electrical loads in resiliency analyses when the user selects to include grid outages. 

Equipment redundancy requirements and factors of safety are not modeled. 

## **2.2 Formulation** 

The REopt web tool solves a mixed-integer linear program. The objective function minimizes total life cycle cost, which consists of a set of possible revenues and expenses over the analysis period, subject to a variety of integer and non-integer constraints to ensure that thermal and electrical loads are met at every time step by some combination of chosen technologies. 

19 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

The constraints governing how The REopt web tool builds and dispatches technologies fall into the following categories: 

- Load constraints: Loads must be fully met by some combination of renewable and conventional generation during every time step. Typically, hourly or 15-minute time steps are used in the model. 

- Resource constraints: The amount of energy that a technology can produce is limited by the amount of resource available within a region or by the size of fuel storage systems. The energy production of variable technologies is limited by the renewable resource at the location, while the utility grid is assumed to be able to provide unlimited amounts of energy. 

- Operating constraints: Dispatchable technologies may have minimum turndown limits that prevent them from operating at partial loads below a specified level. Other operating constraints may limit the number of times a dispatchable technology can cycle on and off each day or impose minimum or maximum SOC requirements on battery technology. 

- Sizing constraints: Most sites have limited land and roof area available for renewable energy installations, which may restrict the sizes of technologies like PV or wind. The client may also specify acceptable minimum and maximum technology sizes as model inputs. 

- Policy constraints: Utilities often impose limits on the cumulative amount of renewable generation a site can install and still qualify for a net metering agreement. Other policy constraints may restrict the size of a variable technology system in order for it to be eligible for a production incentive. 

- Scenario constraints (optional): Constraints may require a site to achieve some measure of energy resiliency by meeting the critical load for a defined period of time with on-site generation assets. 

For more details including the complete mathematical formulation, refer to Appendix B. 

## **2.3 Temporal Resolution** 

The REopt web tool uses time series integration to combine the energy production from concurrently operating technologies. The optimization model assumes that production and consumption are constant across all years of analysis, and so only considers the energy balance of Year 1. The typical time step is one hour, resulting in 8,760 time steps in a typical N-year analysis. This ensures that seasonal variation in load and resource availability is captured. Time steps can be adjusted in the API; in the web tool, they are set to hourly. 

## **3 Getting Started** 

## **3.1 Logging In** 

Upon accessing the REopt web tool (https://reopt.nrel.gov/tool), the user has the option of creating or logging into an existing user account via the Log in/Register link in the upper right corner. The REopt web tool can be used without registering or logging in to a user account. However, if a user chooses to set up an account and to log in before running evaluations, their evaluations are saved and can be accessed later. 

In order to create a detailed custom electricity rate, build a custom critical load profile, or manage typical and critical load profiles, users must be registered and logged into their account. 

20 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

There are options to create accounts using Google and/or Facebook. Users can create a Google account that is associated with a non-gmail.com address by clicking on “Use my current email address instead,” entering an email address, then following the instructions to verify the ownership of the email address entered. Users signing in with Facebook must be signed into their Facebook account and have platform apps enabled in that account. 

## _**3.1.1 User Dashboard**_ 

Once logged in, the Saved Evaluations button takes the registered user to a dashboard which presents a summary of their stored data from previous evaluations, along with links to view or download the results page of each evaluation in their browser, copy the evaluation as a basis for creating an edited new evaluation, or to delete the saved evaluation. An additional option exists for users who access the REopt tool through the API. A JSON (JavaScript Object Notation) formatted file containing the evaluation inputs can be downloaded to be used with the API. 

## _**3.1.2 Custom Load Profiles**_ 

The Load Profiles button gives the registered user the option of viewing Saved Typical Loads or Saved Critical Loads. The Typical Load Profiles page presents a button to upload a new load profile and a summary of all previously uploaded typical load profiles, along with lists of the evaluations that used each load profile, a graph of the load profile, and the option to download the profile. Typical load profiles can be deleted if they are not associated with any evaluations. The user must first delete all associated evaluations in order to enable deletion of a typical load profile. 

The Critical Load Profiles page presents a button to upload a new critical load profile and another button to build a new critical load profile. The page also provides a summary of all previously uploaded or built custom critical load profiles, along with lists of the evaluations that used each critical load profile, a graph of the load profile, and the option to download the profile. Critical load profiles can be deleted if they are not associated with any evaluations. The user must first delete all associated evaluations in order to enable deletion of a typical load profile. 

## _**3.1.3 Custom Rates**_ 

The Custom Rates button takes a registered user to a list of previously defined custom electricity rates, or allows them to define a new electricity rate. 

## **3.2 New Evaluation** 

## _**3.2.1 Step 0: Gathering Data**_ 

The Step 0 section details the advantages of optional registration and logging in to a private account, including the ability to save evaluations, create custom electricity rates, build custom critical load profiles, and manage saved typical and critical load profiles. It also lists the data that should be gathered for different types of evaluation. A Financial evaluation will require site location, electricity rate, and either a custom load profile or the combination of a building type and an annual energy consumption estimate for that building. A Resilience evaluation will require these data plus data defining a planned or potential electric outage. The extra resilience data includes a way of determining the load that will need to be met in an outage: either a percentage critical load factor, a custom critical load profile, or the critical load components that 

21 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

would be required in an outage that can be used to build a critical load profile. The other key data are the expected or desired outage duration to be survived and a starting date and time for the outage. If a generic potential outage is to be modeled, then a worst-case scenario can be used by selecting the outage start time as the peak time of the critical load profile. 

## _**3.2.2 Step 1: Choose Your Focus**_ 

The first step in creating a new evaluation is selecting the focus of the analysis—whether to optimize for financial savings or energy resilience. The default selection is financial savings. If Financial is selected, then Resilience inputs are hidden. 

Financial mode optimizes system sizes and dispatch strategy to minimize life cycle cost of energy. Resilience mode does the same thing, but with the added constraint that on-site resources must sustain the critical load, without the utility grid, during the designated outage period(s). Due to the explicit modeling of the utility grid within the REopt web tool, the model can be used to simulate grid outages by turning off the grid for certain time steps. The load profile can also be modified during these grid outages to represent a "critical" load (either via a percent scaling factor or by splicing in a critical load). This enables evaluation of all technologies in the model, both during grid-connected mode (vast majority of the year) and during grid outages. This capability is especially important for renewable energy technologies because they are able to generate value during grid-connected mode while also supporting a critical load during a grid outage (whereas emergency generators may only be able to operate during an outage due to air quality permits). 

## _**3.2.3 Step 2: Select Technologies**_ 

The second step is selecting the technologies to be included in the analysis—whether to evaluate PV, wind, battery storage, CHP, prime generators, chilled water storage, or any combination of these technologies. If CHP is selected, you may also select to evaluate hot water storage and/or absorption chiller. If a Resilience evaluation has been chosen, a diesel emergency generator evaluation is also given as an option. Only the inputs for a selected technology are visible. Inputs for any technology that is not selected are hidden. 

## _**3.2.4 Step 3: Enter Data**_ 

The third step is entering site-specific data for the scenario that the user wishes to evaluate. This data includes the location, electricity rate, and consumption details, as well as financial constraints. A variety of inputs are necessary for a REopt web tool analysis, but the tool provides editable default values for most of these parameters. Note that there is an option in the right margin of each section to “Reset to default values.” See Section 21 for information on default values. 

For a Financial evaluation, there are three or four required inputs that the user must enter. Two of these entry fields are displayed in the Site and Utility Inputs section when the tool is first opened. These two inputs are site location and the applicable electricity rate for that site location. If CHP technology is selected, fuel cost is also required in this section. The final required input is the typical load—entered either as a simulated building type plus an annual energy consumption or as a custom load profile data file upload—entered in the Load Profile section. If CHP technology is selected, a thermal load profile, or profiles, are also required in this section. 

22 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

For a Resilience evaluation, there are four additional required inputs. The first is the critical energy load profile—entered either as a critical load factor percentage, as a custom critical load profile data file upload, or as a custom-built critical load—in the Load Profile section. The final three required inputs are the outage duration, outage start date(s) and outage start time(s) for the grid outage that the resilience evaluation will model. 

There is a total of twelve possible data input sections: Site and Utility, Load Profile, Resilience (visible only when the resilience evaluation is chosen), Financial, Renewable Energy and Emissions, PV, Battery, Wind, Generator (also visible only when the resilience optimization is chosen), Combined Heat & Power, Geothermal Heat Pumps, and Chilled Water Storage. Inputs for Hot Water Storage and Absorption Chilling are found under Combined Heat & Power. As each section is expanded, the key driver input parameters for that Data Input section are displayed. In most cases these top inputs in each section will have the greatest impact on the results of the evaluation. Additional parameters in each section can be displayed by selecting the “Advanced Inputs” option. 

Parameters with default values have these prepopulated values displayed in light gray text in the data entry boxes. All these values can be overridden, and those that have been altered by the user will display in a darker text and the default will be displayed in the right margin next to the input box. Each separate section, as well as the entire form, has an option to reset the parameters to default values. See Section 21 for details and explanations of these values. 

When all desired inputs have been entered and/or edited, the final step is to select the Get Results button. A new page will display while the tool is optimizing the results. This may take up to several minutes to complete, depending on the complexity of the analysis. The Results page displays recommended system sizes, potential savings, the system dispatch strategy returned from the API, and, if requested, analysis of resilience system economics. The user will have the option of downloading a dispatch spreadsheet, a pro forma spreadsheet, and running an outage simulation. The user can also return to the input page to edit the inputs and alter the scenario for a new evaluation. 

Users are cautioned that, although this model provides an estimate of the techno-economic feasibility of solar, wind, CHP, prime generators, GHP, and storage installations, this is not a design tool. The results are indicative of a potential opportunity; they do not describe a design for procurement. Investment decisions should not be made based on these results alone. Before moving ahead with project development, verify the accuracy of important inputs and consider additional factors that are not captured in this model. 

## **3.3 International Use** 

Although the REopt web tool is designed for use with locations within the United States, this section provides suggestions for adjustments that can allow the use of most of the tool’s features for international locations. 

## _**3.3.1 Site Location & Utility Rate**_ 

Selecting a site location outside the United States will prompt a message that no electricity rates can be found for the location. This is because the utility rate database used by the REopt web 

23 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

tool does not include international locations. However, custom utility rates can be entered as simple annual or monthly rates. Detailed rates, with variable prices dependent on times and months, can also be entered if the user is registered and logged in to a user account. Details of rate structures for some international locations can be found at the International Utility Rate Database. 

## _**3.3.2 Currency**_ 

Currency values are all in U.S. dollars. Conversions from the local currency to U.S. dollars can be made for inputs of utility rates, system costs, and incentive values. If converting to a different currency, be sure to convert _all_ monetary inputs (otherwise, REopt will draw from a comination of U.S. and non-U.S. currencies. Conversion of the final results of the evaluation will then be necessary, from U.S. dollars back to the local currency. One popular tool for currency conversion approximation is the Currency.Wiki. 

## _**3.3.3 Load Profile**_ 

The Load Profile option for simulated load data is based on U.S. building and climate area data. If this simulated load option is used, the simulated load profile should be checked for reasonableness for the climate of the selected location. 

## _**3.3.4 Financial Information**_ 

Financial, tax and incentive input defaults in all sections need to be carefully considered and altered to match local tax and interest rates and available financial incentives. Default costs for technology systems are also based on typical costs in the United States. Resources for researching international renewable energy costs can be found at the International Renewable Energy Agency. 

## _**3.3.5 Solar Production Data**_ 

Solar production data is taken from the PVWatts dataset, which includes many international locations. The REopt web tool will use the closest available location that is found to have resource data, so the user should independently confirm that PVWatts includes data for a location that is acceptably close to their site location. The available resource data locations can be found using NREL's PV Watts. Users who have access to hourly custom solar production data for their site can upload it in the Advanced Inputs section, and it will be used instead of PVWatts data. 

## _**3.3.6 Wind Resource Data**_ 

Wind systems cannot currently be modeled from the web tool user interface for international locations due to lack of international wind resource data. However, if the user has hourly wind resource data for their site, they can use this data in the API, instead of the web tool interface, to complete an optimization. 

## _**3.3.7 Ground Thermal Conductivity Data for GHP**_ 

For GHP, a number of ground properties are assumed and these assumptions are dependent on location in the United States based on climate zone. For international sites, the default ground thermal conductivity is based on the same data set. A geometric calculation to find the nearest 

24 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

US city that represents ground thermal conductivity associated with the climate zone will be done. 

Note: Ground thermal conductivity is a key parameter that drives the size of the ground heat exchanger, and therefore the total cost of GHP. Users are advised to do research on this parameter and run appropriate sensitivities during the screening phase and to do ground properties tests before investing in GHP. 

## _**3.3.8 Ambient Temperature**_ 

For GHP, the geothermal heat exchanger model requires typical hourly ambient temperature data. This temperature data is pulled in from the PVWatts API. The PVWatts API is described in Section 10 Photovoltaics. 

## _**3.3.9 Grid Emissions**_ 

Default grid emissions data are not available for sites outside of the U.S. For international evaluations, users can enter hourly or annual custom climate and health emissions rates for the given location. If custom values are not entered, grid emissions will not be calculated (and will show as zero). 

## **3.4 Solver Settings** 

The solver optimality tolerance is an input that can be adjusted for evaluations that result in a timeout error message because they are not reaching a solution within the time allowed. It is the threshold for the difference between the solution’s objective value (life cycle cost) and the best possible value (lower bound of the objective function as determined by the optimization model) at which the solver terminates. Note, there is no guarantee that the best possible value would be achieved if the model ran longer. It’s possible that the solution achieved within the optimality tolerance is the same solution that would be found if the model ran indefinitely. 

It is suggested to increase this value to 2-3% if no solution is found within the model’s timeout limit. Increase the value further if the model still times out. The maximum allowed tolerance value is 5%. Once a solution is found with the higher tolerance, the user could choose to bound the technology sizes using the minimum and maximum size inputs and run the model with a lower tolerance. 

## **4 Economic Model** 

As previously mentioned, the objective of the optimization is to minimize life cycle costs, i.e., to maximize NPV. Other financial metrics like internal rate of return (IRR) and payback are reported but cannot be selected as the driving objective. It is not unusual to get a ‘null’ solution, where no technologies are recommended, if DERs are not found to be cost-effective. The user can select from two financial models: self-financed owner-operator and third-party financed. 

The approach and terminology are based on the _Manual for the Economic Evaluation of Energy E_ ffi _ciency and Renewable Energy Technologies_ (Short, Packey, and Holt 1995) and abides by 

25 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

the life cycle cost methods and criteria for federal energy projects as described in the Federal Code of Regulations 10 CFR Part 436 - Subpart A, and which are detailed in National Institute of Standards and Technology (NIST) Handbook 135, Life-Cycle Costing Manual for the Federal Energy Management Program (Fuller and Petersen 1995). 

## **4.1 Definitions, Inputs, and Assumptions** 

The primary economic calculations considered are the NPV of the alternative energy project and the total LCC. LCC[2] is the present value of all costs, after taxes and incentives, associated with each project option. NPV[3] is the present value of the savings (or costs if negative) realized by the project. The general equation for NPV is given below: 

_NPV of alternative = LCC of Business-as-Usual Case - LCC of Investment Case_ Equation 1 

Here, Business-as-Usual Case refers to the total cost of energy services over the analysis period if the site continues to purchase energy services solely from its existing suppliers. These are typically the site’s existing serving utility, but if on-site energy systems exist, those are also included in the Business-as-Usual Case. For example, PV systems or CHP plants already in service at the site are modeled to ensure the Base Case scenario properly represents the site’s current utility demand, supply sources, and costs. Life cycle utility costs include annual cost escalation rate projections specific to and specified by the client. 

The Investment Case is the project scenario with additional alternatives to continuing the business-as-usual operation. The Investment Case considers: 

- Capital Expenditure (CAPEX[4] ) of the alternative project 

- O&M costs of the alternative project 

- The cost of fuels 

- All applicable incentives made available by utilities, states or the federal government (e.g., Investment Tax Credit (ITC), Production Tax Credit, and accelerated depreciation) 

- Balance of remaining utility costs if the alternative project considered does not supply all of the site’s energy loads. 

Costs that occur in years beyond the base year (Year 0) are discounted to present value. An endof-year discounting convention is applied. The discounting function properly discounts for: 

1. One-time future costs (e.g., a PV system’s inverter replacement in Year 15 if it is included in the O&M forecast) 

2. Annual recurring costs (e.g., regular annual maintenance for a wind turbine in a real economic analysis) 

> 2 LCC or total life-cycle cost has the meaning as described in (Short, Packey, & Holt, 1995), where it is abbreviated as TLCC 

> 3 NPV as described here has the same meaning as Net Savings (NS) as described in (Fuller & Petersen, 1995) 4 Note that the term CAPEX and capital costs are both used interchangeably in this document and have the same meaning. 

26 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

3. Annual recurring costs that are escalating at a fixed rate each year (e.g., an annual utility cost escalation rate is applied to the base year utility costs to account for projected utility rate increases). 

With these considerations in mind, the primary economic inputs into the REopt web tool are as follows: 

- Discount rate: The rate at which the future value of all future costs and savings is discounted—an after-tax value if the owner is a taxable entity 

- Current utility costs and assumed utility cost escalation rates: The expected annual escalation rate for the price of electricity or fuel 

- Length of the analysis period: The financial life of the project 

- Income tax rate: The percent of income that goes to tax. The tax value default is currently 26%—the sum of a 21% federal rate plus a 5% average state rate 

- O&M cost escalation rate: The expected annual escalation rate for O&M costs over the financial life of the system 

- Tax and non-tax-based incentives depending on the client’s tax disposition. 

To calculate the economic outputs, the REopt web tool makes the following assumptions: 

- CAPEX are considered overnight costs (i.e., all projects are completed at the end of Year 0 and produce energy starting in Year 1) and assumed to be the same in both ownership models (see Section 4.2). Construction periods and construction loans are not modeled. 

- A site’s annual electric and thermal load demand profiles remain constant from year to year for the duration of the analysis period. 

- One-year discounting periods are used (i.e., no mid-year discounting subperiods). 

- All cash flows occur at end of year. 

- available tax incentives in their entirety. 

- O&M costs escalate at the O&M cost escalation rate. 

- Sales tax, insurance costs, and property taxes are not considered. 

- Debt service coverage and reserve requirements are not considered. 

Although the input fields in the user interface are labelled as nominal values, a real or nominal analysis can be performed as long as discount rates, O&M cost escalation rate (general inflation), and utility cost escalation rates are consistently represented in real or nominal terms. The REopt web tool assumes all technologies except battery storage have a useful life equal to the analysis period; any residual value at the end of the analysis period is not captured. For battery storage, one replacement can be modelled during the analysis period. 

## **4.2 Ownership Models** 

Many economic or pro forma financial analyses consider project options only from the perspective of the project owner, assuming that the party that consumes the energy from an energy-producing technology also purchases, owns, and operates the system. However, on-site renewable energy and nonrenewable energy systems are often financed and owned by an unrelated party that does not consume the energy output but instead sells these energy services to 

27 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

the owner of the building or site. In this type of business arrangement, the site acts as the "host" (or off-taker) of the energy project while the third party both finances and owns the project. 

A facility owner may consider a project of this type if they do not have or do not want to use their own funds to build energy systems, or if they do not want to take on ownership overhead. In this case, facility owners want to know if a project is economically feasible if a third party builds and operates the system at the facility and sells the energy services to the facility owner. Business arrangements of this type are sometimes referred to as alternative financed projects and include power purchase agreements (PPAs), energy savings performance contracts (ESPCs) or utility energy service contracts (UESCs). 

The REopt web tool is formulated to allow techno-economic screenings of projects for facilities under the following general ownership models: 

1. Single Party Economic Model: The facility is interested in projects that the facility owner will purchase, own, operate, and consume energy from. This is the conventional ownership model described in the references. The economic screening here answers the question: Should the facility owner consider buying additional energy systems to displace energy purchases from their existing utility and/or other existing assets? 

2. Third-Party Economic Model: The facility owner is interested in procuring energy services from a third party that owns and operates the system(s) on or adjacent to the facility owner’s property, and sells the energy produced to the facility owner. Here, there are two parties, the Third-Party Owner and the Host, each with potentially different discount rates and income tax rates. The facility owner is the system Host, or consumer of the energy from the project. The Third-Party Owner builds and operates the systems and sells energy services to the Host. The Third-Party Owner is an unrelated party who invests in the project as a business venture. The economic screening here answers the question: Should the facility owner consider engaging an energy services provider to procure electricity, heat, or other energy services to reduce total costs of energy paid to their conventional utility providers or to consume electricity or heat provided by other existing assets? 

The Third-Party model of ownership uses the same general economic principles as the Single Party model, but considers two sets of discount rates and tax rates: (1) the Third-Party Owner’s discount rate and tax rate for evaluating ownership costs and revenues necessary for the project to be a sound investment for the Third-Party Owner, and (2) the Host’s discount rate and tax rate to determine the economic merits of procuring energy services from the Third-Party Owner instead of the serving utility. Alternative financing projects are complex and ultimately need to be evaluated using complex proformas that depend on the financing approach taken. The ThirdParty Model in the REopt web tool is a simplified screening-level analysis to identify potential opportunities for facilities considering alternative financing. 

The Third-Party Model screens projects that the facility would engage in under an alternative financing plan (e.g., through a PPA or an ESPC). The model considers the perspective of both the Third-Party Owner and the Host. The general approach is as follows: 

28 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

1. Find the total Net Present Cost of the project using the Third-Party Owner’s discount rate, tax rate and all incentives available to the project owner. This discount rate is the same as the Third-Party Owner’s IRR. As applied in the REopt web tool, the Third-Party Owner’s discount rate is Third-Party Owner’s IRR after taxes. 

2. Determine the annual payment (annuity) for energy services required by the Third-Party Owner over the analysis period to cover all ownership costs at the Third-Party Owner’s discount rate (after tax IRR). In the user interface, this is both the Third-Party Owner’s ‘Annual Payment from Host’ and the Host’s ‘Annual Payment to Third Party Owner’. 

3. Determine the LCC of energy for the Host using the Host’s discount rate, considering: 

   - Purchasing energy from the serving utilities and fuel suppliers 

   - Energy services payments the Host will make to the Third-Party Owner for procuring energy from the project. 

4. Calculate the NPV for the Host, considering payments to conventional utilities in the Business-as-Usual Case and the sum of conventional utility costs and energy services payments in the Alternative Energy Case. If the NPV is greater than zero, the project is considered economically viable for the Host and the Third-Party Owner is able to meet their profit requirements. 

## **4.3 Economic Incentives** 

The REopt web tool models three types of incentives for applicable technologies: capital costbased incentives, production-based incentives, and tax depreciation. 

## _**4.3.1 Capital Cost Based Incentives**_ 

Capital cost-based incentives, or CBI, are structured either as a fraction of the total installed cost or as a rebate amount per DER unit capacity. The user can enter programmatic maximum rebate limits to CBI incentives. The value defaults to 'Unlimited.' Federal and state tax credits are entered as CBI in the REopt web tool. The federal percentage-based incentive is treated as a taxbased incentive to model the federal investment tax credit. All other incentives are not tax-based. 

Incentives are considered in the following order: utility, state, then federal. For example, if there is a 20% utility incentive and a 30% state incentive, the 20% utility incentive would be applied first, then the 30% state incentive would be applied to the reduced cost. The incentives are not additive; that is, the site would not get a 20% + 30% = 50% discount. 

## _**4.3.2 Production Based Incentives**_ 

Production-based incentives, or PBI, are entered as a dollar value of the incentive per kWh produced. The number of years the PBI is available and the maximum incentive amount are available fields. Additionally, the user can enter a maximum available generator size for incentive programs that include a system capacity limit. If there is more than one productionbased incentive offered (for example, a federal and a utility incentive), the combined value can be entered and should be discounted back to year one if the incentive duration differs. 

29 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **4.4 Tax Policies** 

The Modified Accelerated Cost Recovery System (MACRS) is the current tax depreciation system in the United States. Under this system, the capitalized cost (basis) of tangible property is recovered over a specified life by annual deductions for depreciation. If available, the user may specify the duration over which accelerated depreciation will occur (five or seven years). When claiming the ITC, the MACRS depreciation basis is reduced by half of the value of the ITC. 

## **5 Existing Facility Infrastructure** 

This section provides a detailed description and assumptions used for the performance models of the assumed existing facility infrastructure in the REopt web tool. This infrastructure includes electric utility service, space and domestic hot water heating systems, and a space cooling system. The REopt web tool does not size and cost this assumed existing infrastructure. 

## **5.1 Utility Services** 

The site is assumed to be served by an electric utility and, if natural gas is selected by the user, a natural gas utility. In addition, if other fuel types are selected for the heating system or to be considered for use by the potential CHP system, we assume those fuel storage and delivery components are in place, i.e., they are not included in the REopt web tool cost models. The costs for fuels and power via the utility services are user inputs. 

## **5.2 Heating System** 

If the user screens for systems to replace or augment facility heating, the model construct assumes the facility has an existing heating system. For CHP screening, the heating systems are assumed to be centrally located and that they could accommodate the integration of supplementary waste heat from a CHP unit. For GHP screening, the heating system can be either centralized or decentralized. The heating systems are modeled as a lumped heat generator; individual boilers in a multiple boiler facility or distributed heating systems are not individually modeled. Additionally, when screening for CHP, the user selects whether the heating system is hot water or steam in the user interface using the ‘Existing boiler type’ dropdown menu. A configuration with both steam and hot water cannot be modeled. 

The model does not include heating system turn-down limits (minimum unloading ratio constraint) or minimum runtime constraints, e.g., the model allows the heating system to be off in one hour, run one hour, and then be off the following hour. 

Natural gas is the default fuel for the heating system. Additional fuel options include propane, diesel, and biogas. For natural gas and biogas, the user enters costs in units of $/MMBtu while the costs for diesel and propane are entered in units of $/gallon. For the analysis, entered unit costs are converted from $/gallon to $/MMBtu using the following higher heating values (HHV)[5] : 

- Diesel, 138,490 Btu/gallon (HHV) 

- Propane, 91,420 Btu/gallon (HHV). 

> 5 https://afdc.energy.gov/fuels/fuel_comparison_chart.pdf 

30 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

The user-selected fuel type impacts carbon dioxide (CO2) emissions accounting. See Section 9, Renewable Energy and Emissions. 

Heating system efficiency is modeled as constant throughout the year, i.e., there are no efficiency adjustments for heating system loading. When screening for CHP, the default plant efficiency is dependent on whether the user selects hot water or steam for the process heat loop. Efficiency is based on the HHV of the fuel. The default heating plant efficiencies (HHV-basis) are 0.80 for a hot water plant and 0.75 for a steam plant. For GHP screenings, the heating system efficiency default is 0.80. 

For hot water systems, the assumed loop temperatures are: 

- Hot water supply temperature of 180°F 

- Hot water return temperature of 160°F. 

In a future release, the user will be able to adjust loop temperatures to inform adjustments to the CHP thermal efficiency (higher thermal efficiency if the required supply water temperature is lower, and vice versa). 

For steam systems, the assumed loop pressure is 150 psig with return to the boiler at a temperature of 180°F. In a future release, the user will be able to adjust the steam pressure. Fraction of condensate returned is not a required input as described in Section 7.4, Heating Loads. If hot water TES is considered for hot water systems, the distribution loop temperature differential is used to estimate the tank’s thermal storage capacity. 

It is assumed that the existing heating system is sized to serve the maximum demand in the facility heating load with an additional 25% excess capacity. This value is a default assumption that can be changed by the user. This assumption imposes a maximum charging rate of hot water into hot water TES. See Section 17.2, Hot Water Thermal Energy Storage for details. 

## **5.3 Cooling System** 

If the user chooses to consider chilled water TES or an absorption chiller, the facility cooling load is assumed to be served by a centralized cooling plant comprised of electrically driven chiller(s). It is also assumed that the cooling plant could accommodate the integration of chilled water TES or a supplemental absorption chiller. 

For GHP screening, the facility baseline cooling system can either be central plant or cooling units distributed throughout the facility. 

The efficiency of the facility’s existing cooling systems needs to be entered by the user or the user can use the default value. In addition, the capacity of the cooling system is assumed to be fixed to put an upper constraint on the maximum charging capacity of chilled water TES. The default assumption is that the chiller plant cooling capacity is 125% of the peak cooling load. This is a value that the user can adjust. 

Cooling system unit power requirements are not adjusted based on cooling loading or outside air conditions. The user’s entered coefficient of performance (COP) value is assumed to represent 

31 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

the average system performance throughout the year. The COP includes the power requirements for the compressors/chiller(s) and heat rejection. 

The user can use the default COP value if their annual average COP is unknown. The default value depends on the assumed capacity of the cooling system. These are determined by the cooling loads entered by the user and the following assumptions: 

- Chillers are water cooled. 

- By default, the cooling system’s capacity is assumed to be 1.25 times the peak cooling load in the interval data. This value can be modified by the user. 

- For peak cooling loads less than or equal to 300 tons, the cooling plant is assumed to have one chiller. For peak cooling loads greater than 300 tons, we assume there are two or more chillers of approximately equal capacity, with no chiller capacity exceeding 800 tons (Pacific Northwest National Laboratory 2016). 

The default COP in the bottom row of Table 1 are used as provided (Sweetser 2020). 

**Table 1. Default COPs for Existing Cooling Plant** 

||**Chiller capacity<= 100 tons**|**Chiller capacity> 100 tons**|
|---|---|---|
|Chiller power (kW/ton)|0.60|0.55|
|Condenser heat rejection<br>(kW/ton)|0.20|0.20|
|Chiller plant total power<br>(kW/ton)|0.80|0.75|
|**Default chiller plant COP**<br>**(kW thermal/kW electric)**|**4.40**|**4.69**|



In any hour, the cooling load must be met by some combination of the existing cooling system and the following REopt retrofit technologies:  absorption chiller, chilled water TES, and GHP if they are included. Note, GHP is sized and dispatched to serve the total cooling load in every timestep, so if GHP is chosen by the REopt optimization model then there will be no remaining cooling load to serve and therefore will preclude any economic benefit from absorption chiller and chilled water TES. 

The model does not include turn-down limits (minimum unloading ratio constraint) on the cooling system. 

If chilled water TES is considered, the distribution loop temperature differential is used to estimate the tank’s thermal storage capacity. See Section 17.1, Chilled Water Thermal Energy Storage for details. 

For centralized chilled water systems, the assumed chilled water loop temperatures are (Pacific Northwest National Laboratory 2016): 

- Supply temperature: 44°F 

- Return temperature: 56°F. 

In a future release, the user will be able to adjust chilled loop temperatures which will only impact the thermal storage capacity of chilled water TES per unit gallon of storage. 

32 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **5.4 Land and Roof Area Available** 

Users can specify the amount of land and/or roof area available for DER. Land area available is used to limit the amount of PV or wind recommended at the site; roof area available is used to limit the amount of PV recommended. These inputs do not limit the size of any other technology. 

PV size is constrained by land area available, assuming a power density of six acres per MW, and by roof area available, assuming a power density of 10 DC-Watts/ft[2] . Wind size is constrained by land area available, assuming a power density of 30 acres per MW for turbine sizes above 1.5 MW. If the turbine size recommended is smaller than 1.5 MW, the input for land available will not constrain the system size. If the turbine size recommended is greater than 1.5 MW, but the land available input is less than 30 acres per MW, then the system size will be capped at 1.5 MW, no matter how small the land available input. It may be wise to run the evaluation with unconstrained land as a check that density constraints are limiting results in the manner expected. The default value is unlimited, meaning PV or wind size is not limited by land or roof area available. Note that both land and roof availability limits should be entered to limit PV size. 

Currently, there is no user input field for the space available for a GHP geothermal heat exchanger. The user is advised to review the size of the geothermal heat exchanger in the solution when considering where and how a system could be installed at their facility. 

## **6 Electricity and Fuel Tariffs** 

This section describes the utility rate tariff inputs to the REopt web tool. 

## **6.1 Electric Rate Tariff** 

For all evaluations, details of the site’s electrical rate tariff must be specified. The electricity rate can either be selected from a dropdown list of options (for locations within the U.S.) or modeled as a custom electricity rate. 

The default option is to select an electricity rate from a list of rates available within 25 miles of the user-entered location. The rates are downloaded from the Utility Rate Database (URDB).[6] If available, the most common rates are listed at the top of the list. Utility rates that are not in URDB can be modeled as custom rates. 

A custom electricity rate can be modeled as an annual, monthly, hourly, detailed rate, or URDB label. If the electricity rate will stay constant through the year, select the “Annual” option and enter the $/kWh Energy cost and, if relevant, the $/kW/month Demand cost. If an “annual” demand charge is specified, it will still be applied on a monthly basis. If the electricity rate varies by month during the year, select the “Monthly” option and enter the $/kWh Energy cost and, if relevant, the $/kW Demand cost that applies in each month of the year. 

If you want to use a URDB rate that isn’t available in the dropdown list for your selected location, you can enter a URDB label that corresponds to an unlisted rate. This label can be found in the URL for the URDB rate on the Open EI website. For example, the label for the rate 

> 6 https://openei.org/wiki/Utility_Rate_Database 

33 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

found at the URL https://openei.org/apps/IURDB/rate/view/5e6134175457a3cf56019407 would be entered as just the label **5e6134175457a3cf56019407** . 

If the electricity rate varies during a single month, such as a rate with weekday/weekend or timeof-use rate differences, or has tiered or lookback charges, select the Detailed option. You must be registered and logged in to a user account to access this feature. The Custom Electricity Rate Builder will open and allow you to enter different rates for different time periods, along with time and month schedules for applying these period rates. Once you have named, created, and saved detailed custom rates, they will show up in the “Select Custom Rate” dropdown menu on the main input page and they can be selected to be applied to a current optimization. To build a custom rate tariff: 

- Start by entering a name for the custom rate. Once you have named, created, and saved detailed custom rates, these names will show up in the "Select Custom Rate" dropdown menu on the main input page and can be selected to be applied to an optimization. An optional description can also be entered in order to assist in identifying a custom rate. 

- Enter each separate rate into the Rate Periods tables for both Energy Charges and Demand Charges. If the rate for a time period includes usage tiers, add tier(s) to that period and enter the total energy purchases allowed in the tier(s). The final tier will have unlimited maximum usage. 

For example, if you enter the following for Period 1: 

||**Max. Energy Purchases**|**Energy Charge**||
|---|---|---|---|
|**Tier**||||
||<br>**(kWh/month)**|<br>**($/kWh)**||
|||||
|1|100|$0.01||
|2|200|$0.10||
|3|900|$0.50||
|||||



For a month in which Period 1 applies, if the site uses 1,000 kWh, the site will be charged the following: 

   - Tier 1: $0.01*100 kWh 

   - Tier 2: $0.1*200 kWh (this tier applies to consumption between 100 kWh to 300 kWh) 

   - Tier 3: $0.5*700 kWh (this tier applies to consumption between 300 kWh – 1200 kWh) 

- After you have defined the Rate Periods, use the Weekday and Weekend Schedule Tables to select the months/times when each period applies. When you have selected a block of time cells, a popover will appear with a dropdown menu so that you can select the relevant period for those cells. 

- Periods do not have to be sequential; however, tiers within a given period must be sequential. 

- An optional fixed monthly charge, in $/day, can be entered in the top section. 

- An additional option exists for users who access the REopt tool through the API. A detailed rate can be created then downloaded as a JSON to be used with the API. JSONs can be 

34 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

downloaded from the Custom Electricity Rate Manager. A previously created JSON can also be uploaded for editing and then saving as a new rate. 

- An option can be selected to populate the tool’s rates and schedules with an existing URDB rate, which can then be edited and saved as a new rate. The rate location chosen does not need to be the same location as the evaluation’s site location. 

- An optional simple Facility Demand Charge can be selected. This monthly/noncoincident/facility demand charge is one value per month, that is charged based on the highest demand of the month, regardless of time of day. This charge is in addition to the TOU demand charge. Also available in this section is a simple lookback percent, or ratchet charge, which considers both the current month and previous months’ peaks in the calculation of demand charges. 

The Custom Electricity Rate Builder allows for modeling utility rates that do not appear in the URDB. Currently, this option can only be chosen as a substitute for the URDB rates and not as an additional add-on charge to a URDB rate. 

The Custom Electricity Rate Manager allows you to view, edit, and copy the detailed custom electricity rates that you have created, or download a JSON version of the rate. _NOTE: Once a custom rate has been used in an optimization, that particular rate can no longer be edited or deleted. However, the rate can be copied to create a new or corrected rate_ . The table lists your custom rates in chronological order based on when they were created. The name and description you assigned are listed in the table along with the maximum and minimum charges. If you wish to look at the details of the rates by time period, click on View Charge Periods. 

## _**6.1.1 CHP Standby Charge**_ 

Standby tariffs for on-site generation are sometimes imposed to cover the utility’s cost to provide backup power to the customer for periods of time when the customer’s generator might be unavailable due to planned or unplanned maintenance activities. Standby tariffs are not unusual for CHP systems. Sometimes described as ‘partial requirements’ tariffs, they can take the form of a relatively simple additional charge added to a customer’s existing tariff, sometimes described as a ‘full requirements’ tariff, or can involve switching to an entirely different tariff if CHP is installed. Tariff switching, i.e., modeling both the existing tariff and alternative tariffs that may be activated if the consumer were to install certain types of DG, cannot be modeled in the REopt web tool.[7] However, the user can include potential standby charges that might be imposed if CHP is installed that are added to the existing electricity tariff by using the ‘CHP standby charge based on CHP size ($/kW/month)’ field in the rate tariff section of the user interface. This option is only available and visible to the user when CHP technology is included. 

This optional additional standby charge for CHP includes monthly charges based on the installed power capacity of CHP ($/kW/month of CHP rated capacity). This is a fixed monthly charge 

> 7 If the standby ‘supplemental’ tariff cannot be modeled as the standard ‘full requirements’ tariff plus some combination of the charges described above, the user will have to model the standby tariff in the tariff template instead of the full requirements tariff. The user will have to keep in mind that the financial results are only relevant if CHP is included in the investment scenario returned and that the business-as-usual costs in that solution are not accurate because they are calculated for the standby tariff rather than the non-standby tariff. Further, if the investment scenario also includes PV, wind power, and/or battery, the user should confirm with the serving utility whether the modeled standby tariff applies to the hybrid CHP system. 

35 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

dependent on the CHP rated power output. Standby demand charges are entered as a single value and applied monthly ($/kW-month). The default value is $0. 

## _**6.1.2 Compensation for Exported Electricity**_ 

REopt web tool users can select between four categories of compensation for exported electricity: 

- **No compensation for exports -** This is the default option and indicates that the DER system(s) will not receive any compensation for electricity exported to the grid (e.g., the system cannot participate in net metering nor net billing). Without any compensation for exports, any excess DER electricity production will be modeled as curtailed in REopt, rather than exported. 

- **Net metering (full retail rate) -** Choose this option if the DER system(s) will be compensated for grid exports at the site’s full retail cost of electricity during the time of export. This is often referred to as “true net metering” or “1-to-1 compensation.” When net metering is selected, you must enter a net metering system size limit (kW), which is the combined system capacity that can net meter under a net metering agreement with the utility. Projects sized up to the net metering limit will receive credit for any exported energy at the electric retail rate at the time of export. Information on state net metering limits is available at www.dsireusa.org. If the cost-optimal system is sized above the net metering limit, the system will not receive any compensation for grid exports. When net metering is applied, only annual grid exports less than or equal to annual grid purchases will be compensated at the NEM (retail) rate. In other words, there is no incentive to export more electricity than is consumed in the optimized case. However, if you add a value for “Compensation for excess export beyond annual site load ($/kWh),” then the system will receive compensation at the specified rate for the additional export beyond 100% of the site’s grid consumption. When using this input, the system size eligible for compensation will still be limited to the “Net metering system size limit (kW)." 

- **Net billing (not full retail rate) -** Choose this option if the DER system(s) will be compensated for grid exports at a rate that differs from the retail cost of electricity. This is often referred to as “net billing” or “wholesale rate” compensation. Once selected, enter the net billing compensation rate. When modeling net billing compensation, there is currently no limit placed on the system size that can receive compensation. If a compensation policy does limit the system size eligible for net billing, users can utilize the maximum system size inputs under the applicable technology (e.g., PV) section(s). 

- **Net metering or net billing options -** Choose this option to allow REopt to costoptimally determine whether to utilize net metering or net billing compensation. A common use case for this option would be a compensation policy that allows systems sized under a capacity limit to net meter (full retail rate compensation) but provides net billing compensation (not full retail rate) for the entire system if sized above the capacity limit. 

For both net metering and net billing options, users can select the technologies that can receive compensation for exported electricity. For net metering, the combined electric capacity of all the 

36 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

selected systems is used for the net metering limit. By default, it is assumed that CHP and Prime Generators cannot participate in net metering or net billing programs, as it is not uncommon for power export to be prohibited as part of a CHP interconnection agreement with the serving electric utility. 

## **6.2 Fuel Costs** 

Fuel costs are entered for analyses that include a fuel-burning technology. The fuel type and fuel costs must be entered for both the existing heating system and for the new technology (e.g., CHP or Prime Generator) if screened. Fuel types are used to track CO2 emissions associated with their consumption. No other defaults, including CHP prime mover performance and costs, are adjusted when the user changes the fuel type from the natural gas default. 

Fuel costs can be entered as a single annual value or as a monthly value. For natural gas and biogas, the user enters costs in units of $/MMBtu based on the HHV of the fuel, while the costs for diesel and propane are entered in units of $/gallon. For the analysis, entered unit costs are converted from $/gallon to $/MMBtu using HHV of the fuel. 

## **7 Loads** 

This section describes the required load inputs. Because the REopt web tool models a full year, the model requires typical load values for every hour of the year. If finer interval data is available, e.g., 15-minute interval data, the user can input that data and the REopt web tool user interface will down-sample it to 1-hour intervals. If running the API directly, the user can run at 15-minute, 30-minute, or 1-hour interval length. Because only one year of load is modeled, the implicit assumption is that the load does not change significantly from year to year over the analysis period. 

For PV, wind, and battery storage analysis, only electricity loads are needed. For CHP and GHP analysis, heating loads are also required. If the user considers chilled water TES or absorption chillers, cooling load interval data is also required. 

## **7.1 Actual (Custom) Load Profile** 

If available to the user, the user uploads actual interval load data for the facility. In the REopt web tool user interface, this is called a custom load profile. Actual load data will result in the most accurate results. If “Upload” is selected, the user must upload one year (January through December) of hourly, 30-minute, or 15-minute load data, in kW, by clicking the browse button and selecting a file. A sample custom load profile[8] is available, which includes an optional header and optional additional column A with the 8,760 hour-long intervals listed for reference. 

The file should be formatted as a column of 8,760, 17,520, or 35,040 rows. The file should be saved as a .csv file. If the file does not contain the correct number of rows (8,760, 17,520, or 35,040), or there are rows with blank entries, the user will receive an error message. 

In the web interface, the option to use 15-minute or 30-minute load data is provided for user convenience, not for higher model resolution. If 15-minute or 30-minute data is uploaded, it will 

> 8 https://reopt.nrel.gov/tool/load_profile_template.csv 

37 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

be down-sampled to hourly data for the evaluation. In the API, the user can run sub-hourly analysis. 

If the load profile is from a leap year, where an extra day’s worth of data is part of the file, the December 31 data should be deleted so that the file will be the correct length. Deleting December 31 will have the least impact on the evaluation results. The February 29 data should not be deleted, because it would impact the day of the week status for all days from March to December, and many utility rates have different rates for weekdays and weekends. The calendar year the load profile represents is entered in the ‘Year of load profile’ field. This information is needed to correctly apply tariffs that vary by days of the week. The default for this input is the current year. 

## **7.2 Simulated Load Profile from Models** 

If actual interval data is unavailable, the user has access to 16 load profiles from DOE Commercial Reference Building (CRB) models that can be used either to analyze one or a mix of the standard building types or to synthesize user-entered annual or monthly total values into hourly load profiles (see Table 2). The climate for CRB loads is selected based on the user’s entered location (see Table 3). In addition to using these load profiles, the user can model flat or constant loads. In the user interface, loads generated with CRB models and flat load options are called Simulated Load Profiles. 

The loads are generated from DOE’s post-1980 CRB models assuming ASHRAE 90.1-1989 building energy code for the climate zone of the site using EnergyPlus[®] simulation software. The simulated load profile is created for a generic year that starts on Sunday. Because January 1, 2017 is a Sunday, 2017 shows as the load year when using CRB loads. If the user uses Simulated Load Profiles and overwrites the default Annual Energy Consumption displayed in the interface for the selected building type model, the Simulated Load Profile will be scaled to match the user’s Annual Energy Consumption value. This is useful when the user has total annual energy consumption but requires use of the CRB hourly interval load values to synthesize interval data. The user can select to enter energy totals by month and the CRB hourly interval data will instead be scaled to match the monthly totals entered. The building chosen for the electric load simulation does not need to be the same building type chosen for the heating or cooling loads. 

38 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 2. DOE Commercial Reference Building Types** 

|**Building Type**|**Floor Area (ft2) **|**No. of Floors**|
|---|---|---|
|Large Office|498,588|12|
|Medium Office|53,628|3|
|Small Office|5,500|1|
|Warehouse|52,045|1|
|Stand-alone Retail|24,962|1|
|Strip Mall|22,500|1|
|Primary School|73,960|1|
|Secondary School|210,887|2|
|Supermarket|45,000|1|
|Quick Service Restauran|t<br>2,500|1|
|Full-Service Restaurant|5,500|1|
|Hospital|241,351|5|
|Outpatient Health Care|40,946|3|
|Small Hotel|43,200|4|
|Large Hotel|122,120|6|
|Midrise Apartment|33,740|4|



Source: https://energy.gov/eere/buildings/commercial-reference-buildings 

**Table 3. Climate Zones** 

|**Climate Zone**|**Representative City**|
|---|---|
|1A|Miami,Florida|
|2A|Houston,Texas|
|2B|Phoenix,Arizona|
|3A|Atlanta,Georgia|
|3B-Coast|Los Angeles,California|
|3B|Las Vegas,Nevada|
|3C|San Francisco,California|
|4A|Baltimore,Maryland|
|4B<br>|Albuquerque,New Mexico|
|4C|Seattle,Washington|
|5A|Chicago,Illinois|
|5B|Boulder,Colorado|
|6A|Minneapolis,Minnesota|
|6B|Helena,Montana|
|7|Duluth,Minnesota|



39 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Climate Zone**|<br>**Representative City**|
|---|---|
|8|Fairbanks,Alaska|



Dropdown menu options include the 16 modeled building types and flat load options—for a site with a relatively constant electric load. Flat loads are meant to approximate the hourly load(s) using average energy consumption values. These flat loads are based on different operating schedules (hours per day / days per week) listed below. The values for annual or monthly energy are spread out evenly throughout the days/hours included in the description of each load below (loads are zero for hours not included in descriptions): 

- 24/7 – constant load for all days/hours of the year (truly “flat”) 

- 24/5 – constant load for all hours of the weekdays 

- 16/7 – two 8-hour shifts for all days of the year; 6–10 a.m. 

- 16/5 – two 8-hour shifts for the weekdays; 6–10 a.m. 

- 8/7 – one 8-hour shift for all days of the year; 9 a.m.–5 p.m. 

- 8/5 – one 8-hour shift for the weekdays; 9 a.m.–5 p.m. 

The annual or monthly energy values for these flat loads are expected to be entered by the user; however, the model provides default annual energy load values which is the average of all the CRB types for a given climate zone. 

## _**7.2.1 Modeling a Campus with Multiple Simulated Building Load Profiles**_ 

The user can choose multiple commercial reference building types to model a space with mixeduse or multiple buildings on a campus. If “Simulate Campus” is selected, an annual electric consumption for the entire campus is entered along with up to five building types and the percentage of that annual total energy consumption that each of the building types is expected to consume. The simulated load for each building type will be scaled based on the percentage of the annual energy consumption entered. The REopt web tool will use the resulting blended simulated electric load profile in determining a single optimally sized energy system for the entire campus. 

## **7.3 Electric Loads** 

The electric interval data entered or generated with CRB models is the facility’s total electric consumption through the utility meter that DER could offset. There is no cost function for integrating multiple metering points within a facility and therefore it is assumed the loads entered are for a single electric meter and are addressable by DER. The units for electric interval load are kW. The units for Annual Energy Consumption and Monthly Energy Consumption are kWh. 

## _**7.3.1 Electric Load Adjustment**_ 

Users can adjust the electric load profile up or down by a specified percentage using the electrical load adjustment slider. The default value is 100% of the entered load, meaning no adjustment will be made. Entering a value greater than 100% will increase the load in each timestep. Entering a value less than 100% will decrease the load in each timestep. The adjustment applies to all three methods of entering the typical load, including simulate building, simulate campus, or upload.  The adjusted load will be used in the optimization and the results will be based on the adjusted load. This feature can be used to reflect the impact of energy efficiency measures that may reduce the electric load, or new construction that may increase the 

40 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

electric load. For a resilience analysis, adjustments made to the typical load through the load adjustment slider are also applied to the critical load if the “percent” critical load factor option is selected. If the “upload” or “build” option for the critical load is selected, the adjustment made to the typical load through the load adjustment slider will apply only to the typical load and will not change the uploaded or built critical load. 

## **7.4 Heating Loads** 

The heating load can include space heating, domestic hot water, industrial heating, and, if considering CHP, any high-temperature thermal energy provided to the absorption chiller if by CHP. 

The entered heating load interval data has units of fuel (MMBtu of fuel/hour, HHV-basis). Units of fuel, rather than heat, are used since it is assumed that the user is likely to have total fuel consumption from utility bills or invoices and will use CRB modeled heating loads to synthesize hourly interval data that matches the user-entered total fuel consumption. Fuel loads are converted to thermal values (heat) using the heating system thermal conversion efficiency. The resultant heating loads are gross loads on the plant; therefore, heat for a boiler deaerator makeup water and heating losses in the distribution piping are included. 

By default, the model assumes the entire heating (fuel) load entered can be served by (is addressable by) the CHP system. If some of the total heating load is not addressable by CHP (for example, it is used for cooking or other processes that are not served by the heating loop), the user can include a value for Addressable load percent (%) between 0 and 100% (single value for annual fuel energy or monthly values for monthly fuel energy. For GHP, the default assumption is that only space heating, not domestic hot water (DOMHW), is supplied by heat pumps. However, the user interface includes a toggle if the domestic hot water heating loads are also to be served by GHP. 

If GHP is not to serve domestic hot water, the determination of the split of fuel used for space heating and DOMHW depends on how the user enters the heating system fuel load. If the user enters annual or monthly gas usage and leverages the CRB models to synthesize the hourly loads, REopt parses the fuel for space heating and DOMHW using the hourly fractions from the CRB model. If the user enters their own hourly interval data or uses a flat load, the current assumption is that the fuel for space heating and DOMHW is split 50/50. A future improvement will allow the user to specify their own fraction of fuel that is used for space heating, and the remainder will be used for DOMHW. As a workaround, if the intention is to model a custom heating load that represents only space heating, the user should check the box for “Heat pump can serve the domestic hot water load” in the GHP accordion which will assume all of the userentered heating load can be served by GHP. 

Simulating a campus for the heating load is similar to what is described in Section 7.2.1 for the electric load; the user enters the annual fuel energy and the mix of buildings to shape the heating load profile. 

41 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **7.5 Cooling Loads** 

The electrical consumption of the cooling system is assumed to be included within the total facility electric load (i.e. it is a _subset_ of the total facility electric load). However, if the user is interested in modeling GHP, chilled water TES, or absorption chillers, the cooling load must be explicitly defined. The user has several options for specifying the cooling load that differ slightly from the total facility electric load and the heat load: 

1. Specify the building type(s) **only** (without annual or monthly cooling thermal energy values) using the _Simulate Building_ or _Simulate Campus_ tabs 

   - a. This uses simulated building’s hourly profile of _fraction of total facility electric load_ that is allocated to cooling. The cooling electric profile is converted to a cooling thermal profile using the cooling system COP. 

2. Specify the building type(s) **and** the amount of cooling thermal energy delivered by the cooling system using the _Simulate Building_ or _Simulate Campus_ tabs. 

   - a. This generates the hourly cooling thermal profile using the analogous method to total facility electric and heating load described above but with annual or monthly cooling thermal energy. 

   - b. **WARNING** : this method has a risk that the cooling-based electric load (converted from the user-entered cooling thermal load) **exceeds** the total facility electric load during certain hours of the year, which is non-sensical. However, the user will get an error immediately that specifies which hours of the year this occurs, and if this happens it is suggested to check the cooling thermal energy inputs and compare to the total facility electric load in more detail. 

3. Specify an annual or monthly fixed percentage of total electric load (%) using the _Custom_ tab. 

   - a. This applies the fixed percentage to the total facility electric load for each hour of the year (annual fixed percentage) or month (monthly fixed percentage), and it then converts the load to a thermal load using the cooling plant COP. 

The _Upload_ tab is used if the existing hourly cooling system thermal load (units of tons of cooling) is available. The associated electricity consumption is calculated using user-entered or default cooling system COP value. As described in Section 5.3, the COP is inclusive of the heat rejection electricity requirements. 

We assume cooling losses in the distribution system are captured in the entered cooling load; losses in distribution are not separately modeled. 

## **8 Resilience Analysis** 

By default, the REopt web tool optimizes systems to maximize grid-connected economics. Users have the option of specifying additional resilience requirements to design a system that will also 

42 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

sustain a critical load for a specified outage period. Users can select to model one or four outage periods. Modeling more outage periods should result in a more robust resilience solution. 

## **8.1 Critical Load** 

The critical load is the load that must be met during a grid outage. It can be calculated as a consistent percent of the typical load profile that is being used, uploaded as a separate custom load profile, or built specifically to correspond to important loads at the site. 

If “Percent” is selected, the critical load is a percentage of the typical load profile. This factor is multiplied by the typical load to determine the critical load that must be met during the specified outage period. If “Upload” is selected, the user can upload one year of hourly, 30-minute, or 15minute critical load data. If “Build” is selected, the user can create a custom critical load profile based on specified load components. Only the one active option for specifying the critical load will be applied to the optimization. 

## _**8.1.1 Critical Load Builder**_ 

The Critical Load Builder allows you to create a daily emergency load profile by building a list of equipment that is critical at your site—along with wattage, quantity, daily operation hours, and annual operation months. Once you have named, built, and saved critical load profiles, they will be available for selection from the Critical Load Profile dropdown menu on the main input page, and can be used in an optimization. You must be registered and logged in to a user account to access this feature. This tool is based on SolarResilient, a tool developed by Arup, under contract to the City and County of San Francisco, with funding from DOE. 

To build a new critical load profile, the registered and logged-in user can click the “Build New Critical Load Profile” link and build a new load in the resulting pop-up window while retaining the other inputs already entered. Alternatively, the user can click “Build, copy, and manage your critical load profiles” below the blue box, or “Critical Loads” in the top right-hand corner of the webpage and be taken to a different page to either copy and edit a previously built critical load or to build a new critical load profile from component electrical loads. If the user chooses either of these options, a new evaluation must be started and all inputs that had been entered for the current optimization will need to be re-entered. 

To build a critical load profile: 

- Start by entering a name for the Critical Load Profile. Once you have named, built, and saved critical load profiles, they will be available for selection from the Critical Load Profile dropdown menu on the main input page, and can be used in an optimization. 

- Select load components from the dropdown list. The load component will populate with default suggestions for the power, hours, and months. 

- Once added, you can edit the details of the load component to better simulate your critical load conditions. 

- Add as many load components as necessary. The last load in the dropdown menu is a custom load, which can be used as a starting point to add components that are not in the menu. 

43 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

_Note that these components are being modeled as flat loads at user-specified power and operation times. There is no cycling, for example, on the air conditioner or space heater. The load does not change based on the weather or room temperature._ 

## **Load Type** 

Select a preexisting load type and add the load component to your new critical load profile. Once added, you can edit the details of the load component to best simulate your critical load conditions. Add as many load components as necessary. 

## **Power (W)** 

This is the power requirement for the selected load type. Default values are taken from Lawrence Berkeley National Laboratory’s Home Energy Saver Engineering Documentation,[9] ENERGY STAR Certified Product data sets,[10] and the DOE Appliance and Equipment Compliance Certification Database.[11] Many appliances have the wattage stamped on the unit, representing the maximum power drawn by the appliance. The wattage can also be estimated by multiplying the electric current draw, in amperes, by the voltage used by the appliance (typically 120 volts). Amperes may be stamped on the unit or listed in the owner’s manual. Energy.gov also provides a calculator for estimating appliance and electronic energy use.[12] 

## **Start Hour** 

Start hour is represented similar to military time. For example, 0 represents 12 a.m. and 16 represents 4 p.m. To simulate a component that would run all day, the start hour would be 0 and the end hour would be 24. To simulate a component that runs from 3 a.m. to 5 p.m., the start hour would be 3 and the end hour would be 17. The start hour must be a whole number and cannot be greater than 23 (representing 11 p.m.). 

## **End Hour** 

End hour is represented similar to military time. For example, 1 represents 1 a.m., 13 represents 1 p.m., and 24 represents 12 a.m. **on the following day** . To simulate a component that would run all day, the start hour would be 0 and the end hour would be 24. To simulate a component that runs from 3 a.m. to 5 p.m., the start hour would be 3 and the end hour would be 17. The end hour must be a whole number and cannot be less than 1 (representing 1 a.m.). 

## **End Month** 

To specify a load component duration of one month, select the same start month and end month. The year of the custom critical load profile is assumed to be the same as the year set for the custom load profile. 

The Critical Load Profiles summary allows you to view, edit, and copy the critical load profiles that you have built. The table lists your critical load profiles in the chronological order in which they were created. The name and description you assigned are listed in the table along with the 

> 9 http://hes-documentation.lbl.gov/calculation-methodology/calculation-of-energy-consumption/majorappliances/miscellaneous-equipment-energy-consumption/default-energy-consumption-of-mels 

> 10 https://www.energystar.gov/productfinder/advanced 

> 11 - = * https://www.regulations.doe.gov/certification data/products.html#q Product_Group_s%3A 

> 12 https://www.energy.gov/energysaver/save-electricity-and-fuel/appliances-and-electronics/estimating-applianceand-home 

44 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

minimum, average, and maximum loads. The dates for the minimum and maximum load values refer to the first chronological instance of that minimum or maximum load. If you wish to look at the details of the critical load profiles by time period, click on the icon to view load profile components. Icons are also available to chart or download the critical load profile. Once a critical load profile has been used in an optimization, that particular load profile can no longer be edited or deleted. However, the load profile can be copied to create a new or corrected load profile. 

## **8.2 Outage Start Time and Duration** 

The user specifies the outage period(s) that the system must sustain by specifying the outage start date, time, and duration (number of hours). It is a user’s option to model either one or multiple outage periods. 

The single-outage model allows users to specify one outage during the year. The user can choose to automatically populate the outage start date and time with the date and time centered around the maximum load hour using the “autoselect using critical load profile” link. The multipleoutage model allows users to specify four outages during the year. For the multiple-outage model, default outage periods will be auto-selected based on the critical load profile, with the outages centered around the seasonal peaks. Users can override the default values with custom outage start dates and times. Modeling multiple outages may result in REopt recommending a more costly system; however, the tradeoff is likely a system that is more reliable during grid outages.With a resilience analysis, the system will be configured to minimize the life cycle cost of energy, with the additional requirement that it must also sustain the critical load during the outage periods specified. The outage duration must be a number between zero and 672 hours. 

In general, selecting an outage start date when the site’s load is higher (often summer) will result in larger system sizes that can sustain the critical load during more outages. Selecting an outage period during a time of year when the site’s load is lower may result in smaller system sizes that sustain the critical load during fewer outages. However, solar and/or wind resource will also impact the resiliency of the system. 

The outage events may change the size or DER types selected in the optimization. However, the outage periods do not impact the lifecycle costs of grid purchased electricity and any additional fuel burned during the outage periods is not added into the life-cycle costs. 

For information on typical outages in the United States, the user can check Electric Power Monthly, the U.S. Energy Information Administration’s compilation of the location, duration, and description of major electric disturbances by month. 

## **9 Renewable Energy and Emissions** 

The REopt web tool provides metrics on renewable energy (RE) consumption and avoided emissions associated with the identified combination of DER technologies. Avoided climate and health-related emissions are reported both in mass (metric tons) and monetary impacts on climate and public health, and account for emissions from grid-purchased electricity and on-site fuel consumption (e.g., for a modeled backup generator or natural gas heating). 

45 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

In the web tool, the “Renewable Energy and Emissions Accounting” accordion contains modifiable default values for RE and emissions inputs. By selecting “Clean Energy” in the “Choose Your Energy Goals” section, users can additionally define a renewable electricity or emissions reduction target or include climate and/or health costs in REopt’s objective function. REopt’s key inputs and outputs related to RE and emissions are summarized in Table 4. 

**Table 4. Summary of key inputs and outputs related to renewable energy and emissions calculations in REopt. All inputs include default values that can be overridden by the user.** 

**==> picture [468 x 398] intentionally omitted <==**

**----- Start of picture text -----**<br>
Key Outputs Related to Renewable<br>User Inputs Related to  Energy and Emissions<br>Renewable Energy and Emissions  (Reported for Business-As-Usual<br>and Investment Cases)<br>• Renewable content of fuels burned on-site • Percentage of electric load<br>powered by on-site renewable<br>• Electric grid climate emissions factors  (hourly<br>electricity<br>using Cambium data, annual, or custom upload)<br>[metric tons/kWh]   • Percentage of combined electric<br>and thermal loads served by on-<br>• Electric grid health-related emissions factors<br>site renewable energy<br>(hourly using AVERT, annual, or custom upload)<br>[metric tons/kWh]  • Climate emissions  (CO2e) over<br>the analysis period and an<br>• Projected decrease  in climate and health<br>average year<br>emissions factors from grid electricity [1]<br>• Health emissions  (NOx, SO2,<br>• Treatment of  exported electricity  (included vs.  PM2.5) over the analysis period and<br>excluded in renewable energy and/or emissions<br>an average year<br>goals)<br>• Breakdown of climate and health<br>• Cost of climate emissions  [$/metric ton]  emissions by  on-site fuel burn<br>• Cost of health-related emissions  from on-site  vs. grid-purchased electricity<br>fuel consumption and from grid electricity  • Cost of climate emissions<br>[$/metric ton]<br>• Cost of health emissions<br>• Escalation rate  of health-related emissions<br>costs [%]<br>• Optionally define an onsite renewable energy<br>or emissions reduction target<br>• Optionally include climate and/or health costs<br>the model’s objective function  (treat as true<br>costs)<br>**----- End of picture text -----**<br>


1 The projected decrease in climate emissions factors is zeroed out when using Cambium data, as these datasets include levelized emissions factors that already account for the projected evolution of the grid. 

Note that for resilience analyses, renewable energy and emissions calculations do _not_ account for operations during grid outages (calculations are made as if no outages occurred). 

The sections below detail the REopt tool’s RE and emissions accounting methodologies, default data sources for grid and fuel emissions factors, and user-defined clean energy goals. 

46 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **9.1 Renewable Energy Accounting** 

REopt calculates the quantity and proportion of the electricity and thermal loads served by renewable energy in the Business-as-Usual (BAU) case and the Optimal (Investment) case. Table 5 summarizes the assumed renewable energy factor (REF) for each technology, and whether the technology generates electricity, heat, or both. For technologies that generate both electricity and heat, the REF is assumed to apply to both its electricity generation and its heat generation. Grid electricity is not currently ascribed any renewable energy attribute, so REopt’s RE accounting currently only includes RE generated onsite. 

**Table 5. Renewable energy contributions by technology** 

|**Technology**|**Percent of generation assumed to be**<br>**renewable**<br>**(“Renewable energy factor (****_REF_)”)**|**Generates electricity,**<br>**heat, or both?**|
|---|---|---|
|Solar PV|100%|Electricity|
|Wind|100%|Electricity|
|Emergency Generator|User-input (0-100%)1, based on percentage of<br>fuel classified as renewable|Electricity|
|Prime Generator|User-input (0-100%)1, based on percentage of<br>fuel classified as renewable|Electricity|
|Boilers|User-input (0-100%)1, based on percentage of<br>fuel classified as renewable|Heat|
|CHP|User-input (0-100%)1, based on percentage of<br>fuel classified as renewable|Both electricity and<br>heat|
|Steam Turbine|Calculated (0-100%) based on source(s) of<br>steam; depends on what portion of the steam<br>used to power the steam turbine is generated<br>from renewable fuels|Both electricity and<br>heat|
|GHP|Calculated (0-100%) based on site’s fraction of<br>electricity derived from renewable generation|Heat|
|ASHP|Calculated (0-100%) based on site’s fraction of<br>electricity derived from renewable generation|Heat|



1 The default REF for all fuels is 0%. 

Note that these REFs are distinct from, and not applied to, emissions factors or calculations. Fuel emissions factors should be separately entered after considering any renewable composition of the fuel and whether the user wants to include emissions associated with combustion of renewable fuels. For instance, if a site burns fuel that is 10% from landfill gas and enters 10% renewable fuel as an input, the emissions rate input by the user is _not_ decreased by 10%. 

47 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

By default, exported electricity is included in RE and emissions calculations. However, users can opt to exclude excess renewable electricity generation that is exported to the grid as contributing to site RE (and/or emissions) totals. Some policies assign RE attributes of onsite generation exported to the grid to the host site, but in some regions those RE attributes go to the utility, especially if the site is compensated for the generation via net metering. Additionally, for third party ownership arrangements, some state and utility policies assign RE attributes to the developer rather than the host site/off-taker. Users should research policies applicable to their site in making this selection. 

RE outputs on the REopt results page include: 

- **Percentage of annual electric load served by renewable electricity:** Annual RE consumption is calculated as total annual onsite RE generation, minus battery storage losses and considering curtailment, with the user selecting whether exported renewable electricity is included or excluded from the total (see note below). Note that this includes any renewable contributions to electric heating (i.e., GHP) and/or cooling (i.e., electric chiller, absorption chiller) loads. This value is divided by total annual electric load to determine the percentage renewable electricity. 

- **Percentage of total annual energy consumption (electric loads plus steam/hot water thermal loads) served by renewable energy:** The numerator is calculated as total annual renewable electricity consumption (see above) plus total annual thermal energy content of steam/hot water generated from renewable fuels (non-electrified heating loads). The thermal energy content is calculated as total energy content of steam/hot water generation from renewable fuels, minus waste heat generated by renewable fuels, minus any applicable hot water thermal energy storage efficiency losses (decay rate not considered). The denominator is calculated as total annual electric load (including electric heating (i.e., GHP) and/or cooling (i.e., electric chiller, absorption chiller) loads) plus total annual thermal steam/hot water load (including steam for absorption chiller). 

   - Note: In cases involving steam turbines, some fuel-burning technologies (boiler and CHP) can provide steam to the steam turbine. In calculating annual steam load (and contribution of renewable energy to this steam load), the thermal energy content of the steam feeding the steam turbine is not included in the total steam load as some of it may be used to produce electricity, but thermal output from the steam turbine is included. 

Both the renewable electricity and renewable energy percentage outputs focus on annual _consumption_ rather than annual generation. Renewable content of generation will always be greater than or equal to that of consumption, depending on technology performance and efficiency losses. Reporting renewable content of consumption avoids double-counting of energy consumption by technologies that operate at the intersection of electricity and thermal consumption or generation. 

In cases involving GHP, converting a heating source from fuels to electricity increases electricity demand and decreases steam/hot water heating loads (and fuel consumption). Thus, the renewable heat output is inclusive of the renewable electricity used to power GHP, so the 

48 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

renewable heat and renewable electricity outputs are not additive in cases involving GHP. They are additive in all other cases. 

Unlike emissions accounting options, no dollar value (e.g., $/kWhRE or $/MMBTURE) is attributed to overall RE generation. To account for a monetary value of RE generation, users can enter a production incentive for a specific technology (e.g., $/kWh for PV generation). 

## **9.2 Climate and Health Emissions** 

## _**9.2.1 Emissions Accounting Overview**_ 

REopt estimates climate and health impacts of DERs based on avoided emissions from the electric grid and on-site fuel consumption. Climate impacts are estimated by changes in carbon dioxide equivalent (CO2e)[13] emissions, which are known to trap heat in the atmosphere and contribute to climate change (NASA, 2024) and thus increase risks ecosystems, livelihoods, food security, water supplies, security, health, and economic growth (IPCC, 2022). Health impacts are estimated by changes in nitrogen oxides (NOx), sulfur dioxide (SO2), and primary particulate matter 2.5 microns or less in width (PM2.5), which affect human health through their secondary formation of ambient PM2.5. Together, these three species account for approximately 96% of the PM2.5 exposure, and associated increase in premature mortalities, from the electricity sector (Dedoussi & Barrett, 2014). In 2018, across the contiguous U.S., approximately 8,500 early deaths were attributable to emissions from electric power generation (Dedoussi, Eastham, Monier, & Barrett, 2020). 

Emissions are calculated over the analysis period and for an average year, accounting for an expected change in the emissions rate of grid electricity over time. The monetary cost of climate emissions is calculated as the social cost of carbon [$/metric ton CO2e] multiplied by expected CO2e emissions [metric tons]. The total climate emissions cost over the analysis period accounts for an assumed year-over-year escalation rate of the cost of carbon emissions as well as expected decrease in grid emissions rates over time. The monetary cost of health-related emissions is calculated as the location- and pollutant-specific health damage cost [$/metric ton NOx, SO2, and PM2.5] multiplied by expected emissions of each species [metric tons]. The total health emissions cost over the analysis period accounts for an assumed year-over-year escalation rate of the cost of health-related emissions as well as expected decrease in grid emissions rates over time. 

As marginal grid emissions rates are used by default in REopt, users should focus on the change in emissions and emissions costs between the BAU and investment cases, rather than the absolute emissions totals. See Section 19.7.3 for more details on interpreting emissions results. 

Users can select to consider grid emissions offset by exported electricity in the emissions calculations (the default behavior), or to exclude these exports. Emissions inventories and reporting protocols such as the Greenhouse Gas Protocol do not allow users to count exported renewable electricity as an emissions offset, but academic users may want to include these since realistically these exports are displacing grid generation and the associated emissions. 

> 13 By default, REopt uses CO2e emissions data to estimate climate impacts of DERs. However, users may instead enter CO2 data for grid emissions factors and on-site fuel consumption, if desired. 

49 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

The following sections describe the default grid and on-site fuel emissions factors and emissions costs used in REopt, along with options with user-modifiable inputs. 

## _**9.2.1 Electric Grid Emissions Factors**_ 

Electric grid emissions rates can be reported at varying time and geographic scales, using average or marginal metrics, and at different points along the transmission and distribution (T&D) system. See Table 6 for examples of emissions rate variables, and an explanation of marginal vs. average emissions rates. 

REopt’s default climate and health emissions rates for grid-purchased electricity are hourly marginal emissions rates that include T&D losses. Marginal emissions rates are used by default in REopt to capture avoided emissions resulting from the introduction of new DERs at a site. At this time, default grid emissions rates are not available for sites outside of the United States. Users can override default emissions inputs based on their needs, or provide emissions inputs if defaults are not available (e.g., for international sites). The type of emissions data used in a REopt analysis should depend on the user’s goals and applicable emissions accounting protocols. 

## _9.2.1.1 Climate Emissions Factors for the Contiguous United States_ 

For site locations in the contiguous U.S., grid climate emissions data is obtained from NREL’s Cambium database (https://scenarioviewer.nrel.gov/), which contains modeled emissions projections for a range of possible futures of the U.S. electricity sector through 2050 (Gagnon P. S., 2024). The default grid climate emissions factors in REopt are hourly, long-run marginal emissions rates[14] (LRMERs) for CO2e averaged over the analysis period at a resolution of “generation and emission assessment (GEA) regions.” CO2e values are calculated using 100-year (AR6) global warming potential values (GWP) from the IPCC’s Sixth Assessment Report (2023), with GWP values for CO2, CH4, and N2O of 1, 29.8, and 273, respectively. The default emissions rates include precombustion and combustion emissions and T&D losses. 

> 14 LRMERs have been shown to outperform average and short-run marginal emissions rates at estimating emissions impacts of changes in end-use electrical load 

> (https://www.sciencedirect.com/science/article/pii/S2589004222001857?via%3Dihub). 

50 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [384 x 259] intentionally omitted <==**

**Figure 2. Cambium’s generation and emission assessment (GEA) regions, 2023 version (Gagnon P. S., 2024). This is the default geographic resolution for the long-run marginal emissions rates used in REopt.** 

An _averaged_ (i.e., levelized without discounting) hourly LRMER emissions profile is used to capture the multi-year impacts of DERs within REopt’s single year optimization. For instance, for a project beginning in 2024 with an analysis period of 25 years, the default emissions profile will reflect projected emissions rates averaged (with no weighting of out-years) on an hourly basis from 2024 through 2048 (Gagnon P. S., 2024). 

Users can choose to modify the grid climate emissions projections used in the analysis by changing any of the inputs shown in Table 6. The version of Cambium (i.e., year of data release) used for default REopt inputs is listed in the “Defaults” section of this manual. 

**Table 6. User-modifiable inputs to generate hourly levelized grid climate emissions factors from NREL’s Cambium data sets, for locations in the contiguous United States. See the Cambium Documentation for more details on each input (Gagnon P. S., 2024).** 

|**Input**|**Description**|**Options (REopt default in bold)**|
|---|---|---|
|**Geographic**<br>**resolution**|Geographic unit at which grid emissions<br>are determined.|•<br>**GEA Regions: Cambium Generation and**<br>**Emission Assessment region (GEA). These**<br>**are 20 regions covering the contiguous**<br>**United States that are based on (but not**<br>**identical to) the U.S. Environmental**<br>**Protection Agency's (EPA's) eGRID**<br>**regions.**<br>•<br>Nation:Entire contiguous U.S.|
|**Metric**|Grid emissions metric type.|•<br>Average emissions rates (AER) Generation<br>CO2Combustion<br>•<br>AER Generation CO2e Combustion|
||(See explanations below.)||
||||



51 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [251 x 146] intentionally omitted <==**

- AER Generation CO2e Combined 

- AER Load CO2 Combustion 

- AER Load CO2e Combustion 

- AER Load CO2e Combined 

- Long-run marginal emissions rates (LRMER) CO2 Combustion 

- LRMER CO2e Combustion 

- **LRMER CO2e Combined** 

- Short-run marginal emissions rates (SRMER) CO2 Combustion 

- SRMER CO2e Combustion 

- SRMER CO2e Combined 

## Metric type explanations: 

## **AER vs. LRMER vs. SRMER:** 

- Average emissions rates (AER): average emissions rate of all generation within a region for a specified duration. 

- Marginal emissions rates: quantify the change in grid emissions that result from a marginal change in gridpurchased electricity. 

   - Short-run marginal emissions rates (SRMER) represent the immediate operational response of the electric grid to an increase. 

   - Long-run marginal emissions rates (LRMER) additionally account for how a perturbation in load may influence the building and retiring of generation and transmission lines on the grid. 

   - For further discussion of use of marginal and average emissions rates, refer to (Ryan, Johnson, & Keoleian, 2016) and (Gagnon P. S., 2024). 

## **CO2 vs. CO2e:** 

- CO2: carbon dioxide 

- CO2e: CO2 equivalent. Combined impact of CO2, CH4, and N2O using 100-year global warming potential values from the Intergovernmental Panel on Climate Change (IPCC) _Sixth Assessment Report_ . 

- **Combustion vs. Combined:** 

- Combustion: Emissions from direct combustion. 

- Combined: Precombustion (including fuel extraction, processing, and transport) + Combustion emissions. 

- **Generation vs. Load (for AERs only):** 

- Generation: average emissions rates of in-region generation. No adjustments for policy-related accounting. 

- • Load: average emissions rates induced by a region's load. Includes effects of imported and exported power; reflects credit trading for state portfolio standards; and assigns emissions to storage technologies based on the weighted average emission rates when the storage generators were charging. 

   - **Mid-case** 

   - Low Renewable Energy and Battery Costs 

Cambium grid future scenario used to **Grid scenario** estimate out-year emissions. **Use emissions averaged** Whether to account for the projected **over the** evolution of the grid or utilize a single **analysis** year’s emissions factors. **period?** 

- High Renewable Energy and Battery Costs 

- • High Demand Growth 

- Low Natural Gas Price 

- High Natural Gas Price 

- Mid-case with 95% Decarbonization by 2050 

- • Mid-case with 100% Decarbonization by 2035 

- **Yes: Utilize grid emissions factors that are averaged over the analysis period in order to capture the emissions impact of the identified technologies throughout the planning horizon. (Note: The analysis period can be modified under the “Financial” accordion.)** 

- • No (use a single year's emissions): Assume that grid emissions factors for a chosen year 

52 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|||remain the same throughout the analysis<br>period. Users can specify this year by entering<br>a specific “Emissions year” between 2024 and<br>2050.|
|---|---|---|
|**Emissions**<br>**year(s)**|The year(s) of the climate emissions data<br>used to calculate the emissions impact of<br>h d hli Dd|•<br>**If “Yes” is selected for “Use emissions**<br>**averaged over the analysis period?”, then**<br>**this input field will not be modifiable, and**<br>**will display the range of years used to**<br>**calculate the average hourly emissions**<br>**profile (starting in current year and**<br>**extending for the analysis period.**<br>•<br>If “No (use a single year's emissions)” is<br>selected for “Use emissions averaged over the<br>analysis period?”, then this field will be<br>modifiable, and users can enter a year<br>available within the Cambium dataset. In this<br>case, REopt's calculated emissions impacts<br>will assume that each year of the analysis<br>period has the electric grid climate emissions<br>factors of the yearenteredhere.|
||te suggeste tecnooges. epens on<br>it “U ii d  th||
||npu se emssons average over e<br>analysis period?”.||
|**Include**<br>**distribution**<br>**losses?**|Whether distribution losses are included<br>in the calculated emissions factors.<br>“**Busbar**” refers to the point where bulk<br>generating stations connect to the grid;<br>emissions rates at this point do not<br>include distribution losses. “**Enduse**”<br>refers emissions rates at the point of<br>consumption, including distribution<br>losses. Enduse emissions rates will be<br>higher than busbar emissions rates (with<br>the difference equal to the estimated<br>distribution loss rate between the two<br>points).|•<br>**Yes (use enduse emissions)**<br>•<br>No (use busbar emissions)|



## _9.2.1.2 Health Emissions Factors for the Contiguous United States_ 

At the time of this writing, Cambium data sets do not contain projections for health-related emissions of the U.S. electricity sector. Therefore, for site locations in the contiguous United States, default grid health-related emissions factors (SO2, NOx, and PM2.5) in REopt are obtained from the EPA’s AVoided Emissions and geneRation Tool (AVERT) 

(https://www.epa.gov/avert). The default health-related emissions data are hourly marginal 

emissions factors for the EPA AVERT region corresponding to the site’s location and accounting for T&D losses.[15] The version of AVERT used for default data is listed in the “Defaults” section of this manual. Unlike the climate emissions, users do not have the option to change the emissions type or exclude T&D losses for REopt’s grid health emissions factors. 

> 15 A 1 MW load is entered into the AVERT spreadsheet for every hour of the year on the 'Enter EERE data' tab (1 is entered in "Reduce each hour by constant MW", cell G17) to determine the marginal emissions impact of a reduction in load. 

53 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

AVERT data are based on historical grid operations for a single year, whereas Cambium data are based on modeled grid operations for future years. To account for the evolution of the electric grid in the health emissions data used in REopt, a projected year-over-year annual percent decrease in grid emissions factors is applied to the emissions factor profiles for NOx, SO2, and PM2.5. As forward-projected emissions factors do not yet exist for these emissions species, in REopt, health-related emissions are approximated to decrease at the same rate as climate emissions. The default projected annual percent decrease in grid health emissions factors is thus calculated as the U.S. national average percent decrease in long-run marginal CO2e (Combined Combustion+Precombustion) emissions from the first and last year available in the latest NREL Cambium dataset, assuming the Mid-Case scenario (Gagnon P. S., 2024). In the REopt API, a user can enter separate percent decrease values for each emission species. 

## _9.2.1.3 Climate and Health Emissions Factors for Alaska and Hawaii_ 

Neither Cambium nor AVERT currently contain emission factors for Hawaii and Alaska. If a site is in Hawaii or Alaska, REopt’s default grid climate and health emissions rates are annual emissions factors from the EPA eGRID database (U.S. Environmental Protection Agency, 2023). The default data are eGRID’s ‘non-baseload’ emission rates, which most closely emulate marginal emissions factors. The non-baseload emissions factors are adjusted to account for subregion-specific T&D losses. CO2e values are calculated using 100-year (AR6) global warming potential values (GWP) from the IPCC’s Sixth Assessment Report (2023) (aligning with the GWP values used in REopt’s default Cambium data). The resulting climate and health emission rates for Alaska and Hawaii are in **Table** _**7**_ . PM2.5 emissions are assumed to be zero due to lack of available data. 

**Table 7. EPA eGRID 2022 emission factors, EFg, for grid electricity in Alaska and Hawaii. CO2e values are used for REopt climate emissions calculations. NOx, PM2.5, and SO2 are used for REopt health emissions calculations.** 

|**State**|Alaska|Hawaii, excluding<br>Oahu Island|Hawaii, Oahu Island|
|---|---|---|---|
|**eGRID Subregion Acronym**|AKGD|HIMS|HIOA|
|**eGRID Subregion Name**|ASCCaAlaska Grid|HICCbMiscellaneous|HICCbOahu|
|**T&D Losses**|5.0%|5.4%|5.4%|
|**eGRID Subregion**<br>**Annual Emission**<br>**Rate with T&D**<br>**Losses**<br>**CO2e [lb/kWh]** <br>**NOx [lb/kWh]** <br>**PM2.5 [lb/kWh]** <br>**SO2 [lb/kWh]**|1.294|1.719|1.922|
||0.007|0.012|0.005|
||N/A|N/A|N/A|
||0.0006|0.0043|0.0077|



a. ASCC = Alaska Systems Coordinating Council 

b. HICC = Hawaiian Islands Coordinating Council 

The annual average of the default marginal health emissions rates for each region are in Figure 3. 

54 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [227 x 166] intentionally omitted <==**

**==> picture [226 x 166] intentionally omitted <==**

**==> picture [233 x 172] intentionally omitted <==**

**Figure 3. Annual average of the default hourly marginal emissions factors for SO2, NOx, and PM2.5 for grid electricity in each AVERT or eGrid (for HI and AK) subregion used in REopt.** 

(AVERT Regions: Upper Midwest (WMW), Rocky Mountains (RM), Lower Midwest (SC), Northwest (NW), Great Lakes / Mid-Atlantic (EMW), Southeast (SE), Southwest (AZNM), Texas (TX), Northeast (NE), California (CA); eGrid Regions: Hawaii, Oahu Island (HI-Oahu), Hawaii, excluding Oahu Island (HI), Alaska (AK)) 

## _9.2.1.4 Custom User-Provided Climate and Health Emissions Data_ 

As an alternative to the default grid climate and health emissions factors, or for sites outside of the United States, users can enter a single annual grid emissions rate or custom hourly profiles for each emissions species in lbs/kWh. The single annual grid emissions rate is applied to gridsourced electricity in each hour of the year. The custom hourly profiles should include columns corresponding to CO2e for climate emissions and NOx, SO2, and PM2.5 for health emissions. If default values are not available for a given location and no emission rate selection is made, emissions from the electricity grid will not be calculated and will be reported as zero. 

## _**9.2.2 Fuels Emissions Factors**_ 

Emission factors for on-site fuel consumption default to the assumed value for the user-selected fuel type as shown in Table 8. 

**Table 8. Default fuel-specific emissions factors used in REopt.** 

**Used to Calculate CO2e Default Emissions Factors** 

55 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Fuel Type**|**Applicable**<br>**Technology**|**CO2 **a|**CH4**<br>**a**|**N2Oa**|**CO2e **|**NOxb**|**SO2 b**|**PM2.5 b**|
|---|---|---|---|---|---|---|---|---|
|Natural Gas<br>[lb/MMBtu]|Boiler, CHP|116.9|2.2E-3|2.20E-04|117.03|0.0914|5.79E-4|7.33E-3|
|Landfill gas,<br>other biomass<br>gases<br>[lb/MMBtu]|Boiler, CHP|114.8|7.05E-3|1.39E-03|115.38|0.14|0.045|0.02484|
|Propane<br>[lb/MMBtu]|Boiler, CHP|138.6|6.61E-3|1.32E-03|139.16|0.153|0|9.91E-3|
|Diesel fuel,<br>NO. 2<br>[lb/MMBtu]|Boiler, CHP|163.1|6.61E-3|1.32E-03|163.61|0.56|0.289|0|
|Diesel<br>[lb/gallon]|Generator|22.51|9.04E-4|1.76E-04|22.58|0.0776|0.0400|0|



a. (GHG Emission Factors Hub, 2023) 

b. (U.S. Environmental Protection Agency, n.d.) 

CO2, CH4, and N2O emissions factors for each fuel type were obtained from the EPA Greenhouse Gas Emissions Factor’s Hub for 2023 (U.S. Environmental Protection Agency, 2023). CO2e values were calculated using 100-year (AR6) global warming potential values (GWP) from the IPCC’s Sixth Assessment Report (2023), with GWP values for CO2, CH4, and N2O of 1, 29.8, and 273, respectively. 

NOx, SO2, and PM2.5 emissions factors for each fuel type were calculated from the EPA’s WebFIRE database (U.S. Environmental Protection Agency, n.d.). In the WebFIRE database, fuel-specific emissions factors were filtered to exclude technologies not modeled in REopt, as well as very large system sizes not expected to be used in most commercial applications. Entries in the database with data quality “U”, indicating an unverified emissions rate, were also removed. Commercial/Institutional values were used where applicable. The fuel- and speciesspecific average of the resulting NOx, SO2, and PM2.5 emissions factors are used as the default values (Table 8). These health emissions averages encompass multiple control types and technology types. While CO2e emissions factors are primarily dependent on fuel type, NOx, SO2, and PM2.5 emissions factors vary by specific technology and emissions controls. Because these differences are not captured in the REopt defaults, users should supply emissions factors specific to their technology options whenever possible. 

## _**9.2.1 Emissions Costs**_ 

For the identified DER technology sizes, REopt estimates the avoided climate cost of CO2e emissions and health cost of NOx, SO2, and PM2.5, using cost per metric ton (t) valuations of the impacts of each emissions species. 

## _9.2.1.1 Climate Emissions Costs_ 

The default value of $51/t CO2 (in $2020) is the average social cost of CO2 using a 3% discount rate as determined by the U.S. Interagency Working Group on Social Cost of Greenhouse Gases (Interagency Working Group on Social Cost of Greenhouse Gases, United States Government, 2021). This monetary value captures climate change impacts of CO2e emissions, including (but not limited to) changes to net agricultural productivity, property damage from increased flood risk, disruption of energy systems, and changes to the value of ecosystem services. Climate costs over the analysis period account for an average annual percent increase in the nominal social cost 

56 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

of CO2 of 4.02%/year, nominal, calculated as the compound annual growth rate (CAGR) of the Interagency Working Group’s forward-projected costs.[16] 

## _9.2.1.2 Health Emissions Costs_ 

Marginal health costs of emissions are dependent on the local population, atmospheric conditions, and the height from which emissions are released (Heo, Adams, & Gao, 2017). REopt therefore utilizes separate health cost inputs for on-site fuel burn and grid emissions. The default marginal health costs are annual averages from the extensively-validated Estimating Air Pollution Social Impact Using Regression (EASIUR) model, as cited in multiple sources (Heo, Adams, & Gao, 2017), (Vaishnav, Horner, & Azevedo, 2017) and (Sergi, et al., 2020). EASIUR is a reduced-form air quality model that estimates the increase in premature deaths caused by an increase in PM2.5 precursor emissions (including NOx, SO2, and primary PM2.5) in a given location. The EASIUR model estimates health costs across the continental United States and parts of Canada and Mexico at a spatial resolution of 36 km x 36 km. 

The default marginal emissions health costs in REopt assume emissions occur at the building location, with grid emissions released at 150 meters above ground (emulating a smokestack) and on-site fuel burn emissions released at ground level. Defaults assume a population and emissions year of 2020 and adjust the marginal costs to $2020. Emissions costs over the analysis period account for an annual percent increase in the marginal health costs of NOx, SO2, and PM2.5, calculated as the CAGR of the EASIUR marginal health costs at the site’s location for income and population years of 2020-2024, assuming emissions released from 150 meters (2024 is the last year for which data are available in the reference). These values are in $2010 (therefore the CAGR is a real rate) and the costs are linear with respect to time. We adjust the real CAGR to the nominal CAGR using an assumed average inflation rate equal to the O&M cost escalation rate.[17] 

## **9.3 Clean Energy Targets** 

By selecting “Clean Energy” in the step “Choose Your Energy Goal,” users can enter a renewable electricity target, emissions reduction target, and/or can consider emissions climate costs as true financial costs. REopt will identify the least-cost DER system that meets these userdefined goals. Note that including renewable electricity and/or emissions reductions targets could increase solve times or cause infeasibilities, especially when considering thermal technologies or battery storage. 

## _**9.3.1 Renewable Electricity Targets**_ 

Users can opt to set an annual renewable electricity target for their site in the form of a minimum and/or maximum percentage of the site’s electric load that should be served by renewable 

16 To convert from real to nominal escalation rate, we assume an inflation rate equal to the default O&M cost escalation rate. 

> 17 The annual percent increase is unique to each location and each pollutant. However, to simplify the modeling workflow and because the REopt web tool focuses mainly on grid emissions, we calculate the annual percent increase of emissions costs only for a release height of 150 meters (as opposed to calculating separate cost escalation rates for on-site fuel burn). For a given location, the annual percent increase in emissions factors for a release height of 150m differs by approximately 0.2% as compared to the percent increase for a release height of 0m. 

57 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

electricity. REopt identifies the least-cost technology mix, sizing, and dispatch to meet this target. 

If a user wants “at least” x% of their annual electric load met with renewable generation, they can set a minimum renewable electricity target of x%. Alternatively, if the user wants “exactly” x% of their annual electric load me with renewable generation, they can set the minimum and maximum renewable electricity inputs to the same value of x%. 

The underlying calculations of what constitutes renewable electricity generation are described in Section 9.1. The formulation of the renewable energy target constraints can be found in Appendix C. 

## _**9.3.2 Emissions Reductions Targets**_ 

Users can opt to set an emissions reductions target that applies to the site’s optimized CO2e emissions relative to BAU emissions. REopt identifies the least-cost technology mix, sizing, and dispatch to meet this target. This input should only be used if users select or upload _average_ emissions rates for grid-purchased electricity and are seeking to reduce their emissions footprint (as calculated with average emissions) by a given percentage. If users utilize the default marginal grid emissions rates, then the percent reduction calculation will not be methodologically accurate, as it will utilize marginal emissions rates to estimate total BAU emissions (whereas these rates should only be used to estimate changes in emissions). 

This target is applied relative to the total (analysis period) CO2e emissions in the BAU case. If a user assumes some future “greening of the grid” that reduces grid emissions, this greening of the grid is included in the BAU emissions calculations and is not counted towards emissions reductions calculated by REopt. Thus, REopt’s emissions reduction percentage only “counts” emissions reductions facilitated by DERs. 

As with the renewable electricity target, users can enter a minimum and/or maximum percentage emissions reduction target. If a user wants to reduce the site’s total emissions by “at least” x% relative to the BAU emissions, they can set a minimum emissions reduction target to x%. Alternatively, if the user wants to reduce the site’s total emissions by “exactly” x%, they can set the minimum and maximum emissions reduction target inputs to the same value of x%. 

## _**9.3.3 Include climate and/or health emissions costs in the objective function**_ 

In a typical REopt analysis, climate and health cost savings over the analysis period are reported but are _not_ included in the reported net present value or life cycle cost of energy. However, under the “Clean Energy” accordion, users can opt to include total (analysis period) climate costs and/or total health costs in the life cycle cost objective function of the REopt tool. 

Selecting this option indicates that emissions costs will actually be in incurred by the off-taker. Therefore, if “include climate (or health) emissions in objective function” is selected, REopt’s objective function will include these emissions costs alongside all other cost considerations (e.g., capital expenses, utility bill costs) to determine the optimal system sizing and dispatch strategy. 

Including emissions costs will likely impact system sizes and cost-optimal dispatch strategies, as dispatchable technologies will work to avoid grid purchases during times when emissions rates 

58 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

are relatively high. When reviewing results, users should note that the project lifecycle cost and net present value will include climate and/or health costs if “include climate (and/or health) emissions in objective function” is selected. 

## **10 Photovoltaics** 

The REopt web tool uses NREL’s PVWatts application to determine the electricity production of installed PV systems. The amount of electricity produced by the PV array at each time step is proportional to the hourly capacity factor at the site. Because the production of PV arrays tends to decline over their lifespan, and the model only optimizes over one year, the REopt web tool uses an average annual production profile based on an assumed 0.5% per-year degradation rate over the analysis period. We assume the inverter is replaced once during the system lifetime, and replacement cost is amortized into annual O&M costs. 

The size of the PV installation is limited by available roof or land space. The default assumption allows one MW-DC of PV to be installed for every six acres of space available, and 10 DC watts per square foot of roof space. Hourly solar radiation data comes primarily from the National Solar Radiation Database, which uses a physics-based modeling approach to provide solar radiation data for the United States in 4-km gridded segments using geostationary satellites. Data for international sites is also available for a growing number of countries as described at https://nsrdb.nrel.gov/about/international-data.html. 

Refer to the PVWatts technical reference manual for further modeling assumptions and descriptions (Dobos 2014). 

## **10.1  PV Costs** 

PV system costs include capital cost and O&M cost. The capital cost represents the fully burdened installed cost, including both equipment and labor. O&M includes asset cleaning, administration costs, and replacing broken components. It also includes the cost of inverter replacement. Incentives can be applied to reduce the cost; these are described in Section 4.3, Economic Incentives. 

The default PV capital cost and O&M cost are based on the calculated “size class”. There are five size classes, listed in Table 9. The size classes are determined based on an estimated PV size which is the minimum of 1) the size that can fit in the user-specified roof and land area, 2) the size that is estimated to produce 50% of the site’s annual electric consumption, and 3) the userinput maximum size. The size class is chosen for which the calculated size is within the specified size range. The user may also override this logic and choose the size class which will then decouple the logic described above. A warning will be displayed on the results page if the REopt-optimized PV size is outside of the determined or chosen size class size range, where it is then advised to re-run with the appropriate size class. 

59 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 9. PV size classes and the capital cost and O&M cost default values for each, based on roofmounted PV systems except for the Utility size class. See below for cost increases for groundmounted PV for Residential through Large Commercial size classes.** 

|||||
|---|---|---|---|
|**Size class name (DC size range)**|**Capital cost**|**O&M cost**|**Reference**|
||<br>**($/kW-DC)**|**($/kW/yr)**||
|||||
|||||
|Residential (up to 11 kW)||||
||$2,783|$32|ATB Residential|
|||||
|Small Commercial (12 – 100 kW)|$2,232|$26|Scaled ATB1|
|||||
|Large Commercial (101 – 2,000 kW)|$1,920|$20|ATB Commercial|
|||||
|Industrial (2,001 – 10,000 kW)|$1,661|$20|Scaled ATB1|
|||||
|Utility (10,001 kW and larger)2|$1,239|$17|ATB Utility|
|||||
|1(Ramasamy, Feldman, Margolis, & Desai, 2021)||||
|2Utility PV cost assumes ground-mounted panels with single-axis tracking||||



The published values from the 2024 NREL ATB are based on 2022 historical data (the base year for most technologies) and are inflated to 2024 inflation-adjusted annual average U.S. dollars, using the consumer price index ratio from the U.S. Bureau of Labor Statistics: https://www.bls.gov/cpi/. 

The small commercial and industrial size classes were created to bridge a gap in the reference sizes from ATB-published data where there are important “in-between” cost differences to capture. Cost data points for these two “in-between” size classes as well as the same ATBpublished sizes are included in the reference (Ramasamy, Feldman, Margolis, & Desai, 2021) which serves as the basis for ATB cost estimating methodology, so the nearest-size ATBpublished costs were scaled based on the appropriate scaling factor. 

Additionally, the default ground-mounted PV has a capital cost increase of 30% compared to roof-mounted PV for the residential and small-commercial size classes, and a capital cost increase of 15% for the large commercial size class based on approximations from literature (Ramasamy, Feldman, Margolis, & Desai, 2021). Industrial and utility size classes are assumed to have the same cost for roof- and ground-mounted systems. The default capital cost that is displayed will update to reflect the cost for the selected PV array mounting type. 

## **10.2  PV System Characteristics** 

## _**10.2.1 PV Size**_ 

The REopt web tool identifies the system size, in kW-DC, that minimizes the life cycle cost of energy at the site. By default, there is no lower or upper limit on the size. If desired, the user can bound the range of sizes considered with a minimum and a maximum size.  The minimum new PV size forces a new PV system of at least this size to appear at the site. If there is not enough land available, or if the interconnection limit will not accommodate the system size, the problem will be infeasible. 

60 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

The maximum new PV size limits the new PV system (not including any existing PV system) to no greater than the specified maximum. 

To remove the option of a new PV system from consideration in the analysis, set the maximum size to zero. If a specific-sized system is desired, enter that size as both the minimum size and the maximum size. 

The minimum and maximum new PV size limits for technologies are assumed to be in addition to any existing PV; for example, there could be a 10-kW existing PV system, and if the user inputs a maximum new PV size of 2 kW, then the upper limit that will be allowed by the REopt web tool is 10+2 =12 kW. 

## _**10.2.2 Existing PV**_ 

If the site has an existing PV system, this can be modeled in the REopt web tool by entering its size in kW. The existing PV system will be factored into business-as-usual O&M cost calculations and net metering credits and limits. No incentives will be included for the existing PV system. If the user has chosen to optimize for energy resilience, the energy from this existing PV system will be factored into the energy resilience optimization. 

When entering existing PV, the user selects how the typical energy load profile will be characterized with the addition of the existing PV system load. The default selection is Net load profile, which is the gross load minus the existing PV generation. The other option is to consider the typical energy load profile that has been entered as the gross load. 

## _**10.2.3 Module Type**_ 

The module type describes the PV modules in the array. If you do not have information about the modules in the system, use the default Standard module type. Otherwise, you can use the nominal module efficiency, cell material, and temperature coefficient from the module data sheet to choose the module type. 

**Table 9. Module Types** 

||**Approximate**||**Temperature Coefficient**|
|---|---|---|---|
|**Type**||**Module Cover**||
||**Efficiency**||**of Power**|
|||||
|Standard (crystalline||Glass with anti-||
||<br>19%||-0.37 %/°C|
|<br>silicon)||reflective coating||
|||||
|Premium (crystalline||Glass with anti-||
||<br>21%||-0.35 %/°C|
|<br>silicon)||reflective coating||
|||||
|||Glass with anti-||
|Thin Film|18%||-0.32 %/°C|
|||reflective coating||
|||||



PVWatts uses a basic set of equations to represent the module’s physical properties and performance. The module type determines how PVWatts calculates the angle-of-incidence correction factor as sunlight passes through the module cover to the photovoltaic cell, and the cell’s operating temperature. See the PVWatts Technical Reference for details (Dobos 2014). 

61 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## _10.2.3.1 Array Type_ 

The array type describes whether the PV modules in the array are fixed or whether they move to track the movement of the sun across the sky with one or two axes of rotation. Options include Rooftop, Fixed; Ground Mount, Fixed (open rack); and Ground Mount, 1-Axis Tracking. The default value is a rooftop, fixed system. If 0 is entered in the roofspace available input field, the default changes to ground mount, fixed. 

For systems with fixed arrays, you can choose between an open rack or a roof mount option. The open rack option is appropriate for ground-mounted systems. It assumes that air flows freely around the array, helping to cool the modules and reduce cell operating temperatures. (The array’s output increases as the cell temperature decreases at a given incident solar irradiance.) The roof mount option is typical of residential installations where modules are attached to the roof surface with standoffs that provide limited air flow between the module back and roof surface (typically between two and six inches). 

For the open rack option, PVWatts assumes an installed nominal operating temperature of 45 degrees Celsius. For roof mount systems, the installed nominal operating temperature is 50°C, which corresponds roughly to a three- or four-inch standoff height. See the Technical Reference for details (Dobos 2014). 

## _10.2.3.2 Array Azimuth_ 

For a fixed array, the azimuth angle is the angle clockwise from true north describing the direction that the array faces. An azimuth angle of 180° is for a south-facing array, and an azimuth angle of zero degrees is for a north-facing array. For an array with one-axis tracking, the azimuth angle is the angle clockwise from true north of the axis of rotation. 

The default value is an azimuth angle of 180° (south-facing) for locations in the northern hemisphere. This value typically maximizes electricity production over the year, although local weather patterns may cause the optimal azimuth angle to be slightly more or less than the default values. For the northern hemisphere, increasing the azimuth angle favors afternoon energy production, and decreasing the azimuth angle favors morning energy production. 

**Table 10. Azimuth Angles for Different Compass Headings** 

|||
|---|---|
|**Heading**|**Azimuth Angle**|
|||
|N|0°|
|NE|45°|
|E|90°|
|SE|135°|
|S|180°|
|SW|225°|
|W|270°|
|NW|315°|



The maximum number entered must be less than or equal to 360—an error will display if a higher value is entered. 

62 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## _10.2.3.3 Array Tilt_ 

The tilt angle is the angle from horizontal of the PV modules in the array. For a fixed array, the tilt angle is the angle from horizontal of the array where 0° = horizontal, and 90° = vertical. For arrays with one-axis tracking, the tilt angle is the angle from horizontal of the tracking axis. 

By default, the REopt webtool sets both rooftop and ground-mounted fixed arrays default to a tilt angle of 20 degrees, consistent with PVWatts' defaults. One-axis tracking systems maintain a tilt angle of 0 degrees. Lower tilt angles are generally preferred during summer to maximize energy production when solar irradiance is high. Conversely, higher tilt angles are advantageous in winter to optimize lower solar irradiance. When selecting a tilt angle, it's important to consider the balance between maximizing energy yield and minimizing costs and risks associated with the installation hardware, especially in terms of wind exposure and debris accumulation. 

For a PV array on a building’s roof, you may want to choose a tilt angle equal to the roof pitch. Use Table 11 to convert roof pitch in ratio of rise (vertical) over run (horizontal) to tilt angle. 

**Table 11. PV Array Tilt Angle for Different Roof Pitches** 

|**Roof Pitch**||
|---|---|
||**Tilt Angle**|
|**(Rise/Run)**||
|||
|4/12|18.4°|
|5/12|22.6°|
|6/12|26.6°|
|7/12|30.3°|
|8/12|33.7°|
|9/12|36.9°|
|10/12|39.8°|
|11/12|42.5°|
|12/12|45°|



The maximum number entered must be less than or equal to 90—an error will display if a higher value is entered. 

## _10.2.3.4 Direct Current to Alternating Current Size Ratio_ 

The direct current (DC) to alternating current (AC) size ratio is the ratio of the inverter’s AC rated size to the array’s DC rated size. Increasing the ratio increases the system’s output over the year, but also increases the array’s cost. The default value is 1.20, which means that a 4-kW system size would be for an array with a 4 DC kW nameplate size at standard test conditions and an inverter with a 4 DC kW/1.2 = 3.33 AC kW nameplate size. 

For a system with a high DC to AC size ratio, during times when the array’s DC power output exceeds the inverter’s rated DC input size, the inverter limits the array’s power output by increasing the DC operating voltage, which moves the array’s operating point down its currentvoltage curve. PVWatts models this effect by limiting the inverter’s power output to its rated AC size. 

63 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

The default value of 1.20 is reasonable for most systems. A typical range is 1.10 to 1.25, although some large-scale systems have ratios of as high as 1.50. The optimal value depends on the system’s location, array orientation, and module cost. The maximum number entered must be less than or equal to 2—an error will display if a higher value is entered. 

## _10.2.3.5 System Losses_ 

The system losses account for performance losses you would expect in a real system that are not explicitly calculated by the PVWatts model equations. The default value for the system losses of 14% is based on the categories in the table below, and calculated as follows: 

100% * (1 - (1 - 0.02) * (1 - 0.03) * (1 - 0.02) * (1 - 0.02) * (1 - 0.005) * (1 - 0.015) * (10.01) * (1 - 0.03)) = 14% 

The inverter’s DC-to-AC conversion efficiency is a separate, non-adjustable input with a value of 96%. Do not include inverter conversion losses in the system loss percentage. PVWatts calculates temperature-related losses as a function of the cell temperature, so you should not include a temperature loss factor in the system loss percentage. See the PVWatts Technical Reference for details (Dobos 2014). 

**Table 12. Default Values for the System Loss Categories** 

|**Category**|**Default Value (%)**|
|---|---|
|Soiling|2|
|Shading|3|
|Snow|0|
|Mismatch|2|
|Wiring|2|
|Connections|0.5|
|Light-Induced Degradation|<br>1.5|
|Nameplate Rating|1|
|Age|0|
|Availability|3|



The maximum number entered must be less than or equal to 99—an error will display if a higher value is entered. 

## _**10.2.4 Custom PV Generation Profile**_ 

By default, the PV production values for new PV modeled, as well as any existing PV system that is included in the evaluation, are sourced from PVWatts®. Custom PV production factors can be used in place of these profiles by uploading a user-defined PV generation profile. The file must be normalized to units of kW-AC/kW-DC nameplate, representing the AC power (kW) output per 1 kW-DC of system capacity in each time step. The file must be one year (January through December) of hourly, 30-minute, or 15-minute PV generation data. 

64 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## _**10.2.5 PV Resource Data and Station Search Radius**_ 

Where available, REopt utilizes gridded TMY data from the NSRDB dataset, which covers locations within the U.S. as well as a growing number of international locations. If NSRDB data are not available for a site, then data from stations within the TMY3 or PVWatts International datasets will be utilized (see the PVWatts API documentation for more information on these datasets). 

The PV station search radius input allows the user to constrain the solar resource data sites that PVWatts will consider to those within a specified radius from the analysis site. If you choose a PV Stations Search Radius that does not include any data stations in the NSRDB, TMY3, or International datasets, then the evaluation will be stopped immediately and you will get a message that you need to increase the radius. 

In addition to this optional search radius input, the REopt web tool gives the user a warning message if the closest solar data site in PVWatts is more than 200 miles away. This warning message will ask for your acknowledgement before you can view your results. You can search for an alternative site location that is closer to NREL's NSRDB, TMY3, or international datasets at NSRDB Data Viewer or PVWatts web tool. 

## **11 Battery Storage** 

Battery energy storage is modeled as a “reservoir” in the REopt web tool so that energy produced during one time step can be consumed during another. The REopt web tool does not explicitly model battery chemistries, but rather includes parameters for cost, efficiency, and SOC that can be adjusted to reflect different chemistries. The default values are representative of lithium-ion batteries. The model selects and sizes both the capacity of the battery in kWh and the power delivery in kW-AC. The battery power (kW-AC) and capacity (kWh) are independently optimized for economic performance (and resiliency, if resiliency requirements are specified)—a power-to-energy ratio is not predefined. By default, any technology can charge the energy storage device, but charging can also be limited to specific technologies. 

Energy storage technologies are modeled to capture revenue from multiple value streams: performing energy arbitrage, time-shifting excess renewable energy production, and reducing demand charges or "peak shaving.” The user can define the battery energy storage model characteristics including minimum SOC, initial SOC, efficiencies, minimum size, maximum size, capital cost, and replacement cost. The minimum SOC applies for financial optimization while grid tied. During a grid outage, the battery SOC is allowed to drop to zero. The user can also decide whether or not the grid can be used to charge the battery. Battery cycling degradation is not included in the model; rather, we assume the battery will be replaced once during the analysis period (in year ten by default) based on calendar degradation, and include amortized replacement costs in the model. These inputs are described in more detail below. 

## **11.1 Battery Cost** 

## _**11.1.1 Capital Cost**_ 

Battery cost is defined by three parameters: constant cost ($), energy capacity cost ($/kWh) and power capacity cost ($/kW). These costs are additive. 

65 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

The constant cost is the baseline cost which is not dependent on the size (energy or power capacity) of the battery. This constant term captures economy-of-scale of battery storage systems where this constant cost will be a larger portion of the total cost for smaller systems and a smaller portion of the total cost for larger systems when adding the energy and power capacity cost terms. 

Energy capacity cost is the cost of the energy components of the battery system (e.g., battery pack). Power capacity cost is the cost of the power components and interconnection of the battery system (e.g., inverter and balance of system). The amount of energy that a battery can store is determined by its capacity (kWh) while the rate at which it charges or discharges is determined by its power rating (kW). While PV system cost is typically estimated based on power rating (kW) alone, battery costs are estimated based on both capacity (kWh) and power (kW). 

The power components of the system (e.g., inverter, balance of system) are captured by the power metric of $/kW and the energy components of the system (e.g., battery) are captured by the energy metric of $/kWh. This allows the capacity (kWh) and power (kW) rating of the battery to be optimized individually for maximum economic performance based on the load, rate tariff, and resiliency requirements of the site. Some systems are optimized to deliver high power capacity (kW), while others are optimized for longer discharges through more energy capacity (kWh). 

For example, assume the constant cost is $5,000, the unit cost of power components is $1,000/kW, and the unit cost of energy components is $500/kWh. Consider a battery with 5 kW of power capacity and 10 kWh of energy capacity (5 kW/10 kWh). The total cost of the battery would be: 

$5,000 + (5 kW * $1,000/kW) + (10 kWh * $500/kWh) = $15,000 

The published values from the referenced 2024 ATB version are inflated from the 2022 reference year of the provided data to the 2024 inflation-adjusted annual average U.S. dollars, using the consumer price index ratio from the U.S. Bureau of Labor Statistics: https://www.bls.gov/cpi/. 

## _**11.1.2 Operating and Maintenance (O&M) Cost**_ 

The operating and maintenance (O&M) cost represents the expenses to maintain and replace components of the battery storage system. The O&M cost methodology is to estimate yearly costs a percentage of the upfront capital cost. This cost includes upkeep and replacement of power-related equipment as well as battery pack augmentation to maintain the energy capacity of the battery. 

## _**11.1.3 Replacement Cost**_ 

Replacement costs are similarly defined by energy capacity and power capacity costs, as well as replacement year. They are the expected cost, in today’s dollars, of replacing the energy components of the battery system (e.g., battery pack) and power components of the battery system (e.g., inverter, balance of systems), respectively, during the project life cycle. Replacement year is the year in which the energy or power components of the battery system are replaced during the project life cycle; the default is Year 10. 

66 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## 11.1.4 _**Allowing Grid to Charge Battery**_ 

The REopt web tool allows the user to specify whether the utility grid can be used to charge the battery. If this input is set to no, the grid cannot charge the battery. Only the renewable energy system will charge the battery. If it is set to yes, either the grid or the renewable energy system can charge the battery. The default is set to yes in order to allow evaluation of batteries that are not connected to a renewable energy system. 

Whether or not the grid charges the battery impacts the owner’s ability to take advantage of the federal ITC and MACRS. The 2020 federal 26% ITC is generally understood to be available to batteries charged 100% by eligible renewable energy technologies, including solar and wind, when they are installed as part of a renewable energy system. Batteries charged by a renewable energy system 75%–99% of the time are eligible for that portion of the ITC. For example, a system charged by renewable energy 80% of the time is eligible for the 26% ITC multiplied by 80%, which equals a 20.8% ITC instead of 26%. The user must calculate and input the appropriate total incentive percentage. 

Without a renewable energy system installed, battery systems are eligible for the seven-year MACRS depreciation schedule—an equivalent reduction in capital cost of about 20% (assuming a 26% federal tax rate and an 8% discount rate). The same benefit applies to battery systems installed along with a renewable energy system if the battery is charged by the renewable energy system less than 75% of the time. If the battery system is charged by the renewable energy system more than 75% of the time on an annual basis, the battery should qualify for the five-year MACRS schedule, equal to about a 21% reduction in capital costs. 

When claiming the ITC, the MACRS depreciation basis is reduced by half of the value of the ITC. Note new tax laws concerning battery systems are pending. Refer to the Internal Revenue Service for the latest regulations. 

## **11.2  Battery Characteristics** 

## _**11.2.1 Battery Size**_ 

The REopt web tool identifies the system size that minimizes the life cycle cost of energy at the site. By default, there is no lower or upper limit on size. If desired, the user can bound the range of sizes considered with a minimum and maximum size. The minimum energy capacity size forces a battery energy capacity of at least this size to appear at a site. The maximum energy capacity size limits the battery energy capacity to no greater than the specified maximum. 

To remove a technology from consideration in the analysis, set the maximum size to zero. If a specific sized system is desired, enter that size as both the minimum size and the maximum size. 

An existing battery size cannot be specified. 

67 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## _**11.2.2 Battery Efficiency**_ 

The efficiency of the battery is defined by three components: 

- Rectifier efficiency: The rectifier’s nominal rated AC-to-DC conversion efficiency, defined as the rectifier’s rated DC power output divided by its rated AC power output. The default value is 96%. 

- Round trip efficiency: This is the ratio of the DC power put into a battery to the DC power retrieved from the same battery. The default value is 97.5%. 

- Inverter efficiency: The inverter’s nominal rated DC-to-AC conversion efficiency, defined as the inverter’s rated AC power output divided by its rated DC power output. The default value is 96%. 

The product of these three efficiencies provides the total AC-AC round trip efficiency, which is the ratio of the AC power put into a battery to the AC power retrieved from the same battery. The default value is 89.9%. Note that the round-trip efficiency only accounts for DC power in and out of the battery, while the total AC-AC round trip efficiency also accounts for the need to convert AC power to DC in order to charge the battery, and DC power to AC in order to discharge the battery. 

## _**11.2.3 Battery State of Charge**_ 

The user can enter a minimum SOC to define the lowest desired level of charge of the battery. The default is 20%. 

The user can also enter the initial SOC of the battery at the beginning of the analysis period. The default is 50%. 

## **12 Wind Turbine** 

The REopt web tool models wind turbines of four different sizes: residential (<20 kW), commercial (21–100 kW), midsize (101–999 kW), and large (≥1000 kW). Turbine sizes and power curves for each size class are shown below. 

The REopt web tool uses the site location and the wind size class selected to access wind resource data from the Wind Integration National Dataset (WIND) Toolkit. The WIND Toolkit includes meteorological conditions and turbine power for more than 126,000 sites in the continental United States for the years 2007–2013.  The REopt web tool uses 2012 data because it is close to the WIND Toolkit overall average wind generation across 2007–2013. 

The WIND Toolkit provides wind speed, air pressure, air temperature, and wind direction at an hourly resolution. These values returned by the WIND Toolkit are processed by the System Advisor Model (SAM) to produce the wind energy production curves used for the optimization.[18] Refer to the WIND Toolkit technical reference manual for further modeling assumptions and descriptions (Draxl et al 2015). 

> 18 https://sam.nrel.gov/ 

68 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

Wind projects exceeding 1.5 MW are constrained by land availability when this information is provided, assuming a power density of 30 acres per MW. 

## **12.1  Wind Cost** 

Wind turbine costs include capital cost and O&M cost. The capital cost represents the fully burdened cost of installed wind system in dollars per kilowatt. See “The REopt Web Tool Default Values, Typical Ranges, and Sources” Section for current default wind capital and O&M costs. If a custom cost is entered, it will be used instead of the default cost. 

## **12.2 Wind characteristics** 

## _**12.2.1 Size Class**_ 

The wind size class selected will determine the potential wind energy production for the site location. The size class should be selected based on site load and wind resource. The size class label refers only to the turbine size, as determined by the rated capacity (or system size), and not the end-use sector. For example, residential sized turbines are often used in commercial applications. The REopt web tool models wind turbines of four different sizes: 

- Large (>=1000 kW-AC) 

- Midsize (101–999 kW-AC) 

- Commercial (21–100 kW-AC) 

- Residential (0–20 kW-AC). 

Table 14 provides the representative turbine sizes used by the REopt web tool for each wind size class. For the optimization, a single turbine installation is generally assumed. 

**Table 14. Wind Size Class Representative Sizes** 

|**Size Class**|**System Size**<br>**(kW-AC)**|**Hub Height**<br>**(m)**|**Rotor**<br>**Radius (m)**|
|---|---|---|---|
|Residential|2.5|20|1.85|
|Commercial|100|40|13.8|
|Midsize|250|50|21.9|
|Large|2,000|80|55|



Source: Lantz et al. (2016) 

The representative power curves are based on Lantz et al. (2016) but assume near-future turbine technology advancements. 

69 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 15. Representative Power Curves** 

||**Residential(2.5kW)  **|**Commercial(100kW)  **|**Midsize(250kW) **|**Large (2000kW)**|
|---|---|---|---|---|
|**Wind Speed(m/s)**|**kW**|**kW**|**kW**|**kW**|
|**2**|0|0|0|0|
|**3**|0.070542773|3.50595|8.764875|70.119|
|**4**|0.1672125|8.3104|20.776|166.208|
|**5**|0.326586914|16.23125|40.578125|324.625|
|**6**|0.564342188|28.0476|70.119|560.952|
|**7**|0.896154492|44.53855|111.346375|890.771|
|**8**|1.3377|66.4832|166.208|1329.664|
|**9**|1.904654883|94.66065|236.651625|1893.213|
|**10**|2.5|100|250|2000|



Source: Lantz et al. (2016) 

If no wind size class is selected, the default wind class value of ‘commercial’ will be used. 

The selection of a size class does not limit the minimum and maximum sizes considered in the optimization to that range; the optimization may recommend a wind capacity that is outside of the range of sizes defined by the selected size class. In this case, the production and cost data used in the model may not apply to the system size recommended. For example, if the user selects the large size class (>1000 kW) but gets a recommendation for a 50-kW wind turbine, the recommended 50-kW turbine was incorrectly costed at the cheaper large-class cost and its production estimate used the superior wind resource of a taller large-class turbine. 

If the results recommend a wind turbine in a different size class than that selected, the results will be flagged and the user can iterate on the analysis inputs, updating the size class and rerunning the optimization. 

## _**12.2.2 Wind Size**_ 

The REopt web tool identifies the system size that minimizes the life cycle cost of energy at the site. By default, there is no lower or upper limit on size. If desired, the user can bound the range of sizes considered with a minimum and maximum size. If there is not enough land available, or if the interconnection limit will not accommodate the system size, the problem will be infeasible. 

To remove a technology from consideration in the analysis, set the maximum size to zero. If a specific sized system is desired, enter that size as both the minimum size and the maximum size. 

## **13 Emergency Generator & Offgrid Generator** 

The same technology module in REopt is used to model emergency generator for grid-tied facilities and to model a conventional generation plant for remote off-grid systems. The generator model is not specific to any generator type however the default performance and costs represent a reciprocating engine generator type. Fuel is assumed to be liquid and therefore fuel costs and heating values are entered on a per gallon basis. The default fuel type is assumed to be diesel as represented by the default higher heating value of fuel in the advanced settings. Fuel consumption is modeled using a linear fuel curve as described for the CHP generator in Section 

70 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

14.2, CHP Fuel Consumption, and is limited to the fuel reserve entered by the user. Off-grid scenarios assume unlimited fuel supply so there is not input for available fuel when running this scenario. Generator costs include the fully burdened installed cost, non-fuel O&M cost, and fuel cost. 

## **13.1 Emergency Generator** 

For resilience analyses (for grid-tied applications), the generator is considered a conventional backup emergency generator. The default fuel reserve is assumed to be unlimited (modeled in REopt as 1 million gallons). If the site has limited fuel reserve storage capacity, the user should edit the default value to the site’s fuel storage constraint. Fuel availability represents the amount of fuel available on-site on an annual basis for new and existing generators. Fuel resupply is not modeled; the generator can no longer run after available fuel is expended. 

In the web tool, the default assumption is that the emergency generator only operates during grid outages and can only be modeled when the “Resilience” goal is checked. The user can elect to allow the generator to operate in grid-parallel mode, however, this may not be allowed in many jurisdictions depending on the fuel type, pollution controls, regional air-quality, etc. The user may also find that allowing this option does not change the results. This could be because REopt does not find value in operating the generator, due to the cost of fuel, to be more cost-effective than other options. 

For resilience scenarios, the emergency generator is assumed to be able to operate at any partial loading (0%-100%) during a grid outage. The user can change this default assumption, however doing so might impact the mix and size of all DER or may result in infeasible solutions. 

If the site has an existing generator, this can be modeled in the REopt web tool by entering its size in kW. O&M costs for an existing generator are included in both the business-as-usual and optimum solution. 

## **13.2 Off-grid Generator** 

For off-grid scenarios, a minimum turndown constraint can be included, meaning the generator can operate at partial loading down to a given fraction of its nameplate capacity; any lower and it must shut off (see Section 20 for more details). Fuel supply is not considered constrained for generator in off-grid analyses; therefore no input exists for fuel availability in this case. 

## **13.3  Generator Costs** 

Generator costs include the installed cost, O&M cost, and fuel cost. The capital cost represents the fully burdened installed cost, including both equipment and labor. O&M includes fixed regular O&M based on calendar intervals including testing, stored fuel maintenance, and service contracts. Variable O&M includes non-fuel O&M costs which vary with the amount of electricity produced. Variable O&M may include filters and oil changes, and other maintenance requirements based on engine run-hours. For emergency generators, default cost assumptions and sources are included in Section 22, Table 47. For off-grid generators, default cost assumptions are the same as grid paralleling emergency generators. The user should review and adjust these costs appropriately considering the requirements and remoteness of the location. 

71 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

Fuel cost is input separately in units of dollars per gallon. Fuel availability represents the amount of fuel available on-site on an annual basis for new and existing generators. Fuel resupply is not modeled; the generator can no longer run after available fuel is expended. 

## **13.4  Generator Size** 

The REopt web tool identifies the system size in kW-AC that minimizes the life cycle cost of energy while meeting the critical load during the specified grid outage at the site (recommended sizing differs for off-grid microgrids; see Section 20 for more details). By default, there is no lower or upper limit on the size. If desired, the user can bound the range of sizes considered with a minimum and a maximum size. The minimum new generator size forces a new generator system of at least this size to appear at the site. The maximum new generator size limits the new generator system (not including any existing generator) to no greater than the specified maximum. 

To remove the option of a new generator system from consideration in the analysis, set the maximum size to zero. If a specific sized system is desired, enter that size as both the minimum size and the maximum size. 

The minimum and maximum new generator size limits are assumed to be in addition to any existing generator; for example, there could be a 10-kW existing generator, and if the user inputs a maximum new generator size of 2 kw; then the upper limit that will be allowed by the REopt web tool is 10+2 =12 kW. 

## **14 Combined Heat and Power** 

This section describes modeling and assumptions for the CHP prime mover and heat recovery system. If the user is considering CHP, assumptions include the following: 

1. There is a central heating plant and heat distribution system that the CHP system can tie into. The REopt web tool does not size nor cost a conventional heating plant and heating distribution piping. 

2. There is an existing fuel supply and the fuel is costed on a per-unit-of-consumption basis. There are no embedded cost assumptions for adding fuel supply infrastructure (pipeline, storage tanks, fuel pretreatments) or increasing the capacity of the fuel supply infrastructure. 

3. The CHP system can operate parallel to the serving utility, providing some, all, or none of the electrical demand in any hour. The exception to this is during a resilience analysis when a power outage is simulated. Then, the critical electrical load identified by the user must be met by the CHP unit and any other sources considered for inclusion, without the utility. 

4. The CHP system can serve some, all, or none of the heating load in any hour. There is no requirement that the CHP system serve all of the heating load. 

5. If there is excess available heat from the CHP plant, that heat can be dumped to the atmosphere either through a generator exhaust bypass configuration or utilization of a heat exchanger unit. 

72 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

6. The facility has space to install any selected system. Costs for construction of a building to house a new CHP system are not included beyond basic container costs that may be included in the total installed costs assumptions. 

7. For a steam turbine CHP evaluation, the existing boiler is assumed to produce steam at the pressure and temperature required for the applicable steam turbine, and the expanded low pressure steam is at an appropriate pressure and temperature for the end-use process heat load. 

Default performance parameters are available for three different natural gas-fueled CHP prime mover types: reciprocating engine, microturbine, combustion turbine, and fuel cell. Defaults are described in Section 14.8,  Topping Cycle Default CHP Cost & Performance Parameters by Prime Mover Type and Size Class. 

Each of these CHP systems has the same set of inputs which characterize installed system cost, O&M cost, electric production performance, heat recovery performance, and other constraints. The user may use defaults provided and shown in the user interface or adjust them to reflect details of the system performance and cost under consideration. 

## **14.1 CHP Prime Mover Overview** 

The REopt web tool considers CHP system sizes in the range of 1 to 20 MW (20,000 kW). The CHP performance model is a generalized description of the relations of CHP outputs of power and heat to the input of fuel. These relations are linearized and capture fuel consumption and available recoverable heat as a function of the CHP prime mover’s electric loading. Default CHP performance parameters are included within the model for the following prime movers: 

1. Reciprocating engine 

2. Combustion turbine 

3. Microturbine 

4. Fuel cell 

5. Steam turbine 

All prime movers are topping cycles except the steam turbine which is a bottoming cycle. For the topping cycles, fuel is consumed in the generation of electricity while excess heat from combustion (or chemical reaction in the fuel cell) can be captured to served site thermal loads. 

The user can use the default parameters provided or modify them to represent the performance of a system of their own specification, selection, or design. 

Figure 4 illustrates the energy flows for the topping cycle CHP units. Fuel is converted to electricity and recoverable usable heat. 

73 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [468 x 162] intentionally omitted <==**

**Figure 4. Topping cycle CHP diagram to illustrate the energy flows** 

This recovered heat can be in the form of hot water or steam. In the REopt web tool, thermal loads are assumed to be either hot water or steam. Systems that serve both hot water and steam loads are not modeled. 

Figure 5 illustrates the energy flows for the bottoming cycle back pressure steam turbine CHP. Fuel is burned in the existing steam boiler to produce steam, and the steam turbine expands the steam from high pressure to a lower pressure to generate electricity. The recovered useful heat for the end-use application is extracted by condensing the low pressure steam to a saturated liquid condition. 

**==> picture [485 x 166] intentionally omitted <==**

**Figure 5. Bottoming cycle CHP: back pressure steam turbine** 

## **14.2  CHP Fuel Consumption** 

CHP fuel options include natural gas, propane, diesel, and biogas. The user-selected fuel type impacts emissions accounting. 

74 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

The model for topping cycle prime movers uses a linear equation for fuel burn rate as a function of power generation. Figure 6 shows the relationship of fuel burn rate and fuel efficiency as a function of generator power output for a representative packaged CHP unit[19] selected from the DOE eCatalog for packaged CHP units (Lawrence Berkeley National Laboratory 2019). 

**==> picture [398 x 226] intentionally omitted <==**

**----- Start of picture text -----**<br>
12 40<br>35<br>10<br>30<br>8<br>25<br>6 20<br>Fuel = 9.0632E-03*Power + 8.0012E-01<br>15<br>4 R² = 9.9022E-01<br>10<br>2<br>5<br>0 0<br>0 200 400 600 800 1000 1200<br>Prime Mover Electrical Power Output (kW)<br>Fuel Input (MMBtu/hr) Net Electric Efficiency % (HHV)<br>Fuel Burn Rate (MMBtu/hr)<br>Electrical Efficiency (% HHV-basis)<br>**----- End of picture text -----**<br>


**Figure 6. Modeling of CHP fuel burn rate** 

The figure shows the electrical generation efficiency plotted on the secondary Y-axis versus load as provided. The nonlinear shape of electrical efficiency is typical, with zero efficiency at no load, poor efficiency at low load, and efficiency increasing to a maximum near or at full load. Electric efficiency is defined as: 

**==> picture [267 x 30] intentionally omitted <==**

**==> picture [57 x 12] intentionally omitted <==**

This variable efficiency is accurately modeled by use of the linear equation fit to the fuel burn rate (MMBtu/hr) versus load data also provided. As can be seen in the figure, the fuel burn rate can be accurately modeled this way (R-fit in this example is 99%). The fuel burn rate equation is: 

**==> picture [410 x 15] intentionally omitted <==**

The parameters _mf_ and _bf_ are calculated within the model using electrical efficiency of the prime mover at 100% load and 50% load since it is expected that these values are more readily available and less likely to be mis-entered than fuel burn rates. These efficiency points are converted to a normalized fuel burn rate (normalized based on rated electric capacity of the prime mover) to get a linear performance curve. 

> 19 https://chp.ecatalog.lbl.gov/package/10-SP4-ZC90001 

75 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

Electrical efficiency, and therefore the parameters _m_ and _b,_ will vary depending on the prime mover type and size of the prime mover with electrical efficiency generally increasing with increasing rated power. 

The REopt web tool includes default values for full load and half load electrical efficiency for various prime movers. These defaults are based on DOE fact sheets, review of eCatalog packaged CHP units, and technical specifications of various commercially available units. Performance is generally reported at some standard operating conditions, typically International Organization for Standardization (ISO) reference temperature and atmospheric pressure.[20] Users should consider how performance may differ for the site specified and modify defaults as appropriate with consultation of subject matter experts. 

## **14.3  CHP Available Heat Production** 

In a topping cycle, the balance of the fuel that is not converted to electricity becomes heat. In a system that generates only electricity, the heat is not useful. In a CHP system, some of this waste heat is recovered to become useful for serving facility heating loads. The level of waste heat recovery depends on both the prime mover type and design choices of the CHP system developer. In the REopt web tool the maximum available rate of heat recovery from the system is modeled similarly to fuel burn rate. Figure 7 shows the available heat from the same CHP system shown in Figure 6. The efficiency of heat recovery is shown on the secondary Y-axis and the available recoverable heat is shown on the primary axis. The equation for heat recovery efficiency is: 

**==> picture [426 x 31] intentionally omitted <==**

The available useful heat is modeled as: 

**==> picture [443 x 15] intentionally omitted <==**

The parameters _mh_ and _bh_ are calculated within the REopt web tool using heat recovery efficiency at 100% load and 50% load. These parameters are determined from CHP system specifications. 

> 20 ISO conditions are 59°F and 1 atmosphere for combustion turbines and 77°F and 1 atmosphere for reciprocating engines. 

76 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [387 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
5.0 50<br>4.5 45<br>4.0 40<br>3.5 35<br>3.0 30<br>2.5 25<br>Heat = 3.4332E-03*Power + 7.9535E-01<br>2.0 20<br>R² = 9.9998E-01<br>1.5 15<br>1.0 10<br>0.5 5<br>0.0 0<br>0 200 400 600 800 1000 1200<br>Prime Mover Electrical Power Output (kW)<br>Hot Water Capacity (MMBtu/hr) Thermal Efficiency % (HHV)<br>Available Useable Heat (MMBtu/hr)<br>Useable Heat Capture Effic. (% HHV-basis)<br>**----- End of picture text -----**<br>


**Figure 7. Modeling of CHP available useful heat** 

The heat recovery is described in terms of ‘maximum availability’ as we assume that if available heat is not needed, it can be rejected to atmosphere. That is, all, some, or none of the available heat can be used in any time step when the CHP unit is operating. 

The level of heat available depends on the load, prime mover type, each vendor’s heat recovery system design, and the process heat load conditions, e.g., hot water or steam. Default values for maximum available heat at full and half load are provided for the four prime mover types. 

A representative heat recovery system schematic is shown for the default reciprocating engine CHP unit in Figure 8. Figure 9 shows the assumed heat recovery configuration for a microturbine and Figure 10 shows a combustion turbine. Heat recovery configuration for a combustion turbine is similar to that shown for the microturbine although the default performance parameters included in the REopt web tool for the combustion turbine are based on a unit without a recuperator. 

77 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [360 x 323] intentionally omitted <==**

**Figure 8. Heat recovery configuration for reciprocating engine CHP** 

**==> picture [360 x 135] intentionally omitted <==**

**Figure 9. Heat recovery configuration for microturbine CHP** 

78 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [444 x 201] intentionally omitted <==**

**Figure 10. Heat recovery configuration for combustion turbine CHP** 

Default performance and costs are included in Section 14.8 Topping Cycle Default CHP Cost & Performance Parameters by Prime Mover Type & Size Class. 

As previously described, performance data is generally provided by CHP equipment providers at some specific conditions, e.g., standard ISO conditions. Additionally, vendor-reported heat recovery values are based on some specific process heat conditions, e.g., some fixed water temperatures, water flow rates, or steam pressures. 

## **14.4 Modeling Multiple Ganged Units** 

Designers will at times build a CHP system from multiple smaller prime movers that can then operate as a unit to provide greater maximum rated power and lower minimum turndown levels. In the REopt web tool, ganged prime movers are modeled as a single unit using the same approach and set of inputs described in Sections 14.2 and 14.3. An example of ganging multiple generators into a packaged unit would be packaging of three 200-kW microturbines to get a CHP system with 600 kW of rated power output. 

As an example, Figure 11 shows the fuel consumption and electrical efficiency of one 200-kW microturbine[21] and Figure 12 shows the fuel burn rate and electrical efficiency curves for three of the units shown in Figure 11 if operated together to provide 600 kW of power. 

> 21 Capstone Turbine Corporation, _Capstone C1000 Series Microturbine Systems Technical Reference_ (November 2011), publication 410072 Rev B. 

79 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [290 x 606] intentionally omitted <==**

**----- Start of picture text -----**<br>
2.5 35%<br>30%<br>2.0<br>25%<br>1.5<br>20%<br>15%<br>1.0<br>10%<br>0.5<br>5%<br>0.0 0%<br>0 50 100 150 200<br>Prime Mover Electrical Power Output<br>Actual Fuel (MMBtu/hr) Actual Eff.<br>8.0 35%<br>7.0<br>30%<br>6.0<br>25%<br>5.0<br>20%<br>4.0<br>15%<br>3.0<br>10%<br>2.0<br>5%<br>1.0<br>0.0 0%<br>0 100 200 300 400 500 600<br>Prime Mover Electrical Power Output<br>Actual Fuel (MMBtu/hr) Modeled Fuel (MMBtu/hr)<br>Actual Eff. Modeled Eff.<br>Fuel Burn Rate (MMBtu/hr)<br>Electrical Efficiency (% HHV-basis)<br>Fuel Burn Rate (MMBtu/hr)<br>Electrical Efficiency (% HHV-basis)<br>**----- End of picture text -----**<br>


**Figure 11. Fuel consumption and electrical efficiency versus load for one 200-kW microturbine** 

**Figure 12. Actual and REopt-modeled fuel and electrical efficiency curves for three 200-kW generators packaged as one unit** 

80 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

In Figure 12 the discontinuous efficiency curve and fuel burn rate curve are the actual expected performance values. Each discontinuity shows how the fuel consumption changes as each 200kW microturbine is turned on. In the REopt web tool, we simplify this behavior to allow the ganged packaged units to be modeled as one prime mover rather than, in this case, three separate generators. The continuous efficiency and fuel burn rates in Figure 12 show the simplification. In this example, the simplification introduces some error on fuel burn rates from -7% to +4% over the ganged unit’s power output range. The available heat recovery parameters are similarly approximated. 

## **14.5  Combustion Turbine Supplementary Duct Firing** 

It is common in combustion turbine CHP applications to add supplementary firing capability to the heat recovery steam generator (HRSG) when there is a steam load in excess of what can otherwise be produced from the hot exhaust gas. This involves installing burners near the exhaust flow inlet to the HRSG, and in operation the burners raise the temperature of the exhaust gas which allows additional steam production. Analyzing the cost-benefit of adding supplementary firing with combustion turbines can be done in REopt. 

The incremental thermal efficiency for supplementary firing is very high (about 92% HHV) because the burners are adding heat to pre-heated air. The steam production with supplementary firing can be up to three times the unfired steam production. If the combustion turbine prime mover is selected, there are three inputs for supplementary firing at the bottom of the CHP section, under advanced inputs, in the CHP System Characteristics section. Table 16 shows the available input parameters and default values for supplementary duct firing of combustion turbines. 

**Table 16. Supplementary firing input parameters and default values** 

|**Input parameter**|**Default value**|
|---|---|
|Supplementary firing maximum steam<br>production ratio|1.0 (none), but typical is 3.0<br>for supplementary firing|
|Supplementary firing thermal efficiency<br>(% HHV-basis)|92%|
|Supplementary firing capital cost22<br>($/kW)|150|



In the user interface, if the user changes the ‘Supplementary firing maximum steam production ratio’ to a value greater than the 1.0 default, the REopt web tool will consider whether the incremental cost for the supplementary firing is worth the investment in the optimization. 

> 22 This is a placeholder cost. The REopt web tool team does not have a citable reference for the incremental cost of supplementary firing of a heat recovery steam generator. 

81 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **14.6  CHP Auxiliary and Parasitic Loads** 

Parasitic and auxiliary loads include power required to run the CHP fuel pump/compressor, feedwater pumps, waste heat rejection fans, etc. For the default CHP units included in the REopt web tool, these loads are captured in the CHP net rated power output and fuel efficiency parameters. For user-entered CHP systems, the user is advised account for these auxiliary loads in the performance metrics entered. 

## **14.7  CHP Operations Constraints** 

As a best practice to avoid increased O&M requirements, there are low load regimes that prime movers should not be operated within for extended periods of time. For this reason, the REopt web tool includes a user-adjustable constraint called Minimum Electric Loading of Prime Mover. The value is entered as fraction of nameplate rated power. Minimum electric load fractions for default parameters by prime mover type are described in Section 14.8,  Topping Cycle Default CHP Cost & Performance Parameters by Prime Mover Type and Size Class. 

As a user option, CHP generated power can export to the grid in the model.[23] 

## **14.8  Topping Cycle Default CHP Cost & Performance Parameters by Prime Mover Type & Size Class** 

Default CHP performance and cost parameters are provided within the model for a number of topping cycle prime movers and size classes (size ranges) for each prime mover. The topping cycles are reciprocating engine, microturbine, combustion turbine, and fuel cell. Default costs and performance for the backpressure steam turbine (bottoming cycle) are provided in Section 14.9. Default costs and performance values assume one prime mover per CHP system. Default costs and performance parameters are shown in Table 18 through Table 21, one table for each prime mover type. The numbers in these tables are in the range of expected cost and performance based on the DOE CHP Fact Sheets (DOE Advanced Manufacturing Office 2017). The raw data used to calculate the average values for each size class are given in Appendix A. All default values are based on natural gas and are provided at near ISO rated conditions. 

## **Note: Default costs and performance for natural gas CHP are not modified for other user-selected fuels. It is incumbent upon the user to review and modify costs and performance as warranted.** 

The values in the tables for electrical and thermal efficiency, and the expected input for userspecified values, are based on fuel HHV. 

Note: The default values in the user interface set the electric efficiency and heating efficiency at 50% to 100% load values described in this section. The result is that the prime movers are modeled as constant efficiency units over their operating load range. This greatly simplifies the complexity of the optimization model and therefore reduces model runtimes. The user can adjust the 100% and 50% load efficiency values to model prime movers as variable efficiency units but should expect longer solve times and some 

> 23 In a scenario where there is no financial value for exported power, the REopt web tool may still export power to the grid in some time periods to avoid the CHP minimum loading constraint to generate and make use of the heat. 

82 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

runs that may time out before a solution is found. If modeling a variable efficiency prime mover, the user is encouraged to fix the size of the generator of interest by setting the maximum size equal to the minimum size. 

The total installed costs for CHP are entered as per-unit electric power capacity. The user can enter a single power-specific cost ($/kW) or enter two costs ($/kW) to generate a linear cost function. If a single input is entered, the model uses the same total installed cost ($/kW) for all CHP sizes. If both input fields are entered, total installed costs will be calculated by linear interpolation between the two cost limits. For linear interpolation, costs must be entered in ascending order (from left to right) and the total installed cost input must also have both input fields entered. CHP sizes less than the smaller size will have the first cost ($/kW), and CHP sizes larger than the larger size will have the second cost ($/kW). This linear interpolation of costs is not available for the other technology options. CHP costs have been updated to reflect costs in 2023. 

In the user interface, the user first selects the existing boiler thermal production type (which the CHP system will also supply)—either hot water or steam. Then the user inputs their electric and heating loads. Built-in logic uses the thermal production type and the average annual heating load to determine the default CHP prime mover type—either reciprocating engine or combustion turbine—and the size class of that prime mover. Table 17 gives the threshold of average boiler fuel load over which the default prime mover switches from reciprocating engine to combustion turbine for hot water and steam. The reasoning for this logic is that reciprocating engines are more cost effective at smaller scales and similarly efficient at producing hot water compared to combustion turbines. Combustion turbines become applicable at larger scales and are more efficient at producing steam. 

**Table 17. Threshold of Average Boiler Fuel Load over which the Default Prime Mover Switches from Reciprocating Engine to Combustion Turbine** 

||**Hot Water (Assumes Boiler**<br>**Efficiency of 0.8)**|**Steam (Assumes Boiler**<br>**Efficiency of 0.75)**|
|---|---|---|
|Threshold of average boiler fuel<br>load over which the default<br>prime mover switches from<br>reciprocating engine to<br>combustion turbine|27.0 MMBtu/hr (equates to<br>roughly 5,100 kW reciprocating<br>engine and 3,600 kW<br>combustion turbine)|7.0 MMBtu/hr (equates to<br>roughly 3,700 kW reciprocating<br>engine and 1,000 kW<br>combustion turbine)|



The user has the option override this default prime mover logic by clicking the “Change default prime mover & size class?” checkbox. In this case, the user has full control of the prime mover, and they must also select the size class that they want to consider. 

It is the user’s option to constrain the search space for CHP size. For the example above, the user could enter the ‘Minimum non-zero power capacity (kW)’ as 100 kW and the ‘Maximum electric power capacity (kW)’ as 600 kW. In this case, the REopt web tool would run the optimization with default costs and performance representative of this range and the model would return a size within this 100-to-600-kW range, if cost effective, or a 0-kW size if CHP in this size range is not cost effective. Alternatively, the user could select to model a CHP system with costs and performance for a generator in the range of 100 to 600 kW but can expand the search space of 

83 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

the model to allow it to consider system sizes that are either above or below this range to see if cost-optimal sizing might indicate sizes outside the selected range might be cost effective. In the REopt web tool, the defaults for the minimum and maximum sizes for the search space are greater than the size class size ranges as shown in the tables. 

As seen in Table 18 through Table 21, the default minimum size is 0 kW for all prime movers and size classes, meaning “no CHP” is always a possible result based on the optimization to minimize life cycle cost. The default ‘Minimum non-zero power capacity (kW)’ is 50% of the lower bound of the size class; however, if the result is a CHP size less than the lower bound of the size class, it is advised to rerun the model with the next-lowest size class. The default ‘Maximum electric power capacity (kW)’ is set to a high value for all size classes, although it is also advised to increase the size class appropriately if the result is higher than the upper bound of the chosen size class. 

The user can enter a single power-specific cost ($/kW) or enter two costs ($/kW) to generate a linear cost function. If a single input is entered, the model uses the same total installed cost ($/kW) for all CHP sizes. If two size-cost pairs are entered, total installed costs are calculated by linear interpolation between the two cost limits. Default costs are provided for two size-cost pairs as shown in Table 18 through Table 21. When two size-cost pairs are entered, CHP sizes less than the smaller size will have the first cost pair ($/kW) and sizes larger than the larger cost pair will have the second cost ($/kW). 

Default heat recovery parameters assume the following process heat load conditions: 

- Hot water is generated assuming 160°F inlet and 180°F outlet, (consistent with default heat loop conditions described in Section 5.2, Heating System) for reciprocating engines and microturbines. 

- Steam is generated at 150 psig saturated. 

Note: It is possible that the user could set up a model that is internally inconsistent/illogical. For example, a user could specify that the existing heating plant generates steam and selects a prime mover type that is appropriate only for hot water systems. The model might still run in this case but solution results would be invalid. 

84 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 18. Reciprocating Engine Cost and Performance Parameters Included in the REopt web tool** 

|**Size Class**|**Class 0**|**Class 1**|**Class 2**|**Class 3**|**Class 4**|**Class 5**|**Class 6**|**Class 7**|
|---|---|---|---|---|---|---|---|---|
|Class size low(kW)|35|35|100|250|500|1,000|2,000|3,000|
|Class size high(kW)|4,500|100|250|500|1,000|2,000|3,000|4,500|
|Minimum non-zero<br>power capacity (kW)|17.5|17.5|50|125|250|500|1,000|1,500|
|Installed cost function,<br>installed cost ($/kW),<br>and size pair at lower<br>size|$4,250,<br>35 kW|$4,250,<br>35 kW|$3,700,<br>100 kW|$3,450,<br>250 kW|$3,150,<br>500 kW|$2,800,<br>1,000<br>kW|$2,550,<br>2,000<br>kW|$2,350,<br>3,000<br>kW|
|Installed cost function,<br>installed cost ($/kW),<br>and size pair at larger<br>size|$2,000,<br>4,500<br>kW|$3,700,<br>100 kW|$3,450,<br>250 kW|$3,150,<br>500 kW|$2,800,<br>1,000<br>kW|$2,550,<br>2,000<br>kW|$2,350,<br>3,000<br>kW|$2,000,<br>4,500<br>kW|
|Fixed O&M($/kW/yr)|0|0|0|0|0|0|0|0|
|Variable O&M cost<br>($/kWh)|0.0195|0.0275|0.0235|0.021|0.0185|0.016|0.0145|0.0135|
|Electric efficiency at<br>100% load (HHV basis)|35.6%|28.7%|31.2%|34.5%|36.6%|38.5%|40.3%|40.5%|
|Hot water thermal<br>efficiency at 100% load<br>(HHV basis)|43.8%|52.0%|48.5%|44.5%|41.9%|40.2%|38.4%|38.4%|
|Steam thermal efficiency<br>at 100% load (HHV<br>basis)|14.2%|0.0%|0.0%|0.0%|16.9%|14.2%|13.0%|12.1%|
|Cooling thermal factor<br>(single effect)|0.84|0.0|0.80|0.85|0.85|0.85|0.85|0.85|
|Min. electric loading of<br>prime mover (% of rated<br>electric capacity)|25%|25%|25%|25%|25%|25%|25%|25%|



85 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 19. Micro-Turbine Cost and Performance Parameters Included in the REopt web tool** 

|**Size Class**|**Class 0**|**Class 1**|**Class 2**|**Class 3**|
|---|---|---|---|---|
|Class size low(kW)|65|65|200|600|
|Class size high(kW)|1,000|200|190|1,000|
|Minimum non-zero power<br>capacity (kW)|45.5|45.5|140|420|
|Installed cost function, installed<br>cost ($/kW), and size pair at<br>lower size|$4,900,<br>65 kW|$4,900,<br>65 kW|$4,400,<br>200 kW|$3,700,<br>600 kW|
|Installed cost function, installed<br>cost ($/kW), and size pair at<br>larger size|$3,400,<br>1,000<br>kW|$4,400,<br>200 kW|$3,700,<br>600 kW|$3,400,<br>1,000<br>kW|
|Fixed O&M($/kW/yr)|0|0|0|0|
|Variable O&M cost($/kWh)|0.015|0.016|0.016|0.014|
|Electric efficiency at 100% load<br>(HHV basis)|27.4%|26.5%|28.2%|28.3%|
|Hot water thermal efficiency at<br>100% load (HHV basis)|40.2%|42.8%|38.4%|37.8%|
|Steam thermal efficiency at<br>100% load (HHV basis)|0.0%|0.0%|0.0%|0.0%|
|Cooling thermal factor (single<br>effect)|0.94|0.94|0.94|0.94|
|Min. electric loading of prime<br>mover (% of rated electric<br>capacity)|30%|30%|30%|30%|



86 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 20. Combustion Turbine Cost and Performance Parameters Included in the REopt web tool** 

|**Size Class**|**Class 0**|**Class 1**|**Class 2**|**Class 3**|**Class 4**|**Class 5**|**Class 6**|
|---|---|---|---|---|---|---|---|
|Class size low(kW)|2,000|2,000|3,500|5,000|8,000|10,000|15,000|
|Class size high(kW)|25,000|3,500|5,000|8,000|10,000|15,000|25,000|
|Minimum non-zero power<br>capacity (kW)|2,000|2,000|3,500|5,000|8,000|10,000|15,000|
|Installed cost function,<br>installed cost ($/kW), and<br>size pair at lower size|$5,200,<br>2,000 kW|$5,200,<br>2,000<br>kW|$4,200,<br>3,500<br>kW|$3,400,<br>5,000<br>kW|$2,850,<br>8,000<br>kW|$2,500,<br>10,000<br>kW|$2,150,<br>15,000<br>kW|
|Installed cost function,<br>installed cost ($/kW), and<br>size pair at larger size|$1,700,<br>25,000<br>kW|$4,200,<br>3,500<br>kW|$3,400,<br>5,000<br>kW|$2,850,<br>8,000<br>kW|$2,500,<br>10,000<br>kW|$2,150,<br>15,000<br>kW|$1,700,<br>25,000<br>kW|
|Fixed O&M($/kW/yr)|0|0|0|0|0|0|0|
|Variable O&M cost($/kWh)|0.0127|0.0145|0.0140|0.0135|0.0130|0.0120|0.0100|
|Electric efficiency at 100%<br>load (HHV basis)|28.54%|23.60%|25.55%|28.40%|30.00%|30.55%|33.20%|
|Hot water thermal efficiency<br>at 100% load (HHV basis)|43.39%|44.99%|46.04%|45.60%|44.28%|42.24%|39.16%|
|Steam thermal efficiency at<br>100% load (HHV basis)|39.44%|40.90%|41.85%|41.45%|40.25%|38.40%|35.60%|
|Cooling thermal factor<br>(double effect)|0.90|0.90|0.90|0.90|0.90|0.90|0.90|
|Min. electric loading of<br>prime mover (% of rated<br>electric capacity)|50%|50%|50%|50%|50%|50%|50%|



87 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 21. Fuel Cell Cost and Performance Parameters Included in the REopt web tool** 

||**Class 0**|**Class 1**|**Class 2**|
|---|---|---|---|
|Class size low (kW)|440|440|1,400|
|Class size high (kW)|10,000|1,400|10,000|
|Minimum non-zero power capacity (kW)|440|440|1400|
|Installed cost function, installed cost<br>($/kW), and size pair at lower size|$6,400,<br>440kW|$6,400,<br>440kW|$5,890,<br>1,400kW|
|Installed cost function, installed cost<br>($/kW), and size pair at larger size|$4,710,<br>10,000kW|$5,890,<br>1,400kW|$4,710,<br>10,000kW|
|Fixed O&M ($/kW/yr)|0|0|0|
|Variable O&M cost ($/hr/kW-rated)|0.049|0.051|0.046|
|Electric efficiency at 100% load (HHV<br>basis)|39.9%|38.6%|41.3%|
|Hot water thermal efficiency at 100% load<br>(HHV basis)|23.5%|20.6%|26.5%|
|Steam thermal efficiency at 100% load<br>(HHV basis)|17.2%|14.6%|19.7%|
|Cooling thermal factor (double effect)|0.85|0.85|0.85|
|Min. electric loading of prime mover (% of<br>rated electric capacity)|30%|30%|30%|



The default minimum CHP system size is zero, and the default maximum CHP system size is double the heuristic size based on the average heating load on site for each prime mover.  The parameter ‘Cooling thermal factor’ included in Table 18 through Table 21 is the ‘Knockdown factor for CHP-supplied thermal to Absorption Chiller’ input in the user interface.  See Section 16, Absorption Chilling for more information. 

## **14.9 Back-Pressure Steam Turbine CHP** 

The back-pressure steam turbine CHP is a bottoming-cycle CHP, and the operating parameters are much different than the topping-cycle CHP. The high-level system configuration diagram is illustrated in Figure 13. Condensed water at point 1 is pumped to high pressure at point 2 where it gets heated to steam at point 3. The high-pressure steam at point 3 is expanded in the steam turbine to low pressure steam at state 4, and this process generates electricity. The low pressure steam at point 4 is condensed to a saturated liquid condition by extracting heat to the process heating load. 

88 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [370 x 199] intentionally omitted <==**

**Figure 13. Back-pressure steam turbine CHP diagram (DOE CHP Fact Sheet)** 

When screening for backpressure steam turbine, the REopt web tool assumes an existing steam plant exists for generating steam to serve the existing process heating loads. The REopt web tool then considers whether it is cost-effective to add a backpressure steam turbine to the system for generating electricity. If added to the model, the steam turbine is assumed to be available for power generation only when heat is needed. The steam turbine can generate power in each time step using all or some of the steam going to process load. It can also choose not to generate any power. The REopt web tool assumes that if the user screens for backpressure steam turbine, the existing steam system is capable of providing the steam flow at the user-entered (or default) temperature and pressure. The REopt web tool does not consider the impact of adjusting the existing steam plant’s temperatures and pressures on boiler system efficiency. 

If the user selects the steam option for “Existing boiler type and assumed CHP thermal production type”, steam turbine is added to the prime mover options in the CHP technology input section. The input parameters and default values for the steam turbine prime mover are listed in Table 22. The data for size classes 1 – 3 are based on the three steam turbine sizes listed in the DOE CHP Fact Sheets. The size class 0 data is the average data across all three size classes. The size class initially chosen by the web tool is the steam turbine size based on the average heating load of the site. 

89 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 22. Steam turbine default cost and performance parameters from DOE CHP Fact Sheets** 

|**Size class**|**0**|**1**|**2**|**3**|
|---|---|---|---|---|
|Steam turbine size from Fact Sheet(kW)|Avgof ->|500|3,000|15,000|
|Size class range (kW)|0 – 25,000|0 – 1,000|1,000 –<br>5,000|5,000 –<br>25,000|
|Total installed cost ($/kW)|$828|$1,136|$682|$666|
|Steam turbine inlet pressure (psig)|600|500|600|700|
|Steam turbine inlet temperature (°F)|592|550|575|650|
|Steam turbine outlet pressure (psig)|117|50|150|150|
|_Advanced inputs_|||||
|Fixed O&M Cost ($/kW/yr)|0.0|0.0|0.0|0.0|
|Variable O&M Cost ($/kWh)|0.008|0.010|0.009|0.006|
|Isentropic efficiency|63.9%|52.5%|61.2%|78.0%|
|Gearbox and electric generator efficiency|94.7%|94.0%|94.0%|96.0%|
|Net-to-gross electric power ratio|97.1%|97.4%|96.6%|97.3%|



Figure 14 illustrates the steam turbine CHP performance parameters which are used to calculate the conversion efficiency of steam to net electric power. The heat recovered from the low pressure steam to the process heating load is determined by assuming the steam is condensed to a saturated liquid state and all of that energy is used (no additional heat losses). 

**==> picture [388 x 263] intentionally omitted <==**

**Figure 14. Steam turbine performance parameter diagram** 

90 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

The performance of the back pressure steam turbine is described in the following equations, and the referenced steam state point numbers are used from Figure 13. 

The specific work (w shaft) of the steam turbine shaft is defined by the actual enthalpy difference between the high pressure and low pressure steam which can be calculated using the isentropic (constant entropy) pressure letdown enthalpy h4,s and the isentropic efficiency (ηisentropic). 

**==> picture [381 x 16] intentionally omitted <==**

The gross electric specific work (w electric,gross) is calculated by the shaft power and the gearbox and generator efficiency (η𝑔 𝑔 𝑔 𝑔𝑔&𝑔 𝑔 𝑔 𝑔 𝑔𝑔). 

**==> picture [393 x 15] intentionally omitted <==**

The thermal production from the steam turbine is determined by condensing the low pressure steam (state point 4) to a saturated liquid state (state point 1). 

**==> picture [359 x 15] intentionally omitted <==**

The saturated liquid (state point 1) is then pumped up to a high pressure liquid prior to entering the boiler: 

**==> picture [351 x 25] intentionally omitted <==**

The pumping power (wpump) is not handled explicitly in the model. Instead, the pumping power is lumped into the net-to-gross electric power (η𝑔 𝑔𝑔−𝑔 −𝑔 𝑔 𝑔𝑔−𝑝𝑝𝑔𝑔𝑝𝑝𝑔 ) ratio which accounts for any auxiliary power requirements of the steam turbine system, including pumping and controls equipment. 

**==> picture [63 x 12] intentionally omitted <==**

**==> picture [294 x 15] intentionally omitted <==**

The boiler thermal energy to heat state point 1 to state point 2 required is defined by: 

**==> picture [343 x 15] intentionally omitted <==**

The model works by using ratios of: 

**==> picture [283 x 20] intentionally omitted <==**

2. Thermal production to thermal consumption: qprocess heat 

**==> picture [28 x 7] intentionally omitted <==**

These ratios are calculated in a preprocessing step based on the user’s input steam conditions and efficiencies, and they are assumed to be constant and not a function of load. This allows the model to size and dispatch the steam turbine in REopt’s mixed integer linear optimization model. 

91 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

For the optimization, the maximum power available in a timestep is determined by the user’s entered heating load. 

Unlike the topping cycle CHP systems, there is no constraint included in the REopt web tool for minimum turndown limit for the backpressure steam turbine. 

## **14.10  CHP Scheduled and Unscheduled Maintenance** 

Scheduled and unscheduled maintenance is required for CHP systems, and the REopt model accounts for this by using predetermined periods of time for which CHP is unavailable to produce electric and thermal power. Default maintenance periods are provided for reciprocating engine, microturbine, and combustion turbine prime movers based on operational data and consultation with industry experts. CHP suppliers give warranty or guarantees based on a minimum availability (hours available to operate divided by all 8,760 hours of the year); often this number is lower than the _actual_ availability of the CHP system because the suppliers want to have some safety margin on their guarantees. The maintenance period defaults used in the REopt web tool represent estimates for the _actual_ CHP availability. The schedule of the default periods and summary metrics can be viewed in the REopt web tool, but a high-level summary is given in Table 23. 

**Table 23. Default Maintenance Periods and Unavailability Summary Metrics** 

||**Recip.**<br>**Engine**|**Combustion**<br>**Turbine**|**Micro-**<br>**turbine**|**Fuel**<br>**Cells**|
|---|---|---|---|---|
|Number ofplanned maintenance events|6|2|2|2|
|Duration ofplanned(days)|3|2|3|3|
|Number of unplanned maintenance events|3|2|2|2|
|Duration of unplanned(days)|2|2.5|2.5|2.5|
|Availability|95%|97%|97%|97%|



The number of planned and unplanned outages are spread out throughout the year, and in the default schedules there is no more than one in any given month. Each period is assumed to be a consecutive block of time. The planned maintenance periods are assumed to be scheduled on the weekends (which is typically off-peak if there is a time-of-use characteristic to the electric rate tariff) to the extent possible (if 2 days or less in duration). The unplanned maintenance periods are assumed to occur during the weekdays to be conservative in that the electricity rates and loads are typically the highest during the weekdays. 

The user may also upload their own custom maintenance schedule with the provided form. The form is available by clicking the “Download schedule” link under the CHP Maintenance Schedule section of the CHP accordion. Table 24 provides a description of the form headings and valid inputs for those attributes. 

92 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 24. Custom Uploaded CHP Maintenance Schedule Form Description** 

||**_month_**|**_start_week__**<br>**_of_month_**|**_start_day__**<br>**_of_week_**<br>**_(1=Monday)_**|**_start_hour (1-_**<br>**_24)_**|**_duration_hours_**|
|---|---|---|---|---|---|
|Description|The month in<br>which the<br>outage starts|The week of<br>the month in<br>which the<br>outage starts|The day of the<br>week in which<br>the outage<br>starts|The hour of<br>the day in<br>which the<br>outage starts|The duration of<br>the outage, in<br>hours|
|Valid range|1–12|1–6|1–7|1–24|8,760|
|Other notes|All values must be integers. The_start_week_of_month_=1 and<br>_start_week_of_month_=5 or 6 often do not contain all 7 days of the week; see Figure<br>15 for a grid of how the_start_week_of_month_and_start_day_of_week_align with an<br>example month (January 2017). Some months do not have a_start_week_of_month_=5<br>or 6. An outage must not extend past the end of the year; alternatively, specify two<br>separate outages, one for the end and one for the beginning of the year.|||||



**==> picture [201 x 186] intentionally omitted <==**

**Figure 15. Example month for understanding how to build a maintenance period with respect to the year/month calendar** 

In the example month and year of Figure 15 (January 2017), the _start_week_of_month_ =1 only has Sunday ( _start_day_of_week_ =6) in it, so the first valid Monday of the month would be specified by _start_week_of_month_ =2 and _start_day_of_week_ =1. Regarding an outage specified at the end of the month, _start_week_of_month_ =6 only has Monday and Tuesday in it, so an entry of _start_week_of_month_ =6 and _start_day_of_week_ =3 (Wednesday) would be invalid. Note too that valid numbers for _start_hour_ are 1 to 24 and that 1 represents the first hour of the day, midnight to 1 a.m. So, if the user wants to model a maintenance starting at 7 a.m., the value entered as _start_hour_ would be 6. 

The REopt web tool identifies the total system size that minimizes the life cycle cost of energy at the site. The minimum non-zero electric power capacity is used to narrow the lower limit of size range of the search space that the REopt web tool can select. For example, if the user enters a ‘Minimum electric power capacity (kW)’ of 0 and a ‘Maximum electric power capacity (kW)’ of 100, the REopt web tool could return a value anywhere between 0 and 100 kW. With this ‘Minimum non-zero power capacity (kW)’ input, the user could enter a value of 30 kW, for 

93 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

example, so that the REopt web tool can only return a system size of 0 or a size between 30 kW and 100 kW. 

## **15 Prime Generator** 

The following prime generators can be modeled: reciprocating engine, microturbine, combustion turbine, and fuel cell. Note that the prime generator and the CHP technology use the same set of code within REopt. To model a prime generator, the heat recovery parameters for CHP are set to 0, meaning that the unit only generates electricity. In the REopt Web Tool, this is done automatically by selecting ‘Prime Generator’ on the inputs page in Step 2. 

Because the prime generator and CHP technologies are the same technology module within REopt, the user can only run one or the other, not both simultaneously. In the web tool user interface, if the user selects CHP, the prime generator technology cannot be selected. And if the user chooses prime generator, CHP cannot be selected. 

For detailed description of the prime generator performance model, refer to section 14.2, CHP Fuel Consumption. The user may also find the discussions in sections 14.4, 14.6, 14.7, 14.8, and 14.10 helpful. 

The default electric efficiency for the prime generators is assumed to be the same as those described for CHP in section 14.8, Topping Cycle Default CHP Cost & Performance Parameters by Prime Mover Type & Size Class. The prime generator costs are lower than the comparable CHP costs due to the absence of heat recovery equipment and being simpler to construct and interconnect at a facility. Default installed and O&M cost values are assumed to be 75% of the default costs for the full CHP system with the same prime mover; see Table 18 through Table 21 for the CHP default costs by prime mover and size class.  Additionally, the federal ITC  is reduced to zero for the reciprocating engine and combustion turbine prime mover types – microturbine and fuel cell prime generator defaults to the 30% which is the same as CHP. 

## **16 Absorption Chilling** 

Absorption chillers generate chilled water using a heat source to drive a refrigeration cycle. If an absorption chiller is considered, it is assumed there is an existing chilled water loop served by existing electrically driven chillers and the condenser water loop has sufficient capacity to dissipate the increased load required by the absorption chiller. The REopt web tool does not size or cost the cooling distribution system, the existing electrically driven chiller, nor size or cost incremental capacity requirements for absorption chiller condenser heat rejection. 

The user can elect to consider adding an absorption chiller to supplement cooling provided by the existing electricity driven chiller plant. The heat required for the absorption chiller can be provided from CHP, the existing heating plant, and hot water TES if it is included in the model solution. The model assumes the optional absorption chiller would be connected to the process heating loop, i.e., it would add heating load to the user-entered heat load. A direct-fired absorption chiller cannot be modeled. 

Absorption chiller unit heat requirements are not adjusted based on chiller loading or other operational conditions. The COP value is assumed to represent the average absorption chiller 

94 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

performance throughout the year. The user can adjust the default COP value. The default absorption chiller COP is dependent on whether the user selects the existing facility’s boiler as producing steam or hot water. If the user selects steam, the absorption chiller is assumed to be a double-effect unit driven by steam with a COP of 1.42 kW thermal cooling output per kW thermal heat input. For a hot water boiler, we assume the absorption chiller is driven by hot water and therefore a single-effect unit with a COP of 0.74 (DOE Advanced Manufacturing Office 2017). 

The parameter ‘Cooling thermal factor’ included in Table 18 through Table 21 in Section 14.8, Topping Cycle Default CHP Cost & Performance Parameters by Prime Mover Type & Size Class, is a ‘knockdown’ factor that is used to estimate the impact of absorption chillers’ higherquality heat requirements on the recoverable heat from CHP. It is the ‘Knockdown factor for CHP-supplied thermal to Absorption Chiller’ input in the user interface. The cooling thermal factor effectively reduces the absorption chiller COP based on two considerations: (1) the hot water-driven single effect absorption chiller requires slightly higher-temperature water than the assumed hot water loop temperatures used to estimate the default heat recovery parameters; and (2) the absorption chiller’s return water temperature is not as low as the building’s hot water loop return water temperature (see Section 7.4, Heating Loads). Both factors reduce the amount of CHP-produced thermal power that can be applied to the absorption chiller with its nominal COP value. For a combustion turbine prime mover supplying steam to a two-stage absorption chiller, a cooling thermal factor is also applied for a similar reason. 

In addition to heat, the absorption chiller consumes electricity for heat rejection to cooling towers. The electric-based COP default is 14.1 kWt/kWe, which is equivalent to 0.25 kWe/ton. This is also a user input and can be changed. 

The model does not include turn-down limits (minimum unloading ratio constraint) on the absorption chiller. 

If the user selects to screen for an absorption chiller, the default cost assumption is that there is room for the absorption chiller within the existing cooling plant and that integration for parallel operation with the existing electric chillers can be accomplished. Additional costs for constructing a new building or extensive retrofits are not included. The user can change the default costs to include these. 

The default capital and O&M costs for absorption chiller are dependent on the cooling capacity of the absorption chiller system. Since the web tool does not know the cost-optimal absorption chiller size before the model is run, the maximum value of the facility cooling load (units of ton) entered by the user is used as a proxy for this capacity. Table 25 lists the data used for absorption chiller installed cost and O&M cost based on consulting from industry representatives. If the peak cooling load is below the smallest data point (10 ton) or above the largest data point (1000 ton), the smallest and largest data point costs are used, respectively. If the peak cooling load is between two adjacent data points, linear interpolation is used to calculate the costs. 

**Table 25. Absorption Chiller Installed Cost and O&M Cost** 

||Peak Cooling Load (ton)|<10|50|200|300|400|500|600|700|800|900|>1000|
|---|---|---|---|---|---|---|---|---|---|---|---|---|



95 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
|_Total Installed Costs($/ton)_||||||||||||
|Single Effect|7,000|3,066|2,027|1,587|1,527|1,426|1,365|1,313|1,312|1,277|1,248|
|Double Effect|N/A|3,723|2,461|1,960|1,855|1,709|1,623|1,547|1,520|1,470|1,427|
|_O&M Costs ($/ton-year)_||||||||||||
|Single Effect|300|80|36|32|31|30|28|26|23|20|18|
|Double Effect|N/A|100|43|36|34|32|30|28|26|23|20|



## **17 Thermal Energy Storage** 

Hot water and chilled water storage tanks are insulated tanks used to store thermal energy to decouple production from consumption. We assume TES can be added to the existing systems without replacing hot water boilers or chillers. If significant system upgrades are required to add TES, the user should adjust the TES capital costs to reflect those. 

The TES tank is assumed to be stratified with a thermocline that separates the supply water (hot water in hot water TES or chilled water in a chilled water TES) from the return water. 

Tank capacity and costs are entered in units of gallons and $/gallon respectively. Volumetric units are converted to thermal capacity units within the model based on _temperature difference_ between the supply and return water temperatures of the hot water loop (for Hot Water TES) chilled water loop (for Chilled Water TES). 

Hot water from the boiler plant or the CHP heat recovery unit can be stored in a hot water TES. This hot water can then be applied to the facility hot water load or to an absorption chiller load, if considered. 

Chilled water generated from the existing electric chiller and possible supplementary absorption chiller can be stored in the chilled water TES tank. 

The model determines the size of TES based on the cost-optimal maximum volume of stored energy. We assume the TES can be fully charged with either hot water or chilled water. However, a minimum stored energy requirement is imposed as a fraction of total TES tank volume. This is used to represent the thermocline region which must be maintained at low stored energy levels to separate the warmer and colder sides of the thermocline. The default minimum energy storage value is 10% for both the hot and chilled water TES. The minimum SOC default is estimated from Figure 2 in ASHRAE (2016). Any minimum SOC constraint applies all year and therefore the implicit assumption is that if a tank is selected by the model, it is thermally maintained all year. 

In the first hour of the simulation, stored energy is assumed to be 50% of the TES capacity. Between the maximum and minimum stored energy limits, the capacity of stored hot/chilled water is a function of the water volume stored in the tank’s supply side of the thermocline. 

The heat loss (or gain) depends on many factors, including the temperature of the stored fluid (and therefore the SOC of the tank), surface area to volume of the tank (which varies with TES capacity and diameter-to-height ratio), thickness of tank insulation, and ambient conditions 

96 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

(temperature, solar insolation, and wind speed) (ASHRAE 2016). For the REopt web tool, thermal loss is modeled as a constant rate and comes from general rules of thumb in the cited references and heat transfer calculations. The default value is 0.04% per hour (approximately 1% per day). It is intended to capture heat loss (or gain in the case of chilled water TES) of the tank to and from the environment. This time-dependent lost energy has to be met by the chiller by producing more chilled water for chilled water TES and by the boiler by producing more hot water for hot water TES when TES is included in the solution. 

The maximum discharge rate from TES is not constrained as we assume in application it would be determined by the facility cooling or heating loads and therefore in the model we allow the load in any hour to be completely served by stored chilled water or hot water if the TES has sufficient stored energy. 

The maximum charge rates for hot water and chilled water TES are described in the two sections that immediately follow. 

Default capital costs are taken from Glazer (2019), which provides estimated total installed costs for chilled water TES over a range of sizes. Costs from the reference in units of $/ton-hour are converted to $/gallon assuming a 14°F temperature difference. The average costs range from $2.82/gallon for 100,000-gallon tank to $0.93/gallon for a 2,000,000-gallon system. These costs from the reference, converted as described, are shown in Figure 16. 

**==> picture [433 x 292] intentionally omitted <==**

**----- Start of picture text -----**<br>
$4.00<br>$3.50<br>$3.00<br>$2.50<br>$2.00<br>Cost ($) = 197.01*gallons [-0.369]<br>$1.50<br>$1.00<br>$0.50<br>$0.00<br>0 500,000 1,000,000 1,500,000 2,000,000 2,500,000<br>TES Tank Volume (gallons)<br>Installed Costs ($/gallon)<br>**----- End of picture text -----**<br>


**Figure 16. TES installed cost estimates from Glazer (2019) and applying a 14°F temperature differential assumption** 

97 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

In the REopt web tool, we set the default value to $1.50/gallon which is the cost in the reference for a tank of about 550,000 gallons. We assume hot water and chilled water TES tanks cost the same on a per-gallon basis. 

O&M for the chilled water storage tank is assumed to be a fixed yearly cost, so there is no variable O&M cost component. The default cost is $0/gallon/year but the user may add this for more detailed cost assessment. 

## **17.1 Chilled Water TES** 

If included, the storage system is assumed to be a single stratified water tank. The thermal storage capacity per gallon of chilled water storage is a function of the supply and return temperatures of the chilled water process loop. The default supply water temperature is 44°F and the default return water temperature is 56°F. The user may change these values to change the conversion of gallons to energy. 

As described in Section 5.3, there is an assumed upper limit on the cooling capacity of the cooling plant to impose a reasonable upper limit on the maximum charging rate of chilled water TES. Therefore, the maximum charge rate is determined by the assumed size of the cooling plant. There is no constraint on discharge rate. 

## **17.2 Hot Water TES** 

Hot water TES can support economics of CHP by allowing time shifting of CHP’s thermal resource in situations where the electricity demand and thermal demands are not time coincident. Hot water TES is an option only for hot water process loads. If the user selects steam as the ‘Existing boiler type,’ the hot water TES option is disabled. 

If included, the storage system is assumed to be a single stratified water tank. The thermal storage capacity per gallon of hot water storage is a function of the supply and return temperatures of the hot water process loop. The default supply water temperature is 180°F and the default return water temperature is 160°F. The user may change these values to change the conversion of gallons to energy. 

As described in Section 5.2, there is an assumed upper limit on the heating capacity of the hot water heating plant to impose a reasonable upper limit on the maximum charging rate of hot water TES. Therefore, the maximum charge rate is determined by the assumed size of the heating plant. There is no constraint on discharge rate. 

## **18 Geothermal Heat Pumps** 

Geothermal heat pumps can be used to provide space heating and cooling (and optionally domestic hot water (DOMHW)). There are multiple configuration options for heat pumps in REopt. What configuration the user chooses might depend on the type of existing HVAC equipment or whether the goal of GHP retrofit is to minimize HVAC energy usage. The configuration options in REopt are: 

1. Distributed water-to-air heat pumps (WAHP) or also described as water-source heat pumps (WSHP), are zone-level units that are coupled to the geothermal heat exchanger 

98 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

(GHX) with a building interior loop, sometimes called an ‘ambient’ loop. WAHPs 

   - ‘pump’ heat to and from the GHX fluid to deliver conditioned air to the zone to maintain zone temperatures. 

2. Central plant water-to-water heat pumps (WWHP) generate cooling water and heating water that is distributed throughout the facility to each zone via hydronic cooling and heating loops. In application, WWHP can be either located in a central mechanical room, or they can be multiple units distributed in a facility. However, in REopt, our cost model assumes only a central plant configuration. 

3. Hybrid geothermal heat exchange systems include either a supplemental cooling tower or boiler to augment the GHX. Both WAHP and WWHP can include hybrid geothermal GHX if appropriate for the facility. Hybrid GHX can be used to reduce the size of the GHX and therefore reduce the retrofit costs and improve economics. 

4. Hybrid GHP systems with boiler and/or chiller backup are systems in which the GHP and/or GHX are undersized and unable to serve the entire facility’s thermal loads at all time. In the time periods that GHP cannot serve all thermal loads, an existing boiler and/or chiller is dispatched to serve the remaining thermal loads. Under-sizing GHP and/or GHX below the facility’s peak thermal load can help reduce installation costs while requiring little actual dispatch of the boiler/chiller. 

This section describes the modeling and assumptions for GHP screening in the REopt web tool. In the model, a GHP retrofit for a facility is assumed to be comprised of the following major components: 

1. Heat pumps. 

2. A GHX to act as the heat source and sink for the heat pumps. 

3. For WSHP configuration, a building interior water loop that connects the heat pumps to the GHX. 

4. For hybrid GHX systems (described in 18.5), an auxiliary cooling tower or boiler is also included for supplementary heat exchange to or from the heat exchange fluid. 

5. For hybrid GHP systems, a boiler and/or chiller is need to meet thermal loads that the undersized GHP/GHX cannot serve. 

If the user is considering GHP, the following apply: 

1. By default, the GHP system serves the entire facility space heating and space cooling as entered by the user. If using DOE commercial reference buildings (see Section 7.2 Simulated Load Profile from Models) to synthesize the heating loads, the user may choose to have the heat pumps also serve the domestic hot water heating loads. See Section 7.4 Heating Loads for how the REopt web tool handles the split of heating fuel usage between space heating and domestic hot water. 

2. If the user specifies a hybrid GHP system where the GHP only serves part of the facility space heating and cooling load, they can set the maximum GHP size and/or maximum number of GHX boreholes. If these pre-defined GHP and/or GHX sizes are not sufficient to serve all the facility’s thermal load, REopt will dispatch a boiler and/or chiller to meet the remaining load. 

99 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

3. For WAHP, the GHP system is assumed to include distributed heat pumps in each HVAC zone of the facility. WAHP can operate either in heating or cooling mode as the zone requires. 

4. For WWHP, the GHP system is assumed to have a single heat pump for heating and a separate heat pump for cooling located in a mechanical room. These heat pumps are assumed to connect to hydronic heating and cooling loops that serve zone-level heat exchangers.For WAHP, heat exchange fluid piping, or ambient water loop, is added to the facility to connect the GHX to the heat pumps to serve as each heat pump’s heat source and sink. 

5. There is available space at the facility for geothermal heat exchanger bore field. 

GHP screening in the REopt web tool is fundamentally different than other REopt technology models for the following reasons: 

1. Sizing: Although the size of the heat pumps is an output from the model, the size is not found through an optimization. Instead, GHP is assumed to serve the entire or a portion of heating and cooling loads entered by the user. This is different than other REopt technologies where the DER are assumed to be able to operate in parallel with existing infrastructure such that it can either supplement or serve the entire/a partial set of loads if cost effective. If the user constrains the size of GHP, REopt will split their provided thermal loads into thermal loads served by the undersized GHP and thermal loads served by the system’s backup boiler and chiller. 

2. Dispatch: The heat pumps are assumed to operate at every hour to serve the heating and cooling loads as needed per the user’s inputs. Therefore, heat pump operation times and load levels are not a decision within the optimization. 

3. Because of these two key differences from REopt DER technologies, GHP can be described as a ‘Go / No-go’ technology, meaning that the full system is either cost effective or not; there is no decision-making internal to the model in terms of how much of the heating and cooling loads are to be served by GHP and how the heat pumps should be operated. 

## **18.1 Overview of the GHP Performance Model** 

The general approach for GHP analysis in the REopt web tool is as follows: 

1. The total facility heating fuel usage and cooling loads are entered by the user. 

2. An initial GHX size is chosen based on a heuristic multiplier on the coincident peak heating and cooling heat pump thermal power. 

3. The hourly thermal energy being sourced from and sunk to the water loop and the hourly electricity consumption of the heat pumps is determined based on the heat pump’s COP map. See 18.3 Heat Pump. 

4. The net energy added into the water loop from the heat pumps is used to estimate the water loop temperature entering the GHX. 

5. A separate GHX model calculates the heat transfer between the fluid loop and the ground to determine the water temperature leaving the GHX (and therefore entering the heat pumps) and the temperature of the earth in the vicinity of the GHX. 

6. Steps 3 – 5 are repeated for every timestep of the simulation (typically 1-4 timesteps per hour for the simulation duration (default of 25 years)). 

100 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

7. The minimum and maximum entering fluid temperature (EFT) of the heat pumps over the life of the system are compared to their respective limits, and a solver calculates the next iteration of GHX size to both, 1) minimize the GHX size, while 2) staying within the heat pump EFT limits. For hybrid GHX screening, this step is slightly different. For a description of the hybrid GHX screening option, see section 18.5. 

8. Steps 3 – 7 are repeated until the solver finds the smallest GHX size which stays within the heat pump EFT limits. 

GHP inputs are intended to characterize system costs, heat pump performance, and properties necessary for modeling GHX. The user may use defaults provided and shown in the user interface or adjust them to reflect details of the system performance and cost under consideration. Heat pump and GHX model and defaults are described in the following sections. 

## **18.2 GHP Cost Model** 

GHP retrofit costs include capital costs and O&M costs. The capital cost represents the fully burdened installed cost, including both equipment and labor. For GHP, the total capital cost is the sum of the costs for the heat pumps, the building interior heat exchange fluid loop, if needed, and the GHX system. For central plant WWHP, there is no need for an interior building ambient water loop to deliver GHX water to the heat pumps so that cost is $0 in this case. 

Note that the cost model does not include costs for WWHP heating and cooling loop distribution loops. These are assumed to exist within the facility if a user selects this configuration option. Retrofit costs for geothermal heat pumps are highly variable and will depend on the site-specific details of the existing HVAC infrastructure. General cost rules of thumb are provided as defaults for screening level analysis however, costs and performance should be developed by GHP experts after review of the facility’s equipment and loads. 

The O&M cost is the incremental cost difference for GHP HVAC retrofit over the conventional HVAC system it replaces. The O&M costs do not include energy impacts of GHP retrofit as those are separately accounted for in REopt. In the REopt web tool, the _default incremental O&M cost for GHP is negative_ , meaning that the O&M costs for the GHP system is assumed to be lower than the existing conventional HVAC equipment. 

There is an input field in the user interface called, ‘Avoided HVAC upgrades ($)’ that has a default value of $0. If the facility of interest has HVAC equipment at or near the end of its useful life and these equipment purchases can be avoided by GHP retrofit, the user can enter these avoided HVAC equipment costs here. These avoided costs, if entered by the user, will reduce the cost of the GHP retrofit equivalently and will increase the economic outlook for GHP retrofit. 

Another important cost assumption for GHP is the useful life of the GHX. The input ‘GHX useful life (years)’ has a default value of 50 years. If the economic analysis period is less than the ‘GHX useful life (years)’ a residual value for the GHX is calculated at the end of the analysis period using straight-line depreciation. That is, for useful life of 50 years and an analysis period of 25 years, the GHX would have a residual value that is 50% of its initial cost. This residual value is assumed to occur at the end of the analysis period and is discounted using standard economic methods back to Year 0 and applied as a ‘credit’ to the GHP retrofit capital costs. 

101 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

Default costs and references for them are provided Section 21, The REopt Web Tool Default Values, typical Ranges, and Sources. Incentives can be applied to reduce the cost; these are described in Section 4.3, Economic Incentives. 

## **18.3 Heat Pump** 

## _**18.3.1 Distributed Heat Pumps in WAHP configuration**_ 

The WAHP performance model is an amalgam of commercially available vendor water-to-air heat pumps[24] based on NREL market research. Vendor units were selected that were near 5-ton capacity, the assumed nominal rating for distributed units. The performance of the heat pump is largely a function of the entering fluid temperature (EFT) from the GHX. In REopt, we assume the energy requirements are solely a function of EFT, i.e., the impact of water flow rates, air flow rates, and loading on the unit are not modeled. Energy requirements as a function of EFT are entered as coefficient of performance (COP) values, where COP is a unitless parameter of thermal energy that is delivered by the heat pump divided by the electrical energy required to drive the unit. 

Figure 17 shows the default heat pump COP map for the distributed WSHP as a function of GHX EFT. The user can use the default parameters provided or modify them to represent the performance of a system of their own specification, selection, or design. 

**==> picture [362 x 217] intentionally omitted <==**

**----- Start of picture text -----**<br>
12<br>10<br>8<br>6<br>4<br>2<br>0<br>20 40 60 80 100 120<br>GHX Entering Fluid Temperature (F)<br>Cooling COP (kWt/kWe) Heating COP (kWt/kWe)<br>COP (kWt/kWe)<br>**----- End of picture text -----**<br>


**Figure 17. Default water-sourced heat pump performance map as a function of entering fluid** 

**temperature** 

> 24 Water Furnace Versatec variable speed, Trane Axiom Horizontal and Vertical Water Source Heat pumps, ClimateMaster 30 Digital Series 

102 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

The data points plotted in the figure above are included in Table 26. WAHP performance is linearly interpolated for EFTs between the performance points entered while heat pump performance is assumed to be constant outside the lower and upper bounds of the EFT values. 

**Table 26. Default heat pump performance as a function of entering fluid temperature** 

|**GHX EFT**<br>**(°F)**|**Cooling COP**<br>**(kWt/kWe)**|**Heating COP**<br>**(kWt/kWe)**|
|---|---|---|
|20|11.023|3.351|
|30|11.023|3.639|
|40|11.023|4.161|
|50|10.481|4.681|
|60|9.168|5.081|
|70|7.263|5.678|
|80|5.826|6.047|
|90|4.803|6.341|
|100|3.900|6.341|
|110|3.279|6.341|
|120|2.707|6.341|



The user can use the default heat pump performance parameters or model their own. If the user uploads a custom heat pump performance map, the minimum required number of rows is one and there is no upper limit on the maximum number of rows. However, each subsequent row must have EFT greater than the EFT in the previous row. That is, heat pump performance in the table must be entered in order of increasing EFT. 

Since the REopt web tool does not model each HVAC zone individually, and therefore size the heat pump for each individual zone, a ‘Heat pump capacity sizing factor’ is included as a user input that is used to increase the total capacity of the heat pumps above the maximum of the aggregated heating and cooling loads. With this factor set to 1.0, the total installed capacity of the heat pumps would be set to the maximum of the aggregated hourly heating or cooling loads. A factor above 1.0 ensures additional heat pump capacity is included based on the assumption that the heat pump capacity requirements for the individual zones will sum up to a value greater than the zone-aggregated heating and cooling loads. The default value for the ‘Heat pump capacity sizing factor’ is 1.1. 

## _**18.3.2 Central Plant Heat Pumps in WWHP configuration**_ 

The user might select central plant WWHP configuration option when facility has existing hydronic heating and cooling loops served by centralized chiller and hot water system. This configuration _could_ make use of the existing building hydronic loops and HVAC equipment. However, WWHP are most efficient when the cooling/chilled water and heating water temperatures for the zone level equipment are more temperate than was customarily utilized in older building stock. For example, older buildings may have heating loops with a setpoint temperature of 180 F. For WWHP, this is a high ‘lift’ and the WWHP efficiency would be considerably lower than a system that delivered lower temperature heating water, e.g., 160 F or 140 F. In older building stock, in the case where heating water loop setpoint might be 180 F, the zone level heat exchangers would be designed for this temperature, and they might not be able to deliver required level of heat if loop temperatures are reduced to allow more efficient operation 

103 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

of the WWHP. At the heating WWHP, there may be a need to stage two heat pumps in series to achieve higher loop temperatures. This would add costs and increase electricity consumption. Alternatively, the facility owner could consider retrofitting the heat exchangers in the airhandling units to increase their surface area and perhaps increase the size of the heating and cooling loop distribution piping. This too would impact the costs of the retrofit. 

The WWHP performance model is an amalgam of commercially available vendor water-to-water heat pumps[25] based on NREL market research. Currently, it is difficult to find performance data for 200-300 ton or larger WWHP. The performance estimate defaults in REopt are based on smaller WWHP units where published vendor data could be located. Additionally, published data for WWHP was difficult to find over a wide range of GHX source temperatures and load temperatures. REopt performance for WWHP therefore is based on limited data and includes some extrapolation, in some cases, outside equipment operating envelopes. 

The performance of the heat pump is largely a function of the entering fluid temperature (EFT) from the GHX, also called ‘source’ temperature, and the setpoint temperatures of the hydronic heating and cooling loops. In REopt, we assume the energy requirements are solely a function of EFT, i.e., the impact of water flow rates and loading on the unit are not modeled. Energy requirements as a function of GHX EFT are entered as coefficient of performance (COP) values, where COP is a unitless parameter of thermal energy that is delivered by the heat pump divided by the electrical energy required to drive the unit. 

Figure 18 shows the default cooling WWHP COP as a function of GHX EFT and cooling loop setpoint temperature. Figure 19 shows the performance for the heating unit as a function of the heating loop setpoint temperature. The user can use the default parameters provided or modify them to represent the performance of a system of their own specification, selection, or design. 

> 25 Climate Master TMW840, Trane EXW-240, Carrier 61WG Heating, Carrier 30WG & 30WGa Cooling 

104 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [327 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
10.0<br>9.0<br>8.0<br>7.0<br>6.0<br>5.0<br>4.0<br>3.0<br>2.0<br>1.0<br>0.0<br>30 40 50 60 70 80 90 100<br>GHX Entering Fluid Temperature (F)<br>40F cooling water 50F cooling water 60F cooling water<br>COP (kWt/kWe)<br>**----- End of picture text -----**<br>


**Figure 18. Default cooling WWHP performance map as a function of GHX EFT and cooling loop setpoint temperature** 

**==> picture [327 x 283] intentionally omitted <==**

**----- Start of picture text -----**<br>
6.0<br>5.0<br>4.0<br>3.0<br>2.0<br>1.0<br>0.0<br>30 40 50 60 70 80 90 100<br>GHX Entering Fluid Temperature (F)<br>120F heating water 130F heating water<br>140F heating water<br>COP (kWt/kWe)<br>**----- End of picture text -----**<br>


**Figure 19. Default heating WWHP performance map as a function of GHX EFT and heating loop setpoint temperature** 

105 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

The performance plotted in the figures above are included in Table 27 and 28. WWHP performance is linearly interpolated for EFTs between the performance points entered while heat pump performance is assumed to be constant outside the lower and upper bounds of the EFT values. Similarly, WWHP performance is linearly interpolated between columns of cooling loop setpoint temperatures if the user-entered cooling loop temperature falls between setpoint temperature columns. For setpoint temperatures above the highest temperature or below the lowest temperature, the values in the maximum temperature column and minimum temperature column, respectively, are used. 

**Table 27. Default cooling WWHP COP (kW/kWe) as a function of GHX EFT and cooling loop setpoint temperature** 

||<br>**setpoint temperature**|<br>**setpoint temperature**|<br>**setpoint temperature**|
|---|---|---|---|
|**EFT**<br>**(°F)**|**Cooling Loop Setpoint Temperature**|||
||40F|50F|60F|
|50|6.9|8.0|9.1|
|60|6.2|7.2|8.3|
|70|5.6|6.5|7.4|
|80|4.9|5.8|6.6|
|90|4.3|5.1|5.8|
|100|3.6|4.4|5.0|



**Table 28. Default heating WWHP COP (kW/kWe) as a function of GHX EFT and heating loop setpoint temperature** 

||<br>**setpoint temperature**|<br>**setpoint temperature**|<br>**setpoint temperature**|
|---|---|---|---|
|**EFT**<br>**(°F)**|**Heating Loop Setpoint Temperature**|||
||120F|130F|140F|
|30|2.7|2.3|2.2|
|40|3.2|2.8|2.7|
|50|3.7|3.2|3.1|
|60|4.2|3.7|3.5|
|70|4.7|4.1|4.0|
|80|5.2|4.6|4.4|



The user can use the default heat pump performance parameters or model their own. If the user uploads a custom heat pump performance map, the minimum required number of rows is one and there is no upper limit on the maximum number of rows. However, each subsequent row must have EFT greater than the EFT in the previous row. That is, heat pump performance in the table must be entered in order of increasing EFT. 

Similar to WAHP, a ‘Heat pump capacity sizing factor’ is included as a user input that is used to increase the total capacity of the heat pumps above the maximum heating and cooling loads. With this factor set to 1.0, the total installed capacity of each WWHP would be set to the maximum of the hourly heating and cooling loads. A factor above 1.0 ensures additional heat pump capacity is included based on the assumption that the heat pump capacity requirements might require a factor of safety above the loads entered. The default value for the ‘Heat pump capacity sizing factor’ is 1.1. 

106 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **18.4 Geothermal Heat Exchanger** 

Ground-source geothermal heat pumps require a large heat exchanger in the earth to reject heat to during cooling or to extract heat from during heating. Water or a water-glycol mix is used as the heat exchange fluid and is pumped through the ground heat exchanger (GHX, or GHE) and then through the building’s interior heat transfer fluid loop to each heat pump. 

In the REopt web tool, we assume a vertical bore field heat exchanger configuration. The GHX model used in the REopt tool was developed by Thermal Energy System Specialists, LLC[26] (TESS) of Madison, Wisconsin. This GHX model is proprietary to TESS, LLC and therefore is not part of the REopt tool’s open-source code repository. However, a free executable file of the GHX model is available for download in a separate GitHub repository that is governed under a different license agreement than REopt. The TESS GHX model license does not allow for distribution if downloaded. 

For simulation timesteps with both heating and cooling loads, the thermal energy sourced and sunk to the building interior loop from the distributed heat pumps is added together before heat exchange to the ground. That is, the heating and cooling loads from the heat pumps are netted within the water loop in each timestep to determine the entering fluid temperature to the GHX. 

The following additional assumptions apply to the GHX model: 

1. Vertical bore heat exchanger configuration. 

2. There is one U-tube per borehole. 

3. All boreholes are connected in parallel. 

4. Initial ground temperature (before GHX is added) is isothermal, undisturbed, and determined by the typical meteorological year ambient dry bulb temperatures at the start of the simulation. 

5. Soil is homogeneous. 

The default duration of the GHX model’s simulation time horizon is 25 years, the same default as the REopt tool’s economic analysis period. Depending on the relative magnitude of the heating and cooling needs, i.e., climate and facility type, the simulation years can greatly impact the size of the GHX (the number of vertical bores) and therefore the economic viability of a GHP retrofit. For unbalanced heating and cooling loads to the GHX, the size of the GHX will increase with increasing model simulation years to avoid violating the temperature limits of the heat transfer fluid. For example, in a cooling-dominated climate, the heat pumped to the GHX for space cooling is greater than the heat sourced from the GHX for space heating. Therefore, with time, the ground temperature will increase. The GHX model will iteratively increase the size of the GHX to find the minimum size GHX required so as not to violate the higher temperature limit for the GHX exiting fluid temperature. For a facility with relatively balanced heating and cooling loads to and from the ground, the GHX ground temperature will not drift as much with time and therefore the size of the GHX is less sensitive to the GHX simulation years parameter. An alternative configuration for the heat exchange system is called ‘hybrid GHX’. In REopt, a hybrid GHX system includes supplementary heat exchange to the GHX fluid with the addition of either a small boiler to add heat or a cooling tower to extract heat. Hybrid GHX is often 

> 26 Thermal Energy System Specialists, http://www.tess-inc.com/ 

107 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

considered to reduce the GHX size for facilities that have significantly imbalanced heating and cooling. Section 18.5 describes the hybrid GHX capability in REopt. 

## _**18.4.1 Inputs to the GHX model**_ 

The GHX model requires heating and cooling loads for the facility, relevant soil properties, GHX parameters, heat transfer fluid properties, heat pump performance parameters, and the hourly climate ambient temperature conditions for a typical meteorological year. Hourly ambient temperature values are determined by the site location as entered by the user. The hourly ambient temperature data comes from the PVWatts API. (See Section 10 Photovoltaics.) 

A full list of GHX inputs and default parameters is shown in Table 29. The default heat exchange fluid parameters are based on water although, depending on climate, water-glycol or other antifreeze solution may be required to protect against freezing. 

108 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 29. Geothermal heat exchanger system characteristics inputs** 

|**Parameter**|**Default**|**Reference**|
|---|---|---|
|GHX simulation years|25||
|Borehole (GHX bore/well) depth (ft.)|443|1*|
|Maximum allowable GHX return water temperature (°F)|104|1|
|Minimum allowable GHX return water temperature (°F)|23**|1|
|Borehole spacing distance (ft)|20|2, 3|
|Borehole spacing type (dropdown)|rectangular or<br>hexagonal||
|Borehole diameter (in)|6|1*|
|Grout thermal conductivity (Btu/hr-ft-°F)|0.75|1*|
|GHP nominal flow rate of GHX fluid (GPM/ton)|2.5|2|
|GHX fluid pump power (Watt/GPM)|15|4|
|GHX fluid pump minimum turndown|0.1|4|
|GHX fluid pump power curve exponent|2.2|4|
|GHX pipe diameter (in)|1.66|2, 3|
|GHX pipe wall thickness (in)|0.16|2|
|GHX pipe thermal conductivity (Btu/hr-ft-deg F)|0.23|1*|
|GHX pipe centerline distance between upwards and<br>downwards u-tube legs (in)|1.27|1*|
|GHX fluid density (lbm/cubic ft)|62.4|2|
|GHX fluid specific heat (Btu/lbm-F)|1.0|2|
|GHX fluid thermal conductivity (Btu/hr-ft-deg F)|0.34|6|
|GHX fluid dynamic viscosity (lbm/ft-hr)|2.75|6|
|GHX header depth (ft)|6.6|1*|
|GHX simulation solver tolerance (°F)|2|4|
|GHX simulation solver initial guess (ft/ton)|75|4|



* Standardized with default values from ComStock, URBANopt and/or ResStock 

**Although this is below the freezing point of water, this value is used as the default to allow the model to solve in colder climates. It is advised that the GHX fluid properties for colder climates be adjusted by the user to represent glycol-water or other anti-freeze solutions that may be applicable to prevent freezing. 

## References for Table 29: 

(1) URBANopt, based on Subject Matter Expert/Technical Advisory group (SME/TAG) input 

(2) Kavanaugh, Steve; Rafferty, Kevin; Geothermal Heating and Cooling: Design of Ground-Source Heat Pump Systems; ASHRAE RP-1674; 2014 

(3) ASHRAE, 2019 ASHRAE Handbook - HVAC Applications, Chapter 35 "Geothermal Energy"; 2019 

(4) Thermal Energy System Specialists, LLC GHX model default 

(5) Zheng, Z.; Wang, W.; Ji, C. A study on the thermal performance of vertical U-tube ground heat exchangers. Energy Procedia 2011, 12, 906–914. 

109 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

(6) Thermal conductivity:  https://www.engineeringtoolbox.com/water-liquid-gas-thermal-conductivity- - - - temperature pressure d_2012.html Viscosity: https://www.engineeringtoolbox.com/water dynamic kinematic-viscosity-d_596.html 

Default values for the ground properties are shown in Table 30 and Table 31. 

**Table 30. Ground properties** 

|**Parameter**|**Default**|
|---|---|
|Ground thermal conductivity (Btu/hr-ft-°F)|Climate zone dependent.<br>See Table 31|
|Ground density (lbm/ft³)|162.3|
|Ground specific heat (Btu/lbm-°F)|0.203|



**Table 31. Default ground thermal conductivity values by climate zone** 

|**Climate Zone**|**Ground thermal conductivity (Btu/hr-ft-°F)**|
|---|---|
|1A|1.029|
|2A|1.348|
|2B|0.917|
|3A|1.243|
|3B|1.364|
|3B-Coast|1.117|
|3C|1.117|
|4A|1.023|
|4B|0.972|
|4C|1.418|
|5A|1.726|
|5B|1.177|
|6A|0.977|
|6B|0.981|
|7|1.271|
|8|1.189|



Note that default data for ground thermal conductivity shown in Table 31 is highly uncertain and that this could be a key parameter that drives results. The user is advised to include a sensitivity on this parameter as well as to research or perform tests to determine a more accurate value of this and other ground properties. The default ground thermal conductivity values in Table 31 come from, Liu, Xiaobing; Joseph Warner; Mark Adams; _FY16 Q3 Milestone Report for Geothermal Vision Study Thermal Application (Geothermal Heat Pump) Complete Simulations of GHP Installations for Representative Buildings_ ; ORNL/LTR-2016/344; July 2016. The reference has a ground thermal conductivity of 1.034 for climate zone 7A and 1.508 for climate zone 7B. In the REopt web tool, we have only climate zone 7 (not 7A and 7B) so the default here is the average of these two values. Also, the reference does not include a value for climate zone 

110 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

8. In the REopt web tool we include the average value of the of the other climate zones as the default for climate zone 8 so that the user can run the model without getting an error. 

## **18.5 Hybrid Geothermal Heat Exchange** 

The investment costs of a GHP system are often greatly dependent on the size of the GHX due to significant costs for drilling and installing the vertical bore heat exchanger. Hybrid GHX can be considered to reduce the size of the GHX for facilities with imbalanced heating and cooling loads to potentially identify a lower initial-cost GHP configuration. 

In REopt, hybrid GHX means that in addition to the GHX as heat sink and heat source for heat pumps, an auxiliary heat exchange unit is installed to supplement geothermal heat exchange. This auxiliary unit provides additional heat exchange to the heat exchange fluid loop to reduce the size of the GHX, and therefore GHX costs, with a goal to make GHP retrofits more costeffective. In REopt, if additional heat is needed, the auxiliary heat exchange unit is a boiler; if additional cooling is required, the auxiliary heat exchange unit is a cooling tower. Hybrid GHX is provided as an option for GHP screening. The method for modeling hybrid-GHX capability in REopt was developed by TESS, LLC in the GHX model sourced from them (see section 18.4). 

Note: The existing hybrid GHX capability assumes a certain configuration and operation scheme. The approach may not result in more cost-effective GHP than non-hybrid GHE in all cases. Further, the hybrid model may not find a solution in some scenarios. Because of this, the user interface only offers hybrid GHP option for facilities where the ratio of heating to cooling loads is less than 10 and greater than 0.1. Outside of this ratio, the asymmetry in heating and cooling loads is too great for the hybrid GHX configuration modeled. 

While space heating with GHP, heat is ‘pumped’ by the heat pumps from the heat exchange fluid loop into the conditioned space, and therefore space heating will tend to make the heat exchange loop, and therefore earth surrounding the GHX, colder. Conversely, space cooling tends to heat the ground. The GHX model sizes the geothermal heat exchanger so that the liquid temperature entering the heat pumps does not get too warm or too cold but also ensures that the GHX is not oversized to keep capital costs down. In non-hybrid / full GHX analyses, the GHX is sized to ensure that the EFT to the heat pumps is constrained within specified high and low temperature limits (defaults provided that can be modified by the user) every hour of the simulation duration, e.g., 25 years. In facilities with imbalanced heating and cooling on an annual basis, the temperature of the ground increases or decreases year by year. Ensuring that the ground does not get too hot or too cold, i.e., violate the high and low temperature limits, is critical. The size of the GHX can be greatly impacted by this. In the model, to ensure the GHX is not oversized (and therefore not too costly), the fluid temperature leaving the GHX will generally hit either the high temperature limit (in cooling dominated facilities) or low limit (in heating dominated facilities) in at least one hour of the GHX simulation period. 

In hybrid GHX, the auxiliary heat exchange unit is utilized to minimize the effect of imbalanced ground heat exchange on the sizing of the GHX. As described above however, when facility heating and cooling loads differ by more than ten times, the hybrid GHX model in REopt is not 

111 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

applicable. REopt will check the ratio of heating to cooling based on user inputs and only allow hybrid GHX screening option when the ratio is greater than 0.1 and less than 10. 

In hybrid GHX, the geothermal heat exchanger is sized to serve an approximate balanced heating and cooling load on an annual basis where load refers to the load to/from ground, not the facility loads. The sizing methodology used by REopt for hybrid GHX will not guarantee fully balanced ground heating and cooling, but it will result in more balanced ground heat exchange than nonhybrid systems and therefore a smaller GHX. 

For GHX hybrid systems in REopt, only one heat pump EFT temperature limit is used for sizing the GHX while the auxiliary heat transfer unit is employed to control temperature to the other limit. Whether the high or low heat pump EFT limit serves as the constraint for sizing GHX is based on the relative magnitude of the total annual thermal energy pumped _from_ the heat exchange fluid loop (for space heating) or _to_ the heat exchange fluid loop (space cooling). The smaller of these determines which heat pump EFT limit is used as the constraining requirement for GHX sizing. See Table 32. 

**Table 32. Application of ground loop temperature limits in non-hybrid and hybrid GHX design** 

|GHX Type|Heat pump EFT high limit is a<br>constraint for GHX sizing|Heat pump EFT low limit is a<br>constraint for GHX sizing|
|---|---|---|
|Non-hybrid / full GHX|Yes|Yes|
|Hybrid GHX, heating-dominated<br>facility and therefore cooling<br>load is smaller|Yes|No|
|Hybrid GHX, cooling-dominated<br>facility and therefore heating<br>load is smaller|No|Yes|



Although the smaller of the heating and cooling loads will determine the size of the GHX, both load types are served by geothermal heat exchange. The auxiliary heat exchange unit will supplement geothermal heat exchange as needed for the larger load in some time periods, serving essentially as a ‘peaker’ unit for heat exchange loop temperature management. 

In a hybrid GHX system, the auxiliary heat exchange unit is either a boiler (for heating dominated facilities) or a fan-powered cooling tower (for cooling dominated facilities). 

In REopt hybrid GHX, the auxiliary heat exchange unit is downstream from the GHX and heat exchange loop fluid is diverted to it when auxiliary heat exchange is needed. See the concept schematic in Figure 20. 

112 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [419 x 338] intentionally omitted <==**

**Figure 20. GHP concept schematic for distributed water-source heat pumps (WSHP)** 

In the figure, point 1 is fluid leaving the heat pumps and entering the GHX. The fluid from each WSHP is assumed to be fully mixed before entering the ground loop. 

Point 2 is the leaving fluid temperature (LFT) from GHX and upstream of the auxiliary heat exchange unit. For sizing the GHX, the fluid temperatures at this point are checked against the heat pump EFT temperature limits. The GHX is sized to ensure point-2 LFT complies with the limits as described in Table 32. 

Point 3 is the fluid leaving the auxiliary unit and entering the heat pumps, or EFT. In non-hybrid systems, there is no auxiliary heat exchange unit, so the temperature at point 2, the GHX LFT, is always the same as the temperature at point 3, the heat pump EFT. 

In hybrid GHX, the auxiliary unit is only operated when the GHX LFT, point 2, is outside the heat pump EFT limits. When the auxiliary unit is not operating, it is bypassed and the temperature at point 2 and point 3 are identical. But when needed to ensure heat pump EFT limits are met, the auxiliary unit operates to ensure heat pump EFTs meet the requirements. For cooling dominated buildings, the auxiliary unit is a cooling tower. In this case, the cooling tower ensures the fluid entering the heat pumps is not too hot. The default maximum heat pump entering fluid temperature limit is 104 F. So, if the GHX LFT at point 2 is greater than 104 F, the auxiliary cooling unit will operate to 'trim’ the fluid temperature down to 104 F at point 3. For heating dominated facilities, the auxiliary unit is a boiler. In this case, the boiler is used to ensure 

113 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

the fluid entering the heat pumps is not too cold. The default minimum heat pump EFT is 23 F. If the GHX LFT at point 2 is less than 23 F, the auxiliary boiler will add heat to raise the fluid temperature entering the heat pumps (point 3) to 23 F. 

As an example, to demonstrate the modeling approach, a hybrid screening analysis for a building in a cooling-dominated climate would roughly follow the steps described below. In this example, the heat pump EFT high limit is assumed to be 104 F and the low limit is assumed to be 23 F. 

1. Building loads are analyzed in REopt to determine whether the heating load _from_ the heat exchange loop or the cooling load _to_ the heat exchange loop is greater on an annual basis. In this case, the energy to the loop for cooling is greater and this scenario is categorized as ‘cooling dominated.’ Without a hybrid system, the ground would tend to warm over time and the GHX would have to be sized to ensure that the ground does not become too warm. 

2. REopt determines this facility is cooling dominated and sets the auxiliary heat exchange unit as a cooling tower. 

3. Because the facility is cooling dominated, the smaller heating loads are assigned load priority for sizing the ground loop heat exchanger. As shown in Table 32, the GHX is sized such that the LFT of the GHX, point 2, is never lower than the heat pump EFT low temperature limit, 23 F in this example. 

In hybrid GHX, although the 104 F heat pump EFT upper temperature limit is not used as a constraint for GHX sizing, it is used as a constraint for sizing and estimating the energy consumption of the auxiliary heat exchange unit. Continuing with this example: 

4. The 104 F heat pump EFT upper temperature limit is assigned as the constraint to trigger operation of the auxiliary cooling unit. 

5. During cooling-dominated periods, the temperature of the fluid leaving the GHX, point 2, will sometimes exceed the heat pump 104 F upper entering temperature limit. When this occurs, the cooling tower will operate to cool the fluid entering the heat pumps, Point 3, down to the 104 F upper temperature limit. 

6. The thermal energy dissipated by the cooling tower is determined for every hour of the year that it needs to operate to keep the heat pump EFT from exceeding the 104 F upper limit. 

7. The hourly electricity consumption of the heat pumps is estimated based on the heat pump COP curves as a function of heat pump EFT. 

8. The size of the auxiliary cooling unit is estimated based on the maximum value of cooling required over the year. The cost of this unit is estimated based on its size and added to REopt’s objective function. 

9. The electricity consumption of the auxiliary unit, the cooling tower in this example, is determined by its efficiency and is added to the facility’s energy consumption. In this example, the electricity consumption of the cooling tower is added to that of the heat pumps and fluid circulating pumps to get a total hourly energy consumption profile for the GHP retrofit. 

114 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

An ‘Auxiliary unit capacity sizing factor’ is included as a user input to increase the capacity of the auxiliary boiler or cooling tower above the size required as determined from the dispatch. With this factor set to 1.0, the total installed capacity of the auxiliary unit would be set to the maximum of the hourly heat added by the boiler or dissipated by the cooling tower. A factor above 1.0 ensures additional capacity is included and costed. The sizing factor is included because auxiliary unit operation in REopt is based on the average of the hybrid GHX dispatches across the simulation period while the maximum auxiliary heat input or dissipation is likely to occur in the last year of the GHX’s useful life. The default value for the ‘Auxiliary unit capacity sizing factor’ 1.2 provides a 20% factor of safety on sizing. 

Default efficiency of the auxiliary cooling tower and boiler are provided in Table 33. 

**Table 33. Default values for auxiliary heat exchange units** 

|Auxiliary Unit Type|Efficiency|
|---|---|
|Electric boiler|98%|
|Cooling tower|0.02 kW electric / kW thermal|



The auxiliary boiler is assumed to be electric. Its default efficiency is 98%. The user can adjust this value. 

The energy intensity of the cooling unit is a user input while the default value assumes a closedcircuit cooling tower with propeller fans. The default value has been selected in consultation with ASHRAE 90.1-2019 Table 6.8.1-7 _Performance Requirements for Heat Rejection Equipment – Minimum Efficiency Requirements._ For a closed-circuit cooling tower, the maximum energy intensity in the reference for heat dissipation is 1 hp of fan and pump loads per 16.1 gpm fluid being cooled at rated conditions[27] . Using this requirement at stated design conditions and converting units, the maximum energy intensity by ASHRAE is 0.026 kWe/kWt. This includes fan and spray pump power. A value of 0.02 kWe/kWt is the default value in REopt. This parameter can be modified by the user. 

We ignore any additional pumping power for pumping heat exchange fluid through the auxiliary heat exchange unit since it would be a small incremental contribution to the total pumping power already estimated for the ground heat exchanger and building interior loops. 

Note: There is considerable literature about optimal design and operations of hybrid GHX systems. For example, one reference[28] describes a hybrid GHX system where the auxiliary unit is installed upstream of the GHX rather than downstream as described as the approach taken for REopt. That reference also describes a complex operation of the auxiliary unit and GHX based on heat pump leaving fluid temperatures, outdoor temperature, whether in heating or cooling mode, etc. Due to both the limitations of core 

> 27 102F entering fluid, 90F leaving fluid, 70F dry bulb air temperature 

> 28 Hackel, Scott, Gregory Nellis, Sanford Klein; _Optimization of Cooling-Dominated Hybrid Ground-Coupled Heat Pump Systems_ ; ASHRAE Transactions, 2009, volume 115, part 1. 

115 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

REopt formulation as well as the GHX model sourced from TESS, ‘optimal’ hybrid design, configuration, and operations cannot be assured in REopt. 

## **18.6  Efficiency Gain of Replacing VAV HVAC Equipment with GHP** 

There are inherent inefficiencies in facilities with variable-air-volume (VAV) HVAC systems that result from the need to supply air from a central air handling unit to serve the worst-case cooling need of one of the HVAC zones. As a result, facilities with VAV systems, the cooling system often generates more cooling than is required to serve the conditioned spaces and ventilation air. And the heating system often generates more heating than is required to serve the zones and ventilation air. With a GHP retrofit of a facility with VAV HVAC, elimination of the VAV system can reduce total system heating and cooling loads. 

In the REopt web tool, we allow this potential reduction in heating and cooling loads to be considered. Because the REopt tool is not a building energy model, the potential heating and cooling reductions for facilities with VAV retrofits are model inputs. It is up to the user to determine whether the facility being screened includes VAV, and therefore might have a reduction in total system heating and cooling loads, and if so, how much those loads might be reduced. 

To provide some estimates of potential reductions in heating and cooling loads, the REopt web tool includes default heating and cooling ‘thermal efficiency factors’ that users can apply in GHP retrofit analysis for facilities with VAV HVAC. 

Default values were determined by performing a rigorous analysis of the DOE commercial reference building models[29] . It is important to note that these efficiency factors are based only on the models and that a careful review of assessed facility and potential thermal efficiency gains is required beyond the screening level of analysis that is possible within the REopt web tool. 

Table 34 shows the default thermal efficiency factors in percentage (%) included in the REopt web tool. The factors are automatically included for analyses where the user leverages the DOE commercial reference building loads as described in Section 7 Loads. Only DOE commercial reference building models that include VAV systems have a non-unitary correction system and therefore are included in the table. For non-VAV facilities, the correction factor should be 1.0, meaning no reduction in heating and cooling system loads is expected with GHP retrofit. 

> 29 See Section 7.2 for additional information on the DOE commercial reference buildings and how they are leveraged in the REopt web tool. 

116 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 34. Default thermal correction factors in percentage (%) by climate zone and building type** 

|Building<br>Type|Thermal<br>Load|1A|2A|2B|3A|3B|3C|4A|4B|4C|5A|5B|6A|6B|7A|8A|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Large Office|Heating|63|33|62|65|83|49|73|94|91|97|97|98|97|98|99|
||<br>Cooling|50|50|40|46|39|34|44|38|33|38|38|38|36|36|31|
|Medium<br>Office|Heating|70|55|58|81|78|46|88|92|88|97|96|98|97|98|99|
||Cooling|67|63|59|59|55|43|57|56|38|49|56|49|50|46|40|
|Primary<br>School|Heating|87|93|78|98|88|76|99|95|94|98|97|99|98|99|99|
||Cooling|88|88|79|85|74|63|85|72|58|72|75|73|72|72|64|
|Secondary<br>School|Heating|93|97|88|99|95|88|100|98|98|99|99|99|98|99|99|
||Cooling|92|92|88|90|86|75|90|86|75|79|83|76|76|71|59|
|Hospital|Heating|76|65|66|62|72|62|67|79|82|85|84|87|88|89|93|
||Cooling|74|73|68|69|68|63|69|71|70|70|73|70|74|71|73|
|Outpatient|Heating|99|89|83|86|87|79|71|89|88|92|92|94|94|95|97|
||Cooling|84|85|77|81|77|70|69|76|73|74|77|75|76|75|73|
|Large Hotel|Heating|100|93|84|95|91|84|98|95|95|99|97|99|98|99|99|
||Cooling|91|92|87|87|83|81|88|80|82|85|79|82|81|80|77|



For more detailed discussion of the methodology and assumptions used to generate the default thermal correction factors, see Appendix B. 

## **19 Air-Source Heat Pumps** 

Air-source heat pumps (ASHP) can be used to provide space heating, space cooling, and/or domestic hot water (DHW) heating. In REopt, ASHP can be evaluated for: 

1. Space heating only 

   - a. To electrify gas-based heating systems, while not modifying the cooling system (chillers and direct-expansion air-conditioners are already types of heat pump) 

2. Space heating and cooling 

   - a. A single ASHP system can offer both heating and cooling, operating in one mode or the other at any given time; modular central or distributed ASHP may supply heating and cooling at the same time. 

3. All three loads, including DHW. 

   - a. DHW ASHP systems, referred to in REopt as ASHP Water Heater, is typically a separate system which is integrated with hot water storage tanks. These could be in a central plant or distributed throughout the facility. 

   - b. This is included as a “sub-technology” which is enabled to be selected after ASHP is selected. Note, for commercial buildings, the DHW heating load is typically _much smaller_ than the space heating load. 

There are multiple configuration options for heat pumps in REopt, described later in this section. The configuration that the user should choose depends on the type of existing HVAC system 

117 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

they have, whether the goal of the ASHP retrofit is to electrify heating loads, and if they want to either supplement or completely replace the existing HVAC systems. 

## **19.1 Background to building HVAC systems and scope of ASHP in REopt** 

REopt is not a physics-based building energy model, so the heating and cooling loads must be input by the user. The user can leverage the DOE Commercial Reference Building profiles (prerun building energy models) available in the tool to scale the user’s annual or monthly energy into an hourly profile, or they can upload a year-long hourly profile directly into the tool. It is common to evaluate energy efficiency measures along with ASHP retrofits in order to “rightsize” ASHP to avoid oversizing and using more electricity for ASHP to serve the heating and cooling loads than needed. This is currently outside of the scope to evaluate directly in a single REopt run, but the user may consider evaluating ASHP with modified heating or cooling load profiles which represents the energy efficiency measures, to look at the impact of ASHP economic and emissions outcomes. 

Two common types of HVAC systems for commercial and industrial facilities include **centralplant** variable air volume (VAV) systems and **distributed** units, both for space heating and/or cooling and water heating. REopt’s ASHP assumes that in a retrofit, the existing HVAC system is replaced by a similar type of ASHP system. Note REopt’s ASHP model currently focuses on commercial and industrial applications and may be less applicable (at this time) for residential applications. 

Two example VAV HVAC systems are illustrated by Figure 21. On the left, the cooling is provided by a chiller heat exchanger in the main air handler, shown in blue, while the heating is provided by a boiler distributing hot water to “reheat” coils in the terminal VAV boxes which control the air flow and reheat needed to maintain the temperature and required ventilation. On the right, the system shows both a chiller _and hot water heat exchanger_ in the central air handler unit to provide cooled or heated air to all the zones throughout the facility; there may also be additional heating coils within the VAV boxes for further reheat control. These central plants are typically located on the ground-level, basement, or on the roof of the facility. 

**==> picture [152 x 197] intentionally omitted <==**

**==> picture [314 x 170] intentionally omitted <==**

118 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **Figure 21. Diagram of two example central-plant HVAC systems for heating and cooling; on the left, the heating is provided solely in the terminal VAV boxes, while on the right, there is heating coil in the central AHU.** 

Another common type of HVAC system for commercial and industrial facilities is **distributed** units. The most common type of distributed system is where all the equipment is packaged within containers which sit on the roof, and they deliver heated or cooled air to zones or sets of zones within the facility; these are called packaged roof-top units (RTU). A less-common type of distributed system is multi-split where just the outdoor units which contain the air-to-refrigerant heat exchanger and compressor are outside (could also be on the roof), and the ODU supplies refrigerant to the indoor-units (IDU) which are located inside the building. Figure 22 illustrates the concepts of packaged RTUs which each serve specific zones of the building; in the illustration, the system is providing cooling (dashed blue) to the space by cooling a mixture of the warm return air (dashed orange) from the space with new outside air for ventilation. 

**==> picture [468 x 221] intentionally omitted <==**

**Figure 22. Illustration of roof-top unit HVAC systems, each of which are serving specific zones** 

Heat pump water heaters are typically separate systems from the heat pumps that provide space heating and cooling (Ref https://www.pmengineer.com/articles/96733-heat-pumps-maximizeefficiency-combining-hot-water-and-space-heating). Water heaters are “heating only”, and the heat pump either directly or indirectly (through a heat exchanger) dumps heat into a storage tank. In the example illustration of a central hot water heat pump system in Figure 23, hot water from the primary storage tanks are fed into “swing” tanks (could be in the central plant location or distributed throughout the facility) that provide temperature control for the water which is delivered to the end-use of the domestic hot water. 

119 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [426 x 294] intentionally omitted <==**

**Figure 23. Example diagram of ASHP water heater, including water storage tanks and piping.** 

In REopt, the storage aspect of the ASHP water heater systems is not explicitly modeled, unless the user models the hot water TES with ASHP water heater. The ASHP water heater is sized based on the peak domestic hot water load that it serves. In reality, there is a design trade-off between storage tank size and the “recovery rate” (the speed at which the ASHP can heat the tank back up) of the ASHP water heater that may allow a smaller heat pump size at the expense of larger storage tanks. If the user would like to consider specific ASHP water heater systems with known storage and recovery rates, along with an understanding of the DHW load profile, the user may input a “sizing factor” of less than one (reduces cost proportionally) to estimate to benefit of not requiring the heat pump capacity to directly serve the DHW load. Alternatively, the user may evaluate Hot Water TES separately along with ASHP Water Heater. However, REopt currently does not restrict any technology, including ASHP for space heating, from charging the Hot Water Storage, so it would allow that system to also arbitrage heat energy to/from Hot Water Storage which may not be practical or desired if it is a separate system. 

For the purposes of evaluating ASHP in REopt, it is assumed that the retrofit of the existing HVAC system is replaced by a similar type of ASHP system. For a facility with a central-plant HVAC system, the retrofit is assumed to be a central-plant ASHP system that distributes cooled air for cooling and either 1) hot water or refrigerant to terminal AHUs for heating, or 2) heats the air directly in the main AHU, to either supplement (configurations 1 and 3, described below) or 

120 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

replace (configurations 2 and 4, described below) the existing chiller and boiler systems. For distributed systems, it is assumed that the ASHP retrofit is an equivalent packaged RTU or multisplit system that replaces the gas-fueled furnace or boiler with a heat pump; this type of system would typically be a _full replacement_ , so configuration 4 is the most applicable choice. 

Similarly, for the ASHP water heater, the retrofit is assumed to replace a similar configuration gas-fueled boiler and storage tank system, whether centralized or distributed throughout the facility. If there is a significant retrofit which changes the architecture of the HVAC system and requires significant additional piping, ducting, electrical, etc, then the user may consider increasing the installed cost input to account for those additions. 

The user has the option to evaluate and **hybrid system,** where the existing heating and cooling systems supplement and provide back-up to the new ASHP system, or **full replacement** of the existing HVAC system. The hybrid configuration options have an incremental O&M cost for ASHP because the site would have two systems, while the full replacement assumes the O&M for ASHP is the same as the system it’s replacing, i.e. zero incremental O&M cost. The configuration options for fully replacing the existing system includes a sizing factor (which adds to the installed cost) and back-up resistive heating equipment, by default. The default cost and performance values for each configuration are listed later in this section. 

## _Configuration options_ 

## 1. Hybrid heating (default selection) 

- a. Use the ASHP for space heating only, keep existing boiler as supplemental and backup. Keep the existing cooling system as the primary cooling system. b. The ASHP capacity and dispatch are determined based on **costoptimality** . 

c. The default minimum non-zero ASHP system size that REopt can choose is 50% percent of the required capacity to replace the full heating system, in order to prevent REopt sizing an insignificant and/or impractical ASHP size for the hybrid system. 

d. This is the default configuration based on discussions with C&I HVAC applications experts which believe it will offer the most cost-beneficial solution when supplementing the existing system. It also reduces the complexity of ASHP sizing based on heating alone, with the most important emissions benefit to electrify gas-based heating. 

2. Full replacement heating 

a. Use ASHP for space heating only, remove existing boiler and replace completely with ASHP, and use integrated resistive heating as supplemental and backup. Keep the existing cooling system as the primary cooling system. b. The ASHP capacity is determined based on the capacity to replace the full heating system. This is a “forced in” capacity and **is likely not as costeffective** as a hybrid heating solution (but could be compared to full boiler replacement costs; see below). 

c. If the current HVAC system of the facility is packaged RTUs to serve heating and the user wants to evaluate an ASHP RTU retrofit, choose this option. 

121 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

d. A default sizing factor of 1.1 of the peak heating load is used to provide a capacity safety-factor on the design of the system, with the assumption that the capacity need may be larger than the modeled loads. 

3. Hybrid heating and cooling 

   - a. Space heating and cooling, keep existing boiler and chiller as 

   - supplemental and backup. 

   - b. The ASHP capacity and dispatch are determined based on **costoptimality** . 

c. The default minimum non-zero size that REopt can choose is 50% of the required capacity to replace the full heating and cooling systems, in order to prevent REopt sizing an insignificant and impractical ASHP size for the hybrid system. 

4. Full replacement heating and cooling 

a. Space heating and cooling, remove existing boiler and chiller and replace completely with ASHP, use integrated resistive heating as supplemental and backup for heating. 

b. The ASHP capacity is determined based on the capacity to replace the full and cooling heating systems. This is a “forced in” capacity and is likely **not cost-optimal** . 

- c. If replacing a packaged RTU gas furnace/air-conditioner, choose this option for ASHP RTU 

d. By default, a sizing factor of 1.1 of the peak coincident heating and cooling load is used to provide a capacity safety-factor on the design of the system, with the assumption that the capacity need may be larger than the modeled loads. 

Figure 24 illustrates the concept of the hybrid configurations (1 and 3, with the cooling system only included for 3) and full replacement configurations (2 and 4, with the cooling system only included for 4). The orange boxes indicate new ASHP equipment. The dashed red and blue lines indicate the supply and return of either water or air, depending on the type of HVAC system being retrofitted. The ASHP Water Heater (optional to evaluate) is sized and operates independently of the space heating and cooling ASHP system, and the hot water (only) is indicated by the solid red line. 

122 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [468 x 236] intentionally omitted <==**

## **Figure 24. Diagram illustrating how ASHP integrates with the existing HVAC system depending on configuration. The orange boxes highlight new ASHP equipment.** 

For a centralized VAV system, the ASHP in cooling mode would cool the air in the central air handling unit to provide cold air throughout the facility. For heating mode, the ASHP could either heat the central air with condensing unit in the central AHU, it could send superheated vapor refrigerant to heat air directly in the terminal AHU (distributed heat pumps with variable refrigerant flow), or it could heat up water in a central heat exchanger and send hot water to terminal AHUs for heating the zones. The latter two options could also be used for reheating air for zones which would otherwise be over-cooled during the cooling season or for ventilation needs. 

For hybrid configuration 3, if there is both heating and cooling loads _at the same time_ , the existing boiler or chiller will typically serve the lesser of the two loads to avoid adding additional ASHP capacity to serve that load. However, the economics or emissions reduction goals may drive the solution toward sizing the ASHP larger to serve both loads. 

For full replacement configuration 4, the ASHP system is assumed to be made up of multiple modular units which can operate in either heating or cooling mode. If there is both heating and cooling load in the same time step, it is assumed that there is enough capacity to provide each of the loads, and REopt sizes the ASHP system based on the peak capacity to serve the total coincident heating and cooling load. For example, if the peak heating load is 100 ton, but there is also a time where the heating load is 90 ton and the cooling load is 30 ton, the total heat pump capacity is sized to 120 ton in this case (ignoring capacity factor impacts from outdoor air temperature). 

123 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **19.2 ASHP Cost Model** 

ASHP retrofit costs include capital costs and O&M costs. The capital cost represents the fully burdened installed cost, including both equipment and labor. Retrofit costs for ASHP are highly variable and will depend on the site-specific details of the existing HVAC infrastructure. An estimate of **$2,250/ton** for the installed cost of the ASHP retrofit is provided as a default for screening level analysis. However, costs and performance should be developed by ASHP experts after review of the facility’s equipment, configuration, and loads. The default installed cost is based on discussions with multiple vendors to estimate commercial/industrial-scale ASHP equipment cost to be about $1,500/ton along with an estimated installation cost adder of 50% ($1,500 + $750 = $2,250/ton). 

The O&M cost is modeled to represent the _incremental cost difference_ for ASHP HVAC retrofit over the conventional HVAC system it replaces. The O&M costs do not include energy impacts of ASHP retrofit as those are separately accounted for in REopt. For configurations 1 and 3, the default incremental O&M cost for ASHP is **$40/ton/year** because the site keeps the existing HVAC system along with the new ASHP. For configurations 2 and 4, the default incremental cost is **zero** because it assumes there is no difference in O&M compared to maintaining the existing equipment. 

There are no assumed incentives for ASHP. The only available incentive for the user to include is MACRS (but that defaults to zero). If there are incentives available for ASHP, the user may reduce the installed cost input appropriately. 

## **19.3 Considerations based on ASHP configuration** 

## _**19.3.1 Hybrid ASHP considerations (configurations 1 and 3)**_ 

For configurations 1 and 3, assuming the existing heating and cooling systems are still in place, REopt determines the cost-optimal ASHP size which may only serve a small portion of the total heating and/or cooling loads. To avoid REopt sizing an impractically small ASHP system, there is a minimum allowable/non-zero size threshold that can be input in two different ways: 

1. Minimum non-zero size as percent of the full replacement capacity (default) a. This calculates the minimum tonnage required based on the heating and cooling loads, in a preprocessing step. This also accounts for the capacity factors based on the outdoor air temperature profile. 

2. Minimum non-zero size in tonnage 

   - a. This is a user-specified tonnage regardless of the heating and cooling loads 

REopt will only size ASHP to be either 0 ton, if not cost optimal, or greater than the minimum allowable/non-zero size. This is not relevant for configurations 2 and 4 where REopt is required to size and dispatch ASHP to serve all of the heating and cooling loads. 

To “force-in” a minimum size, without the option for REopt to choose zero, the “Minimum size (ton)” system may be used. However, this only forces the capacity, and **not the dispatch** . REopt determines the lowest cost way to serve the loads, and running the existing (natural gas) boiler 

124 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

and/or the existing (water-cooled) chiller may be the lowest cost operation. This can happen for heating when the ASHP COP is lower during colder times and/or when the electricity price is much higher than natural gas. This can happen for cooling when the COP of the existing chiller is higher than the ASHP for cooling. Note, the existing cooling system COP is assumed to be water cooled, with a COP of about 4.5. The default ASHP cooling COP is lower, around 3.0 (but see COP vs OAT below for more details), so the existing chiller will be preferentially dispatched unless the user lowers the existing chiller COP or raises the default ASHP cooling COP. 

The hybrid configuration for heating in particular may be used to represent the opportunity to evaluate a dual-fuel ASHP which would include a gas-furnace/boiler for supplemental and backup heating. While the user does not have control over the dispatch, REopt will generally dispatch the existing gas system at lower outdoor air temperatures and/or high heating loads to avoid low COP and over-sizing ASHP, respectively. The user should consider increasing the installed cost of ASHP to represent the additional cost of that gas supplemental system, if it’s not practical to use the existing heating system. 

## _**19.3.2 Full replacement ASHP considerations (configurations 2 and 4)**_ 

For configurations 2 and 4, it is assumed that if the OAT profile includes sufficiently cold hours of the year, such as below 10 °F by default, then a backup resistive heater with adequate capacity to serve the load, is included in the design. The COP and capacity factor are both assumed to be 1.0 for the resistive heater backup. The user may adjust the temperature threshold (sometimes called the “cutoff” temperature) at which the resistive backup heater kicks on. To model a verycold-climate heat pump which does not require a resistive backup, adjust the appropriate cost and performance table, and reduce the temperature threshold to -50 or something much below the expected OAT at that location. The default capital cost is assumed to include this backup heater, but it may require additional cost depending on the sizing of that which is outside of the current scope of REopt. 

A sizing factor is included as a user input to increase the total capacity of the heat pumps above the peak coincident heating and cooling thermal production. A factor above 1.1 ensures 10% additional heat pump capacity is included based on the expectation that the system should be designed to serve peak loads greater than those input in the heating and cooling load profile inputs. 

There is an input field in the user interface called, ‘Avoided HVAC upgrades ($)’ that has a default value of $0. If the facility of interest has HVAC equipment at or near the end of its useful life and these equipment purchases can be avoided by ASHP retrofit, the user can enter these avoided HVAC equipment costs here. These avoided costs, if entered by the user, will reduce the cost of the ASHP retrofit equivalently and will increase the economic outlook for ASHP retrofit. 

## **19.4 ASHP Performance Model** 

## _**19.4.1 Heat Pump COP and Capacity Dependence on Outdoor Air Temperature**_ 

ASHP coefficient of performance (COP) and capacity to supply heating or cooling energy is known to be dependent on the outdoor air temperature (OAT). The COP determines how much electricity is consumed to produce thermal energy. The capacity factor (CF) is a multiplier on the nominal rated capacity of the heat pump to supply thermal energy, which is less than 1.0 for 

125 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

heating when the OAT is below 47 °F and less than 1.0 for cooling when the OAT is above 95 °F, and it is greater than 1.0 on the other side of that those respective temperatures. 

The COP and CF curves were developed based on performance data from multiple heat pump models from different suppliers. The data were plotted in and linear trendlines were created from these data (See Appendix C: ASHP Performance Data).  An extrapolated range of temperatures were applied with the linear equations to use as the default ASHP performance for COP and CF to estimate the performance lower than (e.g. down to -5°F for heating) and greater than (e.g. up to 110 °F for cooling) the data provided in the specification sheets. Table 35 shows the resulting default data. If the OAT in a given hour is lower or higher than the minimum or maximum provided temperature, then the same COP and CF are applied as those minimum or maximum data points. If the OAT is in between two data points, linear interpolation is used to calculate the COP and CF. 

**Table 35. Default coefficient of performance (COP) and capacity factor (CF) dependence on outdoor air temperature (OAT) for heating and cooling.** 

|**Outdoor Air**|**Heating**|**Heating**|**Outdoor Air**|**Cooling**|**Cooling**|
|---|---|---|---|---|---|
|**Temp. for**|<br>**COP**|<br>**CF**|**Temp. for**|<br>**COP**|<br>**CF**|
|**Heating (°F)**|||**Cooling (°F)**|||
|||||||
|-5|1.5|0.38|70|4.0|1.03|
|17|2.3|0.64|82|3.5|0.98|
|47|3.3|1.00|95|2.9|0.93|
|80|4.5|1.40|110|2.2|0.87|



The user can use the default heat pump performance parameters or model their own. If the user uploads a custom heat pump performance table, the minimum required number of rows is one and there is no upper limit on the maximum number of rows. However, each subsequent row must have OAT greater than the OAT in the previous row. That is, heat pump performance in the table must be entered in order of increasing OAT. The easiest way to ensure the proper formatting is to download the default table in .csv format, modify the data, and upload the table. 

ASHP systems have also may have a “max production” mode for lower temps (for heating) which has a higher CF with a lower COP compared to nominal operating mode at that condition. This may result in less “over-sizing” of the ASHP to operate at lower temperatures. This could be modeled by changing the COP and CF input data, but REopt is not able to apply two different performance values for the same OAT, so the user may have to evaluate the “max production” mode operation in a separate REopt run. Also, the “max production” operating mode may avoid the need for the resistive backup system, which can be evaluated by lowering the resistive heating back-up temperature threshold input along with updating the COP and CF table. 

126 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **20 Concentrating Solar Thermal (CST)** 

Concentrating solar thermal (CST) technology collects solar irradiance and concentrates it to a focal point(s) to produce high temperature thermal energy. Historically, at large scale, this technology has been used to generate electric power by converting the high temperature thermal energy to power in a steam turbine or other conversion device. More recently, and when colocated at a site which uses high temperature energy directly in a process (e.g. chemical plant, food and beverage industries), thermal energy from CST has been used to directly serve that process heat to offset fuel consumption which would otherwise provide the heat. 

Credit is given to the STEP1 Solar Thermal Energy Planner web tool for the development of the CST module in the REopt.jl Julia package, and much of that work was leveraged to enable the representation of CST in REopt. 

## **20.1 Parabolic Trough Collectors for Industrial Process Heat** 

For industrial process heat applications, parabolic trough collectors is the most commercially available CST technology type. More information on this technology can be found on the DOE EERE solar thermal website. 

## **20.2 High Temperature Thermal Energy Storage** 

High temperature thermal energy storage (HT-TES), such as molten salt, is often paired with CST collectors to be able to serve heating load during non-solar hours (i.e. the evening or night). HT-TES is relatively low-cost compared to electric storage options such as Li-Ion batteries because it uses cheaper materials and involves more common construction techniques. HT-TES provides a higher total utilization of the heat produced by CST, and it enables a constant supply of heat to industrial processes which often operate either two or three shifts per day. 

## **20.3 Applications for Heating Loads** 

By default, CST+HT-TES serves the **process** heat load input, and not the space heating or domestic hot water (DHW) heating loads. The user may choose to include those heating loads in the applicable loads that CST may serve. However, it is advised that CST be used to serve higher temperature loads for which the process heat load input is intended; this is because there are lower-cost technologies such as heat pumps available to serve lower temperature heating loads. While other solar thermal technologies like flat plate and evacuated tube collectors may also be more-suited to serve lower temperature heating loads, the REopt model focuses on parabolic trough collectors which are more applicable to higher temperature process heat. 

Figure 4 illustrates an example schematic for a parabolic trough collector solar field with molten salt tanks for the thermal energy storage. The solar field consisting of parabolic trough collectors produces hot oil to either heat the process heating fluid through the boiler or store the thermal energy by heating up the molten salt and storing in the hot (upper) tank. During evening and night hours, the molten salt can heat up the oil to heat the process heating fluid without the solar field. 

127 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [400 x 275] intentionally omitted <==**

**Figure 4. Schematic of a parabolic trough CST with molten salt tank HT-TES system (modified diagram from Alami et al 2023)** 

The REopt model calls NREL’s SAM tool’s SAM Simulation Core (SSC) module to generate a normalized thermal production profile for CST. REopt then determines the cost-optimal size of CST and HT-TES for the site. Documentation for SAM’s CST module can be found on the CST section of the SAM website. 

Default cost and performance values for CST and HT-TES are listed in Table 10 and Table 11. 

## **21 Outputs** 

## **21.1 Cases** 

The REopt web tool reports results for up to three cases: Business-as-Usual, Financial, and Resilience. Resilience is reported only if the user selects a resilience analysis. 

- **Business-as-Usual:** In this case, the site purchases energy solely from the utility. In a scenario modeling a grid outage where the critical load can be fully met by an existing generator for some period of time, then Business-As-Usual also includes the costs of using that existing generation capacity for that time. 

- **Financial:** The case that minimizes the present value of all future energy costs over the analysis period. This case may include a combination of utility, PV, wind, CHP, GHP, 

128 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

chilled water storage, hot water storage, absorption chiller, and/or battery. This case is not optimized for a grid outage. 

- **Resilience:** This case is optimized to sustain a critical load in the event of a grid outage while minimizing the present value of all future energy costs over the analysis period. This case may include a combination of utility, PV, wind, battery, CHP, GHP, chilled water storage, hot water storage, absorption chiller, and/or backup generator. 

## **21.2 System Size** 

The REopt web tool leverages a mathematical optimization model to determine the cost-optimal size and dispatch of DER including PV, wind, CHP, backup diesel generator, absorption chiller, battery, and thermal storage subject to technology costs, the site’s load, cost of electricity and fuel, solar or wind resource, and other financial inputs. 

A technology is typically recommended if it reduces the life cycle cost of energy for the site. In general, DER is often cost effective at sites that have a higher utility rate, higher utility escalation rate, lower DER cost, good incentives, and/or good renewable resource that make energy generated by DER less expensive than energy purchased from the utility. For CHP, the combination of high electric rate, low fuel cost, and high thermal load can make electricity generated by CHP less expensive than electricity purchased from the utility and heat generated by CHP less expensive than heat produced by the existing boiler. For batteries, high demand charges are important for economic viability. Thermal storage is often cost effective at sites where thermal energy is produced at a different time than when it is needed. An absorption chiller may be cost effective at sites that have a high cooling load, high electricity costs, low fuel costs, and/or CHP. 

If DER is not recommended, this is likely because utility costs, incentives, and/or renewable resources are low, and therefore DER may not be cost competitive with utility prices at this time. The cheapest option might be to continue to purchase grid electricity. On the other hand, if the model over-sizes a technology, resulting in energy curtailed or sent back to the grid at no value, this is likely because the value it gains from energy generated at other times reduces total life cycle cost of energy, even if energy is curtailed in certain hours. 

If the user specified a minimum DER size or a resiliency requirement, DER may be recommended to meet these requirements even if it does not reduce the life cycle cost of energy. If the user did not select a technology for inclusion in the analysis, or set the maximum technology size to zero, the technology will not be recommended even if it is cost effective. The total system size includes an existing system if one has been specified in the inputs (for PV and diesel generator). 

With the exception of GHP, the model considers a continuous range of technology sizes; it is not limited to the discrete sizes available in the marketplace. Therefore, the system sizes recommended may not be commercially available. In this case, the user may identify available sizes close to the optimal recommendation and rerun the model with fixed sizes equal to the commercially available size. 

129 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## _**21.2.1 Energy Production**_ 

In addition to system size, the REopt web tool also reports energy generation from each technology, and fuel used to generate this energy (where applicable). The expected annual energy production from the PV system is the average expected production over the system lifetime (including degradation), not Year 1 production. 

## **21.3  Dispatch Strategy** 

The model optimizes the dispatch strategy of each technology to meet the load at minimum life cycle cost of energy. In each time step, generation may serve the load, or be stored, curtailed, or, in the case of electricity, exported back to the grid. Storage technologies may be charged or discharged. The dispatch strategies for electric, heating, and cooling loads are provided in interactive graphs that allow the user to scroll through the year, zoom in on select days, and zoom out to see the full year. The full hourly dispatch strategy for one year can be downloaded as a .csv file. 

## _**21.3.1 Electric Dispatch**_ 

For every hour of the year, the electric dispatch chart titled System Performance Year One shows the electric load as a black line. For evaluations that include chilled water TES or an absorption chiller, a dashed black line represents the business-as-usual electric load, which was entered by the user. The total electric load, shown as the solid black line, is the net of this business-as-usual load and any cooling electric offsets or additions due to recommended absorption chiller and/or chilled water TES systems. This net total electric load is the load that must be met by some combination of technologies in every hour of the year. 

The load must be met in each hour by either energy purchased from the grid, PV, wind, battery storage, CHP, or, in an outage, by an optional backup diesel generator. PV and wind generate energy according to when the resource is available and either serve the load, charge the battery, or export to the grid. CHP generates energy according to site economics and either serves the load, charges the battery, or exports to the grid. Load not met by PV and/or wind is met either by the CHP prime mover, the battery discharging, the grid, or, in an outage, by an optional backup diesel generator. During a grid outage, excess generated electricity is curtailed. 

The optimization model decides whether to charge, discharge, or do nothing with the battery in each hour. If it charges or discharges, it also decides by how much. The battery SOC is shown as a dotted black line. The battery is sized and dispatched to minimize the life cycle cost of energy at the site. There is no demand target. Instead, demand levels are determined by the optimization model. 

## _**21.3.2 Heating Thermal Dispatch**_ 

A similar chart is provided for the heating thermal dispatch. The business-as-usual heating load is shown as a dotted black line. This heating load represents the typical heating boiler fuel load entered by the user. It does not include the hot water TES or absorption chiller loads which are included in the total heating load, shown with a solid black line. 

The load must be met in each hour by either the existing boiler, CHP, or hot water TES serving the load. The CHP generates heat and the hot water TES stores and releases heat according to 

130 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

site economics. Both CHP and hot water TES either serve the load, charge the TES, or supply heat to an absorption chiller. The hot water TES state of charge in each hour is represented by a dotted red line. 

Like the battery, the optimization model decides whether to charge, discharge, or do nothing with the hot TES in each hour. If it charges or discharges, it also decides by how much. The TES is sized and dispatched to minimize the life cycle cost of energy at the site. 

## _**21.3.3 Cooling Thermal Dispatch**_ 

Finally, a third chart is provided for the cooling thermal dispatch. For every hour of the year, the chart shows the total cooling load as a solid black line. This load must be met in each hour by either the electric chiller, the absorption chiller, or the chilled water TES. The absorption chiller and electric chiller either meet the load or charge the chilled water TES according to site economics. The chilled water TES state of charge in each hour is represented by a dotted red line. 

The optimization model decides whether to charge, discharge, or do nothing with the chilled water TES in each hour. If it charges or discharges, it also decides by how much. The TES is sized and dispatched to minimize the life cycle cost of energy at the site. There is no demand target; demand levels are determined by the optimization model. 

## **21.4 Economics** 

The REopt web tool reports economic metrics on the financial viability of each case. Metrics reported include Year 1 utility costs before tax, life cycle utility costs after tax, capital cost before and after incentives, Year 1 and life cycle O&M costs, total life cycle cost, NPV, payback period, internal rate of return, and technology-based levelized cost of energy. For third partyfinanced systems, annual payments from the host to the third-party owner are also reported. More detailed financials are available in the downloadable pro forma spreadsheet. 

The objective of the optimization is to minimize life cycle cost (and therefore maximize NPV). The life cycle cost is the present value of costs, after taxes and incentives associated with each case. For the Business-as-Usual Case, this includes only the utility demand and energy costs, existing boiler fuel costs, and future O&M costs for any existing PV and/or generator. In a scenario where a critical load is fully met by an existing backup diesel generator, then this calculation also includes the fuel and operating cost of using that existing generation capacity to meet the outage. For the Financial or Resilience cases, this includes the utility demand and energy costs as well as the capital expenditure, tax benefits and incentives, and O&M costs associated with the project, including PV, wind, energy storage, CHP, GHP, absorption chiller, and total backup diesel generator (if recommended). Note that fixed fees charged by the utility are not always included, and therefore the actual life cycle cost of energy may be higher if the utility charges fixed fees. However, because fixed fees cannot be offset by PV, wind, energy storage, or CHP, these net out in the calculation of NPV. 

The NPV is the present value of the savings (or costs if negative) realized by the project. This is calculated as the difference between the Business-As-Usual Case life cycle energy cost and the Resilience Case or Financial Case life cycle energy cost. For financial analysis, NPV will be 

131 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

greater than or equal to zero, unless the user has forced a minimum technology size. For a resilience analysis, the NPV may be positive or negative. A negative NPV indicates the project is not economically viable, or in other words, the site will pay more than their base case cost of electricity. Note that avoided outage costs are not considered in the NPV calculation; adding in these avoided costs may increase NPV. 

While the REopt web tool reports payback period and IRR as well, the optimization does not maximize these metrics. The REopt web tool is maximizing NPV, and IRR and payback period are simply calculated for the system that maximizes NPV. 

## **21.5 Resilience** 

If the user selects a resilience evaluation, the REopt web tool optimizes the system to meet the typical load at minimum life cycle cost, with the additional constraint that the load must be met without the grid during the specified outage periods. The results then compare the system optimized for resilience to one optimized for financial benefit. In addition, users can access the Energy Resilience Performance (ERP) tool on the results page. The optimization result assumes DER are available at the start of the outages and will not fail during the outage. The ERP allows the user to evaluate REopt’s optimization architecture with real-world reliability performance values for different DER types. 

## _**21.5.1 Resilience vs. Financial Comparison**_ 

The Resilience vs. Financial Comparison table shows the architecture and cost differences between the Resilience system and the Financial system that does not consider resilience requirements. The DER technologies selected for the Resilience system and their sizes assume they are 100% available and reliable. To evaluate the probability of serving critical load considering variable reliability and for all possible outages in a year, run the ERP which is accessible on the REopt results page in the Energy Resilience Performance Tool section. 

## _**21.5.2 Energy Resilience Performance Tool**_ 

When running resilience analyses in REopt, the optimization solution assumes that the assets for serving critical load during a grid outage are functional and will be 100% reliable for the duration of the outage. The resilience solution also only considered the outage periods entered on the REopt inputs page. In the real world, an outage can occur at any time of the year. And equipment can be down for service when needed or fail unexpectedly when operating. The ERP tool is provided for users to post-process REopt optimization results to assess the probability of serving critical load during a loss of grid power across all hours of the year and considering equipment reliability. Additionally, users can use the ERP to explore how modifying the microgrid architecture and fuel storage reserve capacity might increase or decrease the probability of serving critical load during a loss of grid power. Default reliability parameters are provided for DER and users can also change these parameters to see how results change if equipment reliability is better or worse than the default values. 

Here we define reliability as the probability that the system of DERs identified for backup power will successfully serve the critical load for the outage duration selected by the user. Probability analysis includes consideration of the availability of the DER at the start of the outage, 

132 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

probability of failure to start, and probability of failure to run during the loss of grid power for emergency diesel generators, prime power, CHP, solar PV, wind turbine generators, and BESS. 

The ERP reliability analysis post-processes the optimization results. The optimization by REopt, in determining sizing and life-cycle costs, etc., assumes DER are 100% reliable and available. The relationship and structure of the ERP reliability analysis to the optimization is illustrated in Figure 25. 

**==> picture [446 x 170] intentionally omitted <==**

**Figure 25. Relationship and workflow between REopt techno-economic optimization and the Energy Resilience Performance tool accessible on the REopt results web page.** 

In the figure, ‘Optimization’ describes the REopt optimization baseline model. 

The ERP reliability analysis approach is based on work by Marqusee et al[30] . It estimates the probability of the system of DERs to serve critical loads based on the individual DERs’ reliability, availability, and fuel limitations. It calculates the probability of the system meeting 100% of the critical load for every time step of an outage that can start at any time step of the year based on DER reliability. 

System level reliability is modeled using a Markovian approach. Markovian analysis uses failure behavior of individual components to determine the probability that the overall system will transition from one state of operation to another. 

The ERP requires a small set of inputs, in addition to those used and generated from the optimization. In addition to the data passed from the REopt optimization, the ERP requires the number and sizes of emergency backup generators, prime generators, and CHP generators. The ERP allows the user to match, reduce, or increase DER capacities determined by the REopt optimization. Most DERs come in a limited number of sizes and the ERP allows the user to 

> 30 Jeffrey Marqusee, William Becker, and Sean Ericson, “Resilience and Economics of Microgrids with PV, Battery Storage, and Networked Diesel Generators”, Advances in Applied Energy, 3, 10004, 2021 and Jeffrey Marqusee, Sean Ericson, and Donald Jenket, “Impact of Emergency Diesel Generator Reliability on Microgrids and BuildingTied Systems”, Applied Energy 285, 116437 (2021). 

133 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

recognize this practical constraint. In addition, many users desire or require an additional emergency generator beyond the minimum number needed to provide enhanced system level reliability. This is sometimes called ‘N+1’ reliability requirement. These size and required capacity scenarios can be analyzed using the ERP. 

Because the user can change the capacity of the DERs from the REopt optimized capacities, an option to rerun the REopt optimization is provided in the ERP tool to determine a new optimized dispatch strategy and life cycle cost. 

**WARNING** : Changing the system architecture, emergency generator fuel reserve, and reliability metrics in the ERP for exploring impacts on reliability DOES NOT update the techno-economic optimization results displayed on the REopt results page. If the user identifies a modification to the optimization results of interest that they would like to reevaluate for economics, emissions, or other metrics, the user should use the ‘Copy ERP Inputs to Re-Run REopt’ button and re-run the techno-economic optimization. If the number or unit size of an emergency generator, prime generator, or prime mover has changed the cost and performance per kW and minimum electric loading may also need to be modified. 

Quantitively calculating the reliability of a backup power system requires estimates for the key reliability metrics of each DER. REopt default reliability estimates are derived from empirical data when available and supplemented by modeling results when needed. These estimates are documented in an NREL report[31] . These reliability estimates are for the DERs ability to provide power during a grid outage ranging from minutes to four weeks. 

The table below lists the DERs modeled in the ERP. 

> 31 Marqusee, Jeffrey and Andrew Stringer. 2023. Distributed Energy Resource (DER) Reliability for Backup Electric Power Systems. Golden, CO: National Renewable Energy Laboratory. NREL/TP-7A40-83132. https://www.nrel.gov/docs/fy23osti/83132.pdf. 

134 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **Table 36. DER modeled in ERP** 

|**DER**|**Type & Fuel**|
|---|---|
|Emergency Generator|Packaged Diesel|
|CHP|Reciprocating Natural Gas Engine|
||Natural Gas Turbine|
||Microturbine|
||Fuel Cell|
|Prime Generator|Reciprocating Natural Gas Engine|
||Natural Gas Turbine|
||Microturbine|
||Fuel Cell|
|Solar Photovoltaics|Silicon|
|Wind Turbine|NA|
|BESS|Stationary Li-ion|



## _**21.5.3 Modeling Approach in Energy Resilience Performance Tool**_ 

A description of the modeling approach in the ERP is given in this section. The cited works describe the modeling approach in greater detail. 

The key assumptions and simplifications for the ERP include: 

1. The assumed approach is valid for grid outages up to four weeks in duration. 

2. All critical loads must be served. If there is insufficient energy available to meet the load in any timestep, the system fails. 

3. Only the reliability of the DER is modeled. Reliability of the distribution network, switchgear, transformers, etc., are not assessed. 

4. Outage durations are constrained to be no longer than four weeks. 

5. Renewable resources are perfectly predicted. Uncertainty of renewable resources is not assessed. 

6. The ERP tool does not consider the repair of failed DERs[32] . If an asset fails during a grid outage, it is assumed to remain off-line for the duration of the outage. 

> 32 Under “blue sky” conditions repair times are measured in days. During a “black sky” event, such as a multi-day grid outage, it is unlikely that parts and staff with appropriate expertise will be available in the same amount of time. In modeling an extended grid outage, a failed DER is assumed to remain offline until grid electricity is restored. This assumption breaks down for outages longer than a few weeks. 

135 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

7. Regardless of the minimum state of charge constraint the user might have used for the REopt techno-economic optimization, the ERP assumes that during grid outages the full energy capacity range of the battery is useable to serve critical loads. Therefore, the allowable minimum state of charge in the ERP dispatch is 0%. 

DER ability to reliably serve critical load is determined by: 

- Mean Time to Failure (MTTF) – the mean time to failure as a function of run time. 

- Operational Availability (Ao) – The probability that at the time the outage starts the DER is available to operate (it is not offline due to maintenance or repairs). 

- Failure to Start (FTS) – Failure of DER to start from a cold state. 

- Fuel Limitation – Finite diesel fuel supply limits the DERs runtime. 

- Fuel Availability – Probability that natural gas pipeline delivery is available at the start of the power outage. 

The two required metrics for assessing the performance of backup power systems for all DERs are reliability and availability. 

_Reliability_ is defined as the ability of a component to perform the required functions under stated conditions for a stated period. Reliability is typically high during the early hours of a grid outage when backup power is initially required but declines as the length of the outage increases and the probability grows of a DER failing to provide power. Reliability is useful for assessing the risk of experiencing a failure over a specified time interval but does not account for the expected downtime associated with that failure. 

There are two metrics for measuring failure rates. One based on the number of failures during a DERs lifetime, and one based on the number of failures during a DERs run time. The reliability literature is not consistent on its terminology. In the ERP we call these the Mean Time Between Failures (MTBF) and the Mean Time to Failure (MTTF) 

**==> picture [158 x 30] intentionally omitted <==**

And 

**==> picture [236 x 31] intentionally omitted <==**

MTTF must be used when considering backup power systems. Prime generators only run between 30% to 80% of the time in almost all locations because of economic conditions. Emergency generators are run even less often, usually less than 100 hours per year. Measuring run time failures (MTTF) as opposed to annual frequency of failures (MTBF) isolates the generator’s reliability from its frequency of use. 

136 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

_Availability_ is defined as the ability of an item to perform its required function when called upon at the start of an outage. Essentially, availability is a measure of the percentage of “potential uptime” as opposed to the actual “uptime” for a DER over a year. For example, solar PV generates electricity only during sunlight hours however its availability includes all hours, even nighttime hours, that the system is in working order. 

8760 −ℎ𝑔𝑔𝑜𝑜𝑔 𝑔𝑔𝑜 𝑜 𝑔 𝑝𝑝𝑔 𝑦𝑦𝑔 𝑔𝑔 𝑑𝑑𝑜𝑜𝑔𝑔 𝑔 𝑔 𝑝𝑝𝑔𝑔𝑜𝑜𝑔 𝑔 𝑑𝑑 𝑚𝑚𝑔𝑔𝑜𝑜𝑔 𝑔 _Annual_ 𝐴 𝑓𝑓𝑙 𝑓𝑓𝑛𝑛𝑙 𝑙 𝐴𝐴= 8760 

For assessing availability of DERs for backup power, “potential uptime” is not the same as runtime. DERs are often not in operation due to economic or market constraints. Their availability to provide backup power at the start of an outage is not limited due to grid-tied economic constraints. 

There are two principal measures of availability used in the literature: inherent availability (Ai), and operational availability (Ao). 

**Inherent availability, Ai:** When only reliability and corrective maintenance or repair (i.e., design) effects are considered, we are dealing with inherent availability. This level of availability is solely a function of the inherent design characteristics of the system. 

**Operational availability, Ao:** Availability is determined not only by reliability and repair, but also by other factors related to preventative or corrective maintenance and logistics. When these effects of preventative and corrective maintenance and logistics are included, we are dealing with operational availability. Operational availability is a "real-world" measure of availability and accounts for delays such as those incurred when spares or maintenance personnel are not immediately at hand to support maintenance. 

ERP uses operational availability to quantify the probability a DER will be unavailable at the start of a grid outage and assumes during a grid outage that no routine maintenance activities will take place. 

Operational availability can be directly measured or calculated by: 

**==> picture [135 x 30] intentionally omitted <==**

Where MTTR is the Mean Time to Repair, MTTM is the Mean Time to Maintain, and MTBM is the Mean Time Between Maintenance events. Unlike reliability, MTBF must be used as opposed to MTTF for calculating Availability. MTTR and MTTM must include the logistical time to bring parts and personnel to the DER. Availability can be low due to frequent failures or maintenance events and/or due to long repair or maintenance times. 

Finally, for DERs that are run very infrequently, such as emergency generators, it is important to understand the Failure to Start (FTS): 

137 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

> [𝑙𝑙𝑛𝑛𝑙𝑙𝑛𝑛 𝑜𝑜𝑙𝑙 𝑙𝑙𝑓𝑓𝑙][𝑛][𝑙𝑙𝑓𝑓 𝑙𝑙𝑜𝑜 𝑓𝑓𝑙𝑙𝑓𝑓𝑛𝑛𝑙𝑙] 𝑀 𝐹𝐹=[𝑛] 𝑛 𝑙𝑙𝑛𝑛𝑙𝑙𝑛𝑛 𝑜𝑜𝑙𝑙 𝑓𝑓𝑙 𝑙 𝑎𝑎𝑙 𝑎𝑎 𝑓𝑓𝑙𝑙𝑓𝑓𝑛𝑛𝑙𝑙𝑓𝑓 

The table below provides the default values for the reliability metrics for each DER modeled. For certain DERs the values are sensitive to the size of the DER and thus we use size-dependent values. 

**Table 37. Default reliability metrics by DER** 

|**DER**|**Type & Fuel**|**Size**|**MTTF**<br>**(hours)**|**Ao **|**FTS**|
|---|---|---|---|---|---|
|Emergency Generator|Packaged Diesel|<4,000 kW|1100|99.5%|0.94%|
|CHP|Reciprocating Natural<br>Gas Engine|< 800 kW|870|96%|0%|
|||>800 kW|2150|98%|0%|
||Natural Gas Turbine|< 5MW|990|98%|0%|
|||>5 MW|3160|97%|0%|
||Microturbine|<500 kW|none|none|0%|
||Fuel Cell|<3MW|2500|90%|0%|
|Prime Generator|Reciprocating Natural<br>Gas Engine|< 800 kW|920|96%|0%|
|||>800 kW|2300|98%|0%|
||Natural Gas Turbine|< 5MW|1040|98%|0%|
|||>5 MW|3250|97%|0%|
||Microturbine|<500 kW|none|none|0%|
||Fuel Cell|<3MW|2500|none|0%|
|Solar Photovoltaics|Silicon|>25 kW|Infinite|98%|0%|
|Wind Turbine|Land based|NA|Infinite|97%|0%|
|BESS|Stationary Li-ion|NA|Infinite|97%|0%|



These values assume the DER is well-maintained. Poor maintenance practices can have large impacts on the DER reliability. For example, a poorly maintained emergency generator can have an MTTF as short as 50 hours. The user can examine the impact of maintenance practices by changing the default MTTF value to one that is much shorter. The sizes listed above are driven by both differences in reliability data and constraints on the availability of commercial system sizes. The default values for MTTF of solar PV, wind turbine generators, and BESS are set to infinity because it is so much longer than the four-week limit on outage duration that it is not necessary to consider run time failures for these technologies. 

Although most causes of a DER failure can be repaired without replacement of the entire system, the tool does not treat reparability during a grid outage. Data on repair times is usually obtained under “blue sky” conditions. That is the repairs have taken place due to failures when the grid is operating and the facility and region around the facility are not experiencing an emergency. 

138 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

Repair time estimates are appropriate to use when calculating the DER’s operational availability but may be overly optimistic when considering the repairability during a multi-day grid outage. Under “blue sky” conditions MTTR are measured in days. During a “black sky” event, such as a multi-day grid outage, it is unlikely that parts and staff with appropriate expertise will be available in the same amount of time. For this reason, a failed DER is assumed to remain offline until grid electricity is restored. 

In analyzing DERs in backup power systems, we assume that they have passed acceptance testing, were properly engineered, and manufactured, and are not near the end of their lifetime. In terms of the reliability literature’s “Bathtub Model” (Figure 26), the DER is in its useful life period and is assumed to have a constant failure rate. 

**==> picture [307 x 141] intentionally omitted <==**

## **Figure 26. A reliability bathtub model showing a low constant failure rate during the useful life period** 

Under these conditions reliability R( _t_ ) decays exponentially and is given by 

**==> picture [176 x 30] intentionally omitted <==**

Where λ is the inverse of MTTF **.** 

## **21.6  Renewable Energy Outputs** 

In the Results Comparison Table, the REopt web tool reports the percentage of annual electricity consumption provided by on-site renewable generation (from PV, wind, or renewable fuels). By default, this percentage includes any renewable electricity that is exported to the grid, but the user may change this assumption on the inputs page. If fuel-burning technologies that serve thermal loads are modeled, then the percentage of annual _energy_ consumption (electric loads plus non-electrified heat (steam/hot water) loads) that is derived from on-site renewable generation is also reported. 

Note that for resilience analyses, renewable energy and emissions outputs do not consider operations during grid outages (calculations are made as if no outages occurred). 

139 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **21.7  Climate and Health Emissions Outputs** 

## _**21.7.1 Emissions Outputs in Results Comparison Table**_ 

The Results Comparison Table reports key climate & health emissions outputs for the Business as Usual and optimized cases. This includes avoided climate and health emissions throughout the analysis period as compared to business-as-usual operations. These avoided emissions account for grid-purchased electricity and on-site fuel consumption. By default, avoided emissions are calculated using marginal emissions rates and assume that exported electricity offsets grid emissions (as described in the “Climate and Health Emissions” section of this document). 

If, on the inputs page, the user selects “Clean Energy” as a goal and then selects “include climate (and/or health) emissions in objective function”, then the cost of climate and/or health emissions (included in the objective) over the analysis period will appear as non-zero values under the “Life Cycle Cost Breakdown” section of the Results Comparison table. This indicates that the costs are assumed to be true costs incurred by the project in both the BAU and optimized cases. By default, climate and health emissions costs are calculated and reported in the Renewable Energy & Emissions Metrics table (described below), but are not included in the LCC. 

Note that for resilience analyses, renewable energy and emissions outputs do not consider operations during grid outages (calculations are made as if no outages occurred). 

## _**21.7.2 Renewable Energy & Emissions Metrics Table**_ 

The Renewable Energy & Emissions table includes the renewable energy outputs described above along with more detailed emissions results by species (CO2e, NOx, SO2, and PM2.5), including breakdowns between emissions from grid purchases and fuel burn. 

Emissions of each pollutant over the financial life of the project are calculated as the sum of grid and fuel emissions. Emissions from fuel burn are assumed to remain constant throughout the analysis period (i.e., year one fuel emissions multiplied by the number of years). By contrast, emissions from grid-purchased electricity are assumed to decrease throughout the analysis period (see grid emissions data section), and the reported total emissions account for this year-over-year decrease. 

For each emissions species, average annual emissions from grid purchases are calculated as emissions over the analysis period divided by the number of years in the analysis period. Therefore, the average annual emissions results account for the assumed decreases in grid emissions rates over time. 

Total emissions costs for each pollutant are calculated as the present value of the marginal cost of each emission [$/t] times the quantity of emissions [t] over the analysis period for grid and fuel emissions.  The default values for the marginal costs used in these calculations are described in the Emissions Costs section. The full formulation of this calculation can be found in Appendix C. The present worth factor for grid emissions costs accounts for the projected annual percent increase in the marginal emissions cost for each species, the projected annual percent decrease in the marginal emission rate of each species, and the off-taker’s discount rate. The present worth factor for fuel emissions costs mirrors the grid present worth factor, but does not assume an annual decrease in emissions factors. Climate costs over the analysis period are reported for 

140 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

CO2e and health costs over the analysis period are reported as the sum of costs for NOx, SO2, and PM2.5. 

The “breakeven cost of CO2 emissions reduction ($/t CO2)” is also reported for scenarios in which the project NPV is negative. This value indicates the cost of CO2e that would bring a negative NPV to 0 (making the project “break even” with BAU costs of energy). This cost of CO2 can be compared to the social cost of carbon and/or other emissions reduction approaches. 

For more details on the methodology and data sources used for emissions and renewable energy calculations, refer to Section 9. 

## _**21.7.3 Interpreting Emissions Results Based on Emissions Type**_ 

Emissions results in the Renewable Energy & Emissions Metrics table (e.g., “CO2 Emissions Throughout Analysis Period”) should be interpreted differently depending on whether average or marginal emissions rates are utilized for grid-purchased electricity (by default, marginal emissions rates are used in REopt). Marginal emissions rates are used to describe _changes_ in emissions resulting from a change in load whereas average emissions rates are typically used for baselining (or “footprinting”) a facility’s emissions. The two emissions rate types should never be combined in calculations. 

For “Cost Savings” runs, the results table contains “Business as Usual”, “Financial”, and “Difference” columns. The first two columns contain outcomes for the BAU and optimized cases, respectively. The “Difference” column captures the _change_ in outcomes between the BAU and Financial cases. For “Resilience” runs, the result tables contain “Business as Usual,” “Resilience,” and “Financial” columns, which capture outcomes for each of these separate scenarios. 

If _marginal_ grid emissions rates are used (all default emissions rates are marginal) then the “Difference” column accurately captures the change in emissions-related metric tons and cost outcomes. The metrics in the “Difference” column account for how the grid responds to a small change in load: by increasing or decreasing the output of marginal generators. Therefore, this column can be used to estimate avoided emissions resulting from an investment in DERs. For “Resilience” runs, users must calculate the difference between BAU and Resilience case emissions to estimate avoided emissions. Using marginal emissions rates, care should be taken in interpreting emissions and emissions cost _totals_ for the “Business-as-Usual,” “Financial,” and “Resilience” cases. The emissions and emissions cost totals for each of these cases are included to allow for flexibility in utilizing REopt’s emissions calculations, but do not accurately capture total emissions if calculated using marginal emissions rates. 

Conversely, if _average_ grid emissions rates are used in REopt, then emissions results in the “Difference” column will not accurately represent the grid’s response to a marginal change in load. However, the “BAU”, “Financial”, and “Resilience” column totals may accurately capture average annual or analysis period emissions, as required by some emissions reporting protocols. 

**Table 38** provides simplified guidance for which Renewable Energy & Emissions Metrics columns to utilize when interpreting emissions results, based on the grid emissions rate type utilized in the analysis. 

141 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **Table 38. Simplified summary of how to interpret emissions results in the Renewable Energy & Emissions Metrics table, given the table column header and use of marginal vs. average grid emissions rates. Check mark indicates metric is appropriate to use and “X” indicates metric is not appropriate to use.** 

|Grid<br>Emissions<br>Rate Type|||REopt Results Tables Column Headers|REopt Results Tables Column Headers|REopt Results Tables Column Headers|
|---|---|---|---|---|---|
|||Business||Difference<br>(does not appear for<br>Resilienceruns)|Resilience|
||Typical Use|As Usual|Financial|||
|||||||
|Marginal<br>(default)|To determine<br>avoided<br>emissions<br>from an<br>intervention.||||(To determine avoided<br>emissions for resilience<br>runs, users must calculate<br>the difference between the<br>BAU and Resilience<br>emissions outcomes)|
|Average|To calculate<br>an emissions<br>baseline or<br>footprint for<br>an existing<br>facility.|||||



Users should refer to any applicable reporting protocols for guidance on which emissions type (e.g., marginal or average, data source, temporal resolution, geographic resolution) to use for their analysis and for guidance in interpreting REopt’s emissions results. 

## **21.8   Caution Information** 

Investment decisions should not be made on the REopt web tool results alone. These results assume perfect prediction of solar irradiance, wind speed, and electrical and thermal loads. In practice, actual savings may be lower based on the ability to accurately predict solar irradiance, wind speed, and load, and the control strategies used in the system. When modeling a grid outage, the results assume perfect foresight of the impending outage, allowing the battery system to charge in the hours leading up to the outage. If a natural gas-fueled CHP system is included, the resiliency results assume the natural gas supply is not disrupted during an electrical grid outage. 

The results include both expected energy and demand savings. However, the hourly model does not capture intra-hour variability of the PV and wind resource. Because demand is typically determined based on the maximum 15-minute peak, the estimated savings from demand reduction may be exaggerated. The hourly simulation uses one year of load data and one year of solar and wind resource data. Actual demand charges and savings will vary from year to year as load and resource vary. 

Asset dispatch decisions are determined by the model as part of the cost-minimization objective. In application, some aspects of these operational decisions may not work well with the existing infrastructure or may not follow best practices. For example, in results with CHP, boiler dispatch 

142 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

may result in short cycling or periodic boiler use that is not possible without hot-standby. The user should review the dispatch results with these limitations in mind. 

The REopt web tool may find CHP is cost effective but upon review of its operation, the user may find that the REopt web tool operated CHP in an unconventional manner. For example, CHP systems are often operated in baseload and sized to maximize heat recovery. In the REopt web tool, CHP sizing and dispatch are determined as part of the cost-minimization objective. In some modeled scenarios, the determining value of CHP may be reduction of electric utility demand charges. The value of heat recovery and avoided utility electricity costs in off-peak hours may be insufficient to offset the operation costs of CHP and therefore the REopt web tool might not operate CHP in baseload. Examination of the results may reveal the CHP system operated at low capacity factors or that the size of the unit resulted in low utilization of the available waste heat. The user is advised to review the relevant metrics and resultant economics to identify why the model has indicated CHP might be cost effective. For low capacity factors and/or low heat utilization, the value of the CHP unit might be heavily tilted to the power generated. 

PV system performance predictions calculated by PVWatts include many inherent assumptions and uncertainties and do not reflect variations between PV technologies nor site-specific characteristics except as represented by inputs. For example, PV modules with better performance are not differentiated within PVWatts from lesser-performing modules. 

Wind performance predictions are approximate only. Actual wind turbine performance is greatly affected by obstacles surrounding the turbine, including trees, buildings, silos, fences, or any other objects that could block the wind flow. Looking at a wind rose for the site is the best way to estimate the impact of local terrain and obstacles on the potential turbine energy production; Figure 27 gives a rule of thumb for where not to install a wind turbine (wind from the left). 

**==> picture [468 x 209] intentionally omitted <==**

**Figure 27. Obstacles to potential wind energy production** 

143 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **21.9  Next Steps** 

This model provides an **estimate** of the techno-economic feasibility of solar, wind, CHP, GHP, and battery, but investment decisions should not be made based on these results alone. **Before moving ahead with project development, verify:** 

- The utility rate tariff is correct 

   - Note that a site may have the option or may be required to switch to a different utility rate tariff when installing a PV, wind, CHP, or battery system 

   - Contact your utility for more information 

- Actual load data is used rather than a simulated load profile 

- PV, wind, CHP, GHP, and battery costs and incentives are accurate for your location 

   - There may be additional value streams not included in this analysis such as ancillary services or capacity payments 

- Financial inputs are accurate, especially discount rate and utility escalation rate 

- Other factors that can inform decision-making, but are not captured in this model, are considered. These may include: 

   - roof integrity 

   - shading considerations 

   - obstacles to wind flow 

   - ease of permitting 

   - mission compatibility 

   - regulatory and zoning ordinances 

   - utility interconnection rules 

   - availability of funding 

- Multiple systems integrators are consulted, and multiple proposals are received. These will help to refine system architecture and projected costs and benefits. The REopt web tool results can be used to inform these discussions. 

## **22 Off-grid Microgrids** 

By default, REopt optimizes systems to maximize grid-connected economics. Users have the option to instead model an entirely off-grid microgrid by toggling off the “Grid” technology option in the web tool. This differs from a resilience analysis, in which a facility is primarily grid-connected, but experiences a specified grid outage. The sections below detail the modified inputs, modeling changes, and outputs relevant to off-grid analyses. Default input values that are unique to off-grid modeling are detailed in relevant tables in Section 22. 

144 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **22.1 Off-grid inputs** 

The user inputs described here are included or modified when modeling an off-grid microgrid. The system is assumed to be entirely isolated from a bulk power system and thus no utility- or grid-related inputs are required for off-grid analyses. 

## **Technologies** 

REopt is capable of modeling an off-grid microgrid with solar PV, battery storage, and/or generators. Other technologies, including wind, CHP, and thermal energy storage cannot currently be modeled in an off-grid system in the web tool. 

## **Load Profile** 

In off-grid analyses, only electrical loads can be included; heating loads and cooling loads cannot be modeled. 

_Typical electrical load (units: kW per timestep):_ The load profile for off-grid analyses is assumed to be the aggregate load profile for all facilities that are to be served by the microgrid. For microgrids in rural Sub-Saharan Africa, NREL’s Microgrid Load Profile Explorer tool[33] may be useful for generating hourly load profiles for various household types and commercial entities. The user can also use the DOE Commercial Reference Buildings, as described in Section 7.2, however these profiles are not based on building modeling specific to off-grid scenarios and therefore the user is advised to consider their relevance for the analysis being performed. 

_Minimum load met (units: % of annual load):_ The minimum load met represents the percentage of total annual electrical load that must be met. This optional input is unique to off-grid analyses and enables the user to potentially relax the general constraint that 100% of the typical electrical load must be met in every hour of the analysis year. If a value less than 100% is entered, the model selects the timestep(s) in which to shed load, if needed. For off-grid power systems that rely on PV, building a system for 100% availability during extended days of low solar resource can result in very large battery energy storage solutions and can therefore be considerably more expensive than systems that have a lower availability requirement. By relaxing the constraint on meeting all of the annual electrical load, the user can explore the tradeoff between total costs and availability. 

_Load operating reserve requirement (units: % of load):_ The load operating reserve requirement is the surplus operating capacity (as a percentage of load) that must be able to respond to an unexpected increase in load in any timestep. For example, if the modeled load in a given timestep is 10 kW and the load operating reserve requirement is 20%, REopt will ensure that there are available operating reserves to meet an extra 2 kW of load during that timestep. In REopt, operating reserves (commonly referred to as spinning reserves) can be supplied by curtailed PV, PV charging batteries in the current time step, stored energy in batteries, and/or spinning generators. A higher load operating reserve requirement provides a greater safety margin to ensure reliable electricity supply. This is particularly useful if the true load is expected 

> 33 Microgrid Load Profile Explorer Tool: https://data.nrel.gov/submissions/79 

145 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

to be more variable than the load profile supplied to REopt. A separate REopt input defines the operating reserve requirements to cover a sudden decrease in solar generation (described below). 

## **Financial** 

_Additional capital costs (units: upfront cost):_ The construction of off-grid microgrids often entails additional capital costs beyond the purchase of generation technologies. These costs can include distribution network costs, powerhouse or battery container structure costs, etc. REopt assumes additional capital costs are for depreciable assets. Straight-line depreciation is applied to these costs for a period equal to the analysis period, reducing the owner’s taxable income. The user can enter these costs here to be included in the life-cycle cost analysis. The default cost is $0. 

_Additional annual costs (units: annual cost):_ Off-grid microgrids also often incur additional annual expenses beyond fuel costs, non-fuel operation and maintenance costs, and replacement costs. These additional expenses can include labor costs, land lease costs, software costs, and any other ongoing expenses not included in other cost inputs. REopt assumes any annual costs entered in this field escalate at the same rate as O&M costs (see Section 4.1). These costs are considered tax-deductible for the system owner. 

## **PV** 

_PV operating reserve requirement (units: % of PV generation):_ Operating reserve requirement as a percentage of solar PV generation in each timestep. The user input represents the percentage of solar generation that is assumed to potentially drop in any timestep, e.g., due to passing clouds. Operating reserves must be available to cover the user-specified drop in PV generation as well as a potential increase in load. Consider, for example, a microgrid with a 100-kW load in a given timestep, 50 kW of which is served by solar generation. If the load operating reserve requirement is 20% and the PV operating reserve requirement is 20%, then 20 kW (20% * 100 kW) of operating reserves are required to cover the potential increase in load and 10 kW (20% * 50 kW) of operating reserves are required to cover a potential decrease in PV generation, for a total of 30 kW of operating reserves required in that timestep. In REopt, operating reserves (commonly referred to as spinning reserves) can be supplied by available generation capacity from curtailed PV, PV charging batteries in the current time step, stored energy in the batteries, and/or spinning generators. 

## **Generator** 

_Generator size adjustment (units: % of peak load_ or _kW):_ For off-grid analyses in the web tool, the size of the diesel generator is a user input and is not determined by REopt. The user can set the generator size to either a percentage of annual peak electrical load or a custom size. The default generator size is 200% of the peak electrical load. Although only a single generator is modeled, the capacity could be installed in two units (each sized at 100% of peak load). In this case, the default system would provide N+1 capacity reserve, or enough generator capacity to support the peak electrical load when one of the units is off-line for maintenance. In the REopt API, it is possible to optimally size a diesel generator in an off-grid analysis, but longer solve times should be expected. 

146 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

_Minimum turndown (units: % of rated capacity):_ The minimum generator loading as a percentage of its rated capacity. Generators are typically designed to operate at 50 percent capacity or higher. Continuously underloading a generator can decrease the useful life of the unit, increase O&M costs, and cause unplanned shutdowns.[34] By default, the generator’s minimum turndown for off-grid analyses is set to 15% to limit the likelihood of infeasible solutions while avoiding unreasonable underloading.[35] As described above, we assume N+1 generator capacity reserve by default, and thus a 15% minimum turndown equates to one of the two assumed generators running at 30% minimum turndown. 

_Replacement year (units: years):_ The number of years the generator asset will be used before replacement. For off-grid analyses, the generator (and battery system) is assumed to be replaced once, in the specified replacement year. The replacement cost of a generator is assumed to be equal to its original installed cost. This input is unique to off-grid scenarios; for grid-connected evaluations, the backup diesel generator is assumed to last the entire analysis period. 

The actual life of a generator depends on many factors, including the generator’s detailed design, size, frequency at which it runs, typical loading capacity, climate, and maintenance schedule. If multiple generator replacements are anticipated, the following approach can be used to model the cost of these multiple replacements in REopt: 

1. Calculate the “net present value” of all future replacements as: 

**==> picture [321 x 43] intentionally omitted <==**

Where _i_ is the project year in which the asset is replaced, _n_ is the number of replacements, _d_ is the discount rate, and _F_ is the future cost of each replacement in $/kW. _F_ should account for inflation. 

2. Add the NPV of future replacements to the installed capital cost, both in $/kW. 

3. Enter this sum as the generator installed cost ($/kW) and set the replacement year equal to the analysis period (to ensure additional replacements are not modeled). 

## **22.2 Off-grid model** 

Several additional constraints are included in the REopt model for off-grid analyses, as formulated in Appendix C, Section 1.4.10. These constraints implement load and solar PV operating (or spinning) reserve requirements and a minimum load met requirement. 

## **22.3 Off-grid outputs** 

Several additional or modified outputs are reported for off-grid analyses, as described below. 

> 34 https://www.cat.com/en_US/by-industry/electric-power/Articles/White-papers/the-impact-of-generator-setunderloading.html 

> 35 The default generator minimum turndown for grid-connected “Resilience” scenarios is 0%. This input is modifiable in the REopt API, but is not exposed in the web tool for Resilience cases. 

147 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

_Life cycle cost (LCC):_ The life cycle cost (LCC) for off-grid analyses includes technology capital costs, O&M costs, and generator fuel costs (similar to grid-connected analyses), as well as usersupplied “additional capital costs” and the net present value of any “additional annual costs. The LCC will also include climate and/or health costs if the user chooses to include those costs in the objective function (See Section **Error! Reference source not found.** ) For _grid-connected_ analyses, the LCC is calculated for a business-as-usual case (BAU), and the net-present value (NPV) of the investment is calculated as the difference between the LCC in the investment and BAU cases. In contrast, for off-grid analyses there is no “business-as-usual” case, and thus no BAU LCC nor NPV is calculated. 

_Levelized cost of electricity (LCOE):_ This project-level output is specific to off-grid analyses. The off-grid LCOE is calculated as: 

**==> picture [343 x 42] intentionally omitted <==**

Where _LCC_ is the life cycle cost over the analysis period, _pwf_ is an annuity used to amortize the LCC into a constant annual cost (given the off-taker or owner’s discount rate, depending on the ownership structure), and _AnnualGeneration_ is the total microgrid generation in a year [kWh]. 

_Breakdown of LCOE by cost component:_ The results page of the web tool also breaks down the LCOE into the following cost components: renewable energy capital expenses (includes the installed cost of the solar PV and battery systems and replacement costs and salvage value for battery systems), generator capital expenses (includes the generator installed cost, replacement costs, and salvage value), other capital expenses (as input by the user), fuel costs, operations & maintenance costs (for the PV and generator), and other annual costs (as input by the user). This breakdown provides insights into the most costly aspects of the microgrid and potential opportunities for cost savings. 

## **23 The REopt Web Tool Default Values, Typical Ranges, and Sources** 

Note: Unless otherwise specified, all default values assume commercial projects in the United States. 

148 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 39. Site and Utilities Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**CHP Standby**<br>**charge based**<br>**on CHP size**<br>**($/kW/month)**|0|0–30|**Standby Rates for Customer-sited Resources; Issues,**<br>**Considerations, and the Elements of Model Tariffs;**<br>**2009.**<br>https://www.epa.gov/sites/production/files/2015-<br>10/documents/standby_rates.pdf<br>**Standby Rates for Combined Heat and Power**<br>**Systems; Economic Analysis and Recommendations**<br>**for Five States; 2014.**<br>https://www.raponline.org/knowledge-center/standby-<br>rates-for-combined-heat-and-power-systems-economic-<br>analysis-and-recommendations-for-five-states/|
|**Solver**<br>**optimality**<br>**tolerance (%)**|0.1%<br>general<br>1% CHP<br>5% Off-<br>grid|0.1% -<br>5%|Higher optimality tolerance values can be used when no<br>solution is found within the model’s timeout limit.<br>The additional constraints implemented for CHP and off-<br>grid analyses require a higher optimality tolerance default<br>to increase the likelihood that the model will find a timely<br>optimal solution.|



**Table 40. Load Profile Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Electric**<br>**cooling plant**<br>**coefficient of**<br>**performance**<br>**(COP)**<br>**(kWt/kWe)**|4.40<br>capacity<br><100<br>tons<br>4.69<br>capacity<br>>100<br>tons|2–7|**Sweetser, R. (2020, June). Exergy Partners**<br>**Corporation.****_Personal Communication_.**<br>**U.S. DOE Commercial Reference Buildings**<br>https://www.energy.gov/eere/buildings/commercial-<br>reference-buildings|
|**Existing**<br>**heating**<br>**system**<br>**efficiency (%**<br>**HHV-basis)**|Hot<br>water:<br>80%<br>Steam:<br>75%|50–95%|**U.S. DOE Commercial Reference Buildings**<br>https://www.energy.gov/eere/buildings/commercial-<br>reference-buildings<br>Default depends on whether the user selects hot water or<br>steam for the process heat loop.|
|**Max. boiler**<br>**thermal**<br>**capacity as**<br>**factor of peak**<br>**heating load**|1.25||This value is based on engineering judgment.|
|**Total installed**<br>**cost for**<br>**existing boiler**|0|53,000 –<br>70,000|EIA Updated Buildings Sector Appliance and Equipment<br>Costs and Efficiencies|



149 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**($/MMBtu-**<br>**hour)**|||https://www.eia.gov/analysis/studies/buildings/equipcosts/<br>pdf/full.pdf<br>If specified, the total installed cost of the existing boiler is<br>captured in the financial outputs of the optimal system and<br>the BAU system. In the BAU system, the existing boiler’s<br>total installed cost represents the cost of<br>upgrading/replacing the existing HVAC system, which can<br>be avoided with investment in DERs like GHP and ASHP.<br>The default value of $0 assumes that the site does**not**<br>have to install a new boiler.|
|---|---|---|---|
|**Total installed**<br>**cost for**<br>**existing boiler**<br>**($)**|0||This total installed cost is independent of the size of the<br>boiler. The user can use this instead of the**total installed**<br>**cost for existing boiler ($/MMBtu-hour)**above if they<br>know the total $ of upgrading/replacing their facility’s<br>existing boiler instead of the $/MMBtu-hour cost.<br>The default value of $0 assumes that the site does**not**<br>have to install a new boiler.|
|**Max. chiller**<br>**thermal**<br>**capacity as a**<br>**factor of peak**<br>**cooling load**|1.25||This value is based on engineering judgment.|
|**Total installed**<br>**cost for**<br>**existing**<br>**chiller ($/ton)**|0|850 -<br>1000|EIA Updated Buildings Sector Appliance and Equipment<br>Costs and Efficiencies<br>https://www.eia.gov/analysis/studies/buildings/equipcosts/<br>pdf/full.pdf<br>If specified, the total installed cost of the existing chiller is<br>captured in the financial outputs of the optimal system and<br>the BAU system. In the BAU system, the existing chiller’s<br>total installed cost represents the cost of<br>upgrading/replacing the existing HVAC system, which can<br>be avoided with investment in DERs like GHP and ASHP.<br>The default value of $0 assumes that the site does**not**<br>have to install a new chiller.|
|**Total installed**<br>**cost for**<br>**existing**<br>**chiller ($)**|0||This total installed cost is independent of the size of the<br>chiller. The user can use this instead of the**total installed**<br>**cost for existing chiller ($/ton)**above if they know the<br>total $ of upgrading/replacing their facility’s existing chiller<br>instead of the $/ton cost.<br>The default value of $0 assumes that the site does**not**<br>have to install a new chiller.|
|**Minimum load**<br>**met (%)**|99.9%||Off-grid analyses only. The default value slightly lower<br>than 100% reduces the likelihood of infeasible solutions.|
|**Load**<br>**operating**<br>**reserve**<br>**requirement**<br>**(% of load in**|10%||Off-grid analyses only. The load operating reserve<br>required is largely a user preference, based on the desired<br>reliability of the system. Previous work has assumed 10%<br>of the load must be covered by operating reserves.|



150 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**each**<br>**timestep)**|||**Power Generation Planning of Galapagos’ Microgrid**<br>**Considering Electric Vehicles and Induction Stoves.**<br>**Clairand, Jean-Michel, Mariano Arriaga, Claudio A.**<br>**Canizares, and Carlos Alvarez-Bel. IEEE**<br>**TRANSACTIONS ON SUSTAINABLE ENERGY,**<br>**ACCEPTED OCTOBER 2018.**<br>https://uwaterloo.ca/scholar/sites/ca.scholar/files/ccanizar/f<br>iles/clairand_power_gen_planning_galapagos.pdf|
|---|---|---|---|



**Table 41. Financial Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Analysis**<br>**period (years)**|25|10–40|**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>https://atb.nrel.gov/electricity/2024/data <br>Defaults for Economic lifetime of distributed commercial<br>renewable technologies used for NREL analyses vary. The<br>2024 Annual Technology Baseline includes options for 20<br>or 30 years.The default period is 30 years.Typical internal<br>REopt analyses use 25 years.<br>**ASTM E917-17, Standard Practice for Measuring Life-**<br>**Cycle Costs of Buildings and Building Systems, ASTM**<br>**International, West Conshohocken, PA, 2017.**<br>www.astm.org<br>This ASTM standard uses a 25-year study period for most<br>examples.<br>**NREL’s System Advisory Model (SAM)**uses a 25-year<br>analysis period default. September 2024.<br>https://sam.nrel.gov<br>**Energy Independence and Security Act of 2007, Sec.**<br>**441. Public Law 110-140, 110th US Congress.**<br>https://www.gpo.gov/fdsys/pkg/PLAW-<br>110publ140/pdf/PLAW-110publ140.pdf<br>Public building lifecycle costs are evaluated over a 40-year<br>period in federal analyses.|
|**Discount rate,**<br>**nominal (%)**|6.24%|2%–15%|**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>**https://atb.nrel.gov/electricity/2024/data.**|



151 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||The NREL 2024 Annual Technology Baseline has a<br>projected 2025 WACC Nominal of 6.24% for Distributed<br>Commercial PV and 6.25% for Land-based Wind.<br>Discount rate varies significantly between distributed PV<br>and wind adopters.|
|**Effective tax**<br>**rate (%)**|26%<br>21%<br>federal<br>+5%<br>state<br>average|15%–<br>21% for<br>federal<br>corporate<br>income<br>taxes plus<br>0%–9.8%<br>state<br>corporate<br>income<br>taxes|**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>**https://atb.nrel.gov/electricity/2024/data **<br>Tax rate (federal plus state) used for NREL analyses is<br>typically 26%. ATB lists 25.7%.<br>**2023 Instructions for Form 1120: U.S. Corporation**<br>**Income Tax Return. U.S. Department of the Treasury,**<br>**Internal Revenue Service, January 2024.**<br>https://www.irs.gov/pub/irs-pdf/i1120.pdf <br>Federal corporate income tax rate of a flat 21% is listed<br>under Schedule J, Tax Computation and Payment on page<br>20.<br>**State Corporate Income Tax Rates and Brackets for**<br>**2024. Tax Foundation, January 2024.**<br>https://taxfoundation.org/data/all/state/state-corporate-<br>income-tax-rates-brackets-2024/ <br>State corporate income tax rates and brackets listed for<br>2024.<br>Local income and state and local property taxes should<br>also be taken into account.|
|**Electricity**<br>**cost**<br>**escalation**<br>**rate, nominal**<br>**(%/year)**|1.66%|0-5%|Projected U.S. commercial annual electricity costs are<br>provided in the U.S. Energy Information Administration’s<br>(EIA) Annual Energy Outlook for the subsequent 25 years.<br>From their projections, we determine the nominal<br>escalation rate that would result in the equivalent net<br>present value of these 25-year costs, assuming REopt’s<br>current default discount rate and annual inflation rate.<br>**Annual Energy Outlook 2025 – Energy Prices by**<br>**Sector and Source. EIA, April 2025.**<br>https://www.eia.gov/outlooks/aeo/data/browser/#/?id=3-<br>AEO2025&cases=ref2025&sourcekey=0|



152 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Existing boiler**<br>**fuel cost**<br>**escalation**<br>**rate, nominal**<br>**(%/year)**|3.48%|0-5%|Projected U.S. commercial annual natural gas costs are<br>provided in the U.S. Energy Information Administration’s<br>(EIA) Annual Energy Outlook for the subsequent 25 years.<br>From their projections, we determine the nominal<br>escalation rate that would result in the equivalent net<br>present value of these 25-year costs, assuming REopt’s<br>current default discount rate and annual inflation rate.<br>**Annual Energy Outlook 2025 – Energy Prices by**<br>**Sector and Source. EIA, April 2025.**<br>https://www.eia.gov/outlooks/aeo/data/browser/#/?id=3-<br>AEO2025&cases=ref2025&sourcekey=0|
|**CHP and**<br>**Prime**<br>**Generator fuel**<br>**cost**<br>**escalation**<br>**rate, nominal**<br>**(%/year)**|3.48%|0-5%|Projected U.S. commercial annual natural gas costs are<br>provided in the U.S. Energy Information Administration’s<br>(EIA) Annual Energy Outlook for the subsequent 25 years.<br>From their projections, we determine the nominal<br>escalation rate that would result in the equivalent net<br>present value of these 25-year costs, assuming REopt’s<br>current default discount rate and annual inflation rate.<br>**Annual Energy Outlook 2025 – Energy Prices by**<br>**Sector and Source. EIA, April 2025.**<br>https://www.eia.gov/outlooks/aeo/data/browser/#/?id=3-<br>AEO2025&cases=ref2025&sourcekey=0|
|**Emergency**<br>**Generator fuel**<br>**cost**<br>**escalation**<br>**rate, nominal**<br>**(%/year)**|1.97%|0-5%|Projected U.S. commercial annual distillate fuel oil costs<br>are provided in the U.S. Energy Information<br>Administration’s (EIA) Annual Energy Outlook for the<br>subsequent 25 years. From their projections, we determine<br>the nominal escalation rate that would result in the<br>equivalent net present value of these 25-year costs,<br>assuming REopt’s current default discount rate and annual<br>inflation rate.<br>**Annual Energy Outlook 2025 – Energy Prices by**<br>**Sector and Source. EIA, April 2025.**<br>https://www.eia.gov/outlooks/aeo/data/browser/#/?id=3-<br>AEO2025&cases=ref2025&sourcekey=0|
|**O&M cost**<br>**escalation**<br>**rate (%/year)**|2.5%|-0.2% –<br>9.1%.|O&M costs are assumed to escalate at inflation rate.<br>**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>https://atb.nrel.gov/electricity/2024/data <br>NREL analyses assume an inflation rate of 2.5%.<br>**Energy Price Indices and Discount Factors for**<br>**LifeCycle Cost Analysis – 2024 Annual Supplement to**<br>**NIST Handbook 135. DOE, March 2024.**<br>**https://doi.org/10.6028/NIST.IR.85-3273-39**<br>Federal projects use an inflation rate of 1.2%.<br>**Historical Inflation Rates: 1914-2024. U.S. Inflation**<br>**Calculator, September 2024.**|



153 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||http://www.usinflationcalculator.com/inflation/historical-<br>inflation-rates/<br>Lists monthly U.S. inflation rates from 1914-2024. Inflation<br>rate average for 2023 listed as 4.1%. Since 2014, inflation<br>rates have ranged from -0.2% to 9.1%.|



**Table 42. Emissions Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Utility-**<br>**sourced**<br>**electricity**<br>**CO2e **<br>**emissions**<br>**factors**<br>**(lb/kWh)**|Contiguous<br>U.S.: hourly<br>projections<br>Alaska/Ha<br>waii:<br>annual<br>values<br>Internation<br>al: No<br>defaults||Hourly values for contiguous U.S.:**Cambium 2023**<br>**Datasets**. January 2024.<br>https://www.nrel.gov/docs/fy24osti/88507.pdf. Defaults are<br>projected GEA-level long-run marginal emissions rates<br>averaged over the analysis horizon.<br>Annual values for Hawaii and Alaska:**Emissions &**<br>**Generation Resource Integrated Database (eGRID).**<br>**Last modified version is ‘eGRID2022’.**Dec 2024.<br>https://www.epa.gov/energy/emissions-generation-<br>resource-integrated-database-egrid|
|**Utility-**<br>**sourced**<br>**electricity**<br>**NOx, SO2, and**<br>**PM2.5**<br>**emissions**<br>**factors**<br>**(lb/kWh)**|hourly or<br>annual|0 –<br>0.012|Hourly values for contiguous U.S.:**AVoided Emissions**<br>**and geneRation Tool (AVERT),**Version v4.3. April 2024.<br>https://www.epa.gov/avert/avoided-emission-rates-<br>generated-avert<br>Annual values for Hawaii and Alaska:**Emissions &**<br>**Generation Resource Integrated Database (eGRID).**<br>**Last modified version is ‘eGRID2022.**Dec 2024.<br>https://www.epa.gov/energy/emissions-generation-<br>resource-integrated-database-egrid|
|**Projected**<br>**annual**<br>**percent**<br>**decrease in**<br>**grid health**<br>**emissions**<br>**factors**<br>**(%/year)**|4.59%||Calculated as the U.S. national average percent decrease<br>in long-run marginal CO2e (Combined<br>Combustion+Precombustion) emissions from the first and<br>last year available in the latest NREL Cambium dataset,<br>assuming the Mid-Case scenario (Gagnon P. S., 2024).|
|**On-site fuel**<br>**usage CO2e **<br>**emissions**<br>**factors**<br>**(lb/MMBtu)**|Natural<br>gas:<br>117.03|139-<br>163|Values depend on fuel type used for each technology.<br>**EPA, 2023. “GHG Emission Factors Hub”**CO2, CH4and<br>N2O emissions factors. January 2024.<br>https://www.epa.gov/climateleadership/ghg-emission-<br>factors-hub.|



154 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||Landfill<br>biogas:<br>115.38<br>Propane:<br>139.16<br>Diesel oil:<br>163.61||CO2e values calculated using 100-year (AR6) global<br>warming potential values (GWP) from the**IPCC’s Sixth**<br>**Assessment Report (2023),**with GWP values for CO2,<br>CH4, and N2O of 1, 29.8, and 273, respectively.|
|**On-site fuel**<br>**usage NOx,**<br>**SO2, and PM2.5**<br>**emissions**<br>**factors**<br>**(lb/MMBtu)**|See “Fuel<br>Emissions<br>Factors”<br>section.|0 –<br>0.56|Values depend on fuel type used for each technology.<br>**EPA WebFIRE database.**January 2021.<br>https://cfpub.epa.gov/webfire/.|



**Table 43. PV Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**System**<br>**capital cost**<br>**($/kW)**|See<br>Section<br>10.1|$1,000 –<br>$4,000|**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>**https://atb.nrel.gov/electricity/2024/data **<br>Capital cost is based on the size class methodology<br>described in section 10.1 with direct ATB costs for<br>residential, large commercial, and utility size classes and<br>scaled ATB costs based on (Ramasamy, Feldman,<br>Margolis, & Desai, 2021) for small commercial and<br>industrial size classes. ATB data uses the 2024 class 5<br>moderate forecast, inflated from 2022 average annual data<br>provided to average annual 2024 dollars, using the<br>consumer price index ratio of 1.07 from the U.S. Bureau of<br>Labor Statistics: https://www.bls.gov/cpi/.<br>**U.S. Solar Photovoltaic System and Energy Storage**<br>**Cost Benchmarks, With Minimum Sustainable Price**<br>**Analysis: Q1 2023. September 2023.**<br>https://www.nrel.gov/docs/fy23osti/87303.pdf <br>**Spring 2024 Solar Industry Update. NREL, May 14,**<br>**2024.**<br>https://www.nrel.gov/docs/fy24osti/90042.pdf<br>From H1 2023 to early 2024, price data for distributed PV<br>systems for select states (AZ, CA, MA, NY) decreased to<br>$4,170/kW for 2.5-10 kW systems, decreased to<br>$3,460/kW for 10 to 100 kW systems, decreased to<br>$2,610/kW for 100 to 500 kW systems, decreased to<br>$2,230/kW for 500 to 1000kW systems, decreased to|



155 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||$1,650/kW for 1 to 5 MW systems, and decreased to<br>$1,140/kW for systems larger than 5 MW.|
|**O&M cost**<br>**($/kW/year)**|See<br>Section<br>10.1|$19 –$32|**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>**https://atb.nrel.gov/electricity/2024/data **<br>Fixed O&M expenses for PV depends on the determined<br>size class as described in section 10.1.|
|**Array azimuth**|180° or<br>0°|0° - 360°|The default value of 180° assumes the array is in the<br>northern hemisphere and is facing due south. When the<br>array is in the southern hemisphere, the assumption is that<br>it is facing due north and the array azimuth default value<br>changes to 0°.<br>**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>PVWatts uses a default azimuth of 180° in the northern<br>hemisphere and 0° in the southern hemisphere.<br>**U.S. Solar Photovoltaic System and Energy Storage**<br>**Cost Benchmark: Q1 2020. NREL, January 2021.**<br>https://www.nrel.gov/docs/fy21osti/77324.pdf<br>The resource specifies an array azimuth of 180°.|
|**Array tilt –**<br>**Rooftop,**<br>**Fixed**|20°|0° – 60°|Rooftop PV is usually mounted at 10-20 degrees on a flat<br>roof to reduce wind loading and shading losses. PV on a<br>sloped roof is typically installed parallel to the roof’s<br>surface, though azimuth and tilt angle can be adjusted if<br>desired.<br>**Current PVWatts online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>The PVWatts® default value for the tilt angle depends on<br>the array type: For a fixed array, the default value is 20<br>degrees, and for one-axis tracking the default value is<br>zero..<br>**U.S. Solar Photovoltaic System and Energy Storage**<br>**Cost Benchmarks, With Minimum Sustainable Price**<br>**Analysis: Q1 2023**<br>https://www.nrel.gov/docs/fy23osti/87303.pdf<br>The resource specifies an array tilt of 10° for commercial<br>rooftop systems. Note that the 2023 version did not model<br>the 100 kW commercial system.<br>**Best Practices for Operation and Maintenance of**<br>**Photovoltaic and Energy Storage Systems; 3rd**<br>**Edition. 2018.**|



156 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||https://www.nrel.gov/docs/fy19osti/73822.pdf<br>For a ballasted system on a flat roof, a low tilt angle<br>(usually 10° tilt) is required to reduce wind loads.|
|**Array tilt –**<br>**Ground**<br>**mount, Fixed**|20°|0° – 90°|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>The PVWatts® default value for the tilt angle depends on<br>the array type: For a fixed array, the default value is 20<br>degrees, and for one-axis tracking the default value is<br>zero.<br>**Advanced Photovoltaic Installations. Balfour, John,**<br>**Michael Shaw, and Nicole Bremer Nash. The Art and**<br>**Science of Photovoltaics. 2013.**<br>https://books.google.com/books?id=t5uTktdsu3AC&pg=PA<br>77&lpg=PA77&dq=pv+geometry+flat+roof&source=bl&ots<br>=K4v99ljXqq&sig=spZ0uf0Zdh-<br>zrK66Zldm6UN6ECs&hl=en&sa=X&ved=0ahUKEwiErOjBl<br>evVAhUKw4MKHTzoCMMQ6AEIcDAM#v=onepage&q=pv<br>%20geometry%20flat%20roof&f=false<br>Page 71 describes how in order to maximize annual yield,<br>the array should be tilted at the site’s latitude. Decreasing<br>the tilt angle increases summer yield while increasing tilt<br>angle increases winter yield. To maximize output in<br>summer, it should be tilted at (latitude – 15)°. To maximize<br>output in winter, it should be tilted at (latitude + 15) °.|
|**Array tilt –**<br>**Ground**<br>**mount, 1-Axis**<br>**Tracking**|0|0° – 10°<br>based on<br>site slope|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>For arrays with one-axis tracking, the tilt angle is the angle<br>from horizontal of the tracking axis. For flat ground, the tilt<br>would be 0°, or parallel to the ground’s surface. For<br>installations that are not on flat ground, the tilt would be<br>the slope of the hillside.<br>**Solar Balance-of-System: To Track or Not to Track,**<br>**Part 1. Greentech Media,**<br>https://www.greentechmedia.com/articles/read/solar-<br>balance-of-system-to-track-or-not-to-track-part-i<br>One-axis tracking systems rotate over an axis that is<br>parallel to the ground’s surface.|
|**DC to AC ratio**|1.2|1.1 – 1.5|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php|



157 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||PVWatts inputs list 1.2 as the default. The help manual<br>also lists a default DC/AC ratio of 1.2 and a corresponding<br>range of 1.1 to 1.5.|
|**Incentives**|30%<br>ITC, 5<br>year<br>MACRS<br>100%<br>Bonus<br>deprecia<br>tion||**Database of State Incentives for Renewables &**<br>**Efficiency. NC Clean Energy Tech Center**<br>http://www.dsireusa.org/<br>Incentives are available at the federal, state, and local<br>level. This site provides searchable specifics about<br>incentives based on location. The following federal<br>incentives are default values in the REopt web tool:<br>**Business Energy Investment Tax Credit (ITC)**<br>https://programs.dsireusa.org/system/program/detail/658<br>Includes a base tax credit of 6-30%, depending on project<br>status, labor factors, and system size). To qualify for the<br>tax credit, solar and wind energy systems must be either<br>placed in service by December 31, 2027, or construction<br>must commence by July 4, 2026, and must comply with<br>Foreign Entity of Concern rules. <br>**Cost recovery for qualified clean energy facilities,**<br>**property and technology**<br>https://www.irs.gov/credits-deductions/cost-recovery-for-<br>qualified-clean-energy-facilities-property-and-technology <br>Qualified clean energy facilities placed in service after<br>2024 may be classified as 5-year property via MACRS<br>under Provision 13703 of the Inflation Reduction Act of<br>2022. Qualified property includes technologies as defined<br>in § 48E and 45Y, which include solar generation placed in<br>service after 2024.<br>**Modified Accelerated Cost-Recovery System.**<br>**Database of State Incentives for Renewables &**<br>**Efficiency, NC Clean Energy Tech Center, July 2025.**<br>http://programs.dsireusa.org/system/program/detail/676<br>Pursuant to Public Law No. 119-21, qualified property<br>acquired and placed in service after January 19, 2025 may<br>qualify for 100% first year bonus depreciation. Qualified<br>property includes depreciable assets with a recovery<br>period of 20 years or less. The law additionally repeals the<br>ability of “energy property” under § 48(a)(3)(A) to qualify<br>for 5-year MACRS (projects that qualify under §48E/§45Y<br>will continue to be treated as 5-year MACRS property).<br>Thus, solar projects that qualify as §48E/45Y property may<br>utilize 100% first year bonus depreciation.|
|**System losses**<br>**– General**|||Total losses calculated as ( 1 - (1-loss1)*(1-loss2)*…*(1-<br>lossN) )|
|**System losses**<br>**– Soiling**|2%|2% –<br>25%|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf|



158 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||**Current PVWatts online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>PVWatts applies a default soiling loss of 2%.<br>**Performance Parameters for Grid-Connected PV**<br>**Systems. NREL, February 2005.**<br>https://www.nrel.gov/docs/fy05osti/37358.pdf<br>Table 1 lists a typical soiling AC derate factor as 0.95, with<br>a typical range of 0.75-0.98. These values correspond to a<br>typical soiling loss of 5% with a typical range of 2%-25%.|
|**System losses**<br>**– Shading**|3%|0% –<br>30%|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>PVWatts applies a default shading loss of 3%.<br>**Photovoltaic Shading Testbed for Module-Level Power**<br>**Electronics: 2016 Performance Data Update. NREL**<br>**and PV Evolution Labs, September 2016.**<br>https://www.nrel.gov/docs/fy16osti/62471.pdf <br>Based on a survey of shading of residential PV systems,<br>this study classifies light shading as <15% annual shading<br>(7.6% is representative of typical light shading), moderate<br>shading as 15%-20% annual shading (19% is<br>representative of typical moderate shading), and heavy<br>shading as >20% annual shading (25.5% is representative<br>of typical heavy shading). If the shading increases to<br>>30% of the modules in a string, the maximum power point<br>tracking (MPPT) minimum voltage would be reached.<br>**Performance Parameters for Grid-Connected PV**<br>**Systems. NREL, February 2005.**<br>https://www.nrel.gov/docs/fy05osti/37358.pdf<br>Table 1 lists a typical shading derate factor as 0.975 for<br>fixed-tilt rack-mounted systems. These values correspond<br>to a typical shading loss of 2.5%.|
|**System losses**<br>**– Snow**|0%|0% –<br>15%<br>typical in<br>US, 0% –<br>100%<br>possible|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>PVWatts applies a default snow loss of 0%.<br>**Integration, Validation, and Application of a PV Snow**<br>**Coverage Model in SAM. NREL, August 2017.**<br>https://www.nrel.gov/docs/fy17osti/68705.pdf<br>Figures 2 and 3 show estimated snow losses for cities and<br>regions, respectively, of the United States. Appendices A<br>and B provide the respective data in more detail.|



159 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**System losses**<br>**– Mismatch**|2%|1.5% –<br>3%|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>PVWatts applies a default mismatch loss of 2%.<br>**Performance Parameters for Grid-Connected PV**<br>**Systems. NREL, February 2005.**<br>https://www.nrel.gov/docs/fy05osti/37358.pdf<br>Table 1 lists a typical mismatch derate factor as 0.98, with<br>a typical range of 0.97-0.985. These values correspond to<br>a typical mismatch loss of 2% with a typical range of 1.5%-<br>3%.|
|**System losses**<br>**–Wiring**|2%|0.7% –<br>2%|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>PVWatts applies a default wiring loss of 2%.<br>**Performance Parameters for Grid-Connected PV**<br>**Systems. NREL, February 2005.**<br>https://www.nrel.gov/docs/fy05osti/37358.pdf<br>Table 1 lists a typical wiring derate factor as 0.99, with a<br>typical range of 0.98-0.993. These values correspond to a<br>typical wiring loss of 1% with a typical range of 0.7%-2%.|
|**System losses**<br>**– Connection**|0.5%|0.3% –<br>0.1%|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>PVWatts applies a default connection loss of 0.5%.<br>**Performance Parameters for Grid-Connected PV**<br>**Systems. NREL, February 2005.**<br>https://www.nrel.gov/docs/fy05osti/37358.pdf<br>Table 1 lists a typical diodes and connections derate factor<br>as 0.995, with a typical range of 0.99-0.997. These values<br>correspond to a typical connection loss of 0.5% with a<br>typical range of 0.3%-1%.|
|**System losses**<br>**– Light-**<br>**induced**<br>**degradation**<br>**(LID)**|1.5%|0.3% –<br>10%|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>PVWatts applies a default light-induced degradation loss<br>of 1.5%.<br>**Performance Parameters for Grid-Connected PV**<br>**Systems. NREL, February 2005.**|



160 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||https://www.nrel.gov/docs/fy05osti/37358.pdf<br>Table 1 lists a typical LID derate factor as 0.98, with a<br>typical range of 0.90-0.99. These values correspond to a<br>typical mismatch loss of 2% with a typical range of 1%-<br>10%.|
|**System losses**<br>**– Nameplate**<br>**Rating**|1%|-5% –<br>15%|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>PVWatts applies a default nameplate rating loss of 1%.<br>**Performance Parameters for Grid-Connected PV**<br>**Systems. NREL, February 2005.**<br>https://www.nrel.gov/docs/fy05osti/37358.pdf<br>Table 1 lists a typical nameplate rating derate factor as<br>1.0, with a typical range of 0.85-1.05. These values<br>correspond to a typical nameplate rating loss of 0% with a<br>typical range of -5%-15%.|
|**System losses**<br>**– Age**|0%|0% –<br>100%|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>PVWatts applies a default loss due to age of 0%.|
|**System losses**<br>**– Availability**|3%|0.5% –<br>100%|**PVWatts Version 5 Manual. Dobos, Aron P., NREL,**<br>**September 2014.**<br>https://www.nrel.gov/docs/fy14osti/62641.pdf<br>**Current PVWatts Online Help Manual. September 2024.**<br>https://pvwatts.nrel.gov/index.php<br>PVWatts applies a default availability loss of 3%.<br>**Performance Parameters for Grid-Connected PV**<br>**Systems. NREL, February 2005.**<br>https://www.nrel.gov/docs/fy05osti/37358.pdf<br>Table 1 lists a typical availability derate factor as 0.98, with<br>a typical range of 0-0.995. These values correspond to a<br>typical availability loss of 2% with a typical range of 0.5%-<br>100%.|
|**PV operating**<br>**reserve**<br>**requirement**<br>**(% of PV**<br>**generation in**<br>**each time**<br>**step)**|25%||Off-grid analyses only. The PV operating reserve required<br>is largely a user preference, based on the desired<br>reliability of the system. Previous work has assumed 25%<br>of solar power must be covered by operating reserves.<br>**Renewable Energy Deployment in Canadian Arctic.**<br>**Das, Indrajit and Claudio Canizares. World Wildlife**<br>**Fund (WWF) Canada. 2016.**<br>https://wwf.ca/wp-content/uploads/2020/03/Fuelling-<br>change-in-the-arctic_2016.pdf|



161 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||**Power Generation Planning of Galapagos’ Microgrid**<br>**Considering Electric Vehicles and Induction Stoves.**<br>**Clairand, Jean-Michel, Mariano Arriaga, Claudio A.**<br>**Canizares, and Carlos Alvarez-Bel. IEEE Transactions**<br>**on Sustainable Energy, Accepted October 2018.**<br>https://uwaterloo.ca/scholar/sites/ca.scholar/files/ccanizar/f<br>iles/clairand_power_gen_planning_galapagos.pdf|



**Table 44. Battery Storage Inputs, Default Values, Ranges, and Sources** 

_Note: All values listed assume the use of lithium-ion battery systems_ 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Constant cost**<br>**($)**|$222,11<br>5|$5,000 -<br>$1e6|**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>**https://atb.nrel.gov/electricity/2024/data**<br>Commercial Battery Storage, 2024 moderate forecast,<br>inflated from mid-year 2022 data provided to mid-year<br>2024 dollars, using the consumer price index ratio of 1.07<br>from the U.S. Bureau of Labor Statistics:<br>https://www.bls.gov/cpi/.<br>For reference for residential-scale systems:<br>$5,926 (2024 dollars)|
|**Energy**<br>**capacity cost**<br>**($/kWh)**|$253|$289 –<br>$686|**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>**https://atb.nrel.gov/electricity/2024/data**<br>Commercial Battery Storage, 2024 moderate forecast,<br>inflated from mid-year 2022 data provided to mid-year<br>2024 dollars, using the consumer price index ratio of 1.07<br>from the U.S. Bureau of Labor Statistics:<br>https://www.bls.gov/cpi/.<br>For reference for residential-scale systems:<br>$452/kWh (2024 dollars)<br>**U.S. Energy Storage Monitor: Q2 2023 Full Report.**<br>**Wood Mackenzie Power & Renewables/American**<br>**Clean Power Association, June 2023.**<br>This analysis starts with Wood Mackenzie's all-inclusive<br>cost of system, installation, normal interconnection, and|



162 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**||**Source**|
|---|---|---|---|---|
|||||metering costs to be $1,821/kW for a non-residential<br>behind-the-meter 2-hour system, with a cost range of<br>$1,156 - $2,743/kW.<br>To determine energy capacity and energy demand<br>components of the cost, the system can be assumed to<br>have an energy:power ratio of 2:1 (i.e. 2 kWh:1kW), the<br>resulting median costs are approximately $455/kWh and<br>$910/kW (with ranges of 289-686 kWh and 578-1372 kW)<br>**Lazard's Levelized Cost of Storage Analysis – Version**<br>**8. April 2023.**<br>https://www.lazard.com/research-insights/2023-<br>levelized-cost-of-energyplus/<br>Key Assumptions table gives Initial Capital cost for a 2-hr<br>1 MW Commercial & Industrial battery of $429-$469/kWh<br>and $50-$80/kW-AC|
|**Power**<br>**capacity cost**<br>**($/kW)**|$968|$578 –<br>$1372||**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>**https://atb.nrel.gov/electricity/2024/data**<br>Commercial Battery Storage, 2024 moderate forecast,<br>inflated from mid-year 2022 data provided to mid-year<br>2024 dollars, using the consumer price index ratio of 1.07<br>from the U.S. Bureau of Labor Statistics:<br>https://www.bls.gov/cpi/.<br>For reference for residential-scale systems:<br>$489/kW (2024 dollars)|
|**O&M Cost (%**<br>**CapEx/yr)**|2.5%|0 – 5%||**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>**https://atb.nrel.gov/electricity/2024/data**<br>Commercial Battery Storage, 2024 moderate forecast,<br>scaled from 2022 to 2024 dollars.|
|**Battery**<br>**energy**<br>**capacity**<br>**replacement**<br>**cost ($/kWh)**|$0|$0 – $480||**U.S. Energy Storage Monitor: Q2 2023 Full Report.**<br>**Wood Mackenzie Power & Renewables/American**<br>**Clean Power Association, June 2023.**<br>Woods Mackenzie notes a 5-% decline in since the Q1<br>2023 peak, but note that further declines are uncertain.<br>**2023 Annual Technology Baseline and Standard**<br>**Scenarios. NREL, 2023.**<br>https://atb.nrel.gov/<br>Battery energy capacity replacement costs estimated to<br>decline by approximately 30% by the year 10 replacement.|



163 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**||**Source**|
|---|---|---|---|---|
|||||This was based on ATB estimate of $153/kWh in the year<br>2034 for a commercial battery under the moderate<br>scenario. This is a decline of about 30% from the 2024<br>cost of $219. Costs range from $129/kWh (Advanced) to<br>$219/kWh (Conservative).<br>**Energy Storage Technology and Cost Characterization**<br>**Report.  Pacific Northwest National Laboratory. July**<br>**2019**<br>https://www.pnnl.gov/main/publications/external/technical_<br>reports/PNNL-28866.pdf<br>A cost drop of 5% per year was assumed to be a<br>conservative estimate for batteries on the lower end of the<br>cost range. This is in light of significant cost drops seen in<br>the 2009-2019 period.|
|**Energy**<br>**capacity**<br>**replacement**<br>**year**|10|9 – 20||Because the replacement timeline for Li-ion batteries is<br>impacted by the SOC at which it is utilized, the<br>replacement year is difficult to predict. The REopt web tool<br>does not currently account for battery degradation or loss<br>of capacity over time in its dispatch and energy/power<br>calculations but allows the user to input a replacement<br>year. The Year 10 replacement default assumes that the<br>technology for this replacement will have improved to the<br>point that it will last for the remaining 15 years of the<br>default 25-year analysis period.<br>**Energy Storage Grand Challenge Cost and**<br>**Performance Assessment 2022, August 2022.**Finds<br>lifetime of Lithium-ion NMC batteries to be 13 years and<br>lifetime of lithium-ion LFP batteries to be 16 years. Range<br>for lithium-ion batteries overall found to be 10-15 years.<br>https://www.pnnl.gov/sites/default/files/media/file/ESGC%2<br>0Cost%20Performance%20Report%202022%20PNNL-<br>33283.pdf and https://www.pnnl.gov/lithium-ion-battery-lfp-<br>and-nmc<br>**Economic Analysis Case Studies of Battery Energy**<br>**Storage with SAM. NREL, November 2015.**<br>https://www.nrel.gov/docs/fy16osti/64987.pdf <br>Uses the Tesla Powerwall specifications as an example<br>and estimates that it will last 5 years longer than its 10-<br>year warranty. At one cycle per day, this amounts to<br>approximately 5,475 cycles.|
|**Power**<br>**capacity**<br>**replacement**<br>**cost ($/kW)**|$0|$0 –<br>$1078||See above description of basis for energy capacity<br>replacement cost.|
|**Power**<br>**capacity**<br>**replacement**<br>**year**|10|9 – 20||See above description of basis for energy capacity<br>replacement year.|



164 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Rectifier**<br>**efficiency (%)**|96%||**An integrated approach for the analysis and control of**<br>**grid connected energy storage systems. Journal of**<br>**Energy Storage, Volume 5, February 2016.**<br>http://www.sciencedirect.com/science/article/pii/S2352152<br>X15300335<br>Depending on the SOC, the converter efficiency of a<br>100kW/50kWh lithium-ion system was found to sit around<br>96% for SOCs of 30-100%, as illustrated in Figure 14.<br>The efficiency of this converter is applied to both the<br>inverter and rectifier in the REopt web tool.|
|**Round trip**<br>**efficiency (%)**|97.5%|95% –<br>98%|**An integrated approach for the analysis and control of**<br>**grid connected energy storage systems. Journal of**<br>**Energy Storage, Volume 5, February 2016.**<br>http://www.sciencedirect.com/science/article/pii/S2352152<br>X15300335<br>Depending on the SOC, the battery efficiency of a<br>100kW/50kWh lithium-ion system was found to vary<br>between 97% and 98% for SOCs of 30%-100%, as<br>illustrated in Figure 14.<br>**Lithium Batteries and Other Electrochemical Storage**<br>**Systems. Glazie, Christian and Geniès, Sylvie, August**<br>**2013.**<br>http://onlinelibrary.wiley.com/doi/10.1002/9781118761120.<br>ch6/pdf<br>The efficiency depends on the battery’s state of charge<br>and it’s charge/discharge conditions (voltage, rate of<br>charge/discharge, temperature), especially at high or low<br>SOC. The following values give average efficiencies at<br>mid-range SOCs.<br>95% for C-LiFePO4– see Section 6.2.18.<br>98% for C-Li(Co,Ni)O2– see Section 6.2.18.|
|**Inverter**<br>**efficiency (%)**|96||**An integrated approach for the analysis and control of**<br>**grid connected energy storage systems. Journal of**<br>**Energy Storage, Volume 5, February 2016.**<br>http://www.sciencedirect.com/science/article/pii/S2352152<br>X15300335<br>Depending on the SOC, the converter efficiency of a<br>100kW/50kWh lithium-ion system was found to sit around<br>96% for SOCs of 30-100%, as illustrated in Figure 14.<br>The efficiency of this converter is applied to both the<br>inverter and rectifier in the REopt web tool.|
|**Minimum**<br>**state of**<br>**charge (%)**|20|15% –<br>30%|**An integrated approach for the analysis and control of**<br>**grid connected energy storage systems. Journal of**<br>**Energy Storage, Volume 5, February 2016.**<br>http://www.sciencedirect.com/science/article/pii/S2352152<br>X15300335<br>When the state of charge of a lithium-ion battery drops<br>below 20%, the voltage drops rapidly and impedance,|



165 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||which reduces round trip efficiency and generates heat, so<br>optimal performance is achieved above 20% SOC.|
|**Initial state of**<br>**charge (%)**|50%<br>general<br>100%<br>Off-grid||For off-grid scenarios, the battery is assumed to start fully<br>charged. This avoids oversizing the battery solely to<br>supply power during the first several hours of the modeled<br>year of operations, during which time solar PV would not<br>be generating any power.|
|**Incentives**|30%<br>ITC, 5-<br>year<br>MACRS<br>100%<br>Bonus<br>deprecia<br>tion||**Database of State Incentives for Renewables &**<br>**Efficiency. NC Clean Energy Tech Center**<br>http://www.dsireusa.org/<br>Incentives are available at the federal, state, and local<br>level. This site provides searchable specifics about<br>incentives based on location. The following federal<br>incentives are default values in the REopt web tool:<br>**Business Energy Investment Tax Credit (ITC)**<br>https://programs.dsireusa.org/system/program/detail/658 <br>Energy storage projects are eligible for the Investment Tax<br>Credit (ITC) under IRC §48E if placed in service after<br>2024. The Inflation Reduction Act of 2022 expanded ITC<br>eligibility to include stand-alone energy storage<br>technology. The base credit is 6% of eligible costs,<br>increased to 30% if prevailing wage and apprenticeship<br>requirements are met, with potential bonus credits for<br>domestic content, energy communities, or low-income<br>projects. To qualify, the battery must have a capacity of at<br>least 5 kWh.<br>**Cost recovery for qualified clean energy facilities,**<br>**property and technology**<br>https://www.irs.gov/credits-deductions/cost-recovery-for-<br>qualified-clean-energy-facilities-property-and-technology<br>Qualified energy storage property placed in service after<br>2024 may be classified as 5-year property via MACRS<br>under Provision 13703 of the Inflation Reduction Act of<br>2022. Qualified property includes energy storage<br>technology as defined in 26 U.S. Code Section 48E(c)(2).<br>**Modified Accelerated Cost-Recovery System.**<br>**Database of State Incentives for Renewables &**<br>**Efficiency, NC Clean Energy Tech Center, July 2025.**<br>http://programs.dsireusa.org/system/program/detail/676<br>Pursuant to Public Law No. 119-21, qualified property<br>acquired and placed in service after January 19, 2025 may<br>qualify for 100% first year bonus depreciation. Qualified<br>property includes depreciable assets with a recovery<br>period of 20 years or less. The law additionally repeals the<br>ability of “energy property” under § 48(a)(3)(A) to qualify<br>for 5-year MACRS (projects that qualify under §48E/§45Y<br>will continue to be treated as 5-year MACRS property).|



166 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||Thus, energy storage projects that qualify as §48E<br>property may utilize 100% first year bonus depreciation.|



167 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 45. Wind Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**||**Source**|
|---|---|---|---|---|
|**Wind size**<br>**class**|Res: 0-<br>20 kW<br>Comm:<br>21 kW-<br>100 kW<br>Midsize:<br>101-999<br>kW<br>Large:<br>>=1,000<br>kW|2.5 kW–<br>2,000 kW||Wind Class size options, and the representative turbine<br>sizes, are Residential 0-20 kW (2.5 kW), Commercial 21-<br>100 kW (100 kW), Midsize 101-999 kW (250 kW) and<br>Large ≥ 1000 kW (2,000 kW).<br>**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>**https://atb.nrel.gov/electricity/2024/data**<br>https://atb.nrel.gov/<br>**2021 Cost of Wind Energy Review. December 2022.**<br>Tyler Stehly and Patrick Duffy, NREL. Distributed wind<br>categorized as: Residential (0-20 kW), Commercial (21-<br>100 kW), and Large (101-1500 kW)<br>https://www.nrel.gov/docs/fy23osti/84774.pdf<br>**Distributed Wind Market Report: 2021 Edition.**Alice<br>Orrell, Kamila Kazimierczuk, and Lindsay Sheridan of<br>Pacific Northwest National Laboratory. August 2021.<br>https://www.pnnl.gov/main/publications/external/technical_<br>reports/PNNL-31729.pdf<br>**Benchmarking US Small Wind Costs with the**<br>**Distributed Wind Taxonomy**. AC Orrell and EA<br>Poehlman. Pacific Northwest National Laboratory.<br>September 2017.<br>https://www.pnnl.gov/main/publications/external/technical_<br>reports/PNNL-26900.pdf|
|**System**<br>**capital cost**<br>**($/kW) Class**|Res:<br>$7,692<br>Comm:<br>$5,776<br>Midsize:<br>$3,807<br>Large:<br>$2,896|||**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>**https://atb.nrel.gov/electricity/2024/data**<br>Distributed Wind (Wind Speed Class 7), 2024 moderate<br>forecast by size class, scaled from 2022 to 2024 dollars.<br>**2022 Cost of Wind Energy Review. December 2023.**<br>**Tyler Stehly, Patrick Duffy, and Daniel Mulas**<br>**Hernando. NREL. Residential (20kW) CapEx:**<br>**$8425/kW, Commercial (100kW) CapEx: $6327/kW, and**<br>**Large (1.5 MW) CapEx: $3270/kW.**<br>**https://www.nrel.gov/docs/fy24osti/88335.pdf**<br>**Distributed Wind Market Report: 2022 Edition.**Gives<br>installed costs for turbines over 100 kW as $2900/kW.<br>https://www.energy.gov/sites/default/files/2022-<br>08/distributed_wind_market_report_2022.pdf<br>**Land-Based Wind Market Report: 2024 Edition. August**<br>**2024.**|



168 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||**https://www.energy.gov/eere/wind/land-based-wind-**<br>**market-report**<br>Since 2018, Project-level costs have<br>largely held steady at ~$1,700/MW on a capacity-weighted<br>average basis<br>.|
|**O&M cost**<br>**($/kW/year)**|$42|$33–$59|**NREL (National Renewable Energy Laboratory). 2024.**<br>**"2024 Annual Technology Baseline." Golden, CO:**<br>**National Renewable Energy Laboratory.**<br>**https://atb.nrel.gov/electricity/2024/data**<br>Distributed Wind (Wind Speed Class 7), 2024 moderate<br>forecast, scaled from 2022 to 2024 dollars. Forecast is the<br>same across size classes.<br>**Land-Based Wind Market Report: 2024 Edition. August**<br>**2024.**<br>**https://www.energy.gov/eere/wind/land-based-wind-**<br>**market-report**<br>Operating expenses for recently installed projects average<br>between $20/kW/year and $30/kW/year.<br>https://www.energy.gov/sites/default/files/2022-<br>08/distributed_wind_market_report_2022.pdf|
|**Incentives**|30%<br>ITC,<br>5 year<br>MACRS<br>100%<br>bonus<br>deprecia<br>tion||**Database of State Incentives for Renewables &**<br>**Efficiency. NC Clean Energy Tech Center**<br>http://www.dsireusa.org/<br>Incentives are available at the federal, state, and local<br>level. This site provides searchable specifics about<br>incentives based on location. The following federal<br>incentives are default values in the REopt web tool:<br>**Business Energy Investment Tax Credit (ITC).**<br>**Database of State Incentives for Renewables &**<br>**Efficiency, NC Clean Energy Tech Center, updated**<br>**July 2025.**<br>https://programs.dsireusa.org/system/program/detail/658<br>Wind projects placed in service in 2023 or later and<br>beginning construction before 2033 are eligible for a 30%<br>ITC if they meet labor requirements issued by the<br>Treasury Department or are under 1 megawatt (MW-<br>AC) in size. Additional bonus credits are available for<br>meeting certain domestic content requirements and/or<br>siting in an energy community. Wind projects may<br>alternatively claim the Production Tax Credit (PTC).<br>**Modified Accelerated Cost-Recovery System**<br>**(MACRS). Database of State Incentives for**<br>**Renewables & Efficiency, NC Clean Energy Tech**<br>**Center, July 2025.**<br>http://programs.dsireusa.org/system/program/detail/676<br>Wind projects are eligible for accelerated depreciation<br>deductions over a 5-year period. The provision which<br>defines ITC technologies as eligible also adds the general|



169 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||term "wind" as an eligible technology, extending the five-<br>year schedule to large wind facilities as well.<br>**Cost recovery for qualified clean energy facilities,**<br>**property and technology**<br>https://www.irs.gov/credits-deductions/cost-recovery-for-<br>qualified-clean-energy-facilities-property-and-technology<br>Qualified clean energy facilities placed in service after<br>2024 may be classified as 5-year property via MACRS<br>under Provision 13703 of the Inflation Reduction Act of<br>2022. Qualified property includes technologies as defined<br>in § 48E and 45Y, which include wind generation placed in<br>service after 2024.<br>**Modified Accelerated Cost-Recovery System.**<br>**Database of State Incentives for Renewables &**<br>**Efficiency, NC Clean Energy Tech Center, July 2025.**<br>http://programs.dsireusa.org/system/program/detail/676<br>Pursuant to Public Law No. 119-21, qualified property<br>acquired and placed in service after January 19, 2025 may<br>qualify for 100% first year bonus depreciation. Qualified<br>property includes depreciable assets with a recovery<br>period of 20 years or less. The law additionally repealed<br>the ability of “energy property” under § 48(a)(3)(A) to<br>qualify for 5-year MACRS (projects that qualify under<br>§48E/§45Y will continue to be treated as 5-year MACRS<br>property). Thus, wind projects that qualify as §48E/45Y<br>property may utilize 100% first year bonus depreciation.|



**Table 10. Concentrating solar thermal (CST) Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**System**<br>**capital cost**<br>**($/kW) Class**|$2200||**System Advisor Model™ Version 2025.4.16 (SAM™**<br>**2025.4.16).**National Renewable Energy Laboratory.<br>Golden, CO. Accessed Sept 22, 2025.<br>https://https://sam.nrel.gov.<br>•<br>Module: Industrial Process Heat, Parabolic<br>Trough, Distributed, Commercial Owner<br>•<br>Default values used from the Installation Costs<br>section, with storage and land cost zeroed out.<br>•<br>Land is assumed to be owned by the site owner<br>•<br>Storage is costed separately.<br>The basis of the costs from the SAM reference above are<br>described in this publication, with the chosen size of about<br>5 MWt capacity parabolic trough CST:<br>Akar, S., & Kurup, P. (2024).**Parabolic Trough Collector**<br>**Cost Update for Industrial Process Heat In The United**<br>**States.**Paper presented at EuroSun 2024, Limassol,<br>Cyprus.|



170 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||https://proceedings.ises.org/conference/eurosun2024/pap<br>ers/eurosun2024-0042-Akar.pdf|
|**O&M cost**<br>**($/kW/year)**|$33||**System Advisor Model™ Version 2025.4.16 (SAM™**<br>**2025.4.16).**National Renewable Energy Laboratory.<br>Golden, CO. Accessed Sept 22, 2025.<br>https://https://sam.nrel.gov.<br>•<br>Module: Industrial Process Heat, Parabolic<br>Trough, Distributed, Commercial Owner<br>•<br>Default value for Fixed cost by capacity from the<br>Operating Costs section|
|**Inlet process**<br>**heating**<br>**temperature**<br>**(°F)**|400.0 °F||Estimated temperature at which hot thermal energy must<br>be supplied to the process or facility|
|**Return**<br>**process**<br>**heating**<br>**temperature**<br>**(°F)**|70.0 °F||Estimated temperature at which the cooled thermal energy<br>returns from the process or facility back to the CST|
|**Incentives**|0% ITC,<br>No<br>MACRS<br>or bonus<br>depreciat<br>ion||CST is not eligible for the federal ITC or MACRS or bonus<br>depreciation.|



**Table 11. High Temperature Thermal Storage Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Install cost**<br>**($/kWht)**|$86||**System Advisor Model™ Version 2025.4.16 (SAM™**<br>**2025.4.16).**National Renewable Energy Laboratory.<br>Golden, CO. Accessed Sept 22, 2025.<br>https://https://sam.nrel.gov.<br>•<br>Module: Industrial Process Heat, Parabolic<br>Trough, Distributed, Commercial Owner<br>•<br>Default value from the Installation Costs section,<br>starting with the base storage cost and applying<br>the contingency, indirect, and sales tax factors.<br>This cost is based on thermal storage capacity (thermal<br>kWh)|
|**Fixed O&M**<br>**cost**<br>**($/kWht/yr)**|$0||Any O&M associated with the CST + HT-TES system is<br>accounted for with the CST O&M default value. This value<br>may not be changed in the web tool.|
|**Thermal loss**<br>**rate (%/hour)**|0.04%||The thermal loss rate based on the thermal energy storage<br>capacity, per hour.|
|**Minimum**<br>**state of**<br>**charge (%)**|10%||The minimum percent of thermal energy capacity that is<br>maintained at all times. This value may not be changed in<br>the web tool.|



171 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Incentives**|30%<br>ITC, 5-<br>year<br>MACRS<br>100%<br>bonus<br>deprecia<br>tion||**Business Energy Investment Tax Credit (ITC)**<br>https://programs.dsireusa.org/system/program/detail/658 <br>Energy storage projects are eligible for the Investment Tax<br>Credit (ITC) under IRC §48E if placed in service after<br>2024. The Inflation Reduction Act of 2022 expanded ITC<br>eligibility to include stand-alone energy storage technology.<br>The base credit is 6% of eligible costs, increased to 30% if<br>prevailing wage and apprenticeship requirements are met,<br>with potential bonus credits for domestic content, energy<br>communities, or low-income projects. To qualify, the<br>battery must have a capacity of at least 5 kWh.<br>**Cost recovery for qualified clean energy facilities,**<br>**property and technology**<br>https://www.irs.gov/credits-deductions/cost-recovery-for-<br>qualified-clean-energy-facilities-property-and-technology<br>Qualified energy storage property placed in service after<br>2024 may be classified as 5-year property via MACRS<br>under Provision 13703 of the Inflation Reduction Act of<br>2022. Qualified property includes energy storage<br>technology as defined in 26 U.S. Code Section 48E(c)(2),<br>which includes thermal energy storage.<br>**Modified Accelerated Cost-Recovery System.**<br>**Database of State Incentives for Renewables &**<br>**Efficiency, NC Clean Energy Tech Center, July 2025.**<br>http://programs.dsireusa.org/system/program/detail/676<br>Pursuant to Public Law No. 119-21, qualified property<br>acquired and placed in service after January 19, 2025 may<br>qualify for 100% first year bonus depreciation. Qualified<br>property includes depreciable assets with a recovery<br>period of 20 years or less. The law additionally repeals the<br>ability of “energy property” under § 48(a)(3)(A) to qualify for<br>5-year MACRS (projects that qualify under §48E/§45Y will<br>continue to be treated as 5-year MACRS property). Thus,<br>energy storage projects that qualify as §48E property may<br>utilize 100% first year bonus depreciation.|
|---|---|---|---|



**Table 46. Resilience Evaluations- Load Profile Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Critical load**<br>**factor (%)**|50%|10%–<br>100%|The critical load varies widely based on building use.|



**Table 47. Resilience Evaluations- Emergency and Off-Grid Generator (Diesel) Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**System**<br>**capital cost**<br>**($/kW)**|Emerge<br>ncy<br>Generat<br>or: $650|$600-<br>$1600|Installation costs include the generator, integrated fuel<br>tank with diesel fuel, enclosure, switch gear, cabling,<br>engineering, and program management. REopt assumes<br>that the emergency generator can run in parallel with other|



172 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||if the<br>generat<br>or only<br>runs<br>during<br>outages;<br>$800 if it<br>is<br>allowed<br>to run<br>parallel<br>with the<br>grid;<br>Off-grid:<br>$880 for<br>off-grid||DERs when islanded. Generators larger than 200 kW have<br>nearly constant costs per kW. Smaller generators’ cost per<br>kW rise rapidly as the size decreases. Generators as small<br>as 25 kW typically cost $1600/kW. If the emergency<br>generator is to be run parallel to the grid it must be Tier IV<br>certified which adds approximately $150/kW to the<br>installation cost. Off-grid generator costs are likely to be<br>higher due to higher utilization and higher cooling<br>requirements. For off-grid systems manufactures may<br>derate the maximum power by 10%, resulting in a default<br>cost assumption of $880/kW. Cost estimates are based on<br>**Army Corp of Engineers estimates (Army Facilities**<br>**Pricing Guide, PAX Newsletter 3.2.2, Dated 21 May**<br>**2021) EPRI study (Cost of Utility Distributed**<br>**Generators, 1-10 MW, EPRI 2003) and Generac’s**<br>**public cost tool**<br>(https://www.generac.com/Industrial/professional-<br>resources/generator-specifying-and-sizing-tools/total-cost-<br>of-ownership-calculator)|
|**Fuel cost**<br>**($/gal)**|$2.25|$2 - $4|Default value assumes diesel fuel.<br>**Short-term Energy Outlook Data Browser. July 2025.**<br>Monthly No. 2 Diesel fuel wholesale price shows variable<br>price around $2.25/gal in 2025 and 2026. 2026 projected<br>annual cost of $2.24/gal.<br>https://www.eia.gov/outlooks/steo/data/browser/#/?v=8&f=<br>A&s=0&start=2018&end=2026&map=&linechart=~DSWH<br>UUS&maptype=0&ctype=linechart|
|**Fuel**<br>**reserve**<br>**(gallons)**|unlimite<br>d|1 -<br>unlimited|The default assumption of unlimited fuel reserve implies<br>that either a large existing centralized fuel reserve is<br>located on site or that fuel delivery from off site is<br>guaranteed even during an outage. Fuel reserve<br>limitations impact on resiliency can be explored in the<br>Energy Resilience Tool.|
|**Fixed O&M**<br>**($/kW/yr)**|Emerge<br>ncy<br>Generat<br>or: $20<br>Off-grid:<br>$10|$10-$60|Fixed annual O&M includes the costs for generator<br>maintenance, required testing, and annual fuel polishing<br>for fuel in the integrated tank. Small generators’ cost per<br>kW rises rapidly as the size decreases. For generators as<br>small as 25 kW, annual O&M costs are as high as<br>$60/kW/yr. Annual O&M are also sensitive to the size of<br>the integrated tank. Fixed O&M for off-grid generators is<br>often lower, as they will not require periodic load testing<br>nor fuel polishing. Design specific estimates can be<br>calculated from the Generac public tool<br>(https://www.generac.com/Industrial/professional-<br>resources/generator-specifying-and-sizing-tools/total-cost-<br>of-ownership-calculator).|
|**Variable O&M**<br>**($/kWh)**|$0|$0.005 -<br>$0.01|**Lazard's Levelized Cost of Energy Analysis—Version**<br>**11.0. November 2017**. (NOTE: 2020 version doesn’t<br>include diesel analysis)<br>https://www.lazard.com/media/450337/lazard-<br>levelizedcost-of-energy-version-110.pdf <br>For an output of 250-1000 kW, the Key Assumptions table|



173 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||lists a variable O&M of $0.01/kWh. However, these cited<br>costs are based on regular diesel generator use. The<br>emergency generator modeled in the REopt web tool is<br>expected to have limited use, therefore the default for<br>these costs is set to $0/kWh. The user can set a higher<br>value if the emergency generator will be used more<br>extensively.|
|**Generator fuel**<br>**higher heating**<br>**value (HHV)**<br>**(kWh/gal)**|40.7|||
|**Electric**<br>**efficiency at**<br>**100% load (%**<br>**HHV-basis)**|32.2%|27% -<br>35%|**Generator Source Website: Approximate Diesel Fuel**<br>**Consumption Chart.**February 2021<br>https://www.generatorsource.com/Diesel_Fuel_Consumpti<br>on.aspx. A constant specific fuel efficiency across<br>generator sizes and load conditions are used due to fuel’s<br>relatively small percentage of the lifecycle cost for a<br>emergency generators and due to the resulting significant<br>positive impact on solution times. The median value<br>across a size range of 20 kW to 2250 kW and a load range<br>of 25% to 100% was selected as representative.<br>See Appendix A for more detail.|
|**Electric**<br>**efficiency at**<br>**50% load (%**<br>**HHV-basis)**|32.2%|27% to<br>35%|**Generator Source Website: Approximate Diesel Fuel**<br>**Consumption Chart**. February 2021<br>https://www.generatorsource.com/Diesel_Fuel_Consumpti<br>on.aspx. A constant specific fuel efficiency across<br>generator sizes and load conditions are used due to fuel’s<br>relatively small percentage of the lifecycle cost for a<br>emergency generators and due to the resulting significant<br>positive impact on solution times. The median value<br>across a size range of 20 kW to 2250 kW and a load range<br>of 25% to 100% was selected as representative.<br>See Appendix A for more detail|
|**Emergency**<br>**Generator**<br>**replacement**<br>**year**|Emerge<br>ncy<br>Generat<br>or:<br>unlimite<br>d<br>Off-grid:<br>10||Diesel generators typically run between 15,000 – 50,000<br>hours before requiring a major engine overhaul. This<br>typical translates to a lifetime of 25 to 40 years.<br>Replacement cost is therefore not considered for<br>emergency generators in Resilience analyses.<br>If a generator were run for half the year, this would equate<br>to a lifespan of 3.5-11.5 years, a quarter of the year would<br>equate to 6.8-23 years. By default, REopt assumes a<br>single replacement of the off-grid generator in year 10.<br>**Worldwide Power Products Website: How Long Do**<br>**Diesel Generators Last?**Accessed 12/9/21.<br>https://www.wpowerproducts.com/news/diesel-engine-<br>lifeexpectancy/<br>Approximate lifespan: 12,000-20,000 hours|



174 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Minimum**<br>**turndown (%**<br>**of capacity)**|Emerge<br>ncy<br>Generat<br>or: 0%<br>Off-grid:<br>15%||The default generator minimum turndown for off-grid<br>analyses is 15% to limit the likelihood of infeasible<br>solutions while avoiding unreasonable underloading. An<br>N+1 generator capacity reserve is assumed by default,<br>and thus a 15% minimum turndown equates to one of the<br>two assumed generators running at 30% minimum<br>turndown.|



**Table 48. Combined Heat and Power Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Size Class**|||See default/reference in Section 14.8, 14.9, & Appendix A<br>Please note that an update may be pending for this data.|
|**Electric power**<br>**capacity (kW)**|||See default/reference in Section 14.8, 14.9, & Appendix A<br>Please note that an update may be pending for this data.|
|**Install cost**<br>**($/kW)**|||See default/reference in Section 14.8, 14.9, & Appendix A<br>Please note that an update may be pending for this data.|
|**Fixed O&M**<br>**cost ($/kW/yr)**|||See default/reference in Section 14.8, 14.9, & Appendix A<br>Please note that an update may be pending for this data.|
|**Variable O&M**<br>**cost ($/kWh)**|||See default/reference in Section 14.8, 14.9, & Appendix A<br>Please note that an update may be pending for this data.|
|**Incentives**|0% ITC<br>for CHP,<br>No<br>accelera<br>ted<br>MACRS<br>schedul<br>e, 100%<br>bonus<br>deprecia<br>tion||**Database of State Incentives for Renewables &**<br>**Efficiency. NC Clean Energy Tech Center, updated**<br>**October 2024.**<br>http://www.dsireusa.org/<br>Incentives are available at the federal, state, and local<br>level. This site provides searchable specifics about<br>incentives based on location. The following federal<br>incentives are default values in the REopt web tool:<br>**Investment Tax Credit (§48 and §48E)**<br>https://www.irs.gov/pub/irs-access/p6045_accessible.pdf<br>https://chpalliance.org/wp-content/uploads/2024/01/CHPA-<br>IRA-FAQ-Updated-2024.pdf<br>CHP projects that began construction prior to January 1,<br>2025 may qualify for the ITC under §48. Projects placed in<br>service on or after January 1, 2025 may only qualify for the<br>ITC (under §48E) if they meet zero emissions<br>requirements.<br>**Modified Accelerated Cost-Recovery System (MACRS).**<br>**Database of State Incentives for Renewables &**<br>**Efficiency, NC Clean Energy Tech Center, July 2025.**<br>http://programs.dsireusa.org/system/program/detail/676<br>Pursuant to Public Law No. 119-21, qualified property<br>acquired and placed in service after January 19, 2025 may<br>qualify for 100% first year bonus depreciation. Qualified<br>property includes depreciable assets with a recovery<br>period of 20 years or less. The law additionally repeals the<br>ability of “energy property” under § 48(a)(3)(A) to qualify for<br>5-year MACRS (projects that qualify under §48E/§45Y will|



175 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||continue to be treated as 5-year MACRS property). Thus,<br>CHP projects that do not meet the requirements of<br>§48E/§45Y are treated as depreciable assets with recovery<br>periods defined per Rev. Proc. 87‑56. REopt’s defaults<br>assume CHP can either be classified as an asset with a<br>recovery period less than or equal to 20-years or is used in<br>manufacturing and qualifies as asset class 00.4. By<br>default, 100% first year bonus depreciation is thus<br>assumed.|
|**CHP**<br>**maintenance**<br>**schedule**|||See default/reference in Section 14.10<br>Please note that an update may be pending for this data.|
|**Electric**<br>**efficiency at**<br>**100% load (%**<br>**HHV-basis)**|||See default/reference in Section 14.8 & Appendix A<br>Please note that an update may be pending for this data.|
|**Electric**<br>**efficiency at**<br>**50% load (%**<br>**HHV-basis)**|||See default/reference in Section 14.8<br>Please note that an update may be pending for this data.|
|**Thermal**<br>**efficiency at**<br>**100% load (%**<br>**HHV-basis**|||See default/reference in Section 14.8 & Appendix A<br>Please note that an update may be pending for this data.|
|**Thermal**<br>**efficiency at**<br>**50% load (%**<br>**HHV-basis)**|||See default/reference in Section 14.8<br>Please note that an update may be pending for this data.|
|**Min. electric**<br>**loading of**<br>**prime mover**<br>**(% rated**<br>**electric cap)**|||See default/reference in Section 14.8<br>Please note that an update may be pending for this data.|
|**Knockdown**<br>**factor for**<br>**CHP-supplied**<br>**thermal to**<br>**Absorption**<br>**Chiller (%)**|||See default/reference in Section 14.8 and Section 16<br>Please note that an update may be pending for this data.|
|**Supplementar**<br>**y firing**<br>**maximum**<br>**steam**<br>**production**<br>**ratio**|||See default/reference in Section 14.5<br>Please note that an update may be pending for this data.|
|**Supplementar**<br>**y firing**<br>**thermal**<br>**efficiency (%**<br>**HHV-basis)**|||See default/reference in Section 14.5<br>Please note that an update may be pending for this data.|
|**Installed Cost**<br>**of**|||See default/reference in Section 14.5<br>Please note that an update may be pending for this data.|



176 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Supplementar**<br>**y Firing ($/kW)**||||



**Table 49. Hot Water Storage Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Install cost**<br>**($/kW)**|||See default/reference in Section 17|
|**Fixed O&M**<br>**cost ($/gal/yr)**|||See default/reference in Section 17|
|**Thermal loss**<br>**rate (%)**|||See default/reference in Section 17|
|**Minimum**<br>**state of**<br>**charge (%)**|||See default/reference in Section 17|
|**Incentives**|30%<br>ITC, 5-<br>year<br>MACRS<br>100%<br>bonus<br>deprecia<br>tion||**Business Energy Investment Tax Credit (ITC)**<br>https://programs.dsireusa.org/system/program/detail/658 <br>Energy storage projects are eligible for the Investment Tax<br>Credit (ITC) under IRC §48E if placed in service after<br>2024. The Inflation Reduction Act of 2022 expanded ITC<br>eligibility to include stand-alone energy storage technology.<br>The base credit is 6% of eligible costs, increased to 30% if<br>prevailing wage and apprenticeship requirements are met,<br>with potential bonus credits for domestic content, energy<br>communities, or low-income projects. To qualify, the<br>battery must have a capacity of at least 5 kWh.<br>**Cost recovery for qualified clean energy facilities,**<br>**property and technology**<br>https://www.irs.gov/credits-deductions/cost-recovery-for-<br>qualified-clean-energy-facilities-property-and-technology<br>Qualified energy storage property placed in service after<br>2024 may be classified as 5-year property via MACRS<br>under Provision 13703 of the Inflation Reduction Act of<br>2022. Qualified property includes energy storage<br>technology as defined in 26 U.S. Code Section 48E(c)(2),<br>which includes thermal energy storage.<br>**Modified Accelerated Cost-Recovery System.**<br>**Database of State Incentives for Renewables &**<br>**Efficiency, NC Clean Energy Tech Center, July 2025.**<br>http://programs.dsireusa.org/system/program/detail/676<br>Pursuant to Public Law No. 119-21, qualified property<br>acquired and placed in service after January 19, 2025 may<br>qualify for 100% first year bonus depreciation. Qualified<br>property includes depreciable assets with a recovery<br>period of 20 years or less. The law additionally repeals the<br>ability of “energy property” under § 48(a)(3)(A) to qualify for<br>5-year MACRS (projects that qualify under §48E/§45Y will<br>continue to be treated as 5-year MACRS property). Thus,<br>energy storage projects that qualify as §48E property may<br>utilize 100% first year bonus depreciation.|



177 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 50. Absorption Chiller Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Coefficient of**<br>**performance**<br>**(kWt/kWt)**|||See default/reference in Section 16|
|**Electric**<br>**consumption**<br>**COP for heat**<br>**rejection**<br>**(kWt/kWe)**|||See default/reference in Section 16|
|**Install cost**<br>**($/kW)**|||See default/reference in Section 16|
|**Fixed O&M**<br>**cost ($/ton/yr)**|||See default/reference in Section 16|



**Table 51. Chilled Water Storage Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Install cost**<br>**($/kW)**|||See default/reference in Section 17|
|**Fixed O&M**<br>**Cost ($/gal/yr)**|||See default/reference in Section 17|
|**Thermal loss**<br>**rate, percent**<br>**of stored**<br>**energy (%)**|||See default/reference in Section 17|
|**Minimum**<br>**state of**<br>**charge (%)**|||See default/reference in Section 17|
|**Incentives**|30%<br>ITC, 5-<br>year<br>MACRS<br>100%<br>bonus<br>deprecia<br>tion||**Business Energy Investment Tax Credit (ITC)**<br>https://programs.dsireusa.org/system/program/detail/658 <br>Energy storage projects are eligible for the Investment Tax<br>Credit (ITC) under IRC §48E if placed in service after<br>2024. The Inflation Reduction Act of 2022 expanded ITC<br>eligibility to include stand-alone energy storage<br>technology. The base credit is 6% of eligible costs,<br>increased to 30% if prevailing wage and apprenticeship<br>requirements are met, with potential bonus credits for<br>domestic content, energy communities, or low-income<br>projects. To qualify, the battery must have a capacity of at<br>least 5 kWh.<br>**Cost recovery for qualified clean energy facilities,**<br>**property and technology**<br>https://www.irs.gov/credits-deductions/cost-recovery-for-<br>qualified-clean-energy-facilities-property-and-technology<br>Qualified energy storage property placed in service after<br>2024 may be classified as 5-year property via MACRS<br>under Provision 13703 of the Inflation Reduction Act of<br>2022. Qualified property includes energy storage<br>technology as defined in 26 U.S. Code Section 48E(c)(2),<br>which includes thermal energy storage.|



178 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Modified Accelerated Cost-Recovery System. Database of State Incentives for Renewables & Efficiency, NC Clean Energy Tech Center, July 2025.** http://programs.dsireusa.org/system/program/detail/676 Pursuant to Public Law No. 119-21, qualified property acquired and placed in service after January 19, 2025 may qualify for 100% first year bonus depreciation. Qualified property includes depreciable assets with a recovery period of 20 years or less. The law additionally repeals the ability of “energy property” under § 48(a)(3)(A) to qualify for 5-year MACRS (projects that qualify under §48E/§45Y will continue to be treated as 5-year MACRS property). Thus, energy storage projects that qualify as §48E property may utilize 100% first year bonus depreciation. 

**Table 52. Geothermal Heat Pump Inputs, Default Values, Ranges, and Sources** 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
|**Installed cost**<br>**for WAHP**<br>**heat pumps**<br>**($/ton)**|$1075||RSMeans 2018 for 5-ton unit|
|**Installed cost**<br>**for WWHP**<br>**cooing heat**<br>**pump ($/ton)**|$700||Total installed costs for WWHP are not widely used<br>equipment and reference costs are difficult to find. As a<br>proxy, costs for variable speed centrifugal chillers are<br>referenced and a cost premium of 20% is assumed and<br>added.<br>Guidehouse and Leidos; "Updated Buildings Sector<br>Appliance and Equipment Costs and Efficiencies"; U.S.<br>Energy Information Administration; March 2023;<br>Page 125, 2022 typical total installed cost of $590/ton<br>https://www.eia.gov/analysis/studies/buildings/equipcosts/<br>pdf/full.pdf|
|**Installed cost**<br>**for WWHP**<br>**heating heat**<br>**pump ($/ton)**|$700||Total installed costs for WWHP are not widely used<br>equipment and reference costs are difficult to find. As a<br>proxy, costs for variable speed centrifugal chillers are<br>referenced and a cost premium of 20% is assumed and<br>added.<br>Guidehouse and Leidos; "Updated Buildings Sector<br>Appliance and Equipment Costs and Efficiencies"; U.S.<br>Energy Information Administration; March 2023;<br>Page 125, 2022 typical total installed cost of $590/ton<br>https://www.eia.gov/analysis/studies/buildings/equipcosts/<br>pdf/full.pdf|
|**Installed cost**<br>**GHX ($/ft)**|$14|$7-$23|Liu, Xiaobing; Hughes, Patrick; McCabe, Kevin; et al.;<br>"GeoVision Analysis Supporting Task Force Report:<br>Thermal Applications - Geothermal Heat Pumps";<br>ORNL/TM-2019/502; April 2019|



179 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||Default is the national average value.|
|**Installed cost**<br>**building**<br>**interior GHX**<br>**hydronic loop**<br>**($/ft2) **|$1.70||Liu, Xiaobing; Hughes, Patrick; McCabe, Kevin; et al.;<br>"GeoVision Analysis Supporting Task Force Report:<br>Thermal Applications - Geothermal Heat Pumps";<br>ORNL/TM-2019/502; April 2019|
|**Installed cost**<br>**for hybrid**<br>**auxiliary**<br>**boiler**<br>**($/MMBtu/hr)**|$26,000||Doheny, Matthew. Building Construction Costs with<br>RSMeans Data, 2022. Ed. Matthew Doheny. 80th annual<br>edition. Greenville, SC: Gordian/RSMeans Data, 2021.<br>Print.<br>US Energy Information Administration; “Updated Buildings<br>Sector Appliance and Equipment Costs and Efficiencies”;<br>January 2023. Accessed March 2023:<br>https://www.eia.gov/analysis/studies/buildings/equipcosts/<br>pdf/full.pdf|
|**Installed cost**<br>**for hybrid**<br>**auxiliary**<br>**cooling tower**<br>**($/ton)**|$400||Doheny, Matthew. Building Construction Costs with<br>RSMeans Data, 2022. Ed. Matthew Doheny. 80th annual<br>edition. Greenville, SC: Gordian/RSMeans Data, 2021.<br>Print.|
|**O&M cost**<br>**($/ft2-yr)**|-$0.51<br>(negativ<br>e)||Liu, Xiaobing; Hughes, Patrick; McCabe, Kevin; et al.;<br>"GeoVision Analysis Supporting Task Force Report:<br>Thermal Applications - Geothermal Heat Pumps";<br>ORNL/TM-2019/502; April 2019|
|**Incentives**|30%<br>ITC,<br>No<br>MACRS<br>0%<br>bonus<br>deprecia<br>tion||**Database of State Incentives for Renewables &**<br>**Efficiency. NC Clean Energy Tech Center**<br>http://www.dsireusa.org/<br>Incentives are available at the federal, state, and local<br>level. This site provides searchable specifics about<br>incentives based on location. The following federal<br>incentives are default values in the REopt web tool:<br>**Business Energy Investment Tax Credit. Database of**<br>**State Incentives for Renewables & Efficiency, NC**<br>**Clean Energy Tech Center, July 2025.**<br>https://programs.dsireusa.org/system/program/detail/658<br>GHP projects placed in service in 2023 or later and<br>beginning construction before 2033 are eligible for a 30%<br>ITC if they meet labor requirements issued by the<br>Treasury Department or are under 1 megawatt (MW-<br>AC) in size. Additional bonus credits are available for<br>meeting certain domestic content requirements and/or<br>siting in an energy community. The tax credit is not<br>available for systems that begin construction after<br>December 31, 2025 if that facility or property includes any<br>material assistance from a prohibited foreign entity.<br>**Modified Accelerated Cost-Recovery System.**<br>**Database of State Incentives for Renewables &**<br>**Efficiency, NC Clean Energy Tech Center, July 2025.**<br>http://programs.dsireusa.org/system/program/detail/676|



180 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

|**Input**|**Default**<br>**Value**|**Range**|**Source**|
|---|---|---|---|
||||Pursuant to Public Law No. 119-21, qualified property<br>acquired and placed in service after January 19, 2025 may<br>qualify for 100% first year bonus depreciation. Qualified<br>property includes depreciable assets with a recovery<br>period of 20 years or less. The law additionally repeals the<br>ability of “energy property” under § 48(a)(3)(A) to qualify<br>for 5-year MACRS (projects that qualify under §48E/§45Y<br>will continue to be treated as 5-year MACRS property).<br>Thus, GHP projects, which can qualify as § 48 energy<br>property but not under §48E/§45Y, are treated as<br>depreciable assets with recovery periods defined per<br>Rev. Proc. 87‑56. REopt’s default assumptions assume the<br>GHP is treated as building equipment with a recovery<br>period of 39 years and thus is not eligible for first year<br>bonus depreciation nor accelerated depreciation.|



## **References** 

American Society of Heating, Refrigerating and Air-Conditioning Engineers. (2016). _ASHRAE Handbook. HVAC Systems and Equipment. Chapter 51, Thermal Storage._ ASHRAE. ASHRAE. (2015). _Combined Heat and Power Design Guide._ ASHRAE. 

Becker, W., Cutler, D., Anderson, K., & Olis, D. (2019). REopt: Enabling Renewable Energy, Storage, and Combined Heat and Power. _ACEEE Summer Study on Energy Efficiency in Industry._ Portland, OR. 

- Cutler, D., Olis, D., Elgqvist, E., Li, X., Laws, N., Diorio, N., . . . Anderson, K. (2017). _REopt: A Platform for Energy System INtegration and Optimization._ Golden: National Renewable Energy Laboratory. 

- Deddousi, I., & Barrett, S. (2014). Air pollution and early deaths in the United States. Part II: Attribution of PM2.5 exposure to emissions species, time, location and sector. _Atmospheric Environment, 99_ , 610-617. 

- Dedoussi, I. C., Eastham, S. D., Monier, E., & Barrett, S. R. (2020). Premature mortality related to United States cross-state air pollution. _Nature_ , 261-265. 

- Dedoussi, I., & Barrett, S. (2014). Air pollution and early deaths in the United States. Part II: Attribution of PM2.5 exposure to emissions species, time, location and sector. _Atmospheric Environment, 99_ , 610-617. 

- Department of Energy Advanced Manufacturing Office. (2017). _Absorption Chillers for CHP Systems (DOE CHP Technology Fact Sheet Series)- Fact Sheet, 2017._ Retrieved from https://www.energy.gov/eere/amo/downloads/absorption-chillers-chp-systems-doe-chptechnology-fact-sheet-series-fact-sheet 

- Department of Energy Advanced Manufacturing Office. (2017). _Combined Heat and Power Basics._ Retrieved from Fact Sheets: https://www.energy.gov/eere/amo/combined-heatand-power-basics 

Dobos, A. (2014). _PVWatts version 5 manual._ Golden: National Renewable Energy Laboratory. 

Dorgan, C. E., & Elleson, J. S. (1993). _Design guide for cool thermal storage._ Atlanta: American Society of Heating, Refrigerating and Air-Conditioning Engineers. 

181 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

- Draxl, C., Hodge, B.-M., Clifton, A., & McCaa, J. (2015). _Overview and Meteorological Validation of the Wind Integration National Dataset Toolkit._ Golden: National Renewable Energy Laboratory. 

- Fuller, S. K., & Petersen, S. R. (1995). _Life-Cycle Costing Manual for the Federal Energy Management Program._ Boulder: National Insitute of Standards and Technology. 

- Gagnon, P. S. (2024). _Cambium 2023 Scenario Descriptions and Documentation._ Golden, CO: National Renewable Energy Laboratory. 

- Gagnon, P., Frazier, W., Hale, E., & Cole, W. (2020). _Cambium data for 2020 Standard Scenarios_ . Retrieved from https://cambium.nrel.gov/ 

- _GHG Emission Factors Hub_ . (2023). Retrieved from 

   - https://www.epa.gov/climateleadership/ghg-emission-factors-hub 

- Glazer, J. (2019). _Design Guide for Cool Thermal Storage, 2nd Edition._ American Society of Heat, Refrigeration, and Air-Conditioning Engineers. 

- Heo, J., Adams, P. J., & Gao, H. O. (2017). Public health costs accounting of inorganic PM2.5 pollution in metropolitan areas of the United States using a risk-based source-receptor model. _Environment International_ , 119-126. 

- Hirwa, J. O. (2021). Optimizing Design and Dispatch of a Renewable Energy System with Combined Heat and Power. _Submitted to: Optimization and Engineering_ . 

- Interagency Working Group on Social Cost of Greenhouse Gases, United States Government. (2021). _Technical Support Document: Social Cost of Carbon, Methane, and Nitrous Oxide._ 

- IPCC. (2022). _Climate Change 2022: Impacts, Adaptation, and Vulnerability._ Contribution of Working Group II to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change [H.-O. Pörtner, D.C. Roberts, M. Tignor, E.S. Poloczanska, K. Mintenbeck, A. Alegría, M. Craig, S. Langsdorf, S. Löschke, V. Möller, A. Okem, . Cambridge, UK and New York, NY, USA: Cambridge University Press. 

- Lantz, E., Sigrin, B., Gleason, M., Preus, R., & Baring-Gould, I. (2016). _Assessing the Future of Distributed Wind: Opportunities for Behind-the-Meter Projects._ Golden: National Renewable Energy Laboratory. 

- Lawrence Berkeley National Laboratory. (2019). _Combined Heat and Power eCatalog_ . Retrieved from https://chp.ecatalog.lbl.gov/ 

- MacCraken, M. (2004). Thermal Energy Storage in Sustainable Buildings. _ASHRAE Journal_ . 

- NASA. (2024, January). _Carbon Dioxide_ . Retrieved from Global Climate Change: https://climate.nasa.gov/vital-signs/carbon-dioxide/ 

- Ogunmodede, O. A. (2021). Optimizing Design and Dispatch of a Renewable Energy System. _Accepted for Publication: Applied Energy_ . 

- Pacific Northwest National Laboratory. (2016). _ANSI/ASHRAE/IES Standard 90.1-2010 Performance Rating Method Reference Manual, PNNL-25130._ Richland: Pacific Northwest National Laboratory. 

- Ramasamy, V., Feldman, D., Margolis, R., & Desai, J. (2021). _U.S. Solar Photovoltaic System and Energy Storage Cost Benchmarks: Q1 2021._ Golden: NREL. 

- Rushing, A. S., Kneifel, J. D., & Lippiatt, B. C. (2013). _Energy Price Indices and Discount Factors for Life-Cycle Cost Analysis._ Boulder: National Institute of Standards and Technology. 

182 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

- Ryan, N., Johnson, J. X., & Keoleian, G. (2016). Comparative Assessment of Models and Methods To Calculate Grid Electricity Emissions. _Environmental Science & Technology_ , 8937-8953. 

- Sergi, B. J., Adams, P., Muller, N., Robinson, A., Davis, S., Marshall, J., & Azevedo, I. (2020). Optimizing Emissions Reductions from the U.S. Power Sector for Climate and Health Benefits. _Environmental Science & Technology_ , 7513−7523. 

- Short, W., Packey, D., & Holt, T. (1995). _A Manual for the Economic Evaluation of Energy Efficiency and Renewable Energy Technologies._ Golden: National Renewable Energy Laboratory. 

- Sweetser, R. (2020, June). Exergy Partners Corporation. _Personal Communication_ . 

- U.S. Environmental Protection Agency. (2015). _Fuel and Carbon Dioxide Emissions Savings Calculation Methodology for Combined Heat and Power Systems._ Washington, D.C.: U.S. Environmental Protection Agency. 

- U.S. Environmental Protection Agency. (2018, March). _Emission Factors for Greenhouse Gas Inventories._ Retrieved from https://www.epa.gov/sites/production/files/201803/documents/emission-factors_mar_2018_0.pdf 

- U.S. Environmental Protection Agency. (2019). _AVoided Emissions and geneRation Tool (AVERT) User Manual, Version 2.3._ Washington, D.C.: US Environmental Protection Agency. 

- U.S. Environmental Protection Agency. (2020, March 9). _eGrid2018._ Retrieved from Download Data: https://www.epa.gov/egrid/download-data 

- U.S. Environmental Protection Agency. (2023). _eGRID 2021 Data._ Retrieved from eGRID: https://www.epa.gov/egrid/download-data 

- U.S. Environmental Protection Agency. (n.d.). _WebFIRE_ . Retrieved from https://cfpub.epa.gov/webfire/ 

- United States Government Interagency Working Group on Social Cost of Greenhouse Gases. (2016). _Technical Support Document: Technical Update of the Social Cost of Carbon for Regulatory Impact Analysis Under Executive Order 12866._ Washington D.C. : U.S. Environmental Protection Agency. 

- Vaishnav, P., Horner, N., & Azevedo, I. L. (2017). Was it worthwhile? Where have the benefits of rooftop solar photovoltaic generation exceeded the cost? _Environmental Research Letters_ . 

183 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **Appendix A: CHP Cost and Performance Data by Prime Mover Type and Size Class** 

The cost and performance data in Section 14.8, Topping Cycle Default CHP Cost & Performance Parameters by Prime Mover Type & Size Class, was generated by averaging the available data within the size class range from the DOE CHP Fact Sheets (DOE Advanced Manufacturing Office 2017). The following tables show the raw data and highlights the data that was averaged to get the size class cost and performance parameters. For fuel cells, the DOE CHP Fact Sheet data for phosphoric acid fuel cells (PAFC) and molten carbonate fuel cells (MCFC) was heavily modified by industry estimates. 

|**Reciprocating Engine**||||**System**|**System**||||
|---|---|---|---|---|---|---|---|---|
||1|2|3|4|5|6|7|8|
|Net Electric Power(kW)|35|99|248|495|990|1,980|2,970|4,455|
|Fuel Input(MMBtu/hr,HHV)|0.43|1.14|2.58|4.65|9.18|16.80|25.10|37.40|
|Useful Thermal,Hot Water(MMBtu/hr)|0.23|0.57|1.21|1.95|3.85|6.45|9.65|14.40|
|CoolingThermal Factor(Single Effect)|80%|80%|85%|85%|85%|85%|85%|85%|
|Electric Efficiency (%,HHV,netpower basis)|27.7%|29.7%|32.7%|36.3%|36.8%|40.2%|40.4%|40.6%|
|Hot Water Thermal Efficiency (%,HHV)|54.0%|50.0%|47.0%|41.9%|41.9%|38.4%|38.4%|38.5%|
|Steam Thermal Efficiency (%,HHV)|N/A|N/A|N/A|18.3%|15.5%|12.9%|13.0%|11.2%|
||||||||||
|O&M Cost($/kWh)|$0.030|$0.025|$0.022|$0.020|$0.017|$0.015|$0.014|$0.013|
|**Total Installed Cost($/kW)**|$4,250|$3,700|$3,450|$3,150|$2,800|$2,550|$2,350|$2,000|
|_REopt Class 0_|||||||||
|_REopt Class 1_|||||||||
|_REopt Class 2_|||||||||
|_REopt Class 3_|||||||||
|_REopt Class 4_|||||||||
|_REopt Class 5_|||||||||
|_REopt Class 6_|||||||||
|_REopt Class 7_|||||||||



|**Microturbine**|1|**System**|**System**||
|---|---|---|---|---|
|||2|3|4|
|Net Electric Power(kW)|61|190|570|950|
|Fuel Input(MMBtu/hr,HHV)|0.84|2.30|6.90|11.40|
|Useful Thermal,Hot Water(MMBtu/hr)|0.39|0.90|2.60|4.30|
|CoolingThermal Factor(Single Effect)|94%|194%|294%|394%|
|Electric Efficiency (%,HHV,netpower basis)|24.8%|28.2%|28.2%|28.4%|
|Hot Water Thermal Efficiency (%,HHV)|46.4%|39.1%|37.7%|37.7%|
|Steam Thermal Efficiency (%,HHV)|N/A|N/A|N/A|N/A|
||||||
|O&M Cost($/kWh)|$0.014|$0.017|$0.015|$0.013|
|**Total Installed Cost($/kW)**|$4,900|$4,400|$3,700|$3,400|
|_REopt Class 0_|||||
|_REopt Class 1_|||||
|_REopt Class 2_|||||
|_REopt Class 3_|||||



184 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [468 x 194] intentionally omitted <==**

**==> picture [468 x 322] intentionally omitted <==**

185 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

Back-pressure steam turbine performance data from the DOE CHP Fact Sheets: 

**==> picture [463 x 443] intentionally omitted <==**

186 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

Back-pressure steam turbine cost data from the DOE CHP Fact Sheets: 

**==> picture [468 x 199] intentionally omitted <==**

**Appendix B: Efficiency Gain Potential of GHP Retrofit in Facilities with Variable-Air-Volume HVAC Equipment** This appendix describes the methodology used to estimate the excess heating and cooling associated with inefficient sub-cooling-and-reheat-based multi-zone VAV HVAC design that could be eliminated with GHP retrofit. This work is to approximate efficiency gains that may be available within facilities with VAV when retrofitted with distributed water-to-air heat pumps. See Section 18.6 for an introduction on this topic. 

In VAV systems, multiple spaces are often served by one HVAC unit. Because of this, these systems can have inherent inefficiencies. Inefficiencies can occur when spaces served by a single central air handling unit have different levels of heating or cooling needs. When this occurs, the air supplied to the duct is cooled to meet the worst-case need. The following describes a scenario that results in excessive cooling and heating: 

1. The central air handler supplies air to individual VAV boxes at a temperature suitable for space cooling. 

2. When zones have different levels of cooling need, the dampers in the VAV box adjust the flowrate of conditioned air to match the zone’s cooling requirement. A fully open damper provides the maximum amount of cooling to a zone. As less and less cooling is needed, the damper position adjusts down to a minimum stop position, which is typically specified to ensure adequate ventilation. 

3. At a damper’s minimum stop position, if space cooling sill exceeds the cooling needs of the zone, the zone will be cooled below the upper limit of the thermostat setting. Cooling below the thermostat upper limit is considered excessive because it is more than is needed to provide thermal comfort according to the definition of the space dead-band. 

187 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

4. If the cooling provided at the minimum stop position were excessive to the point where the lower dead-band temperature limit of the thermostat is reached, the airstream is often ‘reheated’ at the VAV box to keep the zone above the thermostat’s lower temperature limit. At this point, excessive cooling is exacerbated by simultaneous heating to offset it. 

Outside air, or ventilation air, is often mixed at the intake of the central HVAC unit and oftentimes this air needs to be dehumidified. Dehumidification is often done via subcooling to wring moisture until the desired humidity level is achieved. In our analysis, we assume subcooling for dehumidification is a requirement of the system, and therefore not excessive regardless of space conditioning requirements.  Additionally, where reheat is needed at the zone level, the portion of that reheat needed to offset subcooling of ventilation air needed for dehumidification is also not considered excessive. 

In this analysis: 

1. We assume all cooling below the upper limit of the thermostat space temperature is excessive. This excessive cooling is considered an inefficiency that a GHP retrofit could eliminate. 

2. We assume all reheat applied to offset over-cooling _beyond_ what is needed to temper ventilation air that was sub-cooled for dehumidification is excessive. This additional reheat is considered an inefficiency that a GHP retrofit could eliminate. 

An analysis was done to estimate HVAC inefficiencies in facilities with VAV HVAC systems using DOE Commercial Reference Buildings (CRB). EnergyPlus is used and accessed via OpenStudio. The following CRB reference building types contain multi-zone VAV systems with zone-level reheat and therefore have potential for efficiency gain with a GHP retrofit: 

1. Large Office 

2. Medium Office 

3. Large Hotel 

4. Primary School 

5. Secondary School 

6. Hospital 

7. Outpatient Healthcare 

The thermal loads to be served by the HVAC system include the heating and cooling needed for each conditioned space as well as the additional heating and cooling required for ventilation air. While the sensible zone-level heating and cooling thermal loads are provided directly from EnergyPlus, estimating the required versus excess cooling and heating at the building level is more involved. 

Firstly, the conditioning needed for the ventilation air is inherently tied to the ventilation strategy used in the building. For more advanced systems, a dedicated outside air system (DOAS) could be employed to handle ventilation separate from space conditioning. Since this analysis leverages the reference building models, which do not contain DOAS, this analysis assumes no DOAS. 

188 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

We also assume that the sub-cooling and reheat required for humidity control are required loads and that these loads too will need to be served by GHP. It is the excessive cooling beyond that needed for dehumidification and space conditioning that can occur in multi-zone VAV that is being estimated for elimination by GHP retrofit. In the application of the results in REopt, we currently assume reheat is hydronic and that the reheat load is within the facility entered gas heating loads. In a future update to REopt, accounting for electric reheat in the CRBs and the impact of eliminating inefficient reheat on the facility electric load will be included. 

It is also assumed that the ventilation airstream needs to be cooled to 55°F to sufficiently dehumidify the building. This is a generic assumption that may or may not match what a system designer would specify. Seasonal resets are often employed to reduce excessive subcooling, however we do not consider seasonal resets in this analysis. 

All heating and cooling done by multi-zone VAV systems with reheat was analyzed and corrected as necessary. Heating and cooling done by other air-loops are assumed to remain unchanged with GHP retrofit with the exception of CRB Hospital and Outpatient Healthcare. For these building types, load corrections were only done for multi-zone VAV systems serving noncritical zones. Healthcare HVAC systems (and the corresponding code requirements) are complex and the correction assumptions approach taken here are not fully applicable in those facilities. For healthcare facilities’ HVAC systems serving critical zones, loads were assumed to be unchanged with GHP retrofit. This is likely a conservative approach since there is likely waste in those systems as well. 

## **Details of Load Correction Calculations** 

Relevant quantities were calculated as follows: 

- **Reheat.** Not all heating done at the zone terminals is reheat. Heating is only reheat when it is canceling out mechanical cooling (i.e., mechanical cooling is done at the AHU to cool the mixed air stream to 55°F, and the portion of that air stream delivered to a zone is reheated to maintain the zone heating setpoint). Reheat is calculated as the amount of zone terminal heating needed to cancel out the net sensible cooling done by the AHU chilled water coils (coil sensible cooling load – fan heat). 

- **Credited reheat.** This is the reheat needed to cancel out the sub-cooling required to dehumidify the ventilation air. This is the smaller between the actual reheat energy and the amount of heating needed to balance the net sensible ventilation cooling load (sensible ventilation cooling – fan power for AHUs in cooling mode). 

- **Excess reheat.** This is reheat above which is needed to cancel out the net sub-cooling required to dehumidify the ventilation air. In most cases this makes up a small percentage of total reheat. 

- **Excess AHU heat.** This is applicable only in cases where simultaneous cooling and heating are done at the central air handler. Realistically, this should only happen for these system types if there is a control logic issue.  As such, this should be zero or very close to zero for all cases. 

- **Total ventilation cooling load.** The total cooling load (including the latent load) required to cooling the outdoor air stream to 55°F. This is based on the enthalpy difference between outdoor air at current conditions when that air is cooled to 55°F (which may or may not 

189 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

achieve a saturated condition). Mass flow rate is taken directly from the EnergyPlus simulation. 

- **Sensible ventilation cooling load.** Similar to above but just the sensible component (calculated based on the temperature difference). 

- **Latent ventilation cooling load.** The difference between the total and sensible loads. 

- **Sensible cooling provided by outdoor air.** When the ventilation air is cooled to 55°F, the resulting sensible cooling can meet all or most of the zone cooling load most of the time. When outdoor air is colder than 55°F, this load is based on the temperature difference between the AHU return air stream and the outdoor air (and the mass flow is the outdoor air flow rate). When outdoor air is warmer than 55°F, this load is based on the temperature difference between AHU return air stream and 55°F (and the mass flow is the outdoor air flow rate). 

- **Excess total cooling.** This is calculated as total cooling minus the total ventilation cooling load, the fan power of AHUs in cooling mode, and any excess zone cooling load above the sensible cooling provided by the ventilation load. 

- **Corrected Heating Demand – Excess Reheat and AHU Heat Removed.** This is the total heating load for the building minus excess reheat and any excess AHU heat. This is the heating load to be passed to the GHP model. 

- **Corrected Total Cooling Demand - Excess Removed.** This is the total cooling load for the building minus excess total cooling.  This is the total cooling load to be passed to the GHP model. 

## **Analysis Findings** 

The results of the analysis are summarized in the tables below. Note that the defaults in REopt are currently using the results from the 1989 ASHRAE 90.1 code shown in Table 51. The results in Table 52 are included for reference. 

190 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**Table 53. Default thermal correction factors in percentage (%) by climate zone and building type (ASHRAE 90.1 1989)** 

|Building<br>Type|Thermal<br>Load|1A|2A|2B|3A|3B|3C|4A|4B|4C|5A|5B|6A|6B|7A|8A|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Large Office|Heating|63|33|62|65|83|49|73|94|91|97|97|98|97|98|99|
||<br>Cooling|50|50|40|46|39|34|44|38|33|38|38|38|36|36|31|
|Medium<br>Office|Heating|70|55|58|81|78|46|88|92|88|97|96|98|97|98|99|
||Cooling|67|63|59|59|55|43|57|56|38|49|56|49|50|46|40|
|Primary<br>School|Heating|87|93|78|98|88|76|99|95|94|98|97|99|98|99|99|
||Cooling|88|88|79|85|74|63|85|72|58|72|75|73|72|72|64|
|Secondary<br>School|Heating|93|97|88|99|95|88|100|98|98|99|99|99|98|99|99|
||Cooling|92|92|88|90|86|75|90|86|75|79|83|76|76|71|59|
|Hospital|Heating|76|65|66|62|72|62|67|79|82|85|84|87|88|89|93|
||Cooling|74|73|68|69|68|63|69|71|70|70|73|70|74|71|73|
|Outpatient|Heating|99|89|83|86|87|79|71|89|88|92|92|94|94|95|97|
||Cooling|84|85|77|81|77|70|69|76|73|74|77|75|76|75|73|
|Large Hotel|Heating|100|93|84|95|91|84|98|95|95|99|97|99|98|99|99|
||Cooling|91|92|87|87|83|81|88|80|82|85|79|82|81|80|77|



**Table 54. Thermal correction factors in percentage (%) by climate zone and building type for ASHRAE 90.1 2007.** 

|Building<br>Type|Thermal<br>Load|1A|2A|2B|3A|3B|3C|4A|4B|4C|5A|5B|6A|6B|7A|8A|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Large Office|Heating|99|76|81|94|96|79|81|98|96|99|99|100|99|100|100|
||<br>Cooling|77|79|64|78|66|66|67|67|73|73|70|73|74|75|79|
|Medium<br>Office|Heating|99|63|76|89|95|77|86|98|96|99|99|99|99|100|100|
||Cooling|75|75|62|70|59|48|56|55|41|52|56|53|52|52|45|
|Primary<br>School|Heating|96|98|93|99|99|74|100|100|98|99|100|100|100|100|100|
||Cooling|95|97|84|94|83|75|93|81|73|81|83|81|81|81|80|
|Secondary<br>School|Heating|100|95|86|98|94|73|99|98|96|99|99|99|99|99|100|
||Cooling|94|95|91|94|90|86|94|91|88|89|91|88|92|89|92|
|Hospital|Heating|100|99|95|99|95|93|82|97|97|98|98|98|99|99|99|
||Cooling|95|95|92|94|92|81|84|92|87|88|93|89|91|89|90|
|Outpatient|Heating|99|89|83|86|87|79|71|89|88|92|92|94|94|95|97|
||Cooling|84|85|77|81|77|70|69|76|73|74|77|75|76|75|73|
|Large Hotel|Heating|98|90|91|94|96|80|96|97|94|98|99|99|99|99|99|
||Cooling|72|74|73|67|69|46|65|69|41|56|68|59|60|55|43|



191 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## **Appendix C: ASHP Performance Data** 

Heat pump performance data was collected for multiple units relevant for the commercial and industrial scale applications (10 – 100 ton units). A linear fit was manually applied to approximately match the average performance across the units as a function of outdoor air temperature. The linear fit allows performance estimates below and above the minimum and maximum temperature data points from the data source. The linear fit was then used to create the four default data points used in the “performance (COP and CF) versus temperature” tables as inputs to REopt. 

The default four data points all fall on the same linear fit. Even though only the minimum and maximum temperature data points would be required with linear interpolation between consecutive data points to represent the performance, the default table provides a more flexible “template” from which users can update/customize performance values at one or more of the data points to represent the unique aspects of particular ASHP units that they would like to evaluate. As shown in the charts, there are non-linear dependencies with some units, and that can be captured by inputting custom performance at different temperatures. REopt **linearly interpolates between consecutive data points provided** , but the relationship across all data points does not have to be linear. The performance at the input minimum and maximum temperature data points is assumed to stay the same, instead of extrapolating below or above those values, so it is important to provide an estimate of the performance that captures the minimum and maximum expected outdoor air temperature at the site. 

**==> picture [468 x 282] intentionally omitted <==**

**Figure 28. ASHP coefficient of performance (COP) data for heating from which the linear curve fit is used to determine the default performance; this applies to both ASHP for space heating and ASHP Water Heater defaults.** 

192 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [468 x 185] intentionally omitted <==**

**Figure 29. ASHP capacity factor (CF) data for heating from which the linear curve fit is used to determine the default performance; this applies to both ASHP for space heating and ASHP Water Heater defaults.** 

**==> picture [468 x 207] intentionally omitted <==**

**Figure 30. ASHP coefficient of performance (COP) data for cooling from which the linear curve fit is used to determine the default performance; this applies to ASHP for space cooling defaults.** 

193 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

**==> picture [468 x 165] intentionally omitted <==**

**Figure 31. ASHP capacity factor (CF) data for cooling from which the linear curve fit is used to determine the default performance; this applies to ASHP for space cooling defaults.** 

194 

This report is available at no cost from the National Renewable Energy Laboratory at www.nrel.gov/publications. 

## REopt[TM] 

## **1 Appendix** D **: Mathematical Formulation** 

We define, in alphabetic order within a group, indices and sets, parameters, and variables, in that order, and then state the objective function and the constraints. We choose as our naming convention calligraphic capital letters to represent sets, lower-case letters to represent parameters, and upper-case letters to represent variables; in the latter case, _Z_ -variables are binary. _X_ -variables represent continuous decisions, e.g., quantities of energy. All subscripts denote indices. Names with the same “stem” are related, and superscripts and “decorations” (e.g., hats, tildes) differentiate the names with respect to, e.g., various indices included in the name or maximum and minimum values for the same parameter. 

## **1.1 Sets and Parameters** 

## **Sets** 

|**ts**|||
|---|---|---|
|_B_||Storage systems|
|_C_||Technology classes|
|_D_||Time-of-use demand periods|
|_E_||Electrical time-of-use demand tiers|
|_F_||Fuel types|
|_H_||Time steps|
|_K_||Subdivisions of power rating|
|_M_||Months of the year|
|_N_||Monthly peak demand tiers|
|_P_||Pollutant types|
|_P_r|_⊆P_|Pollutant types with emissions reduction targets|
|_S_||Power rating segments|
|_T_||Technologies|
|_U_||Total electrical energy pricing tiers|
|_V_||Net metering regimes|



## **Subsets and Indexed Sets** 

|**Subsets and **|**Indexed Sets**|
|---|---|
|_B_c _⊆B_th|Cold thermal energy storage systems|
|_B_e _⊆B_|Electrical storage systems|
|_B_h _⊆B_th|Hot thermal energy storage systems|
|_B_th _⊆B_|Thermal energy storage systems|
|_H_g _⊆H_|Time steps in which grid purchasing is available|
|_Hm ⊆H_|Time steps within a given month _m_|
|_Hd ⊆H_|Time steps within electrical power time-of-use demand tier _d_|
|_Kt ⊆K_|Subdivisions applied to technology _t_|
|_K_c _⊆K_|Capital cost subdivisions|
|_M_lb|Look-back months considered for peak pricing|
|_Stk ⊆S_|Power rating segments from subdivision _k_ applied to technol-|
||ogy _t_|



1 

|_Tb ⊆T_|Technologies that can charge storage system _b_|
|---|---|
|_Tc ⊆T_|Technologies in class _c_|
|_Tf ⊆T_|Technologies that burn fuel type _f_|
|_Tu ⊆T_|Technologies that may access energy sales pricing tier _u_|
|_Tv ⊆T_|Technologies that may access net-metering regime _v_|
|_T_ ac _⊆T_ cl|Absorption chillers|
|_T_ CHP _⊆T_ f|CHP technologies|
|_T_ cl _⊆T_|Cooling technologies|
|_T_ e _⊆T_|Electricity-producing technologies|
|_T_ ec _⊆T_ cl|Electric chillers|
|_T_ f _⊆T_ e|Fuel-burning, electricity-producing technologies|
|_T_ ht _⊆T_|Heating technologies|
|_T_ s _⊆T_|Technologies that can provide operating reserves|
|_T_ td _⊆T_|Technologies that cannot turn down, i.e., PV and wind|
|_U_nm _⊆Us_|Electrical energy sales pricing tiers used in net metering|
|_U_p _⊆U_|Electrical energy purchase pricing tiers|
|_U_s _⊆U_|Electrical energy sales pricing tiers|
|_U_s<br>_t ⊆U_s|Electrical energy sales pricing tiers accessible by technology _t_|
|_U_sb _⊆U_s|Electrical energy sales pricing tiers accessible by storage|



## **Scaling Parameters** 

|Γ|Number of time periods within a day|[-]|
|---|---|---|
|∆|Time step scaling|[h]|
|Θ|Peak load oversizing factor|[-]|
|_M_|Sufciently large number|[various]|



## **Parameters for Costs and their Functional Forms** 

|_c_afc|Utility annual fxed charge|[$]|
|---|---|---|
|_c_amc|Utility annual minimum charge|[$]|
|_c_cb<br>_ts_|_y_-intercept of capital cost curve for technology _t_ in segment _s_|[$]|
|_c_cm<br>_ts_|Slope of capital cost curve for technology _t_ in segment _s_|[$/kW]|
|_c_e<br>_uh_|Export rate for energy in energy demand tier _u_ in time step _h_|[$/kWh]|
|_c_g<br>_uh_|Grid energy cost in energy demand tier _u_ during time step _h_|[$/kWh]|
|_c_f<br>_p_|Marginal cost of emissions for pollutant _p_ related to on-site|[$/ton]|
||fuel burn in the frst year||
|¯_c_g<br>_p_|Marginal cost of emissions for pollutant _p_ related to grid-|[$/ton]|
||purchased electricity in the frst year||
|_c_kW<br>_b_|Capital cost of power capacity for storage system _b_|[$/kW]|
|_c_kWh<br>_b_|Capital cost of energy capacity for storage system _b_|[$/kWh]|
|_c_omb<br>_b_|Operation and maintenance cost of storage system _b_ per unit|[$/kWh]|
||of energy rating||
|_c_omp<br>_t_|Operation and maintenance cost of technology _t_ per unit of|[$/kWh]|
||production||
|_c_om_σ_<br>_t_|Operation and maintenance cost of technology _t_ per unit of|[$/kW]|
||power rating, including standby charges||
|_c_r<br>_de_|Cost per unit peak demand in time-of-use demand period _d_|[$/kW]|
||and tier _e_||



2 

_c_[rm] _mn_ Cost per unit peak demand in tier _n_ during month _m_ [$/kW] _c_[u] _f_ Unit cost of fuel type _f_ [$/MMBTU] 

## **Demand Parameters** 

|_δ_c<br>_h_|Cooling load in time step _h_|[kW]|
|---|---|---|
|_δ_d<br>_h_|Electrical load in time step _h_|[kW]|
|¯_δ_gs<br>_u_|Maximum allowable sales in electrical energy demand tier _u_|[kWh]|
|_δ_h<br>_h_|Heating load in time step _h_|[kW]|
|_δ_lp|Look-back proportion for ratchet charges|[fraction]|
|¯_δ_mt<br>_n_|Maximum monthly electrical power demand in peak pricing|[kW]|
||tier _n_||
|¯_δ_t<br>_e_|Maximum power demand in time-of-use demand tier _e_|[kW]|
|¯_δ_tu<br>_u_|Maximum monthly electrical energy demand in tier _u_|[kWh]|
|_δ_<br>an|Minimum annual load that must be met|[%]|
|_θℓ_<br>_h_|Load operating reserve requirement in time step _h_|[%]|
|_θ_pv<br>_h_|PV operating reserve requirement in time step _h_|[%]|



## **Incentive Parameters** 

|**Incentive **|**Parameters**||
|---|---|---|
|¯_ıt_|Upper incentive limit for technology _t_|[$]|
|_i_n<br>_v_|Net metering limits in net metering regime _v_|[kW]|
|_i_r<br>_t_|Incentive rate for technology _t_|[$/kWh]|
|¯_ıσ_<br>_t_|Maximum power rating for obtaining production incentive for|[kW]|
||technology _t_||
|**Technology-Specifc Time-Series Factor Parameters**|||
|_f_ed<br>_th_|Electrical power de-rate factor of technology _t_ at time step _h_|[unitless]|
|_f_fa<br>_th_|Fuel burn ambient correction factor of technology _t_ at time|[unitless]|
||step _h_||
|_f_ha<br>_th_|Hot water ambient correction factor of technology _t_ at time|[unitless]|
||step _h_||
|_f_ht<br>_th_|Hot water thermal grade correction factor of technology _t_ at|[unitless]|
||time step _h_||
|_f_p<br>_th_|Production factor of technology _t_ during time step _h_|[unitless]|
|**Technology-Specifc Factor Parameters**|||
|_f_d<br>_t_|Derate factor for turbine technology _t_|[unitless]|
|_f_l<br>_t_|Levelization factor of technology _t_|[fraction]|
|_f_li<br>_t_|Levelization factor of production incentive for technology _t_|[fraction]|
|_f_pf<br>_t_|Present worth factor for fuel for technology _t_|[unitless]|
|_f_pi<br>_t_|Present worth factor for incentives for technology _t_|[unitless]|
|_f_<br>td<br>_t_|Minimum turn down for technology _t_|[unitless]|



## **Pollutant and Generic Factor Parameters** 

|_e_f<br>_pt_|Fuel emissions rate of pollutant _p_ by technology _t_|[ton/MMBTU]|
|---|---|---|
|_e_g<br>_ph_|Grid emissions rate of pollutant _p_ in time step _h_|[ton/kWh]|
|_f_e|Energy present worth factor|[unitless]|



3 

|_f_fc<br>_p_||Present worth factor for fuel emissions costs related to pollu-|[unitless]|
|---|---|---|---|
|||tant _p_||
|_f_gc<br>_p_||Present worth factor for grid emissions costs related to pollu-|[unitless]|
|||tant type _p_||
|_f_fe<br>_p_||Present worth factor for fuel emissions related to pollutant _p_|[unitless]|
|_f_ge<br>_p_||Present worth factor for grid emissions related to pollutant|[unitless]|
|||type _p_||
|_f_om||Operations and maintenance present worth factor|[unitless]|
|_f_tot||Tax rate factor for of-taker|[fraction]|
|_f_tow||Tax rate factor for owner|[fraction]|
|_f_re<br>_t_||Proportion of renewable electricity produced by technology _t_|[fraction]|
|_f_rh<br>_t_||Proportion of renewable heat production from technology _t_|[fraction]|
|_b_<br>e<br>_p_||Minimum allowable lifecycle emissions of pollutant _p_|[ton]|
|¯_b_e<br>_p_||Maximum allowable lifecycle emissions of pollutant _p_|[ton]|
|_b_<br>re||Minimum allowable proportion of renewable electricity produc-|[fraction]|
|||tion||
|¯_b_re||Maximum allowable proportion of renewable electricity pro-|[fraction]|
|||duction||
|_b_<br>rh||Minimum allowable proportion of renewable heat production|[fraction]|
|¯_b_rh||Maximum allowable proportion of renewable heat production|[fraction]|
|**Power **|**Rating **|**and Fuel Limit Parameters**||
|_b_fa<br>_f_||Amount of available fuel for fuel type _f_|[MMBTU]|
|_b_p<br>_th_||Total production potential for technology _t_ in time step _h_|[kW]|
|_b_<br>_σ_<br>_c_||Minimum power rating for technology class _c_|[kW]|
|¯_bσ_<br>_t_||Maximum power rating for technology _t_|[kW]|
|_b_<br>_σ_s<br>_tks_||Minimum power rating for technology _t_ applied to subdivision|[kW]|
|||_k_, segment _s_||
|¯_bσ_s<br>_tks_||Maximum power rating for technology_t_applied to subdivision|[kW]|
|||_k_, segment _s_||



## **Efficiency Parameters** 

|**Efciency **|**Parameters**||
|---|---|---|
|_η_+<br>_bt_|Efciency of charging storage system _b_ using technology _t_|[fraction]|
|_η_-<br>_b_|Efciency of discharging storage system _b_|[fraction]|
|_η_ac|Absorption chiller efciency|[fraction]|
|_η_ac-e|Absorption chiller electrical efciency|[fraction]|
|_η_b|Boiler efciency|[fraction]|
|_η_ec|Electric chiller efciency|[fraction]|
|_η_g+|Efciency of charging electrical storage using grid power|[fraction]|



## **Storage Parameters** 

|¯_w_bkW<br>_b_|Maximum power output of storage system _b_|[kW]|
|---|---|---|
|_w_<br>bkW<br>_b_|Minimum power output of storage system _b_|[kW]|
|¯_w_bkWh<br>_b_|Maximum energy capacity of storage system _b_|[kWh]|
|_w_<br>bkWh<br>_b_|Minimum energy capacity of storage system _b_|[kWh]|
|_w_d<br>_b_|Decay rate of storage system _b_|[1/h]|
|_w_<br>mcp<br>_b_|Minimum percent state of charge of storage system _b_|[fraction]|



4 

_w_[0] _b_ 

Initial percent state of charge of storage system _b_ 

[fraction] 

|**Fuel Burn **|**Parameters**||
|---|---|---|
|_m_fb<br>_t_|_y_-intercept of the fuel rate curve for technology _t_|[MMBTU/h]|
|_m_fbm<br>_t_|Fuel burn rate _y_-intercept per unit size for technology _t_|[MMBTU/kWh]|
|_m_fm<br>_t_|Slope of the fuel rate curve for technology _t_|[MMBTU/kWh]|
|**CHP Thermal Performance Parameters**|||
|_k_te<br>_t_|Thermal energy production of CHP technology_t_per unit elec-|[unitless]|
||trical output||
|_k_tp<br>_t_|Thermal power production of CHP technology_t_per unit power|[unitless]|
||rating||



## **1.2 Variables** 

|**Boundary **|**Conditions**||
|---|---|---|
|_X_se<br>_b,_0|Initial state of charge for storage system _b_|[kWh]|
|**Continuous Variables**|||
|_X_ar-b<br>_h_|Available operating reserves from excess battery capacity in|[kW]|
||time step _h_||
|_X_ar<br>_th_|Available operating reserves from technology _t_ in time step _h_|[kW]|
|_X_bkW<br>_b_|Power rating for storage system _b_|[kW]|
|_X_bkWh<br>_b_|Energy rating for storage system _b_|[kWh]|
|_X_de<br>_de_|Peak electrical power demand allocated to tier _e_ and time-of-|[kW]|
||use demand period _d_||
|_X_dfs<br>_bh_|Power discharged from storage system _b_ during time step _h_|[kW]|
|_X_dn<br>_mn_|Peak electrical power demand allocated to tier _n_ in month _m_|[kW]|
|_X_e<br>_h_|Proportion of electrical load served in time step _h_|[%]|
|_X_f<br>_th_|Fuel burned by technology _t_ in time step _h_|[MMBTU/h]|
|_X_fb<br>_th_|_y_-intercept of fuel burned by technology _t_ in time step _h_|[MMBTU/h]|
|_X_g<br>_uh_|Power purchased from the grid for electrical load in demand|[kW]|
||tier _u_ during time step _h_||
|_X_gts<br>_h_|Electrical power from the grid used to charge storage in time|[kW]|
||step _h_||
|_Xℓ_<br>_th_|Production from technology_t ∈T s_ serving load in time step_h_|[kW]|
|_X_mc|Annual utility minimum charge adder|[$]|
|_X_pi<br>_t_|Production incentive collected for technology _t_|[$]|
|_X_plb|Peak electrical demand during look-back periods|[kW]|
|_X_ptg<br>_tuh_|Exports from production to the grid by technology_t_in demand|[kW]|
||tier _u_ during time step _h_||
|_X_pts<br>_bth_|Power from technology_t_used to charge storage system_b_during|[kW]|
||time step _h_||
|_X_ptw<br>_th_|Thermal power from technology _t_ sent to waste or curtailed|[kW]|
||during time step _h_||
|_X_ptc<br>_th_|Electrical power from technology _t_ curtailed in time step _h_|[kW]|



5 

|_X_r<br>_h_|Total operating reserves requirement in time step _h_|[kW]|
|---|---|---|
|_X_rp<br>_th_|Rated production of technology _t_ during time step _h_|[kW]|
|_Xσ_<br>_t_|Power rating of technology _t_|[kW]|
|_Xσ_s<br>_tks_|Power rating of technology _t_ allocated to subdivision _k_, seg-|[kW]|
||ment _s_||
|_X_se<br>_bh_|State of charge of storage system _b_ at the end of time step _h_|[kWh]|
|_X_stg<br>_uh_|Exports from storage to the grid in demand tier_u_ during time|[kW]|
||step _h_||
|_X_tp<br>_th_|Thermal production of technology _t_ in time step _h_|[kW]|
|_X_tpb<br>_th_|_y_-intercept of thermal production of CHP technology_t_in time|[kW]|
||step _h_||



## **Binary Variables** 

|_Z_dmt<br>_mn_|1 If tier _n_ has allocated demand during month _m_; 0 otherwise|[unitless]|
|---|---|---|
|_Z_dt<br>_de_|1 if tier _e_ has allocated demand during time-of-use period _d_; 0|[unitless]|
||otherwise||
|_Z_nmil<br>_v_|1 If generation is in net metering interconnect limit regime _v_;|[unitless]|
||0 otherwise||
|_Z_pi<br>_t_|1 If production incentive is available for technology _t_; 0 other-|[unitless]|
||wise||
|_Zσ_s<br>_tks_|1 If technology _t_ in subdivision _k_, segment _s_ is chosen; 0 oth-|[unitless]|
||erwise||
|_Z_to<br>_th_|1 If technology _t_ is operating in time step _h_; 0 otherwise|[unitless]|
|_Z_ut<br>_mu_|1 If demand tier _u_ is active in month _m_; 0 otherwise|[unitless]|



6 

## **1.3 Objective Function** 

**==> picture [308 x 492] intentionally omitted <==**

The objective function minimizes energy life cycle cost, i.e., capital costs, O&M costs, utility costs, and emissions costs; it maximizes (by subtracting) payments for energy exports and other incentives. 

## **1.4 Constraints** 

## **1.4.1 Fuel constraints** 

**==> picture [358 x 27] intentionally omitted <==**

7 

**==> picture [358 x 73] intentionally omitted <==**

Constraint (1a) limits fuel consumption for each fuel type, which can be burned by different technologies. Constraint (1b) uses a linear function to relate a non-CHP, fuel-burning electricityproducing technology’s output to the corresponding consumption. Constraint (1c) defines the fuel burn of each non-CHP heating technology as directly proportional to its thermal production in each hour. Constraint (1d) defines fuel consumption using a size-dependent _y_ -intercept and fixed slope, for every CHP technology and hour. Constraint (1e) limits the _y_ -intercept of fuel burned by a CHP technology in a given time step based on the power rating of the technology as long as the technology is operating, and is void otherwise. 

## **1.4.2 Thermal production constraints** 

**==> picture [387 x 63] intentionally omitted <==**

Constraints (2a)-(2b) limit the fixed component of thermal production of CHP technology _t_ in time step _h_ to the product of the thermal power production per unit of power rating and the power rating itself if the technology is operating, and 0 if it is not. Constraint (2c) relates the thermal production of a CHP technology to its constituent components, where the relationship includes a term that is proportional to electrical power production in each time step. 

## **1.4.3 Storage System Constraints** 

_Boundary Conditions and Size Limits_ 

**==> picture [308 x 49] intentionally omitted <==**

Constraint (3a) initializes a storage system’s state of charge using a fraction of its energy rating; constraints (3b) - (3c) limit the storage system size under the implicit assumption that a storage system’s power and energy ratings are independent. These constraints are identical to those given in ( _R_ ), but work in conjunction with significantly modified storage constraints that directly follow. _Storage Operations_ 

**==> picture [382 x 63] intentionally omitted <==**

8 

**==> picture [382 x 181] intentionally omitted <==**

**==> picture [382 x 15] intentionally omitted <==**

Constraints (3d) and (3e) restrict the electrical power that charges storage and is exported to the grid (in the former case), or that charges storage only (in the latter case, when grid export is unavailable) from each technology in each time step relative to the amount of electricity produced. Constraint (3f) provides an analogous restriction to that of constraint (3e) for thermal production, and constraint (3g) provides the same restriction for the thermal production of CHP systems. Constraints (3h), (3i), and (3j) balance state-of-charge for each storage system and time period for three specific cases, respectively: (i) available grid-purchased electricity, (ii) lack of grid-purchased electricity, and (iii) thermal storage, in which we account for decay. Constraint (3k) ensures that minimum state of charge requirements are not violated. 

_Charging Rates_ 

**==> picture [343 x 57] intentionally omitted <==**

**==> picture [343 x 27] intentionally omitted <==**

**==> picture [343 x 13] intentionally omitted <==**

Constraints (3l) and (3m) require that power available must meet or exceed that put into or discharged from storage; the latter constraint considers the case in which the grid is not available. Constraint (3n) reflects the power requirements for the thermal system. Constraint (3o) requires a storage system’s energy level to be at or below the corresponding rating. 

_Cold and hot thermal loads_ 

**==> picture [378 x 93] intentionally omitted <==**

9 

Constraints (4a) and (4b) balance cold and hot thermal loads, respectively, by equating the power production and the power from storage with the sum of the demand, the power to storage, and, in the case of cold loads, from the absorption chillers as well. Here, for legacy reasons, we have scaled the power by the efficiency of the respective technology; based on our variable definitions, we could have equivalently adjusted these by a coefficient of performance. 

## **1.4.4 Production Constraints** 

**==> picture [336 x 14] intentionally omitted <==**

**==> picture [336 x 14] intentionally omitted <==**

**==> picture [335 x 15] intentionally omitted <==**

Constraint set (5) ensures that the rated production lies between a minimum turn-down threshold and a maximum system size; constraints (5a)-(5b) are copied from Ogunmodede et al. (2021), while constraint (5c) is available in Hirwa et al. (2022). Constraint (5a) restricts system power output to its rated capacity when the technology is operating, and to 0 otherwise. Constraint (5b) ensures a minimum power output while a technology is operating; otherwise, the constraint is dominated by simple bounds on production. Constraint (5c) ensures that the thermal production of non-CHP heating and cooling technologies does not exceed system size. 

## **1.4.5 Production Incentives** 

**==> picture [368 x 52] intentionally omitted <==**

Constraint (6a) calculates total production incentives, if available, for each technology. Constraint (6b) sets an upper bound on the size of system that qualifies for production incentives, if production incentives are available. 

## **1.4.6 Power Rating** 

**==> picture [352 x 26] intentionally omitted <==**

**==> picture [352 x 26] intentionally omitted <==**

**==> picture [351 x 25] intentionally omitted <==**

**==> picture [352 x 78] intentionally omitted <==**

10 

Constraint (7a) permits nonzero power ratings only for the selected technology and corresponding subdivision in each class. Constraint (7b) allows at most one technology to be chosen for each subdivision in each class. Constraint (7c) limits the power rating to the minimum allowed for a technology class. Constraint (7d) prevents renewable technologies from turning down; rather, they must provide output at their nameplate capacity. Constraint (7e) limits rated production from all non-renewable technologies to be less than or equal to the product of the power rating and the derate factor for each time period. Constraint (7f) imposes both lower and upper limits on power rating of a technology, allocated to a subdivision in a segment, and constraint (7g) sums the segment sizes to the total for a given technology and subdivision. 

## **1.4.7 Load Balancing and Grid Sales** 

**==> picture [419 x 270] intentionally omitted <==**

Constraint (8a) balances load by requiring that the sum of power (i) produced, (ii) discharged from storage, and (iii) purchased from the grid is equal to the sum of (i) the power charged to storage, (ii) the power sold to the grid from in-house production or storage, (iii) the power charged to storage directly from the grid, (iv) any additional power consumed by the electric and absorption chillers (where these are additional terms relative to the original model ( _R_ )), and (v) the electrical load on site. Constraint (8b) provides an analogous load-balancing requirement for hours in which the site is disconnected from the grid due to an outage (and contains the same additional term relative to the original model ( _R_ )). Constraint (8c) restricts charging of storage from grid production to the grid power purchased for each hour. Similarly, constraint (8d) restricts the sales from the electrical storage system to its rate of discharge in each time period. Constraints (8e) and (8f) restrict the annual energy sold to the grid at net-metering rates; only one of these is implemented in each case according to user-specified options. While a collection of pre-specified technologies may contribute to net-metering rates in both cases, constraint (8e) allows storage to contribute to net-metering while constraint (8f) does not. 

11 

## **1.4.8 Rate Tariff Constraints** _Net Metering_ 

**==> picture [382 x 56] intentionally omitted <==**

**==> picture [381 x 40] intentionally omitted <==**

Constraint (9a) limits the net metering to a single regime at a time. Constraint (9b) restricts the sum of the power rating of all technologies to be less than or equal to the net metering regime. Constraint (9c) ensures that energy sales at net-metering rates do not exceed the energy purchased from the grid. 

_Monthly Total Demand Charges_ 

**==> picture [357 x 26] intentionally omitted <==**

**==> picture [357 x 44] intentionally omitted <==**

Constraint (10a) limits the quantity of electrical energy purchased from the grid in a given month from a specified pricing tier to the maximum available. Constraint (10b) forces pricing tiers to be charged in a specific order, and constraint (10c) forces one pricing tier’s purchases to be at capacity if any charges are applied to the next tier. 

_Peak Power Demand Charges: Months_ 

**==> picture [338 x 50] intentionally omitted <==**

**==> picture [338 x 25] intentionally omitted <==**

Constraint (11a) limits the energy demand allocated to each tier to no more than the maximum demand allowed. Constraint (11b) forces monthly demand tiers to become active in a prespecified order. Constraint (11c) forces demand to be met in one tier before the next demand tier. Constraint (11d) defines the peak demand to be greater than or equal to all of the demands across the time horizon, where an equality is actually induced by the sense of the objective function. A userdefined option precludes CHP technology production from reducing peak demand; if selected, constraint (11d) becomes: 

**==> picture [338 x 40] intentionally omitted <==**

12 

_∀m ∈M, h ∈Hm._ 

_Peak Power Demand Charges: Time-of-Use Demand and Ratchet Charges_ 

**==> picture [352 x 79] intentionally omitted <==**

**==> picture [351 x 26] intentionally omitted <==**

Constraints (12a)-(12d) correspond to constraints (11a)-(11d), respectively, but pertain to a type of charge not related to monthly use, but rather to time of use within a month. These _ratchet charges_ are implemented using constraints (12d). The charge applied for each time-of-use period is a linearizable function of the greater of the peak electrical demand during that period (as given by the first term on the right-hand side of (12d)) and a fraction of the peak demand that occurs over a collection of months (known as _look-back months_ ) during the year (as given by the second term on the right-hand side of (12d)). Constraint (12d) ensures the peak demand over the set of look-back months is no lower than the peak demand for each look-back month. In this way, charges are based not only on use in a given month, but also on a fraction of use over the last several months, and becomes relevant when this latter use is high relative to current use. If CHP technologies are not allowed to reduce peak demand, constraint (12d) becomes: 

**==> picture [332 x 56] intentionally omitted <==**

## **1.4.9 Minimum Utility Charge** 

**==> picture [394 x 166] intentionally omitted <==**

Constraint (13) enforces a minimum payment to the utility provider, which is a fixed constant less charges incurred from grid energy, time-of-use demand and monthly demand payments, plus sales from exports to the grid. 

13 

## **1.4.10 Operating Reserves** 

**==> picture [390 x 116] intentionally omitted <==**

**==> picture [391 x 94] intentionally omitted <==**

Constraints (14a) define the load served as the sum of (i) production less (ii) the quantity sold and less (iii) storage (both produced and coming from the grid). Constraints (14b) require the total operating reserves in any time step to be at least the sum of the load and PV operating reserve requirements. Constraints (14c) ensure that the operating reserves provided by the battery in any time step be no more than both the excess available energy and the power capacity. Constraints (14d) and (14e) guarantee that the operating reserves provided by PV and the generator, respectively, must be less than or equal to the excess available capacity for each technology in time step, while constraints (14f) ensure that these operating reserves can only be provided if the corresponding devices are operational in that time step. Total operating reserves, as given by the sum of the generators and PV devices, must be greater than those required for each time step by (14g) while the total annual load served must be at least the minimum specified (constraints (14h)). 

## **1.4.11 Emissions and Renewable Production Targets** 

**==> picture [413 x 182] intentionally omitted <==**

14 

**==> picture [368 x 158] intentionally omitted <==**

Constraint (15a) places bounds on the total lifecycle emissions attributed to fuel consumption on site and electricity purchases from the grid. These limits are derived from user-specified emissions reduction targets. Constraints (15b) and (15c) enforce an upper and lower bound on the total electricity produced by onsite renewable technologies, respectively; these are presented as fractions of the total electricity consumed on site. Constraints (15d) nd (15e) establish analogous bounds to those of constraints (15b) and (15c), respectively, on the usable heat produced by renewables. 

## **1.4.12 Non-negativity** 

**==> picture [360 x 201] intentionally omitted <==**

## **1.4.13 Integrality** 

**==> picture [315 x 97] intentionally omitted <==**

**==> picture [315 x 13] intentionally omitted <==**

15 

Finally, constraints (16) ensure all of the variables in our formulation assume non-negative values. In addition to non-negativity restrictions, constraints (17) establish the integrality of the appropriate variables. 

## **References** 

- Hirwa J, Ogunmodede S, Zolan A, Newman A (2022) Optimizing design and dispatch of a renewable-combined heat and power energy system. Optimization and Engineering 

- Ogunmodede O, Anderson K, Cutler D, Newman A (2021) Optimizing design and dispatch of a renewable energy system. Applied Energy 287:116527 

16 

