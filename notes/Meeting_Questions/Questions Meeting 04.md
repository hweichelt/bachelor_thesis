# Questions : 25.05.2022
Questions about paper-2: "Unsatisfiable Core Shrinking for Anytime Answer Set Optimization", Alviano, Dodaro

I've looked again at the two proposed algorithms in this paper and applied them on a few examples. I think I generally worked out what they do and how.

**Q : UC Shrinking Algorithm**

It seems to me that the first algorithm isn't really concerned with unsatisfiable core shrinking which is the part of the second algorithm. Should the focus in this paper therefore be set on the second algorithm?

***

Questions about paper-3: "A Scalable Algorithm for Minimal Unsatisfiable Core Extraction", Dershowitz, Hanna, Nadel

**Q : CLASP DPLL**

In the Introduction it is mentioned that the SAT-Solver GRASP uses an implementation of DPLL enhanced by a failure driven assertion loop. I was wondering whether CLASP is implemented in a similar way and what this failure driven assertion loop looks like.

**Q : CRR Algorithm**

In Algorithm 1 line 4 the unreachable vertices from initial clause $C, UnRe(\Pi,C)$ are used as a clause set for the SAT solver. As I understand it, this is to exclude the initial clause $C$ and all conflict clauses containing $C$ to check if $C$ is part of the MUC. Is that correct?