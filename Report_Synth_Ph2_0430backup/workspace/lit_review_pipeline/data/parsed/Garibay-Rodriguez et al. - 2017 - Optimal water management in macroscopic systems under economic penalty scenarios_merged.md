**==> picture [30 x 19] intentionally omitted <==**

# Optimal Water Management in Macroscopic Systems Under Economic Penalty Scenarios 

Jaime Garibay-Rodriguez and Vicente Rico-Ramirez 

Dept. de Ingenieria Quimica, Instituto Tecnologico de Celaya, Av. Tecnologico y Garcia Cubas S/N, Celaya, Guanajuato 38010, Mexico 

## Jose M. Ponce-Ortega 

Dept. de Ingenieria Quimica, Universidad Michoacana de San Nicolas de Hidalgo, Morelia, Michoacan 58060, Mexico 

## DOI 10.1002/aic.15712 

Published online March 24, 2017 in Wiley Online Library (wileyonlinelibrary.com) 

An integrated optimization approach to assess the sustainability of water management strategies in a macroscopic system is proposed. Those strategies include alternative water sources, such as rainwater harvesting, and the design of distributed water treatment systems. To deal with the economic challenges inherent to wastewater treatment, an economic penalization scheme is presented as an alternative that can achieve better cost-effectiveness and pollution abatement than traditional command and control practices. The proposed approach results in an MINLP multiperiod model, which R has been solved through the GAMS[V] modeling environment. The solution of our case-study allows finding the minimum investment to meet the desired environmental goals with respect to freshwater consumption and pollution abatement. Results include the number, size, and location of rainwater storage devices as well as treatment technologies, the total amount of recycled wastewater, and the total amount of fines charged to the users for violation of environmental regulations. VC 2017 American Institute of Chemical Engineers AIChE J, 63: 3419–3441, 2017 Keywords: sustainable water management, mathematical programming, distributed water treatment systems, economic penalizations 

## Introduction 

Finding the optimal solution for resources distribution and wastewater treatment in a complex network of usage and disposal of water is not always as straightforward as obtaining the minimum investment at which environmental regulations are satisfied. In most cases, a compromise between the economic and environmental aspects has to be taken into account. That is not a simple task, because the required investment sometimes becomes prohibitive; especially when the users (e.g., domestic, industrial, agricultural) are affected by economic constraints regarding budgets, profitability of their products, market share, and so forth. In general, sustainable water management policies must consider both the availability of water and water pollution. 

On the one hand, the availability of water resources is a major concern for most of the governments and much debate has been done in recent years to provide better policies and strategies to prevent water shortages throughout the world. Water scarcity always emerges from a combination of excessive use and hydrological variability. This issue may in part be mitigated by storage infrastructure. However, climate drives the water cycle and the increasing variability in precipitation 

Correspondence concerning this article should be addressed to V. Rico-Ramirez at vicente@iqcelaya.itc.mx. 

> VC 2017 American Institute of Chemical Engineers 

and evaporation also increases the seasonal and spatial variations of water supply.[1] It has been noted that water scarcity is a result of (1) physical water scarcity, (2) economic water scarcity (due to lack of infrastructure because of technical or financial constraints) or (3) institutional water scarcity (due to failure of institutions to ensure a reliable and safe water supply). On the other hand, water pollution is also an increasing problem as a result of the industrial development and population growth. However, a generalization on this regard is difficult; in some parts of the world water resources are vast and clean while in others most people struggle with water availability. Even within some countries there are water sanitation and supply inequalities often masked by the national averages. Furthermore, in some regions water acts as carrier for diseases, mainly in the developing world.[2] The effort needed to deal with these issues is large and it must be tackled from many perspectives. 

Water pollution is still a challenge in developing countries and a financial issue in large cities and industries throughout the world. The design of distributed treatment systems has been previously addressed through optimization models; these systems can achieve lower costs with the segregation of large wastewater effluents. However, significant economic challenges are inherent to wastewater treatment despite the investment in optimal treatment designs. To deal with this issue, economic penalizations schemes are an alternative which can accomplish better cost-effectiveness and pollution abatement 

3419 

August 2017 Vol. 63, No. 8 

AIChE Journal 

than traditional command and control practices. In this article, we propose an integrated approach of these optimization strategies to assess the sustainability of a macroscopic system. 

In recent years, optimization models have been used to propose solutions to water concerns from many aspects.[3–7] Napoles-Rivera et al.[8] proposed an optimization approach that aims to mitigate water scarcity through the implementation of storage infrastructure for precipitation. Their approach evaluated the minimum investment needed in storage infrastructure to maintain sustainable amounts of underground and superficial water in a city. Later, Rojas-Torres et al.[9] applied the fundamental concepts proposed by Napoles-Rivera et al.[8] and analyzed the impact of the variations with time of important model parameters; such as population growth, change in the time value of money, and change in the precipitation patterns. The authors developed a multiperiod analysis to provide future projections of the optimal decisions driven by the variations on such model parameters. Similarly, Burgara-Montero et al.[4] proposed a mathematical programming model for the design of optimal distributed treatment systems in a watershed. 

Further, the idea of pollution abatement through penalizations and trading pollution[10–12] has been widely implemented in the United States with their Emissions Trading Program (or cap and trade) for air quality. The same idea has been extended for water quality through trading effluents. The strategy seeks to obtain the best tradeoff between pollution abatement and cost-effectiveness.[13,14] In the context of water pollution abatement from a trading and penalty perspectives, literature reports several efforts in the area of mathematical programming.[15–19] These approaches are based on an ideal scenario, where charging environmental violators with fines and exchanging pollution credits among various sources achieve lower global costs while environmental constraints are met. However, none of those approaches has considered a macroscopic system which also takes into account the sustainability of water resources within a watershed and its surroundings. 

Therefore, this article proposes a mathematical programming model to account for the sustainability of a macroscopic system through the optimal management of resources, including the evaluation of alternative technologies for reducing fresh water consumption, a distributed treatment system to improve the quality of water effluents from different sources, and the possibility of penalty scenarios for wastewater treatment and pollution. In general, the ideas provided by NapolesRivera et al.,[8] Rojas-Torres etal.,[9] Burgara-Montero et al.,[4] and Lopez-Villarreal et al.[17] are used to formulate the MINLP model. 

In summary, this article shows two fundamental differences with respect to the previous approaches. First, the efficient management of water resources and the implementation of distributed treatment systems are integrated into a single mathematical model. Such approach not only involves a larger number of variables and constraints but also gets more complex due to the nonlinearities resulting from the integration; one of the main issues is that linear water balance constraints used in previous formulations become nonlinear (bilinear), as both the composition and flows of a large number of streams are now unknown (variables). Second, a fundamental idea in our formulation, analysis, and discussion is the incorporation of the economic penalization schemes for wastewater treatment. Two alternatives to implement a penalization scheme are proposed, as well as a method to calculate fixed fines for users who do not meet environmental regulations. 

Furthermore, a thorough analysis of the performance and impact of the economic penalizations has been made in order to achieve a better understanding of the consequences of the implementation of a penalization scheme. The aim is to assess the implications of the penalties over the costs and the environmental objectives of the problem. To the best of our knowledge, no previous publications on the application of mathematical programming to water management consider the three main issues described above. 

## Problem Description 

The system under investigation might be any hydrological network that involves a certain amount of users (for instance, cities and agricultural fields), in which the users require a known amount of water for their activities and generate a known amount of wastewater with a given type and amount of pollutants. In this work, this hydrological network consists of a watershed and its surroundings. In a perfectly sustainable system, the amount of water available from the natural sources in a watershed would be sufficient to meet the demands of the users without compromising their future availability. Furthermore, the amount and type of pollutants discharged over the water bodies would be completely degraded by the natural flora and fauna present in the aquatic ecosystems, however, this is not a common scenario. A strategy is then needed to mitigate the harmful consequences on the environment. 

## Alternative water sources 

In this context, alternative sources of water can be used to reduce water consumption from traditional sources to help them recover their sustainable levels. The alternative water sources considered in this problem come from rainwater harvesting and storage in different devices, such as elevated tanks, artificial ponds, and artificial aquifers. Rainwater can be harvested in the roofs of houses and buildings and, with a mild treatment, be safely used by any kind of user. Tanks can be located among houses and buildings in a city, whereas artificial ponds and aquifers can be located mostly outside residential areas near to the agricultural fields. The capacity and amount of rain storage devices are tied to rainwater availability, land space, targeted water consumption reduction and of course, size of the investment. A multiperiod strategy divided in months is proposed to deal with the variability in rain patterns and demands of water. This means that it is expected to find a solution that indicates in which periods of time rainwater should be stored and in which should be used to minimize the water consumption from natural sources and ensure that demands are met. 

## Wastewater treatment 

Conversely, pollution over water bodies not only damages the aquatic ecosystems, but also reduces superficial and underground water availability. Wastewater treatment from largepoint sources can be significantly expensive; to reduce costs, a distributed treatment system has been proposed in several approaches. In this distributed system, the wastewater generated by the different users can be segregated and treated in a number of facilities or a “network” of smaller wastewater treatment plants. This network is formed by a number of individual treatment plants, where each one of them can have a different efficiency, size, and cost. Once the wastewater is treated, the targeted composition after the treatment is the overall composition when all segregated flows in the network 

3420 DOI 10.1002/aic 

August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

AIChE Journal 

are mixed. Now, treated wastewater can be recycled only if it falls under the required quality conditions or, it can be disposed to the environment with the warranty that no harmful or unsustainable consequences will come from that. Recycled wastewater can be used in agricultural areas to irrigate crops and in domestic and industrial areas, but only to irrigate public gardens and fields. This consideration is made because of the high demand of water by these sectors and due to the complexity of implementing a large-scale reuse and recycle water network within cities and industries. A division of the main river in the watershed is used to track flows and compositions. A material flow analysis approach is finally used to take into account every inlet and outlet streams, as well as natural phenomena occurring in the watershed. 

## Economic penalizations 

To this point, the solution of the problem would not have any flexibility regarding environmental constraints. This can cause significantly higher costs in the expense of having an optimal solution. Flexibility in the solution has to be seen from the cost of the wastewater treatment perspective, because that is the most expensive part of the investment, due to the high costs of the technologies and their operation. Obtaining a flexible solution, closer to a realistic scenario, is the main aim of this work. The purpose of this work is not promoting unsustainable habits, but to give a choice to decision makers when it comes to make an investment to mitigate environmental impact and to make sure that those relaxed or less ecological choices, in the bigger picture, fall inside the desired strategy to help overcome negative effects over the environment. 

The aforementioned flexibility can be achieved by modeling a system, as the one described before, but under penalty scenarios for wastewater treatment. These penalty scenarios are described as follows. The distributed treatment system is obtained in accordance with an environmental constraint imposed on the model. This constraint is a uniform parameter for all wastewater generated and lies within a range set by environmental norms and regulations in a region or a country. However, users (e.g., industries) can pay fines if the environmental constraint is violated. There are two approaches in which these violations can be dealt with, (1) the amount per gram or unit of mass above the set environmental constraint is measured and a proportional fine, according to the degree of such violation, is charged to the user and, (2) a fixed fine is charged if the user transgresses the regulation by any degree. For the first approach, the degree of transgression is a variable that will be decided in the optimization strategy. In addition, the fine per unit of mass has to be calculated and its value can dramatically change the results to select the more economically attractive option. The second approach also needs to establish a fine for transgressors; however, this fine will be much larger than the one in the first approach. It is worth noting that the potential transgression of the environmental constraint in both approaches has to be bounded by a maximum amount. 

distributed wastewater treatment system, the total amount of recycled wastewater, and the total amount of fines charged to the users for transgression of environmental constraints regarding pollution over water bodies. 

## Mathematical Model 

Figure 1 shows the layout of the macroscopic system and its relationship with the river in a watershed. As mentioned before, the main river is divided into several sections. Each section is represented with the index r. For every section r, there is a domestic area d, an agricultural area a, and an industrial area i. Every one of these areas can be composed by a number of users of the same type. For example, a small town can have its own domestic area d, however, a big city can be divided in several domestic areas, which would correspond to the various neighborhoods on it. In addition, every section r has a number of potential locations for s storage tanks, p artificial ponds, and q artificial aquifers. Industrial and domestic areas are considered to have their own wastewater effluents and every one of them has a network of treatment plants distributed throughout the watershed. The individual treatment plants in those networks are called interceptors and their existence is modeled with the index x. Wastewater can be composed by a number of different l pollutants. Finally, all variables and relationships have an index t to model the different time periods. 

