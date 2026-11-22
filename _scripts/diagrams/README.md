# EDA-Learn diagrams

Every figure on the EDA-Learn pages is rendered from TikZ, so the website and the
LaTeX documents share one source and cannot drift apart. A body under `tex/` holds
only the drawing; a preamble holds everything else.

```bash
./build.sh                      # all figures
./build.sh eda-learn-ecosystem  # just one
```

Needs `latex` and `dvisvgm` (`texlive-latex-extra`, `texlive-font-utils`). Output
goes to `assets/img/projects/ml-eda/<name>.svg`.

| Body | Figure | Source | Used on |
| --- | --- | --- | --- |
| `tex/eda-learn-ecosystem.tex` | `eda-learn-ecosystem.svg` | PESOSE Track 1, Fig. 1 (adapted) | `/projects/eda-learn/` (hero) |
| `tex/prediction-problem.tex` | `prediction-problem.svg` | drawn here | `/projects/eda-learn/` |
| `tex/openml-config-flow.tex` | `openml-config-flow.svg` | drawn here | `/projects/eda-learn/` |
| `tex/openml-workflow.tex` | `openml-workflow.svg` | EDA-OpenML paper, Fig. 2 | `/eda-openml/` |

## Adding a figure

Drop the `\begin{tikzpicture}...\end{tikzpicture}` into `tex/<name>.tex` and run
`./build.sh <name>`. Do not put `\documentclass`, `\usepackage`, colour definitions
or font commands in a body file — they belong in a preamble, and leaving them out
is what lets a body stay a straight copy of a document's own source.

## Which preamble a figure gets

A body carrying the line `%!preamble: verbatim` is built with
**`verbatim-preamble.tex`**, which renders it exactly as its source document does:
stock `xcolor` tints, `lmodern`, black rules. Use this when the figure has to match
the printed version. Every current figure does.

Everything else is built with **`site-preamble.tex`**, which restyles a figure to
look like the website without touching its body. It redefines the *base* colours so
the `blue!7`, `green!7`, `orange!8` and `purple!7` fills a paper figure already uses
land on the site palette, and sets the ambient colour to Drexel navy — which TikZ
also takes as its default stroke colour. So no `fill=` or `draw=` key has to change.
Fonts come from `helvet`. It also carries a shared idiom for figures drawn here
rather than imported: a `sitecanvas` style, a type scale (`kicker`, `body`, `lead`,
`cardtitle`, `figtitle`), surfaces (`card`, `panel`, `chip`) and connectors (`flow`,
`hair`).

**No figure currently uses `site-preamble.tex`** — it is kept for the next one that
should match the site rather than a paper.

## Three things to know about the build

**It uses `latex` → DVI, not `pdflatex` → PDF.** The DVI route lets `dvisvgm` emit
real `<text>` elements with a subsetted font rather than tracing every glyph as a
path. That is roughly ten times smaller — the figures total well under 100 KB gzipped — and
it leaves the text selectable and searchable. Embedded fonts do render inside an
`<img>`-loaded SVG, which is how the pages include them.

**Font format follows the preamble.** Computer Modern comes out of `woff2` with
wrong advance widths ("ED A-Learn", "benchmarkcircuits"), so verbatim figures are
built with `ttf` and site figures with the smaller `woff2`. `build.sh` picks this.

**The dvips driver has no alpha channel.** Use a colour mix (`accamber!18`) rather
than `fill opacity=0.18`; opacity silently does nothing on this route.

## Previewing

Open the SVG in a browser, not `inkscape` — inkscape misrenders the embedded `ttf`
fonts and will show broken letter spacing that is not in the file. A quick check:

```bash
printf '<img src="%s" style="width:1200px">' NAME.svg > /tmp/p.html
google-chrome --headless=new --screenshot=/tmp/p.png --window-size=1240,800 file:///tmp/p.html
```
