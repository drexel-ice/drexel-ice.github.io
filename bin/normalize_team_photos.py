#!/usr/bin/env python3
"""Normalize team headshots to square JPEGs for consistent card cropping."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEAM_DIR = ROOT / "assets" / "img" / "team"
ORIGINALS_DIR = TEAM_DIR / "_originals"
SIZE = 800
QUALITY = 88

# Per-image tuning when automatic gravity is not ideal.
OVERRIDES: dict[str, dict[str, str | float]] = {
    # Selfie with phone at bottom — drop lower portion before squaring.
    "ashish-sharma.jpeg": {"gravity": "north", "height_ratio": 0.82},
    # Head sits high in frame.
    "kyle-juretus.jpeg": {"gravity": "north"},
    "pratik-shrestha.png": {"gravity": "north"},
    "saran-phatharodom.jpeg": {"gravity": "north"},
    "nnaemeka-achebe.jpeg": {"gravity": "north"},
    "amit-varde.png": {"gravity": "north"},
}


def run_magick(args: list[str]) -> None:
    subprocess.run(["magick", *args], check=True)


def dimensions(path: Path) -> tuple[int, int]:
    out = subprocess.check_output(
        ["magick", "identify", "-format", "%w %h", str(path)],
        text=True,
    ).strip()
    w, h = out.split()
    return int(w), int(h)


def gravity_for(path: Path) -> str:
    override = OVERRIDES.get(path.name, {})
    if "gravity" in override:
        return str(override["gravity"])
    w, h = dimensions(path)
    if abs(w - h) <= max(w, h) * 0.08:
        return "center"
    return "north" if h > w else "center"


def output_path(path: Path) -> Path:
    return path.with_suffix(".jpeg")


def normalize(path: Path) -> Path:
    if path.name.startswith("_") or path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        return path

    dest = output_path(path)
    override = OVERRIDES.get(path.name, {})
    gravity = gravity_for(path)
    tmp = TEAM_DIR / f".{path.stem}.work.jpeg"

    steps: list[str] = [str(path), "-auto-orient"]
    if "height_ratio" in override:
        w, h = dimensions(path)
        crop_h = max(1, int(h * float(override["height_ratio"])))
        steps += ["-gravity", "North", "-crop", f"{w}x{crop_h}+0+0", "+repage"]

    steps += [
        "-resize",
        f"{SIZE}x{SIZE}^",
        "-gravity",
        gravity.capitalize(),
        "-extent",
        f"{SIZE}x{SIZE}",
        "-strip",
        "-quality",
        str(QUALITY),
        str(tmp),
    ]
    run_magick(steps)
    tmp.replace(dest)

    if dest != path and path.exists():
        path.unlink()

    return dest


def main() -> int:
    if not TEAM_DIR.is_dir():
        print(f"Missing team image directory: {TEAM_DIR}", file=sys.stderr)
        return 1

    ORIGINALS_DIR.mkdir(exist_ok=True)
    updated: list[str] = []

    for path in sorted(TEAM_DIR.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        if path.parent.name == "_originals":
            continue

        backup = ORIGINALS_DIR / path.name
        if not backup.exists():
            backup.write_bytes(path.read_bytes())

        dest = normalize(path)
        updated.append(dest.name)
        print(f"  {dest.name} ({SIZE}x{SIZE})")

    print(f"Normalized {len(updated)} team photo(s). Originals kept in {ORIGINALS_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