## Water management 

To model the water consumption, monthly averaged demand parameters for every domestic, agricultural, and industrial areas are used. The following relationship stands for water consumption from fresh sources 

**==> picture [234 x 33] intentionally omitted <==**

where FWSr;t is a variable for water consumption from fresh sources in section r and time period t. DFWSr;d;t, IFWSr;i;t, and AFWSr;a;t are calculated variables in accordance with demands of domestic, industrial, and agricultural areas, respectively. These demands must be equal to the summation of the amount of water from fresh sources, rainwater, and recycled wastewater as shown in Eqs. 2–4, respectively 

**==> picture [215 x 64] intentionally omitted <==**

## Objective 

The solution of the optimization problem will obtain the size of the minimum investment to meet the desired environmental objectives with respect to freshwater consumption and pollution over water bodies. This investment consists of the number, size, and location of rainwater storage devices, the number, size, type, and location of treatment plants in the 

**==> picture [204 x 65] intentionally omitted <==**

DOI 10.1002/aic 3421 

AIChE Journal August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

**==> picture [408 x 354] intentionally omitted <==**

Figure 1. Schematic representation of one river section and its interaction with the watershed. [Color figure can be viewed at wileyonlinelibrary.com] 

**==> picture [214 x 64] intentionally omitted <==**

where DDAr;d;t, DIAr;i;t, and DAAr;a;t are monthly average demand parameters for domestic, industrial, and agricultural areas, respectively. The rest of the terms in the right member of previous equations represent water inlets from recycled wastewater and stored rainwater. For instance, in Eq. 2 DRWWr;d;t is the total amount of recycled water sent to area d in river section r at time period t. DSTr;s;d;t represents rainwater sent from storage tank s to area d, DAPr;p;d;t stands for rainwater sent from artificial pond p, and DAQr;q;d;t for artificial aquifers. The rest of the terms in Eqs. 3 and 4 are selfexplanatory since indexes s, p, and q remain the same and only the index d is substituted by the indexes i and a for industrial and agricultural areas, respectively. 

Additional constraints for recycled wastewater in domestic and industrial areas are included in Eqs. 5 and 6. Those equations involve parameters that represent the percentage of wastewater that can be reused for irrigation of gardens and andareas, the total demand of recycled wastewater can be used forfields. The parameterb[I] r;i;t[is][the][parameter] b[D] r;d;t[for][is the parameter for domestic areas][industrial][areas.][In][agricultural] irrigation of crops (Eq. 7) 

**==> picture [228 x 47] intentionally omitted <==**

In addition, the given demands are equal to the sum of consumedEq. 8 forwaterdomesticðCW[D] r;dareas.;t[Þ][and] For[wastewater] industrial[ð][WW] areas,[D] r;d;t[Þ] an[as] analogous[shown][in] equation is formulated in Eq. 9. In agricultural areas, since the total demand of water is used for irrigation of crops, no wastewater is generated 

**==> picture [228 x 31] intentionally omitted <==**

## Rainwater harvesting and storage system design 

The design of the rainwater harvesting system depends on whether: (1) rainwater is available or not in a period of time, (2) rainwater is more cost effective or not than other sources, and (3) rainwater is needed or not to achieve a target consumption of water from fresh sources. The first part of the design is to establish the amount of available rainwater. Availability of water is assumed to be the same per section of the river and per period of time. Values of the monthly average rainwater are needed for a given geographical area in millimeters. Values of effective rainwater harvesting for each possible storage 

3422 DOI 10.1002/aic 

August 2017 Vol. 63, No. 8 AIChE Journal 

Published on behalf of the AIChE 

SW[Q] r;q;t[�][AQ][max] r;q 8r 2 R; q 2 Q; t 2 T (24) 

device are also required. The following equations consider rainwater availability on each storage device in the macroscopic system 

**==> picture [217 x 14] intentionally omitted <==**

**==> picture [220 x 32] intentionally omitted <==**

where PAr;t represents the total amount of rainwater in millimeters, Area[S] r;s;t[,][Area][P] r;p;t[,][and][Area][Q] r;q;t[represent][the][areas][of] roofs of houses and buildings available to harvest rainwater, and RC[S] , RC[P] , and RC[Q] stands for the runoff coefficient of the roofs for storage tanks, artificial ponds, and artificial aquifers, respectively. The following relationships account for the rainwater stored in time period t 

**==> picture [219 x 50] intentionally omitted <==**

whereand NSThe terms for stored and discarded rainwater in Eqs. 14 and 15SW[S] r;s;t[S] r[the amount of water that cannot be stored in tank] ;s;t[represents][the][amount][of][water][stored][in][tank][ s][s][.] are similar from the ones in Eq. 13 for artificial ponds and artificial aquifers, respectively. 

Storage devices distribute rainwater to the final users within each section of the river. Balances in each storage device are stated as follows 

**==> picture [197 x 64] intentionally omitted <==**

**==> picture [200 x 64] intentionally omitted <==**

**==> picture [202 x 64] intentionally omitted <==**

The amount of available rainwater is determined with the variables STr;s;t, APr;p;t, and AQr;q;t for storage tanks, artificial ponds, and artificial aquifers, respectively. As the number of storage devices has to be calculated, the previous variables are constrained in terms of the maximum capacities as follows 

**==> picture [198 x 26] intentionally omitted <==**

**==> picture [200 x 30] intentionally omitted <==**

**==> picture [201 x 12] intentionally omitted <==**

where ST[max] r;s[,][AP][max] r;p[,][and][AQ][max] r;q provide the maximum storage capacity for each device. These variables are involved in the following series of disjunctions to model the existence or nonexistence of rainwater storage devices 

**==> picture [206 x 80] intentionally omitted <==**

maximum capacity parameters for storage tanks. The BooleanIn the previous disjunction, dr[s][;] ;[min] s and dr[s][;] ;[max] s are minimum and variable z[st] r;s;t[accounts][for][the][installation][of][storage][tanks][in] the system. Ifits capacity lies z[st] r;s;betweent[is true, the corresponding tank] the aforementioned bounds[ s][ is installed,] and the cost function of the tank is activated. If z[st] r;s;t[is false, the maxi-] mum capacity of the tank is zero and the cost function is also equal to zero. Analogous disjunctions for artificial ponds and aquifers are shown in Eqs. 26 and 27, respectively 

**==> picture [208 x 163] intentionally omitted <==**

Nonlinearities in previous cost functions can be eliminated with the following equations 

**==> picture [162 x 47] intentionally omitted <==**

where A[0] , B[0] , C[0] , D[0] , E[0] , and F[0] are linearized cost parameters for a designed capacity range of each storage device. The three previous disjunctions are reformulated algebraically using the Big-M reformulation.[20] The Big-M reformulation is preferred as, in this case, such relaxation uses a small number of variables and constraints and is equivalent to the convex hull relaxation (notice that one clause of each disjunction implies that all conditional variables are zero) 

**==> picture [238 x 62] intentionally omitted <==**

**==> picture [232 x 14] intentionally omitted <==**

DOI 10.1002/aic 3423 

AIChE Journal August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

**==> picture [432 x 237] intentionally omitted <==**

Figure 2. Superstructure of the distributed treatment system. [Color figure can be viewed at wileyonlinelibrary.com] 

**==> picture [233 x 13] intentionally omitted <==**

**==> picture [235 x 93] intentionally omitted <==**

## Balances in river sections 

Equation 40 accounts for all inlets and outlets in a river section. The flow is equal to the summation of the flow from the previous sectioncontribution from ðJtributariesr21;tÞ, the contribution from rainðTribr;tÞ, wastewater ðdischargesPr[J] r;t[Þ][, the] fromminusdomesticthe directðWWusagesr[D] ;d[;][dis] ;tð[Þ] Ur[and][J] ;t[Þ][,][and][industrial][the][losses][ð][WW][by][I] r[;] ;[dis] i;[filtration] t[Þ][sources,][or] evaporation ðLossr;tÞ 

**==> picture [230 x 35] intentionally omitted <==**

To measure the quality of water throughout the system, a component balance is needed, as shown in Eq. 41. This balance involves all inlets and outlets, as well as the natural phenomena occurring in the section of the river. Each term of Eq. 40 is multiplied by a concentration of pollutant l. The last term of the following equation represents chemical and biochemical reactions occurring in the section of the river 

**==> picture [212 x 127] intentionally omitted <==**

Note that the natural degradation of pollutants is usually modeled as a first-order kinetic reaction. For that case, the term Ðis VVrrthe;;tt50[rx] Arrhenius[r][;][l][dV][r][;][t][would] constant[be][equal] for the[to][k] natural[r][;][l][3][CJ][r][;] degradation[l][;][t][3][V][r][;][t][.][Where] of the[k][r,l] pollutants and Vr,t is the volume of the river section at a time period t. The term rxr;l can be represented using different kinetic relationships to model complex phenomena occurring in the water bodies. The use of a large number of pollutants is possible through the definition of the set L. A simple approach (less number of variables and constraints), however, can be achieved by assuming a pseudo-single pollutant, as it will be explained later. 

The key variable in Eq. 41 is CJr;l;t, which represents the concentration of the river in section r, for pollutant l, at time period t. This variable is used in the optimization strategy to accomplish the targeted environmental objectives through its minimization and/or limit, as it will be further explained in the section of the objective function. 

## Distributed treatment system design 

To overcome the harmful effects of wastewater streams discharged over water bodies, the implementation of a distributed treatment system is proposed. Disjunctions are used to model the design of the distributed system. This design involves the 

3424 DOI 10.1002/aic 

August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

AIChE Journal 

number, location, and type of facilities to be installed; the flows to be treated in each facility, the time periods in which these facilities must be installed and used, the concentration of pollutants after treatment, and the total cost. In addition, the design must determine the amount and distribution of recycled 

wastewater All of this in accordance with the given environmental constraint. The superstructure of the distributed treatment system is shown in Figure 2. The following disjunction represents the discrete decisions involved in the design for domestic wastewater streams 

**==> picture [402 x 292] intentionally omitted <==**

This disjunction is reformulated using the Convex-hull method.[21] For Eq. 42, the convex hull is preferred over the Big-M formulation to achieve a tighter relaxation. The reformulation is as follows 

**==> picture [238 x 99] intentionally omitted <==**

**==> picture [239 x 26] intentionally omitted <==**

**==> picture [236 x 27] intentionally omitted <==**

**==> picture [16 x 9] intentionally omitted <==**

**==> picture [232 x 26] intentionally omitted <==**

**==> picture [240 x 27] intentionally omitted <==**

**==> picture [233 x 27] intentionally omitted <==**

**==> picture [227 x 20] intentionally omitted <==**

> x (46) wheresource CTand[D] r;dCTR;t[is][the][D] r;d;t[concentration][is][the][concentration][of][pollutant][after][the][in][the][treatment.][domestic][f] X fs[d] r;d;x;t[3] �[1][2][a][x][;][l] �3CT[D] r;d;l;t[5][WW] r[D] ;d;t[3][CTR] r[D] ;d[;][d] ;l[1] ;t s[d] r;d;x;t[is the segregated flow sent to the interceptor][ x][,][ a][x][;][l][is the] x2X (47) efficiency of the interceptor, and Xr[d] ;[;] d[min] ;x and Xr[d] ;[;] dx[max] are the 8r 2 R; d 2 D; l 2 L; t 2 T minimum and maximum capacity parameters of interceptors. CRE[max] l is a parameter used to represent the maximum conCTR[D] r;d[;][d] ;l[2] ;t[5][CT] r[D] ;d;l;t[3][ð][1][2][y][r][;][d][;][t][Þ] (48) centration of pollutants allowed in recycled wastewater.a positive integer parameter greater than one used for model- M[D] is 8r 2 R; d 2 D; l 2 L; t 2 T ing purposes. 

DOI 10.1002/aic 3425 

August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

AIChE Journal 

An analogous disjunction is used for industrial wastewater streams as follows 

**==> picture [397 x 294] intentionally omitted <==**

As in Eq. 42, the Convex-hull reformulation is also used for Eq. 54 and is shown in the following constraints 

**==> picture [240 x 27] intentionally omitted <==**

