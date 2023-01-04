{unsat_core(S)} :- assumption(S).

#heuristic unsat_core(_). [1,false]

:- not unsat.

assumption(a(1..50)).

a(X) :- unsat_core(a(X)).
unsat_core(a(X)) :- a(X).


#show unsat_core/1.
