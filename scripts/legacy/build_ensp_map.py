import pandas as pd
import os

INFO = os.path.join("data","string","9606.protein.info.v11.0.txt")
OUT = os.path.join("data","string","ensp_to_gene.csv")

df = pd.read_csv(INFO, sep="\t")

df = df[["protein_external_id", "preferred_name"]]

df.to_csv(OUT, index=False)

print("Saved:", OUT)
print("Total mappings:", len(df))