**==> picture [216 x 14] intentionally omitted <==**

**==> picture [16 x 10] intentionally omitted <==**

**==> picture [238 x 27] intentionally omitted <==**

**==> picture [240 x 83] intentionally omitted <==**

**==> picture [16 x 9] intentionally omitted <==**

**==> picture [221 x 46] intentionally omitted <==**

**==> picture [16 x 9] intentionally omitted <==**

**==> picture [16 x 9] intentionally omitted <==**

**==> picture [221 x 36] intentionally omitted <==**

**==> picture [235 x 36] intentionally omitted <==**

In addition, the following constraints are needed to limit the existence of segregated flows into the interceptors and recycled wastewater streams only when a treatment unit is selected 

**==> picture [231 x 115] intentionally omitted <==**

To model the distribution of recycled wastewater, the following equations are used 

**==> picture [231 x 47] intentionally omitted <==**

**==> picture [229 x 32] intentionally omitted <==**

3426 DOI 10.1002/aic Published on behalf of the AIChE 

August 2017 Vol. 63, No. 8 

AIChE Journal 

**==> picture [203 x 71] intentionally omitted <==**

**==> picture [147 x 23] intentionally omitted <==**

Finally, factors /[d] and /[i] are used to multiply CPG[d] and CPG[i] to calculate the fines F[d] and F[i] , respectively 

**==> picture [150 x 11] intentionally omitted <==**

**==> picture [147 x 12] intentionally omitted <==**

**==> picture [202 x 32] intentionally omitted <==**

Hence, if /[d] and /[i] are greater than one, it means that the penalization for an environmental constraint violation is greater than the cost of reducing the pollutants discharge through technology implementation. Thus, even though the formulation allows transgression of environmental regulations, the greater the values of /[d] and /[i] , the greater the fines. In that case, the optimization of an economic objective tends to drive the solution toward the fulfillment of the environmental regulations. Finally, to obtain the amount in which regulations are violated,lowing constraintsvariables DPfor[d] r;d;l;tdomestic[and][D][P][i] r;i;l;andt[are][involved] industrial[in the fol-] sources, respectively 

where DRW[in] r;d;t[and][IRW][in] r;i;t[represent][the][total][amount][of] treated wastewater that can be recycled from a domestic source and an industrial source, respectively. The right member term in Eq. 72 represents the distribution of recycled wastewater to every type of user in the system. The terms wastewater sent to domestic, industrial, and agricultural areas,DRW[out] r;d;[;] d[d] ;t[,][DRW][out] r;d;[;] i[i] ;t[,][and][DRW][out] r;d;[;] a[a] ;t represent recycled respectively. The same goes for right-side members in Eq. 73. Equations 74–76 represent the summation of recycled wastewater from domestic and industrial sources coming to domestic, industrial, and agricultural areas, respectively. 

**==> picture [188 x 32] intentionally omitted <==**

## Economic penalizations 

Alternative 1. One of the two approaches to represent a penalization system is charging a fine per unit of mass discharged above the environmental constraint. The first challenge is to calculate an appropriate fine to charge transgressors with. Most likely, the fine would be provided by a government agency or regulator. However, the estimation of this parameter is made in accordance with the work of Lopez-Villarreal et al.[17] as follows. First, the total treatment cost required to achieve environmental constraints can be estimated when there is no possibility for constraint violations in domestic and industrial sources. These parameters can be calculated a priori by solving the MINLP model without allowing penalizations 

tionswhereforUpperlimdischarged[d] r;d;l;t wastewater[and][Upperlim] from[i] r;i;l;tdomestic[are][upper] and[limit] industrial[restric-] sources. 

Alternative 2. The second approach consists of charging transgressors with a fixed fine. This fine is in all cases the same, without concerning the degree of violation; although the fixed fines for domestic and industrial users are different from each other. The determination of these fines could represent a challenge; in fact, we believe that our formulation could be used for decision makers and authorities to estimate such value in practice. We propose the estimation of fixed fines as follows. CPG[d] and CPG[i] are estimated as in Alternative 1. Then, the cost of fixed fines for domestic and industrial sources is calculated through the definition of M[p] and the use of Eqs. 87 and 88 

**==> picture [157 x 12] intentionally omitted <==**

**==> picture [156 x 11] intentionally omitted <==**

CWP[d] and CWP[i] represent the total treatment cost required to achieve environmental constraints when there is no possibility for constraint violations. Since pollution from domestic and industrial sources can be significantly different from each other, a different fine should be implemented. Similarly, the total expected pollution reduction can be calculated using Eqs. 79 and 80 

**==> picture [156 x 11] intentionally omitted <==**

**==> picture [154 x 11] intentionally omitted <==**

M[p] is a parameter that represents the maximum degree of violation allowed for the environmental constraints (grams), CFF[d] and CFF[i] are the costs of fixed fines for domestic and industrial sources, respectively. These costs can also be multiplied by another parameter which helps enforce regulations as in Alternative 1 

**==> picture [490 x 73] intentionally omitted <==**

Additionally, four constraints (Big-M formulation) in terms of alternative as followsthe binary variables w[p] r;[;] d[d] ;l;t[and][w][p] r;[;] i[i] ;l;t[are][needed][to][model][this] 

The total expected pollution reduction is then used to estimate CPG[d] and CPG[i] in Eqs. 81 and 82. CPG[d] and CPG[i] are the costs per gram when pollution reduction is achieved only through technology implementation for domestic and industrial sources, respectively 

**==> picture [227 x 32] intentionally omitted <==**

**==> picture [149 x 23] intentionally omitted <==**

**==> picture [223 x 14] intentionally omitted <==**

Published on behalf of the AIChE DOI 10.1002/aic 3427 

AIChE Journal August 2017 Vol. 63, No. 8 

**==> picture [197 x 13] intentionally omitted <==**

If a user violates the regulation, for example, a domestic user, thedomesticbinaryuservariableis alsow[p] ractivated;[;] d[d] ;l;t[is][activated] in the objective[and][the][fixed] function.[fine][for] The[a] same constraints shown in Eqs. 85 and 86 are used to model this alternative but, in this case, the values of DP[d] r;d;l;t[and][D] P[i] r;i;l;t[will][not][participate][directly][in][the][objective][function.] Notice the importance of parameter M[p] , as it will determine the cost of fines and will also affect the relaxation of the amount of pollutant discharged. The estimation of the fixed fines proposed here can be used to make a comparative analysis between Alternatives 1 and 2, when the upper limits for D Pof the MINLP model increases with Alternative 2, as it adds a[d] r;d;l;t[and][D][P][i] r;i;l;t[are][the][same][in][both][cases.][The][complexity] greater number of binary variables to the problem (combinatorial complexity gets worse). 

## Costs 

Treatment Costs. Equation 95 defines the wastewater treatment cost for domestic sources and Eq. 96 for industrial sources. All of the following equations involve annual costs if the time periods are selected to be 12 months 

**==> picture [233 x 97] intentionally omitted <==**

In the previous equations, FCx and VCx are coefficients for the capital costs of the interceptor x and Cu[op] x is the operational cost of interceptor x. The exponent u is used to consider the economies of scale. 

Storage Costs. Annual costs for the rainwater harvesting system include installation of gutters and mild treatment devices for rainwater collection on the roofs of houses and buildings, in addition to the cost of the installation of storage tanks, artificial ponds, and artificial aquifers, as represented by the following expression 

**==> picture [234 x 36] intentionally omitted <==**

Piping and Pumping Costs. Piping and pumping installations include the infrastructure needed to send water from rainwater storage devices to the different areas ðppRHSÞ, to transport recycled wastewater where it is required ðppRWÞ and to obtain, treat, and distribute water from fresh sources ðppNSÞ. These costs consider several terms, including the rain harvesting system, the recycling of water, and the transportation of water from natural resources. 

Rain harvesting system. The annual costs for piping and pumping of rainwater distribution are defined by Eq. 98 

**==> picture [218 x 244] intentionally omitted <==**

where PCSAr;s;a, PCSDr;s;d, and PCSIr;s;i represent unitary costs for sending rainwater from a storage tank s, to an agricultural, domestic, and industrial area, respectively. The terms PCPAr;p;a, PCPDr;p;d, and PCPIr;p;i are analogous but for the case of artificial ponds, as well as the terms PCWAr;q;a, PCQDr;q;d, and PCQIr;q;i for artificial aquifers. 

Recycled water. The same strategy is followed for recycled wastewater transportation as shown in Eq. 99 

**==> picture [224 x 156] intentionally omitted <==**

where PCRDDr;d;d, PCRDIr;d;i, and PCRDAr;d;a are the unitary costs for the transportation of water from domestic wastewater sources to domestic, industrial, and agricultural areas, respectively. The terms PCRIDr;i;d, PCRIIr;i;i, and PCRIAr;i;a are analogous but they are defined for industrial wastewater sources. 

Natural sources. Each area in every section of the river has an inlet of water from fresh sources; to estimate the piping and pumping costs, the total amount of the inlet stream of water is multiplied by a factor, which includes costs of extraction from the source, required treatment, and final distribution to the area. The terms PCNSDr;d, PCNSIr;i, and PCNSAr;a account for these costs for domestic, industrial, and agricultural areas, respectively, as shown in Eq. 100 

3428 DOI 10.1002/aic Published on behalf of the AIChE 

August 2017 Vol. 63, No. 8 AIChE Journal 

Table 1. Water Demands by Sector of the Illustrative Example 

||January|February|March|April|May|June|
|---|---|---|---|---|---|---|
|Total demand (m3)|27,966,495|32,123,992|29,498,655|29,421,508|27,841,841|14,606,257|
|% Domestic|22.88|22.64|24.66|28.03|28.66|51.18|
|% Industrial|2.03|1.77|1.93|1.94|2.04|3.89|
|% Agricultural|75.09|75.58|73.41|70.04|69.3|44.93|
||July|August|September|October|November|December|
|Total demand (m3)|11,894,519|11,499,631|15,282,838|22,501,404|31,026,109|31,422,017|
|% Domestic|58.8|60.82|44.75|30.4|22.02|20.5|
|% Industrial|4.79|4.94|3.72|2.53|1.83|1.81|
|% Agricultural|36.41|34.24|51.53|67.08|76.14|77.69|



**==> picture [213 x 75] intentionally omitted <==**

Finally, the total piping and pumping costs are given by Eq. 101 

**==> picture [187 x 10] intentionally omitted <==**

Economic Penalization Costs (Alternative 1). In the first alternative, the total amounts of pollutant above the environðmentalDP[i] r;i;l;tconstraint[Þ][users][are] for[multiplied] both domestic[by][the] ðDP[corresponding][d] r;d;l;t[Þ][and][industrial][fines] ðF[d] and F[i] Þ to obtain the total annual economic penalization ðEPCÞ as given by Eq. 102 

**==> picture [187 x 42] intentionally omitted <==**

Economic Penalization Costs (Alternative 2). Conversely, if the second alternative is chosen, EPC will be equal to the total number of both domestic ðw[p] r;[;] d[d] ;l;t[Þ][and] byindustrialthe correspondingðw[p] r;[;] i[i] ;l;t[Þ][users] total[that] fixed[violate] fine[the] ðF[constraints][d][;][2] ; F[i][;][2] Þ, as[multiplied,] defined in Eq. 103 

**==> picture [191 x 42] intentionally omitted <==**

## Objective function 

The simultaneous minimization of the total annual cost ðTACÞ, the total annual consumption of water from fresh sources ðFWS[total] Þ, and the concentration of pollutants in the discharge ðCJ[discharge] Þ are the objective functions. Thus, the objective function of this work is defined by Eq. 104 

**==> picture [222 x 23] intentionally omitted <==**

The total annual cost ðTACÞ is the sum of wastewater treatment, rainwater harvesting and storage, and piping and pumping costs. Additionally, there could be economic penalizations ðEPCÞ when regulations are violated, as shown in Eq. 105 

TAC5TRcost[d] 1TRcost[i] 1STRcost1PPcost1EPC (105) 

where TRcost[d] and TRcost[i] are the total wastewater treatment costs for domestic and industrial sources, respectively. STRcost represents the total cost of the rainwater harvesting and storage system, and PPcost is the total cost of piping and pumping. The total consumption of water from fresh sources is given by Eq. 106 

**==> picture [169 x 20] intentionally omitted <==**

