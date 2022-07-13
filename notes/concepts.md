# Concepts

## Tasks
When looking at Unsat-Cores many tasks come to mind that are useful when dealing with them. This here is a growing collection of Tasks to somehow minimize Unsat Cores. Each Task is suited for a different problem, and some Tasks are way harder to solve than others, so this Collection aims to give an overview over the whole problem setting.


### T1 : Finding all Unsat Cores of an Assumption Set
This task aims to find every single unsatisfiable core inside a set of assumptions. This includes all minimal unsatisfiable cores, the minimum unsatisfiable core and also all bigger cores that have a minimal unsatisfiable core as a subset.

#### Algorithms:
+ [A1 : Brute-Force : Finding all Unsat Cores](#a1--brute-force--finding-all-unsat-cores)

### T2 : Finding all Minimal Unsat Cores of an Unsat Assumption Set
In this task, the goal is to find every minimal unsatisfiable core contained inside an assumption set. This also includes the minimum core.

#### Algorithms:
+ [A2 : Brute-Force : Finding all Minimal Unsat Cores](#a2--brute-force--finding-all-minimal-unsat-cores)

### T3 : Finding the Minimum Unsat Core of an Unsat Assumption Set
This Task is highly interesting because its goal is to find the minimum unsatisfiable core of an unsatisfiable assumption set. The minimum unsatisfiable core is the smallest unsatisfiable core and thus optimizes the unatisfiability of the original assumption set with the least number of core assumptions. 

### Algorithms:
+ [A3 : Brute-Force : Finding the Minimum Unsat Core](#a3--brute-force--finding-the-minimum-unsat-core)

### T4 : Reducing an Unsat Core to any Minimal Unsat Core
The task of reducing any unsatisfiable core to a minimal version of itself is also highly useful. Often its not really necessary to find the minimum unsatisfiable core,  but we only have to minimize a given unsatisfiable core. in most cases this can be done very efficiently but doesn't guarantee any minimality.

### Algorithms:
+ [A4 : Finding a Minimal Unsat Core using Assumption Marking](#a4--finding-a-minimal-unsat-core-using-assumption-marking)
	+ Only works If the Unsat Core is not a multi unsatisfiable core!

***

## Definitions

### D1 : Unsatisfiable Core
+ Source : ["On Computing Minimum Unsatisfiable Cores": Lynce, Silva](../papers/1.pdf)


### D2 : Minimal Unsatisfiable Core
+ Source : ["On Computing Minimum Unsatisfiable Cores": Lynce, Silva](../papers/1.pdf)


### D3 : Minimum Unsatisfiable Core
+ Source : ["On Computing Minimum Unsatisfiable Cores": Lynce, Silva](../papers/1.pdf)


### D4 : Multi-Unsat-Core
+ Source : Own Idea

***

## Algorithms 

### A1 : Brute-Force : Finding all Unsat Cores
`minimal_unsatisfiable_core.Container.get_uc_all_brute_force()`

### A2 : Brute-Force : Finding all Minimal Unsat Cores
`NOT IMPLEMENTED YET`

### A3 : Brute-Force : Finding the Minimum Unsat Core
`minimal_unsatisfiable_core.Container.get_minimum_ucs_brute_force()`

### A4 : Finding a Minimal Unsat Core using Assumption Marking
`minimal_unsatisfiable_core.Container.get_muc_on_core_assumption_marking()`
