"""
Undergrad

Implemented informed search algorithms:
  1. Greedy Best-First Search
  2. A* Search
"""

import math
import heapq


def haversine_miles(coord1, coord2):
    #Calculates distance between two coordinates in miles.
    
    lat1, lon1 = coord1["lat"], coord1["lon"]
    lat2, lon2 = coord2["lat"], coord2["lon"]
    R = 3958.8  # Earth radius in miles

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def greedy_best_first_search(graph, start, goal, locations):
    #Greedy Best-First Search.
    counter = 0
    initial_h = haversine_miles(locations[start], locations[goal])
    pq = [(initial_h, counter, start, [start], 0.0)]
    visited = set()
    nodes_expanded = 0

    while pq:
        h_val, _, curr, path, cost = heapq.heappop(pq)
        nodes_expanded += 1

        if curr == goal:
            return path, round(cost, 2), nodes_expanded

        if curr in visited:
            continue
        visited.add(curr)

        for neighbor, weight in sorted(graph.get(curr, {}).items()):
            if neighbor not in visited:
                counter += 1
                h_next = haversine_miles(locations[neighbor], locations[goal])
                heapq.heappush(pq, (h_next, counter, neighbor, path + [neighbor], cost + weight))

    return [], 0.0, nodes_expanded


def a_star_search(graph, start, goal, locations):
    # A* Search
    counter = 0
    initial_h = haversine_miles(locations[start], locations[goal])
    pq = [(initial_h, 0.0, counter, start, [start])]
    g_costs = {start: 0.0}
    nodes_expanded = 0

    while pq:
        f, g, _, curr, path = heapq.heappop(pq)
        nodes_expanded += 1

        if curr == goal:
            return path, round(g, 2), nodes_expanded

        if g > g_costs.get(curr, float('inf')):
            continue

        for neighbor, weight in sorted(graph.get(curr, {}).items()):
            tentative_g = g + weight
            if tentative_g < g_costs.get(neighbor, float('inf')):
                g_costs[neighbor] = tentative_g
                h = haversine_miles(locations[neighbor], locations[goal])
                f_score = tentative_g + h
                counter += 1
                heapq.heappush(pq, (f_score, tentative_g, counter, neighbor, path + [neighbor]))

    return [], 0.0, nodes_expanded