Finally, the concentration of the discharge of the system is the concentration of the outlet of the last section of the river 

**==> picture [173 x 12] intentionally omitted <==**

where the index Dis represents the last section of the river. CJ[discharge] is required to be minimal at each period of time. 

## Scope and limitations of the model 

The purpose of this work is to assess the sustainability in a watershed and to obtain optimal guides for a sustainable water management. The goal is not to promote unsustainable practices within the applicable regulations; even less, the approach does not intend leading the public opinion to believe that allowing the payment of fines could be profitable at the expense of the environment. Key decision variables, for instance, the investment in wastewater treatment, must be carefully evaluated, assessing the economical and the environmental pursuits of decision makers. 

The limiting value on the concentration of pollutant at which wastewater is allowed to be discharged on a river is the parameter that plays the most important role in the sustainability of the watershed. One of the purposes of this work is to provide a framework to understand the degree of sustainability of a watershed and, based on this, to make a conscious decision about the value of such parameter (a task which is commonly left to the state or environmental agencies). We would expect that limit to be placed very near to the most cost-effective and least harmful solution to the environment. Additional limitations of the model formulation are remarked as follows: 

a. Dynamics of pollutants in the water bodies: Due to the assumption of steady state, the time-dependent phenomena, such as dispersion of pollutants or chemical reactions undergoing in the watershed, are not considered in the model. 

b. Linearity of cost functions: Although most nonlinear cost functions are convex, due to the high number of constraints (bilinear terms and most of all, binary variables) the computational effort of solving a more complex problem is not worth the increased precision that could be accomplished with the introduction of nonlinear correlations. This is why 

DOI 10.1002/aic 3429 

AIChE Journal August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

Table 2. Parameters of the Distributed Treatment System 

||Fixed|Variable||Operating|
|---|---|---|---|---|
|Interceptor|Cost ($)|Cost ($/m3)|Effciency|Cost ($/m3)|
|1|195,000|0.058|0.95|0.00170|
|2|144,000|0.031|0.71|0.00144|
|3|0|0|0|0|



cost functions are reduced to pre-optimized cost factors (parameters) which multiply flow variables. That approach is used in the costs of piping and pumping and in the linear cost functions for treatment technologies and rainwater harvesting and storage. 

c. Uncertainty of parameters: Despite variability and uncertainty in some parameters (rain patterns, water demands, wastewater discharges, etc.), the season-dependent parameters are modeled deterministically through a multiperiod strategy. The selected monthly averaged parameters may not always be as certain as expected, but the solution of a Stochastic MINLP is avoided. 

## Illustrative Example 

A case-study is proposed to illustrate the scope of the model. The macroscopic system consists of a variety of domestic, industrial, and agricultural areas connected throughout a main river and its tributaries. The main river is divided into five sections. The different areas share the available natural water sources in the system additionally to alternative water sources (rainwater and recycled water). Houses and businesses in domestic areas as well as factories and industrial parks in industrial areas discharge their wastewater into the main river. Table 1 shows the water demands in the system in a year. We have estimated the data by using a typical demand per habitant (338.75 L/day) and a seasonal dependent deviation from the highest demanding months. 

## Distributed treatment system 

The composition of the wastewater consists of organic compounds and nutrients which can be adequately measured through its Biological Oxygen Demand (BOD). This means that a pseudo-single pollutant case is addressed in this example. Significant differences in domestic and industrial wastewater are encountered; domestic wastewater BOD ranges from 400 to 800 mg/L whereas industrial wastewater ranges from 800 to 1200 mg/L. Wastewater can be treated in a distributed treatment system; it can be recycled, if it reaches the required quality (BOD 5 30 mg/L), or discharged to the river at the maximum allowed concentration limit (BOD 5150 mg/L). There are three possible interceptors in the interceptor network (see Table 2). Two of them correspond to treatment facilities with different technologies and the third acts as a fictitious interceptor for the case when only a part of the wastewater stream is treated. 

Table 3. Parameters of the Rain Harvesting System 

||||Storage Tank|Artifcial Pond|
|---|---|---|---|---|
|Maximum|capacity|(m3)|50,000|600,000|
|A0|||13,080|–|
|B0|||1.8135|–|
|C0|||–|111,968|
|D0|||–|0.8895|



Table 4. Estimated Parameters of the Economic Penalization Scheme 

|$/(mg/L)||CPGd|CPGi|Fd|Fi|
|---|---|---|---|---|---|
|Alternative|1|406|237|446.6|260.7|
|$||CFFd|CFFi|Fd,fxed|Fi,fxed|
|Alternative|2|60,900|35,550|66,990|39,105|



## Water resources management 

The agricultural sector has the highest demand of water in the system; therefore, mitigation of fresh water consumption (FWC) from this sector is much desired. To accomplish this objective, there are a maximum of nine storage tanks and four artificial ponds strategically located in every river section to harvest rainwater and distribute it to the final users. Their capacity depends on rain patterns and the desired reduction on the consumption of water from natural sources. The installation of artificial aquifers is not considered in this example. In addition, optimal distribution of water from traditional sources is also obtained in the optimization strategy. Water consumption can be reduced through recycled wastewater; as a particular illustrative constraint, it is assumed that 20% of the total demand in domestic areas can be satisfied with recycled water and only 10% for industrial areas. Parameters for rain storage devices are shown in Table 3. Additional parameters for estimating piping and pumping costs are shown in Appendix. 

## Economic penalizations 

In this example, as in the work of Lopez-Villarreal et al.,[17] we use Eqs. 77–84 to calculate the costs per gram for alternative 1. Coefficients /[d] and /[i] are equal to 1.1. The maximum amount over which the environmental regulations can be violated by a source is twice the upper limit, which is 300 mg/L of BOD. This definition is arbitrary. That value was selected for assessing the scope and flexibility of the formulation, whereas the sustainability of the system is still taken into account; of course, higher values not only can change the results, but also can lead to an unsustainable solution. Analyzing the effect of the maximum limit allowed is one of the advantages of the approach. For alternative 2, M[p] is defined as 150 mg/L and, through the use of Eqs. 87–90, the costs of fixed fines CFF[d] and CFF[i] are calculated. The value of factors /[d][;][fixed] and /[i][;][fixed] are both also equal to 1.1. A summary of the economic penalization parameters are shown in Table 4. 

The configuration of the system in this illustrative example is shown in Figure 3. The resulting MINLP problem was coded in the GAMS[V] R modeling environment.22 It consists of 33,522 continuous variables, 4020 discrete variables and 21,835 constraints, and it was solved in a computer with an Intel[V] R core i5 processor with 2.40 GHz and 8 GB of RAM with the solvers DICOPT/MINOS/CPLEX for the MINLP/ NLP/LP problems. The optimality gap of the master MILP problem at each iteration was zero. In spite of the problem having a large number of binary variables, every solution has been obtained using a CPU time of about 30 s. This is possible through the use of appropriate bounds on the variables and their initial values. 

## Results and Discussion 

## Minimization of individual objectives 

Although the discussion starts with the minimization of the individual objectives, the minimum optimal value of CJ[discharge] 

August 2017 Vol. 63, No. 8 

3430 DOI 10.1002/aic 

Published on behalf of the AIChE 

AIChE Journal 

**==> picture [360 x 134] intentionally omitted <==**

Figure 3. Representative layout of the proposed example. [Color figure can be viewed at wileyonlinelibrary.com] 

is also a measure of the sustainability of the system, but it is not considered in the multiobjective strategy as our approach consists of imposing constraints in every point source of pollution. 

The minimum optimal value of CJ[discharge] (outlet concentration of the last section of the river) results in 5.2 mg/L of BOD and the TAC is 66,251,945 $/year. The difference between such value and any other solution is an important issue to consider; when constraining every point source to a maximum limit discharge of 150 mg/L of BOD, CJ[discharge] increases to 7.74 mg/L, but the TAC results in 59,451,689 $/year. Notice that this is the policy used the most in practice to enforce regulations; it achieves a significant reduction of costs and still falls into the desired environmental objective. 

Individual optimization of water consumption from fresh sources results in a minimum value of 247,738,204 m[3] /year; a targeted reduction can start with such minimum value. 

Finally, optimization of the TAC results in 8,552,558 $/year without environmental constraints; the pollutant discharge concentration is 27 mg/L and the total demand of water is satisfied only through natural sources. 

## Comparison of solutions at unrestricted FWC 

The epsilon constraint method[23] is used to solve the multiobjective optimization problems addressed in this subsection. In the following scenarios, the consumption of water from fresh sources is unrestricted. This analysis cuts out any bias concerning treatment costs to reduce water consumption and allows focusing only on the performance of the penalization schemes through the minimization of the TAC. 

Base Solution. This solution is obtained by investing only in treatment technologies to deal with pollution abatement. Results are shown in Table 5. According to regulations, the averaged concentrations for both domestic and industrial discharges are below the upper limit of 150 mg/L. The TAC is expected to be the highest whereas the averaged discharge of 

pollutants is the lowest. Although there is no constraint for fresh sources consumption, because the upper limit for the discharge concentration of the pollutants is low enough, usage of recycled wastewater is expected as a result of the synergy between the pollution abatement and fresh sources consumption objectives. 

Solution with Penalizations from Alternative 1. In Table 5, Alternative 1a and Alternative 1b represent solutions obtained by assuming variable fines according to the amount over which the regulations are violated. Alternative 1a involves the optimization of the TAC but no recycled water is used due to the relaxation of the discharge limit. This results on an increase in the average discharge from domestic sources (CTR[D] average). The TAC is 5,887,490 $/year (9.9%) less than the base solution, effectively proving the economic performance of the penalization strategy. Almost six million dollars in savings are obtained with an increase of 1.89 mg/L of pollutants concentration in the final discharge of the river (CJ[discharge] ). Alternative 1b was obtained for comparison purposes by enforcing the same amount of recycled wastewater as the base solution. Alternative 1b performs well enough to decrease the CTR[D] average and the CJ[discharge] with an overall increase in the TAC of 2.5% with respect to Alternative 1a, which is still a significant 7.5% reduction of the TAC with respect to the base solution. 

Solution with Penalizations from Alternative 2. Recall that alternative 2 refers to the use of a fixed fine due to the violation of environmental regulations by any source. Analysis of solutions of Alternative 2a and Alternative 2b is similar to the previous discussion. In this case, however, Alternative 2a is the one that uses a comparable amount of fresh water with respect to the base solution. Alternative 2a shows a small decrease in FWS[total] as well as in the averaged CTR[D] with respect to the base solution; nonetheless, the penalization scheme causes an increase in the averaged CTR[I] , which eventually also increases CJ[discharge] . This alternative achieves only 

Table 5. Optimal Solutions for Unconstrained Water Consumption from Fresh Sources 

|Concept|Base Solution|Alternative 1a|Alternative 1b|Alternative 2a|Alternative 2b|
|---|---|---|---|---|---|
|TAC ($/year)|59,451,689|53,564,198|54,960,923|58,545,759|58,674,935|
|Recycled water (m3/year)|10,563,691|0|10,566,228|10,587,620|0|
|FWStotal (m3/year)|274,521,575|285,085,266|274,521,575|274,497,646|285,085,266|
|CTRD average (mg/L)|123.97|179.52|158.97|123.28|149.98|
|CTRI average (mg/L)|150.00|251.00|251.00|267.67|267.67|
|Treatment cost ($/year)|51,170,719|40,428,255|42,198,448|47,695,314|47,552,337|
|EPC ($/year)|0|4,583,384|4,485,114|2,570,040|2,570,040|
|CJdischarge average (mg/L)|7.74|9.63|8.68|7.99|8.90|



DOI 10.1002/aic 3431 

AIChE Journal August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

Table 6. Optimal Solutions for Minimum Consumption of Water from Fresh Sources 

|Concept|Base Solution|Alternative 1|Alternative 2|
|---|---|---|---|
|TAC ($/year)|69,755,102|65,548,493|68,700,164|
|Storage tanks (m3/year)|9,343,342|9,340,466|9,340,466|
|Artifcial ponds (m3/year)|6,183,367|6,183,367|6,183,367|
|Recycled water (m3/year)|21,820,353|21,823,229|21,823,229|
|FWStotal (m3/year)|247,738,204|247,738,204|247,738,204|
|CTRD average (mg/L)|90.64|117.37|90.61|
|CTRI average (mg/L)|150.00|251.00|267.67|
|Treatment cost ($year)|54,129,097|45,568,494|50,509,374|
|EPC ($/year)|0|4,359,248|2,570,040|
|CJdischarge average (mg/L)|6.76|7.67|7.01|



