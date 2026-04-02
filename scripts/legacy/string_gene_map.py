# scripts/build_string_gene_map.py

import pandas as pd
import os

INFO = "data/string/9606.protein.info.v11.0.txt"

df = pd.read_csv(INFO, sep="\t")

mapping = dict(zip(
    df["protein_external_id"].str.replace("9606.", "", regex=False),
    df["preferred_name"].str.upper()
))

pd.Series(mapping).to_csv("data/string/string_to_gene.csv")
print("Mappings:", len(mapping))
