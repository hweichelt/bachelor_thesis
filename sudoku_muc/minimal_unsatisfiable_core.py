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
    def render_sudoku(symbol_list, visualization_file):
        ctl = clingo.Control()
        fb = Factbase(prefix="viz_", default_graph="sudoku")

        program_string = ". ".join([str(symbol) for symbol in symbol_list])
        if program_string:
            program_string += "."

        print(program_string)

        visualization_string = Util.get_file_content_str(visualization_file)

        ctl.add("base", [], program_string)
        ctl.add("base", [], visualization_string)

        ctl.ground([("base", [])], ClingraphContext())

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


class Container:

    def __init__(self, program, instance, assumptions=None):
        if assumptions is None:
            assumptions = []

        self.control = clingo.Control()
        self.program = program
        self.instance = instance
        self.assumptions = assumptions

        program_string = Util.get_file_content_str(program)
        instance_string = Util.get_file_content_str(instance)

        self.control.add("base", [], program_string)
        self.control.add("base", [], instance_string)

        self.control.ground([("base", [])])

        self.assumptions_lookup = {}
        if self.assumptions:
            self.assumptions_lookup = {self.control.symbolic_atoms[assumption].literal: assumption for assumption in self.assumptions}

    def solve(self, different_assumptions=None):
        shown_atoms = ["solution", "initial", "guess"]

        if different_assumptions is not None:
            assumptions_prep = [(assumption, True) for assumption in different_assumptions]
        else:
            assumptions_prep = [(assumption, True) for assumption in self.assumptions]

        with self.control.solve(assumptions=assumptions_prep, yield_=True) as solve_handle:
            satisfiable = solve_handle.get().satisfiable
            if solve_handle.model() is not None:
                model = [atom for atom in solve_handle.model().symbols(atoms=True) if atom.name in shown_atoms]
            else:
                model = []
            core = [self.assumptions_lookup[index] for index in solve_handle.core()]
        return satisfiable, model, core

    def get_muc_iterative_deletion(self):
        print("MUC ITERATIVE DELETION")
        satisfiable, _, core = self.solve()
        muc_found = False
        if satisfiable:
            return muc_found, []

        minimal_unsatisfiable_core = []
        for index, assumption in enumerate(core):
            partial_assumptions = [a for a in core if a != assumption]
            sat, _, _ = self.solve(different_assumptions=partial_assumptions)
            if sat:
                minimal_unsatisfiable_core.append(assumption)

        return True, minimal_unsatisfiable_core

    def __str__(self):
        out = repr(self) + "\n"
        out += "\t<assumptions>\n"
        for index, assumption in self.assumptions_lookup.items():
            out += f"\t\t{index} : {assumption}\n"
        out += "\t</assumptions>\n"
        return out + f"</{self.__class__.__name__}>"

    def __repr__(self):
        return f"<{self.__class__.__name__} program={self.program} instance={self.instance}>"
