import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from koa.data.drills import DRILLS, drill_key, drill_labels
from koa.metronome import interval_seconds, switches_per_minute


def test_interval_seconds():
    assert interval_seconds(60) == 1.0
    assert interval_seconds(120) == 0.5


def test_interval_rejects_non_positive():
    with pytest.raises(ValueError):
        interval_seconds(0)


def test_switches_per_minute():
    assert switches_per_minute(30, 60) == 30.0
    assert switches_per_minute(15, 30) == 30.0  # extrapolated
    assert switches_per_minute(5, 0) == 0.0


def test_two_chord_drill_key_is_order_independent():
    assert drill_key(["C", "Am"]) == drill_key(["Am", "C"])


def test_longer_loop_keeps_order():
    assert drill_key(["C", "Am", "F"]) == "C-Am-F"
    assert drill_key(["C", "Am", "F"]) != drill_key(["F", "Am", "C"])


def test_beginner_pairs_present():
    labels = {d["label"] for d in DRILLS}
    for expected in ["C ↔ Am", "C ↔ F", "Am ↔ F", "G ↔ Em"]:
        assert expected in labels


def test_drill_labels_map_keys_to_labels():
    labels = drill_labels()
    assert labels[drill_key(["C", "Am"])] == "C ↔ Am"
    assert labels[drill_key(["C", "Am", "F"])] == "C – Am – F"
