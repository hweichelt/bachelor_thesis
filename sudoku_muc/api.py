import signal
import clingo

from typing import Callable

"""
    from xclingo.ucore import CoreComputer
    assumptions,file = file_to_assumptions("instance.lp")
    initial/3 -> assume
    _assume(X):-X.
    c = CoreCompuer(["encoding"],ctl,my_assumptions)
    c.compute_muc(all=True)
"""

# TYPE-ALIASES
UnsatisfiableCore = set[clingo.Symbol]
UnsatisfiableCoreSet = set[UnsatisfiableCore]

# TODO : I used clingo.Symbol which should include Function etc.?? Is this correct?
# TODO : Is there a way in the clingo api to directly load a files content to the control?
#           Because of the scripts location that will be different from the read in files, include dependencies will not
#           be able to be resolved correctly. To avoid this a clingo functionality would be nice or I could also use my
#           already implemented version, which recursively loads all included files (isn't super nice).
# TODO : Check if CoreComputer assumptions only works with sets or also with lists that could contain copies
# TODO : Is it good style to set the type hind of a parameter to for example int and then its default value to None?


class TimeoutException(Exception):
    def __init__(self, message, errors):
        super(TimeoutException, self).__init__(message)
        self.errors = errors


class Util:

    @staticmethod
    def timeout_handler(signum, frame):
        raise TimeoutException("Out of time!")

    @staticmethod
    def function_with_timeout(function: Callable, args: list = None, kwargs: dict = None, timeout: int = None):
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
        except TimeoutException:
            # return None if a timeout occurred
            return None


class CoreComputer:

    def __init__(self, encoding_paths: list[str], assumptions: set[clingo.Symbol], custom_control: clingo.Control = None):
        # Set up the clingo Control object
        self.control = clingo.Control()
        if custom_control is not None:
            self.control = custom_control

        # Read in the encoding files and add them to the clingo Control object

        self.control.add("base", [], _________________)  # TODO : What is the best way to include external files here?

        # Ground the clingo Control object
        self.control.ground([("base", [])])

        # Set up the assumption set
        self.assumptions = assumptions
        self.assumptions_lookup = {self.control.symbolic_atoms[a].literal: a for a in self.assumptions}

    def compute_minimal(self, multiple: bool = False, amount: int = None, timeout: int = None) -> UnsatisfiableCoreSet:
        # select the correct function depending on if the user wants multiple mucs or just one
        function = (self._compute_any_minimal_core, self._compute_multiple_minimal_cores)[multiple]
        # select the correct args and kwargs depending on the selected function
        args = []
        kwargs = {}
        if multiple:
            kwargs["amount"] = amount

        result = Util.function_with_timeout(
            function=function,
            args=args,
            kwargs=kwargs,
            timeout=timeout
        )

        if result is None:
            pass
            # TODO : Here raise an Exception or return None just make it clear that None means that something didn't go
            #  the right way

        if multiple:
            return result
        else:
            # if only one minimal unsatisfiable core is wanted return a set containing only this one core. This is done
            # to maintain a uniform output format
            return {result}

    # This method uses the iterative deletion approach to find any minimal unsatisfiable core of an
    # assumption set. This is a 'private' method, which should be called using the `compute_minimal` method.
    def _compute_any_minimal_core(self) -> UnsatisfiableCore:
        pass

    # This method is used to find multiple minimal unsatisfiable cores inside an assumption set. It uses the iterative
    # deletion method to find minimal cores by looking at all the possible subsets of the assumption set. Subsets that
    # either contain an already found minimal core or are themselves contained inside a minimal core are skipped.
    # This is a 'private' method, which should be called using the `compute_minimal` method.
    def _compute_multiple_minimal_cores(self, amount: int = None) -> UnsatisfiableCoreSet:
        pass
