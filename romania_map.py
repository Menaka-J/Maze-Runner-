import heapq
import random

# Romania map as given
romania_map = {
    'Arad': [('Zerind', 75), ('Timisoara', 118), ('Sibiu', 140)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Dobreta', 75)],
    'Dobreta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Dobreta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)],
}

# Heuristic values for A* (straight-line distance to Bucharest as an example)
heuristic = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Dobreta': 242,
    'Eforie': 161, 'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151,
    'Iasi': 226, 'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
    'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193, 'Sibiu': 253,
    'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
}

# ---------------- BFS ----------------
def bfs(start, goal):
    visited = set()
    queue = [[(start, 0)]]

    while queue:
        path = queue.pop(0)
        city = path[-1][0]

        if city == goal:
            total_cost = sum(step[1] for step in path[1:])
            return [step[0] for step in path], total_cost

        if city not in visited:
            for neighbor, cost in romania_map.get(city, []):
                new_path = list(path)
                new_path.append((neighbor, cost))
                queue.append(new_path)
            visited.add(city)
    return None, float('inf')

# ---------------- DFS ----------------
def dfs(start, goal, visited=None, path=None, cost=0):
    if visited is None:
        visited = set()
    if path is None:
        path = [(start, 0)]

    if start == goal:
        return path, cost

    visited.add(start)

    for neighbor, step_cost in romania_map.get(start, []):
        if neighbor not in visited:
            new_path, total_cost = dfs(neighbor, goal, visited.copy(), path + [(neighbor, step_cost)], cost + step_cost)
            if new_path:
                return new_path, total_cost

    return None, float('inf')

# ---------------- UCS ----------------
def ucs(start, goal):
    visited = set()
    queue = [(0, [start])]

    while queue:
        cost, path = heapq.heappop(queue)
        city = path[-1]

        if city == goal:
            return path, cost

        if city not in visited:
            visited.add(city)
            for neighbor, step_cost in romania_map.get(city, []):
                heapq.heappush(queue, (cost + step_cost, path + [neighbor]))

    return None, float('inf')

# ---------------- Depth Limited Search (DLS) ----------------
def dls(start, goal, limit, path=None, cost=0):
    if path is None:
        path = [(start, 0)]

    if start == goal:
        return path, cost

    if limit <= 0:
        return None, float('inf')

    for neighbor, step_cost in romania_map.get(start, []):
        if neighbor not in [city for city, _ in path]:
            new_path, new_cost = dls(neighbor, goal, limit - 1, path + [(neighbor, step_cost)], cost + step_cost)
            if new_path:
                return new_path, new_cost

    return None, float('inf')

# ---------------- Iterative Deepening Search (IDS) ----------------
def ids(start, goal, max_depth=50):
    for depth in range(max_depth):
        result, cost = dls(start, goal, depth)
        if result:
            return result, cost
    return None, float('inf')

# ---------------- A* Search ----------------
def astar(start, goal):
    visited = set()
    queue = [(heuristic[start], 0, [start])]

    while queue:
        estimated_total, cost_so_far, path = heapq.heappop(queue)
        city = path[-1]

        if city == goal:
            return path, cost_so_far

        if city not in visited:
            visited.add(city)
            for neighbor, step_cost in romania_map.get(city, []):
                new_cost = cost_so_far + step_cost
                estimated = new_cost + heuristic.get(neighbor, float('inf'))
                heapq.heappush(queue, (estimated, new_cost, path + [neighbor]))

    return None, float('inf')

# ---------------- AO* Search (Simplified version) ----------------
def ao_star(start, goal):
    visited = set()
    queue = [(heuristic[start], 0, [start])]

    while queue:
        estimated_total, cost_so_far, path = heapq.heappop(queue)
        city = path[-1]

        if city == goal:
            return path, cost_so_far

        if city not in visited:
            visited.add(city)
            children = romania_map.get(city, [])
            for neighbor, step_cost in children:
                if neighbor not in visited:
                    new_cost = cost_so_far + step_cost
                    estimated = new_cost + heuristic.get(neighbor, float('inf'))
                    heapq.heappush(queue, (estimated, new_cost, path + [neighbor]))

    return None, float('inf')

# ---------------- Genetic Algorithm (Simplified for pathfinding) ----------------
def genetic_algorithm(start, goal, population_size=50, generations=100, mutation_rate=0.1):
    def create_individual():
        path = [start]
        while path[-1] != goal:
            neighbors = romania_map.get(path[-1], [])
            if not neighbors:
                break
            next_city = random.choice(neighbors)[0]
            if next_city not in path:
                path.append(next_city)
        return path

    def fitness(path):
        total = 0
        for i in range(len(path) - 1):
            for neighbor, cost in romania_map.get(path[i], []):
                if neighbor == path[i + 1]:
                    total += cost
                    break
        if path[-1] != goal:
            total += 1000  # penalty
        return total

    def mutate(path):
        if random.random() < mutation_rate:
            idx = random.randint(1, len(path) - 1)
            neighbors = romania_map.get(path[idx - 1], [])
            if neighbors:
                path[idx] = random.choice(neighbors)[0]
        return path

    def crossover(parent1, parent2):
        cut = random.randint(1, min(len(parent1), len(parent2)) - 1)
        child = parent1[:cut]
        for city in parent2:
            if city not in child:
                child.append(city)
        return child

    population = [create_individual() for _ in range(population_size)]
    for generation in range(generations):
        population = sorted(population, key=fitness)
        if fitness(population[0]) < 1000 and population[0][-1] == goal:
            return population[0], fitness(population[0])
        next_generation = population[:10]  # keep top 10
        while len(next_generation) < population_size:
            p1, p2 = random.sample(population[:20], 2)
            child = crossover(p1, p2)
            child = mutate(child)
            next_generation.append(child)
        population = next_generation

    return population[0], fitness(population[0])
