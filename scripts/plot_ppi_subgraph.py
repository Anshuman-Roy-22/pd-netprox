"""Plot a local STRING subgraph around the seed and top-20 candidate proteins."""

from __future__ import annotations

import pickle

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from common import (
    PPI_GRAPH,
    PPI_SUBGRAPH_PLOT,
    SEED_ENSP,
    TOP20_CANDIDATES,
    ensure_parent,
    read_nonempty_lines,
    relpath,
)


def main() -> None:
    print("[1/5] Loading PPI graph...")
    with PPI_GRAPH.open("rb") as handle:
        graph = pickle.load(handle)
    print(f"Graph: {graph.number_of_nodes():,} nodes, {graph.number_of_edges():,} edges")

    print("[2/5] Loading top 20 candidates...")
    top20_df = pd.read_csv(TOP20_CANDIDATES, sep="\t")
    top20_nodes = set(top20_df["ensp_id"].astype(str))

    print("[3/5] Loading seed ENSP identifiers...")
    seed_nodes = set(read_nonempty_lines(SEED_ENSP))

    graph_nodes = set(graph.nodes())
    top20_nodes &= graph_nodes
    seed_nodes &= graph_nodes
    focus_nodes = top20_nodes | seed_nodes

    print(f"Seeds in graph: {len(seed_nodes):,}; top20 in graph: {len(top20_nodes):,}")
    if not focus_nodes:
        raise RuntimeError("No seed or top-20 nodes were found in the graph")

    print("[4/5] Building local neighborhood subgraph...")
    sub_nodes = set(focus_nodes)
    for node in focus_nodes:
        sub_nodes.update(graph.neighbors(node))

    subgraph = graph.subgraph(sub_nodes).copy()
    print(f"Subgraph: {subgraph.number_of_nodes():,} nodes, {subgraph.number_of_edges():,} edges")

    print("[5/5] Writing figure...")
    pos = nx.spring_layout(subgraph, k=0.15, seed=42)
    node_colors = []
    for node in subgraph.nodes():
        if node in seed_nodes:
            node_colors.append("red")
        elif node in top20_nodes:
            node_colors.append("gold")
        else:
            node_colors.append("lightgray")

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(subgraph, pos, node_size=40, node_color=node_colors, alpha=0.8)
    nx.draw_networkx_edges(subgraph, pos, width=0.3, alpha=0.5)

    ensp_to_symbol = dict(zip(top20_df["ensp_id"], top20_df["gene_symbol"]))
    labels = {node: ensp_to_symbol[node] for node in subgraph.nodes() if node in ensp_to_symbol}
    nx.draw_networkx_labels(subgraph, pos, labels=labels, font_size=6)

    plt.axis("off")
    plt.title("Neighborhood of monogenic PD seeds and top-20 candidates in STRING")
    plt.tight_layout()

    ensure_parent(PPI_SUBGRAPH_PLOT)
    plt.savefig(PPI_SUBGRAPH_PLOT, dpi=300)
    print(f"Wrote {relpath(PPI_SUBGRAPH_PLOT)}")


if __name__ == "__main__":
    main()
