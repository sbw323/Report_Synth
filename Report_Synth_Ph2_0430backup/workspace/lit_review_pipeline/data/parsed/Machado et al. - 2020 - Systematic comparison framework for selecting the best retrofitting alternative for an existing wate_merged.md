EDITOR’S CHOICE— RESEARCH ARTICLE 

**==> picture [77 x 16] intentionally omitted <==**

## **Systematic comparison framework for selecting the best retrofitting alternative for an existing water resource recovery facility** 

## **Vinicius Cunha Machado , Javier Lafuente , Juan Antonio Baeza** 

GENOCOV, Department of Chemical, Biological and Environmental Engineering, Universitat Autònoma de Barcelona, Bellaterra, Spain 

Received 3 January 2020; Revised 5 April 2020; Accepted 21 May 2020 

Departament d'Innovació, Universitats i Empresa, Generalitat de Catalunya; Secretaría de Estado de Investigación, Desarrollo e Innovación, Grant/Award Number: CTQ2014-60495-R 

Additional Supporting Information may be found in the online version of this article. 

Correspondence to: Juan Antonio Baeza, GENOCOV, Department of Chemical, Biological and Environmental Engineering, Universitat Autònoma de Barcelona, Bellaterra, Spain. Email: juanantonio.baeza@uab.cat 

*WEF Member. 

## **• Abstract** 

A systematic comparison framework for selecting the best retrofitting alternative for a water resource recovery facility (WRRF) is proposed in this work. The procedure is applied comparing different possible plant configurations to retrofit an existent anoxic/oxic (A/O) WRRF (Manresa, Spain) aiming to include enhanced biological phosphorus removal (EBPR). The framework for comparison was built on system analysis using a calibrated IWA ASM2d model. A multicriteria set of performance variables, as the operational and capital expenditures (OPEX and CAPEX, respectively) and robustness tests for measuring how fast the plant configuration refuses external disturbances (like ammonium and phosphate peak loads), were used for comparison. Starting from the existent WRRF, four plant configurations were tested: single A[2] /O (only one anoxic reactor converted to anaerobic), double A[2] /O (two anoxic reactors converted to anaerobic), BARDENPHO, and UCT. The double A[2] /O plant configuration was the most economical and reliable alternative for improving the existent Manresa WRRF capacity and implementing EBPR, since the effluent quality increased 3.8% compared to the current plant configuration. In addition, the double A[2] /O CAPEX was close to €165,000 which was at the same order of the single A[2] /O and lower than the BARDENPHO and UCT alternatives. © 2020 Water Environment Federation 

## **• Practitioner points** 

- Four configurations including EBPR were evaluated for retrofitting an A/O WRRF. 

- A new multicriteria comparison framework was used to select the best configuration. 

Published online 02 July 2020 in Wiley Online Library (wileyonlinelibrary.com) DOI: 10.1002/wer.1368 

© 2020 Water Environment Federation 

- Up to 13 criteria related to effluent quality, robustness and costs were included. 

- A single function based on the combination of all the criteria was also evaluated. 

## **• Key words** 

A[2] /O; ASM2d; EBPR; retrofitting; WRRF 

## **Introduction** 

Water resource recovery facilities (WRRFs) were created originally to remove only organic matter (Ardern & Lockett, 1914). Along the years, nitrogen (N) removal and, more recently, phosphorus (P) removal (Barnard, Dunlap, & Steichen, 2017; Yang, Shi, Ballent, & Mayer, 2017) have been a new focus. Nevertheless, many of the existing facilities are not designed to remove P biologically and need the addition of chemical precipitant agents such as ferric chloride. As a result, important amounts of chemical sludge are generated that must be disposed, besides the elevated costs of chemicals. To implement enhanced biological phosphorus removal (EBPR), the sludge must be subjected to alternating anaerobic and anoxic/aerobic conditions. Fermentation products as volatile fatty acids (VFAs) are produced at the anaerobic zone, which are consumed by the polyphosphate accumulating organisms (PAO), releasing P to the mixed liquor, and producing polyhydroxyalkanoates (PHA) as internal storage polymer. At 

Water Environment Research • 92: 2072–2085, 2020 

## EDITOR’S CHOICE— RESEARCH ARTICLE 

the anoxic and aerobic zones, PAO grow on PHA taking up P from the mixed liquor and decreasing its concentration. At the effluent of the WRRF, the net balance of P is negative since the last step takes up more P than that previously released anaerobically. As one of the advantages, biomass density increases with polyphosphate content, and EBPR plants have higher density and better settleability than non-EBPR plants (Schuler & Jang, 2007). EBPR also decreases bulking problems caused by filamentous bacteria due to the selector effect of the anaerobic reactor (van Loosdrecht, Brandse, & de Vries, 1998; Orhon & Artan, 1994). 

In Catalonia, about 21.4% of the WRRF are removing P (ACA—Agència Catalana d’Aigües, 2020—Catalonian Water Agency), but most of them are doing it by chemical precipitation (Figure S1). In addition, this percentage must be increased to accomplish current nutrient removal legislation (EEC Council, 1991) (Table S1). Thereby, there is a strong necessity for retrofitting these plants in order to convert them into plants able to remove biologically COD, N, and P. Several classical configurations of activated sludge (AS) plants that allow EBPR are presented in the literature (Tchobanoglous, Burton, & Stensel, 2013), while alternative configurations are currently being proposed to achieve more reliable P-removal (Barnard et al., 2017; Onnis-Hayden et al., 2020). Figure 1 shows the most classical configurations to implement EBPR. The anaerobic/ anoxic/oxic (A[2] /O) promotes PAO activity by adding an anaerobic reactor to the typical anoxic/oxic (A/O) configuration for nitrification/denitrification, typically referred to as modified 

Ludzack–Ettinger (MLE) configuration. BARDENPHO adds two additional stages (anaerobic/anoxic/oxic/anoxic/oxic configuration) with the objective to improve denitrification to decrease the amount of nitrate recycled to the anaerobic reactor. The University Cape Town (UCT) configuration (anaerobic/anoxic/anoxic/oxic) minimizes the dissolved oxygen (DO) and nitrate input to the anaerobic zone (van Loosdrecht et al., 1998), but requires two internal recycles of mixed liquor and an external recycle of concentrated sludge. 

The performance of each configuration can be assessed using modeling techniques to select the optimal one for a given wastewater flow and composition (Guerrero, FloresAlsina, Guisasola, Baeza, & Gernaey, 2013). However, there are only a few works describing a systematic procedure for retrofitting an existing WRRF to other plant configurations to improve effluent quality without expending many resources. Early examples of plant upgrades found in the literature were not based on modeling tools, but on classical design criteria and expert knowledge of the implemented processes (e.g., Jardin et al., 2000; van Loosdrecht et al., 1998). Benedetti, Bixio, Claeys, and Vanrolleghem (2008) developed tools for a model-based benefit/cost/risk analysis of WRRF alternatives. Variability and uncertainty were later incorporated in WRRF design (Benedetti et al., 2013). Recently, decision support systems using static models and multicriteria evaluation (Castillo, Cheali, et al., 2016; Castillo, Porro, et al., 2016) have demonstrated their capability to support decision-makers in selecting treatment alternatives for retrofitting WRRFs. The 

**==> picture [483 x 296] intentionally omitted <==**

**Figure 1.** Activated sludge WRRF configurations including EBPR that were evaluated in this work. (a) A[2] /O; (b) BARDENPHO; (c) UCT. 

Water Environment Research • 92: 2072–2085, 2020 

2073 

## EDITOR’S CHOICE— RESEARCH ARTICLE 

