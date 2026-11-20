# EDA-Learn diagrams

Figures for the EDA-Learn pages. Two toolchains, because the sources differ.

## 1. Rendered from LaTeX — `tex/`

Figures that also exist in the proposal or a paper are rendered from **the same TikZ
source**, so the document and the website can never drift apart. The body files under
`tex/` are kept verbatim; `site-preamble.tex` supplies everything that makes them look
like the website.

```bash
./build.sh                      # all figures
./build.sh eda-learn-ecosystem  # just one
```

Needs `pdflatex` and `dvisvgm` (`texlive-latex-extra`, `texlive-font-utils`). Output goes
to `assets/img/projects/ml-eda/<name>.svg`.

| Body | Figure | Used on |
| --- | --- | --- |
| `tex/eda-learn-ecosystem.tex` | `eda-learn-ecosystem.svg` | `/projects/eda-learn/` (hero) |

**Adding one:** drop the `\begin{tikzpicture}...\end{tikzpicture}` into `tex/<name>.tex`
and run `./build.sh <name>`. Do not put `\documentclass`, `\usepackage`, colour
definitions or font commands in the body — they belong in the preamble, and leaving them
out is what keeps the file a straight copy of the document's own source.

### How the restyling works

`site-preamble.tex` redefines the base colours so the proposal's existing `blue!7`,
`green!7`, `orange!8` and `purple!7` fills land on the site palette, and sets the ambient
colour to Drexel navy — which TikZ also uses as the default stroke colour. So no `fill=`
or `draw=` key in a body file has to change. Fonts come from `helvet`.

A note on size: `dvisvgm` converts text to outlines, so these run ~285 KB raw (~95 KB
gzipped, which is what GitHub Pages serves) against ~9 KB for a hand-built one. That is
the price of a single source of truth. The text is not selectable.

## 2. Hand-built SVG — `gen_*.py`

Figures with no LaTeX original. `svgkit.py` holds the palette, typography and primitives
so they match the rendered ones.

```bash
for f in gen_*.py; do python3 "$f"; done
```

| Script | Figure | Used on |
| --- | --- | --- |
| `gen_prediction.py` | `prediction-problem.svg` | `/projects/eda-learn/` |
| `gen_overview.py` | `eda-learn-overview.svg` | `/projects/eda-learn/` |
| `gen_schema.py` | `eda-schema-pipeline.svg` | `/projects/eda-learn/` |
| `gen_openml.py` | `openml-workflow.svg` | `/eda-openml/` |

If a LaTeX original later appears for one of these, move it to `tex/` and delete the
script — `build.sh` writes to the same filename, so no page needs editing.

Preview any figure with `inkscape <file>.svg -o /tmp/check.png -w 1400`.
