#!/usr/bin/env python3
"""Preflight validation before opening a content PR."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

from common import BLOCKED_PATHS, ROOT, pdf_disk_path

PDF_RE = re.compile(r"pdf\s*=\s*\{([^}]+)\}", re.I)
BIB = ROOT / "_bibliography" / "papers.bib"
MAX_PDF_MB = 10


def check_pdf_paths() -> list[str]:
    issues = []
    warnings = []
    if not BIB.is_file():
        return ["papers.bib not found"]
    for match in PDF_RE.finditer(BIB.read_text()):
        rel = match.group(1).strip()
        if "://" in rel:
            continue
        path = pdf_disk_path(rel)
        if not path.is_file():
            issues.append(f"Missing PDF: assets/pdf/{rel.lstrip('assets/pdf/')}")
        elif path.stat().st_size > MAX_PDF_MB * 1024 * 1024:
            warnings.append(f"Large PDF (>={MAX_PDF_MB}MB): {path.name}")
    for warning in warnings:
        print(f"WARN: {warning}")
    return issues


def check_duplicate_post_slugs() -> list[str]:
    issues = []
    seen: dict[str, str] = {}
    for folder in ("_posts", "_news"):
        for path in (ROOT / folder).glob("*.md"):
            stem = path.stem
            if stem in seen:
                issues.append(f"Duplicate slug stem: {stem} in {folder} and {seen[stem]}")
            seen[stem] = folder
    return issues


def check_referenced_images() -> list[str]:
    issues = []
    for path in list((ROOT / "_team").glob("*.md")) + list((ROOT / "_projects").glob("*.md")):
        text = path.read_text()
        match = re.search(r"^img:\s*(.+)$", text, re.M)
        if match:
            img = match.group(1).strip()
            if not (ROOT / img).is_file():
                issues.append(f"Missing image for {path.name}: {img}")
    return issues


def check_bibtex() -> list[str]:
    try:
        import bibtexparser
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "bibtexparser"], check=True)
        import bibtexparser

    try:
        bib = bibtexparser.load(open(BIB))
    except Exception as exc:
        return [f"BibTeX parse error: {exc}"]
    issues = []
    for entry in bib.entries:
        if "title" not in entry:
            issues.append(f"Entry {entry.get('ID', '?')} missing title")
        if "year" not in entry:
            issues.append(f"Entry {entry.get('ID', '?')} missing year")
    return issues


def check_jekyll_build(skip_build: bool) -> list[str]:
    if skip_build:
        return []
    try:
        subprocess.run(
            ["bundle", "exec", "jekyll", "build"],
            cwd=ROOT,
            env={**os.environ, "JEKYLL_ENV": "production"},
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        return [f"Jekyll build failed:\n{exc.stderr[-2000:]}"]
    except FileNotFoundError:
        return ["bundle not found — skip build locally or run in CI"]
    return []


def check_featured_slider_links() -> list[str]:
    issues = []
    slides_path = ROOT / "_data" / "featured_slides.yml"
    if not slides_path.is_file():
        return issues
    site = ROOT / "_site"
    if not site.is_dir():
        return issues
    for line in slides_path.read_text().splitlines():
        match = re.search(r"link:\s*(/\S+)", line)
        if not match:
            continue
        link = match.group(1).strip("/")
        # /blog/2018/foo/ -> _site/blog/2018/foo/index.html
        parts = link.split("/")
        if parts[0] == "blog" and len(parts) >= 3:
            candidate = site / parts[0] / parts[1] / parts[2] / "index.html"
            if not candidate.is_file():
                issues.append(f"Featured slider dead link (not in _site): /{link}/")
    return issues


def check_blocked_paths() -> list[str]:
    issues = []
    try:
        changed = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.splitlines()
        if not changed:
            changed = subprocess.run(
                ["git", "diff", "--name-only", "--cached"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            ).stdout.splitlines()
    except FileNotFoundError:
        return issues

    for path in changed:
        path = path.strip()
        if not path:
            continue
        for blocked in BLOCKED_PATHS:
            if path == blocked or path.startswith(blocked):
                issues.append(f"Blocked path modified without maintainer review: {path}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight validate content changes")
    parser.add_argument("--skip-build", action="store_true", help="Skip jekyll build")
    args = parser.parse_args()

    checks = [
        ("Blocked paths", check_blocked_paths),
        ("PDF paths", check_pdf_paths),
        ("Duplicate slugs", check_duplicate_post_slugs),
        ("Referenced images", check_referenced_images),
        ("BibTeX", check_bibtex),
        ("Featured slider links", check_featured_slider_links),
    ]
    if not args.skip_build:
        checks.append(("Jekyll build", lambda: check_jekyll_build(False)))

    issues: list[str] = []
    for name, fn in checks:
        result = fn()
        if result:
            issues.extend(f"[{name}] {item}" for item in result)
        else:
            print(f"OK: {name}")

    if issues:
        print(f"\n{len(issues)} issue(s) found:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    print("\nAll preflight checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
