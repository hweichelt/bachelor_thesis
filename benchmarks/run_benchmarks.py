from pathlib import Path
from sudoku_muc import api
from collections.abc import Iterable

import pandas as pd
import clingo
import json
import time
import os


BENCHMARK_DIRS = [
    "10_assumptions/10_mucs",
    "10_assumptions/50_mucs",
    "10_assumptions/100_mucs",
    "50_assumptions/10_mucs",
    "50_assumptions/50_mucs",
    "50_assumptions/100_mucs",
    "100_assumptions/10_mucs",
    "100_assumptions/50_mucs",
    "100_assumptions/100_mucs",
    "1000_assumptions/10_mucs",
    "1000_assumptions/50_mucs",
    "1000_assumptions/100_mucs",
    "10000_assumptions/10_mucs",
    "10000_assumptions/50_mucs",
    "10000_assumptions/100_mucs",
]

# ASSUMPTION SCALING BENCHMARKS
BENCHMARK_DIRS = [
    "../benchmarks_2/assumption_scaling/10_assumptions/5_mucs",
    "../benchmarks_2/assumption_scaling/20_assumptions/5_mucs",
    "../benchmarks_2/assumption_scaling/30_assumptions/5_mucs",
    "../benchmarks_2/assumption_scaling/40_assumptions/5_mucs",
    "../benchmarks_2/assumption_scaling/50_assumptions/5_mucs",
    "../benchmarks_2/assumption_scaling/60_assumptions/5_mucs",
    "../benchmarks_2/assumption_scaling/70_assumptions/5_mucs",
    "../benchmarks_2/assumption_scaling/80_assumptions/5_mucs",
    "../benchmarks_2/assumption_scaling/90_assumptions/5_mucs",
    "../benchmarks_2/assumption_scaling/100_assumptions/5_mucs",
]

# MUC SCALING BENCHMARKS
BENCHMARK_DIRS = [
    "../benchmarks_2/muc_scaling/40_assumptions/1_mucs",
    "../benchmarks_2/muc_scaling/40_assumptions/2_mucs",
    "../benchmarks_2/muc_scaling/40_assumptions/3_mucs",
    "../benchmarks_2/muc_scaling/40_assumptions/4_mucs",
    "../benchmarks_2/muc_scaling/40_assumptions/5_mucs",
    "../benchmarks_2/muc_scaling/40_assumptions/6_mucs",
    "../benchmarks_2/muc_scaling/40_assumptions/7_mucs",
    "../benchmarks_2/muc_scaling/40_assumptions/8_mucs",
    "../benchmarks_2/muc_scaling/40_assumptions/9_mucs",
    "../benchmarks_2/muc_scaling/40_assumptions/10_mucs",
]

# ID ASSUMPTION SCALING BENCHMARKS
BENCHMARK_DIRS = [
    "../benchmarks_2/id_assumption_scaling/100_assumptions/10_mucs",
    "../benchmarks_2/id_assumption_scaling/200_assumptions/10_mucs",
    "../benchmarks_2/id_assumption_scaling/300_assumptions/10_mucs",
    "../benchmarks_2/id_assumption_scaling/400_assumptions/10_mucs",
    "../benchmarks_2/id_assumption_scaling/500_assumptions/10_mucs",
    "../benchmarks_2/id_assumption_scaling/600_assumptions/10_mucs",
    "../benchmarks_2/id_assumption_scaling/700_assumptions/10_mucs",
    "../benchmarks_2/id_assumption_scaling/800_assumptions/10_mucs",
    "../benchmarks_2/id_assumption_scaling/900_assumptions/10_mucs",
    "../benchmarks_2/id_assumption_scaling/1000_assumptions/10_mucs",
]

# ID MUC SCALING BIG BENCHMARKS
BENCHMARK_DIRS = [
    "../benchmarks_2/id_muc_scaling_big/10000_assumptions/50_mucs",
    "../benchmarks_2/id_muc_scaling_big/10000_assumptions/100_mucs",
    "../benchmarks_2/id_muc_scaling_big/10000_assumptions/150_mucs",
    "../benchmarks_2/id_muc_scaling_big/10000_assumptions/200_mucs",
    "../benchmarks_2/id_muc_scaling_big/10000_assumptions/250_mucs",
    "../benchmarks_2/id_muc_scaling_big/10000_assumptions/300_mucs",
    "../benchmarks_2/id_muc_scaling_big/10000_assumptions/350_mucs",
    "../benchmarks_2/id_muc_scaling_big/10000_assumptions/400_mucs",
    "../benchmarks_2/id_muc_scaling_big/10000_assumptions/450_mucs",
    "../benchmarks_2/id_muc_scaling_big/10000_assumptions/500_mucs",
]

STATS_COLUMNS = {
    "algorithm": str,
    "algorithm single muc": bool,
    "benchmark assumptions": int,
    "benchmark mucs": int,
    "number of mucs found": int,
    "computation time": float,
    "timeout occurred": bool,
    "everything found": bool,
}

