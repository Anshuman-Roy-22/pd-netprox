"""Write SHA256 checksums for the tracked reproducibility-critical files."""

from __future__ import annotations

from pathlib import Path

from common import CHECKSUM_FILES, ROOT, relpath, sha256_file


def main() -> None:
    checksum_path = ROOT / "checksums.sha256"
    lines: list[str] = []

    for path in CHECKSUM_FILES:
        if not path.exists():
            raise FileNotFoundError(f"Cannot write checksums because {relpath(path)} is missing")
        lines.append(f"{sha256_file(path)}  {relpath(path)}")

    checksum_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {checksum_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
