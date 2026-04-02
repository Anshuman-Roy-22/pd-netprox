"""Compute protein-network proximity to monogenic PD seed genes."""

from __future__ import annotations

import pickle

import networkx as nx
import pandas as pd

from common import (
    GTEX_SN,
    PPI_GRAPH,
    RANKED_CANDIDATES,
    SEED_ENSP,
    STRING_INFO_CANDIDATES,
    ensure_parent,
    first_existing,
    read_nonempty_lines,
    relpath,
)

TPM_THRESHOLD = 1.0
SN_COLUMN = "Brain - Substantia nigra"


def main() -> None:
    info_path = first_existing(STRING_INFO_CANDIDATES)

    print("[1/7] Loading protein graph...")
    with PPI_GRAPH.open("rb") as handle:
        graph = pickle.load(handle)
    print(f"Graph: {graph.number_of_nodes():,} nodes, {graph.number_of_edges():,} edges")

    print("[2/7] Loading ENSP to gene-symbol mapping...")
    info = pd.read_csv(
        info_path,
        sep="\t",
        usecols=["protein_external_id", "preferred_name"],
        dtype=str,
    )
    ensp_to_gene = dict(zip(info["protein_external_id"], info["preferred_name"].str.upper()))
    print(f"Loaded {len(ensp_to_gene):,} mappings from {relpath(info_path)}")

    print("[3/7] Loading seed ENSP identifiers...")
    seeds = [seed for seed in read_nonempty_lines(SEED_ENSP) if seed in graph]
    print(f"Valid seed nodes in graph: {len(seeds):,}")
    if not seeds:
        raise RuntimeError("No seed ENSP identifiers were found in the graph")

    print("[4/7] Running multi-source Dijkstra...")
    distances = nx.multi_source_dijkstra_path_length(graph, seeds, weight="weight")
    print(f"Computed distances for {len(distances):,} proteins")

    print("[5/7] Converting ENSP IDs to gene symbols...")
    records = [
        (ensp_to_gene[ensp], ensp, distance)
        for ensp, distance in distances.items()
        if ensp in ensp_to_gene
    ]
    df = pd.DataFrame(records, columns=["gene_symbol", "ensp_id", "proximity"])

    print("[6/7] Adding substantia nigra TPM values...")
    gtex = pd.read_csv(GTEX_SN, sep="\t", dtype={"gene_symbol": str})
    gtex["gene_symbol"] = gtex["gene_symbol"].str.upper()
    if SN_COLUMN not in gtex.columns:
        raise RuntimeError(f"Missing '{SN_COLUMN}' column in {relpath(GTEX_SN)}")

    df = df.merge(gtex[["gene_symbol", SN_COLUMN]], on="gene_symbol", how="left")
    df = df.rename(columns={SN_COLUMN: "sn_tpm"})

    print(f"[7/7] Filtering genes with sn_tpm >= {TPM_THRESHOLD} and ranking...")
    df = df.loc[df["sn_tpm"].fillna(0) >= TPM_THRESHOLD].copy()
    df = df.loc[df["gene_symbol"].notna()].sort_values("proximity").reset_index(drop=True)

    ensure_parent(RANKED_CANDIDATES)
    df.to_csv(RANKED_CANDIDATES, sep="\t", index=False)
    print(f"DONE: wrote {relpath(RANKED_CANDIDATES)} with {len(df):,} ranked proteins")


if __name__ == "__main__":
    main()