ALGORITHMS = [
    {
        "name": "[Single-MUC]_Iterative_Deletion",
        "slug": "id_single",
        "single_muc": True,
        "core_computer": api.CoreComputer,
    },
    # {
    #     "name": "[Single-MUC]_Brute_Force",
    #     "slug": "bf_single",
    #     "single_muc": True,
    #     "core_computer": api.CoreComputerBruteForce,
    # },
    # {
    #     "name": "[Single-MUC]_Brute_Force_Improved",
    #     "slug": "bfi_single",
    #     "single_muc": True,
    #     "core_computer": api.CoreComputerBruteForceImproved,
    # },
    # {
    #     "name": "[Multi-MUC]_Iterative_Deletion",
    #     "slug": "id_multi",
    #     "single_muc": False,
    #     "core_computer": api.CoreComputer,
    # },
    # {
    #     "name": "[Multi-MUC]_Brute_Force",
    #     "slug": "bf_multi",
    #     "single_muc": False,
    #     "core_computer": api.CoreComputerBruteForce,
    # },
    # {
    #     "name": "[Multi-MUC]_Brute_Force_Improved",
    #     "slug": "bfi_multi",
    #     "single_muc": False,
    #     "core_computer": api.CoreComputerBruteForceImproved,
    # },
]

TIMEOUT = 300


def evaluate_results(stats_df, results, bench_dir, n_assumptions, n_mucs, results_computation_time, algorithm):
    with open(Path(__file__).parent.absolute().joinpath(bench_dir).joinpath("results.txt"), "r") as f:
        solutions = json.loads(f.read())

    results_iterable = isinstance(results, Iterable)

    solutions_minimal = [set([(clingo.parse_term(a), True) for a in sol]) for sol in solutions["minimal"]]
    results_valid = all([muc in solutions_minimal for muc in results]) if results_iterable else False
    results_valid_string = ["❌", "✅"][results_valid]

    print(results_valid_string, f"[{'{:.4f}'.format(results_computation_time)}s]",
          [[str(a) for a, _ in muc] for muc in results] if results_iterable else "NO RESULT FOUND")

    stats_data = [
        algorithm["slug"],  # algorithm name
        algorithm["single_muc"],  # algorithm single muc
        n_assumptions,  # benchmark assumptions
        n_mucs,  # benchmark mucs
        len(results) if results_iterable else 0,  # number of mucs found
        results_computation_time,  # computation time
        bool(results_computation_time >= TIMEOUT),  # timeout occurred
        bool(len(results) == n_mucs) if results_iterable else False,  # everything found
    ]
    new_stats = pd.DataFrame(data=[stats_data], columns=list(STATS_COLUMNS.keys()), index=[len(stats_df)])
    new_stats = new_stats.astype(STATS_COLUMNS)
    stats = pd.concat([stats_df, new_stats])

    return stats


def run_benchmarks(override_results=False):
    for algorithm in ALGORITHMS:
        statistics_dir = Path(__file__).parent.absolute().joinpath("statistics/")
        if not os.path.isdir(statistics_dir):
            os.mkdir(statistics_dir)

        for b, bench_dir in enumerate(BENCHMARK_DIRS):
            stats = pd.DataFrame(columns=list(STATS_COLUMNS.keys()))
            stats = stats.astype(STATS_COLUMNS)

            n_assumptions = int(Path(bench_dir).parent.name.replace("_assumptions", ""))
            n_mucs = int(Path(bench_dir).name.replace("_mucs", ""))
            stats_filename = f"stats_{n_assumptions}assumptions_{n_mucs}mucs_{algorithm['slug']}_{TIMEOUT}timeout.csv"

            if not override_results and os.path.isfile(statistics_dir.joinpath(stats_filename)):
                print(f"SKIPPED [{stats_filename}] since an result already exists")
                continue

            print(b, bench_dir)

            with open(Path(__file__).parent.absolute().joinpath(bench_dir).joinpath("assumptions.lp"), "r") as f:
                assumptions = {(clingo.parse_term(a.replace('.', '')).arguments[0], True) for a in f.readlines()}

            absolute_benchmark_path = Path(__file__).parent.absolute().joinpath(bench_dir).joinpath("encoding.lp")
            cc = algorithm["core_computer"](
                encoding_paths=[str(absolute_benchmark_path)],
                assumptions=assumptions,
            )
            start_t = time.perf_counter()
            results = cc.compute_minimal(multiple=not algorithm["single_muc"], timeout=TIMEOUT, max_amount=n_mucs)
            end_t = time.perf_counter()

            results_computation_time = end_t - start_t

            stats = evaluate_results(stats, results, bench_dir, n_assumptions, n_mucs, results_computation_time, algorithm)

            stats.to_csv(statistics_dir.joinpath(stats_filename), index=False)

    # df = pd.read_csv(STATS_FILE)
    # print(df.to_string())

    # print("\nOVERVIEW :")
    # print("\tAll Benchmarks passed :", ["❌", "✅"][3])
    # print(f"\t{sum(stats)}/{len(stats)} Benchmarks Passed")
