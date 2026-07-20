import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from koa.data.patterns import STRUMMING_PATTERNS, beat_labels, get_pattern

VALID = {"D", "U", "rest"}


def test_at_least_three_patterns():
    assert len(STRUMMING_PATTERNS) >= 3


def test_pattern_shape():
    ids = set()
    for pattern in STRUMMING_PATTERNS:
        assert {"id", "name", "time_signature", "slots", "songs"} <= set(pattern)
        assert pattern["slots"], pattern["id"]
        assert all(slot in VALID for slot in pattern["slots"])
        assert len(pattern["slots"]) % 2 == 0  # whole beats at eighth resolution
        ids.add(pattern["id"])
    assert len(ids) == len(STRUMMING_PATTERNS)


def test_time_signature_matches_slot_count():
    for pattern in STRUMMING_PATTERNS:
        beats = int(pattern["time_signature"].split("/")[0])
        assert len(pattern["slots"]) == beats * 2


def test_beat_labels():
    pattern = get_pattern("basic_down")
    assert beat_labels(pattern) == ["1", "&", "2", "&", "3", "&", "4", "&"]
    assert beat_labels(get_pattern("waltz")) == ["1", "&", "2", "&", "3", "&"]


def test_get_pattern():
    assert get_pattern("island")["name"] == "Island Strum"
    assert get_pattern("nope") is None
