# -*- coding: utf-8 -*-
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Doc, TONE, NAVY, INK, MUTED, RULE
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "projects", "ml-eda")

W, H = 1200, 478
d = Doc(W, H, "Conventional early estimation compared with learned prediction",
        "The prediction problem: source-stage information, two estimators, one target-stage measurement")

BLUE, GREEN, AMBER = TONE["blue"], TONE["green"], TONE["amber"]

# ----------------------------------------------------------------- flow band
d.kicker(20, 18, "DIGITAL PHYSICAL DESIGN FLOW", MUTED)
STAGES = ["Logic synthesis", "Floorplan", "Global placement", "Detailed placement",
          "Clock tree synthesis", "Global routing", "Detailed routing"]
cw, gap, y0 = 152, 16, 30
for i, s in enumerate(STAGES):
    x = 20 + i * (cw + gap)
    src, tgt = (i == 2), (i == 6)
    tone = "blue" if src else ("amber" if tgt else "neutral")
    f, st, ac = TONE[tone]
    d.add(f'<rect x="{x}" y="{y0}" width="{cw}" height="44" rx="7" fill="{f}" stroke="{st}" '
          f'stroke-width="{1.8 if (src or tgt) else 1}"/>')
    d.head(x + cw / 2, y0 + 21, s, size=11.5, color=NAVY if (src or tgt) else INK,
           weight="700" if (src or tgt) else "400")
    if src or tgt:
        d.kicker(x + cw / 2, y0 + 36, "SOURCE STAGE" if src else "TARGET STAGE", ac, size=8.5, anchor="middle")
    if i < len(STAGES) - 1:
        d.add(f'<path d="M{x+cw+2},{y0+22} L{x+cw+gap-2},{y0+22}" stroke="{MUTED}" stroke-width="1.2"/>')

SRC_X, TGT_X = 20 + 2 * (cw + gap) + cw / 2, 20 + 6 * (cw + gap) + cw / 2

# ------------------------------------------------------- source information
d.add(f'<path d="M{SRC_X},{y0+44} L{SRC_X},96 L600,96 L600,110" stroke="{BLUE[2]}" '
      f'stroke-width="1.8" fill="none" marker-end="url(#ar)"/>')
d.card(300, 112, 600, 66, "blue", label="WHAT EXISTS AT THE SOURCE STAGE")
d.rows(313, 154, ["Numerical attributes  ·  spatial layout maps  ·  graph structure "
                  "— everything the flow has produced so far"], size=11.5)

# ------------------------------------------------------------- two branches
d.add(f'<path d="M600,178 L600,196 L330,196 L330,214" stroke="{MUTED}" stroke-width="1.6" '
      f'fill="none" marker-end="url(#ar)"/>')
d.add(f'<path d="M600,178 L600,196 L870,196 L870,214" stroke="{MUTED}" stroke-width="1.6" '
      f'fill="none" marker-end="url(#ar)"/>')

BRANCH = [
    dict(x=120, w=420, tone="blue", title="Conventional early estimation",
         lbl="ANALYTICAL ESTIMATOR",
         rows=["Wireload models, half-perimeter wirelength,", "Steiner trees, congestion heuristics"],
         out="Estimate"),
    dict(x=660, w=420, tone="green", title="Learned prediction",
         lbl="NEURAL PREDICTOR",
         rows=["Trained on EDA-Schema benchmarks and", "scored on circuits it has never seen"],
         out="Prediction"),
]
for b in BRANCH:
    x, w = b["x"], b["w"]
    f, st, ac = TONE[b["tone"]]
    d.panel(x, 216, w, 150, b["tone"])
    d.head(x + w / 2, 240, b["title"], size=13.5)
    d.card(x + 20, 252, w - 40, 62, b["tone"], label=b["lbl"])
    d.rows(x + 33, 292, b["rows"], size=11, pitch=14)
    pw = 150
    d.add(f'<rect x="{x + w/2 - pw/2}" y="326" width="{pw}" height="26" rx="13" fill="{ac}"/>')
    d.head(x + w / 2, 344, b["out"], size=11.5, color="#ffffff")
    d.add(f'<path d="M{x+w/2},314 L{x+w/2},322" stroke="{ac}" stroke-width="1.4"/>')
    d.arrow(x + w / 2, 366, x + w / 2, 394, color=ac, w=1.6, small=True)

# --------------------------------------------------- target-stage measurement
d.add(f'<path d="M{TGT_X},{y0+44} L{TGT_X},90 L1168,90 L1168,428 L906,428" '
      f'stroke="{AMBER[2]}" stroke-width="1.6" fill="none" stroke-dasharray="5 4" marker-end="url(#ar)"/>')
d.card(300, 396, 600, 66, "amber", label="TARGET-STAGE MEASUREMENT", white=False)
d.rows(313, 438, ["The real wirelength, delay or slack. Both estimates are scored against it — "],
       size=11.5)
d.rows(313, 452, ["it is the yardstick, never an input."], size=11.5)


print("ok")
d.save(os.path.join(OUT_DIR, "prediction-problem.svg"))
print("wrote prediction-problem.svg")
