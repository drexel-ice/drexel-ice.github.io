# EDA-Learn diagrams

The SVG figures on the EDA-Learn pages are generated, not hand-edited, so they share one
visual language. `svgkit.py` holds the palette (Drexel navy/blue plus green, amber and purple
tones), typography and primitives; each `gen_*.py` draws one figure.

```bash
cd _scripts/diagrams && for f in gen_*.py; do python3 "$f"; done
```

Output lands in `assets/img/projects/ml-eda/`:

| Script | Figure | Used on |
| --- | --- | --- |
| `gen_ecosystem.py` | `eda-learn-ecosystem.svg` | `/projects/eda-learn/` (hero) |
| `gen_prediction.py` | `prediction-problem.svg` | `/projects/eda-learn/` |
| `gen_overview.py` | `eda-learn-overview.svg` | `/projects/eda-learn/` |
| `gen_schema.py` | `eda-schema-pipeline.svg` | `/projects/eda-learn/` |
| `gen_openml.py` | `openml-workflow.svg` | `/eda-openml/` |

Preview a change with `inkscape <file>.svg -o /tmp/check.png -w 1200`.
