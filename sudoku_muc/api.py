import signal
import time

import clingo

from typing import Callable
from itertools import chain, combinations
from warnings import warn

"""
    from xclingo.ucore import CoreComputer
    assumptions,file = file_to_assumptions("instance.lp")
    initial/3 -> assume
    _assume(X):-X.
    c = CoreComputer(["encoding"],ctl,my_assumptions)
    c.compute_muc(all=True)
"""

# TYPE-ALIASES
UnsatisfiableCore = set[clingo.Symbol]
UnsatisfiableCoreCollection = list[UnsatisfiableCore]

# TODO : Nice to haves :
#  + Assume all literals of a certain signature (list of signatures) [ ]
#   + Could be achieved through a first grounding step and then taking all grounded symbols of the signature and adding
#     Them as choice rules
#  + Just assume given assumptions an nothing else (already implemented) [X]


class EncodingUnsatisfiableException(Exception):
    def __init__(self, message):
        super(EncodingUnsatisfiableException, self).__init__(message)


class AssumptionsSatisfiableException(Exception):
    def __init__(self, message):
        super(AssumptionsSatisfiableException, self).__init__(message)


class Util:

    @staticmethod
    def timeout_handler(signum, frame):
        raise TimeoutError("took too long!")

    @staticmethod
    def function_with_timeout(function: Callable, args: list = None, kwargs: dict = None, timeout: int = None):
        if timeout is not None:
            signal.signal(signal.SIGALRM, Util.timeout_handler)

        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        if timeout is not None and timeout <= 0:
            raise ValueError("`timeout` has to be a positive number that is greater than 0")

        # start countdown for timeout
        if timeout is not None:
            signal.alarm(timeout)
        try:
            result = function(*args, **kwargs)
            # if a timeout is set, end it after the function finished
            if timeout is not None:
                signal.alarm(0)
            return result
        except:
            print("TimeoutError was caught")
            # return None if a timeout occurred
            return None


