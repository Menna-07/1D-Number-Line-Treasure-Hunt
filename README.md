# 1D Number Line Treasure Hunt — Full-Stack Multi-Language AI Project (V2)

An upgraded, full-stack Artificial Intelligence search simulator solving the **1D Number Line Treasure Hunt** problem across **Python**, **Java**, and an **Interactive HTML5/CSS3/JS Web Application**.

## Project Structure
```text
Treasure_Hunt_Project_V2/
 ├── src/
 │    ├── treasure_hunt.py   # Core AI Engines (BFS, DFS, A* Search, Obstacles, Trace)
 │    ├── app.py             # Python HTTP & JSON REST API Server (Port 8000)
 │    ├── visualize.py       # Console output & Matplotlib figures
 │    ├── test_cases.py      # Automated unit tests & Bellman-Ford verifier
 │    └── main.py            # CLI entry point
 ├── java/
 │    └── TreasureHuntBFS.java  # Object-Oriented Java Engine + Embedded HTTP API (Port 8080)
 ├── web/
 │    └── index.html         # Interactive Web Simulator (Animated Agent, Walls, Benchmarks)
 ├── figures/                # Flowchart & Optimal Path visual figures
 └── Final_Report_Treasure_Hunt_V2.docx
```

## How to Run
1. **Interactive Web Application (Python Server):**
   ```bash
   python src/app.py
   # Open http://127.0.0.1:8000 in your browser (or open web/index.html directly)
   ```
2. **Java Engine & REST Server:**
   ```bash
   javac java/TreasureHuntBFS.java
   java -cp java TreasureHuntBFS
   ```
3. **CLI Experiments & Unit Tests:**
   ```bash
   python src/main.py
   ```
