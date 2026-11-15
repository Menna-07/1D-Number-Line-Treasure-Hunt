"""
visualize.py
============
Owner: Member 2 (Menatallah) - Visualization & Experiments

Everything the professor "sees":
  * print_solution()      -> formatted console output
  * print_levels_table()  -> BFS levels table
  * draw_flowchart()      -> Figure 1 (BFS flowchart)
  * draw_number_line()    -> Figure 2 (optimal path on the number line)

Only depends on matplotlib. Uses the non-GUI "Agg" backend so it works on
any machine (even without a display) and simply saves PNG files.
"""

import matplotlib
matplotlib.use("Agg")                       # save to file, no pop-up window
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch

NAVY = "#1F3864"
BLUE = "#2E75B6"
LIGHT = "#DEEAF6"
YELLOW = "#FFF2CC"
GOLD = "#BF8F00"
GREEN = "#2E8B57"


# ----------------------------------------------------------------------
# 1. Console output
# ----------------------------------------------------------------------
def _short_name(action_name):
    """'Jump Right (+2)' -> 'Jump (+2)',  'Move Left (-1)' -> 'Move (-1)'."""
    verb = action_name.split(" ")[0]              # 'Jump' or 'Move'
    amount = action_name[action_name.index("("):]  # '(+2)'
    return f"{verb} {amount}"


def print_solution(start, goal, path, cost, nodes_explored):
    """Print the metrics, the action sequence and the step table."""
    print("=" * 60)
    print(f"  1D NUMBER LINE TREASURE HUNT  (BFS)   {start} -> {goal}")
    print("=" * 60)

    if path is None:
        print("  No solution found.")
        print(f"  Total nodes explored : {nodes_explored}")
        print("=" * 60)
        return

    print(f"  Total nodes explored : {nodes_explored}")
    print(f"  Solution path cost   : {cost}")

    # Short action sequence: Start (0) -> Jump (+2) -> ... -> Goal (12)
    short = " -> ".join(_short_name(a) for a, _ in path)
    print(f"  Action sequence      : Start ({start}) -> {short} -> Goal ({goal})")
    print("-" * 60)
    print(f"  {'Step':<6}{'Action':<22}{'New position'}")
    print("-" * 60)
    for i, (action, pos) in enumerate(path, start=1):
        tag = " (treasure)" if pos == goal else ""
        print(f"  {i:<6}{action:<22}{pos}{tag}")
    print("=" * 60)


def print_levels_table(levels, goal=None, max_level=None):
    """Print BFS levels: level -> new positions reached at that level."""
    print(f"  {'Level (actions)':<18}New positions reached")
    print("  " + "-" * 45)
    for lvl in sorted(levels):
        if max_level is not None and lvl > max_level:
            break
        cells = []
        for p in levels[lvl]:
            cells.append(f"{p} (treasure)" if p == goal else str(p))
        print(f"  {lvl:<18}{', '.join(cells)}")


# ----------------------------------------------------------------------
# 2. Figure 1 - flowchart
# ----------------------------------------------------------------------
def _box(ax, cx, cy, w, h, text, fc=LIGHT, ec=NAVY):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=fc, ec=ec, lw=1.6))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=9)


def _diamond(ax, cx, cy, w, h, text):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy),
                          (cx, cy - h / 2), (cx - w / 2, cy)],
                         closed=True, fc=YELLOW, ec=GOLD, lw=1.6))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=9)


def _arrow(ax, p1, p2, label=None, label_pos=None):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14,
                                 lw=1.5, color="#222222"))
    if label:
        lx, ly = label_pos
        ax.text(lx, ly, label, fontsize=9, fontweight="bold", color="#444444")


