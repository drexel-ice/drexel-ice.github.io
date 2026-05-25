#!/usr/bin/env python3
"""Mirror legacy publication PDFs referenced in papers.bib."""

from __future__ import annotations

import re
import subprocess
import sys
import urllib.error
import urllib.request
import ssl
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "_bibliography" / "papers.bib"
PUBS_JSON = ROOT / "_data" / "legacy-publications.json"

PDF_FIELD_RE = re.compile(r"pdf\s*=\s*\{([^}]+)\}", re.I)
URL_RE = re.compile(r"https?://[^\s\"']+\.pdf", re.I)


def pdf_urls_from_json() -> dict[str, str]:
    import json

    mapping: dict[str, str] = {}
    for entry in json.loads(PUBS_JSON.read_text()):
        url = entry.get("pdf_url")
        if not url:
            continue
        filename = url.rstrip("/").split("/")[-1]
        mapping[filename] = url
    return mapping


def local_paths_from_bib() -> list[Path]:
    text = BIB.read_text()
    paths = []
    for match in PDF_FIELD_RE.finditer(text):
        rel = match.group(1).strip()
        if rel.startswith("assets/pdf/"):
            paths.append(ROOT / rel)
    return paths


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return True
    result = subprocess.run(
        ["curl", "-fsSL", "-o", str(dest), url],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return True
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "icelab-migration/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
            dest.write_bytes(resp.read())
        return True
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"FAIL {url}: {exc}", file=sys.stderr)
        return False


def main() -> None:
    url_map = pdf_urls_from_json()
    local_paths = local_paths_from_bib()
    ok = 0
    fail = 0
    for path in local_paths:
        filename = path.name
        url = url_map.get(filename)
        if not url:
            print(f"SKIP no source URL for {path.relative_to(ROOT)}")
            fail += 1
            continue
        if download(url, path):
            ok += 1
            print(f"OK   {path.relative_to(ROOT)}")
        else:
            fail += 1
    print(f"\nDone: {ok} downloaded/existing, {fail} failed/skipped")
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