optimal selection of WRRF processes using a superstructure optimization framework was also reported by Bozkurt, van Loosdrecht, Gernaey, and Sin (2016), where the early stage decision was addressed. Plantwide modeling (PWM) developments as reported by Fernández-Arévalo et al. (2017) have also shown a refined analysis of different plant configurations from a techno-economic point of view. Although all these works provide some interesting features for the selection of retrofitting alternatives, they are usually based on static modeling and do not consider simultaneously the variability on effluent quality, robustness to disturbance, operating costs, and implementation costs, while EBPR is not the focus. 

The usual alternatives of plant configurations for implementing EBPR also show a considerable degree of mass integration, like sludge recycles or mixed liquor recycles. The term “mass integration” refers to making a stream from one part of the process useful in another part of the process in an intelligent way. Moreover, the effect of recycling of nutrients from solids-handling processes to the mainstream can have also detrimental effects (Kassouf et al., 2019). These facts bring extra difficulties for the control of these systems, since the performance of a determined process could affect the performance of others that occur in the upstream zone as studied in previous works (Machado, Gabriel, Lafuente, & Baeza, 2009; Machado, Lafuente, & Baeza, 2014, 2015; Ostace et al., 2013). For instance, if the denitrification process works poorly because of lack of COD and then internal recycle is increased, DO may be carried out to the anoxic zone worsening denitrification. 

In addition to this mass integration, WRRF effluent discharge limits have become even more stringent along the years, with regard to the pollutant concentration, in particular COD, BOD5, total N, and total P, pushing up the plants to its physical limitations. In the case of Europe, the European Community directive for regulating effluent concentrations (EEC Council, 1991) defined discharge limits for WRRF effluent (Table S1). Nevertheless, these limits are getting older and 

more restrictive limits are expected after the revision of this directive currently in progress (European Commission, 2018). 

The retrofitting of an existent WRRF to face new requirements (Figure S2) should respect the legal limits of effluent discharge, as stated in Table S1, the physical and economic constraints and needs to deal with the control constraints like the mass integration commented before. In addition, the retrofitting process should reach the maximum plant stability to face external disturbances and to achieve, at least, the same performance of pollutant removal of the existent plant. 

Considering these requirements, this work presents a systematic comparison framework for selecting the best retrofitting alternative for a WRRF. The procedure is applied to retrofit an existent A/O WRRF to a configuration able to remove COD, N, and P biologically. The four alternatives proposed were based on parts of the existent WRRF, without adding new reactors to avoid a significant increase of the capital expenditures (CAPEX), but changing operational conditions and using new recycle streams to favor the desired biological processes. The operational expenditures (OPEX), CAPEX, and a set of performance criteria, like effluent quality and robustness for external disturbances refusal, were used to determine the best alternative. The multicriteria comparison was complemented with a single comparison criteria based on its combination considering different weights and with the evaluation of the robustness of the decision in a sensitivity analysis. 

## **Methodology** 

## **Brief description of the Manresa WRRF** 

The Manresa WRRF is a standard AS A/O WRRF for biological COD and N removal. It has two treatment lines (Figure 2 and Figure S3), each line with three anoxic reactors in series (1,460 m[3] each reactor), an aerobic reactor made up by two parts of 3,391 m[3] , and a secondary settler to separate the treated wastewater from the concentrated activated sludge that is sent 

**==> picture [483 x 209] intentionally omitted <==**

**Figure 2.** Configuration details and monitored variables of the Manresa WRRF. 

_Machado et al._ 

2074 

## EDITOR’S CHOICE— RESEARCH ARTICLE 

back to the anoxic zone (external recycle). The internal recycle flow returns part of the nitrate yielded by the ammonium oxidation in the aerobic zone to the anoxic zone to promote the denitrification process. Chemical precipitation of P is accomplished by adding, in a small contact chamber, ferric chloride to the stream flowing from the aerobic reactor to the secondary settler. The effluent, after leaving the secondary settler, is disposed to the environment at the Cardener River. 

Daily analyses of COD, BOD5, total suspended solids (TSS), NH[+] 4[,][NO][−] 3[,][PO][3] 4[−][, total Kjeldahl nitrogen (TKN), and ] total nitrogen (TN) are done at the influent and the effluent of the secondary treatment. 

The air supply system is composed by four air blowers, whose motor speed is controlled by a single DO feedback controller in the aerobic basins, which receives the information of four DO probes placed along the aerobic basin and tries to maintain the average DO concentration equal to 2.0 mg/L. 

The main OPEX are the electrical energy for aeration and pumping, sludge treatment (anaerobic digestion and composting of the sludge), and the chemical products for P precipitation. 

## **Premises of the A/O WRRF retrofitting** 

The idea of retrofitting the Manresa WRRF is not to change abruptly all the current plant configuration, process technology (suspended growth to attached growth biomasses for instance), nor increasing costs, nor interfere with the current operation of the plant, since the existent plant should be working simultaneously to the changes of the retrofitting project. Besides, the operators should be trained in the new way of operating and this is another reason why extreme changes at the same time are not welcome. The main idea is to use all of the existent plant data and operation knowledge to save labor to improve the facility. 

A typical alternative to improve plant performance for an A/O configuration is to add an anaerobic step ahead of the anoxic one (Tchobanoglous et al., 2013). This modification can decrease or even eliminate the amount of chemical agent for P precipitation (reduction of the operating costs) and can improve sludge settleability. To add an anaerobic volume to the existent A/O WRRF and at the same time keeping the process in continuous operation, it was decided to test a decrease of the existent anoxic volume, changing the connection of the internal recycle, to avoid building new plant compartments. The addition of external organic matter may be evaluated in order to keep the denitrification rate, if the simulation step (current model) indicated lack of anoxic volume or carbon source. 

All the proposed alternatives should be evaluated using the following criteria: CAPEX, OPEX, effluent quality, and plant controllability (robustness of the control system under disturbances and accomplishing legal restrictions as detailed in previous works (Machado, Lafuente, & Baeza, 2015)). 

## **Plant model development** 

The evaluation of process performance for the retrofitting of the Manresa WRRF was a model-based study based on the ASM2d model (Henze, Gujer, Mino, & van Loosdrecht, 2000) for describing the biological processes, while the Takács model 

(Takács, Patry, & Nolasco, 1991) was selected for modeling the settling process. The wastewater characterization and ASM2d calibration were based on previous studies (Machado, Lafuente, & Baeza, 2014; Machado, Tapia, Gabriel, Lafuente, & Baeza, 2009), using experimental samples from the influent to the secondary treatment, which included the effluent from the primary settler and the reject water from the anaerobic digestion. The influent data used for the dynamic simulations were based on the real values measured in the plant, including concentration of main pollutants and temperature. 

Once the process model of the current facility was developed and the physical, economical, legal, and process control limitations were identified, a set of technical alternatives were evaluated to improve the performance of the existent WRRF. Process models were developed for the new plant layouts, one for each scenario, to evaluate operating costs, effluent quality, and the robustness of each tested plant configuration in terms of rejecting load disturbances of ammonium and phosphate. All configurations were simulated using the same operational parameters for sludge retention time (SRT = 10 days), internal recycle ratio (IRR = 2, i.e., _QIR_ = 2 _QIN_ ), and external recycle ratio (ERR = 0.3, i.e., _QER_ = 0.3 _QIN_ ). 

## **Criteria for selecting the best plant configuration** 

**Effluent quality** . The European Community directive for WRRF discharge limits was applied to the simulation data as a first criterion for measuring the performance of the different configurations regarding the effluent quality. The average values of total P, N- NH[+] 4[, N- ][NO][−] 3[, TSS, TKN, total N, COD, and BOD][5] of the effluent stream were computed. Besides, the peak and the flow-weighted average concentrations of the abovementioned variables were calculated for all the plant configurations tested. Specifically for variables COD, BOD5, total N, and total P (related to the EC Directive), the percentages of reduction were calculated with the influent and effluent annual average concentrations. 

