# pd-netprox

Protein-network proximity analysis for Parkinson's disease candidate prioritization using STRING and GTEx substantia nigra expression.

## What this repository guarantees

- A canonical, documented pipeline instead of multiple competing script paths.
- Offline seed mapping from local STRING alias files.
- A tracked analysis rerun path that works from the files stored in Git.
- A full rebuild path for the main network preprocessing if you also provide the raw STRING detailed network download locally.
- SHA256 checksums for the tracked reproducibility-critical inputs and outputs.

## Quick start

```powershell
conda env create -f environment.yml
conda activate pd-netprox
python scripts/verify_repository.py
python scripts/run_pipeline.py
```

If you also have the raw STRING detailed network file locally, the pipeline will rebuild `data/string/ppi_edges.csv`. If not, it will reuse the tracked `data/string/ppi_edges.csv`.

To refresh the checksum file after a fresh run:

```powershell
python scripts/run_pipeline.py --update-checksums
```

## Canonical pipeline order

1. `scripts/extract_gtex_sn.py`
2. `scripts/map_seeds_to_ensp.py`
3. `scripts/process_string.py` if the raw STRING detailed network is available
4. `scripts/build_graph.py`
5. `scripts/compute_proximity.py`
6. `scripts/prepare_top20.py`
7. `scripts/scatter_plot.py`
8. `scripts/plot_ppi_subgraph.py`

## Tracked inputs and outputs

Tracked source or reduced-input files:

- `data/expression/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct.gz`
- `data/expression/gtex_sn_expression.tsv`
- `data/seeds/pd_monogenic.txt`
- `data/seeds/pd_monogenic_ensp.txt`
- `data/seeds/pd_monogenic_seed_mapping.tsv`
- `data/string/9606.protein.aliases.v11.0.txt.gz`
- `data/string/9606.protein.info.v11.0.txt.gz`
- `data/string/ppi_edges.csv`

Tracked canonical outputs:

- `results/ranked_candidates.tsv`
- `results/top20_candidates.tsv`
- `results/top20_genes_for_enrichment.txt`
- `figures/proximity_vs_tpm_corr.png`
- `figures/ppi_subgraph_top20.png`

Not tracked in normal Git history:

- The raw STRING detailed interaction file because it exceeds GitHub's normal file-size limits.
- Local-only large or unused files such as uncompressed alias tables, intermediate graph pickles, and archive material in `data/NOT USED/`.

## Environment files

- `environment.yml`: Small runtime environment for the canonical pipeline.
- `environment.exact.yml`: Full export of the Windows conda environment used for this repository snapshot.
- `requirements.exact.txt`: Exact `pip freeze --all` output from the same environment.

## Validation

Repository validation:

```powershell
python scripts/verify_repository.py
```

Require the raw STRING detailed network to be present too:

```powershell
python scripts/verify_repository.py --full-rebuild
```

## Repository layout

- `scripts/`: Canonical pipeline scripts only.
- `scripts/legacy/`: Archived exploratory or superseded scripts kept for provenance.
- `data/`: Tracked inputs, reduced inputs, and documented optional raw inputs.
- `results/`: Canonical tabular outputs tracked in Git.
- `figures/`: Canonical figures tracked in Git.
- `paper/`: Writing and manuscript material.
