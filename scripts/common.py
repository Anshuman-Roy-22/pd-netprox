"""Shared paths and helpers for the reproducible pd-netprox pipeline."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = ROOT / "figures"
SCRIPTS_DIR = ROOT / "scripts"

STRING_DIR = DATA_DIR / "string"
SEEDS_DIR = DATA_DIR / "seeds"
EXPRESSION_DIR = DATA_DIR / "expression"

STRING_DETAILED_CANDIDATES = [
    STRING_DIR / "9606.protein.links.detailed.v11.0.txt.gz",
    STRING_DIR / "9606.protein.links.detailed.v11.0.txt",
]
STRING_INFO_CANDIDATES = [
    STRING_DIR / "9606.protein.info.v11.0.txt.gz",
    STRING_DIR / "9606.protein.info.v11.0.txt",
]
STRING_ALIASES_CANDIDATES = [
    STRING_DIR / "9606.protein.aliases.v11.0.txt.gz",
    STRING_DIR / "9606.protein.aliases.v11.0.txt",
]
GTEX_GCT_CANDIDATES = [
    EXPRESSION_DIR / "GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct.gz",
    EXPRESSION_DIR / "GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct",
]

PPI_EDGES = STRING_DIR / "ppi_edges.csv"
PPI_GRAPH = STRING_DIR / "ppi_graph.pkl"
SEED_GENES = SEEDS_DIR / "pd_monogenic.txt"
SEED_ENSP = SEEDS_DIR / "pd_monogenic_ensp.txt"
SEED_MAPPING = SEEDS_DIR / "pd_monogenic_seed_mapping.tsv"
GTEX_SN = EXPRESSION_DIR / "gtex_sn_expression.tsv"

RANKED_CANDIDATES = RESULTS_DIR / "ranked_candidates.tsv"
TOP20_CANDIDATES = RESULTS_DIR / "top20_candidates.tsv"
TOP20_GENE_LIST = RESULTS_DIR / "top20_genes_for_enrichment.txt"
PROXIMITY_PLOT = FIGURES_DIR / "proximity_vs_tpm_corr.png"
PPI_SUBGRAPH_PLOT = FIGURES_DIR / "ppi_subgraph_top20.png"

CHECKSUM_FILES = [
    EXPRESSION_DIR / "GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct.gz",
    GTEX_SN,
    SEED_GENES,
    SEED_ENSP,
    SEED_MAPPING,
    STRING_DIR / "9606.protein.aliases.v11.0.txt.gz",
    STRING_DIR / "9606.protein.info.v11.0.txt.gz",
    PPI_EDGES,
    RANKED_CANDIDATES,
    TOP20_CANDIDATES,
    TOP20_GENE_LIST,
    PROXIMITY_PLOT,
    PPI_SUBGRAPH_PLOT,
]

TEXT_CHECKSUM_SUFFIXES = {
    ".cff",
    ".csv",
    ".md",
    ".sha256",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}


def first_existing(candidates: list[Path]) -> Path:
    for candidate in candidates:
        if candidate.exists():
            return candidate
    joined = ", ".join(str(path.relative_to(ROOT)) for path in candidates)
    raise FileNotFoundError(f"None of these files exist: {joined}")


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def read_nonempty_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    if path.suffix.lower() in TEXT_CHECKSUM_SUFFIXES:
        return sha256_text_file(path)

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text_file(path: Path) -> str:
    # Canonicalize line endings so checksum validation is stable on Windows and Linux.
    content = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(content).hexdigest()


def relpath(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")
