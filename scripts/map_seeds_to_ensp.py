"""Map monogenic PD seed genes to STRING ENSP identifiers using local alias files."""

from __future__ import annotations

import pandas as pd

from common import (
    SEED_ENSP,
    SEED_GENES,
    SEED_MAPPING,
    STRING_ALIASES_CANDIDATES,
    STRING_INFO_CANDIDATES,
    ensure_parent,
    first_existing,
    read_nonempty_lines,
    relpath,
)


def choose_seed_match(seed: str, matches: pd.DataFrame) -> pd.Series:
    if matches.empty:
        raise RuntimeError(f"No STRING alias match found for seed gene {seed}")

    exact_name = matches.loc[matches["preferred_name_upper"] == seed].copy()
    if not exact_name.empty:
        return exact_name.sort_values(["preferred_name", "string_protein_id"]).iloc[0]

    unique_ids = sorted(matches["string_protein_id"].unique())
    if len(unique_ids) > 1:
        raise RuntimeError(
            "Ambiguous STRING alias mapping for "
            f"{seed}: {', '.join(unique_ids[:10])}"
        )

    return matches.sort_values(["preferred_name", "string_protein_id"]).iloc[0]


def main() -> None:
    aliases_path = first_existing(STRING_ALIASES_CANDIDATES)
    info_path = first_existing(STRING_INFO_CANDIDATES)
    seeds = [seed.upper() for seed in read_nonempty_lines(SEED_GENES)]

    print("[1/4] Loading STRING alias table...")
    aliases = pd.read_csv(
        aliases_path,
        sep="\t",
        header=None,
        skiprows=1,
        names=["string_protein_id", "alias", "source"],
        dtype=str,
    )
    aliases["alias_upper"] = aliases["alias"].str.upper()

    print("[2/4] Loading STRING protein annotations...")
    info = pd.read_csv(
        info_path,
        sep="\t",
        usecols=["protein_external_id", "preferred_name"],
        dtype=str,
    )
    info["preferred_name_upper"] = info["preferred_name"].str.upper()
    info = info.rename(columns={"protein_external_id": "string_protein_id"})

    aliases = aliases.merge(info, on="string_protein_id", how="left")
    aliases["preferred_name_upper"] = aliases["preferred_name_upper"].fillna("")

    print("[3/4] Resolving seed genes to ENSP IDs...")
    records: list[dict[str, str]] = []
    missing: list[str] = []

    for seed in seeds:
        matches = aliases.loc[aliases["alias_upper"] == seed].copy()
        if matches.empty:
            missing.append(seed)
            continue

        selected = choose_seed_match(seed, matches)
        records.append(
            {
                "seed_gene": seed,
                "ensp_id": selected["string_protein_id"],
                "preferred_name": selected["preferred_name"],
                "matched_alias": selected["alias"],
                "source": selected["source"],
            }
        )

    if missing:
        raise RuntimeError(
            "Missing STRING aliases for these seed genes: " + ", ".join(sorted(missing))
        )

    mapping_df = pd.DataFrame(records).drop_duplicates(subset=["seed_gene"])
    mapping_df = mapping_df.sort_values("seed_gene").reset_index(drop=True)

    print("[4/4] Writing seed mapping outputs...")
    ensure_parent(SEED_MAPPING)
    ensure_parent(SEED_ENSP)
    mapping_df.to_csv(SEED_MAPPING, sep="\t", index=False)
    SEED_ENSP.write_text(
        "".join(f"{ensp_id}\n" for ensp_id in mapping_df["ensp_id"]),
        encoding="utf-8",
    )

    print(f"Wrote {relpath(SEED_MAPPING)}")
    print(f"Wrote {relpath(SEED_ENSP)} with {len(mapping_df):,} ENSP identifiers")


if __name__ == "__main__":
    main()
