import sys
from clingo.application import Application, clingo_main, ApplicationOptions
from clingo import parse_term


class UCOREApp(Application):
    def __init__(self, name):
        self.program_name = name
        self.cores = []
        self.assumption_symbols = set([])

    def parse_assumption(self, assumption_str):
        self.assumption_symbols.add(parse_term(assumption_str))
        return True

    def register_options(self, options: ApplicationOptions) -> None:
        group = 'Clingo.ucore'
        # here you can add other arguments like something that tells you what algorithm to use
        options.add(group, 'assumption', 'Provides an assumption', self.parse_assumption, multi=True)

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


clingo_main(UCOREApp(sys.argv[0]), sys.argv[1:])

# You should now be able to do:
# echo {a}. | python ucore_app.py --assumption=a 0

# Or something where you pass the files to clingo
# python ucore_app.py file1 file2 --assumption=a
