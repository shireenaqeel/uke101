"""SVG renderers for the notation drills (rhythm symbols, treble staff, uke tab).

Framework-agnostic strings, like the fretboard renderer, so drills can be drawn
anywhere and unit-tested. Engraving is intentionally simplified but legible —
these are teaching visuals, not a scoring engine.
"""

_INK = "#333333"
_LETTERS = "CDEFGAB"

# ukulele tab lines, top (highest) to bottom
_TAB_LINES = ["A", "E", "C", "G"]


def render_notation(spec: dict) -> str:
    kind = spec["type"]
    if kind == "rhythm":
        return _rhythm(spec["symbol"])
    if kind == "staff":
        return _staff(spec["note"])
    if kind == "tab":
        return _tab(spec["string"], spec["fret"])
    raise ValueError(f"unknown notation type: {kind}")


def _svg(width: int, height: int, body: str, label: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{label}">{body}</svg>'
    )


# --------------------------------------------------------------------------- #
# Rhythm — notes and rests
# --------------------------------------------------------------------------- #
def _rhythm(symbol: str) -> str:
    nx, ny, stem_top = 52, 74, 28
    stem_x = nx + 10

    def head(filled: bool) -> str:
        fill = _INK if filled else "none"
        return (
            f'<ellipse cx="{nx}" cy="{ny}" rx="11" ry="8" fill="{fill}" stroke="{_INK}" '
            f'stroke-width="2.5" transform="rotate(-20 {nx} {ny})"/>'
        )

    stem = f'<line x1="{stem_x}" y1="{ny - 3}" x2="{stem_x}" y2="{stem_top}" stroke="{_INK}" stroke-width="2.5"/>'
    flag = (
        f'<path d="M{stem_x},{stem_top} C{stem_x + 16},{stem_top + 6} {stem_x + 16},'
        f'{stem_top + 20} {stem_x + 3},{stem_top + 27}" fill="none" stroke="{_INK}" stroke-width="2.5"/>'
    )
    ref = f'<line x1="26" y1="64" x2="94" y2="64" stroke="#bbbbbb" stroke-width="1.5"/>'

    body = {
        "whole": head(False),
        "half": head(False) + stem,
        "quarter": head(True) + stem,
        "eighth": head(True) + stem + flag,
        # rests are drawn relative to a reference line: whole hangs below, half sits above
        "whole_rest": ref + '<rect x="52" y="64" width="22" height="7" fill="#333"/>',
        "half_rest": ref + '<rect x="52" y="57" width="22" height="7" fill="#333"/>',
        "quarter_rest": (
            '<path d="M50,48 C58,56 46,60 54,68 C62,75 50,78 58,86 '
            'C51,82 62,90 55,95" fill="none" stroke="#333" stroke-width="3" stroke-linecap="round"/>'
        ),
        "eighth_rest": (
            '<circle cx="52" cy="56" r="4.5" fill="#333"/>'
            '<line x1="55" y1="56" x2="45" y2="88" stroke="#333" stroke-width="2.5"/>'
        ),
    }[symbol]
    return _svg(120, 120, body, f"{symbol} symbol")


# --------------------------------------------------------------------------- #
# Staff — a note on the treble clef
# --------------------------------------------------------------------------- #
def _dindex(note: str) -> int:
    return int(note[1:]) * 7 + _LETTERS.index(note[0])


def _staff(note: str) -> str:
    top, gap = 40, 12
    lines = [top + i * gap for i in range(5)]  # F5 D5 B4 G4 E4 top->bottom
    bottom_line = lines[-1]  # E4
    step = _dindex(note) - _dindex("E4")
    y = bottom_line - step * (gap // 2)

    parts = []
    for ly in lines:
        parts.append(f'<line x1="20" y1="{ly}" x2="160" y2="{ly}" stroke="{_INK}" stroke-width="1.3"/>')

    # simplified treble (G) clef
    parts.append(
        f'<path d="M30,34 C20,40 22,58 32,60 C43,62 43,46 33,46 C27,46 27,54 33,54" '
        f'fill="none" stroke="{_INK}" stroke-width="2"/>'
        f'<line x1="33" y1="30" x2="33" y2="96" stroke="{_INK}" stroke-width="2"/>'
        f'<circle cx="33" cy="98" r="3" fill="{_INK}"/>'
    )

    # ledger lines for note positions on lines outside the staff (e.g. middle C)
    nx = 120
    if step < 0 and step % 2 == 0:
        for s in range(-2, step - 1, -2):
            ly = bottom_line - s * (gap // 2)
            parts.append(f'<line x1="{nx - 14}" y1="{ly}" x2="{nx + 14}" y2="{ly}" stroke="{_INK}" stroke-width="1.3"/>')

    parts.append(
        f'<ellipse cx="{nx}" cy="{y}" rx="8" ry="6" fill="{_INK}" transform="rotate(-20 {nx} {y})"/>'
    )
    parts.append(f'<line x1="{nx + 7}" y1="{y}" x2="{nx + 7}" y2="{y - 34}" stroke="{_INK}" stroke-width="2"/>')
    return _svg(175, 130, "".join(parts), f"note {note} on treble staff")


# --------------------------------------------------------------------------- #
# Tab — a fret number on the 4-line ukulele tab
# --------------------------------------------------------------------------- #
def _tab(string: str, fret: int) -> str:
    top, gap = 25, 20
    ys = {name: top + i * gap for i, name in enumerate(_TAB_LINES)}
    parts = []
    for name, ly in ys.items():
        parts.append(f'<line x1="34" y1="{ly}" x2="160" y2="{ly}" stroke="{_INK}" stroke-width="1.3"/>')
        parts.append(
            f'<text x="20" y="{ly + 4}" text-anchor="middle" font-size="12" fill="#888">{name}</text>'
        )
    ny = ys[string]
    parts.append(f'<rect x="92" y="{ny - 9}" width="20" height="18" fill="white"/>')
    parts.append(
        f'<text x="102" y="{ny + 5}" text-anchor="middle" font-size="16" font-weight="bold" '
        f'fill="{_INK}">{fret}</text>'
    )
    return _svg(175, 110, "".join(parts), f"tab {string} string fret {fret}")
