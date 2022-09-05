import json
import os.path
from itertools import combinations, chain

import signal
from minimal_unsatisfiable_core import Util, Container, Test, TestAllContained, TestAnyContained

TIMEOUT = 10


def muc_sudoku():
    single_example = [
        "res/examples/abstract_multi_core_big"
    ]
    abstract_examples = [
        "res/examples/abstract_multi_sat",
        "res/examples/abstract_multi_core_medium",
        "res/examples/abstract_multi_core_intersecting",
        "res/examples/abstract_multi_core_big"
    ]
    sudoku_examples = [
        "res/examples/sudoku/sudoku_valid",
        "res/examples/sudoku/sudoku_atomic",
        "res/examples/sudoku/sudoku_internal",
        "res/examples/sudoku/sudoku_multi_atomic",
        "res/examples/sudoku/sudoku_multi_combined",
    ]
    all_examples = abstract_examples + sudoku_examples

    for example in single_example:
        print("\n" + "="*40, ">", example, "<", "="*40, "\n")
        muc_sudoku_on_example(example)


def print_test_results(function, valid_data, test: Test, name=None):
    if name is None:
        name = function.__name__
    runtime, result = Util.measure_function(function, timeout=TIMEOUT)
    print(f"[time={'{:.5f}'.format(runtime)}s]", name,
          [[str(a) for a in muc] for muc in result] if runtime != -1 else "TIMEOUT")
    print("-" * 14 + ">", ("INVALID", "VALID")[test.check(result, valid_data)])


