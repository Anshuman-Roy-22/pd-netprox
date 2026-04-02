import pandas as pd
import numpy as np
import networkx as nx
from pathlib import Path

# Load seeds
seeds = [l.strip() for l in open("data/seeds/monogenic_genes.txt")]

# Load PPI
print("Loading STRING network...")
ppi = pd.read_csv("data/string/protein.links.full.v11.0.txt.gz", sep=" ", header=None, 
                  names=["geneA","geneB","score"])
ppi = ppi[ppi["score"] >= 700]

# Build weighted graph
G = nx.Graph()
for _, r in ppi.iterrows():
    G.add_edge(r["geneA"], r["geneB"], weight=1 / (r["score"]/1000))

# Dijkstra proximity
print("Running Dijkstra proximity...")
prox = {}
for g in G.nodes:
    d = []
    for s in seeds:
        if s in G:
            try:
                d.append(nx.dijkstra_path_length(G, g, s, weight="weight"))
            except nx.NetworkXNoPath:
                pass
    if d:
        prox[g] = min(d)

# Load expression
expr = pd.read_csv("data/expression/gtex_sn_expression.tsv", sep="\t")
expr = expr.set_index("gene_symbol")

# Prioritize candidates in SN
cands = []
for g, p in prox.items():
    if g in expr.index:
        cands.append((g, p, expr.loc[g]["SN_Median_TPM"]))

# Sort best proximity first
cands = sorted(cands, key=lambda x: x[1])

# Save top 5
Path("results").mkdir(exist_ok=True)
with open("results/top_genes.txt","w") as f:
    for gene, p, tpm in cands[:5]:
        f.write(f"{gene}\t{p:.4f}\t{tpm:.2f}\n")

print("Top 5 genes saved.")
