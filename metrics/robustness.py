"""Robustness metrics: connectivity, geodesic length, percolation curve."""

import numpy as np
import networkx as nx


def _component_sets(G, kind="weak"):
    if G.number_of_nodes() == 0:
        return []
    if G.is_directed():
        if kind == "strong":
            return list(nx.strongly_connected_components(G))
        if kind in ("weak", "undirected"):
            return list(nx.weakly_connected_components(G))
        raise ValueError("kind must be 'weak', 'strong', or 'undirected'.")
    if kind == "strong":
        return list(nx.connected_components(G))
    if kind in ("weak", "undirected"):
        return list(nx.connected_components(G))
    raise ValueError("kind must be 'weak', 'strong', or 'undirected'.")


def largest_component_size(G, kind="weak"):
    components = _component_sets(G, kind=kind)
    if not components:
        return 0
    return max(len(c) for c in components)


def number_of_components(G, kind="weak"):
    return len(_component_sets(G, kind=kind))


def giant_component_subgraph(G, kind="weak"):
    components = _component_sets(G, kind=kind)
    if not components:
        return G.subgraph([]).copy()
    largest = max(components, key=len)
    return G.subgraph(largest).copy()


def average_shortest_path_length_giant_component(G, kind="weak", weight=None):
    H = giant_component_subgraph(G, kind=kind)
    if H.number_of_nodes() <= 1:
        return 0.0
    H_for_paths = H
    if H.is_directed() and kind in ("weak", "undirected"):
        H_for_paths = H.to_undirected()
    return nx.average_shortest_path_length(H_for_paths, weight=weight)


def _normalize_removal_order(G, removal_order):
    nodes = list(G.nodes())
    if removal_order is None:
        return nodes
    node_set = set(nodes)
    order = [n for n in removal_order if n in node_set]
    if len(order) < len(nodes):
        remaining = [n for n in nodes if n not in set(order)]
        order.extend(remaining)
    return order


def percolation_curve(G, removal_order=None, num_steps=None, kind="weak", seed=None):
    """Compute giant-component fraction vs removed fraction.

    Returns (removed_fractions, giant_component_fractions).
    """
    n = G.number_of_nodes()
    if n == 0:
        return [0.0], [0.0]

    order = _normalize_removal_order(G, removal_order)
    if removal_order is None:
        rng = np.random.default_rng(seed)
        rng.shuffle(order)

    if num_steps is None or num_steps >= n:
        checkpoints = list(range(0, n + 1))
    else:
        checkpoints = np.unique(np.round(np.linspace(0, n, num_steps + 1)).astype(int))
        checkpoints[0] = 0
        checkpoints[-1] = n

    H = G.copy()
    removed = 0
    removed_fractions = []
    giant_fractions = []

    for target in checkpoints:
        while removed < target and removed < n:
            node = order[removed]
            if H.has_node(node):
                H.remove_node(node)
            removed += 1
        gc_size = largest_component_size(H, kind=kind)
        removed_fractions.append(removed / n)
        giant_fractions.append(gc_size / n)

    return removed_fractions, giant_fractions
