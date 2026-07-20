"""Chord content layer.

Plain data only — no UI, no audio. Ordered easiest to hardest. Frets are given
per string in reentrant tuning order G-C-E-A (0 = open, None = muted).
Fingers are listed in plain language so the UI can show "ring finger, A string,
3rd fret" without hardcoding anything per chord.
"""

STRING_ORDER = ["G", "C", "E", "A"]

CHORDS = [
    {
        "id": "C",
        "name": "C",
        "full_name": "C major",
        "difficulty": "easy",
        "frets": {"G": 0, "C": 0, "E": 0, "A": 3},
        "fingers": [{"string": "A", "fret": 3, "finger": "ring"}],
    },
    {
        "id": "Am",
        "name": "Am",
        "full_name": "A minor",
        "difficulty": "easy",
        "frets": {"G": 2, "C": 0, "E": 0, "A": 0},
        "fingers": [{"string": "G", "fret": 2, "finger": "middle"}],
    },
    {
        "id": "F",
        "name": "F",
        "full_name": "F major",
        "difficulty": "easy",
        "frets": {"G": 2, "C": 0, "E": 1, "A": 0},
        "fingers": [
            {"string": "G", "fret": 2, "finger": "middle"},
            {"string": "E", "fret": 1, "finger": "index"},
        ],
    },
    {
        "id": "A7",
        "name": "A7",
        "full_name": "A dominant 7th",
        "difficulty": "easy",
        "frets": {"G": 0, "C": 1, "E": 0, "A": 0},
        "fingers": [{"string": "C", "fret": 1, "finger": "index"}],
    },
    {
        "id": "C7",
        "name": "C7",
        "full_name": "C dominant 7th",
        "difficulty": "easy",
        "frets": {"G": 0, "C": 0, "E": 0, "A": 1},
        "fingers": [{"string": "A", "fret": 1, "finger": "index"}],
    },
    {
        "id": "G7",
        "name": "G7",
        "full_name": "G dominant 7th",
        "difficulty": "easy",
        "frets": {"G": 0, "C": 2, "E": 1, "A": 2},
        "fingers": [
            {"string": "E", "fret": 1, "finger": "index"},
            {"string": "C", "fret": 2, "finger": "middle"},
            {"string": "A", "fret": 2, "finger": "ring"},
        ],
    },
    {
        "id": "G",
        "name": "G",
        "full_name": "G major",
        "difficulty": "medium",
        "frets": {"G": 0, "C": 2, "E": 3, "A": 2},
        "fingers": [
            {"string": "C", "fret": 2, "finger": "index"},
            {"string": "A", "fret": 2, "finger": "middle"},
            {"string": "E", "fret": 3, "finger": "ring"},
        ],
    },
    {
        "id": "A",
        "name": "A",
        "full_name": "A major",
        "difficulty": "medium",
        "frets": {"G": 2, "C": 1, "E": 0, "A": 0},
        "fingers": [
            {"string": "G", "fret": 2, "finger": "middle"},
            {"string": "C", "fret": 1, "finger": "index"},
        ],
    },
    {
        "id": "D",
        "name": "D",
        "full_name": "D major",
        "difficulty": "medium",
        "frets": {"G": 2, "C": 2, "E": 2, "A": 0},
        "fingers": [
            {"string": "G", "fret": 2, "finger": "index"},
            {"string": "C", "fret": 2, "finger": "middle"},
            {"string": "E", "fret": 2, "finger": "ring"},
        ],
    },
    {
        "id": "Em",
        "name": "Em",
        "full_name": "E minor",
        "difficulty": "hard",
        "frets": {"G": 0, "C": 4, "E": 3, "A": 2},
        "fingers": [
            {"string": "A", "fret": 2, "finger": "index"},
            {"string": "E", "fret": 3, "finger": "middle"},
            {"string": "C", "fret": 4, "finger": "ring"},
        ],
    },
    {
        "id": "D7",
        "name": "D7",
        "full_name": "D dominant 7th",
        "difficulty": "hard",
        "frets": {"G": 2, "C": 2, "E": 2, "A": 3},
        "fingers": [
            {"string": "G", "fret": 2, "finger": "index"},
            {"string": "C", "fret": 2, "finger": "index"},
            {"string": "E", "fret": 2, "finger": "index"},
            {"string": "A", "fret": 3, "finger": "ring"},
        ],
    },
    {
        "id": "Bb",
        "name": "Bb",
        "full_name": "B-flat major",
        "difficulty": "hard",
        "frets": {"G": 3, "C": 2, "E": 1, "A": 3},
        "fingers": [
            {"string": "E", "fret": 1, "finger": "index"},
            {"string": "C", "fret": 2, "finger": "middle"},
            {"string": "G", "fret": 3, "finger": "ring"},
            {"string": "A", "fret": 3, "finger": "pinky"},
        ],
    },
]

CHORDS_BY_ID = {chord["id"]: chord for chord in CHORDS}

_ORDINALS = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th"}


def get_chord(chord_id: str) -> dict | None:
    return CHORDS_BY_ID.get(chord_id)


def fingering_text(chord: dict) -> list[str]:
    """Plain-language fingering instructions, one line per finger."""
    lines = []
    for f in chord["fingers"]:
        fret = _ORDINALS.get(f["fret"], f"{f['fret']}th")
        lines.append(f"{f['finger']} finger on the {f['string']} string, {fret} fret")
    open_strings = [s for s in STRING_ORDER if chord["frets"].get(s) == 0]
    if open_strings:
        lines.append(f"leave {', '.join(open_strings)} open")
    return lines
