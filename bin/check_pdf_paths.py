#!/usr/bin/env python3
"""Verify PDF paths referenced in papers.bib exist on disk."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "_bibliography" / "papers.bib"
PDF_RE = re.compile(r"pdf\s*=\s*\{([^}]+)\}", re.I)


def pdf_disk_path(pdf_file: str) -> Path:
    rel = pdf_file.strip().lstrip("/")
    if rel.startswith("assets/pdf/"):
        return ROOT / rel
    return ROOT / "assets" / "pdf" / rel


def main() -> None:
    if not BIB.is_file():
        print("papers.bib not found", file=sys.stderr)
        sys.exit(1)

    missing: list[str] = []
    checked = 0
    for match in PDF_RE.finditer(BIB.read_text()):
        rel = match.group(1).strip()
        if "://" in rel:
            continue
        checked += 1
        path = pdf_disk_path(rel)
        if not path.is_file():
            missing.append(rel)

    if missing:
        print(f"Missing {len(missing)} PDF(s):", file=sys.stderr)
        for path in missing[:20]:
            print(f"  - {path} (expected at assets/pdf/{path.lstrip('assets/pdf/')})", file=sys.stderr)
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more", file=sys.stderr)
        sys.exit(1)

    print(f"All {checked} referenced PDF path(s) exist under assets/pdf/.")


if __name__ == "__main__":
    main()
