#!/usr/bin/env python3
"""Generate a human-readable plan for a content submission (no file writes)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from common import ROOT, blog_url_full, pdf_disk_path
from generate import build_bib_entry, generate
from intake import validate_intake
from pending import write_intake, write_plan


def assess_risks(data: dict[str, Any], meta: dict[str, Any]) -> list[str]:
    risks: list[str] = []
    content_type = data["type"]

    if content_type == "news_post":
        out = ROOT / "_posts" / f"{data['date']}-{data['slug']}.md"
        if out.is_file():
            risks.append(f"File already exists: {out.relative_to(ROOT)}")

    if content_type == "publication":
        key, _ = build_bib_entry(data)
        if data.get("pdf_file"):
            pdf_path = pdf_disk_path(data["pdf_file"])
            if not pdf_path.is_file() and not data.get("pdf_source"):
                risks.append(f"PDF not on disk yet: {pdf_path.relative_to(ROOT)}")
            elif pdf_path.is_file() and pdf_path.stat().st_size > 10 * 1024 * 1024:
                risks.append(f"Large PDF (>10MB): {pdf_path.name}")
        meta_key = meta.get("bib_key", key)
        risks.append(f"BibTeX key (proposed): {meta_key}")

    if content_type == "team_member":
        photo = ROOT / data["photo_path"]
        if not photo.is_file() and not data.get("photo_source"):
            risks.append(f"Photo not on disk yet: {data['photo_path']}")

    if data.get("maintainer_override"):
        risks.append("Maintainer override flagged in intake")

    return risks


def render_plan(data: dict[str, Any], meta: dict[str, Any], risks: list[str]) -> str:
    content_type = data["type"]
    lines = [
        f"# PLAN — {content_type}",
        "",
        "## Summary",
    ]

    if content_type == "news_post":
        lines.append(f"- **Title:** {data['title']}")
        lines.append(f"- **Date:** {data['date']}")
        lines.append(f"- **Homepage:** {'yes' if data.get('show_on_homepage') else 'no'}")
    elif content_type == "publication":
        lines.append(f"- **Title:** {data['title']}")
        lines.append(f"- **Year:** {data['year']}")
        lines.append(f"- **Venue:** {data.get('venue', 'n/a')}")
    elif content_type == "team_member":
        lines.append(f"- **Name:** {data['name']}")
        lines.append(f"- **Role:** {data['role']}")
    elif content_type == "project":
        lines.append(f"- **Title:** {data['title']}")
        lines.append(f"- **Category:** {data['category']}")
    else:
        lines.append(f"- **Type:** {content_type}")

    lines.extend(["", "## Files to create or modify"])
    for path in meta.get("files", []):
        lines.append(f"- `{path}`")

    lines.extend(["", "## Expected live URLs after maintainer merge"])
    for url in meta.get("urls", []):
        if url.startswith("/"):
            lines.append(f"- https://jiwanizakir.github.io/icelab-website{url}")
        else:
            lines.append(f"- {url}")

    if content_type == "news_post":
        lines.append(f"- {blog_url_full(data['date'], data['slug'])}")

    if content_type == "publication" and meta.get("bib_key"):
        lines.extend(["", "## BibTeX key (draft)", f"`{meta['bib_key']}`"])

    if risks:
        lines.extend(["", "## Risk flags"])
        for risk in risks:
            lines.append(f"- {risk}")

    lines.extend(
        [
            "",
            "## Next step",
            "The GitHub workflow will open a **draft PR** with these changes.",
            "Edit this issue to regenerate the PR, or ask a maintainer to review and merge.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render content plan for human approval")
    parser.add_argument("intake_file", type=Path, nargs="?", help="Intake JSON path")
    parser.add_argument("--thread", help="Save to content-intake/pending/{thread}/")
    parser.add_argument("--write", action="store_true", help="Write plan.md and update status")
    args = parser.parse_args()

    if args.thread and args.intake_file:
        data = validate_intake(json.loads(args.intake_file.read_text()))
        intake_path = write_intake(args.thread, data)
    elif args.intake_file:
        data = validate_intake(json.loads(args.intake_file.read_text()))
        intake_path = args.intake_file
    elif args.thread:
        intake_path = Path(__file__).resolve().parents[2] / "content-intake" / "pending" / args.thread / "intake.json"
        if not intake_path.is_file():
            print(f"No intake for thread {args.thread}", file=sys.stderr)
            return 1
        data = validate_intake(json.loads(intake_path.read_text()))
    else:
        print("Provide intake_file and/or --thread", file=sys.stderr)
        return 1

    try:
        meta = generate(data, dry_run=True)
        risks = assess_risks(data, meta)
        plan_md = render_plan(data, meta, risks)
    except (ValueError, OSError) as exc:
        print(f"Plan failed: {exc}", file=sys.stderr)
        return 1

    if args.thread and args.write:
        write_plan(args.thread, plan_md)
        print(f"Wrote plan to content-intake/pending/{args.thread}/plan.md")

    print(plan_md)
    print(f"Intake: {intake_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
