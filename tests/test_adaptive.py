import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from koa.data.drills import drill_key
from koa.ml import adaptive

# Minimal fixed content so the assertions don't depend on the full song library.
SONGS = [
    {"id": "riptide", "title": "Riptide", "chords_used": ["Am", "G", "C"]},
    {"id": "twinkle", "title": "Twinkle", "chords_used": ["C", "F", "G7"]},
]
CHORDS = [
    {"id": "C", "difficulty": "easy"},
    {"id": "Am", "difficulty": "easy"},
    {"id": "G", "difficulty": "medium"},
    {"id": "F", "difficulty": "easy"},
    {"id": "G7", "difficulty": "easy"},
]


def test_recommend_chords_prioritises_unlocking():
    # Knowing Am and G, learning C completes Riptide -> C should top the list.
    recs = adaptive.recommend_chords({"Am", "G"}, songs=SONGS, chords=CHORDS)
    assert recs[0]["chord"] == "C"
    assert recs[0]["unlocks"] == 1


def test_recommend_chords_skips_learned():
    recs = adaptive.recommend_chords({"C"}, songs=SONGS, chords=CHORDS)
    assert all(r["chord"] != "C" for r in recs)


def test_recommend_chords_new_user_prefers_easy_common():
    recs = adaptive.recommend_chords(set(), songs=SONGS, chords=CHORDS)
    # No song is one-chord-away yet, so it falls to easiest + most-used: C.
    assert recs[0]["chord"] == "C"


def test_weak_drills_untried_first():
    bests = {drill_key(["C", "Am"]): 30}
    ranked = adaptive.weak_drills(bests)
    assert ranked[0]["best"] is None  # an untried drill leads
    am_c = next(r for r in ranked if r["key"] == drill_key(["C", "Am"]))
    assert am_c["best"] == 30


def test_songs_playable_now_excludes_completed():
    playable = adaptive.songs_playable_now(
        {"C", "F", "G7"}, songs=SONGS, completed={"twinkle"}
    )
    assert playable == []  # twinkle would qualify but is completed
    playable = adaptive.songs_playable_now({"C", "F", "G7"}, songs=SONGS)
    assert [s["id"] for s in playable] == ["twinkle"]


def test_songs_one_away():
    result = adaptive.songs_one_away({"Am", "G"}, songs=SONGS)
    assert len(result) == 1
    assert result[0]["song"]["id"] == "riptide"
    assert result[0]["missing"] == "C"
