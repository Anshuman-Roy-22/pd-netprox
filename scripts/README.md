# Scripts

## Canonical pipeline

- `run_pipeline.py`: Runs the reproducible pipeline in the documented order.
- `extract_gtex_sn.py`: Reduces the GTEx median TPM matrix to the substantia nigra column.
- `map_seeds_to_ensp.py`: Maps monogenic PD seed genes to STRING ENSP IDs using the local alias table.
- `process_string.py`: Converts the raw STRING detailed network to `data/string/ppi_edges.csv`.
- `build_graph.py`: Builds `data/string/ppi_graph.pkl` from the filtered STRING protein edges.
- `compute_proximity.py`: Computes seed-to-protein network proximity and writes `results/ranked_candidates.tsv`.
- `prepare_top20.py`: Writes the top-20 non-seed candidates and enrichment gene list.
- `scatter_plot.py`: Creates the proximity-versus-expression scatter plot.
- `plot_ppi_subgraph.py`: Draws the seed-plus-top20 subgraph.
- `verify_repository.py`: Checks for required files and validates `checksums.sha256`.
- `update_checksums.py`: Regenerates `checksums.sha256` for the tracked reproducibility-critical files.

## Supplemental scripts

These files have been moved into `scripts/legacy/` because they represent previous exploratory/superseded and auxiliary work that are not part of the canonical reproducible pipeline.

For cleaner presentation purposes.