a 1.5% smaller value of TAC than that of the base solution. The estimated fine for domestic sources appears to be high enough so that the entire domestic wastewater is treated to attain at least the upper limit of the allowed discharge concentration. Some industrial sources pay fines, though, since treatment costs may be higher than such an option. Alternative 2a is not very different from the base solution in which the treatment and recycle of a portion of wastewater is more costeffective than obtaining the resource from natural sources. Alternative 2b is not an optimal solution because it was obtained by explicitly avoiding the use of recycled water. It then shows an increase in FWS[total] as well as in the averaged values of CTR[D] , CTR[I] and in the CJ[discharge] , with a 1.3% decrease in the TAC with respect to the base solution. 

Further Discussion. Clearly, the averaged value of CTR[D] is an indicator of the performance of the penalization schemes from the economic and environmental points of view. In this example, the average value of CTR[I] shows a lower effect because industrial sources are fewer than domestic sources and due to the assumption of nontoxic industrial wastewater. However, an interesting case could involve another type of pollutants for industrial sources and different fines and regulations for each one of them. Alternative 1 outperforms Alternative 2 in terms of economic objectives (due to flexibility or adaptability of the fines), but Alternative 2 should not be completely discarded; Alternative 2 still achieves a significant reduction of costs (almost a million dollars per year) and outperforms Alternative 1 in terms of environmental objectives. The performance of the penalization schemes is tied to the cost of the fixed and variable fines; this issue will be further discussed in the remaining sections. 

## Comparison of solutions at minimum FWS[total] 

The minimum optimal value of water consumption from fresh sources (FWS[total] ) is 247,738,204 m[3] /year. This means that, in this scenario, additional demands for all users have to be satisfied with nontraditional sources such as recycled water and rainwater from storage devices. The performance of the formulation is assessed at this minimum value of FWS[total] for comparison purposes. Table 6 shows the results for the base solution, Alternative 1, and Alternative 2. 

Base Solution. Two additional sources of water are added (storage tanks and artificial ponds), expressed in yearly supply of water. The averaged values of CTR[D] as well as CJ[discharge] are expected to be lower at minimum FWS[total] ; this is due to the required quality of recycled water (30 mg/L). This solution is the most sustainable of this scenario but it is also the most expensive. Table 6 also shows that the additional sources of water from rain remain practically unchanged among the results of the base solution, Alternative 1 and Alternative 2. 

Solution with Penalizations from Alternative 1. TAC for alternative 1 remains lower (10%) compared to the base solution; however, FWS[total] is practically the same for all of the solutions and the difference lies on the payment of fines as well as on the treatment costs. This is why CTR[D] average and CJ[discharge] , despite having more flexibility for relaxation, are not far above from the values of the base solution. 

Solution with Penalizations from Alternative 2. A 1.5% reduction of the TAC (with respect to the base solution) is achieved. A small (but lower than in Alternative 1) increase of the CJ[discharge] is expected; it appears then that domestic wastewater is better suited for recycling rather than discharging it at the upper limit or paying fines. Similarly, it appears that industrial wastewater, being a lower amount, is too expensive to recycle (or even infeasible) and does not have a significant impact in the environmental objectives. 

Further Discussion. Up to this point, the correct estimation of the values of fines might be a limitation to assess the performance of the formulation. The following section deals with this issue through a sensitivity analysis; our intention is not to improve the method to estimate these fines, we only intend to attain a better performance of the formulation proposed within the parameters used in this example. 

## Sensitivity analysis with respect to parameter / 

Fines are estimated in Eqs. 83–84 and 89–90 through the definition of parameters /[d] and /[i] as well as of parameters /[d][;][fixed] and /[i][;][fixed] . Seeking simplicity in this discussion, they all will be assumed as equal to / (/ was equal to 1.1 in the previous results). Alternative 1 for economic penalization is used. Recall that the upper limit for the pollutant is 150 mg/L and that the penalization scheme allows violation up to 

**==> picture [234 x 173] intentionally omitted <==**

Figure 4. Sensitivity analysis of /. 

3432 DOI 10.1002/aic 

August 2017 Vol. 63, No. 8 AIChE Journal 

Published on behalf of the AIChE 

**==> picture [192 x 219] intentionally omitted <==**

Figure 5. Sensitivity analysis of / at a closer range (see Figure 4). 

300 mg/L. Figure 4 shows the sensitivity of the solutions with respect to the value of /; the optimization results for values of / between 1.5 and 0.05 are plotted. The values shown of EPC, CJ[discharge] , CTR[D] , and fine F[d] were normalized with respect to their maximum value (dimensionless variables); that is why their values range between 1 and 0. Notice that, as / goes to 0, the penalty for constraint violation goes to 0, which causes a minimum value of TAC and maximum values of CJ[discharge] and CTR[D] . As the values of / decreases below 1.1 (base solution), the environmental impact (CJ[discharge] and CTR[D] ) in the system does not change until a significantly lower value of around 0.1 is used (see Figures 4 and 5). The value of / equal to 0.1 then seems to represent an optimal compromise between treatment costs and the payment of fines. If / goes to values lower than 0.1, lower fines are paid, the treatment cost is low, TAC decreases but the environmental impact rapidly increases, going to an averaged CTR[D] of 300 mg/L (highest value of CTR[D] in Figure 4). Conversely, if / goes above 0.1, the TAC increases (due to an increment in fines) but treatment costs are practically constant and, as a consequence, the environmental impact also remains practically constant. That is, treatment costs are applied up to a limit concentration of pollutant and the sources pay fines for the violation of the regulation (150 mg/L). The bigger / is, the bigger it is also the fine that the sources pay, since no additional water treatment is applied. 

**==> picture [234 x 110] intentionally omitted <==**

Figure 6. Pareto curves of water consumption from fresh sources scenarios with economic penalizations. 

**==> picture [234 x 110] intentionally omitted <==**

Figure 7. Pareto curves of water consumption from fresh sources without economic penalizations. 

Figure 5 presents a better view of the behavior of the variables for values of / lower than 0.2. Starting at / equal to 0.05, the amount of fines paid (EPC) slightly increases and then drops down as the cost of fines (F[d] ) also drops. Before the local maxima of the EPC (domestic) curve, every pollution source pays fines. Once the solution passes this local maxima, the number of transgressors decreases until it reaches a constant value (constant averaged CTR[D] ). TAC becomes higher because F[d] is also higher due to the value of /. 

**==> picture [234 x 177] intentionally omitted <==**

Figure 8. Monthly average water consumption from different sources in the watershed. 

**==> picture [234 x 179] intentionally omitted <==**

Figure 9. Monthly average BOD discharges from domestic and industrial sources in the watershed. 

DOI 10.1002/aic 3433 

AIChE Journal August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

**==> picture [408 x 492] intentionally omitted <==**

Figure 10. Water and wastewater management in the first river section in April under economic penalizations. [Color figure can be viewed at wileyonlinelibrary.com] 

This analysis shows the significance of the selection of an appropriate penalization scenario for pollution discharges when implemented in a watershed. Also, the results suggest that this approach could be a way of introducing a framework to estimate the discharge limits to regulate sources of pollution. However, a more exhaustive analysis should be made about the economic and environmental tradeoffs. With the value of / equal to 0.1, the TAC is reduced 17% with respect to the base solution (i.e., more than 10 million dollars per year) with an increment of the environmental impact of 1.96 mg/L in the pollution concentration. We believe that this kind of economic benefit could help to implement a large scale distributed treatment system that could still improve the sustainability of a watershed. 

## Pareto set obtained with different upper limits of FWS[total] 

The previous results lead to investigate what the optimal compromise is between pollution abatement and resources management. Figure 6 shows a Pareto set of optimal solutions at different upper limits of water consumption from fresh sources (/ is equal to 0.1). Again, Alternative 1 is used for economic penalizations. 

For values of TAC from 53 to 60 millions of dollars per year, an almost constant value of averaged CTR[D] is observed. The results allow us to select the solution of FWS[total] equal to 255,000,000 m[3] /year, which achieves a TAC of 56,832,429 $/ year with a CTR[D] average and a CJ[discharge] of 129.2 and 

3434 DOI 10.1002/aic 

August 2017 Vol. 63, No. 8 AIChE Journal 

Published on behalf of the AIChE 

7.74 mg/L of BOD, respectively. We consider that this solution balances the economic and environmental objectives to an acceptable degree but, of course, any other solution in the Pareto set could be selected depending on the concerns of decision makers. 

For comparison purposes, similar Pareto curves are shown in Figure 7 for scenarios where no economic penalizations are allowed. At the same value of FWS[total] selected (260M m[3] /year), the TAC is 64,995,600 $/year (12.56% higher); averaged CTR[D] and CJ[discharge] are 99.3 and 6.81 mg/L of BOD, respectively. Also, the TAC remains the same starting from a FWS[total] of around 275,000,000 m[3] /year. 

The next section provides more detailed results of the previously selected solution (FWS[total] equal to 255,000,000 m[3] /year and TAC of 56,832,429 $/year). We are aware that this is not the best solution in terms of environmental impact; it achieves, however, a significant reduction of water consumption when compared to the solution from Alternative 1, labeled as Alternative 1b in Table 5. 

## Optimal solution at FWS[total] 5 255M m[3] /year 

As mentioned before, only Alternative 1 is considered in this solution. There are a vast number of variables that can be observed, but we present only what we consider the key variables. Figure 8 shows the water consumption from different sources throughout the year. The total amount of water needed from artificial ponds is not significant (with a value of 359,870 m[3] /year) compared to the 8,690,044 m[3] /year from storage tanks, and the 21,035,352 m[3] /year from recycled water. This of course relates to the costs as well as the availability from different sources. In months of higher demands, there is not much rainwater available and the consumption from fresh sources is reduced mostly with recycled water. When available, using rainwater is the most cost-effective way of reducing consumption from fresh sources since costs of storage are avoided. Conversely, recycled water is preferred over rainwater in most of the months; apart from availability, that is feasible due to the tight constraints in the concentration of wastewater discharges; otherwise, the recycled water costs would be much higher compared to costs of the storage and distribution of rainwater. 

Figure 9 shows the monthly averages of the discharge concentration from domestic sources (CTR[D] ), the discharge concentration from industrial sources (CTR[I] ), the penalization discharges from domestic sources (DP[d] ), and the penalization discharges from industrial sources (DP[i] ). In every month, the difference between the regulation (150 mg/L) and the actual concentration of the discharges is less in domestic sources than in industrial ones. This happens because industrial wastewater is too polluted and only domestic wastewater is recycled. Finally, to illustrate the scope of the model, a schematic representation of the distribution of water resources and wastewater treatment is shown in Figure 10. Figure 10 considers only the first section of the river in the month of April; note that every node representing sources of water actually includes a greater number of nodes. For instance, the outlets of the treatment interceptors in domestic areas one, two, and three distribute their recycled water to domestic areas one through five and to agricultural area one. In addition, the distribution of rainwater (which includes nine possible tanks and four artificial ponds) is condensed in individual nodes for simplicity. 

In our example, April is one of the highest demanding months. It presents the highest averaged CTR[I] , which is compensated with a middle range averaged CTR[D] ; the rainwater availability is limited in this month and a significant amount of wastewater from domestic sources is recycled, as seen in the three out of five domestic areas with CTR[D] equal to 30 mg/L of BOD. The optimization also found that industrial wastewater should only be treated to achieve almost the penalized discharge limit; this would not be desired in the cases where more industrial areas were involved in the system. Nonetheless, industrial wastewater streams still require a large investment in order to decrease their concentrations to 300 mg/L. The configurations of the interceptors in the wastewater streams are expected to consist mainly of the highest cost technologies if recycled water is needed and of the lower cost technologies if no recycled water is required. 

To present all of the results in the form of Figure 10, 60 additional figures would be needed (5 river sections times 12). This is why we only present a small glimpse of the results in such form. As a final observation of all of the previous discussions, note that it is always desirable to maintain wastewater discharges at least at the concentration limits established by the regulations. However, through this approach, decision makers can choose (from the economical point of view) which sources of pollution are more convenient to treat and/or recycle and which ones should pay fines. Nonetheless, the decision must consider the issue of water resources sustainability through the assessment of alternative water resources, and make sure that adequate and safe levels of pollution are maintained in every part of the system. 

