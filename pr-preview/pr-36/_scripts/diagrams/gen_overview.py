# -*- coding: utf-8 -*-
import os
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "projects", "ml-eda")
"""Generate the EDA-Learn four-layer overview diagram."""

W, H = 1200, 486
FONT = "Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif"

NAVY = "#07294d"
INK = "#1f2d3a"
MUTED = "#55687c"
RULE = "#d7dee6"

PANELS = [
    dict(n="1", title="EDA-Schema", status="PUBLISHED",
         fill="#eef6fd", stroke="#b7d8f4", accent="#1d7dce",
         q=["What is the data, and what", "exactly is being predicted?"],
         bullets=[["Stage-aware multimodal data model"],
                  ["7,776 open design instances", "across four open PDKs"],
                  ["Twelve benchmark prediction tasks"],
                  ["The EDA tool's own estimate as", "the reference baseline"]]),
    dict(n="2", title="EDA-OpenML", status="IN PREPARATION",
         fill="#ecf7f0", stroke="#bbe1cb", accent="#1b8a51",
         q=["Is the result reproducible,", "and does it hold on new circuits?"],
         bullets=[["Executable model configurations"],
                  ["Leave-one-circuit-out evaluation", "on eighteen held-out circuits"],
                  ["Open-weight release: configs,", "weights, predictions, metrics"],
                  ["Public leaderboard"]]),
    dict(n="3", title="EDA-AutoML", status="IN PROGRESS",
         fill="#fff7e4", stroke="#f0dca8", accent="#a97b09",
         q=["Can the configuration be", "chosen automatically?"],
         bullets=[["TPE architecture and hyper-", "parameter search"],
                  ["Candidates scored by", "circuit-disjoint error"],
                  ["Same tasks and protocol as", "the fixed reference model"]]),
    dict(n="4", title="Neural Architect Agent", status="IN PROGRESS",
         fill="#f5f0fb", stroke="#d8cbee", accent="#6b4fa8",
         q=["Is the search loop", "needed at all?"],
         bullets=[["An LLM reads the task and a", "summary of the data"],
                  ["Returns one executable", "configuration — no search"],
                  ["Evaluated under the same", "circuit-disjoint protocol"]]),
]

M, GAP = 16, 24
PW = (W - 2 * M - 3 * GAP) // 4          # 274
PY, PH = 92, 292
XS = [M + i * (PW + GAP) for i in range(4)]

o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'role="img" aria-label="The four layers of EDA-Learn">')
a('<title>EDA-Learn: four layers, each defined on top of the one before it</title>')
a('<defs>'
  '<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
  f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
  '</defs>')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
a(f'<g font-family="{FONT}">')

# ---- source bar -------------------------------------------------------------
a(f'<rect x="{M}" y="14" width="{W-2*M}" height="48" rx="9" fill="#f3f5f8" stroke="{RULE}"/>')
a(f'<text x="{M+20}" y="44" font-size="15" font-weight="700" fill="{NAVY}">Digital physical design</text>')
a(f'<text x="{M+200}" y="44" font-size="13" fill="{MUTED}">'
  '18 benchmark circuits  ·  4 open PDKs  ·  OpenROAD flow, synthesis through detailed routing  ·  stage artifacts</text>')
cx1 = XS[0] + PW // 2
a(f'<path d="M{cx1},62 L{cx1},{PY-4}" stroke="{MUTED}" stroke-width="1.6" fill="none" marker-end="url(#ar)"/>')

# ---- panels -----------------------------------------------------------------
for i, p in enumerate(PANELS):
    x = XS[i]
    a(f'<rect x="{x}" y="{PY}" width="{PW}" height="{PH}" rx="11" fill="{p["fill"]}" stroke="{p["stroke"]}"/>')
    # badge + title
    a(f'<circle cx="{x+32}" cy="{PY+30}" r="15" fill="{p["accent"]}"/>')
    a(f'<text x="{x+32}" y="{PY+35}" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">{p["n"]}</text>')
    a(f'<text x="{x+56}" y="{PY+36}" font-size="15.5" font-weight="700" fill="{NAVY}">{p["title"]}</text>')
    # status pill
    pw = 15 + 7.1 * len(p["status"])
    a(f'<rect x="{x+16}" y="{PY+56}" width="{pw:.0f}" height="20" rx="10" fill="#ffffff" stroke="{p["stroke"]}"/>')
    a(f'<text x="{x+16+pw/2:.0f}" y="{PY+70}" font-size="9.5" font-weight="700" letter-spacing="0.8" '
      f'fill="{p["accent"]}" text-anchor="middle">{p["status"]}</text>')
    # question
    qy = PY + 100
    for ln in p["q"]:
        a(f'<text x="{x+16}" y="{qy}" font-size="12.5" font-style="italic" fill="{MUTED}">{ln}</text>')
        qy += 17
    a(f'<line x1="{x+16}" y1="{PY+132}" x2="{x+PW-16}" y2="{PY+132}" stroke="{p["stroke"]}"/>')
    # bullets
    by = PY + 158
    for b in p["bullets"]:
        a(f'<circle cx="{x+20}" cy="{by-4}" r="2.6" fill="{p["accent"]}"/>')
        for j, ln in enumerate(b):
            a(f'<text x="{x+32}" y="{by + j*16}" font-size="12.5" fill="{INK}">{ln}</text>')
        by += 16 * len(b) + 10
    # chevron to next panel
    if i < 3:
        gx = x + PW
        a(f'<path d="M{gx+5},{PY+PH/2} L{gx+GAP-4},{PY+PH/2}" stroke="{MUTED}" stroke-width="1.8" '
          f'fill="none" marker-end="url(#ar)"/>')
    # tick down into the artifact bar
    cx = x + PW // 2
    a(f'<path d="M{cx},{PY+PH} L{cx},{PY+PH+24}" stroke="{MUTED}" stroke-width="1.4" fill="none" marker-end="url(#ar)"/>')

# ---- artifact bar -----------------------------------------------------------
BY = PY + PH + 32
a(f'<rect x="{M}" y="{BY}" width="{W-2*M}" height="54" rx="9" fill="#f3f5f8" stroke="{RULE}"/>')
a(f'<text x="{M+20}" y="{BY+32}" font-size="15" font-weight="700" fill="{NAVY}">Released artifacts</text>')
a(f'<text x="{M+180}" y="{BY+32}" font-size="13" fill="{MUTED}">'
  'open dataset  ·  executable configurations  ·  trained weights  ·  out-of-fold predictions  ·  evaluation metrics  ·  public leaderboard</text>')

a('</g></svg>')

print("ok")
open(os.path.join(OUT_DIR, "eda-learn-overview.svg"), "w").write("\n".join(o))
print("wrote eda-learn-overview.svg")
