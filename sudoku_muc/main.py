import clingo
from minimal_unsatisfiable_core import Util, MUCSimple


if __name__ == '__main__':
    print('SUDOKU - MINIMAL UNSATISFIABLE CORE TEST')

    ctl = clingo.Control()

    # program_string = Util.get_file_content_str('res/sudoku_solver.lp')

    program_string = Util.get_file_content_str('res/sudoku_only_rules.lp')
    instance_string = Util.get_file_content_str('res/instances/sudoku_instance_1.lp')
    visualization_string = Util.get_file_content_str('res/visualization/visualize_sudoku.lp')

    muc = MUCSimple()

    ctl.add("base", [], f"{program_string}\n{instance_string}\n{visualization_string}")
    ctl.ground([("base", [])])
    assumption_list = [
        # adding the assumption of : solution(2,2,7) [SAT] or solution(2,2,5) [UNSAT]
        # (clingo.Function("solution", [clingo.Number(2), clingo.Number(2), clingo.Number(7)]), True),
        # (clingo.Function("solution", [clingo.Number(7), clingo.Number(1), clingo.Number(9)]), True),
        # (clingo.Function("solution", [clingo.Number(4), clingo.Number(9), clingo.Number(3)]), True),
    ]
    solve_handle = ctl.solve(assumptions=assumption_list, yield_=True)
    print(solve_handle)
    print("result : ", solve_handle.get())  # blocking until the result is ready
    print("model : ", solve_handle.model())
    print("core : ", solve_handle.core(), " = ", [assumption_list[i] for i in solve_handle.core()])

    # TODO : get the clingraph visualization to work
    # TODO : - this command shows still wrong numbers at the moment
    # TODO : - command line command :
    #  clingo instances/sudoku_instance_1.lp sudoku_solver.lp -n 0 --outf=2 |
    #  clingraph --view --dir='out/sudoku' --format=png --out=render --prefix=viz_ --engine=neato --default-graph=sudoku
    #  --viz-encoding=visualization/visualize_sudoku.lp --name-format=model_{model_number}

    # TODO : implement the clingraph visualization directly into the script

    # TODO : find why it returns UNSAT when I use any assumptions for not yet filled cells