**Robustness of the plant configurations** . The different retrofitting alternatives were tested under extreme operational conditions of the WRRF to evaluate its robustness. The modeled tests included increasing the ammonium and phosphate concentration in the WRRF influent and observing the effluent response. This stress condition tested how fast the plant configurations naturally refused these external disturbances. 

**Economical: investment and operating costs** . Investment costs and operating costs are fundamental issues for a retrofitting process. The main investment cost in the studied retrofitting process is the construction of an anaerobic reactor upstream the conventional A/O process. Hence, land, concrete, steel, earth-moving services, modifications in the biomass recycle line, and the exit line of the primary settler should be provided to perform this task. One alternative not to build new basins is to use part of the anoxic volume as anaerobic volume, just modifying the point where the internal recycle (nitrate recycle) is connected to the process. In this case, only earth moving services and piping services would be necessary. 

Water Environment Research • 92: 2072–2085, 2020 

2075 

## EDITOR’S CHOICE— RESEARCH ARTICLE 

The cost used for materials and services are summarized in Table 1 (US-EPA, 2000). Although data used are neither updated nor localized values, they are useful as a framework for comparison among the evaluated alternatives. 

The most relevant operating costs, aeration, pumping, chemical additions, sludge production, and effluent costs related to penalties when surpassing discharge limits, were based on previous works (Gernaey, Jeppsson, Vanrolleghem, & Copp, 2014; Machado, Gabriel, et al., 2009; Stare, Vrečko, Hvala, & Strmčnik, 2007; Steffens & Lant, 1999; Vanrolleghem & Gillot, 2002). This methodology provides a common simplified framework to compare the daily operating cost of the secondary treatment of a WRRF, as summarized by Equation (1). 

**==> picture [196 x 10] intentionally omitted <==**

Solids concentration in the purge flow was estimated with a solids balance around the settler (Equation 5), assuming that solids concentration in the effluent flow stream was negligible and the biomass hold up in the settler was approximately constant. 

**==> picture [194 x 23] intentionally omitted <==**

where _XTSSLR_ is the solids concentration in the stream that comes from the reactors to the settler. Thereby, it is possible to estimate the sludge production using Equations (4) and (5) and its treatment costs by multiplying by _γSP_ (to convert kg into monetary units). 

Finally, effluent fines were calculated by Equation (6) (Stare et al., 2007), considering ammonium, total nitrogen (TN), and phosphate as the main pollutants. 

**==> picture [235 x 24] intentionally omitted <==**

**==> picture [249 x 18] intentionally omitted <==**

where _AE_ and _PE_ are aeration and pumping energy [kWh/d], _SP_ is the sludge production [kg/d], _EF_ are effluent fines [€/d], and _CC_ are chemicals cost (ferric chloride and external carbon source) in [€/d]. The conversion factors, _γE_ and _γSP_ , are 0.1 €/kWh and 0.5 €/kg (Stare et al., 2007). Aeration energy was calculated by Equation (2), for _r_ aerobic reactors (Copp, Spanjers, & Vanrolleghem, 2002). 

**==> picture [215 x 30] intentionally omitted <==**

where _kLai_ is the oxygen transfer rate [d[−1] ] of each aerobic reactor. 

Pumping energy was calculated by Equation (3), where _PF_ is a pump factor (0.04 kWh/m[3] ) to convert flow rate into energy (Copp et al., 2002). 

**==> picture [189 x 12] intentionally omitted <==**

Instantaneous sludge production was calculated by Equation (4), 

**==> picture [158 x 14] intentionally omitted <==**

**Table 1.** Investment cost associated with the retrofitting process of an A/O plant 

|ITEM<br>Earth moving services<br>Piping (material)<br>Piping (services)<br>Concrete<br>Civil project and<br>documentation|COSTS<br>50.00 €/m3<br>~15.00 €/m<br>~15.00 €/m<br>~300.00 €/m3<br>~15,000.00 €|
|---|---|



where C[EFF] and _C_ are the effluent concentration and disj _L,j_ charge limit of the pollutant “ _j_ ”, respectively; Δ _αj_ is the slope of the curve _EF_ versus C[EFF] j when C[EFF] j _≤ CL,j_ ; and Δ _βj_ is the slope when C[EFF] j > _CL,j_ . The _Heaviside_ function is one when C[EFF] > _C_ and otherwise is zero. The values j _L,j_ of all parameters involved in the _EF_ calculation are given in Table S2. 

Ammonium, nitrate, and phosphate effluent concentrations are estimated by the model. The parameter values for _EF_ calculation concerning ammonium and TN were obtained from Stare et al. (2007). Phosphate parameters for effluent fines calculations were assumed equal to the ammonium parameters except for the effluent discharge limit (Gernaey & Jørgensen, 2004). Figure S4 shows the three effluent fine curves (ammonium, total nitrogen, and phosphate). 

**Multicriteria comparison and single performance index** 

**calculation** . All the criteria previously described for selecting the best retrofitting alternative are based on different measurement types and hence are difficult to compare. Therefore, the different criteria were standardized in ratings in the range of 0–10 points using linear interpolation as a simple option able to provide good discrimination among alternatives. The minimum and maximum reference values detailed in Table S3 were selected based on the range of values obtained in the simulations and with the goal of obtaining significant differences among alternatives. 

Then, a single performance index was calculated by adding the different independent criteria previously developed, using the same weight of one for each criterion. An additional sensitivity analysis with four different sets of weights selected by expert knowledge was also used to evaluate the single performance index to ensure a robust final decision of the best retrofitting alternative (Table S4). 

_Machado et al._ 

2076 

EDITOR’S CHOICE— RESEARCH ARTICLE 

## **Results and discussion** 

The complete procedure for selecting the best retrofitting alternative with the new systematic comparison framework was applied to the A/O WRRF of Manresa (Spain). The methodology starts with the proposal of different alternatives based on process knowledge (Section 3.1) and then compares the performance of the alternatives based on conventional operation (Section 3.2) and when tested for robustness (Section 3.3). Alternatives are evaluated on the basis of economic criteria (Section 3.4) and then compared (Section 3.5) using the multicriteria approach and the single performance index based on the combination of different criteria. Finally, Section 3.6 discusses the limitations of the methodology and compares it with previous works. 

## **Proposed alternatives** 

Based on the particularities of the A/O existent plant and respecting the design premise of minimizing changes and keeping the WRRF processes completely continuous, four retrofitting alternatives were tested for incorporating EBPR, as follows: (a) A[2] /O with two anaerobic reactors (configuration A[2] /O-D, of double anaerobic volume); (b) A[2] /O with one anaerobic reactor (configuration A[2] /O-S, of single anaerobic volume); (c) BARDENPHO configuration; and (d) UCT. 

A[2] /O-D configuration (Figure S5) can be obtained by converting one of the three anoxic reactors per line into an anaerobic reactor. The most important change from the current configuration is modifying the internal recycle, which demands new wastewater lines and connections to the forward anoxic basins. 

**Table 2.** Performance of all the tested alternatives according to the EC directive criteria and other current parameters commonly monitored in full-scale WRRFs 

