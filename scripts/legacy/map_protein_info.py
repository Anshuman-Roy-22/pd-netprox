import pandas as pd
import os

BASE = os.path.dirname(os.path.abspath(__file__))

INFO = os.path.join(BASE, "..", "data", "string", "9606.protein.info.v11.0.txt")
PPI_IN = os.path.join(BASE, "..", "data", "string", "ppi_edges.csv")
PPI_OUT = os.path.join(BASE, "..", "data", "string", "ppi_edges_genes.csv")

print("[1/4] Loading protein.info mapping...")

df_info = pd.read_csv(INFO, sep="\t")
mapping = dict(zip(df_info["protein_external_id"], df_info["preferred_name"]))

print(f"Loaded {len(mapping):,} ENSP → GeneSymbol mappings")

print("[2/4] Loading PPI edges...")
ppi = pd.read_csv(PPI_IN)

print("[3/4] Mapping ENSP IDs to gene symbols...")

ppi["geneA"] = ppi["protein1"].map(mapping)
ppi["geneB"] = ppi["protein2"].map(mapping)

ppi = ppi.dropna(subset=["geneA", "geneB"])

print(f"Mapped gene-level edges: {len(ppi):,}")

print("[4/4] Saving cleaned gene-level PPI...")
ppi[["geneA", "geneB", "combined_score"]].to_csv(PPI_OUT, index=False)

print("DONE — Saved:", PPI_OUT)
