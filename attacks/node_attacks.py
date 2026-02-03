"""Node attack strategies: random, degree, betweenness, Fiedler-magnitude."""

import numpy as np
import networkx as nx

from metrics.spectral import fiedler_vector
from metrics.robustness import giant_component_subgraph


def _ordered_nodes(G):
    return list(G.nodes())


def _sort_by_score(nodes, scores):
    # Stable sort by score descending, tie-break by original order.
    indexed = [(scores[n], i, n) for i, n in enumerate(nodes)]
    indexed.sort(key=lambda x: (-x[0], x[1]))
    return [n for _, _, n in indexed]


def random_attack(G, seed=None):
    nodes = _ordered_nodes(G)
    rng = np.random.default_rng(seed)
    rng.shuffle(nodes)
    return nodes


def degree_attack(G, use_undirected=True, weight=None):
    H = G.to_undirected() if use_undirected and G.is_directed() else G
    nodes = _ordered_nodes(H)
    degrees = dict(H.degree(weight=weight))
    return _sort_by_score(nodes, degrees)


def betweenness_attack(G, use_undirected=True, weight=None, normalized=True):
    H = G.to_undirected() if use_undirected and G.is_directed() else G
    nodes = _ordered_nodes(H)
    centrality = nx.betweenness_centrality(H, weight=weight, normalized=normalized)
    return _sort_by_score(nodes, centrality)


def fiedler_attack(G, use_undirected=True):
    if G.number_of_nodes() <= 1:
        return _ordered_nodes(G)
    H = G.to_undirected() if use_undirected and G.is_directed() else G
    # Fiedler vector requires connectivity; compute on giant component.
    GCC = giant_component_subgraph(H, kind="weak")
    gcc_nodes = _ordered_nodes(GCC)
    if len(gcc_nodes) <= 1:
        return _ordered_nodes(H)

    vec = fiedler_vector(GCC)
    magnitudes = {n: abs(v) for n, v in zip(gcc_nodes, vec)}
    ordered_gcc = _sort_by_score(gcc_nodes, magnitudes)

    # Append nodes not in GCC in their original order.
    gcc_set = set(gcc_nodes)
    remaining = [n for n in _ordered_nodes(H) if n not in gcc_set]
    return ordered_gcc + remaining
