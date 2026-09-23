import os
import json
from flask import Flask, render_template, jsonify, request
from uninformed import bfs, dfs, ucs, ids
from informed import greedy_best_first_search, a_star_search

app = Flask(__name__)

MAP_DATA_FILE = "map_data.json"


def load_map_data():
    """Load graph and location data from map_data.json if available."""
    if os.path.exists(MAP_DATA_FILE):
        try:
            with open(MAP_DATA_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {MAP_DATA_FILE}: {e}")
    return {
        "region": "State / Metro Area",
        "total_cities": 0,
        "total_edges": 0,
        "locations": {},
        "graph": {}
    }


@app.route("/")
def index():
    """Renders the main deployment webpage."""
    return render_template("index.html")


@app.route("/api/map", methods=["GET"])
def get_map():
    """Returns map locations and graph connections."""
    data = load_map_data()
    return jsonify(data)


@app.route("/api/search", methods=["POST"])
def search():
    payload = request.get_json() or {}
    start = payload.get("start", "")
    goal = payload.get("goal", "")
    algorithm = (payload.get("algorithm", "") or "").lower().strip()

    map_data = load_map_data()
    graph = map_data.get("graph", {})
    locations = map_data.get("locations", {})

    if start not in locations or goal not in locations:
        return jsonify({
            "status": "error",
            "message": f"Invalid start ('{start}') or destination ('{goal}').",
            "path": [],
            "cost": 0,
            "nodes_expanded": 0
        }), 400

    path, cost, expanded = [], 0.0, 0

    if algorithm in ("bfs",):
        path, cost, expanded = bfs(graph, start, goal)
    elif algorithm in ("dfs",):
        path, cost, expanded = dfs(graph, start, goal)
    elif algorithm in ("ucs",):
        path, cost, expanded = ucs(graph, start, goal)
    elif algorithm in ("ids",):
        path, cost, expanded = ids(graph, start, goal)
    elif algorithm in ("greedy",):
        path, cost, expanded = greedy_best_first_search(graph, start, goal, locations)
    elif algorithm in ("astar", "a*"):
        path, cost, expanded = a_star_search(graph, start, goal, locations)
    else:
        return jsonify({
            "status": "error",
            "message": f"Unsupported algorithm '{algorithm}'",
            "path": [],
            "cost": 0,
            "nodes_expanded": 0
        }), 400

    return jsonify({
        "status": "success",
        "start": start,
        "goal": goal,
        "algorithm": algorithm,
        "path": path,
        "cost": cost,
        "nodes_expanded": expanded
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)