|**Table 2.**Performance of all the tested<br>in full-scale WRRFs|alternatives according to the EC directive criteria and other current parameters commonly monitored|
|---|---|
|VARIABLE COMPUTED WITH<br>EFFLUENT DATA|CONFIGURATION<br>A/O (CURRENT)<br>A2/O-S<br>A2/O-D<br>BARDENPHO<br>UCT|
|Average concentration [mg/L]<br>Total P<br>2.0<br>0.8<br>0.61<br>1.0<br>0.47<br>N-NH4<br>2.9<br>2.9<br>2. 9<br>19.4<br>2.9<br>N-NO3<br>8.4<br>8.1<br>7.9<br>5.2<br>10.5<br>TSS<br>7.7<br>7.4<br>7.4<br>7.6<br>7.7<br>TKN<br>4.0<br>4.0<br>4.0<br>20.5<br>4.0<br>Total N<br>12.4<br>12.1<br>12.0<br>25.7<br>14.6<br>COD<br>48.0<br>52.5<br>52.8<br>53.4<br>54.1<br>BOD5<br>4.4<br>4.3<br>4.3<br>4.4<br>4.6<br>Peak concentration [mg/L]<br>Total P<br>4.5<br>7.6<br>4.2<br>6.4<br>4.2<br>N-NH4<br>21.0<br>21.0<br>21.0<br>44.1<br>22.0<br>N-NO3<br>16.4<br>15.3<br>14.9<br>11.7<br>17.0<br>TSS<br>24.5<br>8.6<br>8.6<br>24.2<br>24.4<br>TKN<br>21.9<br>21.9<br>22.0<br>45.4<br>23.0<br>Total N<br>33.3<br>33.1<br>32.9<br>49.0<br>35.6<br>COD<br>69.3<br>63.4<br>63.7<br>86.0<br>87.2<br>BOD5<br>11.3<br>5.3<br>5.4<br>11.2<br>11.8<br>Flow-weighted average. concentration [mg/L]<br>Total P<br>2.0<br>0.8<br>0.63<br>1.0<br>0.5<br>N-NH4<br>3.0<br>2.9<br>2.9<br>19.2<br>3.0<br>N-NO3<br>8.3<br>8.1<br>7.9<br>5.2<br>10.4<br>TSS<br>7.7<br>7.4<br>7.4<br>7.6<br>7.7<br>TKN<br>4.0<br>4.0<br>4.0<br>20.3<br>4.1<br>Total N<br>12.4<br>12.1<br>12.0<br>25.5<br>14.5<br>COD<br>47.9<br>52.1<br>52.4<br>53.0<br>53.6<br>BOD5<br>4.3<br>4.3<br>4.3<br>4.4<br>4.6<br>Annual reduction of the influent [%]<br>COD<br>87.0<br>86.0<br>86.0<br>86.0<br>86.0<br>BOD5<br>97.5<br>97.6<br>97.6<br>97.5<br>97.4<br>Total N<br>76.0<br>76.7<br>77.0<br>50.5<br>72.0<br>Total P<br>43.0<br>77.0<br>82.0<br>70.5<br>86.5||



Note. A/O corresponds to the current anoxic/oxic configuration with chemical precipitation of phosphorus. 

Water Environment Research • 92: 2072–2085, 2020 

2077 

## EDITOR’S CHOICE— RESEARCH ARTICLE 

A[2] /O-S configuration (Figure S6) can be implemented using only one anoxic reactor of the current WRRF to build an anaerobic zone (only in one of the treatment lines). Again, to make this change, new lines and connections to bring the entire internal recycle flow rate after the new anaerobic reactor are required. 

The third proposed configuration is BARDENPHO (Figure S7). It can be implemented not only changing the way of the internal recycle like needed in the previous configurations, but also building new air pipes to convert the last anoxic reactor of each treatment line into aerobic. Besides, part of the air control valves of the first part of the current aerobic zone should be closed to create an anoxic zone (in both treatment lines). 

Finally, different changes should be made to implement UCT configuration (Figure S8). The external recycle should be connected to the current second anoxic reactor of each line. The internal recycle should take mixed liquor from the effluent of the aerobic zone and send it to the last anoxic reactor of each line. Finally, another internal recycle stream should be built to recirculate the effluent from the second current anoxic reactor to the new anaerobic zone. No changes are demanded in the current aerobic zone of the plant. 

In terms of number of changes, UCT demands at least three, while BARDENPHO demands two and both A[2] /O-S and A[2] /O-D only one. This certainly weights in the final choice to determine the best alternative of implementing EBPR in the current WRRF. 

## **Performance of the alternatives** 

Once all the developed alternatives were modeled, simulations were performed using the same input data used also for calibrating the model of the current WRRF (experimental influent data reported in Machado et al. (2014)). The simulated period comprises more than 8 months of daily plant data, and it is characterized by long periods of plant stability. 

The European Community directive for WRRF discharge limits was applied to the simulation data as a first criterion for measuring the effluent quality produced by the different WRRF configurations (Table 2). Table 2 points out a better performance of A[2] /O-D and UCT for TN and TP removal, respectively. The lower anaerobic volume of A[2] /O-S with respect to A[2] /O-D decreases its P-removal capacity. Nevertheless, the greater total anoxic volume of A[2] /O-S in comparison with A[2] /O-D does not improve its denitrification efficiency and A[2] /O-D reaches the lowest averaged TN. Higher anaerobic volume promotes higher yield of fermentation products (SA component in the ASM2d model: VFA, like acetic, propionic and butyric acids), which increases PHA storage by PAO, helping to increase the denitrification rate in subsequent anoxic reactors due to simultaneous denitrification by PAO and ordinary heterotrophs. In the current scenario, BARDENPHO could not reach the best results in any variable. These poor results are due to the reduction of the aerobic zone in comparison with the current A/O configuration and the possible transport of oxygen from the first aerobic zone to the second anoxic zone. UCT presented good performance like A[2] /O-D, especially in P-removal. It probably occurs due to the PAO biomass enrichment that occurs because UCT 

reduces the amount of nitrate entering the anaerobic reactor in comparison with A[2] /O-D. Figure 3 shows the PAO biomass concentration in the first anoxic reactor of the treatment line 1 of both configurations, demonstrating a higher concentration of PAO in UCT than in A[2] /O-D. 

In accordance with the discharge limit parameters stated by the EC directive, both A[2] /O-D and UCT could overcome almost all the constraints. Only the TN maximum concentration (annual average) exceeded 10 mg/L in both cases. Such result implies a possible necessity of adding extra carbon source to promote the required denitrification. 

These performance results are comparable to previous works in the literature. Guerrero et al. (2013) also simulated different EBPR configurations, and comparing the three configurations also tested in the present study, they obtained the best effluent quality for A[2] /O followed by UCT and finally for BARDENPHO. However, they obtained better removal efficiency for Johannesburg and modified-UCT, which were untested configurations in the current study. 

## **Robustness tests** 

The retrofitting project also must consider performing robustness tests to evaluate the best alternative in case of strong external disturbances, like abrupt increase of pollutants load. Different pulses of ammonium and phosphate were simulated, and the effluent quality was registered. Three pulse magnitudes were tested: 2, 5, and 10 times the original P concentration and 1.5, 2, and 3 times for ammonium N. The pulse magnitudes tested are deliberatelymuch higher than the current measurements performed in the WRRF of Manresa nowadays, to better visualize the real potential of each proposed configuration for refusing external disturbances. The pollutant pulse was programmed at Day 130 of the input file. The mass of P was integrated during days 131–215 for the P-pulse and the mass of N during the days 131–150 in the case of the ammonium pulse (Figure 4). An 

**==> picture [228 x 206] intentionally omitted <==**

**Figure 3.** PAO biomass in the first anoxic reactor of the treatment line 1 of both UCT and A[2] /O-D configurations during the simulations using the original Manresa WRRF influent data. 

_Machado et al._ 

2078 

EDITOR’S CHOICE— RESEARCH ARTICLE 

**==> picture [483 x 198] intentionally omitted <==**

**Figure 4.** Pulse simulations with extra addition of phosphate and ammonium. Mass of TP (a) and TN (b) released in the effluent stream versus pulse magnitude in the influent for each WRRF configuration. 

