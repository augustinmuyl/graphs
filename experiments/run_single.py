"""Run a single graph + attack experiment and write CSV metrics."""

from __future__ import annotations

import sys

import argparse
import csv
from pathlib import Path

# Allow running this script directly from the repo root.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from attacks import betweenness_attack, degree_attack, fiedler_attack, random_attack
from graph_operations.generators import (
    create_complete_graph,
    create_erdos_renyi_graph,
    create_scale_free_graph,
    create_small_world_graph,
)
from metrics.robustness import (
    average_shortest_path_length_giant_component,
    giant_component_subgraph,
    largest_component_size,
    number_of_components,
)
from metrics.spectral import (
    algebraic_connectivity,
    kirchhoff_index,
    spectral_gap_ratio,
)


GENERATOR_MAP = {
    "complete": create_complete_graph,
    "erdos_renyi": create_erdos_renyi_graph,
    "small_world": create_small_world_graph,
    "scale_free": create_scale_free_graph,
}

ATTACK_MAP = {
    "random": random_attack,
    "degree": degree_attack,
    "betweenness": betweenness_attack,
    "fiedler": fiedler_attack,
}


def _build_graph(args):
    if args.graph == "complete":
        return create_complete_graph(n=args.n)
    if args.graph == "erdos_renyi":
        return create_erdos_renyi_graph(n=args.n, p=args.p)
    if args.graph == "small_world":
        return create_small_world_graph(n=args.n, k=args.k, p=args.p)
    if args.graph == "scale_free":
        return create_scale_free_graph(n=args.n, m=args.m)
    raise ValueError(f"Unknown graph type: {args.graph}")


def _removal_checkpoints(n, num_steps):
    if num_steps is None or num_steps >= n:
        return list(range(0, n + 1))
    checkpoints = np.unique(np.round(np.linspace(0, n, num_steps + 1)).astype(int))
    checkpoints[0] = 0
    checkpoints[-1] = n
    return list(checkpoints)


def run_experiment(G, attack_order, num_steps=None, kind="weak", weight=None):
    n = G.number_of_nodes()
    checkpoints = _removal_checkpoints(n, num_steps)

    H = G.copy()
    removed = 0

    rows = []
    for target in checkpoints:
        while removed < target and removed < n:
            node = attack_order[removed]
            if H.has_node(node):
                H.remove_node(node)
            removed += 1

        gcc_size = largest_component_size(H, kind=kind)
        gcc_fraction = (gcc_size / n) if n > 0 else 0.0
        components = number_of_components(H, kind=kind)
        avg_sp = average_shortest_path_length_giant_component(H, kind=kind, weight=weight)
        gcc = giant_component_subgraph(H, kind=kind)
        if gcc.is_directed() and kind in ("weak", "undirected"):
            gcc = gcc.to_undirected()

        algebraic_conn = None
        spectral_ratio = None
        kirchhoff = None
        if gcc.number_of_nodes() >= 2:
            algebraic_conn = algebraic_connectivity(gcc)
            spectral_ratio = spectral_gap_ratio(gcc)
            try:
                kirchhoff = kirchhoff_index(gcc)
            except ValueError:
                kirchhoff = None

        rows.append(
            {
                "removed_fraction": removed / n if n > 0 else 0.0,
                "removed_nodes": removed,
                "gcc_fraction": gcc_fraction,
                "gcc_size": gcc_size,
                "num_components": components,
                "avg_shortest_path_gcc": avg_sp,
                "algebraic_connectivity_gcc": algebraic_conn,
                "spectral_gap_ratio_gcc": spectral_ratio,
                "kirchhoff_index_gcc": kirchhoff,
            }
        )

    return rows


def main():
    parser = argparse.ArgumentParser(description="Run one graph/attack and write CSV.")
    parser.add_argument("--graph", choices=GENERATOR_MAP.keys(), default="erdos_renyi")
    parser.add_argument("--attack", choices=ATTACK_MAP.keys(), default="random")
    parser.add_argument("--n", type=int, default=100)
    parser.add_argument("--p", type=float, default=0.05)
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--m", type=int, default=3)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--num-steps", type=int, default=None)
    parser.add_argument("--kind", choices=["weak", "strong", "undirected"], default="weak")
    parser.add_argument("--weight", default=None)
    parser.add_argument("--out", default="results.csv")

    args = parser.parse_args()

    G = _build_graph(args)

    attack_fn = ATTACK_MAP[args.attack]
    if args.attack == "random":
        attack_order = attack_fn(G, seed=args.seed)
    else:
        attack_order = attack_fn(G)

    rows = run_experiment(
        G,
        attack_order,
        num_steps=args.num_steps,
        kind=args.kind,
        weight=args.weight,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "removed_fraction",
                "removed_nodes",
                "gcc_fraction",
                "gcc_size",
                "num_components",
                "avg_shortest_path_gcc",
                "algebraic_connectivity_gcc",
                "spectral_gap_ratio_gcc",
                "kirchhoff_index_gcc",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
