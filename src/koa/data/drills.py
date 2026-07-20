"""Chord-switching drill presets, ordered easiest first.

A drill is just an ordered loop of chord ids. Two-chord drills are the core
beginner exercise; three- and four-chord loops come next. The highlight in the
trainer cycles through the loop and each completed change counts as one switch.
"""

DRILLS = [
    {"label": "C ↔ Am", "chords": ["C", "Am"], "group": "Beginner pairs"},
    {"label": "C ↔ F", "chords": ["C", "F"], "group": "Beginner pairs"},
    {"label": "Am ↔ F", "chords": ["Am", "F"], "group": "Beginner pairs"},
    {"label": "G ↔ Em", "chords": ["G", "Em"], "group": "Beginner pairs"},
    {"label": "C – Am – F", "chords": ["C", "Am", "F"], "group": "Three-chord loops"},
    {"label": "G – Em – C", "chords": ["G", "Em", "C"], "group": "Three-chord loops"},
    {"label": "C – Am – F – G", "chords": ["C", "Am", "F", "G"], "group": "Four-chord loops"},
]


def drill_key(chords: list[str]) -> str:
    """Stable id for storing a score. Two-chord drills are order-independent
    (C→Am and Am→C are the same skill); longer loops keep their order."""
    seq = list(chords)
    if len(seq) == 2:
        seq = sorted(seq)
    return "-".join(seq)


def drill_labels() -> dict[str, str]:
    """Map each preset drill's storage key to its human label, for the dashboard."""
    return {drill_key(d["chords"]): d["label"] for d in DRILLS}
