import clingo
import time
import signal
from minimal_unsatisfiable_core import Util, Container

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

    for example in all_examples:
        print("\n" + "="*40, ">", example, "<", "="*40, "\n")
        muc_sudoku_on_example(example)


def timeout_handler(signum, frame):
    raise Exception("OUT OF TIME")


def measure_function(function, args=None, kwargs=None, timeout=10, verbose=0):
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}
    if timeout <= 0:
        raise ValueError("timeout has to be a positive number greater than 0")

    # start countdown for timeout
    signal.alarm(timeout)
    try:
        t_start = time.time()
        result = function(*args, **kwargs)
        t_end = time.time()
        # end countdown for timeout if function was able to complete in time
        signal.alarm(0)
        return t_end - t_start, result
    except Exception as e:
        if verbose > 0:
            print(e)
        return -1, None


def check_result_all(test_result, valid_result):
    if test_result is None:
        return valid_result is None

    valid_result_sets = [set(muc) for muc in valid_result]
    all_there = True
    for muc in test_result:
        if set([str(a) for a in muc]) not in valid_result_sets:
            all_there = False
    return all_there


def check_result_any(test_result, valid_result):
    if test_result is None:
        return valid_result is None
    if not valid_result:
        return not bool(test_result)

    valid_result_sets = [set(muc) for muc in valid_result]
    return set([str(a) for a in test_result]) in valid_result_sets


def muc_sudoku_on_example(example_directory):

    visualization = "res/visualization/visualize_sudoku_core.lp"
    render_sudoku = False

    container_1 = Container(
        example_directory=example_directory
    )

    print([container_1])
    print(container_1)

    satisfiable, model, core = container_1.solve()
    print("result : ", ["UNSAT", "SAT"][satisfiable])
    print("model : ", model)
    print("core : ", core)

    results = Util.read_dictionary_from_file(f"{example_directory}/results.txt")

    print("\n=====> BENCHMARK ALGORITHM PERFORMANCE <=====")

    signal.signal(signal.SIGALRM, timeout_handler)

    # print("\n===> TASK T1 )")
    #
    # runtime, result = measure_function(container_1.get_all_uc_brute_force, timeout=TIMEOUT)
    # print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Brute Force): ",
    #       f"{len(result)} cores" if runtime != -1 else "TIMEOUT")
    #
    # print("\n===> TASK T2 )")
    #
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

    print("\n===> TASK T5 )")

    runtime, result = measure_function(container_1.get_any_minimum_uc_improved_brute_force, timeout=TIMEOUT)
    print(f"[time={'{:.5f}'.format(runtime)}s]", "ANY MINIMUM UCS (Improved Brute Force): ",
          [str(a) for a in result] if runtime != -1 else "TIMEOUT")
    print("-" * 14 + ">", ("INVALID", "VALID")[check_result_any(result, results.get("minimal"))])

    runtime, result = measure_function(container_1.get_any_minimal_uc_iterative_deletion, timeout=TIMEOUT)
    print(f"[time={'{:.5f}'.format(runtime)}s]", "ANY MINIMAL UCS (Iterative Deletion): ",
          [str(a) for a in result] if runtime != -1 else "TIMEOUT")
    print("-" * 14 + ">", ("INVALID", "VALID")[check_result_any(result, results.get("minimal"))])

    runtime, result = measure_function(container_1.get_any_minimal_uc_iterative_deletion_improved, timeout=TIMEOUT)
    print(f"[time={'{:.5f}'.format(runtime)}s]", "ANY MINIMAL UCS (Iterative Deletion Improved): ",
          [str(a) for a in result] if runtime != -1 else "TIMEOUT")
    print("-" * 14 + ">", ("INVALID", "VALID")[check_result_any(result, results.get("minimal"))])

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

    # example_clingraph()
    muc_sudoku()
    # clingraph_factbase_computation()

