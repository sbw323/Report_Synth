Methods · REopt.jl Documentation 

4/16/26, 10:32 AM 

 REopt / Methods 

 GitHub  ⚙  

## **Methods** 

The primary method for using REopt is the `run_reopt` method. In the simplest there are two required inputs to `run_reopt` : a `JuMP.Model` with an op!mizer and the path to a JSON file to define the `Scenario` . Other methods for `run_reopt` are enumerated below. Other methods such as `build_reopt!` are also described to allow users to build custom REopt models. For example, a"er using `build_reopt!` a user could add constraints or change the objec!ve func!on using `JuMP` commands. 

## **run_reopt** 

 `REopt.run_reopt` — Func!on `run_reopt(m::JuMP.AbstractModel, fp::String)`  Solve the model using the `Scenario` defined in JSON file stored at the file path `fp` . `run_reopt(m::JuMP.AbstractModel, d::Dict)`  Solve the model using the `Scenario` defined in dict `d` . `run_reopt(m::JuMP.AbstractModel, s::AbstractScenario)`  Solve the model using a `Scenario` or `BAUScenario` . `run_reopt(t::Tuple{JuMP.AbstractModel, AbstractScenario})`  Method for use with Threads when running BAU in parallel with op!mal scenario. `run_reopt(ms::AbstractArray{T, 1}, fp::String)` **`where`** `T <: JuMP.AbstractModel`  

https://natlabrockies.github.io/REopt.jl/dev/reopt/methods/ 

Page 1 of 6 

Methods · REopt.jl Documentation 

4/16/26, 10:32 AM 

Solve the `Scenario` and `BAUScenario` in parallel using the first two (empty) models in `ms` and inputs defined in the JSON file at the filepath `fp` . 

`run_reopt(ms::AbstractArray{T, 1}, d::Dict)` **`where`** `T <: JuMP.AbstractModel`  

Solve the `Scenario` and `BAUScenario` in parallel using the first two (empty) models in `ms` and inputs from `d` . 

`run_reopt(ms::AbstractArray{T, 1}, p::REoptInputs)` **`where`** `T <: JuMP.AbstractModel`  

Solve the `Scenario` and `BAUScenario` in parallel using the first two (empty) models in `ms` and inputs from `p` . 

## **build_reopt!** 

 `REopt.build_reopt!` — Func!on 

`build_reopt!(m::JuMP.AbstractModel, fp::String)`  Add variables and constraints for REopt model. `fp` is used to load in JSON file to construct REoptInputs. `build_reopt!(m::JuMP.AbstractModel, p::REoptInputs)`  

Add variables and constraints for REopt model. 

## **simulate_outages** 

 `REopt.simulate_outages` — Func!on 

https://natlabrockies.github.io/REopt.jl/dev/reopt/methods/ 

Page 2 of 6 

Methods · REopt.jl Documentation 

4/16/26, 10:32 AM 

`simulate_outages(;batt_kwh=0, batt_kw=0, pv_kw_ac_hourly=[], init_soc=[], critica`  `wind_kw_ac_hourly=[], batt_roundtrip_efficiency=0.829, diesel_kw=0, fuel_avai diesel_min_turndown=0.3` 

```
)
```

Time series simula!on of outages star!ng at every !me step of the year. Used to calculate how many !me steps the cri!cal load can be met in every outage, which in turn is used to determine probabili!es of mee!ng the cri!cal load. 

## **Arguments** 

- `batt_kwh` 

- `batt_kw` 

- `pv_kw_ac_hourly` 

- `init_soc` 

- `critical_loads_kw` 

- `wind_kw_ac_hourly` 

- `batt_roundtrip_efficiency` 

- `diesel_kw` 

- `fuel_available` 

- `b` _x + b_ rated_capacity) [gal/kwh/kw] 

- `m` _x + b_ rated_capacity) [gal/kWh] 

- `diesel_min_turndown` : minimum generator turndown in frac!on of generator capacity (0 to 

- 1) 

## Returns a dict 

`"resilience_by_time_step": vector of time steps that critical load is met for`  `"resilience_hours_min": minimum of "resilience_by_time_step",` 

- `"resilience_hours_max": maximum of "resilience_by_time_step",` 

- `"resilience_hours_avg": average of "resilience_by_time_step",` 

- `"outage_durations": vector of integers for outage durations with non zero pro "probs_of_surviving": vector of probabilities corresponding to the "outage_du "probs_of_surviving_by_month": vector of probabilities calculated on a monthl "probs_of_surviving_by_hour_of_the_day":vector of probabilities calculated on` 

https://natlabrockies.github.io/REopt.jl/dev/reopt/methods/ 

Page 3 of 6 

Methods · REopt.jl Documentation 

4/16/26, 10:32 AM 

```
}
```

`simulate_outages(d::Dict, p::REoptInputs; microgrid_only::Bool=false)`  

Time series simula!on of outages star!ng at every !me step of the year. Used to calculate how many !me steps the cri!cal load can be met in every outage, which in turn is used to determine probabili!es of mee!ng the cri!cal load. 

