#!/usr/bin/env python3
"""Create a git branch, commit content changes, and open a PR."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from common import ROOT, blog_url_full
from intake import validate_intake
from pending import plan_is_approved, pr_is_approved, resolve_pending_from_intake, set_status


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, text=True, check=True, **kwargs)


def git(*args: str) -> str:
    return run(["git", *args], capture_output=True).stdout.strip()


def enforce_pr_approval(intake_path: Path, force: bool) -> None:
    if force:
        return
    pending = resolve_pending_from_intake(intake_path)
    if pending is None:
        raise ValueError(
            "Publish requires pending workflow with PR approval, or pass --force (maintainer only)."
        )
    if not plan_is_approved(pending):
        raise ValueError("Plan not approved yet.")
    if not pr_is_approved(pending):
        raise ValueError(
            f"PR not approved for {pending.name}. User must reply APPROVE PR; "
            f"run: python3 bin/content/approve.py pr {pending.name}"
        )


def slugify_title(title: str) -> str:
    import re

    t = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
    return t[:40] or "item"


def main() -> int:
    parser = argparse.ArgumentParser(description="Commit content and open PR")
    parser.add_argument("intake_file", type=Path, help="Intake JSON used for this change")
    parser.add_argument("--branch", help="Branch name (auto-generated if omitted)")
    parser.add_argument("--title", help="PR title")
    parser.add_argument("--draft", action="store_true", default=True, help="Open draft PR (default)")
    parser.add_argument("--no-draft", action="store_false", dest="draft", help="Open ready-for-review PR")
    parser.add_argument("--force", action="store_true", help="Skip PR approval gate (maintainer)")
    args = parser.parse_args()

    try:
        enforce_pr_approval(args.intake_file, args.force)
    except ValueError as exc:
        print(f"Publish blocked: {exc}", file=sys.stderr)
        return 1

    data = validate_intake(json.loads(args.intake_file.read_text()))
    content_type = data["type"]
    pending = resolve_pending_from_intake(args.intake_file)
    plan_summary = ""
    if pending and (pending / "plan.md").is_file():
        plan_summary = (pending / "plan.md").read_text()[:2000]

    if content_type == "news_post":
        slug = data["slug"]
        branch = args.branch or f"content/news-{data['date']}-{slug}"
        pr_title = args.title or f"content: {data['title']}"
        live_url = blog_url_full(data["date"], slug)
    elif content_type == "news_brief":
        branch = args.branch or f"content/brief-{data['date']}-{data['slug']}"
        pr_title = args.title or f"content: news brief {data['date']}"
        live_url = "/icelab-website/news/"
    elif content_type == "publication":
        branch = args.branch or f"content/pub-{data['year']}-{slugify_title(data['title'])}"
        pr_title = args.title or f"content: add publication — {data['title'][:60]}"
        live_url = "https://jiwanizakir.github.io/icelab-website/publications/"
    elif content_type == "team_member":
        branch = args.branch or f"content/team-{data['slug']}"
        pr_title = args.title or f"content: add team member {data['name']}"
        live_url = "https://jiwanizakir.github.io/icelab-website/team/"
    elif content_type == "project":
        branch = args.branch or f"content/project-{data['slug']}"
        pr_title = args.title or f"content: add project {data['title'][:60]}"
        live_url = "https://jiwanizakir.github.io/icelab-website/projects/"
    else:
        print(f"Unsupported type: {content_type}", file=sys.stderr)
        return 1

    status = git("status", "--porcelain")
    if not status:
        print("Nothing to commit. Run generate.py first.", file=sys.stderr)
        return 1

    try:
        git("checkout", "-b", branch)
        git("add", "-A")
        git("commit", "-m", pr_title)
        run(["git", "push", "-u", "origin", branch])

        pending_note = f"`content-intake/pending/{pending.name}/`" if pending else args.intake_file.name
        body = f"""## Summary
Human-in-the-loop content submission via ICE Lab website agent.

- **Type:** `{content_type}`
- **Intake / audit:** {pending_note}

## Plan (approved by submitter)
{plan_summary or '_No plan.md attached._'}

## Expected live URL after merge
{live_url}

## Maintainer checklist
- [ ] CI passes (Build, YAML, BibTeX, Content Validation)
- [ ] Download site-build artifact and spot-check pages
- [ ] Mark PR ready and merge to `main` to deploy

## Rollback
If this merge causes problems after deploy, see [content-snapshots/ROLLBACK.md](content-snapshots/ROLLBACK.md).
Recent snapshot tags: `git tag -l 'site-snapshot/*' | tail -5`

## After merge
```bash
python3 bin/content/verify_live.py --intake {args.intake_file}
```
"""
        pr_cmd = ["gh", "pr", "create", "--title", pr_title, "--body", body]
        if args.draft:
            pr_cmd.append("--draft")
        result = run(pr_cmd, capture_output=True)
        print(result.stdout)
        if pending:
            set_status(pending.name, "done")
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or exc.stdout or str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
