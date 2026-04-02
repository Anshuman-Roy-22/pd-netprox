"""Filter the raw STRING interaction file to a high-confidence ENSP edge list."""

from __future__ import annotations

import pandas as pd

from common import PPI_EDGES, STRING_DETAILED_CANDIDATES, ensure_parent, first_existing, relpath

MIN_COMBINED_SCORE = 700


def main() -> None:
    ppi_in = first_existing(STRING_DETAILED_CANDIDATES)

    print("[1/3] Loading STRING detailed network...")
    df = pd.read_csv(
        ppi_in,
        sep=r"\s+",
        usecols=["protein1", "protein2", "combined_score"],
    )
    print(f"Loaded {len(df):,} raw interactions from {relpath(ppi_in)}")

    print(f"[2/3] Filtering edges with combined_score >= {MIN_COMBINED_SCORE}...")
    df_filtered = df.loc[df["combined_score"] >= MIN_COMBINED_SCORE].copy()
    print(f"Retained {len(df_filtered):,} high-confidence edges")

    print("[3/3] Writing filtered protein-level edge list...")
    ensure_parent(PPI_EDGES)
    df_filtered.to_csv(PPI_EDGES, index=False)
    print(f"DONE: wrote {relpath(PPI_EDGES)}")


if __name__ == "__main__":
    main()
