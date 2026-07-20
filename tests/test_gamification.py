import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from koa import gamification


def test_level_info_thresholds():
    assert gamification.level_info(0)["level"] == 1
    assert gamification.level_info(99)["level"] == 1
    assert gamification.level_info(100)["level"] == 2  # level 1 costs 100
    # level 1 (100) + level 2 (200) = 300 clears into level 3
    lvl = gamification.level_info(300)
    assert lvl["level"] == 3
    assert lvl["into_level"] == 0
    assert lvl["next_level_xp"] == 300


def test_level_into_and_remaining():
    lvl = gamification.level_info(150)  # level 2, 50 into a 200-xp level
    assert lvl["level"] == 2
    assert lvl["into_level"] == 50
    assert lvl["next_level_xp"] == 200


def test_next_streak_transitions():
    assert gamification.next_streak(None, "2026-07-20", 0) == 1
    assert gamification.next_streak("2026-07-20", "2026-07-20", 4) == 4  # same day, no change
    assert gamification.next_streak("2026-07-19", "2026-07-20", 4) == 5  # consecutive
    assert gamification.next_streak("2026-07-10", "2026-07-20", 4) == 1  # gap resets


def test_earned_badges_from_snapshot():
    snapshot = {
        "learned": 8, "switch_best": 20, "arcade_best": 0,
        "songs": 1, "composed": 0, "notation": 0, "streak": 3,
    }
    earned = gamification.earned_badge_ids(snapshot)
    assert {"first_chord", "chord_collector", "quick_switch", "first_song", "on_a_roll"} <= earned
    assert "chord_master" not in earned  # needs 12
    assert "arcade_star" not in earned
    assert "week_warrior" not in earned  # needs 7-day streak


def test_no_badges_when_empty():
    empty = {k: 0 for k in ["learned", "switch_best", "arcade_best", "songs",
                            "composed", "notation", "streak"]}
    assert gamification.earned_badge_ids(empty) == set()