example of the profiles for P in the influent and the effluent for all the proposed plant configurations, which were obtained for the higher P increase, is shown in Figure 5. The current plant configuration (A/O) and the A[2] /O-S configuration presented the poorest results. They could not refuse the external P disturbance in the same extent as UCT and BARDENPHO, while A[2] /O-D had an intermediate performance. 

Regarding the experiment with ammonium pulses, the best results for refusing external disturbances were achieved by A[2] /O-D, followed by A[2] /O-S. These results (Figure 4b) were slightly better than the current Manresa plant configuration. BARDENPHO configuration resulted in the poorest performance for refusing ammonium pulses, due to the reduction of the aerobic zone. 

**==> picture [487 x 294] intentionally omitted <==**

**Figure 5.** Total P concentration in the effluent for all the proposed retrofitted configurations and the influent profiles of total P concentration (original and modified profile) during the pulse simulations of 10 times the original profile of total P inlet concentration. 

Water Environment Research • 92: 2072–2085, 2020 

2079 

## EDITOR’S CHOICE— RESEARCH ARTICLE 

The sensitivity of the effluent quality to the addition of extra carbon source was also evaluated, simulating all the proposed alternatives. The extra amount of COD added as SA was calculated as a percentage of the COD in the influent of the full-scale WRRF, testing values of 1%, 5%, 10%, 20%, and 50%. Figure 6 shows important parameters of the EC directive calculated with the results of the simulations of the proposed plant configuration and the current plant model. In advance, there was no exceeding in COD and BOD5 variables in any of the plant configurations even though extra biodegradable COD was added to the systems. 

In the case of P removal (Figure 6a), the effect of increasing SA helped A[2] /O-S and BARDENPHO to reach the defined minimum annual reduction determined by the EC directive (80%). UCT and A[2] /O-D were already able to reach the EC directive without adding extra carbon source. With some extra carbon 

source, also the current plant configuration is able to reach the minimum P removal, although N removal is not accomplished. 

Regarding nitrogen removal (Figure 6b), the current plant configuration, and both A[2] /O alternatives presented the best results. Nevertheless, an asymptotic behavior was shown as higher amounts of COD as SA was added. Such an effect suggests that the denitrification was not affected by the lack of extra biodegradable COD, but by the own construction way the plant configuration schemes were built, that permits a considerable amount of nitrate (ammonium nitrified in the aerobic zone) to be released from the end of the aerobic zone to the secondary settler without a new process step. Such problem would be attenuated increasing the internal recycle flow rate, but pump limits of the WRRF and the increase of energy consumption would make a high increase prohibitive (Baeza, Gabriel, & Lafuente, 2004). A possible solution for nitrate recycle is 

**==> picture [483 x 415] intentionally omitted <==**

**Figure 6.** Results for simulations with extra carbon source addition as SA for each WRRF configuration. (a) Total P reduction, (b) Total N reduction, (c) Maximum Total P concentration, (d) Maximum Total N concentration. 

_Machado et al._ 

2080 

## EDITOR’S CHOICE— RESEARCH ARTICLE 

presented by the BARDENPHO philosophy, but poor results were obtained when it was applied into the studied scenario. 

Figure 6c presents the behavior of the maximum total P concentration in the effluent after the experiments of adding extra carbon source to all the plant configurations. No limit was exceeded by any of the plants. Nevertheless, BARDENPHO presented the poorest results. 

Finally, from the proposed retrofitting alternatives, A[2] /O-S, A[2] /O-D and the current plant almost produced a maximum TN concentration (Figure 6d) below the legal limit but only when 50% of the original inlet COD was added as SA, a fact that would considerably increase the operating costs. Again, the present limitations after adding this extra COD rely on the fact that the configurations tested do not allow complete nitrate removal. 

## **Economic comparison** 

The systematic comparison among all the proposed alternatives for WRRF retrofitting includes the cost evaluation, both OPEX and CAPEX. Table 3 presents the involved costs for aeration, pumping, treatment of sludge, effluent quality fines, operating costs, acquisition of new equipment, building of new pipes and tanks, and the cost of the design (US-EPA, 2000). These data show a clear advantage of the two A[2] /O proposed alternatives considering both kinds of costs. With few modifications, which imply less capital costs, A[2] /O-D is able to improve the effluent quality compared to the current plant. It is worth noticing that Table 3 data relate to the WRRF without effluent controllers. Once the best configuration is defined, the operation costs and effluent quality can be improved by selecting the best control structure, tuning of process controllers, and setpoint optimization (Guerrero, Guisasola, Comas, Rodríguez-Roda, & Baeza, 2012; Guerrero, Guisasola, Vilanova, & Baeza, 2011; Machado, Gabriel, et al., 2009; Machado et al., 2015; Ostace et al., 2013). In fact, only by optimizing the operational point 

by selecting the best DO setpoints and internal and external recycling flow rates, the WRRF performance can be highly improved (Ostace et al., 2013). 

## **Multicriteria comparison and single performance index** 

Table 4 presents a relative ranking of all the proposed alternatives considering all the criteria pointed out along the retrofitting proposed methodology: main pollutant concentrations, performance in observing the EC directive, performance obtained in the robustness tests, and the main operating and capital costs. The absolute values obtained were rated according to the procedure described in Section 2.4.4 following the ranges and qualifications of Table S3. The final ratings for 13 categories of Table 4 are presented in Figure 7: capital and operating costs, number of changes, reduction % for COD, BOD5, TN and TP, maximum concentration for COD, BOD5, TN and TP, and mass of N and P in the effluent during the robustness tests. The multicriteria radar plot shows that the A[2] /O-D configuration has the closest shape to a circle, with the best scores on most of the criteria evaluated. A[2] /O-S is only better in the capital costs category, while it is worst in several categories, most significantly in the robustness tests and the ability to remove P. UCT is the other configuration with good performance in most criteria and is the only one with higher capacity than A[2] /O-D to remove P. BARDENPHO is shown again as the worst alternative in most criteria for retrofitting the WRRF of Manresa with the limitations imposed. As observed, the multicriteria comparison enables a more extensive evaluation of different alternatives where none of the criterion is conditional to the other (Guerrero et al., 2012). 

For building a single performance index, the different criteria could be added. Following this logic, the 

**Table 3.** Capital and operational costs of all the proposed alternatives 

|**Table 3.**Capital and operational|co|sts of all the proposed alternatives|
|---|---|---|
|OPERATIONAL COSTS<br>[€/D]||CONFIGURATIONS<br>A/O (CURRENT)<br>A2/O-S<br>A2/O-D<br>BARDENPHO<br>UCT|
|Aeration costs [€/d]<br>Pumping costs [€/d]<br>Sludge treatment costs [€/d]<br>Effluent quality costs [€/d]<br>Total operating costs without<br>effluent quality costs [€/d]<br>Total operating costs with ef-<br>fluentqualitycosts [€/d]||497<br>500<br>495<br>741<br>502<br>521<br>521<br>521<br>1,821<br>822<br>312<br>312<br>312<br>309<br>312<br>1,407<br>1,404<br>1,353<br>9,850<br>1,536<br>1,330<br>1,333<br>1,328<br>2,871<br>1,636<br>2,737<br>2,737<br>2,681<br>12,721<br>3,172|
||||
|CAPITAL COSTS [€]|CONFIGURATIONS<br>A/O (CURRENT)<br>A2/O-S<br>A2/O-D<br>BARDENPHO<br>UCT||
|New equipment (sensors,<br>pumps)<br>Air piping<br>WW piping<br>Project and documentation<br>Total capital cost [€]|-<br>100,000<br>100,000<br>100,000<br>138,564<br>-<br>-<br>-<br>29,940<br>-<br>-<br>42,031<br>54,640<br>54,640<br>120,740<br>-<br>10,000<br>10,000<br>10,000<br>10,000<br>-<br>152,031<br>164,640<br>194,580<br>269,394||



