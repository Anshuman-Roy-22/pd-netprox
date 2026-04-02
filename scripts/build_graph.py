"""Build the protein-level NetworkX graph used by the proximity model."""

from __future__ import annotations

import pickle

import networkx as nx
import pandas as pd

from common import PPI_EDGES, PPI_GRAPH, ensure_parent, relpath


def main() -> None:
    print("[1/2] Loading filtered STRING edges...")
    df = pd.read_csv(PPI_EDGES)
    required_cols = {"protein1", "protein2", "combined_score"}
    missing = required_cols - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing columns in {relpath(PPI_EDGES)}: {sorted(missing)}")

    if (df["combined_score"] <= 0).any():
        raise RuntimeError("Found non-positive combined_score values")

    print(f"Loaded {len(df):,} edges")

    print("[2/2] Building weighted ENSP graph...")
    df["weight"] = 1000.0 / df["combined_score"]
    graph = nx.from_pandas_edgelist(
        df,
        source="protein1",
        target="protein2",
        edge_attr=["weight", "combined_score"],
    )

    ensure_parent(PPI_GRAPH)
    with PPI_GRAPH.open("wb") as handle:
        pickle.dump(graph, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(
        "DONE: wrote "
        f"{relpath(PPI_GRAPH)} with {graph.number_of_nodes():,} nodes and "
        f"{graph.number_of_edges():,} edges"
    )


if __name__ == "__main__":
    main()
