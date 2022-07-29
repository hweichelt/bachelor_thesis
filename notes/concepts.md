# Concepts

## Contents
1. [Tasks](#tasks)
2. [Definitions](#definitions)
3. [Algorithms](#algorithms)

***

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
+ [A5 : Improved Brute Force : Finding all Minimal Unsat Cores](#a5--improved-brute-force--finding-all-minimal-unsat-cores)

### T3 : Finding the Minimum Unsat Core of an Unsat Assumption Set
This Task is highly interesting because its goal is to find the minimum unsatisfiable core of an unsatisfiable assumption set. The minimum unsatisfiable core is the smallest unsatisfiable core and thus optimizes the unatisfiability of the original assumption set with the least number of core assumptions. 

#### Algorithms:
+ [A3 : Brute-Force : Finding the Minimum Unsat Core](#a3--brute-force--finding-the-minimum-unsat-core)
+ [A6 : Improved Brute Force : Finding all Minimum Unsat Cores](#a6--improved-brute-force--finding-all-minimum-unsat-cores)

### T4 : Reducing a Not-Multi-Unsat Core to any Minimal Unsat Core
The task of reducing any unsatisfiable core to a minimal version of itself is also highly useful. Often its not really necessary to find the minimum unsatisfiable core, but we only have to minimize a given unsatisfiable core that's not a multi unsat core. In most cases this can be done very efficiently but doesn't guarantee any minimality.

#### Algorithms:
+ [A4 : Finding a Minimal Unsat Core using Assumption Marking](#a4--finding-a-minimal-unsat-core-using-assumption-marking)
	+ Only works If the Unsat Core is not a multi unsatisfiable core!

### T5 : Reducing a Multi-Unsat Core to any Minimal Unsat Core
This task is very similar to [T4 : Reducing an Unsat Core to any Minimal Unsat Core](#t4--reducing-an-unsat-core-to-any-minimal-unsat-core), only that instead of a not multi unsatisfiable core we're now dealing with a multi unsatisfiable core. This makes the whole task harder and computationally costlier, but it can be applied way more generally.

#### Algorithms:
+ `None implemented yet`

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
`minimal_unsatisfiable_core.Container.get_all_uc_brute_force()`

| | |
|:-|:-|
|**Input**| Assumption Set (Unsatisfiable Core)|
|**Output**| List of all contained Unsatisfiable Cores|

This algorithm is used to solve the task [T1 : Finding all Unsat Cores of an Assumption Set](#t1--finding-all-unsat-cores-of-an-assumption-set). It approaches the problem in a brute force way, by first computing all possible subsets of the assumption set (powerset), and then checks all of them whether they are an unsatisfiable core or not.

### A2 : Brute-Force : Finding all Minimal Unsat Cores
`minimal_unsatisfiable_core.Container.get_all_minimal_uc_brute_force()`

| | |
|:-|:-|
|**Input**| Assumption Set (Unsatisfiable Core)|
|**Output**| List of all contained minimal Unsatisfiable Cores|

This algorithm is used to solve the task [T2 : Finding all Minimal Unsat Cores of an Unsat Assumption Set](#t2--finding-all-minimal-unsat-cores-of-an-unsat-assumption-set). It first uses algorithm [A1 : Brute-Force : Finding all Unsat Cores](#a1--brute-force--finding-all-unsat-cores) to find all unsatisfiable cores for the assumption set (brute force), and then checks if any found core is a superset of another (possibly minimal) found core.

### A3 : Brute-Force : Finding the Minimum Unsat Core
`minimal_unsatisfiable_core.Container.get_all_minimum_uc_brute_force()`

| | |
|:-|:-|
|**Input**| Assumption Set (Unsatisfiable Core)|
|**Output**| Minimum Unsatisfiable Core of Assumption Set|

This algorithm is used to solve the task [T3 : Finding the Minimum Unsat Core of an Unsat Assumption Set](#t3--finding-the-minimum-unsat-core-of-an-unsat-assumption-set). It first uses algorithm [A1 : Brute-Force : Finding all Unsat Cores](#a1--brute-force--finding-all-unsat-cores) to find all unsatisfiable cores for the assumption set (brute force), and then searches for the unsatisfiable core of the smallest size.

### A4 : Finding a Minimal Unsat Core using Assumption Marking
`minimal_unsatisfiable_core.Container.get_any_minimal_uc_assumption_marking()`

| | |
|:-|:-|
|**Input**| Unsatisfiable Core that's not a Multi UC|
|**Output**| A Minimal Unsatisfiable Core (Minimum not guaranteed)|

This algorithm is used to solve the task [T4 : Reducing an Unsat Core to any Minimal Unsat Core](#t4--reducing-an-unsat-core-to-any-minimal-unsat-core). It is important to note though, that the algorithm only works on assumption sets, that aren't multi unsatisfiable cores.
It works by iterating through the assumption set and in each step marking a different assumption. We then try to solve the original problem with the assumption set excluding the marked assumption. If it gets satisfiable this way, the marked assumption is added to the minimal core members. This continues until all assumptions have been checked.

### A5 : Improved Brute Force : Finding all Minimal Unsat Cores
`minimal_unsatisfiable_core.Container.get_all_minimal_uc_improved_brute_force()`

| | |
|:-|:-|
|**Input**| Assumption Set (Unsatisfiable Core)|
|**Output**| A List of all minimal Unsatisfiable Core in the Assumption Set|

This algorithm implements an improved brute force way to solve the task [T2 : Finding all Minimal Unsat Cores of an Unsat Assumption Set](#t2--finding-all-minimal-unsat-cores-of-an-unsat-assumption-set). It iterates over the whole powerset of the assumptions and checks whether the current set is an unsatisfiable core. If it is, it's stored in a list so that every future set that has an already found core as a subset can be skipped.

### A6 : Improved Brute Force : Finding all Minimum Unsat Cores
`minimal_unsatisfiable_core.Container.get_all_minimum_uc_improved_brute_force()`

| | |
|:-|:-|
|**Input**| Assumption Set (Unsatisfiable Core)|
|**Output**| A List of all minimum Unsatisfiable Core in the Assumption Set|

This algorithm implements an improved brute force way to solve the task [T3 : Finding the Minimum Unsat Core of an Unsat Assumption Set](#t3--finding-the-minimum-unsat-core-of-an-unsat-assumption-set). It iterates over the powerset of the assumptions and checks whether the current set is an unsatisfiable core. Because the powerset is ordered by subset-size, if any core is found it is automatically a minimal unsatisfiable core. When this happens the size of the unsatisfiable core is stored, and only the remaining subsets of the same size are checked for unsatisfiable cores. If this is finished, a list containing all minimum unsatisfiable cores is returned.