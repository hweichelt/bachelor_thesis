# Questions : 08.06.2022

General Questions

**Q : Multi unsatisfiable cores**

What would happen if we would have a Program that contains two different independent unsatisfiable cores? Let's look at this example:
$$
At(\Pi) = \{a,b,x\}
$$
$$
c_1 : b \leftarrow a\ ;\quad c_2: a \leftarrow \lnot b\ ; \quad c_3 : \bot \leftarrow b\ ;\quad c_4 : \bot \leftarrow x\ ;\quad c_5 : x \leftarrow \lnot x
$$
Here we have to sets of clauses which form their own two minimal unsatisfiable cores that are independent of each other: 
$$
UC_1:\{c_1, c_2, c_3\} \text{ and } UC_2:\{c_4, c_5\}
$$
When looking for a minimum unsatisfiable core, would only $UC_2$ be returned because it is smaller than $UC_1$ even if they aren't related at all? Is this behavior wanted for a problem like this?

__Example on CRR-Algorithm__ ([paper](https://www.cs.tau.ac.il/~nachum/papers/ScalableAlgorithm.pdf)) :

1. Imagine $c_4$ is the first unmarked clause that is checked by CRR
2. even with removing $c_4$ the problem is still unsatisfiable because it still contains $UC_1$ 
3. $c_4$ is removed from the candidates for the MUC and it becomes impossible to find $UC_2$

Is this a plausible program course? Would the algorithm still produce a useful result like this?

***

Questions about paper-3: "A Scalable Algorithm for Minimal Unsatisfiable Core Extraction", Dershowitz, Hanna, Nadel

**Q : Resolution Refutation**

How is a resolution refutation for an unsatisfiable program built exactly? Is there a way in clingo to compute the refutation and return it? How could it be computed by hand?

***

Organizational Questions for Torsten

+ Is there a formal guideline for a bachelor thesis in info/cs ?
+ how much time do I have after the registration to work on the thesis?
	+ Is there a minimum time?