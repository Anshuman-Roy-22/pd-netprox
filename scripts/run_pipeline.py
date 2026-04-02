"""Run the canonical pd-netprox pipeline from tracked inputs or full raw inputs."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from common import (
    GTEX_GCT_CANDIDATES,
    PPI_EDGES,
    SCRIPTS_DIR,
    STRING_ALIASES_CANDIDATES,
    STRING_DETAILED_CANDIDATES,
    STRING_INFO_CANDIDATES,
    first_existing,
)


def run_step(python_exe: str, script_name: str) -> None:
    script_path = SCRIPTS_DIR / script_name
    print(f"\n==> Running {script_name}")
    subprocess.run([python_exe, str(script_path)], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python interpreter to use for the pipeline commands",
    )
    parser.add_argument(
        "--update-checksums",
        action="store_true",
        help="Refresh checksums.sha256 after a successful run",
    )
    args = parser.parse_args()

    first_existing(GTEX_GCT_CANDIDATES)
    first_existing(STRING_ALIASES_CANDIDATES)
    first_existing(STRING_INFO_CANDIDATES)

    run_step(args.python, "extract_gtex_sn.py")
    run_step(args.python, "map_seeds_to_ensp.py")

    try:
        first_existing(STRING_DETAILED_CANDIDATES)
    except FileNotFoundError:
        if not PPI_EDGES.exists():
            raise RuntimeError(
                "The raw STRING detailed network is missing and "
                "data/string/ppi_edges.csv is not available."
            ) from None
        print("\n==> Skipping process_string.py because the raw STRING detailed network is absent")
        print("    Reusing tracked data/string/ppi_edges.csv")
    else:
        run_step(args.python, "process_string.py")

    run_step(args.python, "build_graph.py")
    run_step(args.python, "compute_proximity.py")
    run_step(args.python, "prepare_top20.py")
    run_step(args.python, "scatter_plot.py")
    run_step(args.python, "plot_ppi_subgraph.py")

    if args.update_checksums:
        run_step(args.python, "update_checksums.py")


if __name__ == "__main__":
    main()
