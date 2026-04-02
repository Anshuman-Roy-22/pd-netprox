"""Extract the substantia nigra median TPM column from the GTEx median matrix."""

from __future__ import annotations

import pandas as pd

from common import GTEX_GCT_CANDIDATES, GTEX_SN, ensure_parent, first_existing, relpath

SN_COLUMN = "Brain - Substantia nigra"


def main() -> None:
    gct_path = first_existing(GTEX_GCT_CANDIDATES)

    print("[1/3] Loading GTEx median expression matrix...")
    df = pd.read_csv(gct_path, sep="\t", skiprows=2, low_memory=False)

    if "Description" not in df.columns:
        raise RuntimeError(f"'Description' column not found in {relpath(gct_path)}")
    if SN_COLUMN not in df.columns:
        raise RuntimeError(f"'{SN_COLUMN}' column not found in {relpath(gct_path)}")

    print("[2/3] Extracting the substantia nigra TPM column...")
    df_sn = df[["Description", SN_COLUMN]].copy()
    df_sn = df_sn.rename(columns={"Description": "gene_symbol"})
    df_sn["gene_symbol"] = df_sn["gene_symbol"].astype(str).str.upper().str.strip()
    print(f"Prepared {len(df_sn):,} rows")

    print("[3/3] Writing reduced GTEx table...")
    ensure_parent(GTEX_SN)
    df_sn.to_csv(GTEX_SN, sep="\t", index=False)
    print(f"DONE: wrote {relpath(GTEX_SN)}")


if __name__ == "__main__":
    main()
