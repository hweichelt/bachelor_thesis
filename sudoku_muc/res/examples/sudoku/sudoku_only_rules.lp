% ########### SUDOKU RULES ###########

% GENERATING

number(1..9).

% Allow solutions
{solution(X,Y,N) : number(X), number(Y), number(N)}.

% Transfer initial values to solution
solution(X,Y,V) :- initial(X,Y,V).
% Generate Cage Variables for lookup
cage(X1,Y1,X2,Y2):- solution(X1,Y1,_), solution(X2,Y2,_), ((X1-1)/3)==((X2-1)/3), ((Y1-1)/3)==((Y2-1)/3).

% INTEGRITY CONSTRAINTS

% Unique Numbers in X-Direction
:- solution(X,Y1,N), solution(X,Y2,N), Y1 != Y2.
% Unique Numbers in Y-Direction
:- solution(X1,Y,N), solution(X2,Y,N), X1 != X2.
% Unique Numbers in cage
:- cage(X1,Y1,X2,Y2), solution(X1,Y1,N), solution(X2,Y2,N), X1!=X2, Y1!=Y2.


#show solution/3.