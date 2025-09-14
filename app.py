from flask import Flask, render_template, request, jsonify
from romania_map import bfs, dfs, ucs, dls, ids, astar, ao_star, genetic_algorithm, romania_map
import random

app = Flask(__name__)

city_coords = {
    "Arad": (100, 150),
    "Zerind": (120, 100),
    "Oradea": (140, 80),
    "Sibiu": (200, 160),
    "Timisoara": (80, 200),
    "Lugoj": (120, 230),
    "Mehadia": (140, 250),
    "Dobreta": (150, 270),
    "Craiova": (200, 300),
    "Rimnicu Vilcea": (220, 200),
    "Fagaras": (250, 150),
    "Pitesti": (250, 250),
    "Bucharest": (300, 270),
    "Giurgiu": (320, 300),
    "Urziceni": (350, 250),
    "Hirsova": (400, 220),
    "Eforie": (420, 260),
    "Vaslui": (380, 200),
    "Iasi": (400, 180),
    "Neamt": (380, 160)
}

@app.route("/")
def home():
    cities = list(romania_map.keys())
    start, end = random.sample(cities, 2)
    return render_template("index.html", cities=cities, start=start, end=end)

@app.route("/get-route", methods=["POST"])
def get_route():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")
    algo = data.get("algorithm", "").lower()

    cities = list(romania_map.keys())
    note = None

    if not start or not end or start == end:
        start, end = random.sample(cities, 2)
        note = f"No valid cities given. Choosing random route from {start} to {end}."

    if start not in romania_map or end not in romania_map:
        return jsonify({"error": "Invalid city name"}), 400

    if algo == "bfs":
        path, cost = bfs(start, end)
    elif algo == "dfs":
        path, cost = dfs(start, end)
        path = [step[0] for step in path] if path else None
    elif algo == "ucs":
        path, cost = ucs(start, end)
    elif algo == "dls":
        limit = 10  # example depth limit
        path, cost = dls(start, end, limit=limit)
        path = [step[0] for step in path] if path else None
    elif algo == "ids":
        path, cost = ids(start, end)
        path = [step[0] for step in path] if path else None
    elif algo == "astar":
        path, cost = astar(start, end)
    elif algo == "ao_star":
        path, cost = ao_star(start, end)
    elif algo == "genetic":
        path, cost = genetic_algorithm(start, end)
    else:
        return jsonify({"error": "Algorithm not supported"}), 400

    return jsonify({
        "path": path if path else [],
        "cost": cost if path else None,
        "note": note,
        "coords": [city_coords[c] for c in path] if path else []
    })

if __name__ == "__main__":
    app.run(debug=True)
