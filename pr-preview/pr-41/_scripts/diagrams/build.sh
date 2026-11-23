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
  # a body may ask to be rendered exactly as its source document renders it
  if grep -q '^%!preamble: verbatim' "$src"; then
    # Computer Modern comes out with wrong advance widths through woff2
    # ("ED A-Learn", "benchmarkcircuits"); ttf renders it correctly and is
    # still smaller than outlining the glyphs.
    pre=verbatim-preamble.tex; fontfmt=ttf
  else
    pre=site-preamble.tex; fontfmt=woff2
  fi
  cat "$pre" "$src" > "$WORK/$name.tex"
  echo '\end{document}' >> "$WORK/$name.tex"
  # latex -> DVI, not pdflatex -> PDF: the DVI route lets dvisvgm emit real
  # <text> elements with a subsetted woff2 font instead of outlining every
  # glyph, which is ~10x smaller and leaves the text selectable. The cost is
  # that the dvips driver has no alpha, so figures must use colour mixes
  # (accent!20) rather than fill opacity.
  latex -interaction=nonstopmode -halt-on-error -output-directory "$WORK" \
        "$WORK/$name.tex" > "$WORK/$name.log" 2>&1 \
    || { echo "LaTeX failed for $name:"; tail -25 "$WORK/$name.log"; exit 1; }
  dvisvgm --exact-bbox --font-format="$fontfmt" --precision=2 \
          -o "$OUT/$name.svg" "$WORK/$name.dvi" > /dev/null 2>&1
  printf '%-28s %6sK  (%s)\n' "$name.svg" \
         "$(( $(stat -c%s "$OUT/$name.svg") / 1024 ))" "${pre%-preamble.tex}"
done
