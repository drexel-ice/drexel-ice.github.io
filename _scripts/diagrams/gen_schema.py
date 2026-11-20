# -*- coding: utf-8 -*-
import os
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "projects", "ml-eda")
"""Generate the EDA-Schema pipeline diagram: generation -> representation -> benchmarks."""

W, H = 1200, 502
FONT = "Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif"
NAVY, INK, MUTED, RULE = "#07294d", "#1f2d3a", "#55687c", "#dde4ec"

PY, PH = 16, 470
PANES = [
    dict(x=16,  w=372, title="Dataset Generation",        fill="#eef6fd", stroke="#b7d8f4", accent="#1d7dce"),
    dict(x=406, w=410, title="Multimodal Representation", fill="#fff7e4", stroke="#f0dca8", accent="#a97b09"),
    dict(x=834, w=350, title="Benchmarks",                fill="#ecf7f0", stroke="#bbe1cb", accent="#1b8a51"),
]

o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  'role="img" aria-label="How EDA-Schema is generated, represented and benchmarked">')
a('<title>EDA-Schema: dataset generation, multimodal representation, and benchmark tasks</title>')
a('<defs>'
  f'<marker id="a1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
  f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
  '<linearGradient id="hm" x1="0" y1="0" x2="1" y2="1">'
  '<stop offset="0%" stop-color="#2b6cb0"/><stop offset="55%" stop-color="#e3b505"/>'
  '<stop offset="100%" stop-color="#c0392b"/></linearGradient>'
  '</defs>')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
a(f'<g font-family="{FONT}">')


def card(x, y, w, h, stroke, label=None, accent=None):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#ffffff" stroke="{stroke}"/>')
    if label:
        a(f'<text x="{x+13}" y="{y+19}" font-size="10" font-weight="700" letter-spacing="0.9" '
          f'fill="{accent}">{label}</text>')


def rows(x, y, lines, size=12, pitch=17, fill=INK, weight="400"):
    for i, ln in enumerate(lines):
        a(f'<text x="{x}" y="{y+i*pitch}" font-size="{size}" font-weight="{weight}" fill="{fill}">{ln}</text>')


def callout(x, y, w, lines, accent, stroke):
    h = 22 + 15 * len(lines)
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#ffffff" stroke="{accent}" stroke-dasharray="4 3"/>')
    for i, ln in enumerate(lines):
        a(f'<text x="{x+13}" y="{y+19+i*15}" font-size="11.5" font-weight="500" fill="{accent}">{ln}</text>')


def footer(x, y, w, text, accent):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="7" fill="{accent}" fill-opacity="0.1"/>')
    a(f'<text x="{x+w/2:.0f}" y="{y+19}" font-size="12" font-weight="700" fill="{accent}" text-anchor="middle">{text}</text>')


# ---- panel shells -----------------------------------------------------------
for p in PANES:
    a(f'<rect x="{p["x"]}" y="{PY}" width="{p["w"]}" height="{PH}" rx="12" fill="{p["fill"]}" stroke="{p["stroke"]}"/>')
    a(f'<text x="{p["x"]+p["w"]/2:.0f}" y="{PY+34}" font-size="17" font-weight="700" fill="{NAVY}" '
      f'text-anchor="middle">{p["title"]}</text>')

# chevrons between panels
for i in (0, 1):
    gx = PANES[i]["x"] + PANES[i]["w"]
    a(f'<path d="M{gx+3},{PY+PH/2} L{PANES[i+1]["x"]-4},{PY+PH/2}" stroke="{MUTED}" stroke-width="2" '
      'fill="none" marker-end="url(#a1)"/>')

# =============================== PANEL 1 =====================================
p = PANES[0]; X, Wd, AC, ST = p["x"], p["w"], p["accent"], p["stroke"]
card(X+14, 66, Wd-28, 80, ST, "DESIGN SPACE", AC)
rows(X+27, 42+6+1, [])
rows(X+27, 102, ["18 benchmark circuits — IWLS'05, OpenCores, IBEX",
                 "4 open PDKs — NG45, SKY130, IHP130, ASAP7",
                 "Sweeps — clock period, utilization, aspect ratio"], size=11.5, pitch=16)
cxa = X + 14 + (Wd - 28) / 2
a(f'<path d="M{cxa:.0f},146 L{cxa:.0f},162" stroke="{MUTED}" stroke-width="1.6" fill="none" marker-end="url(#a1)"/>')

STAGES = ["Logic synthesis", "Floorplan", "Global placement", "Detailed placement",
          "Clock tree synthesis", "Global routing", "Detailed routing"]
sx, sw, y0 = X + 24, 152, 162
for i, s in enumerate(STAGES):
    y = y0 + i * 29
    a(f'<rect x="{sx}" y="{y}" width="{sw}" height="24" rx="5" fill="#ffffff" stroke="{ST}"/>')
    a(f'<text x="{sx+sw/2:.0f}" y="{y+16}" font-size="11" fill="{INK}" text-anchor="middle">{s}</text>')
    if i < len(STAGES) - 1:
        a(f'<path d="M{sx+sw/2:.0f},{y+24} L{sx+sw/2:.0f},{y+29}" stroke="{AC}" stroke-width="1.4"/>')
a(f'<text x="{sx+sw/2:.0f}" y="{y0-6}" font-size="10" font-weight="700" letter-spacing="0.9" '
  f'fill="{AC}" text-anchor="middle">OPENROAD FLOW</text>')

