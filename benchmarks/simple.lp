#const n_assumptions=10.
#const n_mucs=50.

#const max_muc_size=10.
#const min_muc_size=1.

#const mucs_per_size=10.

% #const max_muc_size=16.
% #const min_muc_size=4.

a(1..n_assumptions).
c(1..n_mucs).

opt_max_muc_size(max_muc_size).
opt_min_muc_size(min_muc_size).
opt_n_mucs(n_mucs).
opt_n_assumptions(n_assumptions).


min_muc_size{selected(C,A) : a(A)}max_muc_size :- c(C).

intersecting((C1,C2), A1) :- selected(C1,A1), selected(C2,A2), C1!=C2, A1==A2.

:- c(C1), c(C2), C1!=C2, I1=#count{A: intersecting((C1,C2), A)}, I2=#count{A: selected(C1,A)}, I1==I2.

% ---------- DIFFERENT SIZE DIVERSITY

size(C,S) :- c(C), S=#count{A: selected(C,A)}.

:- a(X), S=#count{C: size(C,X)}, S>mucs_per_size.


#show selected/2.
% #show size/2.
