# Questions : 18.05.2022

Questions about paper-1 : "On Computing Minimum Unsatisfiable Cores", Inês Lynce and João Marques-Silva.

**Q : Iterative Methods**

On page 3 after Definition 3 an example is given why some iterative methods aren't guaranteed to find the minimum unsatisfiable core. There the first iteration produces $UC_1 = \{\omega_1, \omega_3, \omega_4, \omega_5, \omega_6\}$ even though $UC_1$ is earlier defined as $UC_1 = \{\omega_1, \omega_2, \omega_3, \omega_4, \omega_5, \omega_6\}$. Is this a mistake by the authors or intended and if intended why?

> 
> Probably it's a mistake by the authors. I guess UC1 is meant to be the full set of clauses.  
> 

**Q : Clause recording**

On page 4 in Example 3 a new clause is recorded after a solution is found for the current assignment. But even though $s_1$ is assigned as $s_1=0$, the final clause only contains $s_2 \lor s_5$ . They explain this by saying that $\omega_1'$ is satisfied by $x_1=1$. Does that mean, that every other assignment of the X-Space that still is a solution could create a different clause that will be added?

For example:
+ $\{s_1=0, s_2=0, s_3=1, s_4=1, s_5=0, s_6=1, x_1=1, x_2=0, x_3=0 \} \to \omega_8' = s_2 \lor s_5$
+ $\{s_1=0, s_2=0, s_3=1, s_4=1, s_5=0, s_6=1, x_1=0, x_2=0, x_3=0 \} \to \omega_8' = s_1 \lor s_2 \lor s_5$ ?
+ ...

> 
> ANSWER FOLLOWING NEXT WEEK
> 

**Q : SAT generators?**

What are the aim- or uuf50-generators exactly?

>
>No Idea but very likely not important.
>

**Q : The difference between minimum and minimal unsatisfiable core**

As I understand it now, a minimal unsatisfiable core is just a $UC$ that can't be further reduced by throwing out any $\omega_i \in UC$  and still stay an unsatisfiable core. The minimum unsatisfiable core is the smallest $UC$ of a formula $\varphi$, which means that each minimum core is simultaneously a minimal core but not the other way around. Is that correct?

>
>Yes that is correct.
>

