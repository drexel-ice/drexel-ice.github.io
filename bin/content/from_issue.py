#!/usr/bin/env python3
"""Extract intake JSON from a GitHub issue body (form fields or JSON block)."""

from __future__ import annotations

import argparse
import json
import re
import sys

from form_to_intake import content_type_from_labels, form_body_to_intake


def extract_json(body: str) -> dict:
    block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", body, re.S)
    if block:
        return json.loads(block.group(1))

    start = body.find("{")
    end = body.rfind("}")
    if start >= 0 and end > start:
        return json.loads(body[start : end + 1])

    raise ValueError("No JSON intake found in issue body (use a ```json code block)")


def parse_issue_body(body: str, content_type: str | None = None, labels: list[str] | None = None) -> dict:
    """Prefer typed issue forms; fall back to raw JSON for advanced submitters."""
    label_type = content_type_from_labels(labels or [])
    if label_type or content_type:
        try:
            return form_body_to_intake(body, content_type=content_type or label_type, labels=labels)
        except ValueError as form_exc:
            if label_type or content_type:
                raise form_exc

    try:
        return extract_json(body)
    except (ValueError, json.JSONDecodeError):
        return form_body_to_intake(body, content_type=content_type, labels=labels)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract intake JSON from issue body")
    parser.add_argument("--body-file", type=argparse.FileType("r"), required=True)
    parser.add_argument("--output", required=True, help="Write intake JSON here")
    parser.add_argument("--content-type", help="Content type when not inferrable from labels")
    parser.add_argument(
        "--labels",
        default="",
        help="Comma-separated issue labels (e.g. content,content:news_post)",
    )
    args = parser.parse_args()

    body = args.body_file.read()
    labels = [label.strip() for label in args.labels.split(",") if label.strip()]
    try:
        data = parse_issue_body(body, content_type=args.content_type, labels=labels)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Failed to extract intake: {exc}", file=sys.stderr)
        return 1

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
    print(f"Wrote intake to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
