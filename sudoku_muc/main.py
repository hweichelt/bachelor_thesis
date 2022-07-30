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

    print("\n=====> BENCHMARK ALGORITHM PERFORMANCE <=====")

    signal.signal(signal.SIGALRM, timeout_handler)

    print("\n===> TASK T1 )")

    runtime, result = measure_function(container_1.get_all_uc_brute_force, timeout=TIMEOUT)
    print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Brute Force): ",
          f"{len(result)} cores" if result is not None else "TIMEOUT")

    print("\n===> TASK T2 )")

    runtime, result = measure_function(container_1.get_all_minimal_uc_brute_force, timeout=TIMEOUT)
    print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Brute Force): ",
          [[str(a) for a in muc] for muc in result] if result is not None else "TIMEOUT")

    runtime, result = measure_function(container_1.get_all_minimal_uc_improved_brute_force, timeout=TIMEOUT)
    print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMAL UCS (Improved Brute Force): ",
          [[str(a) for a in muc] for muc in result] if result is not None else "TIMEOUT")

    print("\n===> TASK T3 )")

    runtime, result = measure_function(container_1.get_all_minimum_uc_brute_force, timeout=TIMEOUT)
    print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMUM UCS (Brute Force): ",
          [[str(a) for a in muc] for muc in result] if result is not None else "TIMEOUT")

    runtime, result = measure_function(container_1.get_all_minimum_uc_improved_brute_force, timeout=TIMEOUT)
    print(f"[time={'{:.5f}'.format(runtime)}s]", "ALL MINIMUM UCS (Improved Brute Force): ",
          [[str(a) for a in muc] for muc in result] if result is not None else "TIMEOUT")

    print("\n===> TASK T5 )")

    runtime, result = measure_function(container_1.get_any_minimum_uc_improved_brute_force, timeout=TIMEOUT)
    print(f"[time={'{:.5f}'.format(runtime)}s]", "ANY MINIMUM UCS (Improved Brute Force): ",
          [str(a) for a in result] if result is not None else "TIMEOUT")

    runtime, result = measure_function(container_1.get_any_minimal_uc_iterative_deletion, timeout=TIMEOUT)
    print(f"[time={'{:.5f}'.format(runtime)}s]", "ANY MINIMAL UCS (Iterative Deletion): ",
          [str(a) for a in result] if result is not None else "TIMEOUT")

    # signal.alarm(10)
    #
    # try:
    #     t_start = time.time()
    #     any_minimal_uc = container_1.get_any_minimal_uc_iterative_deletion()
    #     t_end = time.time()
    #     print(f"[time={ '{:.5f}'.format(t_end - t_start) }s]", "ANY MINIMAL UC (Iterative Deletion): ", [str(a) for a in any_minimal_uc])
    # except Exception as e:
    #     print(e)

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

    return

    if not muc_found:
        print("MUC : Problem wasn't unsatisfiable to begin with, there is no minimal unsatisfiable core")
    else:
        print(f"MUC : {muc}")

    time_bf_start = time.time()
    ucs = container_1.get_all_uc_brute_force()
    time_bf_end = time.time()

    time_bf_muc_start = time.time()
    mucs = container_1.get_all_minimal_ucs_brute_force()
    time_bf_muc_end = time.time()

    print("time BF All:", time_bf_end - time_bf_start, "s")
    print("time BF Minimal:", time_bf_muc_end - time_bf_muc_start, "s")

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

