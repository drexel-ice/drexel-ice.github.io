#!/usr/bin/env python3
"""Verify live site after deploy using intake metadata."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from common import blog_url_full
from intake import validate_intake

BASE = "https://drexel-ice.github.io"


def fetch(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "ice-content-agent/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify content on live site")
    parser.add_argument("--intake", type=Path, required=True, help="Intake JSON")
    parser.add_argument("--base", default=BASE, help="Live site base URL")
    args = parser.parse_args()

    data = validate_intake(json.loads(args.intake.read_text()))
    base = args.base.rstrip("/")
    issues: list[str] = []

    if data["type"] == "news_post":
        url = base + blog_url_full(data["date"], data["slug"], baseurl="")
        code, body = fetch(url)
        if code != 200:
            issues.append(f"Blog post returned {code}: {url}")
        elif data["title"] not in body:
            issues.append(f"Title not found on page: {data['title']}")
        if data.get("show_on_homepage"):
            home_code, home = fetch(base + "/")
            if data["title"] not in home and data["title"][:30] not in home:
                issues.append("Title not on homepage (inline post)")

    elif data["type"] == "news_brief":
        code, body = fetch(base + "/news/")
        if code != 200:
            issues.append(f"News page returned {code}")
        elif data["body_markdown"][:40].replace("*", "") not in body.replace("*", ""):
            issues.append("Brief content not found on /news/")

    elif data["type"] == "publication":
        code, body = fetch(base + "/publications/")
        if code != 200:
            issues.append(f"Publications page returned {code}")
        elif data["title"] not in body:
            issues.append(f"Publication title not on /publications/: {data['title']}")
        if data.get("pdf_file"):
            pdf_url = base + "/assets/pdf/" + data["pdf_file"].lstrip("/").replace("assets/pdf/", "")
            pdf_code, _ = fetch(pdf_url)
            if pdf_code != 200:
                issues.append(f"PDF returned {pdf_code}: {pdf_url}")
        if re.search(r"\b2077\b", body):
            issues.append("Bad year 2077 found on publications page")

    elif data["type"] == "team_member":
        code, body = fetch(base + "/team/")
        if code != 200:
            issues.append(f"Team page returned {code}")
        elif data["name"] not in body:
            issues.append(f"Team member not on /team/: {data['name']}")

    elif data["type"] == "project":
        code, body = fetch(base + "/projects/")
        if code != 200:
            issues.append(f"Projects page returned {code}")
        elif data["title"] not in body:
            issues.append(f"Project not on /projects/: {data['title']}")

    if issues:
        print(f"Verification failed ({len(issues)} issue(s)):", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    print("Live site verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
