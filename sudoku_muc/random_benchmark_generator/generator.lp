% --- RANDOM MUC BENCHMARK GENERATOR --- %

#const n_assumptions=100.
#const n_mucs=30.

% CREATE N ASSUMPTION ATOMS
assumption(1..n_assumptions).

% CREATE M MUC ATOMS
muc(1..n_mucs).

% ASSOCIATE BETWEEN 1 and N ASSUMPTIONS WITH EACH MUC
1{muc_assumption(M, A): assumption(A)}n_assumptions :- muc(M).

% STORE THE SIZE (AMOUNT OF ASSOCIATED ASSUMPTIONS) FOR EACH CORE
core_size(M, S) :- muc(M), S = #count{A : muc_assumption(M, A)}.
% STORE THE AMOUNT OF ASSUMPTIONS FROM MUC1 CONTAINED IN MUC2
sum_contained(M1, M2, S) :- muc(M1), muc(M2), M1!=M2, S = #count{A : muc_assumption(M2, A), muc_assumption(M1, A)}.

% IT CANNOT BE THAT ALL ASSUMPTIONS OF ONE MUC ARE CONTAINED INSIDE ANOTHER
:- muc(M1), muc(M2), M1!=M2, core_size(M1, S), sum_contained(M1, M2, C), S==C.

%#show core_size/2.
%#show sum_contained/3.
#show muc_assumption/2.
%#show assumption/1.
%#show muc/1.