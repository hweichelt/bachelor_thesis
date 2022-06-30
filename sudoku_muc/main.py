import clingo
from minimal_unsatisfiable_core import Util, Container


def muc_sudoku():

    assumption_list = [
        # adding assumptions
        # CORRECT ASSUMPTIONS
        "solution(4,9,1)",
        "solution(7,1,9)",
        "solution(2,2,7)",
        "solution(4,7,7)",
        "solution(3,9,7)",
        "solution(8,2,8)",
        "solution(1,6,8)",
        "solution(6,7,8)",
        "solution(2,9,8)",
        # CONFLICTING ASSUMPTIONS
        # double value for cell
        "solution(4,9,5)",
        # value at the wrong position in cage (double 7 in cage(1,1))
        "solution(1,3,7)",
    ]

    assumption_list = [clingo.parse_term(string) for string in assumption_list]

    program = "res/sudoku_only_rules.lp"
    instance = "res/instances/sudoku_instance_1.lp"
    visualization = "res/visualization/visualize_sudoku.lp"

    program_string = "\n".join([Util.get_file_content_str(program), Util.get_file_content_str(instance)])

    container_1 = Container(
        program_string=program_string,
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

    print("FIND MUC ON CORE : ASSUMPTION MARKING")
    muc_found, muc = container_1.get_muc_on_core_assumption_marking()

    if not muc_found:
        print("MUC : Problem wasn't unsatisfiable to begin with, there is no minimal unsatisfiable core")
    else:
        print(f"MUC : {muc}")

    print("FIND ALL UCS : BRUTE FORCE APPROACH")

    ucs = container_1.get_uc_all_brute_force()
    print("Cores Found (Cores/|Assumption-Powerset|):", len(ucs), "/", 2**len(container_1.assumptions))


if __name__ == '__main__':
    # example_clingraph()
    muc_sudoku()
    # clingraph_factbase_computation()

