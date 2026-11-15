"""
test_cases.py
=============
Owner: Member 3 (Abdelrahman) - Integration, Testing & Documentation

Two things in one file:
  1. run_report_table()  -> prints the "Additional Test Cases" table
                            (Section 5.2 of the report)
  2. unittest classes    -> automatic checks (run:  python test_cases.py -v)

The automatic checks verify:
  * every test case from the report gives the expected cost and node count
  * optimality formula: goal ahead  -> cost = ceil(d / 2)
                        goal behind -> cost = d
  * edge cases: start == goal, positions outside the line
  * BFS really is optimal: compared against a brute-force "shortest path"
    computed with simple dynamic programming
"""

import math
import unittest

from treasure_hunt import bfs, MIN_POS, MAX_POS

# (start, treasure, expected_cost, expected_nodes, comment)
REPORT_CASES = [
    (0, 1, 1, 2, "One step right"),
    (0, 5, 3, 6, "Two jumps and one step"),
    (0, 12, 6, 13, "Main experiment"),
    (0, 15, 8, 16, "Seven jumps and one step"),
    (0, 30, 15, 31, "All 31 positions explored"),
    (5, 12, 4, 11, "Three jumps and one step"),
    (20, 3, 17, 28, "Treasure is behind the start: only left moves help"),
    (10, 10, 0, 1, "Start is already the goal"),
]


def run_report_table():
    """Run every case and print the table used in Section 5.2."""
    print(f"{'Start':<7}{'Treasure':<10}{'Path cost':<11}{'Nodes explored':<16}Comment")
    print("-" * 80)
    all_ok = True
    for start, goal, exp_cost, exp_nodes, comment in REPORT_CASES:
        path, cost, nodes = bfs(start, goal)
        ok = (cost == exp_cost and nodes == exp_nodes)
        all_ok = all_ok and ok
        print(f"{start:<7}{goal:<10}{cost:<11}{nodes:<16}{comment}"
              f"{'' if ok else '   <-- MISMATCH'}")
    print("-" * 80)
    print("All cases match the expected values." if all_ok
          else "Some cases did NOT match!")
    return all_ok


# ----------------------------------------------------------------------
# Independent reference solution (does NOT use BFS) for optimality checks
# ----------------------------------------------------------------------
def reference_min_cost(start, goal, lo=MIN_POS, hi=MAX_POS):
    """
    Bellman-Ford style relaxation: repeat until no distance improves.
    Slow but obviously correct, so we can use it to double-check BFS.
    """
    INF = float("inf")
    dist = {p: INF for p in range(lo, hi + 1)}
    dist[start] = 0
    changed = True
    while changed:
        changed = False
        for p in range(lo, hi + 1):
            if dist[p] == INF:
                continue
            for step in (+1, -1, +2):
                q = p + step
                if lo <= q <= hi and dist[p] + 1 < dist[q]:
                    dist[q] = dist[p] + 1
                    changed = True
    return dist[goal]


class TestReportCases(unittest.TestCase):
    def test_all_report_cases(self):
        for start, goal, exp_cost, exp_nodes, comment in REPORT_CASES:
            with self.subTest(start=start, goal=goal):
                path, cost, nodes = bfs(start, goal)
                self.assertEqual(cost, exp_cost)
                self.assertEqual(nodes, exp_nodes)


class TestOptimality(unittest.TestCase):
    def test_formula_goal_ahead(self):
        """Goal ahead at distance d  ->  cost = ceil(d / 2)."""
        for start in range(MIN_POS, MAX_POS + 1):
            for goal in range(start, MAX_POS + 1):
                _, cost, _ = bfs(start, goal)
                self.assertEqual(cost, math.ceil((goal - start) / 2),
                                 f"start={start}, goal={goal}")

    def test_formula_goal_behind(self):
        """Goal behind at distance d  ->  cost = d (only Move Left helps)."""
        for start in range(MIN_POS, MAX_POS + 1):
            for goal in range(MIN_POS, start):
                _, cost, _ = bfs(start, goal)
                self.assertEqual(cost, start - goal, f"start={start}, goal={goal}")

    def test_bfs_matches_reference_for_all_pairs(self):
        for start in range(MIN_POS, MAX_POS + 1):
            for goal in range(MIN_POS, MAX_POS + 1):
                _, cost, _ = bfs(start, goal)
                self.assertEqual(cost, reference_min_cost(start, goal))

    def test_nodes_never_exceed_state_space(self):
        total = MAX_POS - MIN_POS + 1
        for start in range(MIN_POS, MAX_POS + 1):
            for goal in range(MIN_POS, MAX_POS + 1):
                _, _, nodes = bfs(start, goal)
                self.assertLessEqual(nodes, total)


class TestPathValidity(unittest.TestCase):
    def test_path_is_consistent(self):
        """Replaying the actions from the start must land exactly on the goal."""
        steps = {"Move Right (+1)": 1, "Move Left (-1)": -1, "Jump Right (+2)": 2}
        for start, goal in [(0, 12), (0, 15), (5, 12), (20, 3), (29, 0)]:
            path, cost, _ = bfs(start, goal)
            pos = start
            for action, new_pos in path:
                pos += steps[action]
                self.assertEqual(pos, new_pos)
                self.assertTrue(MIN_POS <= pos <= MAX_POS)
            self.assertEqual(pos, goal)
            self.assertEqual(len(path), cost)


class TestEdgeCases(unittest.TestCase):
    def test_start_equals_goal(self):
        path, cost, nodes = bfs(10, 10)
        self.assertEqual((path, cost, nodes), ([], 0, 1))

    def test_goal_outside_line(self):
        with self.assertRaises(ValueError):
            bfs(0, 31)
        with self.assertRaises(ValueError):
            bfs(0, -1)

    def test_start_outside_line(self):
        with self.assertRaises(ValueError):
            bfs(-5, 10)
        with self.assertRaises(ValueError):
            bfs(50, 10)

    def test_extreme_positions(self):
        self.assertEqual(bfs(0, 30)[1], 15)
        self.assertEqual(bfs(30, 0)[1], 30)
        self.assertEqual(bfs(0, 29)[1], 15)


if __name__ == "__main__":
    run_report_table()
    print()
    unittest.main(verbosity=2)