Water Environment Research • 92: 2072–2085, 2020 

2081 

## EDITOR’S CHOICE— RESEARCH ARTICLE 

**Table 4.** Relative performance of all the proposed alternatives considering the criteria evaluated, including the single performance index 

|**Table 4.**Relative performance of all the propos|ed alternatives considering the criteria evaluated|, including the single performance index|
|---|---|---|
|CRITERION DESCRIPTION<br>TAG|PHYSICAL VALUE OF THE<br>CRITERION<br>A2/O-S<br>A2/O-D<br>BARD<br>UCT|NORMALIZED CRITERION (0–10)<br>A2/O-S<br>A2/O-D<br>BARD<br>UCT|
|Costs [m€]<br>CAPEX<br>1<br>152.0<br>164.6<br>194.6<br>269.4<br>OPEX<br>2<br>2.74<br>2.68<br>12.72<br>3.17<br>Number of changes<br>3<br>1<br>1<br>3<br>5<br>Reduction [%]<br>COD<br>4<br>86.2<br>86.1<br>85.9<br>85.8<br>BOD5<br>5<br>97.6<br>97.6<br>97.5<br>97.4<br>Total N<br>6<br>76.7<br>77.0<br>50.5<br>72.0<br>Total P<br>7<br>77.1<br>82.3<br>70.5<br>86.5<br>Maximum effluent concentration [mg/L]<br>COD<br>8<br>63.4<br>63.8<br>86.0<br>87.3<br>BOD5<br>9<br>5.3<br>5.4<br>11.3<br>11.8<br>Total N<br>10<br>33.1<br>32.9<br>49.0<br>35.6<br>Total P<br>11<br>7.7<br>4.2<br>6.4<br>4.2<br>Robustness tests. Mass of P in the effluent [kg]<br>2× pulse<br>1,200<br>1,080<br>1,010<br>800<br>5× pulse<br>1,600<br>1,400<br>1,280<br>1,180<br>10× pulse<br>2,700<br>2,300<br>1,950<br>1,850<br>Average P<br>12<br>1,833<br>1,593<br>1,413<br>1,277<br>Robustness tests. Mass of N in the effluent [kg]<br>1.5× pulse<br>7,000<br>6,950<br>15,050<br>7,500<br>2× pulse<br>9,020<br>8,980<br>17,000<br>10,050<br>3× pulse<br>13,800<br>13,700<br>22,300<br>15,020<br>Average N<br>13<br>9,940<br>9,877<br>18,117<br>10,857<br>Total rating<br>Total rating normalized from 0<br>to 10 (Total rating divided by<br>the number of weights)||9.86<br>9.02<br>7.03<br>2.04<br>9.43<br>9.48<br>1.75<br>9.10<br>10.00<br>10.0<br>5.0<br>0.00<br>6.55<br>6.53<br>6.48<br>6.45<br>9.40<br>9.40<br>9.38<br>9.35<br>6.12<br>6.17<br>1.75<br>5.33<br>4.28<br>5.58<br>2.63<br>6.63<br>7.47<br>7.45<br>6.56<br>6.51<br>8.93<br>8.93<br>7.75<br>7.64<br>4.82<br>4.88<br>0.30<br>4.11<br>2.94<br>7.25<br>4.51<br>7.25<br>5.00<br>6.50<br>7.38<br>10.00<br>5.00<br>7.38<br>8.81<br>10.00<br>5.00<br>7.35<br>9.41<br>10.00<br>5.00<br>7.08<br>8.53<br>10.00<br>9.97<br>10.00<br>5.00<br>9.66<br>9.98<br>10.00<br>5.00<br>9.33<br>9.94<br>10.00<br>5.00<br>9.23<br>9.96<br>10.00<br>5.00<br>9.41<br>94.8<br>101.8<br>66.7<br>83.8<br>7.3<br>7.8<br>5.1<br>6.5|



highest summation considering all the criteria is the best result among all the proposed alternatives. Table 4 shows this final rating normalized from 0 to 10: A[2] /O-D shows the best rating of 7.8/10, followed by A[2] /O-S with 7.3/10. Both are the best configurations for retrofitting the WRRF of Manresa including EBPR according to this single performance criterion. However, A[2] /O-D is the most prepared plant configuration to keep acceptable nitrogen removal levels without needing strong modifications. UCT also provides very good removal efficiency for P and lower for N, but need more modifications than A[2] /O-D, a factor that strongly penalizes this configuration. 

A sensitivity analysis was also performed to ensure a robust decision (Table S4). The equal weight used in the previous calculation was modified with three additional sets with twice the weight in (a) P and N removal performance, (b) costs and number of changes, and (c) robustness tests. In all the cases, the order of best configuration was A[2] /O-D > A[2] / O-S > UCT > BARDENPHO, indicating a stable and robust selection of the best alternatives. 

Therefore, our systematic analysis was validated as a reliable decision support methodology for selecting the best 

retrofitting alternative among different possible configurations, providing a clear procedure for such a selection. Its application to the Manresa WRRF to perform EBPR led to selecting an A[2] /O-D configuration using two of the six available anoxic reactors as anaerobic reactors. Such a configuration produces an effluent stream with a total P concentration about 69% lower than the total P effluent concentration of the current configuration, which represents a total P-reduction of 82.3% with the A[2] /O-D configuration. It also presented a good cost-to-profit ratio (relative low investment cost to the effluent quality obtained). 

## **Comparison to previous works and limitations of the proposed methodology** 

The framework developed for the selection of alternatives developed in this work can be compared with previous developments reported in the literature. Some previous works focused on a basic comparison of a wide number of configurations. The work of Bozkurt et al. (2016) addressed the support of process engineers in the early-stage screening of WRRF design and retrofitting, considering the increasing number of treatment technologies available. Hence, more than 200 retrofitting 

_Machado et al._ 

2082 

EDITOR’S CHOICE— RESEARCH ARTICLE 

**==> picture [483 x 235] intentionally omitted <==**

**Figure 7.** Graphical comparison of the proposed plant configurations and the set of criteria used for ranking the tested alternatives. 

alternatives were considered in the developed superstructure optimization framework using static models. Castillo, Porro, et al. (2016) also evaluated different alternatives for the retrofitting of a WRRF using technical, environmental, economic, and social assessment in a decision support system. The outcome was a reliable basis to support decision makers on the bases of a total score with the contribution of different criterion using selected weights based on the specific need of each study and on expert criteria. It was oriented to the selection of different alternatives in a range of more than 150 technologies; consequently, the evaluation was also based on static models and a set of characteristics of each technology. In contrast, our proposal focuses only on the retrofitting of the water line of a WRRF to include EBPR, using dynamic models to evaluate the performance under variable influent and its robustness against disturbances. 

In a subsequent work (Castillo, Cheali, et al., 2016), the development of a superstructure-based optimization was reported. An uncertainty analysis was performed to increase the quality and robustness of the decision by considering the variation in influent composition. 

Fernández-Arévalo et al. (2017) used a plantwide modeling methodology to evaluate three plants layout for a theoretical scenario, analyzing the options for organic matter and nutrient recovery, mass and energy distribution, and cost analysis. The model used was also dynamic, but did not focus on EBPR implementation, and the three criteria studied were considered independently, without the aim of defining any combined performance index as presented in our work. 

It is worth noting that, as in any modeling work, the results depend on the assumptions made during the modeling and simulation exercise. In our study, we assume that the 

