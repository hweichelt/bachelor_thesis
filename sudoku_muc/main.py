import os
import time

import clingo
from minimal_unsatisfiable_core import Util, MUC, Container
from tests import clingraph_factbase_computation

from clingraph.orm import Factbase
from clingraph.graphviz import compute_graphs, render


def muc_sudoku():

    assumption_list = [
        # adding assumptions
        # CORRECT ASSUMPTIONS
        clingo.Function("guess", [clingo.Number(4), clingo.Number(9), clingo.Number(3)]),
        clingo.Function("guess", [clingo.Number(7), clingo.Number(1), clingo.Number(9)]),
        clingo.Function("guess", [clingo.Number(2), clingo.Number(2), clingo.Number(7)]),
        clingo.Function("guess", [clingo.Number(5), clingo.Number(7), clingo.Number(7)]),
        clingo.Function("guess", [clingo.Number(3), clingo.Number(9), clingo.Number(7)]),
        clingo.Function("guess", [clingo.Number(8), clingo.Number(2), clingo.Number(8)]),
        clingo.Function("guess", [clingo.Number(1), clingo.Number(6), clingo.Number(8)]),
        clingo.Function("guess", [clingo.Number(6), clingo.Number(7), clingo.Number(8)]),
        clingo.Function("guess", [clingo.Number(2), clingo.Number(9), clingo.Number(8)]),
        # CONFLICTING ASSUMPTIONS
        # double value for cell
        clingo.Function("guess", [clingo.Number(4), clingo.Number(9), clingo.Number(5)]),
        # value at the wrong position in cage (double 7 in cage(1,1))
        clingo.Function("guess", [clingo.Number(1), clingo.Number(3), clingo.Number(7)]),
    ]

    program = "res/sudoku_only_rules.lp"
    instance = "res/instances/sudoku_instance_1.lp"
    visualization = "res/visualization/visualize_sudoku.lp"

    container_1 = Container(
        program=program,
        instance=instance,
        assumptions=assumption_list,
    )

    print([container_1])
    print(container_1)

    satisfiable, model, core = container_1.solve()
    print("result : ", ["UNSAT", "SAT"][satisfiable])
    print("model : ", model)
    print("core : ", core)

    if satisfiable:
        Util.render_sudoku(model, visualization)

    muc_found, muc = container_1.get_muc_iterative_deletion()

    if not muc_found:
        print("MUC : Problem wasn't unsatisfiable to begin with, there is no minimal unsatisfiable core")
    else:
        print(f"MUC : {muc}")

    # TODO : clingraph in python using the clingraph context with clingo
    # TODO : remove these model strings and instead use maybe these symbolic_atoms
    # TODO : interpret the uc with first creating a dict that associates the assumptions with their int index in the
    #  symbolic atoms so we are able to backtrack the uc to their associated assumption
    # TODO : Look at propagator


if __name__ == '__main__':
    # example_clingraph()
    muc_sudoku()
    # clingraph_factbase_computation()

