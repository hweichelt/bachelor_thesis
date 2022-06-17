import clingo
import minimal_unsatisfiable_core


def on_model(m):
    print("GOT MODEL")
    print(m)


def on_core(c):
    print("GOT UNSAT CORE")
    print(type(c), c)


def get_file_content_str(filename):
    with open(f"{filename}") as f:
        out = f.read()
    return out


if __name__ == '__main__':
    print('SUDOKU - MINIMAL UNSATISFIABLE CORE')

    ctl = clingo.Control()

    # program_string = get_file_content_str('res/sudoku_only_rules.lp')
    program_string = get_file_content_str('res/sudoku_solver.lp')
    instance_string = get_file_content_str('res/instances/sudoku_instance_1.lp')

    ctl.add("base", [], f"{program_string}\n{instance_string}")
    ctl.ground([("base", [])])
    assumption_list = [
        # adding the assumtion of : solution(2,2,7) [SAT] or solution(2,2,5) [UNSAT]
        (clingo.Function("solution", [clingo.Number(2), clingo.Number(2), clingo.Number(7)]), True),
    ]
    ctl.solve(assumptions=assumption_list, on_model=on_model, on_core=on_core)
    # ctl.solve(on_model=on_model, on_core=on_core)


