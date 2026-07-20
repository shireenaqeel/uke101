import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from koa.arcade import GOOD_WINDOW, PERFECT_WINDOW, ArcadeEngine, judge, note_times
from koa.data.patterns import get_pattern


def test_judge_windows():
    assert judge(0.0) == "perfect"
    assert judge(PERFECT_WINDOW) == "perfect"
    assert judge(PERFECT_WINDOW + 0.01) == "good"
    assert judge(GOOD_WINDOW) == "good"
    assert judge(GOOD_WINDOW + 0.01) == "miss"
    assert judge(-0.05) == "perfect"  # sign-agnostic


def test_note_times_only_counts_strokes():
    pattern = get_pattern("basic_down")  # 4 downs in 8 slots
    times = note_times(pattern, bpm=60, loops=1)
    assert len(times) == 4
    # at 60 bpm an eighth note is 0.5s; downs sit on beats -> 0, 1, 2, 3s
    assert times == [0.0, 1.0, 2.0, 3.0]


def test_note_times_loops():
    pattern = get_pattern("basic_down")
    assert len(note_times(pattern, bpm=120, loops=3)) == 12


def test_perfect_tap_scores_and_builds_combo():
    eng = ArcadeEngine([1.0, 2.0])
    assert eng.tap(1.0) == "perfect"
    assert eng.tap(2.01) == "perfect"
    assert eng.score == 200
    assert eng.max_combo == 2


def test_good_tap_scores_less():
    eng = ArcadeEngine([1.0])
    assert eng.tap(1.12) == "good"
    assert eng.score == 50


def test_stray_tap_breaks_combo():
    eng = ArcadeEngine([1.0, 5.0])
    eng.tap(1.0)  # perfect, combo 1
    assert eng.combo == 1
    assert eng.tap(3.0) == "miss"  # nothing near -> stray
    assert eng.combo == 0


def test_expire_marks_missed_notes():
    eng = ArcadeEngine([1.0, 2.0])
    missed = eng.expire(now=3.0)
    assert missed == 2
    assert eng.counts["miss"] == 2
    assert eng.is_finished(3.0)


def test_accuracy():
    eng = ArcadeEngine([1.0, 2.0, 3.0, 4.0])
    eng.tap(1.0)  # perfect
    eng.tap(2.0)  # perfect
    eng.expire(5.0)  # remaining two missed
    assert eng.accuracy() == 0.5


def test_combo_multiplier_kicks_in_after_ten():
    eng = ArcadeEngine([float(i) for i in range(12)])
    for i in range(12):
        eng.tap(float(i))
    # first 10 hits at 1x (100 each) = 1000; 11th and 12th at 2x = 400; total 1400
    assert eng.score == 1400
    assert eng.max_combo == 12
