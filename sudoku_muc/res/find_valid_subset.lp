% ----

% minimal_core(1, assumption(2)).
% minimal_core(1, assumption(3)).
% minimal_core(1, assumption(1)).

% sat_subset(1, assumption(3)).
% sat_subset(1, assumption(4)).

% selection_size(3).

% ----

%#const n_assumptions=4.

%selection_size(3).

% minimal_core(0, assumption(1)).

% ||| --- GENERATING THE SELECTION --- |||

assumption(1..n_assumptions).
core(0..max_cores).
sat(0..max_sat).

1{core_assumptions(N) : N=0..X, X=max_cores*n_assumptions}1.
1{sat_assumptions(N) : N=0..X, X=max_sat*n_assumptions}1.

CA{minimal_core(X,assumption(Y)) : core(X), assumption(Y)}CA :- core_assumptions(CA).
SA{sat_subset(X,assumption(Y)) : sat(X), assumption(Y)}SA :- sat_assumptions(SA).

{selected(assumption(X))} :- assumption(X).
assumptions_selected(N) :- N = #count{ A : selected(A)}.

1{selection_size(X) : assumption(X)}1.

muc_assumption_contained(CORE_ID, assumption(X)) :- selected(assumption(X)), minimal_core(CORE_ID, assumption(X)).
sat_assumption_contained(SAT_ID, assumption(X)) :- selected(assumption(X)), sat_subset(SAT_ID, assumption(X)).


% ||| --- ELIMINATING SKIPPABLE SELECTIONS --- |||

% ELIMINATING ALL INSTANCES WHERE A MUC IS A SUBSET
:- minimal_core(CORE_ID, _), X = #count{ A : muc_assumption_contained(CORE_ID, A)}, Y = #count{ A : minimal_core(CORE_ID, A)}, X==Y.

% ELIMINATING ALL INSTANCES WHICH ARE SUBSET TO A MUC
:- minimal_core(CORE_ID, _), X = #count{ A : selected(A)}, Y = #count{ A : muc_assumption_contained(CORE_ID, A), selected(A)}, X==Y.

% ELIMINATING ALL INSTANCES WHICH ARE SUBSET TO A SAT_SUBSET
:- sat_subset(SAT_ID, _), X = #count{ A : selected(A)}, Y = #count{ A : sat_assumption_contained(CORE_ID, A), selected(A)}, X==Y.


% ||| --- MAXIMIZING THE SIZE OF THE SELECTION --- |||

% MAXIMIZE WORKS BUT MAKES IT REALLY SLOW
% #maximize{N : assumptions_selected(N)}.

% ALTERNATIVE : CONDITION THAT SETS THE SIZE OF THE SELECTION
:- assumptions_selected(N), selection_size(M), M!=N.

%#show minimal_core/2.
#show selected/1.
#show selection_size/1.
#show sat_subset/2.
#show sat_assumptions/1.
