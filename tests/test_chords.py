import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from koa.data.chords import CHORDS, STRING_ORDER, fingering_text, get_chord

REQUIRED_KEYS = {"id", "name", "full_name", "difficulty", "frets", "fingers"}


def test_at_least_eight_chords():
    assert len(CHORDS) >= 8


def test_chord_shape_and_values():
    ids = set()
    for chord in CHORDS:
        assert REQUIRED_KEYS <= set(chord)
        assert chord["difficulty"] in {"easy", "medium", "hard"}
        assert set(chord["frets"]) == set(STRING_ORDER)
        for fret in chord["frets"].values():
            assert fret is None or (isinstance(fret, int) and 0 <= fret <= 12)
        ids.add(chord["id"])
    assert len(ids) == len(CHORDS)  # ids are unique


def test_fingers_match_fretted_strings():
    for chord in CHORDS:
        fretted = {s for s, f in chord["frets"].items() if f and f > 0}
        fingered = {f["string"] for f in chord["fingers"]}
        assert fingered == fretted, chord["id"]


def test_get_chord():
    assert get_chord("C")["full_name"] == "C major"
    assert get_chord("nope") is None


def test_fingering_text_is_human_readable():
    lines = fingering_text(get_chord("C"))
    assert any("ring finger" in line and "A string" in line for line in lines)
