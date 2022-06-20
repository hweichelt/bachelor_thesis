import os
from abc import ABC, abstractmethod

import clingo
from clingraph.orm import Factbase
from clingraph.graphviz import compute_graphs, render


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
    def render_sudoku(model_string, visualization_file):
        # TODO : Remove os.system call
        print("GENERATING CLINGRAPH FACTBASE VIA OS.SYSTEM : REMOVE!")
        # Write the found model to res/models/temp_model.lp
        with open("res/models/temp_model.lp", "w") as f:
            f.write(".\n".join(model_string.split()) + ".")
        os.system(
            f"clingo res/models/temp_model.lp -n 0 --outf=2 | clingraph --view --out=facts --prefix=viz_ "
            f"--default-graph=sudoku --viz-encoding={visualization_file} > res/factbases/factbase.lp "
        )
        print("CLINGRAPH FACTBASE GENERATED")

        fb = Factbase(prefix="viz_", default_graph="sudoku")
        fb.add_fact_file("res/factbases/factbase.lp")

        # TODO : Use the internal function from model somehow
        # fb = Factbase.from_model(solve_handle.model(), prefix="viz_")
        # print(type(fb), fb)

        graphs = compute_graphs(fb)

        render(graphs, format="png", view=True, engine="neato")


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