class CoreComputer:

    def __init__(self, encoding_paths: list[str], assumptions: set[(clingo.Symbol, bool)], custom_control: clingo.Control = None):
        # Set up the clingo Control object
        self.control = clingo.Control()
        if custom_control is not None:
            self.control = custom_control

        # Read in the encoding files and add them to the clingo Control object
        for file in encoding_paths:
            self.control.load(file)

        # Ground the clingo Control object
        self.control.ground([("base", [])])

        # Set up the assumption set
        self.assumptions = assumptions
        self.assumptions_lookup = {self.control.symbolic_atoms[a[0]].literal: a[0] for a in self.assumptions}

    def compute_minimal(self, multiple: bool = False, max_amount: int = None, timeout: int = None) -> UnsatisfiableCoreCollection:
        # check that the encoding is satisfiable by itself (without any assumptions) else raise error
        satisfiable, _, core = self._solve(_different_assumptions=set())
        if not satisfiable:
            # raise error if the encoding instance isn't satisfiable without assumptions
            raise EncodingUnsatisfiableException("The encoding isn't satisfiable on it's own")

        # check that the encoding with all assumptions is unsatisfiable else return empty set of mucs
        satisfiable, _, core = self._solve()
        if satisfiable:
            return []

        # select the correct function depending on if the user wants multiple mucs or just one
        function = (self._compute_any_minimal_core, self._compute_multiple_minimal_cores)[multiple]
        # select the correct args and kwargs depending on the selected function
        args = []
        kwargs = {}
        if multiple:
            kwargs["max_amount"] = max_amount
            kwargs["result_backup"] = []

        result = Util.function_with_timeout(
            function=function,
            args=args,
            kwargs=kwargs,
            timeout=timeout
        )

        if result is None:
            partial_result = kwargs["result_backup"] if "result_backup" in kwargs else None
            warn("The timeout limit was reached and the search stopped. A partial result will be returned")
            return partial_result

        if multiple:
            return result
        else:
            # if only one minimal unsatisfiable core is wanted return a set containing only this one core. This is done
            # to maintain a uniform output format
            return [result]

    # This method is used to solve the clingo control object with either the default assumptions or
    # `_different_assumptions` when defined.
    def _solve(self, _different_assumptions: set[(clingo.Symbol, bool)] = None) -> (bool, list, list):
        assumption_list = list(_different_assumptions) if _different_assumptions is not None else list(self.assumptions)
        with self.control.solve(assumptions=assumption_list, yield_=True) as solve_handle:
            satisfiable = solve_handle.get().satisfiable
            if solve_handle.model() is not None:
                model = solve_handle.model().symbols(atoms=True)
            else:
                model = []
            core = [self.assumptions_lookup[index] for index in solve_handle.core()]
        return satisfiable, model, core

    # This method uses the iterative deletion approach to find any minimal unsatisfiable core of an
    # assumption set. This is a 'private' method, which should be called using the `compute_minimal` method.
    def _compute_any_minimal_core(self, _different_assumptions: set[(clingo.Symbol, bool)] = None) -> UnsatisfiableCore:
        # IMPROVED ITERATIVE DELETION ALGORITHM
        # check for `different_assumptions` if the encoding is unsatisfiable, else return None
        if _different_assumptions is not None:
            satisfiable, _, core = self._solve(_different_assumptions=_different_assumptions)
            if satisfiable:
                raise AssumptionsSatisfiableException("The encoding with `_different_assumptions` isn't unsatisfiable")

        # use object assumptions by default or `_different_assumptions`
        assumption_set = _different_assumptions if _different_assumptions is not None else self.assumptions
        working_set = set(assumption_set)
        probe_set = set()

        for i, assumption in enumerate(assumption_set):
            working_set.remove(assumption)
            sat, _, _ = self._solve(_different_assumptions=working_set.union(probe_set))
            if sat:
                # if the probe set united with the assumption set becomes sat : add last removed assumption to probe set
                probe_set.add(assumption)

                # end for-loop if the encoding becomes unsatisfiable with the new probe set
                if not self._solve(_different_assumptions=probe_set)[0]:
                    break

        return probe_set

    # This method is used to find multiple minimal unsatisfiable cores inside an assumption set. It uses the iterative
    # deletion method to find minimal cores by looking at all the possible subsets of the assumption set. Subsets that
    # either contain an already found minimal core or are themselves contained inside a minimal core are skipped.
    # This is a 'private' method, which should be called using the `compute_minimal` method.
    def _compute_multiple_minimal_cores(self, max_amount: int = None, result_backup: list[set[clingo.Symbol]] = None) -> UnsatisfiableCoreCollection:
        # ITERATIVE DELETION BASED MULTI MUC ALGORITHM
        assumption_set = set(self.assumptions)
        # preparing the search space of subsets of the assumption set bottom up
        search_space = chain.from_iterable(combinations(assumption_set, r) for r in reversed(range(len(assumption_set) + 1)))
        minimal_cores = []
        satisfiable_subsets = []

        for s in search_space:
            subset = set(s)
            # SKIP subsets and supersets of already found MUCs
            if any([muc.issubset(subset) or muc.issuperset(subset) for muc in minimal_cores]):
                continue
            # SKIP subsets of already found satisfiable subsets
            if any([sat.issuperset(subset) for sat in satisfiable_subsets]):
                continue

            try:
                any_muc = self._compute_any_minimal_core(_different_assumptions=subset)
                if any_muc not in minimal_cores:
                    minimal_cores.append(any_muc)
                    # also append newly found MUC to `result_backup` list to keep info in case of timeout
                    if result_backup is not None:
                        result_backup.append(any_muc)
                    # BREAK if the wanted amount of minimal cores is reached
                    if max_amount is not None and max_amount == len(minimal_cores):
                        break
            except AssumptionsSatisfiableException:
                satisfiable_subsets.append(subset)
                continue

        return minimal_cores

# ----------------------------------------------------------------------------------------------------------------------


