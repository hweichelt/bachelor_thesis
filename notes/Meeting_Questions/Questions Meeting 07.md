# Questions : 15.06.2022

Clingo API Questions

**Q : UNSAT Core** 

When I'm using the `on_core` callback method from `clingo.Control.solve` it returns a list of integers. These integers are supposed to represent the assumptions contained in the UNSAT core but I cannot figure out how to retrieve information about the original assumptions from the int list.

**Q : Solve Handle**

When I'm using `clingo.Control.solve` with the argument `yield_` set to `True` it returns a `clingo.solving.SolveHandle`. I tried returning this solve handle from within a function and working with it outside of this function which did the `clingo.Control.solve` but it doesn't seem to work. Is this maybe because of some async behavior or why can't I use this solve handle anymore?

**Q : Clingraph Factbase**

The command-line functionality of clingraph allows to compute a Factbase with a given ASP program and the visualizer program. I tried doing this Factbase computation directly in Python but didn't find a way to do it nicely. The way I currently solved the problem is with a `os.system` call and this command :

```bash
clingo [PROGRAM] -n 0 --outf=2 | clingraph --view --out=facts --prefix=viz_ 
--default-graph=sudoku --viz-encoding={visualization_file} > factbase.lp
```

But if there is a way to do this using the clingraph python API I would love to know how it's done.

***

General Questions

**Q : GitHub**

I created a private GitHub Repository to manage the Code for my thesis. I think it's the easiest most accessible way for me to share my code with you. If you want to, I can add you to view the repository if you send me your GitHub Email or username.

You can find my repository [here](https://github.com/vdkjg/bachelor_thesis). 