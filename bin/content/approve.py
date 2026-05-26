#!/usr/bin/env python3
"""Record human approval for HITL content workflow."""

from __future__ import annotations

import argparse
import sys

from pending import approve_plan, approve_pr, cancel, read_status


def main() -> int:
    parser = argparse.ArgumentParser(description="Approve plan or PR stage for pending submission")
    parser.add_argument("action", choices=["plan", "pr", "cancel", "status"])
    parser.add_argument("thread_id", help="Pending thread id (content-intake/pending/{thread_id}/)")
    args = parser.parse_args()

    try:
        if args.action == "plan":
            path = approve_plan(args.thread_id)
            print(f"Plan approved: {path}")
        elif args.action == "pr":
            path = approve_pr(args.thread_id)
            print(f"PR stage approved: {path}")
        elif args.action == "cancel":
            cancel(args.thread_id)
            print(f"Cancelled pending submission: {args.thread_id}")
        elif args.action == "status":
            print(read_status(args.thread_id))
    except ValueError as exc:
        print(f"Approval error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
