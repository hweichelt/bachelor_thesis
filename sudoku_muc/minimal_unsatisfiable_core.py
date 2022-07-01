import os
import random
from abc import ABC, abstractmethod
from itertools import chain, combinations

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


class Container:

    def __init__(self, program_string, assumptions=None):
        if assumptions is None:
            assumptions = []

        self.control = clingo.Control()
        self.program_string = program_string
        self.assumptions = assumptions

        self.control.add("base", [], program_string)

        self.control.ground([("base", [])])

        self.assumptions_lookup = {}
        if self.assumptions:
            self.assumptions_lookup = {
                self.control.symbolic_atoms[assumption].literal: assumption for assumption in self.assumptions
            }

    def solve(self, different_assumptions=None):
        shown_atoms = ["solution", "initial"]

        if different_assumptions is not None:
            assumptions_prep = [(assumption, True) for assumption in different_assumptions]
        else:
            assumptions_prep = [(assumption, True) for assumption in self.assumptions]

        with self.control.solve(assumptions=assumptions_prep, yield_=True) as solve_handle:
            satisfiable = solve_handle.get().satisfiable
            if solve_handle.model() is not None:
                # filter out all atoms from the model that are not in shown_atoms
                model = [atom for atom in solve_handle.model().symbols(atoms=True) if
                         any([atom.match(signature, 3, True) for signature in shown_atoms])]
            else:
                model = []
            core = [self.assumptions_lookup[index] for index in solve_handle.core()]
        return satisfiable, model, core

    def get_muc_on_core_assumption_marking(self):
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

        muc_found = True
        return muc_found, minimal_unsatisfiable_core

    def get_muc_iterative_deletion(self):
        # This algorithm aims to return a minimal unsatisfiable core from the assumption set that is given for the
        # container. In this way this algorithm is specifically optimized to also handle Multi Unsatisfiable Cores and
        # compute more efficiently than the brute force algorithm.
        # It works in the way that the assumption set is iteratively reduced until it becomes satisfiable or empty. When
        # this point is reached, the last removed assumption is added to a list of minimal core members, and the process
        # is repeated with an assumption set, that is missing this assumption. This is continued until the remaining
        # assumption set becomes satisfiable from the start.

        satisfiable, _, core = self.solve()
        if satisfiable:
            return []

        minimal_unsatisfiable_core_members = []
        assumption_set = self.assumptions

        # shuffling assumption_set before solving for added suspense
        # TODO : remove when sufficiently tested
        random.shuffle(assumption_set)

        print([str(a) for a in assumption_set])

        remaining_set_satisfiable = False
        while not remaining_set_satisfiable:
            working_set_satisfiable = False
            for i in range(len(assumption_set)):
                # iteratively remove assumptions from the set until it becomes satisfiable or empty
                if self.solve(different_assumptions=assumption_set[i:])[0]:
                    working_set_satisfiable = True
                    break

            # check if the working set became satisfiable or the end was reached
            if not working_set_satisfiable:
                # select last assumption of the working set
                unsat_core_member = assumption_set[-1]
            else:
                # select last removed item
                unsat_core_member = assumption_set[i-1]

            # update step
            minimal_unsatisfiable_core_members.append(unsat_core_member)
            assumption_set = [a for a in assumption_set if a != unsat_core_member]

            # check whether the remaining assumption set is already satisfiable
            if self.solve(different_assumptions=assumption_set)[0]:
                remaining_set_satisfiable = True

        # TODO : Check if it really always works !

        return minimal_unsatisfiable_core_members

    def get_uc_all_brute_force(self):
        # The simplest brute force approach to get all unsatisfiable cores. Taking the list of assumptions and checking
        # every possible subset for being an unsatisfiable core. This approach will definitely include all minimal
        # unsatisfiable cores and even the minimum core. In turn this approach takes (O(2^n)) Exponential time and
        # will not at all be useful in real world scenarios which require big assumption sets and fast solving times.

        # get the powerset of the assumption_list
        powerset = chain.from_iterable(combinations(self.assumptions, r) for r in range(len(self.assumptions) + 1))

        unsatisfiable_cores = []
        for assumption_set in powerset:
            sat, _, _ = self.solve(different_assumptions=assumption_set)
            if not sat:
                unsatisfiable_cores.append(assumption_set)

        return unsatisfiable_cores

    def get_minimum_ucs_brute_force(self):
        # this algorithm just implements the brute force algorithm for all ucs (get_uc_all_brute_force()) and finds the
        # smallest core within the set of ucs that is returned

        unsatisfiable_cores = self.get_uc_all_brute_force()
        minimum = min(unsatisfiable_cores, key=lambda x: len(x))
        return [uc for uc in unsatisfiable_cores if len(uc) == len(minimum)]

    def __str__(self):
        out = repr(self) + "\n"
        out += "\t<assumptions>\n"
        for index, assumption in self.assumptions_lookup.items():
            out += f"\t\t{index} : {assumption}\n"
        out += "\t</assumptions>\n"
        return out + f"</{self.__class__.__name__}>"

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
