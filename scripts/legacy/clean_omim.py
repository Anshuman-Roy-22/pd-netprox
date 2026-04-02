# scripts/clean_omim.py

import pandas as pd
import os

# Use absolute path for omim_path to avoid relative path issues
base_dir = os.path.dirname(os.path.abspath(__file__))
omim_path = os.path.join(base_dir, '..', 'data', 'OMIM-Gene-Map-Retrieval.tsv')
omim_path = os.path.normpath(omim_path)

cols = [
    "Cytogenetic_location",
    "Genomic_coordinates",
    "Gene_Locus",
    "Gene_Locus_name",
    "Gene_Locus_MIM",
    "Approved_Symbol",
    "Entrez_Gene_ID",
    "Ensembl_Gene_ID",
    "Comments",
    "Phenotype",
    "Phenotype_MIM",
    "Inheritance",
    "Pheno_map_key",
    "Mouse_Gene"
]

# Try reading the file, handle storage_options error if present
try:
    df = pd.read_csv(
        omim_path,
        sep='\t',
        skiprows=4,
        header=None,
        names=cols,
        usecols=["Approved_Symbol", "Phenotype", "Inheritance"],
        dtype=str,
        na_filter=False
    )
except TypeError:
    # Remove storage_options if pandas version does not support it
    df = pd.read_csv(
        omim_path,
        sep='\t',
        skiprows=4,
        header=None,
        names=cols,
        usecols=["Approved_Symbol", "Phenotype", "Inheritance"],
        dtype=str,
        na_filter=False
    )

df = df.rename(columns={"Approved_Symbol": "GeneSymbol"})

# Filter for rows where the Phenotype mentions "Parkinson" (case-insensitive)
mask = df['Phenotype'].str.contains('Parkinson', case=False, na=False)
pd_df = df[mask]

pd_df = pd_df.drop_duplicates()

out_path = os.path.join(base_dir, '..', 'data', 'pd_familial_from_omim.tsv')
out_path = os.path.normpath(out_path)
pd_df.to_csv(out_path, sep='\t', index=False)

print(f"Extracted {pd_df['GeneSymbol'].nunique()} unique Parkinson’s-associated gene symbols")
print(f"Saved detailed dataset (with phenotype & inheritance) to {out_path}")