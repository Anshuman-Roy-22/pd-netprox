"""Verify that the repository contains the required tracked files and valid checksums."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    CHECKSUM_FILES,
    ROOT,
    STRING_DETAILED_CANDIDATES,
    relpath,
    sha256_file,
)

REQUIRED_REPO_FILES = [
    Path(".gitignore"),
    Path(".gitattributes"),
    Path("README.md"),
    Path("PUBLISHING.md"),
    Path("environment.yml"),
    Path("environment.exact.yml"),
    Path("requirements.exact.txt"),
    Path("checksums.sha256"),
    Path("data/README.md"),
    Path("scripts/README.md"),
    Path(".github/workflows/repo-check.yml"),
]


def load_checksum_file(checksum_path: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        digest, rel = line.split("  ", maxsplit=1)
        mapping[rel] = digest
    return mapping


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full-rebuild",
        action="store_true",
        help="Also require the raw STRING detailed network file to be present locally",
    )
    parser.add_argument(
        "--skip-checksums",
        action="store_true",
        help="Skip SHA256 validation of tracked data/results files",
    )
    args = parser.parse_args()

    missing_repo = [path for path in REQUIRED_REPO_FILES if not (ROOT / path).exists()]
    missing_tracked = [path for path in CHECKSUM_FILES if not path.exists()]
    checksum_mismatches: list[str] = []

    if not args.skip_checksums and not missing_tracked:
        checksum_map = load_checksum_file(ROOT / "checksums.sha256")
        for path in CHECKSUM_FILES:
            rel = relpath(path)
            expected = checksum_map.get(rel)
            if expected is None:
                checksum_mismatches.append(f"Missing checksum entry for {rel}")
                continue
            observed = sha256_file(path)
            if observed != expected:
                checksum_mismatches.append(f"Checksum mismatch for {rel}")

    raw_string_present = any(path.exists() for path in STRING_DETAILED_CANDIDATES)

    if missing_repo:
        print("Missing repository files:")
        for path in missing_repo:
            print(f"  - {path.as_posix()}")

    if missing_tracked:
        print("Missing tracked analysis files:")
        for path in missing_tracked:
            print(f"  - {relpath(path)}")

    if checksum_mismatches:
        print("Checksum problems:")
        for item in checksum_mismatches:
            print(f"  - {item}")

    if args.full_rebuild and not raw_string_present:
        joined = ", ".join(path.relative_to(ROOT).as_posix() for path in STRING_DETAILED_CANDIDATES)
        print(f"Missing raw STRING detailed network. Expected one of: {joined}")

    if missing_repo or missing_tracked or checksum_mismatches or (args.full_rebuild and not raw_string_present):
        raise SystemExit(1)

    print("Repository verification passed.")
    if raw_string_present:
        print("Full raw STRING rebuild input is present.")
    else:
        print("Full raw STRING rebuild input is absent; analysis reruns will use tracked ppi_edges.csv.")


if __name__ == "__main__":
    main()
