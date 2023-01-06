% ---[ AUTO GENERATED MUC BENCHMARK ]
% ---[ assumptions : 10 ]
% ---[ mucs : 10 ]

num(1..10).
{a(X): num(X)}.

{CUSTOM_UNSAT_HEAD}:- a(1), a(3), a(7).
{CUSTOM_UNSAT_HEAD}:- a(1), a(4), a(7), a(8), a(10).
{CUSTOM_UNSAT_HEAD}:- a(1), a(2), a(7).
{CUSTOM_UNSAT_HEAD}:- a(8), a(9), a(5), a(6).
{CUSTOM_UNSAT_HEAD}:- a(4), a(6), a(7), a(8), a(10).
{CUSTOM_UNSAT_HEAD}:- a(9), a(2), a(4).
{CUSTOM_UNSAT_HEAD}:- a(3), a(4), a(5), a(6), a(7), a(8).
{CUSTOM_UNSAT_HEAD}:- a(1), a(3), a(4), a(5), a(6), a(8).
{CUSTOM_UNSAT_HEAD}:- a(3), a(4), a(8), a(9), a(10).
{CUSTOM_UNSAT_HEAD}:- a(3), a(5), a(6), a(7), a(8), a(10).
