from clingraph.orm import Factbase
from clingraph.graphviz import compute_graphs, render


def example_clingraph():

    fb = Factbase(prefix="viz_", default_graph="sudoku")
    fb.add_fact_file("res/factbases/fb_example_2.lp")

    print(fb)

    graphs = compute_graphs(fb)
    print(graphs, graphs["sudoku"])

    render(graphs, format="png", view=True, engine="neato")
