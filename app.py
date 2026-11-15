"""
app.py
======
Lightweight HTTP & REST API Server for the 1D Number Line Treasure Hunt Web Application.
Uses Python's built-in http.server (zero external dependencies) to serve the frontend
and expose POST /api/solve for BFS, DFS, and A* search comparisons.
"""

import json
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from treasure_hunt import bfs, dfs, astar, bfs_levels

WEB_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web")


class TreasureHuntHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_ROOT, **kwargs)

    def do_POST(self):
        if self.path == "/api/solve":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            start = int(data.get("start", 0))
            goal = int(data.get("goal", 12))
            min_pos = int(data.get("min_pos", 0))
            max_pos = int(data.get("max_pos", 30))
            obstacles = [int(x) for x in data.get("obstacles", [])]
            algo = data.get("algorithm", "BFS").upper()

            solvers = {"BFS": bfs, "DFS": dfs, "ASTAR": astar}
            solver = solvers.get(algo, bfs)

            try:
                path, cost, nodes, trace = solver(
                    start, goal, min_pos, max_pos, obstacles=obstacles, record_trace=True
                )
                # Also compute benchmark comparison across all 3 algorithms
                benchmarks = {}
                for name, fn in solvers.items():
                    p, c, n = fn(start, goal, min_pos, max_pos, obstacles=obstacles)
                    benchmarks[name] = {"cost": c, "nodes_explored": n, "found": p is not None}

                response = {
                    "status": "ok",
                    "algorithm": algo,
                    "found": path is not None,
                    "path": [{"action": a, "position": p} for a, p in (path or [])],
                    "cost": cost,
                    "nodes_explored": nodes,
                    "trace": trace,
                    "levels": bfs_levels(start, min_pos, max_pos, obstacles=obstacles),
                    "benchmarks": benchmarks
                }
                self.send_response(200)
            except Exception as e:
                response = {"status": "error", "message": str(e)}
                self.send_response(400)

            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint not found")


if __name__ == "__main__":
    PORT = 8000
    server = HTTPServer(("127.0.0.1", PORT), TreasureHuntHandler)
    print(f"Treasure Hunt Web Simulator running at http://127.0.0.1:{PORT}")
    server.serve_forever()
