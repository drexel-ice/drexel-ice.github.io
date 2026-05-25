#!/usr/bin/env python3
"""Verify PDF paths referenced in papers.bib exist on disk."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "_bibliography" / "papers.bib"
PDF_RE = re.compile(r"pdf\s*=\s*\{([^}]+)\}", re.I)


def main() -> None:
    missing = []
    for match in PDF_RE.finditer(BIB.read_text()):
        rel = match.group(1).strip()
        if not rel.startswith("assets/pdf/"):
            continue
        path = ROOT / rel
        if not path.is_file():
            missing.append(rel)
    if missing:
        print(f"Missing {len(missing)} PDF(s):", file=sys.stderr)
        for path in missing[:20]:
            print(f"  - {path}", file=sys.stderr)
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more", file=sys.stderr)
        sys.exit(1)
    print(f"All {len(list(PDF_RE.finditer(BIB.read_text())))} referenced PDF paths exist.")


if __name__ == "__main__":
    main()
