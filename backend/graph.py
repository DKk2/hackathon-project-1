"""Graph utilities for shortest-path campus navigation using NetworkX A*."""

from __future__ import annotations

import math
from typing import Any

import networkx as nx

from models import get_connection


def build_graph() -> nx.Graph:
    """Build and return a weighted graph from database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    graph = nx.Graph()

    buildings = cursor.execute(
        "SELECT name, x_coordinate, y_coordinate FROM Buildings"
    ).fetchall()

    for building in buildings:
        graph.add_node(
            building["name"],
            x=float(building["x_coordinate"]),
            y=float(building["y_coordinate"]),
        )

    connections = cursor.execute(
        "SELECT from_building, to_building, distance FROM Connections"
    ).fetchall()

    for connection in connections:
        graph.add_edge(
            connection["from_building"],
            connection["to_building"],
            weight=float(connection["distance"]),
        )

    conn.close()
    return graph


def heuristic(node_a: str, node_b: str, graph: nx.Graph) -> float:
    """Euclidean distance heuristic based on simulated building coordinates."""
    a = graph.nodes[node_a]
    b = graph.nodes[node_b]
    return math.dist((a["x"], a["y"]), (b["x"], b["y"]))


def shortest_path(start: str, end: str) -> dict[str, Any]:
    """Compute shortest path and step-by-step directions with A* pathfinding."""
    graph = build_graph()

    if start not in graph.nodes:
        raise ValueError(f"Start building '{start}' does not exist.")
    if end not in graph.nodes:
        raise ValueError(f"Destination building '{end}' does not exist.")

    path = nx.astar_path(graph, start, end, heuristic=lambda a, b: heuristic(a, b, graph), weight="weight")
    distance = nx.path_weight(graph, path, weight="weight")

    directions = []
    for i, current in enumerate(path):
        if i == 0:
            directions.append(f"You are at {current}")
        elif i == len(path) - 1:
            directions.append(f"Then go to {current} (Destination reached)")
        else:
            directions.append(f"Then go to {current}")

    return {
        "start": start,
        "end": end,
        "path": path,
        "total_distance": round(distance, 2),
        "directions": " → ".join(directions),
    }
