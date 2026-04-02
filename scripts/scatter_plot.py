"""Plot proximity against GTEx substantia nigra expression."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr

from common import PROXIMITY_PLOT, RANKED_CANDIDATES, ensure_parent, relpath


def main() -> None:
    print("[1/5] Loading ranked candidates...")
    df = pd.read_csv(RANKED_CANDIDATES, sep="\t")

    required_cols = {"gene_symbol", "proximity", "sn_tpm"}
    missing = required_cols - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing columns in {relpath(RANKED_CANDIDATES)}: {sorted(missing)}")

    print("[2/5] Filtering TPM outliers using the IQR rule...")
    q1 = df["sn_tpm"].quantile(0.25)
    q3 = df["sn_tpm"].quantile(0.75)
    iqr = q3 - q1
    upper_cutoff = q3 + 1.5 * iqr
    df_filtered = df.loc[df["sn_tpm"] <= upper_cutoff].copy()

    print(f"Removed {len(df) - len(df_filtered):,} outliers")
    print(f"Upper cutoff: {upper_cutoff:.2f} TPM")

    print("[3/5] Computing Pearson correlation...")
    proximity_vals = df_filtered["proximity"]
    tpm_vals = df_filtered["sn_tpm"]
    r_value, p_value = pearsonr(proximity_vals, tpm_vals)
    print(f"Pearson r = {r_value:.4f}, p = {p_value:.3e}")

    print("[4/5] Writing scatter plot...")
    plt.figure(figsize=(7, 5))
    plt.scatter(proximity_vals, tpm_vals, s=12, alpha=0.7)
    plt.xlabel("Network proximity to monogenic PD seeds")
    plt.ylabel("GTEx substantia nigra expression (TPM)")
    plt.title("Proximity vs substantia nigra expression")
    plt.text(
        0.05,
        0.95,
        f"Pearson r = {r_value:.3f}\np-value = {p_value:.2e}",
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.6},
    )
    plt.tight_layout()

    ensure_parent(PROXIMITY_PLOT)
    plt.savefig(PROXIMITY_PLOT, dpi=300)
    print(f"[5/5] Wrote {relpath(PROXIMITY_PLOT)}")


if __name__ == "__main__":
    main()