model calibration performed in a previous work (Machado et al., 2014) is still valid because the influent and environmental conditions have not changed significantly since that calibration. Furthermore, as in all works studying configuration alternatives, it is assumed that the model is capable of describing all configurations using the same set of model parameters, without any specific calibration for each configuration, since they do not yet exist and a specific calibration is not possible. Techniques as defining probability density functions for the inputs and parameters assumed to be uncertain and propagate that uncertainty in the simulations have been proposed to incorporate this possible variability in the modeling exercise (Benedetti et al., 2008, 2013). 

Additionally, our study aimed to find the WRRF retrofitting with the minimum number of configuration changes, in order to minimize costs. Therefore, the available volumes were redistributed in anaerobic, anoxic, and aerobic reactors, but keeping the same total volume of the plant. This produced additional restrictions that would not be required in a fully new design. This limitation may have particularly affected some configurations such as BARDENPHO, which shows in our study the worst performance of the alternatives tested, probably due to a lack of aerobic volume. Additional minor modifications, such as internal baffling of reactors, could also help to create zones of the reactor with the specific operational conditions required, but such modifications were not considered in this study. 

Another possible limitation of the approach could be the lack of an optimized control structure implemented in each one of the proposed configurations. In case of a lack of capacity of the system, we may also consider intensification options to offset the lack of aerobic volume or operate with less safety factor through greater control and automation or process 

Water Environment Research • 92: 2072–2085, 2020 

2083 

EDITOR’S CHOICE— RESEARCH ARTICLE 

optimization. In our study, each one of the configurations can be improved by selecting a proper control structure (Machado, Gabriel, et al., 2009; Machado et al., 2015; Ostace et al., 2013; Stare et al., 2007) and then tuning the controllers and optimizing the setpoints of the control loops (Guerrero et al., 2011, 2012; Rojas, Baeza, & Vilanova, 2011). However, this type of analysis is usually time-consuming and is only applicable to a reduced set of configurations that have been preselected using a more general methodology such as that presented in this manuscript. Therefore, when comparing the efficiency of configurations, it is recommended to take into account that each of them could improve its performance with a well-designed and optimized control structure. In any case, a control system would require less effort in a configuration that naturally better rejects load disturbances. 

## **Conclusions** 

The developed work shows a methodology based on a multicriteria approach to select the best alternative for retrofitting a WRRF. 

- Up to 13 criteria related to effluent quality, robustness under disturbances, operating costs, and implementation costs are studied for four different WRRF configurations including EBPR (A[2] /O-S, A[2] /O-D, BARDENPHO and UCT). 

- The results with the multicriteria approach are compared to the development of a single function based on the combination of all the criteria. Its relevance is corroborated by a sensitivity analysis demonstrating the robustness of the selection of the best alternative. 

- The systematic selection process of a retrofitting alternative with simultaneous removal of COD, N, and P for the current A/O facility selects an A[2] /O configuration with two anaerobic reactors that are two of the six anoxic reactors already existing in the current plant (A[2] /O-D). 

- The proposed alternative decreases 69% P effluent concentration of the current configuration, which represents a total P-reduction of 82.3% (i.e. a mass of 4.5 tons per year not released to the Cardener River). It is also 15% more stable than the existing plant in the case of presence of P disturbances in the influent. 

## **Acknowledgments** 

The authors greatly acknowledge Ricard Tomas and Ana Lupón (Aigües de Manresa S.A.) for all the support provided in conducting this work. Vinicius Cunha Machado received a Pre-doctoral scholarship (2008FIR 00012) of the AGAUR (Agència de Gestió d’Ajuts Universitaris i Recerca - Catalonia, Spain), inside programs of the European Community Social Fund. This work was initially supported by the Spanish Ministerio de Economía y Competitividad (CTQ2014-60495-R) with funds from the Fondo Europeo de Desarrollo Regional (FEDER). The authors are members of 

the GENOCOV research group (Grup de Recerca Consolidat de la Generalitat de Catalunya, 2017 SGR 1175, www.genoc ov.com). 

## **Conflict of interest** 

The authors have no conflict of interest to declare. 

## **Data availability statement** 

Data available on request from the authors. 

## **References** 

Ardern, E., & Lockett, W. T. (1914). Experiments on the oxidation of sewage without the aid of filters. _Journal of the Society of Chemical Industry_ , _33_ (10), 523–539. https://doi. org/10.1002/jctb.50003 31005 

- Baeza, J. A., Gabriel, D., & Lafuente, F. J. (2004). Effect of internal recycle on the nitrogen removal efficiency of an anaerobic/anoxic/oxic (A[2] /O) wastewater treatment plant (WWTP). _Process Biochemistry_ , _39_ (11), 1615–1624. https://doi.org/10.1016/S0032 -9592(03)00300 -5 

Barnard, J. L., Dunlap, P., & Steichen, M. (2017). Rethinking the mechanisms of biological phosphorus removal. _Water Environment Research_ , _89_ (11), 2043–2054. https://doi. org/10.2175/10614 3017X 15051 46591 9010 

- Benedetti, L., Belia, E., Cierkens, K., Flameling, T., De Baets, B., Nopens, I., & Weijers, S. (2013). The incorporation of variability and uncertainty evaluations in WWTP design by means of stochastic dynamic modeling: The case of the Eindhoven WWTP upgrade. _Water Science and Technology_ , _67_ (8), 1841–1850. https://doi.org/10.2166/ wst.2013.064 

- Benedetti, L., Bixio, D., Claeys, F., & Vanrolleghem, P. A. (2008). Tools to support a model-based methodology for emission/immission and benefit/cost/risk analysis of wastewater systems that considers uncertainty. _Environmental Modelling & Software_ , _23_ (8), 1082–1091. https://doi.org/10.1016/j.envso ft.2008.01.001 

- Bozkurt, H., van Loosdrecht, M. C. M., Gernaey, K. V., & Sin, G. (2016). Optimal WWTP process selection for treatment of domestic wastewater – A realistic full-scale retrofitting study. _Chemical Engineering Journal_ , _286_ , 447–458. https://doi.org/10.1016/j. cej.2015.10.088 

- Castillo, A., Cheali, P., Gómez, V., Comas, J., Poch, M., & Sin, G. (2016). An integrated knowledge-based and optimization tool for the sustainable selection of wastewater treatment process concepts. _Environmental Modelling & Software_ , _84_ , 177–192. https://doi.org/10.1016/j.envso ft.2016.06.019 

- Castillo, A., Porro, J., Garrido-Baserba, M., Rosso, D., Renzi, D., Fatone, F., … Poch, M. (2016). Validation of a decision support tool for wastewater treatment selection. _Journal of Environmental Management_ , _184_ , 409–418. https://doi.org/10.1016/j. jenvm an.2016.09.087 

- Copp, J. B., Spanjers, H., & Vanrolleghem, P. A. (2002). _Respirometry in control of the activated sludge process: Benchmarking control strategies. Scientific and technical report no. 11_ . UK: IWA Publishing. 

- EEC Council (1991). Council Directive of 21 May 1991 concerning urban waste water treatment (91/271/EEC). _Official Journal of the European Communities_ . _L135_ , 40–52. https://eur-lex.europa.eu/legal -conte nt/EN/ALL/?uri=CELEX :31991 L0271. 

- European Commission (2018). _Public consultation on the evaluation of the urban waste water treatment directive_ . Retrieved from https://ec.europa.eu/info/consu ltati ons/ publi c-consu ltati on-evalu ation -urban -waste -water -treat ment-direc tive_en 

- Fernández-Arévalo, T., Lizarralde, I., Fdz-Polanco, F., Pérez-Elvira, S. I., Garrido, J. M., Puig, S., … Ayesa, E. (2017). Quantitative assessment of energy and resource recovery in wastewater treatment plants based on plant-wide simulations. _Water Research_ , _118_ , 272–288. https://doi.org/10.1016/j.watres.2017.04.001 

