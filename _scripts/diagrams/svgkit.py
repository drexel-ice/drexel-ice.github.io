# -*- coding: utf-8 -*-
"""Shared drawing language for the EDA-Learn diagrams."""

FONT = "Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif"
NAVY, INK, MUTED, RULE = "#07294d", "#1f2d3a", "#55687c", "#dde4ec"

# role -> (fill, stroke, accent)
TONE = {
    "blue":    ("#eef6fd", "#b7d8f4", "#1d7dce"),
    "green":   ("#ecf7f0", "#bbe1cb", "#1b8a51"),
    "amber":   ("#fff7e4", "#f0dca8", "#a97b09"),
    "purple":  ("#f5f0fb", "#d8cbee", "#6b4fa8"),
    "neutral": ("#f3f5f8", "#d7dee6", "#55687c"),
}


class Doc:
    def __init__(self, w, h, label, title):
        self.w, self.h = w, h
        self.o = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}">',
            f'<title>{title}</title>',
            '<defs>'
            f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
            f'<marker id="arb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
            '</defs>',
            f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
            f'<g font-family="{FONT}">',
        ]

    a = property(lambda self: self.o.append)

    def add(self, s):
        self.o.append(s)

    # --- primitives ----------------------------------------------------------
    def panel(self, x, y, w, h, tone="neutral", rx=12, dashed=False, fill=None):
        f, s, _ = TONE[tone]
        d = ' stroke-dasharray="6 4"' if dashed else ''
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                 f'fill="{fill or f}" stroke="{s}"{d}/>')

    def card(self, x, y, w, h, tone="neutral", rx=8, label=None, white=True):
        f, s, ac = TONE[tone]
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                 f'fill="{"#ffffff" if white else f}" stroke="{s}"/>')
        if label:
            self.kicker(x + 13, y + 19, label, ac)

    def kicker(self, x, y, text, color, size=10, anchor="start"):
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="700" letter-spacing="0.9" '
                 f'fill="{color}" text-anchor="{anchor}">{text}</text>')

    def head(self, x, y, text, size=17, color=None, anchor="middle", weight="700"):
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{color or NAVY}" text-anchor="{anchor}">{text}</text>')

    def rows(self, x, y, lines, size=11, pitch=15, fill=INK, anchor="start", weight="400", style=""):
        st = f' font-style="{style}"' if style else ""
        for i, ln in enumerate(lines):
            self.add(f'<text x="{x}" y="{y+i*pitch}" font-size="{size}" font-weight="{weight}" '
                     f'fill="{fill}" text-anchor="{anchor}"{st}>{ln}</text>')

    def arrow(self, x1, y1, x2, y2, color=None, w=1.8, both=False, small=False):
        m = "arb" if small else "ar"
        s = f' marker-start="url(#{m})"' if both else ""
        self.add(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color or MUTED}" stroke-width="{w}" '
                 f'fill="none" marker-end="url(#{m})"{s}/>')

    def chip(self, x, y, text, tone, size=9.5, h=19):
        _, s, ac = TONE[tone]
        w = 14 + 6.9 * len(text)
        self.add(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="#ffffff" stroke="{s}"/>')
        self.kicker(x + w / 2, y + h / 2 + 3.5, text, ac, size=size, anchor="middle")
        return w

    def save(self, path):
        self.o.append('</g></svg>')
        open(path, "w").write("\n".join(self.o))