The limitations of our illustrative example should also be remarked. A pseudo-single pollutant case is considered to show the scope of the model, but the incorporation of multiple pollutants could bring a new set of analysis that is not addressed here. The use of a deterministic approach is another important limitation. 

## Conclusions 

Our formulation has shown that a well implemented system of economic penalizations is an interesting approach to deal with pollution abatement over water bodies. The formulation not only considers the issue of dealing with wastewater through a distributed treatment system, but also involves the sustainable management of water, which incorporates alternative water sources to mitigate impact over natural resources. The events occurring in a watershed are complex; however, our results indicate that the performance of the formulation helps understand the behavior of the system and its effect over the environment. 

The economic advantages that can be accomplished for a wastewater treatment system under penalty scenarios show potential. With a thorough analysis and a high understanding of the system, sustainability can be evaluated in order to design a robust penalization scheme that allows flexibility but does not fall outside environmental goals. Nonetheless, paying fines instead of using technologies to deal with pollution has several drawbacks. For instance, public opinion may not always approve pollution sources to violate regulations, since most people might think that pollution has to be treated with as much resources as needed. Furthermore, pollution sources might establish the alternative of paying fines as a policy rather than investing in treatment technologies, a situation that 

DOI 10.1002/aic 3435 

AIChE Journal August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

may not be sustainable if it is not evaluated by considering a long-term scenario. 

The sensitivity analysis with respect to the value of / aims to achieve a minimum cost. Notice that cost reduction involves reducing the amounts of money paid for penalizations; that is, penalizations are considered as a cost. If penalizations are considered as a benefit to environmental agencies or the state, then an alternative approach should be considered. A variable measuring such benefit should lead to constraints and policies used to improve sustainability in the watershed. 

The proposed MINLP model aims to involve as many aspects of sustainability as possible; concerning the complete water lifecycle in a watershed, from its acquisition to its safe disposal to the environment. The purpose of our analysis is to understand the interactions occurring in the watershed and, with this, to propose a solution which can balance the economic and environmental aspects of the system. We do not intend to promote the use of economic penalization strategies; they already exist and are currently applied. Our approach might be used to achieve an optimal implementation of such strategies. 

## Acknowledgment 

The authors thank the financial support provided by the Mexican National Council for Science and Technology (CONACYT), grants 257018 and 253660, and by the Tecnologico Nacional de Mexico, grant 5725.16-P. 

## Notation 

## Sets 

- R 5 {1, 2, 3 . . . nR} = river sections 

- D 5 {1, 2, 3 . . . nD} = domestic areas 

- I 5 {1, 2, 3 . . . nI} = industrial areas 

- A 5 {1, 2, 3 . . . nA} = agricultural areas 

- L 5 {1, 2, 3 . . . nL} = pollutants 

- X 5 {1, 2, 3 . . . nX} = interceptors 

- S 5 {1, 2, 3 . . . nS} = storage tanks 

P 5 {1, 2, 3 . . . nP} = artificial ponds Q 5 {1, 2, 3 . . . nQ} = artificial aquifers T 5 {1, 2, 3 . . . nT} = periods of time 

## Parameters 

- Area[P] p[=][available][area][capable][of][collecting][rainwater][in][artifi-] cial pond p 

- Area[Q] q[=][available][area][capable][of][collecting][rainwater][in][artifi-] cial aquifer q 

- Area[S] s[=][available][area][capable][of][collecting][rainwater][in][storage] tank s 

- A[0] = cost coefficient of storage tanks 

   - B[0] = cost coefficient of storage tanks 

- CW[D] r;d;t[=][consumed] time period[water] t[in][domestic][area][d][,][in][river][section][r][at] CW[I] r;i;t[=][consumed] time period[water] t[in][industrial][area][i][,][in][river][section][r][at] CPrr[J] ;l;t[=][concentration][of][pollutant][l][in][fallen][rainwater][onto][river] section r at time period t 

- CTribr;l;t = concentration of pollutant l in tributaries of river section r at time period t 

- CU[J] r;l;t[=][concentration][of][pollutant][l][in][direct][use][water][from][the] river section r 

- CLossr;l;t = concentrationlosses in river sectionof pollutantr at timel periodin evaporation/filtrationt CT[D] r;d;l;t[=][concentration] water in river[of] section[pollutant] r at time[l][in][untreated] period t[domestic][waste-] CRE[max] l = maximum allowable concentration of pollutant l in recycled water 

- CT[I] r;i;l;t[=][concentration] wastewater in riverof pollutantsection r atl timein untreatedperiod t industrial 

- CWP[d] = treatment cost to achieve environmental constraints (domestic wastewater) 

- CWP[i] = treatment cost to achieve environmental constraints (industrial wastewater) 

- CPG[d] = cost per gram to reduce pollution in domestic wastewater CPG[i] = cost per gram to reduce pollution in industrial wastewater CFF[d] = cost of fixed fines for domestic areas (alternative 2) CFF[i] = cost of fixed fines for industrial areas (alternative 2) Cu[op] x[=][operational][cost][of][interceptor][x] C[0] = cost coefficient of artificial ponds 

- DAAr;a;t = watertime perioddemandt in agricultural area a, in river section r at DDAr;d;t = timewaterperioddemandt in domestic area d, in river section r at DIAr;i;t = timewaterperioddemandt in industrial area i, in river section r at D[0] = cost coefficient of artificial ponds E[0] = cost coefficient of artificial aquifers 

- FCx = fixed cost of interceptor x F[d] = fine per gram for domestic areas (alternative 1) F[i] = fine per gram for industrial areas (alternative 1) 

- F[d][;][fixed] = fixed fine for domestic areas (alternative 2) F[i][;][fixed] = fixed fine for industrial areas (alternative 2) F[0] = cost coefficient of artificial aquifers 

- M[D] = integer number greater than one used for modeling M[I] = integer number greater than one used for modeling M[p] = maximum degree of environmental regulation violation allowed 

- Lossr;t = timelossesperioddue tot evaporation/filtration in river section r at PAr;t = total amount of rainwater in river section r at time period t 

- PCPAr;p;a = unitary piping and pumping (p&p) cost to send rainwater from artificial pond p to agricultural area a 

- PCPDr;p;d = unitary p&p cost to send rainwater from artificial pond p to domestic area d 

- PCPIr;p;i = unitary p&p cost to send rainwater from artificial pond p to industrial area i 

- PCQAr;q;a = unitary p&p cost to send rainwater from artificial pond q to agricultural area a 

- PCQDr;q;d = unitary p&p cost to send rainwater from artificial pond q to domestic area d 

- PCQIr;q;i = unitary p&p cost to send rainwater from artificial pond q to industrial area i 

- PCRDAr;d;a = unitary p&p cost to send recycled water from domestic area d to agricultural area a 

- PCRDDr;d;d = unitary p&p cost to send recycled water from domestic area d to domestic area d 

- PCRDIr;d;i = unitary p&p cost to send recycled water from domestic area d to industrial area i 

- PCRIAr;i;a = unitary p&p cost to send recycled water from industrial area i to agricultural area a 

- PCRIDr;i;d = unitary p&p cost to send recycled water from industrial area i to domestic area d 

- PCRIIr;i;i = unitary p&p cost to send recycled water from industrial area i to industrial area i 

- PCSAr;s;a = unitary p&p cost to send rainwater from storage tank s to agricultural area a 

- PCSDr;s;d = unitary p&p cost to send rainwater from storage tank s to domestic area d 

- PCSIr;s;i = unitary p&p cost to send rainwater from storage tank s to industrial area i 

- PCNSDr;d = unitarytic area p&pd cost to send fresh sources’ water to domesPCNSIr;i = unitarytrial areap&pi cost to send fresh sources’ water to indus- 

- PCNSAr;a = unitarytural areap&pa cost to send fresh sources’ water to agriculP[P] r;p;t[=][available][rainwater][to][collect][in][artificial][pond][p][,][in][riv-] er section r at time period t 

- P[Q] r;q;t[=][available][rainwater][to][collect][in][artificial][pond][p][,][in][riv-] er section r at time period t 

- Prr[J] ;t[=][contribution] in river section[of] r[rainwater] at time period[to][the] t[flow][of][the][main][river] P[S] r;s;t[=][available][rainwater][to][collect][in][storage][tank][s][,][in][river] section r at time period t 

- RC[P] = runoff coefficient of the roofs of houses and buildings (artificial ponds) 

3436 DOI 10.1002/aic 

August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

AIChE Journal 

RC[Q] = runoff coefficient of the roofs of houses and buildings (artificial aquifers) 

   - RC[S] = runoff coefficient of the roofs of houses and buildings (storage tanks) 

   - rxr;l = kineticspollutantofl the reaction carried out in river section r for 

   - TER[d] = total expected reduction of domestic wastewater pollution TER[i] = total expected reduction of industrial wastewater pollution 

   - Tribr;t = contributionin river sectionof rtributariesat time periodto thet flow of the main river Ur[J] ;t[=][direct][use][of][the][main][river’s][superficial][water][in][river] section r at time period t 

- Upperlim[d] r;d;l;t[=][maximum][domestic][wastewater][discharge][limit] Upperlim[i] r;i;l;t[=][maximum][industrial][wastewater][discharge][limit] 

   - Vr;t = volume of river section r 

   - VCx = variable cost of interceptor x 

   - WW[D] r;d;t[=][wastewater] period t[of][domestic][area][d][,][in][river][section][r][at][time] WW[I] r;i;t[=][wastewater] period t[of][industrial][area][i][,][in][river][section][r][at][time] 

## Variables 

- AAPr;p;a;t = rainwater sent from artificial pond p to agricultural area a, in river section r at time period t 

- AAQr;q;a;t = rainwater sent from artificial aquifer q to agricultural area a, in river section r at time period t 

- AFWSr;a;t = agricultural consumption of water from fresh sources in river section r at time period t 

- APr;p;t = amount of rainwater in artificial pond p, in river section r at time period t 

- AP[max] r;p[=][storage][capacity][of][artificial][ponds] 

- AQr;q;t = amount of rainwater in artificial pond q, in river section r at time period t 

- AQ[max] r;q[=][storage][capacity][of][artificial][aquifers] 

- ARWWr;a;t = recycled water sent to agricultural area a, in river section r at time period t 

- ASTr;s;a;t = inrainwaterriver sectionsent fromr at timestorageperiodtankt s to agricultural area a, Cost[p] r;p[=][cost][of][artificial][pond][p][,][in][river][section][r] Cost[q] r;q[=][cost][of][artificial][aquifers][q][,][in][river][section][r] Cost[s] r;s[=][cost][of][storage][tank][s][,][in][river][section][r] 

- CJr;l;t = concentrationod t of pollutant l in river section r at time peri- 

- CJ[discharge] = concentration of pollutants in the final discharge of the main river 

- CTR[D] r;l;d;t[=][concentration][of][pollutant][l][in][treated][domestic][wastewater] discharged into river section r 

- CTR[I] r;l;i;t[=][concentration][of][pollutant][l][in][treated][industrial][wastewater] discharged into river section r 

- DAPr;p;d;t = rainwater sent from artificial pond p to domestic area d, in river section r at time period t 

- DAQr;q;d;t = rainwater sent from artificial aquifer q to domestic area d, in river section r at time period t 

- DFWSr;d;t = domestic consumption of fresh sources’ water in river section r at time period t 

- DRW[in] r;d;t[=][amount][of][domestic][recycled][wastewater] 

- DRWWr;d;t = recycled water sent to domestic area d, in river section r at time period t 

- DSTr;s;d;t = rainwater sent from storage tank s to domestic area d, in river section r at time period t 

- EPC = economic penalization cost 

- fs[d] r;d;x;t[=][amount] x in river[of] section[domestic] r at[wastewater] time period[segregated] t[into][interceptor] fs[i] r;i;x;t[=][amount] tor x in river[of][industrial] section r[wastewater] at time period[segregated] t[into][intercep-] 

- FWSr;t = watertime periodconsumptiont from fresh sources in river section r at 

- FWS[total] = total water consumed from fresh sources 

- IAPr;p;i;t = rainwater sent from artificial pond p to industrial area i, in river section r at time period t 

