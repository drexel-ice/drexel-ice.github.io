#!/usr/bin/env bash
# Render every TikZ figure under tex/ to assets/img/projects/ml-eda/<name>.svg.
#
#   ./build.sh            # all figures
#   ./build.sh ecosystem  # just tex/ecosystem.tex
#
# Requires: pdflatex, dvisvgm (texlive-latex-extra + texlive-font-utils).
set -euo pipefail
cd "$(dirname "$0")"

OUT=../../assets/img/projects/ml-eda
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

for src in tex/${1:-*}.tex; do
  name=$(basename "$src" .tex)
  cat site-preamble.tex "$src" > "$WORK/$name.tex"
  echo '\end{document}' >> "$WORK/$name.tex"
  # latex -> DVI, not pdflatex -> PDF: the DVI route lets dvisvgm emit real
  # <text> elements with a subsetted woff2 font instead of outlining every
  # glyph, which is ~10x smaller and leaves the text selectable. The cost is
  # that the dvips driver has no alpha, so figures must use colour mixes
  # (accent!20) rather than fill opacity.
  latex -interaction=nonstopmode -halt-on-error -output-directory "$WORK" \
        "$WORK/$name.tex" > "$WORK/$name.log" 2>&1 \
    || { echo "LaTeX failed for $name:"; tail -25 "$WORK/$name.log"; exit 1; }
  dvisvgm --exact-bbox --font-format=woff2 --precision=2 \
          -o "$OUT/$name.svg" "$WORK/$name.dvi" > /dev/null 2>&1
  printf '%-28s %6sK\n' "$name.svg" "$(( $(stat -c%s "$OUT/$name.svg") / 1024 ))"
done
