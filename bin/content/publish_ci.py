#!/usr/bin/env python3
"""Create branch, commit, and open PR for content intake (used by GitHub Actions)."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, text=True, check=True, **kwargs)


def run_optional(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)


def slugify(text: str, max_len: int = 40) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", str(text).lower()).strip("-")
    return text[:max_len] or "item"


def remote_branch_exists(branch: str) -> bool:
    result = run_optional(["git", "ls-remote", "--heads", "origin", branch])
    return bool(result.stdout.strip())


def existing_pr_url(branch: str) -> str | None:
    result = run_optional(["gh", "pr", "list", "--head", branch, "--json", "url", "--limit", "1"])
    if result.returncode != 0 or not result.stdout.strip():
        return None
    try:
        rows = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    return rows[0]["url"] if rows else None


def checkout_branch(branch: str) -> None:
    run(["git", "checkout", "-B", branch])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", type=Path, required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--draft", action="store_true", default=True, help="Open draft PR (default)")
    parser.add_argument("--no-draft", action="store_false", dest="draft")
    parser.add_argument("--force-push", action="store_true", help="Force-push when updating an existing branch")
    args = parser.parse_args()

    data = json.loads(args.intake.read_text())
    content_type = data["type"]

    run(["git", "config", "user.name", "github-actions[bot]"])
    run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"])
    run(["git", "fetch", "origin", "main"])
    checkout_branch(args.branch)

    run(["git", "add", "-A"])
    status = run(["git", "status", "--porcelain"], capture_output=True).stdout.strip()
    if not status:
        print("Nothing to commit.", file=sys.stderr)
        pr_url = existing_pr_url(args.branch)
        if pr_url:
            print(pr_url)
            if os.environ.get("GITHUB_ENV"):
                with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as handle:
                    handle.write(f"PR_URL={pr_url}\n")
            return 0
        return 1

    run(["git", "commit", "-m", args.title])
    push_cmd = ["git", "push", "-u", "origin", args.branch]
    if args.force_push or remote_branch_exists(args.branch):
        push_cmd.insert(2, "--force-with-lease")
    run(push_cmd)

    body = f"""## Summary
Automated content submission via GitHub intake workflow.

- **Type:** `{content_type}`
- **Intake:** `{args.intake.as_posix()}`

## Maintainer checklist
- [ ] CI passes (Build, YAML, BibTeX, content-validation)
- [ ] Content reads correctly in the PR diff
- [ ] Mark ready and merge to `main` to deploy

## After merge
Run live verification:

```bash
python3 bin/content/verify_live.py --intake {args.intake.as_posix()}
```
"""
    pr_url = existing_pr_url(args.branch)
    if pr_url:
        print(f"Updated branch; existing PR: {pr_url}")
    else:
        pr_cmd = ["gh", "pr", "create", "--title", args.title, "--body", body, "--base", "main", "--head", args.branch]
        if args.draft:
            pr_cmd.append("--draft")
        result = run(pr_cmd, capture_output=True)
        pr_url = result.stdout.strip()
        print(pr_url)

    if os.environ.get("GITHUB_ENV") and pr_url:
        with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as handle:
            handle.write(f"PR_URL={pr_url}\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or exc.stdout or str(exc), file=sys.stderr)
        sys.exit(1)
