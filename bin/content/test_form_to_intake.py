#!/usr/bin/env python3
"""Smoke tests for GitHub Issue Form → intake JSON mapping."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from form_to_intake import build_intake, form_body_to_intake, parse_issue_form_sections
from intake import validate_intake


NEWS_BODY = """
### Date

2026-06-01

### Title

Paper Accepted at ISCAS 2026

### Body

Our paper was accepted.

### Show on homepage

- [x] Show on homepage news table

### Tags (comma-separated)

news, publications
"""

PUBLICATION_BODY = """
### Entry type

inproceedings

### Title

Example Paper

### Authors (one per line)

A. Author
B. Coauthor

### Venue (journal or conference)

IEEE ISCAS

### Year

2026
"""


class FormToIntakeTests(unittest.TestCase):
    def test_parse_sections(self) -> None:
        sections = parse_issue_form_sections(NEWS_BODY)
        self.assertEqual(sections["date"], "2026-06-01")
        self.assertIn("Show on homepage news table", sections["show_on_homepage"])

    def test_news_post_roundtrip(self) -> None:
        data = form_body_to_intake(NEWS_BODY, content_type="news_post")
        normalized = validate_intake(data)
        self.assertEqual(normalized["type"], "news_post")
        self.assertTrue(normalized["show_on_homepage"])
        self.assertEqual(normalized["tags"], ["news", "publications"])

    def test_publication_authors(self) -> None:
        data = form_body_to_intake(PUBLICATION_BODY, content_type="publication")
        normalized = validate_intake(data)
        self.assertEqual(len(normalized["authors"]), 2)
        self.assertEqual(normalized["venue"], "IEEE ISCAS")

    def test_from_issue_json_fallback(self) -> None:
        from from_issue import parse_issue_body

        body = """### ignored\n\n```json\n{\"type\": \"news_brief\", \"date\": \"2099-02-01\", \"body_markdown\": \"Brief note\"}\n```"""
        data = parse_issue_body(body, labels=["content"])
        self.assertEqual(data["type"], "news_brief")


if __name__ == "__main__":
    unittest.main()
