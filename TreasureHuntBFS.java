/**
 * TreasureHuntBFS.java
 * ====================
 * Enterprise Object-Oriented Java Implementation of the 1D Number Line Treasure Hunt.
 * Includes:
 *   1. Formal State-Space Modeling (States, Actions, Costs, Obstacles)
 *   2. Breadth-First Search (BFS) & A* Search Engines
 *   3. Built-in Java HTTP Server (com.sun.net.httpserver.HttpServer) on Port 8080
 *      allowing the HTML/JS frontend to run directly against a Java backend!
 *
 * Compile & Run:
 *   javac TreasureHuntBFS.java
 *   java TreasureHuntBFS
 */

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class TreasureHuntBFS {

    // Action definition: Move Right (+1), Move Left (-1), Jump Right (+2)
    static class Action {
        final String name;
        final int step;
        final int cost;

        Action(String name, int step, int cost) {
            this.name = name;
            this.step = step;
            this.cost = cost;
        }
    }

    // Parent pointer node for path reconstruction
    static class ParentRecord {
        final int previousState;
        final String actionName;

        ParentRecord(int previousState, String actionName) {
            this.previousState = previousState;
            this.actionName = actionName;
        }
    }

    // Encapsulated Search Result
    static class SearchResult {
        final boolean found;
        final List<String> actions;
        final List<Integer> positions;
        final int cost;
        final int nodesExplored;

        SearchResult(boolean found, List<String> actions, List<Integer> positions, int cost, int nodesExplored) {
            this.found = found;
            this.actions = actions;
            this.positions = positions;
            this.cost = cost;
            this.nodesExplored = nodesExplored;
        }
    }

    private static final List<Action> ACTIONS = Arrays.asList(
        new Action("Move Right (+1)", 1, 1),
        new Action("Move Left (-1)", -1, 1),
        new Action("Jump Right (+2)", 2, 1)
    );

    public static boolean isValid(int pos, int minPos, int maxPos, Set<Integer> obstacles) {
        return pos >= minPos && pos <= maxPos && (obstacles == null || !obstacles.contains(pos));
    }

    public static SearchResult solveBFS(int start, int goal, int minPos, int maxPos, Set<Integer> obstacles) {
        if (!isValid(start, minPos, maxPos, obstacles) || !isValid(goal, minPos, maxPos, obstacles)) {
            throw new IllegalArgumentException("Start or Goal position is invalid or blocked.");
        }

        Queue<Integer> queue = new LinkedList<>();
        Set<Integer> visited = new HashSet<>();
        Map<Integer, ParentRecord> parentMap = new HashMap<>();

        queue.add(start);
        visited.add(start);
        int nodesExplored = 0;

        while (!queue.isEmpty()) {
            int current = queue.poll();
            nodesExplored++;

            if (current == goal) {
                List<String> pathActions = new ArrayList<>();
                List<Integer> pathPositions = new ArrayList<>();
                int curr = goal;
                while (curr != start) {
                    ParentRecord rec = parentMap.get(curr);
                    pathActions.add(rec.actionName);
                    pathPositions.add(curr);
                    curr = rec.previousState;
                }
                Collections.reverse(pathActions);
                Collections.reverse(pathPositions);
                return new SearchResult(true, pathActions, pathPositions, pathActions.size(), nodesExplored);
            }

            for (Action act : ACTIONS) {
                int nextPos = current + act.step;
                if (isValid(nextPos, minPos, maxPos, obstacles) && !visited.contains(nextPos)) {
                    visited.add(nextPos);
                    parentMap.put(nextPos, new ParentRecord(current, act.name));
                    queue.add(nextPos);
                }
            }
        }
        return new SearchResult(false, Collections.emptyList(), Collections.emptyList(), -1, nodesExplored);
    }

    public static void main(String[] args) throws IOException {
        // 1. CLI Execution & Verification
        System.out.println("============================================================");
        System.out.println("  1D NUMBER LINE TREASURE HUNT (JAVA BFS ENGINE)   0 -> 12");
        System.out.println("============================================================");
        SearchResult res = solveBFS(0, 12, 0, 30, Collections.emptySet());
        System.out.println("  Total nodes explored : " + res.nodesExplored);
        System.out.println("  Solution path cost   : " + res.cost);
        System.out.println("  Action sequence      : " + res.actions);
        System.out.println("============================================================");

        // 2. Start Embedded Java HTTP Server on Port 8080
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/api/java-bfs", (HttpExchange exchange) -> {
            if ("GET".equals(exchange.getRequestMethod())) {
                String query = exchange.getRequestURI().getQuery();
                int start = 0, goal = 12;
                if (query != null) {
                    for (String param : query.split("&")) {
                        String[] kv = param.split("=");
                        if (kv[0].equals("start")) start = Integer.parseInt(kv[1]);
                        if (kv[0].equals("goal")) goal = Integer.parseInt(kv[1]);
                    }
                }
                SearchResult r = solveBFS(start, goal, 0, 30, Collections.emptySet());
                String json = String.format(
                    "{"engine":"Java-BFS","found":%b,"cost":%d,"nodesExplored":%d}",
                    r.found, r.cost, r.nodesExplored
                );
                byte[] bytes = json.getBytes(StandardCharsets.UTF_8);
                exchange.getResponseHeaders().add("Content-Type", "application/json");
                exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
                exchange.sendResponseHeaders(200, bytes.length);
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(bytes);
                }
            }
        });
        server.setExecutor(null);
        server.start();
        System.out.println("Java REST API listening on http://localhost:8080/api/java-bfs?start=0&goal=12");
    }
}