class CoreComputerBruteForce(CoreComputer):

    def __int__(self, encoding_paths: list[str], assumptions: set[(clingo.Symbol, bool)], custom_control: clingo.Control = None):
        super(CoreComputerBruteForce, self).__init__(encoding_paths, assumptions, custom_control)

    def _compute_any_minimal_core(self, _different_assumptions: set[(clingo.Symbol, bool)] = None) -> UnsatisfiableCore:
        # BRUTE FORCE ANY MUC ALGORITHM
        # check for `different_assumptions` if the encoding is unsatisfiable, else return None
        if _different_assumptions is not None:
            satisfiable, _, core = self._solve(_different_assumptions=_different_assumptions)
            if satisfiable:
                raise AssumptionsSatisfiableException("The encoding with `_different_assumptions` isn't unsatisfiable")

        # use object assumptions by default or `_different_assumptions`
        assumption_set = _different_assumptions if _different_assumptions is not None else self.assumptions
        powerset = chain.from_iterable(combinations(assumption_set, r) for r in range(len(assumption_set) + 1))

        for s in powerset:
            subset = set(s)
            sat, _, _ = self._solve(_different_assumptions=subset)
            if not sat:
                # this has to be the case at some point (at least when checking the whole assumption set in the end)
                return subset

    def _compute_multiple_minimal_cores(self, max_amount: int = None, result_backup: list[set[clingo.Symbol]] = None) -> UnsatisfiableCoreCollection:
        # BRUTE FORCE ALL MUC ALGORITHM
        # use object assumptions
        assumption_set = self.assumptions
        minimal_unsatisfiable_cores = []
        powerset = chain.from_iterable(combinations(assumption_set, r) for r in range(len(assumption_set) + 1))

        curr_len = 0
        for s in powerset:
            subset = set(s)
            if len(subset) > curr_len:
                curr_len = len(subset)
                print(curr_len)
            sat, _, _ = self._solve(_different_assumptions=subset)
            if not sat and not any([muc.issubset(subset) for muc in minimal_unsatisfiable_cores]):
                minimal_unsatisfiable_cores.append(subset)
                result_backup.append(subset)

        return minimal_unsatisfiable_cores


class CoreComputerBruteForceImproved(CoreComputer):

    def __int__(self, encoding_paths: list[str], assumptions: set[(clingo.Symbol, bool)], custom_control: clingo.Control = None):
        super(CoreComputerBruteForceImproved, self).__init__(encoding_paths, assumptions, custom_control)

    def _compute_any_minimal_core(self, _different_assumptions: set[(clingo.Symbol, bool)] = None) -> UnsatisfiableCore:
        # BRUTE FORCE ANY MUC ALGORITHM
        # check for `different_assumptions` if the encoding is unsatisfiable, else return None
        if _different_assumptions is not None:
            satisfiable, _, core = self._solve(_different_assumptions=_different_assumptions)
            if satisfiable:
                raise AssumptionsSatisfiableException("The encoding with `_different_assumptions` isn't unsatisfiable")

        # use object assumptions by default or `_different_assumptions`
        assumption_set = _different_assumptions if _different_assumptions is not None else self.assumptions
        powerset = chain.from_iterable(combinations(assumption_set, r) for r in range(len(assumption_set) + 1))

        for s in powerset:
            subset = set(s)
            sat, _, _ = self._solve(_different_assumptions=subset)
            if not sat:
                # this has to be the case at some point (at least when checking the whole assumption set in the end)
                return subset

    def _compute_multiple_minimal_cores(self, max_amount: int = None, result_backup: list[set[clingo.Symbol]] = None) -> UnsatisfiableCoreCollection:
        # IMPROVED BRUTE FORCE ALL MUC ALGORITHM
        # use object assumptions
        assumption_set = self.assumptions
        minimal_unsatisfiable_cores = []
        powerset = chain.from_iterable(combinations(assumption_set, r) for r in range(len(assumption_set) + 1))

        curr_len = 0
        for s in powerset:
            subset = set(s)
            if any([muc.issubset(subset) for muc in minimal_unsatisfiable_cores]):
                continue
            if len(subset) > curr_len:
                curr_len = len(subset)
                print(curr_len)
            sat, _, _ = self._solve(_different_assumptions=subset)
            if not sat and not any([muc.issubset(subset) for muc in minimal_unsatisfiable_cores]):
                minimal_unsatisfiable_cores.append(subset)
                result_backup.append(subset)

        return minimal_unsatisfiable_cores
