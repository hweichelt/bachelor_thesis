#const n_assumptions=3.

{a(1..3)}.

unsat :- a(1), a(2).
unsat :- a(3).
