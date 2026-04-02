import pandas as pd
import os

PPI = os.path.join("data","string","ppi_edges.csv")
MAP = os.path.join("data","string","ensp_to_gene.csv")
OUT = os.path.join("data","string","ppi_edges_genes.csv")

ppi = pd.read_csv(PPI)
mapping = pd.read_csv(MAP)

map_dict = dict(zip(mapping["protein_external_id"], mapping["preferred_name"]))

ppi["geneA"] = ppi["protein1"].map(map_dict)
ppi["geneB"] = ppi["protein2"].map(map_dict)

ppi = ppi.dropna(subset=["geneA","geneB"])

ppi[["geneA","geneB","combined_score"]].to_csv(OUT, index=False)

print("Mapped edges:", len(ppi))
print("Saved:", OUT)
