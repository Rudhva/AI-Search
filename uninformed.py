"""
Implemented of uninformed search algorithms:
  1. Breadth-First Search (BFS)
  2. Depth-First Search (DFS)
  3. Uniform-Cost Search (UCS)
  4. Iterative Deepening Search (IDS)
"""

from collections import deque
import heapq


def calculate_path_cost(graph, path):
    # Calculates total road distance in miles for the given path between cities
    if not path or len(path) < 2:
        return 0.0
    cost = 0.0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i + 1]]
    return round(cost, 2)


def bfs(graph, start, goal):
    if start == goal:
        return [start], 0.0, 1

    frontier = deque([[start]])
    explored = {start}
    nodes_expanded = 0

    while frontier:
        path = frontier.popleft()
        curr = path[-1]
        nodes_expanded += 1

        if curr == goal:
            return path, calculate_path_cost(graph, path), nodes_expanded

        for neighbor in sorted(graph.get(curr, {}).keys()):
            if neighbor not in explored:
                explored.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                if neighbor == goal:
                    # Found goal Node
                    nodes_expanded += 1
                    return new_path, calculate_path_cost(graph, new_path), nodes_expanded
                frontier.append(new_path)

    return [], 0.0, nodes_expanded


def dfs(graph, start, goal):
    if start == goal:
        return [start], 0.0, 1

    frontier = [(start, [start])]
    explored = set()
    nodes_expanded = 0

    while frontier:
        curr, path = frontier.pop()
        nodes_expanded += 1

        if curr == goal:
            return path, calculate_path_cost(graph, path), nodes_expanded

        if curr not in explored:
            explored.add(curr)
            # Push in reverse sorted order so alphabetical order is popped first
            for neighbor in sorted(graph.get(curr, {}).keys(), reverse=True):
                if neighbor not in explored:
                    frontier.append((neighbor, path + [neighbor]))

    return [], 0.0, nodes_expanded


def ucs(graph, start, goal):
    # Priority queue - (cumulative_cost, tie_breaker_counter, current_node, path)
    counter = 0
    pq = [(0.0, counter, start, [start])]
    visited_cost = {}
    nodes_expanded = 0

    while pq:
        cost, _, curr, path = heapq.heappop(pq)
        nodes_expanded += 1

        if curr == goal:
            return path, round(cost, 2), nodes_expanded

        if curr in visited_cost and visited_cost[curr] <= cost:
            continue
        visited_cost[curr] = cost

        for neighbor, weight in sorted(graph.get(curr, {}).items()):
            new_cost = cost + weight
            if neighbor not in visited_cost or new_cost < visited_cost[neighbor]:
                counter += 1
                heapq.heappush(pq, (new_cost, counter, neighbor, path + [neighbor]))

    return [], 0.0, nodes_expanded


def ids(graph, start, goal, max_depth=50):
    total_nodes_expanded = 0

    def dls(curr, target, limit, current_depth, path, visited):
        nonlocal total_nodes_expanded
        total_nodes_expanded += 1

        if curr == target:
            return path

        if current_depth >= limit:
            return None

        for neighbor in sorted(graph.get(curr, {}).keys()):
            if neighbor not in visited:
                visited.add(neighbor)
                result = dls(neighbor, target, limit, current_depth + 1, path + [neighbor], visited)
                if result is not None:
                    return result
                visited.remove(neighbor)
        return None

    for depth in range(max_depth):
        visited = {start}
        found_path = dls(start, goal, depth, 0, [start], visited)
        if found_path is not None:
            return found_path, calculate_path_cost(graph, found_path), total_nodes_expanded

    return [], 0.0, total_nodes_expanded