def muc_sudoku_on_example(example_directory):

    visualization = "res/visualization/visualize_sudoku_core.lp"
    render_sudoku = False

    container_1 = Container(
        example_directory=example_directory
    )

    print([container_1])
    # print(container_1)

    satisfiable, model, core = container_1.solve()
    print("result : ", ["UNSAT", "SAT"][satisfiable])
    print("model : ", model)
    print("core : ", core)

    results = Util.read_dictionary_from_file(f"{example_directory}/results.txt")

    # -----------

    print(container_1.assumptions[:4])
    muc = container_1.get_any_minimal_uc_iterative_deletion_improved(different_assumptions=[a for a in container_1.assumptions if str(a) != "c"])
    print([str(a) for a in muc])

    # -----------

    print("\n=====> BENCHMARK ALGORITHM PERFORMANCE <=====")

    signal.signal(signal.SIGALRM, Util.timeout_handler)

    # not_vs_without()

    # print("\n===> TASK T1 )")
    #
    # runtime, result = measure_function(container_1.get_all_uc_brute_force, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Brute Force): ",
    #       f"{len(result)} cores" if runtime != -1 else "TIMEOUT")

    print("\n===> TASK T2 )")

    # runtime, result = measure_function(container_1.get_all_minimal_uc_brute_force, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Brute Force): ",
    #       [[str(a) for a in muc] for muc in result] if runtime != -1 else "TIMEOUT")
    # print("-"*14 + ">", ("INVALID", "VALID")[check_result_all(result, results.get("minimal"))])
    #
    # runtime, result = measure_function(container_1.get_all_minimal_uc_improved_brute_force, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Improved Brute Force): ",
    #       [[str(a) for a in muc] for muc in result] if runtime != -1 else "TIMEOUT")
    # print("-" * 14 + ">", ("INVALID", "VALID")[check_result_all(result, results.get("minimal"))])
    #
    # runtime, result = measure_function(container_1.get_all_minimal_uc_iterative_deletion, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Iterative Deletion): ",
    #       [[str(a) for a in muc] for muc in result] if runtime != -1 else "TIMEOUT")
    # print("-" * 14 + ">", ("INVALID", "VALID")[check_result_all(result, results.get("minimal"))])
    #
    # runtime, result = measure_function(container_1.get_all_minimal_uc_iterative_deletion_approach_2, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Iterative Deletion 2): ",
    #       [[str(a) for a in muc] for muc in result] if runtime != -1 else "TIMEOUT")
    # print("-" * 14 + ">", ("INVALID", "VALID")[check_result_all(result, results.get("minimal"))])
    #
    # runtime, result = measure_function(container_1.get_all_minimal_uc_iterative_deletion_approach_3, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Iterative Deletion 3): ",
    #       [[str(a) for a in muc] for muc in result] if runtime != -1 else "TIMEOUT")
    # print("-" * 14 + ">", ("INVALID", "VALID")[check_result_all(result, results.get("minimal"))])

    # runtime, result = Util.measure_function(container_1.get_all_minimal_uc_iterative_deletion_approach_4, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Iterative Deletion 4): ",
    #       [[str(a) for a in muc] for muc in result] if runtime != -1 else "TIMEOUT")
    # print("-" * 14 + ">", ("INVALID", "VALID")[Util.check_result_all(result, results.get("minimal"))])

    print_test_results(
        function=container_1.get_all_minimal_uc_iterative_deletion,
        valid_data=results.get("minimal"),
        test=TestAllContained(),
        name="ALL MINIMAL UCS (Iterative Deletion 3):"
    )

    print_test_results(
        function=container_1.get_all_minimal_uc_iterative_deletion_stopping,
        valid_data=results.get("minimal"),
        test=TestAllContained(),
        name="ALL MINIMAL UCS (Iterative Deletion 4):"
    )

    # runtime, result = Util.measure_function(container_1.get_all_minimal_uc_iterative_deletion_approach_5, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Iterative Deletion 5): ",
    #       [[str(a) for a in muc] for muc in result] if runtime != -1 else "TIMEOUT")
    # print("-" * 14 + ">", ("INVALID", "VALID")[Util.check_result_all(result, results.get("minimal"))])

    # print("\n===> TASK T3 )")
    #
    # runtime, result = measure_function(container_1.get_all_minimum_uc_brute_force, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMUM UCS (Brute Force): ",
    #       [[str(a) for a in muc] for muc in result] if runtime != -1 else "TIMEOUT")
    # print("-" * 14 + ">", ("INVALID", "VALID")[check_result_all(result, results.get("minimum"))])
    #
    # runtime, result = measure_function(container_1.get_all_minimum_uc_improved_brute_force, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMUM UCS (Improved Brute Force): ",
    #       [[str(a) for a in muc] for muc in result] if runtime != -1 else "TIMEOUT")
    # print("-" * 14 + ">", ("INVALID", "VALID")[check_result_all(result, results.get("minimum"))])
    #
    # print("\n===> TASK T5 )")
    #
    # runtime, result = measure_function(container_1.get_any_minimum_uc_improved_brute_force, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ANY MINIMUM UCS (Improved Brute Force): ",
    #       [str(a) for a in result] if runtime != -1 else "TIMEOUT")
    # print("-" * 14 + ">", ("INVALID", "VALID")[check_result_any(result, results.get("minimal"))])
    #
    # runtime, result = measure_function(container_1.get_any_minimal_uc_iterative_deletion, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ANY MINIMAL UCS (Iterative Deletion): ",
    #       [str(a) for a in result] if runtime != -1 else "TIMEOUT")
    # print("-" * 14 + ">", ("INVALID", "VALID")[check_result_any(result, results.get("minimal"))])
    #
    # runtime, result = measure_function(container_1.get_any_minimal_uc_iterative_deletion_improved, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ANY MINIMAL UCS (Iterative Deletion Improved): ",
    #       [str(a) for a in result] if runtime != -1 else "TIMEOUT")
    # print("-" * 14 + ">", ("INVALID", "VALID")[check_result_any(result, results.get("minimal"))])

    return

    if render_sudoku:
        if satisfiable:
            Util.render_sudoku(model, visualization)
        else:
            Util.render_sudoku_with_core(container_1, core, visualization, name_format="1")

    muc = container_1.get_any_minimal_uc_iterative_deletion()
    print("MUC: ", [str(a) for a in muc])

    if render_sudoku and not satisfiable:
        Util.render_sudoku_with_core(container_1, muc, visualization, name_format="2")

    return

    print("FIND MUC ON CORE : ASSUMPTION MARKING")
    muc_found, muc = container_1.get_any_minimal_uc_assumption_marking()

    if render_sudoku and not satisfiable:
        Util.render_sudoku_with_core(container_1, muc, visualization, name_format="3")


if __name__ == '__main__':

    muc_sudoku()

