import os
from abc import ABC, abstractmethod

import clingo
from clingraph.orm import Factbase
from clingraph.graphviz import compute_graphs, render
from clingraph.clingo_utils import ClingraphContext


class Util(ABC):

    @staticmethod
    def get_file_content_str(filename):
        with open(f"{filename}") as f:
            out = f.read()
        return out

    @staticmethod
    def solve(program, instance, assumption_list=None):

        ctl = clingo.Control()

        program_string = Util.get_file_content_str(program)
        instance_string = Util.get_file_content_str(instance)

        ctl.add("base", [], program_string)
        ctl.add("base", [], instance_string)

        ctl.ground([("base", [])])

        assumptions = assumption_list if assumption_list is not None else []
        solve_handle = ctl.solve(assumptions=assumptions, yield_=True)

        satisfiable = solve_handle.get().satisfiable
        model_string = str(solve_handle.model()) if solve_handle.model() is not None else ""
        core = solve_handle.core()

        return satisfiable, model_string, core

    @staticmethod
    def render_sudoku(program, instance, visualization, assumptions=None):
        ctl = clingo.Control()
        fb = Factbase(prefix="viz_", default_graph="sudoku")

        print(program, instance, visualization)

        program_string = Util.get_file_content_str(program)
        instance_string = Util.get_file_content_str(instance)
        visualization_string = Util.get_file_content_str(visualization)

        ctl.add("base", [], program_string)
        ctl.add("base", [], instance_string)
        ctl.add("base", [], visualization_string)

        ctl.ground([("base", [])], ClingraphContext())

        if assumptions is not None:
            print("ASSUMPTIONS")
            solve_handle = ctl.solve(assumptions=assumptions, yield_=True)
        else:
            print("NO-ASSUMPTIONS")
            solve_handle = ctl.solve(yield_=True)

        if solve_handle.get().satisfiable:
            fb.add_model(solve_handle.model())
            graphs = compute_graphs(fb)
            render(graphs, format="png", view=True, engine="neato")
        else:
            print("WARNING: cannot render sudoku. Instance is unsatisfiable")


class MUC(ABC):

    @staticmethod
    def muc_iterative_deletion(program, instance, assumption_list=None):
        # TODO : This algorithm is not using the core but the assumption list. Maye there is a way to use the core
        original_problem_unsatisfiable = False
        (satisfiable, model_string, core) = Util.solve(
            program=program,
            instance=instance,
            assumption_list=assumption_list
        )

        if satisfiable:
            return original_problem_unsatisfiable, None
        else:
            original_problem_unsatisfiable = True
            minimal_core = []
            for i, assumption in enumerate(assumption_list):
                partial_assumption_list = [a for a in assumption_list if a != assumption]
                (sat, _, _) = Util.solve(program=program, instance=instance, assumption_list=partial_assumption_list)
                if sat:
                    minimal_core.append(assumption)

            return original_problem_unsatisfiable, minimal_core
