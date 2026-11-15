"""
treasure_hunt.py
================
Owner: Member 1 (Sarah Mohamed Ayman) - Core AI Search Algorithms & Logic

Upgraded 1D Number Line Treasure Hunt supporting:
  * Multiple Search Algorithms: BFS, DFS, Uniform-Cost Search (UCS), and A* Search
  * Dynamic Environment: Custom bounds, obstacles/traps, and variable action costs
  * Step-by-Step Execution Trace: Captures queue/frontier & visited states at each step
    for interactive web visualization and REST API integration.
"""

from collections import deque
import heapq
import math

MIN_POS = 0
MAX_POS = 30
START = 0
GOAL = 12

# Standard uniform actions: (name, step, cost)
ACTIONS = [
    ("Move Right (+1)", +1, 1),
    ("Move Left (-1)", -1, 1),
    ("Jump Right (+2)", +2, 1),
]


def is_valid(position, min_pos=MIN_POS, max_pos=MAX_POS, obstacles=None):
    """Check if position is within bounds and not blocked by an obstacle."""
    if not (min_pos <= position <= max_pos):
        return False
    if obstacles and position in obstacles:
        return False
    return True


def reconstruct_path(parent, start, goal):
    """Reconstruct optimal/found path from parent pointers."""
    path = []
    current = goal
    while current != start:
        previous, action_name, step_cost = parent[current]
        path.append((action_name, current, step_cost))
        current = previous
    path.reverse()
    return path


def bfs(start=START, goal=GOAL, min_pos=MIN_POS, max_pos=MAX_POS, obstacles=None, record_trace=False):
    """
    Breadth-First Search (BFS) - Guarantees shortest path in steps when costs are uniform.
    Returns (path, total_cost, nodes_explored) or (path, total_cost, nodes_explored, trace) if record_trace=True.
    """
    obstacles = set(obstacles or [])
    if not is_valid(start, min_pos, max_pos, obstacles):
        raise ValueError(f"Invalid start position: {start}")
    if not is_valid(goal, min_pos, max_pos, obstacles):
        raise ValueError(f"Invalid goal position: {goal}")

    queue = deque([start])
    visited = {start}
    parent = {}
    nodes_explored = 0
    trace = []

    while queue:
        current = queue.popleft()
        nodes_explored += 1

        if record_trace:
            trace.append({
                "step": nodes_explored,
                "current": current,
                "frontier": list(queue),
                "visited": sorted(list(visited))
            })

        if current == goal:
            raw_path = reconstruct_path(parent, start, goal)
            path = [(a, p) for a, p, _ in raw_path]
            cost = sum(c for _, _, c in raw_path)
            return (path, cost, nodes_explored, trace) if record_trace else (path, cost, nodes_explored)

        for action_name, step, step_cost in ACTIONS:
            new_pos = current + step
            if is_valid(new_pos, min_pos, max_pos, obstacles) and new_pos not in visited:
                visited.add(new_pos)
                parent[new_pos] = (current, action_name, step_cost)
                queue.append(new_pos)

    return (None, None, nodes_explored, trace) if record_trace else (None, None, nodes_explored)


def dfs(start=START, goal=GOAL, min_pos=MIN_POS, max_pos=MAX_POS, obstacles=None, record_trace=False):
    """Depth-First Search (DFS) - Explores deep branches first using a LIFO stack."""
    obstacles = set(obstacles or [])
    stack = [start]
    visited = {start}
    parent = {}
    nodes_explored = 0
    trace = []

    while stack:
        current = stack.pop()
        nodes_explored += 1

        if record_trace:
            trace.append({
                "step": nodes_explored,
                "current": current,
                "frontier": list(stack),
                "visited": sorted(list(visited))
            })

        if current == goal:
            raw_path = reconstruct_path(parent, start, goal)
            path = [(a, p) for a, p, _ in raw_path]
            cost = sum(c for _, _, c in raw_path)
            return (path, cost, nodes_explored, trace) if record_trace else (path, cost, nodes_explored)

        for action_name, step, step_cost in reversed(ACTIONS):
            new_pos = current + step
            if is_valid(new_pos, min_pos, max_pos, obstacles) and new_pos not in visited:
                visited.add(new_pos)
                parent[new_pos] = (current, action_name, step_cost)
                stack.append(new_pos)

    return (None, None, nodes_explored, trace) if record_trace else (None, None, nodes_explored)


def astar(start=START, goal=GOAL, min_pos=MIN_POS, max_pos=MAX_POS, obstacles=None, record_trace=False):
    """
    A* Search using admissible heuristic h(n):
      * If n <= goal: ceil((goal - n) / 2) since max forward jump is +2
      * If n > goal : (n - goal) since max backward move is -1
    """
    obstacles = set(obstacles or [])

    def heuristic(pos):
        if pos <= goal:
            return math.ceil((goal - pos) / 2.0)
        return pos - goal

    open_heap = [(heuristic(start), 0, start)]
    g_score = {start: 0}
    visited = set()
    parent = {}
    nodes_explored = 0
    trace = []

    while open_heap:
        f_curr, g_curr, current = heapq.heappop(open_heap)
        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1

        if record_trace:
            trace.append({
                "step": nodes_explored,
                "current": current,
                "frontier": [item[2] for item in open_heap],
                "visited": sorted(list(visited))
            })

        if current == goal:
            raw_path = reconstruct_path(parent, start, goal)
            path = [(a, p) for a, p, _ in raw_path]
            return (path, g_curr, nodes_explored, trace) if record_trace else (path, g_curr, nodes_explored)

        for action_name, step, step_cost in ACTIONS:
            new_pos = current + step
            if is_valid(new_pos, min_pos, max_pos, obstacles) and new_pos not in visited:
                tentative_g = g_curr + step_cost
                if tentative_g < g_score.get(new_pos, float("inf")):
                    g_score[new_pos] = tentative_g
                    parent[new_pos] = (current, action_name, step_cost)
                    f_new = tentative_g + heuristic(new_pos)
                    heapq.heappush(open_heap, (f_new, tentative_g, new_pos))

    return (None, None, nodes_explored, trace) if record_trace else (None, None, nodes_explored)


def bfs_levels(start=START, min_pos=MIN_POS, max_pos=MAX_POS, obstacles=None):
    """Return {level: [positions]} for BFS level-order analysis."""
    obstacles = set(obstacles or [])
    level_of = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for _, step, _ in ACTIONS:
            new_pos = current + step
            if is_valid(new_pos, min_pos, max_pos, obstacles) and new_pos not in level_of:
                level_of[new_pos] = level_of[current] + 1
                queue.append(new_pos)

    levels = {}
    for pos, lvl in level_of.items():
        levels.setdefault(lvl, []).append(pos)
    for lvl in levels:
        levels[lvl].sort()
    return levels
