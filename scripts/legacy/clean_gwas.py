# scripts/clean_gwas_file.py

import pandas as pd
import os

BASE = os.path.dirname(os.path.abspath(__file__))
GWAS_IN = os.path.join(BASE, "..", "data", "gwas", "pd_gwas_associations.tsv")
GWAS_OUT = os.path.join(BASE, "..", "data", "gwas", "pd_gwas_genes.txt")

print("[1/4] Loading GWAS TSV...")
df = pd.read_csv(GWAS_IN, sep="\t", dtype=str).fillna("")

# Common gene columns used in GWAS TSV exports
possible_cols = ["MAPPED_GENE", "REPORTED GENE(S)", "MAPPED_GENES", "MAPPED_TRAIT"]

gene_col = None
for col in df.columns:
    if col.upper().replace(" ", "").replace("_", "") in \
        [c.replace(" ", "").replace("_", "") for c in possible_cols]:
        gene_col = col
        break

if gene_col is None:
    raise ValueError("Could not find a gene column in GWAS file.")

print(f"[2/4] Using gene column: {gene_col}")

# Split multiple gene names (comma, semicolon, slash)
genes_raw = (
    df[gene_col]
    .str.replace(",", ";")
    .str.replace("/", ";")
    .str.replace("|", ";")
    .str.split(";")
)

# Flatten + clean
clean_genes = set()
for gene_list in genes_raw:
    for g in gene_list:
        g = g.strip().upper()
        if g and g not in ["NR", "NA", ".", "-"]:
            # Remove text like "LOC12345" if desired
            if not g.startswith("LOC"):  
                clean_genes.add(g)

# Save output
clean_genes = sorted(clean_genes)

print(f"[3/4] Extracted {len(clean_genes)} cleaned GWAS genes.")

with open(GWAS_OUT, "w") as f:
    for g in clean_genes:
        f.write(g + "\n")

print(f"[4/4] Saved cleaned gene list → {GWAS_OUT}")
print("DONE.")
