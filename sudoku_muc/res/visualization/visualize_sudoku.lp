% %%%%%%%%%%%%%%%%%%%%%%%%% Visualization
% based on the example at : https://github.com/potassco/clingraph/blob/master/examples/sudoku/viz.lp

#const cage_size = 3.

% Convert solution to sudoku
sudoku(X,Y,N) :- visualize_sudoku(X,Y,N).
initial(X,Y,N) :- visualize_initial(X,Y,N).

% Generate pos
size(1..cage_size*cage_size).
pos(X,Y) :- size(X), size(Y).

% Generate subgrid
subgrid(X,Y,(((X-1)/cage_size)*cage_size+((Y-1)/cage_size))) :- pos(X,Y).

viz_graph(sudoku).

% Name of graph
viz_attr(graph, sudoku, name, "Sudoku").
viz_attr(graph, sudoku, gradientangle, 270).
viz_attr(graph, sudoku, bgcolor, "#37474F:#263238").
viz_attr(graph, sudoku, style, "linear").
viz_attr(graph, sudoku, pad, "0.5").

% Global graph attributes
viz_attr(graph, sudoku, nodesep, 1).
viz_attr(graph, sudoku, newrank, true).

% Global node attributes
viz_attr(graph_nodes, sudoku, shape, square).
viz_attr(graph_nodes, sudoku, style, filled).
viz_attr(graph_nodes, sudoku, fillcolor, "#37474F").
viz_attr(graph_nodes, sudoku, width, "1").
viz_attr(graph_nodes, sudoku, fontsize, 30).
viz_attr(graph_nodes, sudoku, fontname, "JetBrains Mono").

% Nodes
viz_node(pos(X,Y), sudoku):- pos(X,Y).
viz_attr(node, pos(X,Y), fillcolor, transparent):- pos(X,Y), subgrid(X,Y,S), S\2==0.



viz_attr(node, pos(X,Y), label, V):- sudoku(X,Y,V), not initial(X,Y,_).
viz_attr(node, pos(X,Y), (label,0), "<<B>"):- sudoku(X,Y,V), initial(X,Y,_).
viz_attr(node, pos(X,Y), (label,1), V):- sudoku(X,Y,V), initial(X,Y,_).
viz_attr(node, pos(X,Y), (label,2), "</B>>"):- sudoku(X,Y,V), initial(X,Y,_).
viz_attr(node, pos(X,Y), fontcolor, "#D6F8D6"):- sudoku(X,Y,V), not initial(X,Y,_).
viz_attr(node, pos(X,Y), fontcolor, "#7FC6A4"):- sudoku(X,Y,V), initial(X,Y,_).
viz_attr(node, pos(X,Y), pos, @pos(X,Y)):- pos(X,Y).

% Allow display of Empty cells
viz_attr(node, pos(X,Y), label, " "):- not sudoku(X,Y,_), pos(X,Y).

% Edges to show subgrids
viz_edge((pos(X,Y),pos(X+1,Y)),sudoku):- pos(X,Y), pos(X+1,Y), subgrid(X,Y,S), subgrid(X+1,Y,S).
viz_edge((pos(X,Y),pos(X,Y+1)),sudoku):- pos(X,Y), pos(X,Y+1), subgrid(X,Y,S), subgrid(X,Y+1,S).