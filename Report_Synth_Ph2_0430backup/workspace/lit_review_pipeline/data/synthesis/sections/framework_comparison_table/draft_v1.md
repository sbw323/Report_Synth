{
  "section_id": "framework_comparison_table",
  "content_markdown": "### Pollutant-Specific Parameters and Framework Comparison\n\nThe penalization of wastewater effluent discharge depends critically on both the pollutant-specific parameters encoded within each framework and the structural characteristics of the penalty mechanism itself. This section consolidates two comparison tables drawn from the reviewed literature: the first catalogues pollutant-level parameters across the BSM1 effluent quality index, the Stare et al. piecewise-linear fine formulation, and relevant regulatory limits; the second contrasts the framework-level structural properties reported in the corpus.\n\n#### Table 1: Pollutant-Specific Parameters\n\nThe BSM1 effluent quality index assigns dimensionless weighting factors $b_i$ to each pollutant species, aggregating them into a single composite score expressed in pollution units per day (Gernaey et al., 2014). These weights derive from the Flanders regional fine formula used in Belgian environmental regulation (Vanrolleghem and Gillot, 2002). The Stare et al. (2007) formulation supplements this with a monetary piecewise-linear structure governed by slopes $\\Delta\\alpha_j$ (below-limit) and $\\Delta\\beta_j$ (above-limit), separated by a Heaviside step function at the discharge limit $C_{L,j}$. When $C_j^{\\text{EFF}} > C_{L,j}$, the marginal fine jumps from $\\Delta\\alpha_j$ to $\\Delta\\alpha_j + \\Delta\\beta_j$ (Stare et al., 2007; Machado et al., 2020). The EU Urban Waste Water Treatment Directive 91/271/EEC specifies concentration-based discharge limits applicable to plants above specified population equivalents (EEC Council, 1991). Machado et al. (2020) extended the Stare et al. parameterisation to include phosphate, assuming its fine parameters equal to those of ammonium except for the discharge limit, which was taken from Gernaey and Jorgensen (2004).\n\nThe Flanders-origin weights partition pollutants into organic (TSS, COD, BOD$_5$) and nutrient (TKN, S$_{\\text{NO}}$) categories, with the nutrient species receiving higher per-unit weights to reflect their greater ecological impact in receiving waters. Table 1 below synthesises these parameter values as reported across the reviewed sources.\n\n| Pollutant | BSM1 Weight $b_i$ | BSM1 Discharge Limit (mg/L) | EU 91/271/EEC Limit (mg/L) | Stare et al. $\\Delta\\alpha_j$ (EUR/g d) | Stare et al. $\\Delta\\beta_j$ (EUR/g d) | Flanders Category | Broader Penalty Category |\n|-----------|-------------------|----------------------------|---------------------------|----------------------------------------|----------------------------------------|-------------------|--------------------------|\n| TSS | 2 | 30 | 35 | — | — | Organic | Dimensionless index |\n| COD | 1 | 125 | 125 | — | — | Organic | Dimensionless index |\n| BOD$_5$ | 2 | 25 | 25 | — | — | Organic | Dimensionless index |\n| TKN | 30 | 18 | — | — | — | Nutrient | Dimensionless index |\n| S$_{\\text{NO}}$ | 10 | 18 | — | — | — | Nutrient | Dimensionless index |\n| S$_{\\text{NH}}$ | — | 4 | — | Reported by Stare et al. | Reported by Stare et al. | — | Piecewise-linear fine |\n| TN | — | 18 | 10–15 | Reported by Stare et al. | Reported by Stare et al. | — | Piecewise-linear fine |\n| TP | — | 2 | 1–2 | Assumed equal to S$_{\\text{NH}}$ | Assumed equal to S$_{\\text{NH}}$ | — | Piecewise-linear fine |\n\nThe BSM1 weights for TSS, COD, BOD$_5$, TKN, and S$_{\\text{NO}}$ are well established in the benchmarking literature (Gernaey et al., 2014). The Stare et al. (2007) slopes for S$_{\\text{NH}}$ and TN were calibrated so that the cost of discharge increased approximately threefold when discharge limits were exceeded, a parameterisation that strongly favours control algorithms maintaining concentrations below regulatory thresholds. The phosphate parameters adopted by Machado et al. (2020) represent an extrapolation rather than an independently calibrated set, reflecting the relatively recent inclusion of phosphorus in benchmark-based cost evaluations.\n\n#### Table 2: Framework-Level Structural Comparison\n\nThe frameworks reviewed span a hierarchy from fixed linear aggregation to endogenous market-clearing mechanisms, as established in the upstream synthesis. Table 2 presents their structural attributes.\n\n| Framework | Source Citation | Penalty Structure | Key Mechanism | Application Context |\n|-----------|----------------|-------------------|---------------|---------------------|\n| BSM1/BSM2 Effluent Quality Index | Vanrolleghem and Gillot (2002); Gernaey et al. (2014) | Dimensionless, linear weighted sum | Fixed species-specific weights $b_i$ applied to concentrations; constant marginal penalty per species | Benchmark simulation for control strategy comparison |\n| Stare et al. Effluent Fines | Stare et al. (2007) | Piecewise-linear with Heaviside activation | Dual slopes $\\Delta\\alpha_j$, $\\Delta\\beta_j$ at discharge limit $C_{L,j}$; marginal fine discontinuity at limit | WWTP operating cost comparison; extended by Machado et al. (2020) to phosphate |\n| Garibay-Rodriguez et al. Alternative 1 | Garibay-Rodriguez et al. (2017) | Proportional (per-gram above limit) | Fine $F^d = \\phi^d \\cdot CPG^d$ scaled by enforcement factor $\\phi$; continuous decision variable for violation magnitude | Macroscopic watershed MINLP optimisation |\n| Garibay-Rodriguez et al. Alternative 2 | Garibay-Rodriguez et al. (2017) | Fixed (binary-triggered) | Constant fine $CFF^d$ activated via Big-M constraints and binary variables regardless of exceedance magnitude | Macroscopic watershed MINLP optimisation |\n| Catalan Industrial Tariff | Machado et al. (2020) | Tariff with peak and saturation adjustments | Peak coefficient amplifies charges during elevated loading; volume saturation modulates marginal rate | Regional WRRF retrofitting evaluation (Manresa, Spain) |\n| Emissions Trading with Endogenous Penalty | Jin et al. (2014) | Market-clearing with composite penalty $F(v_i) = F_0 + f(v_i)$ | Marginal compliance condition $\\pi_i f'(v) = p$ ties monitoring probability to permit price; $f'(0) = Tp$ with $\\pi^* = 1/T$ | Permit market regulatory design under costly enforcement |\n| Taxes and Standards (Survey-based) | Xenarios and Bithas (2012) | Banded (tax rates, command-and-control limits) | Expert-preferred instruments; taxes ranked highest for cost-effectiveness; standards preferred via national government implementation | International survey on urban wastewater policy instruments |\n\nSeveral structural contrasts emerge from this tabulation. The BSM index provides computational tractability at the expense of regulatory realism, since its constant marginal weights do not capture the escalating consequences of limit exceedance (Gernaey et al., 2014). The Stare et al. (2007) piecewise-linear formulation addresses this deficiency by introducing a slope discontinuity, and its sensitivity to the ratio $\\Delta\\beta_j / \\Delta\\alpha_j$ has been shown to govern the relative advantage of advanced control algorithms over simpler strategies: when $\\Delta\\beta = 0$ (i.e., constant fine per kilogram across all concentrations), cost reductions from advanced control drop from approximately 12.6% to 6.2% (Stare et al., 2007). The Garibay-Rodriguez et al. (2017) proportional scheme achieved a 9.9% reduction in total annual cost relative to a technology-only baseline, whereas the fixed-fine alternative yielded only a 1.5% reduction but with superior environmental outcomes, illustrating the trade-off between economic flexibility and environmental stringency. At the market-clearing end of the hierarchy, Jin et al. (2014) demonstrated that penalty shape integration with the permit price achieves cost-effective emissions targets, though practical application to wastewater remains constrained by monitoring challenges identified by Xenarios and Bithas (2012).",
  "word_count": 952,
  "heading_level": 3,
  "metadata": {
    "model": "claude-sonnet-4-20250514",
    "generation_timestamp": "2025-01-24T00:00:00Z",
    "section_type": "evidence_table",
    "evidence_chunks_used": [1, 5, 6, 8, 9, 12, 13, 17, 21, 22, 23, 24, 25]
  },
  "column_definitions": [
    "Pollutant",
    "BSM1 Weight b_i",
    "BSM1 Discharge Limit (mg/L)",
    "EU 91/271/EEC Limit (mg/L)",
    "Stare et al. Delta_alpha (EUR/g d)",
    "Stare et al. Delta_beta (EUR/g d)",
    "Flanders Category",
    "Broader Penalty Category"
  ],
  "rows": [
    {
      "Pollutant": "TSS",
      "BSM1 Weight b_i": "2",
      "BSM1 Discharge Limit (mg/L)": "30",
      "EU 91/271/EEC Limit (mg/L)": "35",
      "Stare et al. Delta_alpha (EUR/g d)": "—",
      "Stare et al. Delta_beta (EUR/g d)": "—",
      "Flanders Category": "Organic",
      "Broader Penalty Category": "Dimensionless index"
    },
    {
      "Pollutant": "COD",
      "BSM1 Weight b_i": "1",
      "BSM1 Discharge Limit (mg/L)": "125",
      "EU 91/271/EEC Limit (mg/L)": "125",
      "Stare et al. Delta_alpha (EUR/g d)": "—",
      "Stare et al. Delta_beta (EUR/g d)": "—",
      "Flanders Category": "Organic",
      "Broader Penalty Category": "Dimensionless index"
    },
    {
      "Pollutant": "BOD5",
      "BSM1 Weight b_i": "2",
      "BSM1 Discharge Limit (mg/L)": "25",
      "EU 91/271/EEC Limit (mg/L)": "25",
      "Stare et al. Delta_alpha (EUR/g d)": "—",
      "Stare et al. Delta_beta (EUR/g d)": "—",
      "Flanders Category": "Organic",
      "Broader Penalty Category": "Dimensionless index"
    },
    {
      "Pollutant": "TKN",
      "BSM1 Weight b_i": "30",
      "BSM1 Discharge Limit (mg/L)": "18",
      "EU 91/271/EEC Limit (mg/L)": "—",
      "Stare et al. Delta_alpha (EUR/g d)": "—",
      "Stare et al. Delta_beta (EUR/g d)": "—",
      "Flanders Category": "Nutrient",
      "Broader Penalty Category": "Dimensionless index"
    },
    {
      "Pollutant": "S.NO",
      "BSM1 Weight b_i": "10",
      "BSM1 Discharge Limit (mg/L)": "18",
      "EU 91/271/EEC Limit (mg/L)": "—",
      "Stare et al. Delta_alpha (EUR/g d)": "—",
      "Stare et al. Delta_beta (EUR/g d)": "—",
      "Flanders Category": "Nutrient",
      "Broader Penalty Category": "Dimensionless index"
    },
    {
      "Pollutant": "S.NH",
      "BSM1 Weight b_i": "—",
      "BSM1 Discharge Limit (mg/L)": "4",
      "EU 91/271/EEC Limit (mg/L)": "—",
      "Stare et al. Delta_alpha (EUR/g d)": "Reported by Stare et al.",
      "Stare et al. Delta_beta (EUR/g d)": "Reported by Stare et al.",
      "Flanders Category": "—",
      "Broader Penalty Category": "Piecewise-linear fine"
    },
    {
      "Pollutant": "TN",
      "BSM1 Weight b_i": "—",
      "BSM1 Discharge Limit (mg/L)": "18",
      "EU 91/271/EEC Limit (mg/L)": "10–15",
      "Stare et al. Delta_alpha (EUR/g d)": "Reported by Stare et al.",
      "Stare et al. Delta_beta (EUR/g d)": "Reported by Stare et al.",
      "Flanders Category": "—",
      "Broader Penalty Category": "Piecewise-linear fine"
    },
    {
      "Pollutant": "TP",
      "BSM1 Weight b_i": "—",
      "BSM1 Discharge Limit (mg/L)": "2",
      "EU 91/271/EEC Limit (mg/L)": "1–2",
      "Stare et al. Delta_alpha (EUR/g d)": "Assumed equal to S.NH",
      "Stare et al. Delta_beta (EUR/g d)": "Assumed equal to S.NH",
      "Flanders Category": "—",
      "Broader Penalty Category": "Piecewise-linear fine"
    },
    {
      "Pollutant": "Framework: BSM1/BSM2 EQI",
      "BSM1 Weight b_i": "Source: Vanrolleghem and Gillot (2002); Gernaey et al. (2014)",
      "BSM1 Discharge Limit (mg/L)": "Structure: Dimensionless linear weighted sum",
      "EU 91/271/EEC Limit (mg/L)": "Mechanism: Fixed species-specific weights; constant marginal penalty",
      "Stare et al. Delta_alpha (EUR/g d)": "Context: Benchmark simulation for control strategy comparison",
      "Stare et al. Delta_beta (EUR/g d)": "",
      "Flanders Category": "",
      "Broader Penalty Category": ""
    },
    {
      "Pollutant": "Framework: Stare et al. Effluent Fines",
      "BSM1 Weight b_i": "Source: Stare et al. (2007)",
      "BSM1 Discharge Limit (mg/L)": "Structure: Piecewise-linear with Heaviside activation",
      "EU 91/271/EEC Limit (mg/L)": "Mechanism: