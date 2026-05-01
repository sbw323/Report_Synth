## Economic Equilibrium and the DR–Effluent Quality Tradeoff

Translating demand response (DR) aeration simulation outputs into a monetized optimization problem requires a formal equilibrium framework that jointly quantifies energy savings and effluent quality degradation in commensurate economic units. The methodological architecture rests on three interlinked components: (i) a time-weighted effluent quality index that aggregates pollution loads, (ii) an aeration energy cost model proportional to oxygen transfer intensity and reactor geometry, and (iii) a piecewise-linear fine function that converts effluent quality deviations into pollutant-specific monetary penalties. Together, these elements define a tradeoff surface on which the optimal DR operating point can be located through an equilibrium condition analogous to the permit-market clearing rule.

### Effluent Quality Aggregation via the EQI Integral

The Benchmark Simulation Model framework employs a dimensionless Effluent Quality Index (EQI) that integrates the weighted concentrations of multiple pollutants over a specified evaluation window. Following the conventions adopted in the BSM1 and BSM2 literature (Copp, 2002; Machado et al., 2020), the index is computed as:

$$EQI = \frac{1}{T} \int_0^T \sum_j \omega_j \, C_j^{\text{eff}}(t) \, Q^{\text{eff}}(t) \, dt$$

where $\omega_j$ are pollutant-specific weighting factors calibrated to regional fine formulae, $C_j^{\text{eff}}(t)$ is the instantaneous effluent concentration of pollutant $j$, $Q^{\text{eff}}(t)$ is the effluent flow rate, and $T$ is the evaluation period. The weighting factors, historically calibrated to the Flanders regional tariff, assign relative monetary weights to total suspended solids, chemical oxygen demand, biological oxygen demand, total Kjeldahl nitrogen, and nitrate-nitrogen. Because the weights are fixed and the aggregation is linear, the marginal cost attributed to any incremental gram of a given pollutant remains constant within each simulation period, a property that is computationally convenient but insensitive to the nonlinear cost escalation real regulatory regimes impose once discharge limits are breached (Machado et al., 2020).

### BSM Aeration Energy Formula

Aeration constitutes the dominant electricity cost in activated sludge facilities, accounting for 45–60% of total energy consumption (Zohrabian et al., 2021). The BSM energy model expresses aeration energy $AE$ as a function of the volumetric oxygen transfer coefficient and reactor volume (Stare et al., 2007; Copp, 2002):

$$AE = \frac{1}{T} \int_0^T \sum_i \frac{K_{La,i}(t) \cdot V_i}{V_{\text{ref}}} \, dt$$

where $K_{La,i}(t)$ is the oxygen transfer rate in reactor $i$, $V_i$ is the reactor volume, and $V_{\text{ref}}$ is a reference volume (typically 1333 m$^3$ in the standard BSM1 layout). This formulation ensures that any DR intervention that reduces $K_{La,i}$ during a curtailment window directly reduces $AE$, yielding quantifiable energy savings proportional to both the intensity and the duration of aeration reduction.

### Piecewise-Linear Fine Function

To recover the nonlinear regulatory cost structure suppressed by the linear EQI, the piecewise-linear effluent fine model introduced by Stare et al. (2007) decomposes the EQI back into pollutant-specific monetary penalties. For each pollutant $j$, the daily fine $EF_j$ is:

$$EF_j = \Delta\alpha_j \, C_j^{\text{eff}} \, Q^{\text{eff}} + H(C_j^{\text{eff}} - C_{L,j}) \left[ \Delta\beta_j (C_j^{\text{eff}} - C_{L,j}) \, Q^{\text{eff}} + b_{0,j} \, Q^{\text{eff}} \right]$$

where $\Delta\alpha_j$ is the slope of the fine curve below the discharge limit $C_{L,j}$, $\Delta\beta_j$ is the steeper slope above that limit, $b_{0,j}$ is a fixed surcharge for exceeding the limit, and $H(\cdot)$ is the Heaviside step function. This dual-slope Heaviside structure produces a discontinuous jump in marginal cost at the regulatory threshold, creating a strong economic incentive for the plant to remain compliant while still penalizing residual pollution below the limit (Machado et al., 2020). The total effluent fine is then $EF = \sum_j EF_j$, typically summing contributions from ammonium, total nitrogen, and phosphate.

### Equilibrium Condition: Marginal Abatement Cost Equals Shadow Price

The economic equilibrium governing the optimal DR operating point maps onto the classical permit-market clearing condition whereby the marginal abatement cost equals the permit price (Jin et al., 2014; Weitzman, 1974). In the DR context, this condition takes the following form: the marginal energy savings from an additional unit of aeration reduction must equal the marginal increase in effluent fines at the optimal operating point. Formally, if $S(\mathbf{x})$ denotes the energy savings function and $F(\mathbf{x})$ denotes the total effluent fine, both parameterized by the aeration reduction vector $\mathbf{x}$, optimality requires:

$$\frac{\partial S}{\partial x_k} = \frac{\partial F}{\partial x_k} \quad \forall \, k$$

This condition mirrors the result of Jin et al. (2014), where the firm's marginal abatement cost $c_i'(a_i) = p$ at equilibrium, with $p$ the permit price. In the DR application, the shadow price of effluent quality — the implicit price the facility pays for each additional pollution unit discharged — plays the role of the permit price. As Garibay-Rodriguez et al. (2017) demonstrated through sensitivity analysis of the enforcement multiplier $\phi$, deviations from this equilibrium either waste resources on excessive treatment or incur disproportionate fines.

### Three-Part Policy Banding

The shadow price of effluent quality can be bounded using a three-part policy structure analogous to the Roberts–Spence hybrid instrument described in the environmental economics literature (Xenarios and Bithas, 2012; Goulder and Parry, 2008). Under this design, a tax ceiling caps the maximum marginal cost the facility faces for additional discharge, while a subsidy floor establishes a minimum reward for emission reductions beyond the permit allocation. Within the interior band, the shadow price floats at the market-clearing level. This banding structure hedges against the regulator's uncertainty about true abatement costs and provides upper and lower bounds on the operating cost trajectory across a range of DR intensities. In the wastewater DR setting, the tax ceiling corresponds to the steeper fine slope $\Delta\beta_j$ triggered upon limit exceedance, while the subsidy floor can be interpreted as the baseline energy cost savings rate attainable under non-DR operation.

### Four-Dimensional Aeration Parameter Space

Constructing the response surfaces for both $S(\mathbf{x})$ and $F(\mathbf{x})$ requires systematic exploration of the aeration reduction design space. This space is spanned by four parameters: (1) the start time of the DR curtailment event within the diurnal cycle, (2) the duration of aeration reduction, (3) the intensity of $K_{La}$ reduction relative to the baseline setpoint, and (4) the frequency of curtailment events per evaluation period. Latin Hypercube Sampling (LHS) provides a space-filling experimental design that efficiently covers this four-dimensional domain, avoiding the combinatorial explosion of full-factorial designs while ensuring adequate coverage of parameter interactions. Each sample point defines a complete DR scenario that is propagated through the activated sludge process model to compute both the resulting $AE$ and $EQI$, from which $S$ and $F$ are derived. The resulting paired response surfaces — energy savings and effluent fines as functions of the four-dimensional aeration parameter vector — provide the empirical basis for locating the equilibrium operating point where marginal energy savings equal marginal fine increases, and for verifying that the solution lies within the bounds established by the three-part policy band.