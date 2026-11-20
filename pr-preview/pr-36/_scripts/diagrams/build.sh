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
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory "$WORK" \
           "$WORK/$name.tex" > "$WORK/$name.log" 2>&1 \
    || { echo "LaTeX failed for $name:"; tail -25 "$WORK/$name.log"; exit 1; }
  dvisvgm --pdf --exact-bbox --no-fonts --precision=4 \
          -o "$OUT/$name.svg" "$WORK/$name.pdf" > /dev/null 2>&1
  printf '%-28s %6sK\n' "$name.svg" "$(( $(stat -c%s "$OUT/$name.svg") / 1024 ))"
done