def draw_flowchart(filename):
    """Draw Figure 1: flowchart of the BFS algorithm used in the project."""
    fig, ax = plt.subplots(figsize=(8, 7.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(1.9, 11.7)
    ax.axis("off")

    cx = 4.0
    _box(ax, cx, 11.2, 2.6, 0.7, "Start")
    _box(ax, cx, 9.9, 4.6, 0.9, "Put the initial state in the queue\nand in the visited set")
    _diamond(ax, cx, 8.3, 3.4, 1.6, "Is the queue\nempty?")
    _box(ax, 8.3, 8.3, 2.6, 0.9, "No solution")
    _box(ax, cx, 6.5, 4.2, 0.9, "Pop the first state from the queue\n(nodes explored + 1)")
    _diamond(ax, cx, 5.0, 3.4, 1.6, "Is it the\ngoal state?")
    _box(ax, 8.3, 5.0, 2.6, 1.1, "Rebuild the path\nusing parent\npointers, then stop")
    _box(ax, cx, 2.8, 5.8, 1.2,
         "Generate next states (+1, -1, +2).\nKeep the valid ones that are not visited,\n"
         "mark them visited and add them to the queue")

    _arrow(ax, (cx, 10.85), (cx, 10.35))
    _arrow(ax, (cx, 9.45), (cx, 9.1))
    _arrow(ax, (cx, 7.5), (cx, 6.95), "No", (cx + 0.12, 7.2))
    _arrow(ax, (cx + 1.7, 8.3), (7.0, 8.3), "Yes", (5.9, 8.4))
    _arrow(ax, (cx, 6.05), (cx, 5.8))
    _arrow(ax, (cx, 4.2), (cx, 3.4), "No", (cx + 0.12, 3.8))
    _arrow(ax, (cx + 1.7, 5.0), (7.0, 5.0), "Yes", (5.9, 5.1))

    # loop-back arrow (bottom box -> back up to the "queue empty?" test)
    ax.plot([cx - 2.9, 0.7], [2.8, 2.8], color="#222222", lw=1.5)
    ax.plot([0.7, 0.7], [2.8, 8.3], color="#222222", lw=1.5)
    _arrow(ax, (0.7, 8.3), (cx - 1.7, 8.3))

    plt.savefig(filename, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ----------------------------------------------------------------------
# 3. Figure 2 - path on the number line
# ----------------------------------------------------------------------
def draw_number_line(filename, path, start, goal, min_pos=0, max_pos=30):
    """Draw Figure 2: the solution path as arcs on the number line."""
    fig, ax = plt.subplots(figsize=(11, 2.8))
    ax.set_xlim(min_pos - 1.5, max_pos + 1.5)
    ax.set_ylim(-1.6, 2.0)
    ax.axis("off")

    # the number line
    ax.plot([min_pos, max_pos], [0, 0], color="black", lw=1.4, zorder=1)
    for p in range(min_pos, max_pos + 1):
        ax.plot([p, p], [-0.12, 0.12], color="black", lw=0.8, zorder=1)
        if p % 2 == 0:
            ax.text(p, -0.45, str(p), ha="center", va="top", fontsize=8,
                    color="#444444")

    # one arc per action
    cur = start
    for action, new_pos in (path or []):
        step = new_pos - cur
        rad = -0.9 if step > 0 else 0.9
        ax.add_patch(FancyArrowPatch((cur, 0.15), (new_pos, 0.15),
                                     connectionstyle=f"arc3,rad={rad}",
                                     arrowstyle="-|>", mutation_scale=12,
                                     color=BLUE, lw=1.8, zorder=3))
        label = f"{step:+d}"
        ax.text((cur + new_pos) / 2, 0.85 if abs(step) == 2 else 0.55,
                label, ha="center", fontsize=8, color=BLUE, fontweight="bold")
        cur = new_pos

    ax.scatter([start], [0], s=140, color=GREEN, zorder=5)
    ax.scatter([goal], [0], s=330, color="#F2B01E", marker="*",
               edgecolors=GOLD, zorder=5)
    ax.text(start, -1.2, f"Start ({start})", ha="center", color=GREEN,
            fontweight="bold", fontsize=9)
    ax.text(goal, -1.2, f"Treasure ({goal})", ha="center", color=GOLD,
            fontweight="bold", fontsize=9)

    n_jumps = sum(1 for a, _ in (path or []) if "Jump" in a)
    cost = len(path) if path else 0
    ax.set_title(f"Optimal path found by BFS: {cost} actions "
                 f"({n_jumps} jumps of +2, path cost = {cost})",
                 fontsize=10, color=NAVY, fontweight="bold")

    plt.savefig(filename, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    # Quick self-check: python visualize.py
    from treasure_hunt import bfs, START, GOAL
    p, c, n = bfs()
    print_solution(START, GOAL, p, c, n)
    draw_number_line("../figures/fig2_number_line_path.png", p, START, GOAL)
    draw_flowchart("../figures/fig1_bfs_flowchart.png")
    print("Figures saved in ../figures/")