## **Arguments** 

`d` ::Dict from `reopt_results` 

- `p` ::REoptInputs the inputs that generated the Dict from `reopt_results` 

- `microgrid_only` ::Bool whether or not to simulate only the op!mal microgrid capaci!es or the total capaci!es. This input is only relevant when modeling mul!ple outages. 

## Returns a dict 

```
{
```

 

```
"resilience_by_time_step": vector of time steps that critical load is met for
"resilience_hours_min": minimum of "resilience_by_time_step",
"resilience_hours_max": maximum of "resilience_by_time_step",
```

```
"resilience_hours_avg": average of "resilience_by_time_step",
```

```
"outage_durations": vector of integers for outage durations with non zero pro
"probs_of_surviving": vector of probabilities corresponding to the "outage_du
"probs_of_surviving_by_month": vector of probabilities calculated on a monthl
"probs_of_surviving_by_hour_of_the_day":vector of probabilities calculated on
}
```

## **backup_reliability** 

- `REopt.backup_reliability` — Func!on 

```
backup_reliability(d::Dict, p::REoptInputs, r::Dict)
```

 

## Return dic!onary of backup reliability results. 

https://natlabrockies.github.io/REopt.jl/dev/reopt/methods/ 

Page 4 of 6 

Methods · REopt.jl Documentation 

4/16/26, 10:32 AM 

## **Arguments** 

- `d::Dict` : REopt results dic!onary. Subhourly !me steps are not yet supported. 

- `p::REoptInputs` : REopt Inputs Struct. 

- `r::Dict` : Dic!onary of inputs for reliability calcula!ons. If r not included then uses all defaults. 

Possible keys in r: -generator _opera!onal_ availability::Real = 0.995 Frac!on of year generators not down for maintenance -generator _failure_ to _start::Real = 0.0094 Chance of generator star!ng given outage -generator_ mean _!me_ to _failure::Real = 1100 Average number of !me steps between a generator's failures. 1/(failure to run probability). -num_ generators::Int = 1 Number of generators. - 

generator _size_ kw::Real = 0.0 Backup generator capacity. -num _ba"ery_ bins::Int = depends on ba#ery sizing Number of bins for discretely modeling ba#ery state of charge - 

ba#ery _opera!onal_ availability::Real = 0.97 Likelihood ba#ery will be available at start of outage - pv _opera!onal_ availability::Real = 0.98 Likelihood PV will be available at start of outage - wind _opera!onal_ availability::Real = 0.97 Likelihood Wind will be available at start of outage - max _outage_ dura!on::Int = 96 Maximum outage dura!on modeled -microgrid_only::Bool = false Determines how generator, PV, and ba#ery act during islanded mode 

```
backup_reliability(r::Dict)
```

 

## Return dic!onary of backup reliability results. 

## **Arguments** 

- `r::Dict` : Dic!onary of inputs for reliability calcula!ons. If r not included then uses all defaults. 

Possible keys in r: -cri!cal _loads_ kw::Array Cri!cal loads per !me step. Must be hourly and have length of 8760. (Required input) -microgrid _only::Bool Boolean to check if only microgrid runs during grid outage (defaults to false) -chp_ size _kw::Real CHP capacity. -pv_ size _kw::Real Size of PV System - pv_ produc!on _factor_ series::Array PV produc!on factor per !me step. Must be hourly and have length of 8760. (Required if pv _size_ kw in dic!onary) -pv _migrogrid_ upgraded::Bool If true then PV runs during outage if microgrid _only = TRUE (defaults to false) -ba"ery_ size _kw::Real Ba"ery capacity. If no ba"ery installed then PV disconnects from system during outage -ba"ery_ size _kwh::Real Ba"ery energy storage capacity -ba"ery_ charge _efficiency::Real Ba"ery charge efficiency -_ 

https://natlabrockies.github.io/REopt.jl/dev/reopt/methods/ 

Page 5 of 6 

Methods · REopt.jl Documentation 

4/16/26, 10:32 AM 

_ba"ery_ discharge star!ng _soc_ series _frac!on::Array Ba"ery percent state of charge !me series during normal grid-connected usage. Must be hourly and have length of 8760. -generator_ failure _to_ start::Real = 0.0094 Chance of generator star!ng given outage -generator _mean_ !me _to_ failure::Real = 1100 Average number of !me steps between a generator's failures. 1/(failure to run probability). -num _generators::Int = 1 Number of generators. - generator_ size _kw::Real = 0.0 Backup generator capacity. -num_ ba#ery _bins::Int =_ 

_num_ ba#ery _bins_ default(r[:ba#ery _size_ kw],r[:ba#ery _size_ kwh]) Number of bins for discretely modeling ba#ery state of charge -max _outage_ dura!on::Int = 96 Maximum outage dura!on modeled 

« Outputs 

Examples » 

Powered by Documenter.jl and the Julia Programming Language. 

https://natlabrockies.github.io/REopt.jl/dev/reopt/methods/ 

Page 6 of 6 