- Gernaey, K. V., Jeppsson, U., Vanrolleghem, P. A., & Copp, J. B. (2014). _Benchmarking of control strategies for wastewater treatment plants_ , London, UK: IWA Publishing. https://doi.org/10.2166/97817 80401171 

- Gernaey, K. V., & Jørgensen, S. B. (2004). Benchmarking combined biological phosphorus and nitrogen removal wastewater treatment processes. _Control Engineering Practice_ , _12_ (3), 357–373. https://doi.org/10.1016/S0967 -0661(03)00080 -7 

- Guerrero, J., Flores-Alsina, X., Guisasola, A., Baeza, J. A., & Gernaey, K. V. (2013). Effect of nitrite, limited reactive settler and plant design configuration on the predicted performance of simultaneous C/N/P removal WWTPs. _Bioresource Technology_ , _136_ , 680–688. https://doi.org/10.1016/j.biort ech.2013.03.021 

- Guerrero, J., Guisasola, A., Comas, J., Rodríguez-Roda, I., & Baeza, J. A. (2012). Multicriteria selection of optimum WWTP control setpoints based on microbiology-related failures, effluent quality and operating costs. _Chemical Engineering Journal_ , _188_ , 23–29. https://doi.org/10.1016/j.cej.2012.01.115 

- Guerrero, J., Guisasola, A., Vilanova, R., & Baeza, J. A. (2011). Improving the performance of a WWTP control system by model-based setpoint optimisation. _Environmental Modelling & Software_ , _26_ (4), 492–497. https://doi.org/10.1016/j. envso ft.2010.10.012 

_Machado et al._ 

2084 

## EDITOR’S CHOICE— RESEARCH ARTICLE 

- Henze, M., Gujer, W., Mino, T., & van Loosdrecht, M. C. M. (2000). _Activated sludge models ASM1, ASM2, ASM2d and ASM3: Scientific and technical report no. 9_ , London, UK: IWA Publishing. 

- Jardin, N., Rath, L., Sabin, A., Schmitt, F., Thöle, D., & Kühn, S. (2000). Cost-effective upgrading of the Arnsberg WWTP by post denitrification with a moving bed system. _Water Science and Technology_ , _41_ (9), 123–130. https://doi.org/10.2166/ wst.2000.0186 

- Kassouf, H., García Parra, A., Mulford, L., Iranipour, G., Ergas, S. J., & Cunningham, J. A. (2019). Mass fluxes of nitrogen and phosphorus through water reclamation facilities: Case study of biological nutrient removal, aerobic sludge digestion, and sidestream recycle. _Water Environment Research_ , _92_ (3), 478–489. https://doi.org/10.1002/ wer.1239 

- Machado, V. C., Gabriel, D., Lafuente, J., & Baeza, J. A. (2009). Cost and effluent quality controllers design based on the relative gain array for a nutrient removal WWTP. _Water Research_ , _43_ (20), 5129–5141. https://doi.org/10.1016/j. watres.2009.08.011 

- Machado, V. C., Lafuente, J., & Baeza, J. A. (2014). Activated sludge model 2d calibration with full-scale WWTP data: Comparing model parameter identifiability with influent and operational uncertainty. _Bioprocess and Biosystems Engineering_ , _37_ (7), 1271–1287. https://doi.org/10.1007/s0044 9-013-1099-8 

- Machado, V. C., Lafuente, J., & Baeza, J. A. (2015). Model-based control structure design of a full-scale WWTP under the retrofitting process. _Water Science and Technology_ , _71_ (11), 1661–1671. https://doi.org/10.2166/wst.2015.140 

- Machado, V. C., Tapia, G., Gabriel, D., Lafuente, J., & Baeza, J. A. (2009). Systematic identifiability study based on the Fisher Information Matrix for reducing the number of parameters calibration of an activated sludge model. _Environmental Modelling & Software_ , _24_ (11), 1274–1284. https://doi.org/10.1016/j.envso ft.2009.05.001 

- Onnis-Hayden, A., Srinivasan, V., Tooker, N. B., Li, G., Wang, D., Barnard, J. L., … Gu, A. Z. (2020). Survey of full-scale sidestream enhanced biological phosphorus removal (S2EBPR) systems and comparison with conventional EBPRs in North America: Process stability, kinetics, and microbial populations. _Water Environment Research_ , _92_ (3), 403–417. https://doi.org/10.1002/wer.1198 

- Orhon, D., & Artan, N. (1994). _Modelling of activated sludge systems_ , Lancaster, PA: Technomic Publishing Company. 

control strategies for optimal simultaneous removal of carbon, nitrogen and phosphorus. _Computers & Chemical Engineering_ , _53_ , 164–177. https://doi.org/10.1016/j. compc hemeng.2013.03.007 

   - Rojas, J. D., Baeza, J. A., & Vilanova, R. (2011). Effect of the controller tuning on the performance of the BSM1 using a data driven approach. In _Watermatex 2011. 8th IWA symposium on systems analysis and integrated assessment, 2009_ (pp. 785–792). 

   - Schuler, A. J., & Jang, H. (2007). Causes of variable biomass density and its effects on settleability in full-scale biological wastewater treatment systems. _Environmental Science & Technology_ , _41_ (5), 1675–1681. https://doi.org/10.1021/es061 6074 

   - Stare, A., Vrečko, D., Hvala, N., & Strmčnik, S. (2007). Comparison of control strategies for nitrogen removal in an activated sludge process in terms of operating costs: A simulation study. _Water Research_ , _41_ (9), 2004–2014. https://doi.org/10.1016/j. watres.2007.01.029 

   - Steffens, M. A., & Lant, P. A. (1999). Multivariable control of nutrient-removing activated sludge systems. _Water Research_ , _33_ (12), 2864–2878. https://doi.org/10.1016/S0043 -1354(98)00521 -1 

   - Takács, I., Patry, G. G., & Nolasco, D. (1991). A dynamic model of the clarification-thickening process. _Water Research_ , _25_ (10), 1263–1271. https://doi.org/10.1016/00431354(91)90066 -Y 

   - Tchobanoglous, G., Burton, F. L., & Stensel, H. D. (2013). _Wastewater Engineering: Treatment and Reuse_ (4th ed.). New York: Metcalf & Eddy, Inc., McGraw-Hill. 

   - US-EPA (2000). In S. Hopkins (Ed.), _Development document for final effluent limitations guideline and standards for commercial hazardous waste combustors_ . EPA Number: 821R99020. 

   - van Loosdrecht, M. C. M., Brandse, F. A., & de Vries, A. C. (1998). Upgrading of waste water treatment processes for integrated nutrient removal-the BCFS® process. _Water Science and Technology_ , _37_ (9), 209–217. https://doi.org/10.2166/wst.1998.0359 

   - Vanrolleghem, P. A., & Gillot, S. (2002). Robustness and economic measures as control benchmark performance criteria. _Water Science and Technology_ , _45_ (4–5), 117–126. https://doi.org/10.2166/wst.2002.0565 

   - Yang, Y., Shi, X., Ballent, W., & Mayer, B. K. (2017). Biological phosphorus recovery: Review of current progress and future needs. _Water Environment Research_ , _89_ (12), 2122–2135. https://doi.org/10.2175/10614 3017x 15054 98892 6424 

- Ostace, G. S., Baeza, J. A., Guerrero, J., Guisasola, A., Cristea, V. M., Agachi, P. Ş., & Lafuente, F. J. (2013). Development and economic assessment of different WWTP 

Water Environment Research • 92: 2072–2085, 2020 

2085 

