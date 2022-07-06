import clingo
from minimal_unsatisfiable_core import Util, Container


def muc_sudoku():

    assumptions_valid = [
        "solution(4,9,3)",
        "solution(7,1,9)",
        "solution(2,2,7)",
        "solution(4,7,7)",
        "solution(3,9,7)",
        "solution(8,2,8)",
        "solution(1,6,8)",
        "solution(6,7,8)",
        "solution(2,9,8)",
    ]

    assumptions_unsat_atomic = [
        "solution(5,5,7)"
    ] + assumptions_valid

    assumptions_unsat_multi_atomic = [
        "solution(5,5,7)",
        "solution(1,7,6)",
        "solution(9,1,7)",
    ] + assumptions_valid

    assumptions_unsat_multi_internal = [
        "solution(2,7,4)",
        "solution(9,7,4)",
    ] + assumptions_valid

    assumptions_unsat_multi_combined = [

    ] + assumptions_valid + assumptions_unsat_multi_atomic + assumptions_unsat_multi_internal

    assumption_lists = {
        'valid': assumptions_valid,
        'atomic': assumptions_unsat_atomic,
        "multi_atomic": assumptions_unsat_multi_atomic,
        "multi_internal": assumptions_unsat_multi_internal,
        "multi_combined": assumptions_unsat_multi_combined
    }

    for key, assumption_string_list in assumption_lists.items():
        assumption_lists[key] = [clingo.parse_term(string) for string in assumption_string_list]

    program = "res/sudoku_only_rules.lp"
    instance = "res/instances/sudoku_instance_1.lp"
    visualization = "res/visualization/visualize_sudoku.lp"

    program_string = "\n".join([Util.get_file_content_str(program), Util.get_file_content_str(instance)])

    container_1 = Container(
        program_string=program_string,
        assumptions=assumption_lists["multi_combined"],
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

    return

    print("FIND ALL UCS : BRUTE FORCE APPROACH")

    ucs = container_1.get_uc_all_brute_force()
    print("Cores Found (Cores/|Assumption-Powerset|):", len(ucs), "/", 2**len(container_1.assumptions))
    minimum_ucs = container_1.get_minimum_ucs_brute_force()
    print("Minimum UCs Found: ", minimum_ucs)


if __name__ == '__main__':
    # example_clingraph()
    muc_sudoku()
    # clingraph_factbase_computation()