- IAQr;q;i;t = rainwater sent from artificial aquifer q to industrial area i, in river section r at time period t 

- IFWSr;i;t = industrial consumption of fresh sources’ water in river section r at time period t 

- IRW[in] r;i;t[=][amount][of][industrial][recycled][wastewater] 

- IRWWr;i;t = recycled water sent to industrial area i, in river section r at time period t 

- ISTr;s;i;t = rainwater sent from storage tank s to industrial area i, in river section r at time period t 

- Jr;t = main river’s flow in river section r at time period t 

- NS[P] r;p;t[=][amount][of][not][stored][excess][rainwater][in][artificial][pond][s][,] in river section r at time period t 

- NS[Q] r;q;t[=][amount][of][not][stored][excess][rainwater][in][artificial][aquifer] q, in river section r at time period t 

- NS[S] r;s;t[=][amount][of][not][stored][excess][rainwater][in][storage][tank][s][,][in] river section r at time period t 

- ppNS = piping and pumping cost of fresh sources’ water distribution 

- PPcost = total piping and pumping cost 

- ppRHS = piping and pumping cost of rainwater distribution and storage 

- ppRW = piping and pumping cost of recycled water distribution 

- DP[d] r;d;l;t[=][grams][above][the][environmental][regulation][(domestic wastewater)] DP[i] r;i;l;t[=][grams][above][the][environmental][regulation][(industrial][wastewater)] STr;s;t = amounttime periodof rainwatert in storage tank s, in river section r at 

- STRcost =ST[max] r;s[=][storage] storage[capacity] infrastructure[of][storage] cost[tanks] SW[P] r;p;t[=][amount][of][rainwater][stored][in][artificial][pond][p][,][in][river][sec-] tion r at time period t 

- SW[Q] r;q;t[=][amount][of][rainwater][stored][in][artificial][aquifer][q][,][in][river][sec-] tion r at time period t 

- SW[S] r;s;t[=][amount][of][rainwater][stored][in][storage][tank][s][,][in][river][section] r at time period t 

- TAC = total annual cost 

- TRcost[d] = domestic wastewater treatment cost 

- TRcost[i] = domestic wastewater treatment cost 

- WW[D] r;d[;][dis] ;t[=] river[wastewater] in river[from] section[domestic] r at time[area] period[d][discharged] t[into][the][main] WW[I] r[;] ;[dis] i;t[=][wastewater] river in river[from] section[industrial] r at time[area] period[i][discharged] t[into][the][main] 

## Binary variables 

- z[st] r;s;t[=][existence][of][storage][tanks] z[ap] r;p;t[=][existence][of][artificial][ponds] 

- z[q] r;q;t[=][existence][of][artificial][ponds] 

- yr; d;t = existence of treatment facilities in domestic areas zr;d;x;t = existence of interceptors in the treatment facilities in domestic areas 

- wr; d;t = existence of recycled water from treatment facilities in domestic areas 

- z[i] ry;i[i] r;;xi;;tt[=][=][existence][existence][of][of][treatment][interceptors][facilities][in][the][in][treatment][industrial][facilities][areas][in][industrial] areas 

- w[i] r;i;t[=][existence] al areas[of][recycled][water][from][treatment][facilities][in][industri-] 

- w[p] r;[;] d[d] ;l;t[=][variable] ization scheme[associated] (alternative[to][the][wastewater] 2)[treatment][economic][penal-] w[p] r;[;] i[i] ;l;t[=][variable] ization scheme[associated] (alternative[to][the][wastewater] 2)[treatment][economic][penal-] 

## Greek letters (parameters) 

- b[D] r;d;t[=][maximum][percentage][constraint][of][recycled][water][use][in] domestic areas 

- b[I] r;i;t[=][maximum] trial areas[percentage][constraint][of][recycled][water][use][in][indus-] 

- d[p] p[;][min] = minimum storage constraint of artificial ponds d[p] p[;][max] = maximum storage constraint of artificial ponds d[q] q[;][min] = minimum storage constraint of artificial aquifers d[q] q[;][max] = maximum storage constraint of artificial aquifers d[s] s[;][min] = minimum storage constraint of storage tanks ds[s][;][max] = maximum storage constraint of storage tanks 

- b = exponent used to account for the economies of scale in the cost of storage tanks 

- k = exponent used to account for the economies of scale in the cost of artificial ponds 

- m = exponent used to account for the economies of scale in the cost of artificial aquifers 

- ax;l = removal efficiency of pollutant l in interceptor x 

- Xr[d] ;[;] d[min] ;x[=][minimum][capacity][of][interceptor][x][to][treat][domestic][wastewater] X[d] r;[;] d[max] ;x = maximum capacity of interceptor x to treat domestic wastewater 

DOI 10.1002/aic 

August 2017 Vol. 63, No. 8 

3437 

Published on behalf of the AIChE 

AIChE Journal 

- Xr[i][;] ;[min] i;x[=][minimum capacity][of][interceptor][x][to][treat][industrial][wastewater] X[i] r[;] ;[max] i;x = maximum capacity of interceptor x to treat industrial wastewater 

   - /[d] = coefficient used to enforce environmental regulation compliance (domestic areas) 

   - /[i] = coefficient used to enforce environmental regulation compliance (industrial areas) 

- /[d][;][fixed] = coefficient used to enforce environmental regulation compliance (domestic areas) 

- /[i][;][fixed] = coefficient used to enforce environmental regulation compliance (industrial areas) 

   - u = exponent to account for the economies of scale in treatment facilities 

8. Napoles-Rivera F, Serna-Gonzalez M, El-Halwagi MM, PonceOrtega JM. Sustainable water management for macroscopic systems. J Clean Prod. 2013;47:102–117. 

9. Rojas-Torres MG, N�apoles-Rivera F, Ponce-Ortega JM, Serna-Gonz�alez M, El-Halwagi MM. Optimal design of sustainable water systems for cities involving future projections. Comput Chem Eng. 2014;69:1–15. 

10. Crocker TD. The structuring of atmospheric pollution control systems. In Harold Wolozin (Ed.), The economics of air pollution, New York: W. W. Norton, 1966:61–86. 

11. Dales JH. Pollution, Property & Prices: An Essay in Policy-Making and Economics. Cheltenham, United Kingdom: Edward Elgar Publishing, 2002. 

12. Montgomery WD. Markets in licenses and efficient pollution control programs. J Econ Theory. 1972;5(3):395–418. 

13. Selman M, Greenhalgh S, Branosky E, Jones C, Guiling J. Water quality trading programs: an international overview. WRI Issue Brief. 2009;1(1):15. 

## Literature Cited 

1. WWAP (United Nations World Water Assessment Programme). The United Nations World Water Development Report 2016: Water and Jobs. Paris: UNESCO, 2016. 

2. WHO/UNICEF. Joint Water Supply, Sanitation Monitoring Programme. Progress on Drinking Water and Sanitation: 2014 Update. Geneva, Switzerland: World Health Organization, 2014. 

3. Ponce-Ortega JM, Napoles-Rivera F, El-Halwagi MM, JimenezGutierrez A. An optimization approach for the synthesis of recycle and reuse water integration networks. Clean Technol Environ Policy. 2012;14(1):133–151. 

4. Burgara-Montero O, Ponce-Ortega JM, Serna-Gonz�alez M, ElHalwagi MM. Optimal design of distributed treatment systems for the effluents discharged to the rivers. Clean Technol Environ Policy. 2012;14(5):925–942. 

5. Martinez-Gomez J, Burgara-Montero O, Ponce-Ortega JM, N�apolesRivera F, Serna-Gonz�alez M, El-Halwagi MM. On the environmental, economic and safety optimization of distributed treatment systems for industrial effluents discharged to watersheds. J Loss Prev Process Ind. 2013;26(5):908–923. 

6. Rubio-Castro E, Ponce-Ortega JM, Cervantes-Gaxiola ME, Hernandez-Calderon OM, Ortiz-del-Castillo JR, Mil�an-Carrillo J, Meza-Contreras JA. Optimal design of integrated agricultural water networks. Comput Chem Eng. 2016;84:63–82. 

7. Lira-Barragan LF, Ponce-Ortega JM, Guill�en-Gosalbez G, ElHalwagi MM. Optimal water management under uncertainty for shale gas production. Ind Eng Chem Res. 2016;55(5):1322–1335. 

14. Stephenson K, Shabman L. Rhetoric and reality of water quality trading and the potential for market-like reform. JAWRA J Am Water Resour Assoc. 2011;47(1):15–28. 

15. Hung MF, Shaw D. A trading-ratio system for trading water pollution discharge permits. J Environ Econ Manage. 2005;49(1):83–102. 

16. Prabodanie RR, Raffensperger JF, Milke MW. A pollution offset system for trading non-point source water pollution permits. Environ Resour Econ. 2010;45(4):499–515. 

17. Lopez-Villarreal F, Rico-Ramirez V, Gonz�alez-Alatorre G, QuintanaHernandez PA, Diwekar UM. A mathematical programming approach to pollution trading. Ind Eng Chem Res. 2011;51(17):5922–5931. 

18. Zhang Y, Wu Y, Yu H, Dong Z, Zhang B. Trade-offs in designing water pollution trading policy with multiple objectives: a case study in the Tai Lake Basin, China. Environ Sci Policy. 2013;33:295–307. 

19. L�opez-Villarreal F, Lira-Barrag�an LF, Rico-Ramirez V, PonceOrtega JM, El-Halwagi MM. An MFA optimization approach for pollution trading considering the sustainability of the surrounded watersheds. Comput Chem Eng. 2014;63:140–151. 

20. Vecchietti A, Lee S, Grossmann IE. Modeling of discrete/continuous optimization problems: characterization and formulation of disjunctions and their relaxations. Comput Chem Eng. 2003;27(3):433–448. 

21. Raman R, Grossmann IE. Modelling and computational techniques for logic based integer programming. Comput Chem Eng. 1994; 18(7):563–578. 

22. Rosenthal E. GAMS-A User’s Guide. Washington DC, USA: GAMS Development Corporation, 2008. 

23. Diwekar U. Introduction to Applied Optimization. New York, USA: Springer Science & Business Media, 2008. 

## Appendix: Parameters Used to Estimate Piping and Pumping Costs in the Illustrative Example 

Tables A1–A8 provide the parameters used to estimate the piping and pumping costs with Eqs. 98–101. 

Table A1. Pumping and Piping Unitary Costs for Storage Tanks to Domestic Areas (310[2] $/m[3] ) 

|Storage<br>Tank|Domestic Area<br>1<br>2<br>3<br>4<br>5<br>Storage<br>Tank|Domestic Area|
|---|---|---|
|||1<br>2<br>3<br>4<br>5|
|1.1<br>1.2<br>1.3<br>1.4<br>1.5<br>1.6<br>1.7<br>1.8<br>1.9<br>2.1<br>2.2<br>2.3<br>2.4<br>2.5<br>2.6<br>2.7<br>2.8<br>2.9<br>3.1<br>3.2<br>3.3<br>3.4<br>3.5|4<br>4<br>3<br>2<br>3<br>3.6<br>2<br>1<br>3<br>4<br>1<br>3.7<br>1<br>3<br>1<br>4<br>2<br>3.8<br>2<br>1<br>4<br>3<br>3<br>3.9<br>1<br>4<br>2<br>1<br>4<br>4.1<br>4<br>4<br>3<br>3<br>2<br>4.2<br>2<br>1<br>4<br>1<br>1<br>4.3<br>3<br>4<br>2<br>2<br>3<br>4.4<br>4<br>1<br>1<br>2<br>4<br>4.5<br>4<br>4.6<br>3<br>4.7<br>2<br>4.8<br>1<br>4.9<br>1<br>5.1<br>2<br>5.2<br>3<br>5.3<br>2<br>5.4<br>3<br>5.5<br>1<br>2<br>4<br>2<br>5.6<br>2<br>1<br>4<br>4<br>5.7<br>2<br>1<br>4<br>3<br>5.8<br>4<br>2<br>4<br>4<br>5.9<br>1<br>4<br>3<br>3|2<br>2<br>1<br>3<br>2<br>4<br>3<br>1<br>3<br>3<br>1<br>4<br>1<br>4<br>1<br>1<br>3<br>4<br>3<br>4<br>2<br>1<br>4<br>4<br>1<br>1<br>1<br>3<br>4<br>2<br>4<br>4<br>2<br>3<br>3<br>4<br>3<br>4<br>3<br>3<br>3<br>3<br>1<br>4<br>3<br>1<br>2<br>3<br>3<br>4<br>1<br>2<br>4<br>4<br>2<br>3<br>3<br>2<br>4<br>3<br>3|



