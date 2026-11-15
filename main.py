"""
main.py
=======
Integration entry point - this is the ONLY file you need to run.

    python main.py                      # main experiment 0 -> 12 + all tests
    python main.py --start 5 --goal 20  # custom experiment
    python main.py --no-tests           # skip the test table

It connects the three parts of the project:

    treasure_hunt.py  (Sarah)        -> bfs(), bfs_levels()
    visualize.py      (Menatallah)   -> printing + figures
    test_cases.py     (Abdelrahman)  -> test table + unit tests

and saves everything into ../output and ../figures.
"""

import argparse
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

from treasure_hunt import bfs, bfs_levels, is_valid, START, GOAL, MIN_POS, MAX_POS
from visualize import (print_solution, print_levels_table,
                       draw_flowchart, draw_number_line)
import test_cases

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, "..", "figures")
OUT_DIR = os.path.join(HERE, "..", "output")


def run_experiment(start, goal):
    """Run BFS once, print the results and draw Figure 2."""
    path, cost, nodes = bfs(start, goal)
    print_solution(start, goal, path, cost, nodes)
    draw_number_line(os.path.join(FIG_DIR, "fig2_number_line_path.png"),
                     path, start, goal, MIN_POS, MAX_POS)
    return path, cost, nodes


def main():
    parser = argparse.ArgumentParser(description="1D Number Line Treasure Hunt (BFS)")
    parser.add_argument("--start", type=int, default=START, help="start position")
    parser.add_argument("--goal", type=int, default=GOAL, help="treasure position")
    parser.add_argument("--no-tests", action="store_true", help="skip test cases")
    args = parser.parse_args()

    # Friendly error instead of a Python traceback
    for name, value in (("start", args.start), ("goal", args.goal)):
        if not is_valid(value):
            parser.error(f"--{name} {value} is outside the number line "
                         f"[{MIN_POS}, {MAX_POS}]")

    os.makedirs(FIG_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)

    # Everything printed is also captured and saved to a text file (Appendix B)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        # ---- Part 1: main experiment ------------------------------------
        run_experiment(args.start, args.goal)

        # ---- Part 2: BFS levels table -----------------------------------
        print("\nBFS LEVELS (start = {})".format(args.start))
        print_levels_table(bfs_levels(args.start), goal=args.goal,
                           max_level=None if args.start != 0 else 6)

        # ---- Part 3: additional test cases ------------------------------
        if not args.no_tests:
            print("\nADDITIONAL TEST CASES")
            test_cases.run_report_table()

    text = buffer.getvalue()
    print(text, end="")
    with open(os.path.join(OUT_DIR, "main_output.txt"), "w", encoding="utf-8") as f:
        f.write(text)

    # ---- Part 4: figure 1 (flowchart) -----------------------------------
    draw_flowchart(os.path.join(FIG_DIR, "fig1_bfs_flowchart.png"))

    # ---- Part 5: unit tests (saved separately) --------------------------
    if not args.no_tests:
        stream = io.StringIO()
        suite = unittest.defaultTestLoader.loadTestsFromModule(test_cases)
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        with open(os.path.join(OUT_DIR, "unit_tests_output.txt"), "w",
                  encoding="utf-8") as f:
            f.write(stream.getvalue())
        print("\nUNIT TESTS: {} run, {} failures, {} errors".format(
            result.testsRun, len(result.failures), len(result.errors)))

    print("\nSaved: output/main_output.txt, output/unit_tests_output.txt, "
          "figures/fig1_bfs_flowchart.png, figures/fig2_number_line_path.png")


if __name__ == "__main__":
    sys.exit(main())
