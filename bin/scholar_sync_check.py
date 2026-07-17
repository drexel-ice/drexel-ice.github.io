#!/usr/bin/env python3
"""Propose publications that exist on Google Scholar but not in papers.bib.

Fetches the lab's Scholar profile listing, then reports articles whose id is
not referenced by any bib entry's google_scholar_id and whose title matches no
bib title. Scholar indexes occasional near-duplicates, so proposals are
human-triaged: add real papers via the Add Publication issue form, and append
the article id of anything bogus to .github/scholar-sync-ignore.txt.

Writes a markdown report to the path given as argv[1] (default
scholar-sync-report.md). Exit codes: 0 nothing new, 3 candidates found,
2 fetch failure (soft-fail in CI).
"""

from __future__ import annotations

import html
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "_bibliography" / "papers.bib"
IGNORE = ROOT / ".github" / "scholar-sync-ignore.txt"
SCHOLAR_USER = "qe9QgMZUjAMC"
PAGE_SIZE = 100
MIN_SANE_ROWS = 100
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

ROW_RE = re.compile(
    r'citation_for_view=' + SCHOLAR_USER + r':([^&"]+)"[^>]*class="gsc_a_at">(.*?)</a>.*?'
    r'class="gsc_a_ac[^"]*"[^>]*>(\d*)<.*?'
    r'class="gsc_a_h[^"]*"[^>]*>(\d*)<',
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


def norm(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (title or "").lower())


def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("scholar-sync-report.md")

    articles: dict[str, dict] = {}
    for start in (0, PAGE_SIZE):
        url = (
            "https://scholar.google.com/citations"
            f"?user={SCHOLAR_USER}&hl=en&pagesize={PAGE_SIZE}&cstart={start}"
        )
        try:
            page = fetch(url)
        except RuntimeError as err:
            print(f"WARN: {err}", file=sys.stderr)
            return 2
        rows = ROW_RE.findall(page)
        print(f"cstart={start}: parsed {len(rows)} articles")
        for article_id, title, cites, year in rows:
            articles[article_id] = {
                "title": html.unescape(re.sub(r"<[^>]+>", "", title)).strip(),
                "cites": int(cites) if cites else 0,
                "year": year or "?",
            }
        if len(rows) < PAGE_SIZE:
            break
        time.sleep(5)

    if len(articles) < MIN_SANE_ROWS:
        print(f"WARN: only parsed {len(articles)} articles; aborting", file=sys.stderr)
        return 2

    bib = BIB.read_text()
    bib_ids = set(re.findall(r"google_scholar_id = \{([^}]+)\}", bib))
    bib_titles = [norm(t) for t in re.findall(r"\n  title\s*=\s*\{(.*?)\},", bib, re.S)]
    ignored = set()
    if IGNORE.exists():
        ignored = {
            line.split("#", 1)[0].strip()
            for line in IGNORE.read_text().splitlines()
            if line.split("#", 1)[0].strip()
        }

    def in_bib(article_id: str, title: str) -> bool:
        if article_id in bib_ids:
            return True
        nt = norm(title)
        return any(
            nt == bt or (len(nt) > 25 and (bt.startswith(nt[:40]) or nt.startswith(bt[:40])))
            for bt in bib_titles
        )

    candidates = [
        (aid, art)
        for aid, art in articles.items()
        if aid not in ignored and not in_bib(aid, art["title"])
    ]
    candidates.sort(key=lambda item: -item[1]["cites"])

    if not candidates:
        print("No new publications found on Scholar.")
        return 0

    lines = [
        f"Found **{len(candidates)}** Google Scholar articles not present in `papers.bib` "
        f"(profile has {len(articles)} articles total).",
        "",
        "For each real publication, add it with the **Add Publication** issue form. "
        "For Scholar duplicates or noise, append the article id to "
        "`.github/scholar-sync-ignore.txt`.",
        "",
        "| Citations | Year | Title | Scholar |",
        "|---:|---|---|---|",
    ]
    for aid, art in candidates:
        link = (
            "https://scholar.google.com/citations?view_op=view_citation&hl=en"
            f"&user={SCHOLAR_USER}&citation_for_view={SCHOLAR_USER}:{aid}"
        )
        title = art["title"].replace("|", "\\|")
        lines.append(f"| {art['cites']} | {art['year']} | {title} | [{aid}]({link}) |")
    report_path.write_text("\n".join(lines) + "\n")
    print(f"{len(candidates)} candidates; report written to {report_path}")
    return 3


if __name__ == "__main__":
    sys.exit(main())
