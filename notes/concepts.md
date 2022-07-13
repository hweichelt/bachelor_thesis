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

Given a Formula $\varphi, UC$ is an unsatisfiable core for $\varphi$ if $UC$ is a formula $\varphi_c$ so that $\varphi_c$ is unsatisfiable and $\varphi_c \subseteq \varphi$.

### D2 : Minimal Unsatisfiable Core
+ Source : ["On Computing Minimum Unsatisfiable Cores": Lynce, Silva](../papers/1.pdf)

An unsatisfiable core $UC$ for $\varphi$ is a minimal unsatisfiable core if removing any clause $\omega \in UC$ from $UC$ implies that $UC - \lbrace\omega\rbrace$ is not an unsatisfiable core.

### D3 : Minimum Unsatisfiable Core
+ Source : ["On Computing Minimum Unsatisfiable Cores": Lynce, Silva](../papers/1.pdf)

Consider a Formula $\varphi$ and the set of all unsatisfiable cores for $\varphi: \lbrace UC_1, ..., UC_j\rbrace$. Then $UC_k \in \lbrace UC_1, ..., UC_j\rbrace$ is a minimum unsatisfiable core for $\varphi$ if $\forall UC_i \in \lbrace UC_1, ..., UC_j\rbrace, 0 < i \leq j : |UC_i| \geq |UC_j|$.

### D4 : Multi Unsatisfiable Core
+ Source : Own Idea

A multi unsatisfiable core is a non minimal unsatisfiable core $UC$ for $\varphi$, which contains a set of at least two independent minimal unsatisfiable cores $\lbrace MUC_1, ..., MUC_n\rbrace, n\geq 2$. That means that for each assumption $A_x \in MUC_i$ it holds, that $A_x \not\in MUC_j, i\neq j$.

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
