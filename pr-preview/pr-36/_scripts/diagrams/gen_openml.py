# -*- coding: utf-8 -*-
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Doc, TONE, NAVY, INK, MUTED, RULE
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "projects", "ml-eda")

W, H = 1200, 376
d = Doc(W, H, "The EDA-OpenML workflow",
        "EDA-OpenML: from a prediction problem to a released, reproducible model package")

STEPS = [
    dict(n="1", t="Prediction problem", tone="blue",
         rows=[["PDK and source stage"], ["Target stage and quantity"],
               ["The EDA tool's own estimate", "as the reference baseline"]]),
    dict(n="2", t="Executable configuration", tone="green",
         rows=[["Ordered input features"], ["Network architecture"],
               ["Training hyperparameters"], ["Preprocessing"]]),
    dict(n="3", t="Circuit-disjoint evaluation", tone="amber",
         rows=[["Eighteen LOCO folds"], ["One circuit withheld entirely"],
               ["Train on 17, test on the 18th"], ["No circuit on both sides"]]),
    dict(n="4", t="Aggregation", tone="amber",
         rows=[["Fold-averaged — equal weight", "to every held-out circuit"],
               ["Sample-averaged — all out-of-", "fold predictions pooled"]]),
    dict(n="5", t="Released model package", tone="purple",
         rows=[["Configuration and fold weights"], ["Preprocessing statistics"],
               ["Out-of-fold predictions"], ["Metrics, reports, provenance"]]),
]

M, GAP = 16, 18
PW = (W - 2 * M - 4 * GAP) // 5
PY, PH = 28, 210
XS = [M + i * (PW + GAP) for i in range(5)]

for i, s in enumerate(STEPS):
    x = XS[i]
    f, st, ac = TONE[s["tone"]]
    d.panel(x, PY, PW, PH, s["tone"])
    d.add(f'<circle cx="{x+30}" cy="{PY+30}" r="14" fill="{ac}"/>')
    d.head(x + 30, PY + 35, s["n"], size=13.5, color="#ffffff")
    d.rows(x + 52, PY + 35, [s["t"]], size=12.5, fill=NAVY, weight="700")
    d.add(f'<line x1="{x+16}" y1="{PY+56}" x2="{x+PW-16}" y2="{PY+56}" stroke="{st}"/>')
    d.card(x + 14, PY + 68, PW - 28, 126, s["tone"])
    by = PY + 94
    for r in s["rows"]:
        d.add(f'<circle cx="{x+30}" cy="{by-4}" r="2.4" fill="{ac}"/>')
        d.rows(x + 40, by, r, size=10.5, pitch=14)
        by += 14 * len(r) + 9
    if i < 4:
        d.arrow(x + PW + 3, PY + PH / 2, x + PW + GAP - 3, PY + PH / 2, w=1.8, small=True)

# ---------------------------------------------------------------- source bar
BY = PY + PH + 34
d.card(M, BY, W - 2 * M, 56, "neutral", white=False)
d.rows(M + 22, BY + 33, ["EDA-Schema-V2 benchmarks"], size=14, fill=NAVY, weight="700")
d.rows(M + 262, BY + 33,
       ["4 open PDKs  ·  12 prediction tasks  ·  5 granularities  ·  18 circuits  ·  "
        "stage-specific EDA reference estimates"], size=12, fill=MUTED)
for i in range(3):
    cx = XS[i] + PW // 2
    d.arrow(cx, BY - 4, cx, PY + PH + 4, w=1.4, small=True)


print("ok")
d.save(os.path.join(OUT_DIR, "openml-workflow.svg"))
print("wrote openml-workflow.svg")
