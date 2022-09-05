import os
import random
import json
import time
import signal
from abc import ABC, abstractmethod
from itertools import chain, combinations

import clingo
import numpy as np
from clingraph.orm import Factbase
from clingraph.graphviz import compute_graphs, render
from clingraph.clingo_utils import ClingraphContext


ASSUMPTION_SIGNATURE = "assume"
INITIAL_SIGNATURE = "initial"
SHOWN_SIGNATURES = ["solution", "initial"]


class Util(ABC):

    @staticmethod
    def get_file_content_str(filename):
        with open(f"{filename}") as f:
            out = f.read()
        return out

    @staticmethod
    def read_in_asp_file(path, verbose=0, included_filepaths=None):
        # this function works similarly to the get_file_content_str() function but is optimized for clingo asp programs.
        # If the clingo file contains an #include statement the contents of this included file are also recursively read
        # in and appended to the end of the return string.
        # This algorithm uses a list of already included_filepaths to avoid landing in an infinite loop.

        if included_filepaths is None:
            included_filepaths = [os.path.abspath(path)]

        out = ""
        parent_directory = path[:-len(path.split("/")[-1])]
        with open(f"{path}") as f:
            for line in f:
                # check for each line if it is an include statement
                if "#include" in line:
                    # if it is recursively call this function and add it's output to out after a few checks
                    included_filename = line.split('"')[-2]
                    included_filepath = os.path.abspath(parent_directory + included_filename)
                    if included_filepath not in included_filepaths:
                        if not os.path.isfile(included_filepath):
                            raise ValueError(f"Tried to include {included_filepath} but couldn't find file")
                        if verbose > 0:
                            print("included:", included_filepath)
                        included_filepaths.append(included_filepath)
                        out += Util.read_in_asp_file(
                            included_filepath,
                            included_filepaths=included_filepaths,
                            verbose=verbose
                        )
                else:
                    out += line
        return out

    @staticmethod
    def read_dictionary_from_file(path):
        with open(path) as f:
            data = f.read()
        dictionary = json.loads(data)
        return dictionary

    @staticmethod
    def render_sudoku(symbol_list, visualization_file, name_format=None):

        ctl = clingo.Control()
        fb = Factbase(prefix="viz_", default_graph="sudoku")

        program_string = ". ".join([str(symbol) for symbol in symbol_list])
        if program_string:
            program_string += "."

        visualization_string = Util.read_in_asp_file(visualization_file)

        ctl.add("base", [], program_string)
        ctl.add("base", [], visualization_string)

        ctl.ground([("base", [])], ClingraphContext())

        solve_handle = ctl.solve(yield_=True)

        if solve_handle.get().satisfiable:
            fb.add_model(solve_handle.model())
            graphs = compute_graphs(fb)
            if name_format is not None:
                render(graphs, format="png", view=True, engine="neato", name_format=name_format)
            else:
                render(graphs, format="png", view=True, engine="neato")
        else:
            print("WARNING: cannot render sudoku. Instance is unsatisfiable")

    @staticmethod
    def render_sudoku_with_core(container, core, visualization_file, name_format=None):
        # this method is used to render an unsatisfiable sudoku instance with its unsat core. The Util.render_sudoku
        # method is called after some preprocessing on the input data.
        core_symbols = [clingo.parse_term(f"core({str(a)})") for a in core]
        assumption_symbols = [clingo.parse_term(f"assume({str(a)})") for a in container.assumptions]
        initial_symbols = [s.symbol for s in container.control.symbolic_atoms.by_signature(INITIAL_SIGNATURE, 3)]
        symbol_list = assumption_symbols + core_symbols + initial_symbols
        Util.render_sudoku(symbol_list, visualization_file, name_format=name_format)

    @staticmethod
    def timeout_handler(signum, frame):
        raise Exception("OUT OF TIME")

    @staticmethod
    def measure_function(function, args=None, kwargs=None, timeout=10, verbose=0):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        if timeout <= 0:
            raise ValueError("timeout has to be a positive number greater than 0")

        # start countdown for timeout
        signal.alarm(timeout)
        try:
            t_start = time.perf_counter()
            result = function(*args, **kwargs)
            t_end = time.perf_counter()
            # end countdown for timeout if function was able to complete in time
            signal.alarm(0)
            return t_end - t_start, result
        except Exception as e:
            if verbose > 0:
                print(e)
            return -1, None

    @staticmethod
    def generate_dense_example(size=5, path="res/examples/temp/", name="abstract_multi_core_dense"):
        if not os.path.isdir(path):
            os.mkdir(path)
        if not os.path.isdir(f"{path}{name}"):
            os.mkdir(f"{path}{name}")

        print("START GENERATING")

        encoding_str = " ".join([f"{{a({i})}}." for i in range(size)]) + "\n"
        assumptions_str = " ".join([f"assume(a({i}))." for i in range(size)])
        results = {"minimal": [], "minimum": []}
        for subset in chain.from_iterable([combinations(range(size), size // 2)]):
            encoding_str += ":- " + ", ".join([f"a({s})" for s in subset]) + ".\n"
            results["minimal"].append([f"a({s})" for s in subset])

        with open(f"{path}{name}/encoding.lp", "w") as file:
            file.write(encoding_str)
        with open(f"{path}{name}/assumptions.lp", "w") as file:
            file.write(assumptions_str)
        with open(f"{path}{name}/results.txt", 'w') as file:
            file.write(json.dumps(results))

        print("FINISHED GENERATING")


class Test(ABC):
    @staticmethod
    @abstractmethod
    def check(test_data, valid_data) -> bool:
        pass


class TestAllContained(Test):
    @staticmethod
    def check(test_data, valid_data) -> bool:
        if test_data is None:
            return valid_data is None

        test_result_strings = [{str(a) for a in c} for c in test_data]

        return all([set(muc) in test_result_strings for muc in valid_data])


class TestAnyContained(Test):
    @staticmethod
    def check(test_data, valid_data) -> bool:
        if test_data is None:
            return valid_data is None
        if not valid_data:
            return not bool(test_data)

        valid_result_sets = [set(muc) for muc in valid_data]
        return set([str(a) for a in test_data]) in valid_result_sets


class Container:

    def __init__(self, example_directory):
        if not os.path.isdir(example_directory):
            raise ValueError("example_directory has to be a valid directory path")
        if not os.path.isfile(example_directory + "/assumptions.lp"):
            raise ValueError("example_directory has to contain an assumptions.lp file")
        if not os.path.isfile(example_directory + "/encoding.lp"):
            raise ValueError("example_directory has to contain an encoding.lp file")

        # read in the contents of assumptions.lp and encoding.lp (extras.lp) in example_directory
        file_contents = [
            Util.read_in_asp_file(example_directory + "/assumptions.lp", verbose=1),
            Util.read_in_asp_file(example_directory + "/encoding.lp", verbose=1),
        ]
        if os.path.isfile(example_directory + "/extras.lp"):
            file_contents.append(Util.read_in_asp_file(example_directory + "/extras.lp", verbose=1))
        program_string = "\n".join(file_contents)

        self.control = clingo.Control()
        self.program_string = program_string

        self.control.add("base", [], program_string)

        self.control.ground([("base", [])])

        self.assumptions = [
            a.symbol.arguments[0] for a in self.control.symbolic_atoms.by_signature(ASSUMPTION_SIGNATURE, 1)
        ]

        self.assumptions_lookup = {}
        if self.assumptions:
            self.assumptions_lookup = {
                self.control.symbolic_atoms[assumption].literal: assumption for assumption in self.assumptions
            }

    def solve(self, different_assumptions=None):
        if different_assumptions is not None:
            assumptions_prep = [(assumption, True) for assumption in different_assumptions]
        else:
            assumptions_prep = [(assumption, True) for assumption in self.assumptions]

        with self.control.solve(assumptions=assumptions_prep, yield_=True) as solve_handle:
            satisfiable = solve_handle.get().satisfiable
            if solve_handle.model() is not None:
                # filter out all atoms from the model that are not in shown_atoms
                model = [atom for atom in solve_handle.model().symbols(atoms=True) if
                         any([atom.match(signature, 3, True) for signature in SHOWN_SIGNATURES])]
            else:
                model = []
            core = [self.assumptions_lookup[index] for index in solve_handle.core()]
        return satisfiable, model, core

    def get_any_minimal_uc_assumption_marking(self):
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

    def get_all_uc_brute_force(self):
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

    def get_all_minimal_uc_brute_force(self):
        # This algorithm is used to solve task 2. It first uses the brute force algorithm to find all unsatisfiable
        # cores for the assumption set, and then checks if any found core is a superset of another (possibly minimal)
        # found core.

        unsatisfiable_cores = self.get_all_uc_brute_force()
        unsatisfiable_cores.sort(key=len)
        minimal_unsatisfiable_cores = []
        # iterate over every unsatisfiable core found by the brute force algorithm
        for core in [set(c) for c in unsatisfiable_cores]:
            subset_contained = False
            # for each unsatisfiable core, check if an already found minimal core is a subset
            for minimal_core in [set(c) for c in minimal_unsatisfiable_cores]:
                # break and not include core if any already found minimal core is a subset of the core
                if minimal_core.issubset(core):
                    subset_contained = True
                    break
            if not subset_contained:
                minimal_unsatisfiable_cores.append(core)
        return minimal_unsatisfiable_cores

    def get_all_minimum_uc_brute_force(self):
        # this algorithm just implements the brute force algorithm for all ucs (get_uc_all_brute_force()) and finds the
        # smallest core within the set of ucs that is returned

        unsatisfiable_cores = self.get_all_uc_brute_force()
        if unsatisfiable_cores:
            minimum = min(unsatisfiable_cores, key=lambda x: len(x))
            return [uc for uc in unsatisfiable_cores if len(uc) == len(minimum)]

        return []

    def get_all_minimal_uc_improved_brute_force(self):
        # This algorithm implements the brute force way of finding all minimal unsatisfiable cores of an assumption set
        # (unsatisfiable core). It iterates over the whole powerset of the assumptions and checks whether the current
        # set is an unsatisfiable core. If it is, it's stored in a list so that every future set that has an already
        # found core as a subset can be skipped.

        # powerset ordered by size ascending
        powerset = chain.from_iterable(combinations(self.assumptions, r) for r in range(len(self.assumptions) + 1))

        minimal_unsatisfiable_cores = []
        for assumption_set in powerset:
            # continue if the assumption_set has an already found minimal core as a subset
            if any([all([(a in assumption_set) for a in core]) for core in minimal_unsatisfiable_cores]):
                continue
            sat, _, _ = self.solve(different_assumptions=assumption_set)
            if not sat:
                minimal_unsatisfiable_cores.append(assumption_set)

        return minimal_unsatisfiable_cores

    def get_all_minimum_uc_improved_brute_force(self):
        # This algorithm implements an improved brute force way to solve the task 3. It iterates over the powerset of
        # the assumptions and checks whether the current set is an unsatisfiable core. Because the powerset is ordered
        # by subset-size, if any core is found it is automatically a minimal unsatisfiable core. When this happens the
        # size of the unsatisfiable core is stored, and only the remaining subsets of the same size are checked for
        # unsatisfiable cores. If this is finished, a list containing all minimum unsatisfiable cores is returned.

        powerset = chain.from_iterable(combinations(self.assumptions, r) for r in range(len(self.assumptions) + 1))

        minimum_unsatisfiable_cores = []
        current_minimum_core_size = np.inf
        for assumption_set in powerset:
            # break if the length of the assumption sets starts to be greater than the last found minimal core
            if len(assumption_set) > current_minimum_core_size:
                break
            sat, _, _ = self.solve(different_assumptions=assumption_set)
            if not sat:
                minimum_unsatisfiable_cores.append(assumption_set)
                current_minimum_core_size = len(assumption_set)

        return minimum_unsatisfiable_cores

    def get_any_minimum_uc_improved_brute_force(self):
        # This algorithm implements an improved brute force way to solve the task 6 and thereby also solves task 5.
        # The algorithm starts to iterate over the whole powerset of the multi unsatisfiable core, starting with the
        # smallest subsets ascending. When the first unsatisfiable core is found, the algorithm returns it, because by
        # definition, it has to be one of the minimum cores of the unsatisfiable core.

        powerset = chain.from_iterable(combinations(self.assumptions, r) for r in range(len(self.assumptions) + 1))

        for assumption_set in powerset:
            sat, _, _ = self.solve(different_assumptions=assumption_set)
            if not sat:
                return assumption_set

        return []

    def get_any_minimal_uc_iterative_deletion(self, different_assumptions=None):
        # This algorithm recycles the iterative deletion idea, and applies it now to try to solve task 5. We get an
        # unsatisfiable core as input, that is possibly a multi unsat core, and want to extract any minimal unsat core.
        # We now iteratively remove assumptions from the assumption set until it gets satisfiable. When it does that the
        # last removed assumption is added to the probe set which is always checked together with the assumption set.
        # We now restore the original assumption set, except for the just removed assumption, and start the process
        # again. When the assumption set is completely empty and a solver call yields still unsatisfiable, we have
        # reached the end and the probe set contains our found minimal unsat core.

        satisfiable, _, core = self.solve(different_assumptions=[])
        if not satisfiable:
            # raise error if the encoding instance isn't satisfiable without assumptions
            raise RuntimeError("The encoding for this container isn't satisfiable on it's own")

        satisfiable_with_empty_assumption_set = True

        # check if the encoding with all the assumptions is unsatisfiable
        if different_assumptions is None:
            satisfiable, _, core = self.solve()
        else:
            satisfiable, _, core = self.solve(different_assumptions=different_assumptions)

        if satisfiable:
            # return empty list if the encoding is already satisfiable with the assumptions
            return []

        # use container assumptions by default or different_assumptions
        assumption_set = different_assumptions if different_assumptions is not None else list(self.assumptions)
        probe_set = []

        while satisfiable_with_empty_assumption_set:
            for i in range(len(assumption_set)):
                working_set = assumption_set[i+1:]
                assumption = assumption_set[i]
                sat, _, _ = self.solve(different_assumptions=working_set + probe_set)
                if sat:
                    # if probe + assumption set become sat : add last removed assumption to probe set and remove from
                    # assumption set
                    probe_set.append(assumption)
                    assumption_set = [a for a in assumption_set if a != assumption]
                    break

            # end while loop if the encoding becomes unsatisfiable with the probe set
            if not self.solve(different_assumptions=probe_set)[0]:
                satisfiable_with_empty_assumption_set = False

        return probe_set

    def get_any_minimal_uc_iterative_deletion_improved(self, different_assumptions=None):
        # Just like the iterative deletion algorithm for task 5, but after a core member is found, this algorithm just
        # checks the remaining assumptions, and doesn't start from the beginning again
        # Based on orkunt's idea, to skip unnecessary solving steps

        satisfiable, _, core = self.solve(different_assumptions=[])
        if not satisfiable:
            # raise error if the encoding instance isn't satisfiable without assumptions
            raise RuntimeError("The encoding for this container isn't satisfiable on it's own")

        # check if the encoding with all the assumptions is unsatisfiable
        if different_assumptions is None:
            satisfiable, _, core = self.solve()
        else:
            satisfiable, _, core = self.solve(different_assumptions=different_assumptions)

        if satisfiable:
            # return empty list if the encoding is already satisfiable with the assumptions
            return []

        # use container assumptions by default or different_assumptions
        assumption_set = different_assumptions if different_assumptions is not None else list(self.assumptions)
        probe_set = []

        for i, assumption in enumerate(assumption_set):
            working_set = assumption_set[i+1:]
            sat, _, _ = self.solve(different_assumptions=working_set + probe_set)
            if sat:
                # if probe + assumption set become sat : add last removed assumption to probe set
                probe_set.append(assumption)

                # end for-loop if the encoding becomes unsatisfiable with the new probe set
                if not self.solve(different_assumptions=probe_set)[0]:
                    break

        return probe_set

    def get_all_minimal_uc_iterative_deletion(self, verbose=0):
        # This algorithm uses the iterative deletion algorithm for finding minimal unsatisfiable core to find all the
        # minimal unsatisfiable core inside a bigger unsatisfiable core. Right now the algorithm isn't performing very
        # good for big instance because the traversing of the search space just takes too long (even if most of it is
        # skipped).
        # It works like this :
        # We are checking all subsets of all possible sizes for the initial assumptions set, starting with the biggest
        # one descending. For each subset the iterative deletion algorithm is called an a minimal unsatisfiable core is
        # found. After such a core is found we store it and can from now on skipp all subsets which either are contained
        # inside the minimal core or contain the minimal core itself. The same happens when a satisfiable subset is
        # found. It is recorded but unlike for the MUC, only subsets of the satisfiable set can be skipped, not
        # supersets.

        satisfiable, _, core = self.solve(different_assumptions=[])
        if not satisfiable:
            # raise error if the encoding instance isn't satisfiable without assumptions
            raise RuntimeError("The encoding for this container isn't satisfiable on it's own")

        # check if the encoding with all the assumptions is unsatisfiable
        satisfiable, _, core = self.solve()
        if satisfiable:
            # return empty list if the encoding is already satisfiable with the assumptions
            return []

        # use container assumptions by default or different_assumptions
        assumption_set = list(self.assumptions)

        powerset = chain.from_iterable(combinations(assumption_set, r) for r in reversed(range(len(assumption_set) + 1)))
        minimal_cores = []
        satisfiable_subsets = []

        for subset in powerset:
            if any([core.issubset(subset) for core in minimal_cores]):
                if verbose > 0:
                    print("SKIPPED [UNSAT]:", [str(a) for a in subset])
                continue
            if any([set(subset).issubset(s) for s in satisfiable_subsets]):
                if verbose > 0:
                    print("SKIPPED [SAT]:", [str(a) for a in subset])
                continue

            if verbose > 0:
                print([str(a) for a in subset])
            any_muc = self.get_any_minimal_uc_iterative_deletion_improved(different_assumptions=list(subset))
            if not any_muc:
                satisfiable_subsets.append(subset)
                continue
            if any_muc not in minimal_cores:
                if verbose >= 0:
                    print("FOUND MUC :", [str(a) for a in any_muc])
                minimal_cores.append(set(any_muc))

        return minimal_cores

    def get_all_minimal_uc_iterative_deletion_stopping(self, verbose=0):
        # STOPPING AFTER FIRST LAYER WITH ONLY SKIPPABLE OR SAT SUBSETS IS CLEARED

        satisfiable, _, _ = self.solve(different_assumptions=[])
        if not satisfiable:
            # raise error if the encoding instance isn't satisfiable without assumptions
            raise RuntimeError("The encoding for this container isn't satisfiable on it's own")

        # check if the encoding with all the assumptions is unsatisfiable
        satisfiable, _, core = self.solve()
        if satisfiable:
            # return empty list if the encoding is already satisfiable with the assumptions
            return []

        assumption_set = list(self.assumptions)

        powerset = chain.from_iterable(combinations(assumption_set, r) for r in reversed(range(len(assumption_set) + 1)))
        minimal_cores = []
        satisfiable_subsets = []
        level = len(assumption_set)
        unsat_on_level = False

        for current_subset in powerset:
            subset = set(current_subset)
            if len(subset) < level:
                # BREAK : if the subsets become smaller than the current level and the current level had no unsat
                # subsets in it
                if not unsat_on_level:
                    break
                # RESET : level and found unsat subsets for each level
                else:
                    level = len(subset)
                    unsat_on_level = False

            # SKIP if muc in subset : exclude bigger subsets
            if any([core.issubset(subset) for core in minimal_cores]):
                if verbose > 0:
                    print("SKIPPED :", [str(a) for a in subset])
                continue
            # SKIP if subset in muc : exclude smaller subsets
            if any([subset.issubset(core) for core in minimal_cores]):
                if verbose > 0:
                    print("SKIPPED :", [str(a) for a in subset])
                continue
            # SKIP SAT : exclude smaller subsets of satisfiable subsets
            if any([subset.issubset(sat) for sat in satisfiable_subsets]):
                if verbose > 0:
                    print("SKIPPED :", [str(a) for a in subset])
                continue

            any_muc = self.get_any_minimal_uc_iterative_deletion_improved(different_assumptions=list(subset))
            if any_muc:
                unsat_on_level = True
                minimal_cores.append(set(any_muc))
                if verbose > 0:
                    print("FOUND MUC :", [str(a) for a in any_muc])
            else:
                satisfiable_subsets.append(subset)
                if verbose > 0:
                    print("FOUND SAT :", [str(a) for a in subset], "size :", len(subset))

        return minimal_cores

    def __str__(self):
        out = repr(self) + "\n"
        out += "\t<assumptions>\n"
        for index, assumption in self.assumptions_lookup.items():
            out += f"\t\t{index} : {assumption}\n"
        out += "\t</assumptions>\n"
        return out + f"</{self.__class__.__name__}>"

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
