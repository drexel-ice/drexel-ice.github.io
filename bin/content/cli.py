#!/usr/bin/env python3
"""Unified CLI for ICE Lab website content agent (human-in-the-loop)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run_script(name: str, extra: list[str]) -> int:
    script = HERE / name
    result = subprocess.run([sys.executable, str(script), *extra], cwd=HERE)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="ICE Lab website content agent CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_intake = sub.add_parser("intake", help="Validate intake JSON")
    p_intake.add_argument("file", type=Path)

    p_plan = sub.add_parser("plan", help="Render plan for human approval (no writes)")
    p_plan.add_argument("file", type=Path, nargs="?")
    p_plan.add_argument("--thread", help="Pending thread id")
    p_plan.add_argument("--write", action="store_true", help="Save plan.md to pending/")

    p_approve = sub.add_parser("approve", help="Record APPROVE PLAN / APPROVE PR")
    p_approve.add_argument("action", choices=["plan", "pr", "cancel", "status"])
    p_approve.add_argument("thread_id")

    p_preview = sub.add_parser("preview", help="Dry-run generate after plan approval")
    p_preview.add_argument("file", type=Path)

    p_gen = sub.add_parser("generate", help="Generate repo files (requires plan approval)")
    p_gen.add_argument("file", type=Path, nargs="?")
    p_gen.add_argument("--dry-run", action="store_true")
    p_gen.add_argument("--force", action="store_true")

    p_val = sub.add_parser("validate", help="Run preflight checks")
    p_val.add_argument("--skip-build", action="store_true")

    p_pub = sub.add_parser("publish", help="Commit and open draft PR (requires PR approval)")
    p_pub.add_argument("file", type=Path)
    p_pub.add_argument("--no-draft", action="store_true")
    p_pub.add_argument("--force", action="store_true")

    p_verify = sub.add_parser("verify", help="Verify live site")
    p_verify.add_argument("--intake", type=Path, required=True)

    p_all = sub.add_parser("submit", help="Maintainer-only: full pipeline (--force required)")
    p_all.add_argument("file", type=Path)
    p_all.add_argument("--force", action="store_true", required=True)
    p_all.add_argument("--skip-build", action="store_true")
    p_all.add_argument("--no-draft", action="store_true")

    args = parser.parse_args()

    if args.command == "intake":
        return run_script("intake.py", [str(args.file)])
    if args.command == "plan":
        extra = []
        if args.file:
            extra.append(str(args.file))
        if args.thread:
            extra.extend(["--thread", args.thread])
        if args.write:
            extra.append("--write")
        return run_script("plan.py", extra)
    if args.command == "approve":
        return run_script("approve.py", [args.action, args.thread_id])
    if args.command == "preview":
        return run_script("generate.py", [str(args.file), "--dry-run"])
    if args.command == "generate":
        extra = [str(args.file)] if args.file else []
        if args.dry_run:
            extra.append("--dry-run")
        if args.force:
            extra.append("--force")
        return run_script("generate.py", extra)
    if args.command == "validate":
        extra = ["--skip-build"] if args.skip_build else []
        return run_script("validate.py", extra)
    if args.command == "publish":
        extra = [str(args.file)]
        if args.no_draft:
            extra.append("--no-draft")
        if args.force:
            extra.append("--force")
        return run_script("publish.py", extra)
    if args.command == "verify":
        return run_script("verify_live.py", ["--intake", str(args.intake)])
    if args.command == "submit":
        steps = [
            ["intake.py", str(args.file)],
            ["generate.py", str(args.file), "--force"],
        ]
        val = ["validate.py"]
        if args.skip_build:
            val.append("--skip-build")
        steps.append(val)
        pub = ["publish.py", str(args.file), "--force"]
        if args.no_draft:
            pub.append("--no-draft")
        steps.append(pub)
        for step in steps:
            rc = subprocess.run([sys.executable, str(HERE / step[0]), *step[1:]], cwd=HERE).returncode
            if rc != 0:
                return rc
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
