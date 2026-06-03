"""Shared utilities for ICE Lab website content tooling."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_DIR = ROOT / "content-schemas"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
INTAKE_DIR = ROOT / "content-intake"
PENDING_DIR = INTAKE_DIR / "pending"

BLOCKED_PATHS = (
    "_config.yml",
    "_pages/about.md",
    ".github/workflows/",
)

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def slugify(text: str, max_len: int = 80) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text[:max_len] or "item"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def load_schema(content_type: str) -> dict[str, Any]:
    path = SCHEMAS_DIR / f"{content_type}.json"
    if not path.is_file():
        raise ValueError(f"Unknown content type: {content_type}")
    return load_json(path)


def render_template(template_name: str, **kwargs: Any) -> str:
    template = (TEMPLATES_DIR / template_name).read_text()
    for key, value in kwargs.items():
        placeholder = "{{ " + key + " }}"
        template = template.replace(placeholder, str(value if value is not None else ""))
    return template


def blog_url(date: str, slug: str) -> str:
    year = date[:4]
    return f"/blog/{year}/{slug}/"


def blog_url_full(date: str, slug: str, baseurl: str = "") -> str:
    return f"{baseurl.rstrip('/')}{blog_url(date, slug)}"


def pdf_disk_path(pdf_file: str) -> Path:
    rel = pdf_file.strip().lstrip("/")
    if rel.startswith("assets/pdf/"):
        return ROOT / rel
    return ROOT / "assets" / "pdf" / rel


def normalize_pdf_bib_path(pdf_file: str) -> str:
    rel = pdf_file.strip().lstrip("/")
    if rel.startswith("assets/pdf/"):
        rel = rel[len("assets/pdf/") :]
    return rel


def existing_bib_keys() -> set[str]:
    bib = (ROOT / "_bibliography" / "papers.bib").read_text()
    return set(re.findall(r"@\w+\{([^,\s]+),", bib))


def make_bib_key(authors: list[str], year: int, title: str) -> str:
    first = authors[0] if authors else "anon"
    last = re.sub(r"[^A-Za-z]", "", first.split()[-1] if first else "anon").lower()
    word = slugify(title).replace("-", "")[:12]
    base = f"{last}{year}{word}"
    used = existing_bib_keys()
    key = base
    n = 2
    while key in used:
        key = f"{base}{n}"
        n += 1
    return key
