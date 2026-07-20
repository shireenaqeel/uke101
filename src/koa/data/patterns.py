"""Strumming pattern content layer.

Each pattern is a fixed grid of eighth-note slots (2 per beat). A slot is a
downstroke, an upstroke, or a rest. This uniform grid lets one renderer draw
every pattern and one playback loop tick through any of them at eighth-note
resolution.
"""

D, U, R = "D", "U", "rest"

STRUMMING_PATTERNS = [
    {
        "id": "basic_down",
        "name": "Basic Down",
        "time_signature": "4/4",
        "slots": [D, R, D, R, D, R, D, R],
        "songs": "Almost any first song",
    },
    {
        "id": "down_up",
        "name": "Down-Up Eighths",
        "time_signature": "4/4",
        "slots": [D, U, D, U, D, U, D, U],
        "songs": "Keeps a steady eighth-note groove",
    },
    {
        "id": "island",
        "name": "Island Strum",
        "time_signature": "4/4",
        "slots": [D, R, D, U, R, U, D, U],
        "songs": "Riptide, I'm Yours, Soul Sister",
    },
    {
        "id": "folk",
        "name": "Folk Strum",
        "time_signature": "4/4",
        "slots": [D, R, D, U, U, R, D, U],
        "songs": "Many folk & pop songs",
    },
    {
        "id": "waltz",
        "name": "Waltz",
        "time_signature": "3/4",
        "slots": [D, R, D, R, D, R],
        "songs": "3/4 songs (e.g. Over the Rainbow feel)",
    },
    {
        "id": "reggae",
        "name": "Reggae / Off-beat",
        "time_signature": "4/4",
        "slots": [R, U, R, U, R, U, R, U],
        "songs": "Reggae, ska upstrokes",
    },
]

PATTERNS_BY_ID = {p["id"]: p for p in STRUMMING_PATTERNS}


def get_pattern(pattern_id: str) -> dict | None:
    return PATTERNS_BY_ID.get(pattern_id)


def beat_labels(pattern: dict) -> list[str]:
    """Count labels under each slot: '1 & 2 & 3 & 4 &' at eighth-note spacing."""
    labels = []
    for i in range(len(pattern["slots"])):
        labels.append(str(i // 2 + 1) if i % 2 == 0 else "&")
    return labels
