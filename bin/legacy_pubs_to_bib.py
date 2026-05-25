#!/usr/bin/env python3
"""Convert legacy publications JSON to BibTeX for al-folio."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBS_JSON = ROOT / "_data" / "legacy-publications.json"
OUT_BIB = ROOT / "_bibliography" / "papers.bib"

SECTION_TYPE = {
    "Dissertations": "phdthesis",
    "Journal Papers": "article",
    "Conference Papers": "inproceedings",
    "Book": "book",
    "Book Chapter": "incollection",
    "Tutorials": "inproceedings",
    "Workshop Presentations": "misc",
    "Conference Presenter": "misc",
    "Technical Industrial Presentations": "misc",
}

ABBR_PATTERNS = [
    (r"\bISSCC\b", "ISSCC"),
    (r"\bJSSC\b", "JSSC"),
    (r"\bTVLSI\b", "TVLSI"),
    (r"\bTCAS\b", "TCAS"),
    (r"\bCICC\b", "CICC"),
    (r"\bISCAS\b", "ISCAS"),
    (r"\bDAC\b", "DAC"),
    (r"\bICCD\b", "ICCD"),
    (r"\bGLSVLSI\b", "GLSVLSI"),
    (r"\bGOMACTech\b", "GOMACTech"),
    (r"\bVLSI\b", "VLSI"),
    (r"\bICCAD\b", "ICCAD"),
    (r"\bDATE\b", "DATE"),
    (r"\bASP-DAC\b", "ASP-DAC"),
    (r"\bS3S\b", "S3S"),
    (r"\bSOCC\b", "SOCC"),
]

SELECTED_YEARS = {2024, 2025}
SELECTED_KEYWORDS = ("career", "obfuscation", "hardware trojan", "3-d", "3d", "ntc")


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "", text.lower())
    return text[:24] or "entry"


def bib_key(entry: dict, used: set[str]) -> str:
    authors = entry.get("authors") or ""
    first_author = authors.split(" and ")[0].split(",")[0].strip()
    first_author = re.sub(r"[^A-Za-z]", "", first_author.split()[-1] if first_author else "anon")
    year = entry.get("year") or "0000"
    title_word = slugify(entry.get("title", "paper"))[:12]
    base = f"{first_author.lower()}{year}{title_word}"
    key = base
    n = 2
    while key in used:
        key = f"{base}{n}"
        n += 1
    used.add(key)
    return key


def escape_bib(value: str) -> str:
    return value.replace("{", "\\{").replace("}", "\\}")


def infer_abbr(venue: str) -> str | None:
    for pattern, abbr in ABBR_PATTERNS:
        if re.search(pattern, venue, re.I):
            return abbr
    return None


def local_pdf_path(pdf_url: str | None, section: str) -> str | None:
    if not pdf_url:
        return None
    filename = pdf_url.rstrip("/").split("/")[-1]
    folder = {
        "Journal Papers": "journals",
        "Conference Papers": "conferences",
        "Dissertations": "dissertations",
        "Tutorials": "tutorials",
        "Book Chapter": "books",
        "Book": "books",
        "Workshop Presentations": "workshops",
        "Conference Presenter": "presentations",
        "Technical Industrial Presentations": "presentations",
    }.get(section, "misc")
    return f"assets/pdf/{folder}/{filename}"


def should_select(entry: dict) -> bool:
    year = entry.get("year") or 0
    title = (entry.get("title") or "").lower()
    if year in SELECTED_YEARS and "savidis" in (entry.get("authors") or "").lower():
        return True
    return any(k in title for k in SELECTED_KEYWORDS) and year >= 2015


def field_line(name: str, value: str | int | None, indent: str = "  ") -> str | None:
    if value is None or value == "":
        return None
    if isinstance(value, int):
        return f'{indent}{name} = {{{value}}},'
    return f'{indent}{name} = {{{escape_bib(str(value))}}},'


def entry_to_bib(entry: dict, key: str) -> str:
    section = entry["section"]
    bib_type = SECTION_TYPE[section]
    lines = [f"@{bib_type}{{{key},"]
    title = entry.get("title") or "Untitled"
    authors = entry.get("authors") or "Savidis, Ioannis"
    venue = entry.get("venue") or ""
    year = entry.get("year")

    for line in [
        field_line("title", title),
        field_line("author", authors),
    ]:
        if line:
            lines.append(line)

    if bib_type == "article":
        journal = venue.split(",")[0] if venue else "Journal"
        lines.append(field_line("journal", journal))
    elif bib_type == "inproceedings":
        booktitle = venue
        lines.append(field_line("booktitle", booktitle))
        if section == "Tutorials":
            lines.append(field_line("note", "Tutorial"))
    elif bib_type == "phdthesis":
        lines.append(field_line("school", "Drexel University"))
        lines.append(field_line("address", "Philadelphia, PA, USA"))
    elif bib_type == "book":
        lines.append(field_line("publisher", "Morgan Kaufmann Publishers"))
    elif bib_type == "incollection":
        lines.append(field_line("booktitle", venue))
    elif bib_type == "misc":
        lines.append(field_line("howpublished", venue))

    if year:
        lines.append(field_line("year", year))

    abbr = infer_abbr(venue)
    if abbr:
        lines.append(field_line("abbr", abbr))

    pdf = local_pdf_path(entry.get("pdf_url"), section)
    if pdf:
        lines.append(field_line("pdf", pdf))

    if should_select(entry):
        lines.append("  selected = {true},")

    if lines[-1].endswith(","):
        lines[-1] = lines[-1][:-1]
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    pubs = json.loads(PUBS_JSON.read_text())
    used: set[str] = set()
    blocks = [
        "---",
        "---",
        "",
        "@string{ieee_jssc = {IEEE Journal of Solid-State Circuits}}",
        "@string{ieee_tvlsi = {IEEE Transactions on Very Large Scale Integration Systems}}",
        "@string{isscc = {IEEE International Solid-State Circuits Conference (ISSCC)}}",
        "@string{cicc = {IEEE Custom Integrated Circuits Conference (CICC)}}",
        "@string{iscas = {IEEE International Symposium on Circuits and Systems (ISCAS)}}",
        "",
    ]

    for entry in pubs:
        key = bib_key(entry, used)
        blocks.append(entry_to_bib(entry, key))
        blocks.append("")

    OUT_BIB.write_text("\n".join(blocks) + "\n")
    print(f"Wrote {len(pubs)} entries to {OUT_BIB}")


if __name__ == "__main__":
    main()
