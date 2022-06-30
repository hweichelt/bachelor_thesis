import clingo
from minimal_unsatisfiable_core import Util, Container


def muc_sudoku():

    assumption_list = [
        # adding assumptions
        # CORRECT ASSUMPTIONS
        clingo.Function("guess", [clingo.Number(4), clingo.Number(9), clingo.Number(3)]),
        clingo.Function("guess", [clingo.Number(7), clingo.Number(1), clingo.Number(9)]),
        clingo.Function("guess", [clingo.Number(2), clingo.Number(2), clingo.Number(7)]),
        clingo.Function("guess", [clingo.Number(5), clingo.Number(7), clingo.Number(7)]),
        clingo.Function("guess", [clingo.Number(3), clingo.Number(9), clingo.Number(7)]),
        clingo.Function("guess", [clingo.Number(8), clingo.Number(2), clingo.Number(8)]),
        clingo.Function("guess", [clingo.Number(1), clingo.Number(6), clingo.Number(8)]),
        clingo.Function("guess", [clingo.Number(6), clingo.Number(7), clingo.Number(8)]),
        clingo.Function("guess", [clingo.Number(2), clingo.Number(9), clingo.Number(8)]),
        # CONFLICTING ASSUMPTIONS
        # double value for cell
        clingo.Function("guess", [clingo.Number(4), clingo.Number(9), clingo.Number(5)]),
        # value at the wrong position in cage (double 7 in cage(1,1))
        clingo.Function("guess", [clingo.Number(1), clingo.Number(3), clingo.Number(7)]),
    ]

    program = "res/sudoku_only_rules.lp"
    instance = "res/instances/sudoku_instance_1.lp"
    visualization = "res/visualization/visualize_sudoku.lp"

    container_1 = Container(
        program=program,
        instance=instance,
        assumptions=assumption_list,
    )

    print([container_1])
    print(container_1)

    satisfiable, model, core = container_1.solve()
    print("result : ", ["UNSAT", "SAT"][satisfiable])
    print("model : ", model)
    print("core : ", core)

    if satisfiable:
        Util.render_sudoku(model, visualization)

    muc_found, muc = container_1.get_muc_iterative_deletion()

    if not muc_found:
        print("MUC : Problem wasn't unsatisfiable to begin with, there is no minimal unsatisfiable core")
    else:
        print(f"MUC : {muc}")

    print("UC ALL : BRUTE FORCE APPROACH")

    ucs = container_1.get_uc_all_brute_force()
    print("Cores Found (Cores/|Assumption-Powerset|):", len(ucs), "/", 2**len(container_1.assumptions))


if __name__ == '__main__':
    # example_clingraph()
    muc_sudoku()
    # clingraph_factbase_computation()

