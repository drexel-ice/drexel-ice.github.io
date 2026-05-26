#!/usr/bin/env python3
"""Map GitHub Issue Form bodies to content intake JSON."""

from __future__ import annotations

import re
from typing import Any

from common import slugify

CONTENT_LABEL_PREFIX = "content:"


def parse_issue_form_sections(body: str) -> dict[str, str]:
    """Parse GitHub Issue Form markdown (### Label sections) into a dict."""
    sections: dict[str, str] = {}
    if not body.strip():
        return sections

    chunks = re.split(r"\n### ", body)
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        if chunk.startswith("### "):
            chunk = chunk[4:]
        if "\n" not in chunk:
            continue
        label, _, value = chunk.partition("\n")
        label = label.strip().rstrip("#").strip()
        sections[normalize_label(label)] = value.strip()
    return sections


def normalize_label(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def content_type_from_labels(labels: list[str]) -> str | None:
    for label in labels:
        if label.startswith(CONTENT_LABEL_PREFIX):
            return label.split(":", 1)[1]
    return None


def parse_bool(value: str, default: bool = False) -> bool:
    text = value.strip().lower()
    if not text:
        return default
    if "[x]" in text or text in {"yes", "true", "1", "on"}:
        return True
    if "[ ]" in text or text in {"no", "false", "0", "off"}:
        return False
    return default


def parse_list(value: str) -> list[str]:
    items: list[str] = []
    for line in value.replace(",", "\n").splitlines():
        line = line.strip().lstrip("-").strip()
        if line.startswith("[") and "]" in line:
            line = line.split("]", 1)[1].strip()
        if line:
            items.append(line)
    return items


def parse_int(value: str, default: int = 0) -> int:
    text = value.strip()
    if not text:
        return default
    match = re.search(r"-?\d+", text)
    return int(match.group()) if match else default


def field(sections: dict[str, str], *keys: str, default: str = "") -> str:
    for key in keys:
        if key in sections and sections[key].strip():
            return sections[key].strip()
    return default


def build_intake(content_type: str, sections: dict[str, str]) -> dict[str, Any]:
    if content_type == "news_post":
        title = field(sections, "title")
        return {
            "type": "news_post",
            "date": field(sections, "date"),
            "title": title,
            "slug": field(sections, "slug_optional", "slug") or slugify(title),
            "body_markdown": field(sections, "body", "announcement_body"),
            "description": field(sections, "short_description_optional", "description"),
            "show_on_homepage": parse_bool(field(sections, "show_on_homepage"), default=True),
            "tags": parse_list(field(sections, "tags_comma_separated", "tags")) or ["news"],
        }

    if content_type == "news_brief":
        body = field(sections, "body", "brief_text")
        return {
            "type": "news_brief",
            "date": field(sections, "date"),
            "body_markdown": body,
            "slug": field(sections, "slug_optional", "slug") or slugify(body[:60]),
        }

    if content_type == "publication":
        return {
            "type": "publication",
            "entry_type": field(sections, "entry_type", "bibtex_entry_type"),
            "title": field(sections, "title"),
            "authors": parse_list(field(sections, "authors_one_per_line", "authors")),
            "venue": field(sections, "venue_journal_or_conference", "venue"),
            "year": parse_int(field(sections, "year")),
            "abbr": field(sections, "abbreviation_optional", "abbr"),
            "pdf_file": field(sections, "pdf_path_relative_to_assets_pdf", "pdf_file"),
            "selected": parse_bool(field(sections, "feature_on_homepage", "selected")),
        }

    if content_type == "team_member":
        name = field(sections, "full_name", "name")
        slug = field(sections, "slug_optional", "slug") or slugify(name)
        return {
            "type": "team_member",
            "slug": slug,
            "name": name,
            "role": field(sections, "role_title", "role"),
            "email": field(sections, "email"),
            "category": field(sections, "category"),
            "bio_markdown": field(sections, "bio", "bio_markdown"),
            "photo_path": field(sections, "photo_path_in_repo", "photo_path")
            or f"assets/img/team/{slug}.jpg",
            "importance": parse_int(field(sections, "display_order_importance", "importance"), 5),
        }

    if content_type == "project":
        title = field(sections, "title")
        slug = field(sections, "slug_optional", "slug") or slugify(title)
        return {
            "type": "project",
            "slug": slug,
            "title": title,
            "description": field(sections, "short_description", "description"),
            "body_markdown": field(sections, "full_description", "body"),
            "category": field(sections, "category"),
            "importance": parse_int(field(sections, "display_order_importance", "importance"), 5),
            "image": field(sections, "image_path_optional", "image"),
        }

    raise ValueError(f"Unsupported content type: {content_type}")


def form_body_to_intake(body: str, content_type: str | None = None, labels: list[str] | None = None) -> dict[str, Any]:
    resolved_type = content_type or content_type_from_labels(labels or [])
    if not resolved_type:
        raise ValueError(
            "Could not determine content type. Use a typed issue template "
            "(labels content:news_post, etc.) or paste intake JSON."
        )
    sections = parse_issue_form_sections(body)
    if not sections:
        raise ValueError("No issue form fields found in body.")
    return build_intake(resolved_type, sections)
