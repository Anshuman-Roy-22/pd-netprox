"""Write the top 20 non-seed candidates from the ranked proximity table."""

from __future__ import annotations

import pandas as pd

from common import (
    RANKED_CANDIDATES,
    SEED_ENSP,
    SEED_GENES,
    TOP20_CANDIDATES,
    TOP20_GENE_LIST,
    ensure_parent,
    read_nonempty_lines,
    relpath,
)


def main() -> None:
    print("[1/3] Loading ranked candidates...")
    df = pd.read_csv(RANKED_CANDIDATES, sep="\t")
    if "gene_symbol" not in df.columns:
        raise RuntimeError(f"'gene_symbol' column not found in {relpath(RANKED_CANDIDATES)}")

    print("[2/3] Loading monogenic seed genes...")
    seeds = {seed.upper() for seed in read_nonempty_lines(SEED_GENES)}
    seed_ensp = set(read_nonempty_lines(SEED_ENSP))

    df_nonseed = df.loc[~df["gene_symbol"].str.upper().isin(seeds)].copy()
    if "ensp_id" in df_nonseed.columns:
        df_nonseed = df_nonseed.loc[~df_nonseed["ensp_id"].astype(str).isin(seed_ensp)].copy()
    top20 = df_nonseed.sort_values("proximity").head(20)

    print("[3/3] Writing top 20 outputs...")
    ensure_parent(TOP20_CANDIDATES)
    ensure_parent(TOP20_GENE_LIST)
    top20.to_csv(TOP20_CANDIDATES, sep="\t", index=False)
    TOP20_GENE_LIST.write_text(
        "".join(f"{gene}\n" for gene in top20["gene_symbol"]),
        encoding="utf-8",
    )

    print(f"Wrote {relpath(TOP20_CANDIDATES)}")
    print(f"Wrote {relpath(TOP20_GENE_LIST)}")


if __name__ == "__main__":
    main()
