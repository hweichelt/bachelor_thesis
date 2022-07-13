# Questions : 25.05.2022

Questions from last week:

paper-1 : "On Computing Minimum Unsatisfiable Cores", Inês Lynce and João Marques-Silva.

**Q : Clause recording**

On page 4 in Example 3 a new clause is recorded after a solution is found for the current assignment. But even though $s_1$ is assigned as $s_1=0$, the final clause only contains $s_2 \lor s_5$ . They explain this by saying that $\omega_1'$ is satisfied by $x_1=1$. Does that mean, that every other assignment of the X-Space that still is a solution could create a different clause that will be added?

For example:
+ $\{s_1=0, s_2=0, s_3=1, s_4=1, s_5=0, s_6=1, x_1=1, x_2=0, x_3=0 \} \to \omega_8' = s_2 \lor s_5$
+ $\{s_1=0, s_2=0, s_3=1, s_4=1, s_5=0, s_6=1, x_1=0, x_2=0, x_3=0 \} \to \omega_8' = s_1 \lor s_2 \lor s_5$ ?
+ ...

***

Questions about paper-2: "Unsatisfiable Core Shrinking for Anytime Answer Set Optimization", Alviano, Dodaro

**Q : Symmetry Breakers**

How do the Symmetry Breakers that are added to a Program $\Pi$  after an iteration step in the ONE Algorithm work exactly?

**Q : ONE Algorithm**

Related to the Question above, in Example 3 after the first iteration step the set $S$ is set to $\{s_1, s_2, s_3\}$. How do we get to this new assignment of $S$ and the new rules that extend the Program $\Pi$?
