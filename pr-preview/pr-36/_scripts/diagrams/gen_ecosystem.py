# -*- coding: utf-8 -*-
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Doc, TONE, NAVY, INK, MUTED, RULE
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "projects", "ml-eda")

W, H = 1200, 482
d = Doc(W, H, "The EDA-Learn technical ecosystem",
        "EDA-Learn: open inputs, the four components, and who uses them")

# ------------------------------------------------------------------ open inputs
IX, IW, IY, IH = 16, 176, 44, 268
d.panel(IX, IY, IW, IH, "neutral", dashed=True, fill="#ffffff")
d.kicker(IX + IW / 2, IY + 24, "OPEN INPUTS", MUTED, anchor="middle")
INPUTS = [("Open-source designs", ["18 benchmark circuits"]),
          ("OpenROAD / ORFS", ["RTL-to-GDSII flow"]),
          ("Open PDKs", ["4 technology nodes"])]
for i, (t, sub) in enumerate(INPUTS):
    y = IY + 46 + i * 74
    d.card(IX + 14, y, IW - 28, 62, "blue", white=False)
    d.head(IX + IW / 2, y + 25, t, size=12, color=NAVY)
    d.rows(IX + IW / 2, y + 43, sub, size=10.5, fill=MUTED, anchor="middle")

# ------------------------------------------------------------------ main frame
FX, FY, FW, FH = 228, 44, 956, 268
d.add(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="14" fill="#fbfcfe" stroke="{RULE}" stroke-width="1.6"/>')
d.add(f'<rect x="{FX+22}" y="{FY-11}" width="104" height="22" rx="11" fill="#ffffff" stroke="{RULE}"/>')
d.kicker(FX + 74, FY + 4, "EDA-LEARN", NAVY, size=10.5, anchor="middle")
d.arrow(IX + IW + 5, IY + IH / 2, FX - 5, IY + IH / 2)

CX0, CW, CGAP = 242, 222, 16
COLS = [
    dict(name="EDA-datagen", tone="green", chip="IN DEVELOPMENT",
         code=["Hydra wrapper and", "flow automation"],
         data=("RAW DATASET", ["4 PDKs · 108 configurations", "~2 TB of flow output"])),
    dict(name="EDA-Schema", tone="green", chip="PUBLIC TODAY",
         code=["Schema definition and", "data processing"],
         data=("PROCESSED DATASETS", ["Full set ~400 GB", "Barely-pass / fail set ~10 GB"])),
    dict(name="EDA-ML / AutoML", tone="green", chip="IN PROGRESS",
         code=["12 prediction tasks,", "training and AutoML"],
         data=("MODEL ARTIFACTS", ["Weights and configurations", "Metrics and provenance"])),
    dict(name="Leaderboard", tone="purple", chip="LIVE",
         code=["Rankings against the", "EDA tool baseline"],
         data=("BENCHMARKING", ["Released models", "Comparison playground"])),
]
for i, c in enumerate(COLS):
    x = CX0 + i * (CW + CGAP)
    d.head(x + CW / 2, FY + 36, c["name"], size=14.5)
    cw = 14 + 6.9 * len(c["chip"])
    d.chip(x + CW / 2 - cw / 2, FY + 46, c["chip"], c["tone"], size=9)
    kind = "CODEBASE" if i < 3 else "SERVICE"
    cy = FY + 82
    d.card(x, cy, CW, 76, "green" if i < 3 else "purple", label=kind)
    d.rows(x + 13, cy + 42, c["code"], size=11, pitch=15)
    dy = cy + 90
    lbl, lines = c["data"]
    d.card(x, dy, CW, 76, "amber" if i < 3 else "purple", label=lbl)
    d.rows(x + 13, dy + 42, lines, size=11, pitch=15)
    if i < 3:
        gx = x + CW
        d.arrow(gx + 3, FY + 160, gx + CGAP - 3, FY + 160, w=1.6, small=True)

# ------------------------------------------------------------------ users band
UY, UH = FY + FH + 30, 96
d.panel(FX, UY, FW, UH, "neutral", dashed=True, fill="#ffffff")
d.arrow(FX + FW / 2, FY + FH + 4, FX + FW / 2, UY - 4, w=1.6, both=True, small=True)
USERS = [("ML and EDA researchers", "use + compare"),
         ("Universities and students", "research + training"),
         ("EDA and semiconductor industry", "evaluate + guide"),
         ("Contributors and maintainers", "data + code + models")]
for i, (t, sub) in enumerate(USERS):
    x = CX0 + i * (CW + CGAP)
    d.card(x, UY + 16, CW, 64, "blue", white=False)
    d.head(x + CW / 2, UY + 40, t, size=11.5, color=NAVY)
    d.rows(x + CW / 2, UY + 58, [sub], size=10.5, fill=MUTED, anchor="middle")
d.kicker(FX + FW / 2, UY + UH + 20, "USERS AND CONTRIBUTORS", MUTED, anchor="middle")


print("ok")
d.save(os.path.join(OUT_DIR, "eda-learn-ecosystem.svg"))
print("wrote eda-learn-ecosystem.svg")
