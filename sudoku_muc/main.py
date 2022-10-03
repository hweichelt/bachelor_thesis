import json
import os.path
import time
from itertools import combinations, chain

import clingo

import tests
import api
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
        "res/examples/abstract_multi_core_big",
        "res/examples/abstract_multi_core_many",
        "res/examples/abstract_multi_core_breaking",
        "res/examples/abstract_multi_core_breaking_2",
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
    if result and isinstance(result[0], list):
        # MULTIPLE CORES
        print(f"[time={'{:.5f}'.format(runtime)}s]", name,
              [[str(a) for a in muc] for muc in result] if runtime != -1 else "TIMEOUT")
    else:
        # SINGLE CORE
        print(f"[time={'{:.5f}'.format(runtime)}s]", name,
              [str(a) for a in result] if runtime != -1 else "TIMEOUT")
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

    # print("\n===> TASK T1 )")
    #
    # runtime, result = measure_function(container_1.get_all_uc_brute_force, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Brute Force): ",
    #       f"{len(result)} cores" if runtime != -1 else "TIMEOUT")

    print("\n===> TASK T2 )")

    # print_test_results(
    #     function=container_1.get_all_minimal_uc_brute_force,
    #     valid_data=results.get("minimal"),
    #     test=TestAllContained(),
    #     name="ALL MINIMAL UCS (Brute Force):"
    # )
    #
    # print_test_results(
    #     function=container_1.get_all_minimal_uc_improved_brute_force,
    #     valid_data=results.get("minimal"),
    #     test=TestAllContained(),
    #     name="ALL MINIMAL UCS (Improved Brute Force):"
    # )
    #
    # print_test_results(
    #     function=container_1.get_all_minimal_uc_iterative_deletion,
    #     valid_data=results.get("minimal"),
    #     test=TestAllContained(),
    #     name="ALL MINIMAL UCS (Iterative Deletion):"
    # )

    # print_test_results(
    #     function=container_1.get_all_minimal_uc_iterative_deletion,
    #     valid_data=results.get("minimal"),
    #     test=TestAllContained(),
    #     name="ALL MINIMAL UCS (Iterative Deletion STOPPING):"
    # )

    print_test_results(
        function=container_1.get_all_minimal_uc_iterative_deletion_oracle,
        valid_data=results.get("minimal"),
        test=TestAllContained(),
        name="ALL MINIMAL UCS (Iterative Deletion ORACLE):"
    )

    # res = container_1.get_all_minimal_uc_iterative_deletion_oracle()
    # print(res)

    print("\n===> TASK T3 )")

    # print_test_results(
    #     function=container_1.get_all_minimum_uc_brute_force,
    #     valid_data=results.get("minimum"),
    #     test=TestAllContained(),
    #     name="ALL MINIMUM UCS (Brute Force):"
    # )
    #
    # print_test_results(
    #     function=container_1.get_all_minimum_uc_improved_brute_force,
    #     valid_data=results.get("minimum"),
    #     test=TestAllContained(),
    #     name="ALL MINIMUM UCS (Improved Brute Force):"
    # )

    print("\n===> TASK T5 )")

    # print_test_results(
    #     function=container_1.get_any_minimum_uc_improved_brute_force,
    #     valid_data=results.get("minimum"),
    #     test=TestAnyContained(),
    #     name="ANY MINIMUM UCS (Improved Brute Force):"
    # )
    #
    # print_test_results(
    #     function=container_1.get_any_minimal_uc_iterative_deletion,
    #     valid_data=results.get("minimal"),
    #     test=TestAnyContained(),
    #     name="ANY MINIMAL UCS (Iterative Deletion):"
    # )
    #
    # print_test_results(
    #     function=container_1.get_any_minimal_uc_iterative_deletion_improved,
    #     valid_data=results.get("minimal"),
    #     test=TestAnyContained(),
    #     name="ANY MINIMAL UCS (Iterative Deletion Improved):"
    # )

    return

    # OLD BUT USEFUL CODE

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

    # tests.subset_finder()
    # muc_sudoku()
    # tests.check_comparison()
    # time_start = time.perf_counter()
    # tests.realistic_set_skipping(n_assumptions=20, minimal_cores=[["a(0)", "a(1)"], ["a(1)", "a(2)"], ["a(3)"]])
    # time_end = time.perf_counter()
    #
    # print(f"time={time_end - time_start}s")
    #
    assumptions = {
        "solution(4, 9, 3)",
        "solution(7, 1, 9)",
        "solution(2, 2, 7)",
        "solution(4, 7, 7)",
        "solution(3, 9, 7)",
        "solution(8, 2, 8)",
        "solution(1, 6, 8)",
        "solution(6, 7, 8)",
        "solution(2, 9, 8)",
        "solution(5, 5, 7)",
        "solution(1, 7, 6)",
        "solution(9, 1, 7)",
        "solution(2, 7, 4)",
        "solution(9, 7, 4)",
    }
    assumptions = {(clingo.parse_term(string), True) for string in assumptions}

    directory = "res/examples/sudoku/sudoku_multi_combined"
    cc = api.CoreComputer(
        encoding_paths=[f"{directory}/encoding.lp", f"{directory}/extras.lp"],
        assumptions=assumptions
    )
    res = cc.compute_minimal(multiple=True, timeout=1, max_amount=None)
    print(type(res))
    if res is not None:
        print([[str(a) for a, _ in core] for core in res])

    # TODO : Why the double true for assumptions?
    # tests.bit_array_test()
    # tests.not_vs_without_2()
