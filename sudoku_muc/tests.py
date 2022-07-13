import clingo
from clingraph.orm import Factbase
from clingraph.graphviz import compute_graphs, render
from clingraph.clingo_utils import ClingraphContext

from minimal_unsatisfiable_core import Util


def example_clingraph():

    fb = Factbase(prefix="viz_", default_graph="sudoku")
    fb.add_fact_file("res/factbases/fb_example_2.lp")

    print(fb)

    graphs = compute_graphs(fb)
    print(graphs, graphs["sudoku"])

    render(graphs, format="png", view=True, engine="neato")


def clingraph_factbase_computation():

    print("VIZ NEW")
    ctl = clingo.Control()
    fb = Factbase(prefix="viz_", default_graph="sudoku")

    program_string = Util.get_file_content_str("res/examples/sudoku/sudoku_solver.lp")
    instance_string = Util.get_file_content_str("res/instances/sudoku_instance_very_small.lp")
    # TODO : ERROR INSIDE VISUALIZE SUDOKU .LP
    visualization_string = Util.get_file_content_str("res/visualization/visualize_sudoku_example.lp")

    ctl.add("base", [], program_string)
    ctl.add("base", [], instance_string)
    ctl.add("base", [], visualization_string)

    ctl.ground([("base", [])], ClingraphContext())

    print("NO-ASSUMPTIONS")
    solve_handle = ctl.solve(yield_=True)

    if solve_handle.get().satisfiable:

        fb.add_model(solve_handle.model())

        graphs = compute_graphs(fb)

        render(graphs, format="png", view=True, engine="neato")

    else:
        print(solve_handle.get())

