"""Data-driven fretboard diagram renderer.

Returns an SVG string for a chord's fingering. Framework-agnostic (just a
string), so the chord library, switching trainer and song mode all share this
one renderer instead of duplicating diagram logic.
"""

STRING_ORDER = ["G", "C", "E", "A"]
FINGER_INITIALS = {"index": "1", "middle": "2", "ring": "3", "pinky": "4"}


def render_fretboard(chord: dict, num_frets: int = 4, width: int = 150, height: int = 190) -> str:
    frets = chord["frets"]
    finger_by_string = {f["string"]: f for f in chord.get("fingers", [])}

    pad_x = 22
    pad_top = 30
    pad_bottom = 22
    inner_w = width - 2 * pad_x
    board_h = height - pad_top - pad_bottom
    n_strings = len(STRING_ORDER)

    string_x = [pad_x + i * inner_w / (n_strings - 1) for i in range(n_strings)]
    fret_h = board_h / num_frets

    def fret_line_y(k: int) -> float:
        return pad_top + k * fret_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{chord["name"]} chord diagram">'
    ]
    stroke = "#5b5b6b"

    # Nut (thick top line) then the fret lines below it.
    parts.append(
        f'<line x1="{string_x[0]:.1f}" y1="{pad_top}" x2="{string_x[-1]:.1f}" y2="{pad_top}" '
        f'stroke="{stroke}" stroke-width="4" stroke-linecap="round"/>'
    )
    for k in range(1, num_frets + 1):
        y = fret_line_y(k)
        parts.append(
            f'<line x1="{string_x[0]:.1f}" y1="{y:.1f}" x2="{string_x[-1]:.1f}" y2="{y:.1f}" '
            f'stroke="{stroke}" stroke-width="1.5"/>'
        )

    # Vertical strings.
    for x in string_x:
        parts.append(
            f'<line x1="{x:.1f}" y1="{pad_top}" x2="{x:.1f}" y2="{fret_line_y(num_frets):.1f}" '
            f'stroke="{stroke}" stroke-width="1.5"/>'
        )

    # Markers per string: open circle, muted x, or a fingered dot.
    for i, s in enumerate(STRING_ORDER):
        x = string_x[i]
        fret = frets.get(s)
        if fret is None:
            parts.append(
                f'<text x="{x:.1f}" y="{pad_top - 10}" text-anchor="middle" '
                f'font-size="12" fill="{stroke}">×</text>'
            )
        elif fret == 0:
            parts.append(
                f'<circle cx="{x:.1f}" cy="{pad_top - 13}" r="5" fill="none" '
                f'stroke="{stroke}" stroke-width="1.5"/>'
            )
        else:
            cy = pad_top + (fret - 0.5) * fret_h
            parts.append(f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="9" fill="#7c5cff"/>')
            label = FINGER_INITIALS.get(finger_by_string.get(s, {}).get("finger", ""), "")
            if label:
                parts.append(
                    f'<text x="{x:.1f}" y="{cy + 4:.1f}" text-anchor="middle" '
                    f'font-size="11" fill="white" font-weight="bold">{label}</text>'
                )

    # String name labels along the bottom.
    label_y = height - 6
    for i, s in enumerate(STRING_ORDER):
        parts.append(
            f'<text x="{string_x[i]:.1f}" y="{label_y}" text-anchor="middle" '
            f'font-size="11" fill="#8a8a99">{s}</text>'
        )

    parts.append("</svg>")
    return "".join(parts)
