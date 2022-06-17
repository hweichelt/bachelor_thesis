% %%%%%%%%%%%%%%%%%%%%%%%%% Visualization
% based on the example at : https://github.com/potassco/clingraph/blob/master/examples/sudoku/viz.lp

#const cage_size = 3.

% Convert solution to sudoku
sudoku(X,Y,N) :- solution(X,Y,N).

% Generate pos
size(1..cage_size*cage_size).
pos(X,Y) :- size(X), size(Y).

% Generate subgrid
subgrid(X,Y,(((X-1)/cage_size)*cage_size+((Y-1)/cage_size))) :- pos(X,Y).

viz_graph(sudoku).

% Name of graph
viz_attr(graph, sudoku, name, "Sudoku").

% Global graph attributes
viz_attr(graph, sudoku, nodesep, 1).
viz_attr(graph, sudoku, newrank, true).

% Global node attributes
viz_attr(graph_nodes, sudoku, shape, square).
viz_attr(graph_nodes, sudoku, style, filled).
viz_attr(graph_nodes, sudoku, fillcolor, white).
viz_attr(graph_nodes, sudoku, width, "1").
viz_attr(graph_nodes, sudoku, fontsize, 30).

% Nodes
viz_node(pos(X,Y), sudoku):- pos(X,Y).
viz_attr(node, pos(X,Y), fillcolor, "grey88"):- pos(X,Y), subgrid(X,Y,S), S\2==0.

viz_attr(node, pos(X,Y), label, V):- sudoku(X,Y,V), not initial(X,Y,_).
viz_attr(node, pos(X,Y), (label,0), "<<B>"):- sudoku(X,Y,V), initial(X,Y,_).
viz_attr(node, pos(X,Y), (label,1), V):- sudoku(X,Y,V), initial(X,Y,_).
viz_attr(node, pos(X,Y), (label,2), "</B>>"):- sudoku(X,Y,V), initial(X,Y,_).
viz_attr(node, pos(X,Y), fontcolor, gray):- sudoku(X,Y,V), not initial(X,Y,_).
viz_attr(node, pos(X,Y), pos, @pos(X,Y)):- pos(X,Y).

% Edges to show subgrids
viz_edge((pos(X,Y),pos(X+1,Y)),sudoku):- pos(X,Y), pos(X+1,Y), subgrid(X,Y,S), subgrid(X+1,Y,S).
viz_edge((pos(X,Y),pos(X,Y+1)),sudoku):- pos(X,Y), pos(X,Y+1), subgrid(X,Y,S), subgrid(X,Y+1,S).