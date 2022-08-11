import sys
import warnings

from clingo.application import Application, clingo_main, ApplicationOptions
from clingo import parse_term

ALGORITHMS = {
    0: None,  # TASK 1 : BRUTE FORCE
    1: None,  # TASK 2 : BRUTE FORCE
    2: None,  # TASK 3 : BRUTE FORCE
    3: None,  # TASK 2 : IMPROVED BRUTE FORCE
    4: None,  # TASK 3 : IMPROVED BRUTE FORCE
    5: None,  # TASK 5 : IMPROVED BRUTE FORCE
    6: None,  # TASK 4 : ASSUMPTION MARKING
    7: None,  # TASK 5 : ITERATIVE DELETION
}
# TODO : Select a default algorithm for if no argument or an invalid one is passed
STANDARD_ALGORITHM = ALGORITHMS.get(0)


class UCOREApp(Application):
    def __init__(self, name):
        self.program_name = name
        self.cores = []
        self.assumption_symbols = set([])
        self.algorithm = STANDARD_ALGORITHM

    def parse_assumption(self, assumption_str):
        self.assumption_symbols.add(parse_term(assumption_str))
        return True

    def select_algorithm(self, algorithm_str):
        algorithm = ALGORITHMS.get(algorithm_str)
        self.algorithm = algorithm if algorithm is not None else STANDARD_ALGORITHM
        if algorithm is None:
            warnings.warn(f"the algorithm ({algorithm_str}) you selected is not a valid option. Using the standard option")
        return True

    def register_options(self, options: ApplicationOptions) -> None:
        # TODO : What is the group used for
        group = 'Clingo.ucore'
        # here you can add other arguments like something that tells you what algorithm to use
        options.add(group, 'assumption', 'Provides an assumption', self.parse_assumption, multi=True)
        options.add(
            group,
            'algorithm',
            'Provides the algorithm that is used to minimize the unsatisfiable core',
            self.select_algorithm
        )

    def main(self, ctl, files):
        # Loads files passed in the command line
        # The file with all the assume predicates can also be passed in the command line
        for f in files:
            ctl.load(f)
        if not files:
            ctl.load("-")

        # Here you can call your api functions
        ctl.ground([("base", [])])

        # Here you can call your api functions
        ctl.ground([("base", [])])
        ctl.solve(assumptions=[(a, True) for a in self.assumption_symbols])

    # UNSATISFIABLE CORE ALGORITHMS


clingo_main(UCOREApp(sys.argv[0]), sys.argv[1:])

# You should now be able to do:
    # echo {a}. | python ucore_app.py --assumption=a 0

# Or something where you pass the files to clingo
# python ucore_app.py file1 file2 --assumption=a

