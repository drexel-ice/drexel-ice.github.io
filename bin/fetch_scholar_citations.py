#!/usr/bin/env python3
"""Refresh _data/citations.yml from the Google Scholar profile.

Fetches the profile's article listing (two pages of 100), parses each row's
citation_for_view article id and cited-by count, and rewrites
_data/citations.yml keyed as "<scholar_userid>:<article_id>" - the format
_layouts/bib.liquid reads for the per-publication citation badges.

Scholar throttles datacenter IPs aggressively, so fetches retry with backoff
and the file is only rewritten when parsing looks sane (a partial or blocked
response must never wipe existing data). Exit codes: 0 written/unchanged,
2 fetch or sanity failure (callers may treat as a soft failure).
"""

from __future__ import annotations

import re
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITATIONS = ROOT / "_data" / "citations.yml"
SCHOLAR_USER = "qe9QgMZUjAMC"
PAGE_SIZE = 100
MIN_SANE_ROWS = 100  # profile has ~179 articles; refuse to write fewer
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

ROW_RE = re.compile(
    r'citation_for_view=' + SCHOLAR_USER + r':([^&"]+)"[^>]*class="gsc_a_at".*?'
    r'class="gsc_a_ac[^"]*"[^>]*>(\d*)<',
    re.S,
)


def fetch(url: str, attempts: int = 4) -> str:
    last_err: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as err:  # noqa: BLE001 - retry any transport failure
            last_err = err
            time.sleep(10 * attempt)
    raise RuntimeError(f"failed to fetch {url}: {last_err}")


def parse_rows(html: str) -> dict[str, int]:
    rows: dict[str, int] = {}
    for article_id, cites in ROW_RE.findall(html):
        rows[article_id] = int(cites) if cites else 0
    return rows


def main() -> int:
    rows: dict[str, int] = {}
    for start in (0, PAGE_SIZE):
        url = (
            "https://scholar.google.com/citations"
            f"?user={SCHOLAR_USER}&hl=en&pagesize={PAGE_SIZE}&cstart={start}"
        )
        try:
            html = fetch(url)
        except RuntimeError as err:
            print(f"WARN: {err}", file=sys.stderr)
            return 2
        page_rows = parse_rows(html)
        print(f"cstart={start}: parsed {len(page_rows)} articles")
        rows.update(page_rows)
        if len(page_rows) < PAGE_SIZE:
            break
        time.sleep(5)

    if len(rows) < MIN_SANE_ROWS:
        print(
            f"WARN: only parsed {len(rows)} articles (< {MIN_SANE_ROWS}); "
            "refusing to rewrite citations.yml",
            file=sys.stderr,
        )
        return 2

    lines = ["metadata:", f"  last_updated: '{date.today().isoformat()}'", "papers:"]
    for article_id in sorted(rows):
        lines.append(f"  {SCHOLAR_USER}:{article_id}:")
        lines.append(f"    citations: {rows[article_id]}")
    CITATIONS.write_text("\n".join(lines) + "\n")
    print(f"citations.yml written: {len(rows)} papers, {sum(rows.values())} total citations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