3438 DOI 10.1002/aic 

August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

AIChE Journal 

Table A2. Pumping and Piping Unitary Costs for Storage Tanks to Agricultural Areas (310[2] $/m[3] ) 

|Storage<br>Tank|Agricultural Area<br>1<br>2<br>3<br>4<br>5<br>Storage<br>Tank|Agricultural Area|
|---|---|---|
|||1<br>2<br>3<br>4<br>5|
|1.1<br>1.2<br>1.3<br>1.4<br>1.5<br>1.6<br>1.7<br>1.8<br>1.9<br>2.1<br>2.2<br>2.3<br>2.4<br>2.5<br>2.6<br>2.7<br>2.8<br>2.9<br>3.1<br>3.2<br>3.3<br>3.4<br>3.5|4<br>3<br>5<br>2<br>5<br>3.6<br>3<br>2<br>5<br>5<br>3<br>3.7<br>3<br>4<br>3<br>2<br>5<br>3.8<br>2<br>2<br>4<br>5<br>4<br>3.9<br>2<br>4<br>3<br>2<br>5<br>4.1<br>5<br>3<br>2<br>5<br>5<br>4.2<br>5<br>5<br>5<br>2<br>4<br>4.3<br>5<br>2<br>4<br>4<br>5<br>4.4<br>3<br>3<br>3<br>5<br>2<br>4.5<br>4<br>3<br>2<br>3<br>3<br>4.6<br>3<br>3<br>2<br>3<br>3<br>4.7<br>3<br>3<br>4<br>3<br>3<br>4.8<br>5<br>4<br>5<br>4<br>4<br>4.9<br>4<br>4<br>5<br>2<br>5<br>5.1<br>5<br>5<br>2<br>2<br>3<br>5.2<br>3<br>4<br>5<br>4<br>2<br>5.3<br>5<br>4<br>4<br>3<br>3<br>5.4<br>5<br>2<br>5<br>2<br>4<br>5.5<br>2<br>4<br>5<br>5.6<br>4<br>2<br>4<br>5.7<br>3<br>4<br>5<br>5.8<br>2<br>4<br>3<br>5.9<br>2<br>2<br>5|5<br>3<br>3<br>2<br>3<br>3<br>5<br>2<br>4<br>4<br>3<br>2<br>4<br>4<br>2<br>4<br>2<br>4<br>3<br>5<br>5<br>5<br>4<br>3<br>4<br>4<br>3<br>5<br>4<br>4<br>5<br>4<br>5<br>2<br>5<br>2<br>5<br>3<br>4<br>5<br>2<br>5<br>2<br>5<br>3<br>3<br>5<br>5<br>4<br>4<br>4<br>4<br>2<br>3<br>5<br>5<br>4<br>3<br>4<br>2<br>4<br>5<br>2<br>4<br>5<br>4<br>2<br>5<br>3<br>3<br>5<br>3<br>3<br>2<br>2<br>4<br>2<br>5<br>3<br>5<br>5<br>3<br>2<br>4|



Table A3. Pumping and Piping Unitary Costs for Storage Tanks to Industrial Areas (310[2] $/m[3] ) 

|Table A3. Pumping and|Piping Unitary Costs for Storage Tanks to Industrial Areas (3102 $/m3)|
|---|---|
|Storage Tank|Industrial Area|
||1<br>2<br>3<br>4|
|1.1<br>1.2<br>1.3<br>1.4<br>1.5<br>1.6<br>1.7<br>1.8<br>1.9<br>3.1<br>3.2<br>3.3<br>3.4<br>3.5<br>3.6<br>3.7<br>3.8<br>3.9|3<br>2<br>4<br>3<br>4<br>2<br>4<br>3<br>3<br>3<br>2<br>3<br>3<br>3<br>2<br>4<br>4<br>3<br>2<br>2<br>4<br>3<br>4<br>4<br>2<br>2<br>4<br>3<br>2<br>4<br>3<br>2<br>4<br>3<br>4<br>4<br>2<br>2<br>3<br>4<br>4<br>3<br>3<br>2<br>4<br>2<br>4<br>2<br>4<br>2<br>2<br>3<br>3<br>3<br>3<br>2<br>2<br>4<br>3<br>3<br>4<br>4<br>3|



Table A4. Pumping and Piping Unitary Costs for Artificial Ponds to Domestic Areas (310[2] $/m[3] ) 

|Table A4. Pumping|and Piping Unitary Costs for Artifcial Ponds to Domestic Areas (3102 $/m3)|
|---|---|
|Artifcial Pond|Domestic Area|
||1<br>2<br>3<br>4<br>5|
|1.1<br>1.2<br>1.3<br>1.4<br>2.1<br>2.1<br>2.3<br>2.4<br>3.1<br>3.2<br>3.3<br>3.4<br>4.1<br>4.2<br>4.3<br>4.4<br>5.1<br>5.2<br>5.3<br>5.4|4<br>6<br>4<br>6<br>5<br>5<br>5<br>6<br>4<br>4<br>5<br>5<br>4<br>6<br>5<br>5<br>6<br>4<br>6<br>6<br>4<br>6<br>6<br>4<br>6<br>6<br>4<br>5<br>4<br>6<br>5<br>5<br>6<br>6<br>5<br>6<br>4<br>5<br>4<br>4<br>5<br>5<br>5<br>6<br>6<br>5<br>5<br>6<br>5<br>5<br>5<br>6<br>6<br>4<br>4<br>6<br>5<br>6<br>5<br>5|



DOI 10.1002/aic 3439 

August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

AIChE Journal 

Table A5. Pumping and Piping Unitary Costs for Artificial Ponds to Agricultural Areas (310[2] $/m[3] ) 

|Artifcial Pond|Agricultural Area|
|---|---|
||1<br>2<br>3<br>4<br>5|
|1.1<br>1.2<br>1.3<br>1.4<br>2.1<br>2.1<br>2.3<br>2.4<br>3.1<br>3.2<br>3.3<br>3.4<br>4.1<br>4.2<br>4.3<br>4.4<br>5.1<br>5.2<br>5.3<br>5.4|3<br>1<br>2<br>3<br>2<br>2<br>1<br>2<br>1<br>1<br>2<br>3<br>1<br>2<br>3<br>2<br>2<br>3<br>3<br>1<br>1<br>1<br>2<br>3<br>3<br>3<br>1<br>3<br>1<br>3<br>3<br>2<br>2<br>1<br>1<br>1<br>2<br>2<br>2<br>2<br>2<br>2<br>2<br>2<br>1<br>1<br>3<br>1<br>1<br>1<br>3<br>3<br>3<br>1<br>2<br>1<br>1<br>3<br>3<br>3<br>1<br>2<br>1<br>2<br>1<br>2<br>2<br>3<br>2<br>3<br>1<br>3<br>2<br>2<br>3<br>3<br>1<br>2<br>2<br>3<br>1<br>2<br>1<br>3|



Table A6. Pumping and Piping Unitary Costs for Artificial Ponds to Industrial Areas (310[2] $/m[3] ) 

|Artifcial<br>Pond|Industrial Area|
|---|---|
||1<br>2<br>3<br>4<br>5|
|1.1<br>1.2<br>1.3<br>1.4<br>3.1<br>3.2<br>3.3<br>3.4|5<br>3<br>4<br>3<br>3<br>4<br>6<br>3<br>6<br>4<br>5<br>3<br>4<br>5<br>3<br>5<br>4<br>4<br>6<br>5<br>3<br>3<br>6<br>5<br>6<br>6<br>3<br>3|



Table A7. Pumping and Piping Unitary Costs of Recycling Water from Domestic Areas (310[2] $/m[3] ) 

|Domestic<br>Area|Agricultural<br>Area<br>1<br>2<br>3<br>4<br>5|Industrial<br>Area<br>1<br>2<br>3<br>4|Domestic<br>Area|
|---|---|---|---|
||||1<br>2<br>3<br>4<br>5|
|1.1<br>1.2<br>1.3<br>1.4<br>1.5<br>2.1<br>3.1<br>3.2<br>3.3<br>3.4<br>4.1<br>4.2<br>4.3<br>5.1<br>5.2|1<br>1.5<br>2.5<br>2.5<br>3<br>1<br>1<br>2.5<br>2.5<br>3<br>1.5<br>1.5<br>2<br>2<br>2.5<br>1.5<br>1.5<br>1.5<br>2<br>2<br>2.5<br>3<br>1<br>1<br>1.5<br>1<br>1.5<br>1<br>1<br>1<br>2<br>2.5<br>3<br>1.5<br>1.5<br>2<br>1<br>1.5<br>1.5<br>2<br>1.5<br>1<br>1<br>2<br>2.5<br>2<br>1.5<br>2<br>2<br>1.5<br>2.5<br>3<br>3<br>2.5<br>2<br>1.5<br>1.5<br>2.5<br>2<br>1.5<br>1<br>1.5|3.1<br>5.3<br>5.6<br>4.4<br>4.8<br>3.2<br>4.4<br>5.6<br>3.5<br>4.1<br>5.9<br>5.4<br>5.5<br>4.7<br>4.9<br>3.7<br>3.3<br>4.3<br>4.5<br>5.8<br>5.5<br>4<br>4.3<br>5.4<br>4.7<br>5<br>4.5<br>4<br>5.3<br>5.9<br>4.1|0.1<br>0.9<br>0.6<br>0.2<br>0.6<br>0.5<br>0.1<br>0.2<br>0.8<br>0.8<br>0.2<br>0.3<br>0.1<br>1.0<br>0.7<br>0.4<br>1.0<br>0.9<br>0.1<br>0.4<br>0.9<br>0.3<br>0.3<br>0.2<br>0.1<br>0.1<br>0.1<br>0.3<br>0.7<br>0.7<br>0.5<br>0.1<br>0.2<br>0.5<br>0.2<br>0.7<br>0.1<br>0.2<br>0.8<br>0.9<br>1.0<br>0.1<br>0.1<br>0.4<br>0.2<br>0.7<br>0.1<br>0.7<br>0.2<br>0.9<br>0.1<br>0.1<br>0.3<br>0.2<br>0.1|



DOI 10.1002/aic 

August 2017 Vol. 63, No. 8 AIChE Journal 

3440 

Published on behalf of the AIChE 

Table A8. Pumping and Piping Unitary Costs of Recycling Water from Industrial Areas (310[2] $/m[3] ) 

|Industrial Area|Agricultural Area<br>1<br>2<br>3<br>4<br>5|Industrial Area<br>1<br>2<br>3<br>4|Domestic Area|
|---|---|---|---|
||||1<br>2<br>3<br>4<br>5|
|1.1<br>1.2<br>1.3<br>3.1<br>3.2<br>3.3<br>3.4|2.5<br>2<br>3<br>3<br>3<br>3<br>2.5<br>3<br>3<br>2.5<br>4<br>3.5<br>2<br>1.5<br>1<br>2<br>2.5<br>3<br>1.5<br>1<br>2.5<br>1<br>1<br>1.5<br>1.5<br>1<br>1|0.1<br>0.9<br>0.2<br>0.4<br>0.1<br>0.3<br>0.2<br>0.4<br>0.1<br>0.1<br>0.6<br>0.4<br>0.2<br>1<br>0.1<br>0.4<br>0.8<br>0.8<br>0.2<br>0.1<br>1<br>0.2<br>1<br>0.2<br>0.1|2<br>1.1<br>1.8<br>1.8<br>1<br>1.7<br>1.8<br>2.3<br>1.1<br>2.4<br>1.2<br>1.8<br>2.3<br>2.2<br>2.4<br>1.8<br>2.4<br>2.2<br>2.3<br>1.1<br>1.4<br>2.5<br>1.8<br>1<br>1.7<br>2.5<br>2<br>2.3<br>1.1<br>1.2<br>1.9|



Manuscript received Oct. 2, 2016, and revision received Feb. 13, 2017. 

DOI 10.1002/aic 3441 

AIChE Journal August 2017 Vol. 63, No. 8 

Published on behalf of the AIChE 

