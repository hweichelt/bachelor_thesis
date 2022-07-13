import clingo
from minimal_unsatisfiable_core import Util, Container


def muc_sudoku():

    example_directory = "res/examples/sudoku/sudoku_multi_atomic"
    visualization = "res/visualization/visualize_sudoku.lp"

    container_1 = Container(
        example_directory=example_directory
    )

    print([container_1])
    print(container_1)

    satisfiable, model, core = container_1.solve()
    print("result : ", ["UNSAT", "SAT"][satisfiable])
    print("model : ", model)
    print("core : ", core)

    if satisfiable:
        Util.render_sudoku(model, visualization)

    print("FIND MUC ON CORE : ASSUMPTION MARKING")
    muc_found, muc = container_1.get_muc_on_core_assumption_marking()

    if not muc_found:
        print("MUC : Problem wasn't unsatisfiable to begin with, there is no minimal unsatisfiable core")
    else:
        print(f"MUC : {muc}")

    return

    print("FIND UC ON ASSUMPTION SET : ITERATIVE DELETION")

    uc = container_1.get_uc_iterative_deletion()
    if uc:
        print("UC: ", [str(a) for a in uc])
    else:
        print("No UC was found")

    mucs = container_1.get_muc_all_iterative_deletion()
    if mucs:
        print("MUCs: \n", "\n".join(["\t+ " + " ".join([str(a) for a in core]) for core in mucs]))
    else:
        print("No MUCs were found")

    print("FIND ALL UCS : BRUTE FORCE APPROACH")

    ucs = container_1.get_uc_all_brute_force()
    print("Cores Found (Cores/|Assumption-Powerset|):", len(ucs), "/", 2**len(container_1.assumptions))
    minimum_ucs = container_1.get_minimum_ucs_brute_force()
    print("Minimum UCs Found: ", minimum_ucs)


if __name__ == '__main__':
    # example_clingraph()
    muc_sudoku()
    # clingraph_factbase_computation()