ax, aw = X + 192, 156
card(ax, y0, aw, 196, ST, "STORED PER STAGE", AC)
rows(ax + 13, y0 + 42, ["Verilog netlist", "DEF / LEF geometry", "Timing reports (STA)",
                        "SPEF parasitics", "Power + IR-drop analysis", "QoR metrics and logs"],
     size=11.5, pitch=21)
for i in range(len(STAGES)):
    yy = y0 + i * 29 + 12
    a(f'<path d="M{sx+sw+3},{yy} L{ax-4},{yy}" stroke="{AC}" stroke-opacity="0.22" stroke-width="1"/>')

callout(X + 14, 374, Wd - 28, ["Sweeps deliberately include barely-passing",
                               "and barely-failing operating points"], AC, ST)
footer(X + 14, 436, Wd - 28, "7,776 design instances  ·  1,944 per PDK", AC)

# =============================== PANEL 2 =====================================
p = PANES[1]; X, Wd, AC, ST = p["x"], p["w"], p["accent"], p["stroke"]
card(X+14, 66, Wd-28, 64, ST, "STAGE-AWARE PROPERTY GRAPH", AC)
rows(X+27, 102, ["Flow · stage · constraints   |   netlist, clock tree, timing path, PDN",
                 "gates, nets, pins, arcs   |   cell, area, power, timing, routability QoR"],
     size=11, pitch=16)

MODS = [
    ("GRAPH", ["Netlist graph, timing-path subgraphs, and an",
               "interconnect graph with wire segments as nodes"]),
    ("IMAGE", ["Binary spatial maps — combinational and sequential",
               "cell placement, pin locations, per-layer routing"]),
    ("HEATMAP", ["RUDY routability (net, pin, long- and short-range),",
                 "IR-drop and electromigration maps"]),
]
my = 142
for i, (name, lines) in enumerate(MODS):
    y = my + i * 78
    card(X + 14, y, Wd - 28, 70, ST)
    gx, gy = X + 28, y + 12
    a(f'<rect x="{gx}" y="{gy}" width="46" height="46" rx="6" fill="{p["fill"]}" stroke="{ST}"/>')
    if name == "GRAPH":
        pts = [(gx+13, gy+13), (gx+33, gy+12), (gx+10, gy+33), (gx+24, gy+26), (gx+36, gy+34)]
        for (ax1, ay1), (bx1, by1) in [(pts[0], pts[3]), (pts[1], pts[3]), (pts[2], pts[3]), (pts[3], pts[4])]:
            a(f'<line x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}" stroke="{AC}" stroke-width="1.2"/>')
        for (cx, cy) in pts:
            a(f'<circle cx="{cx}" cy="{cy}" r="3.6" fill="{AC}"/>')
    elif name == "IMAGE":
        fills = [1, 0, 1, 1, 1, 0, 0, 1, 1]
        for k in range(9):
            rx_, ry_ = gx + 9 + (k % 3) * 10, gy + 9 + (k // 3) * 10
            a(f'<rect x="{rx_}" y="{ry_}" width="8" height="8" rx="1.5" fill="{AC}" '
              f'fill-opacity="{0.85 if fills[k] else 0.18}"/>')
    else:
        for k in range(4):
            a(f'<rect x="{gx+8+k*8}" y="{gy+9}" width="7" height="28" rx="1.5" fill="url(#hm)" '
              f'fill-opacity="{0.4 + 0.2*k:.2f}"/>')
    a(f'<text x="{gx+58}" y="{gy+15}" font-size="10" font-weight="700" letter-spacing="0.9" fill="{AC}">{name}</text>')
    rows(gx + 58, gy + 32, lines, size=11, pitch=15)

callout(X + 14, 374, Wd - 28, ["Every attribute records the stage at which it becomes available,",
                               "so the information boundary is part of the task definition"], AC, ST)
footer(X + 14, 436, Wd - 28, "275 M+ gates  ·  75 M+ nets  ·  36 M+ timing paths", AC)

# =============================== PANEL 3 =====================================
p = PANES[2]; X, Wd, AC, ST = p["x"], p["w"], p["accent"], p["stroke"]
card(X+14, 66, Wd-28, 148, ST, "TWELVE PREDICTION TASKS", AC)
TASKS = [("Whole circuit", "area, power, total wirelength"),
         ("Whole circuit", "worst arrival, worst slack, TNS"),
         ("Per interconnect", "length"),
         ("Per timing path", "arrival time, slack"),
         ("Per net arc", "delay"),
         ("Per cell arc", "delay, slew")]
for i, (g, t) in enumerate(TASKS):
    y = 110 + i * 18
    a(f'<text x="{X+27}" y="{y}" font-size="11" font-weight="700" fill="{AC}">{g}</text>')
    a(f'<text x="{X+127}" y="{y}" font-size="11" fill="{INK}">{t}</text>')

card(X+14, 226, Wd-28, 83, ST, "EACH TASK FIXES", AC)
rows(X+27, 262, ["Source stage → target stage",
                 "The EDA tool's own estimate as reference",
                 "MAE, MAPE, R² and upper-tail metrics"], size=11.5, pitch=17)

card(X+14, 321, Wd-28, 83, ST, "EVALUATION", AC)
rows(X+27, 357, ["Leave-one-circuit-out — 18 folds",
                 "One circuit withheld entirely per fold",
                 "Generalization, not interpolation"], size=11.5, pitch=17)

footer(X + 14, 436, Wd - 28, "Open leaderboard  ·  CC BY-NC-SA 4.0", AC)

a('</g></svg>')

print("ok")
open(os.path.join(OUT_DIR, "eda-schema-pipeline.svg"), "w").write("\n".join(o))
print("wrote eda-schema-pipeline.svg")
