# Questions : 08.07.2022

Unsat Core Questions

**Q : Internal Conflicts > 2**

I was thinking about Multi Unsat Core examples that contained internal cores, which have more than two members. For example the Unsat Core $\{a, \underline{b, c, d}, e\}$, where $\{b,c,d\}$ is an internal core. But when thinking of a way to create such a core within the Sudoku domain, I couldn't figure out how to. I think because the integrity constraints in the Sudoku Domain are all just concerned with two cell-values its not possible to create bigger internal conflicts here. Is that true and if so, what would be another good example domain to look at these bigger internal cores?

***

General Questions

**Q : Access to the First Aid Room and Lounge**

Like the Psst Group-Chat in Element a few weeks ago, lost access to the First-Aid-Room and Lounge Chat now. Can I be added back into these groups?

***

Ideas

**IDEA : Orkunt's Implementation to use facts as assumptions**

Last week you showed my Orkunt's implementation to modify an asp program to use its given facts as assumptions. We could use this to identify the corresponding other cell-value that clashes with a found atomic core to make this information about the core more usable. That would effectively transform each found atomic core to an internal core that uses an assumption generated from the facts as its other core member.

**Q : Integrity Constraints**

Is it possible for a valid ASP Program to become unsatisfiable without having integrity constraints, and if so are these integrity constraints always the cause of it being unsatisfiable?

**IDEA : Finding the causing integrity constraint**

If this is the case: We could take each identified MUC to use a similar assumption marking or iterative deletion algorithm to find out which integrity constraints cause the program to become unsatisfiable.