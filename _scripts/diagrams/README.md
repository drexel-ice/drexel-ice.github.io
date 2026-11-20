# EDA-Learn diagrams

Every figure on the EDA-Learn pages is rendered from TikZ, so the website and the
LaTeX documents share one source and cannot drift apart. The bodies under `tex/`
hold only the drawing; `site-preamble.tex` holds everything that makes them look
like the website.

```bash
./build.sh                      # all figures
./build.sh eda-learn-ecosystem  # just one
```

Needs `latex` and `dvisvgm` (`texlive-latex-extra`, `texlive-font-utils`). Output
goes to `assets/img/projects/ml-eda/<name>.svg`.

| Body | Figure | Used on |
| --- | --- | --- |
| `tex/eda-learn-ecosystem.tex` | `eda-learn-ecosystem.svg` | `/projects/eda-learn/` (hero) |
| `tex/prediction-problem.tex` | `prediction-problem.svg` | `/projects/eda-learn/` |
| `tex/eda-learn-overview.tex` | `eda-learn-overview.svg` | `/projects/eda-learn/` |
| `tex/eda-schema-pipeline.tex` | `eda-schema-pipeline.svg` | `/projects/eda-learn/` |
| `tex/openml-workflow.tex` | `openml-workflow.svg` | `/eda-openml/` |

`eda-learn-ecosystem.tex` is a verbatim copy of the PESOSE Track 1 Figure 1 body.
The other four were drawn for the website.

## Adding a figure

Drop the `\begin{tikzpicture}...\end{tikzpicture}` into `tex/<name>.tex` and run
`./build.sh <name>`. Do not put `\documentclass`, `\usepackage`, colour definitions
or font commands in a body file — they belong in the preamble, and leaving them out
is what lets a body stay a straight copy of a document's own source.

## How a paper figure comes out looking like the site

`site-preamble.tex` redefines the *base* colours so that the `blue!7`, `green!7`,
`orange!8` and `purple!7` fills a proposal figure already uses land on the site
palette, and sets the ambient colour to Drexel navy — which TikZ also takes as its
default stroke colour. So no `fill=` or `draw=` key in a body file has to change.
Fonts come from `helvet`.

For figures drawn here rather than imported, the preamble also carries a shared
idiom: a `sitecanvas` style, a type scale (`kicker`, `body`, `lead`, `cardtitle`,
`figtitle`), surfaces (`card`, `panel`, `chip`) and connectors (`flow`, `hair`).

## Two things to know about the build

**It uses `latex` → DVI, not `pdflatex` → PDF.** The DVI route lets `dvisvgm` emit
real `<text>` elements with a subsetted woff2 font rather than tracing every glyph
as a path. That is about ten times smaller — the five figures total 58 KB gzipped
instead of 654 KB — and it leaves the text selectable and searchable. Embedded
woff2 does render inside an `<img>`-loaded SVG, which is how the pages include them.

**The dvips driver has no alpha channel.** Use a colour mix (`accamber!18`) rather
than `fill opacity=0.18`; opacity silently does nothing on this route.

Preview a figure with `inkscape <file>.svg -o /tmp/check.png -w 1300`.
