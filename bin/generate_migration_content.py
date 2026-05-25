#!/usr/bin/env python3
"""Generate team, project, news markdown from legacy JSON."""

from __future__ import annotations

import json
import re
import subprocess
import textwrap
import urllib.request
import ssl
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "_data" / "legacy-site-migration.json"
NEWS = ROOT / "_data" / "legacy-news.json"

PROJECTS = [
    ("tsv-modeling", "TSV Modeling and Characterization", "completed", 10),
    ("3d-synchronization", "Synchronization in 3-D Integrated Circuits", "completed", 9),
    ("3d-cts", "Clock Tree Synthesis (CTS) for 3-D Integrated Circuits", "active", 8),
    ("3d-power-delivery", "3-D Integrated Circuit Power Delivery", "completed", 7),
    ("ocvr-clustering", "On-Chip Power Delivery with Run-Time Voltage Regulator Clustering", "active", 6),
    ("optical-interconnect", "3-D Integrated Free-Space Optical Interconnect for Multi-Core Systems", "completed", 5),
    ("thermal-modeling", "Thermal Modeling and Mitigation", "completed", 4),
    ("hardware-trojan-detection", "Run-time Detection and Countermeasures", "active", 3),
    ("design-for-trust", "Attack Prevention Through Design for Trust Algorithms and Methodologies", "active", 2),
    ("ntc-cml", "Power Reduction using NTC with CML", "active", 1),
]

TEAM_CATEGORIES = {
    "ioannis-savidis": ("faculty", 1),
    "pratik-shrestha": ("phd", 1),
    "jeff-wu": ("phd", 2),
    "ziyi-chen": ("phd", 3),
    "saran-phatharodom": ("phd", 4),
    "alec-aversa": ("phd", 5),
    "ashish-sharma": ("phd", 6),
    "nnaemeka-achebe": ("phd", 7),
    "amit-varde": ("phd", 8),
    "vaibhav-venugopal-rao": ("alumni", 1),
    "divya-pathak": ("alumni", 2),
    "kyle-juretus": ("alumni", 3),
    "shazzad-hossain": ("alumni", 4),
}


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return
    result = subprocess.run(
        ["curl", "-fsSL", "-o", str(dest), url],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={"User-Agent": "icelab-migration/1.0"})
        with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
            dest.write_bytes(resp.read())


def ext_from_url(url: str) -> str:
    name = url.rstrip("/").split("/")[-1]
    if "." in name:
        return name.rsplit(".", 1)[-1].lower()
    return "jpg"


def yaml_quote(text: str) -> str:
    if not text:
        return '""'
    if any(c in text for c in ':"\'\n'):
        escaped = text.replace('"', '\\"')
        return f'"{escaped}"'
    return text


def write_team(members: list[dict]) -> None:
    for member in members:
        slug = member["slug"]
        category, importance = TEAM_CATEGORIES[slug]
        ext = ext_from_url(member["image_url"])
        img_rel = f"assets/img/team/{slug}.{ext}"
        download(member["image_url"], ROOT / img_rel)

        role = member.get("role") or "Researcher"
        email = member.get("email")
        description = role
        if email:
            description += f" | {email}"

        bio = member.get("bio") or f"{member['name']} is a member of the ICE Lab at Drexel University."
        bio = bio.replace("\n\n", "\n\n")

        redirect = "redirect: https://ece.drexel.edu/savidis/\n"

        front = f"""---
layout: page
title: {yaml_quote(member['name'])}
description: {yaml_quote(description)}
img: {img_rel}
importance: {importance}
category: {category}
{redirect}---

{bio}
"""
        (ROOT / "_team" / f"{slug}.md").write_text(front)


def project_description(title: str, sub_projects: list[dict]) -> str:
    for sp in sub_projects:
        if sp["title"] == title or title.startswith(sp["title"][:20]):
            return sp["description"]
    return ""


def write_projects(sub_projects: list[dict]) -> None:
    title_map = {sp["title"]: sp for sp in sub_projects}
    alt_titles = {
        "On-Chip Power Delivery with Run-Time Voltage Regulator Clustering": "On-Chip Power Delivery with Run-Time Voltage Regulator Clustering for 3-D and 2-D ICs",
    }
    for slug, title, status, importance in PROJECTS:
        lookup = alt_titles.get(title, title)
        sp = title_map.get(lookup) or title_map.get(title)
        desc = sp["description"] if sp else title
        category = "active" if status == "active" else "completed"
        front = f"""---
layout: page
title: {yaml_quote(title)}
description: {yaml_quote(desc[:200] + ('...' if len(desc) > 200 else ''))}
importance: {importance}
category: {category}
---

{desc}
"""
        (ROOT / "_projects" / f"{slug}.md").write_text(front)


def clean_news_body(body: str) -> str:
    body = re.sub(r"\s+", " ", body).strip()
    return body


def slug_from_title(title: str, date: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]
    return base or date


def write_news(posts: list[dict]) -> None:
    posts_dir = ROOT / "_posts"
    posts_dir.mkdir(exist_ok=True)
    for post in posts:
        date = post["date"][:10]
        slug = post.get("slug") or slug_from_title(post["title"], date)
        if slug in {"1706-2", "second-image", "title"}:
            slug = slug_from_title(post["title"], date)
        filename = f"{date}-{slug}.md"
        body = clean_news_body(post["body"])
        content = f"""---
layout: post
title: {yaml_quote(post['title'])}
date: {date}
description: {yaml_quote(body[:160])}
tags: news
---

{body}
"""
        (posts_dir / filename).write_text(content)

    highlights = posts[:5]
    news_dir = ROOT / "_news"
    for post in highlights:
        date = post["date"][:10]
        slug = slug_from_title(post["title"], date)
        filename = f"{date}-{slug}.md"
        body = clean_news_body(post["body"])
        content = f"""---
layout: post
date: {date}
inline: true
related_posts: false
---

{body}
"""
        (news_dir / filename).write_text(content)


def download_images(data: dict) -> None:
    images = data["images"]
    download(images["logo"], ROOT / "assets/img/icelab_logo.png")
    for area, url in images["research_figures"].items():
        ext = ext_from_url(url)
        download(url, ROOT / f"assets/img/research/{area}.{ext}")


def main() -> None:
    data = json.loads(MIGRATION.read_text())
    news = json.loads(NEWS.read_text())
    news.sort(key=lambda p: p["date"], reverse=True)

    download_images(data)
    write_team(data["team_members"])
    write_projects(data["sub_projects"])
    write_news(news)
    print("Generated team, projects, news, and downloaded images.")


if __name__ == "__main__":
    main()
