"""Adaptive difficulty / recommendation logic (first ML phase, no audio).

Pure functions over the progress data the app already tracks — rule-based, in
the spirit of spaced repetition: surface the weak spots and recommend what
unlocks the most next. Kept in ``koa.ml`` so it can grow into a real model
(bandit, spaced-repetition scheduler) without touching the UI.
"""

from koa.data.chords import CHORDS
from koa.data.drills import DRILLS, drill_key
from koa.data.songs import SONGS

_DIFF_ORDER = {"easy": 0, "medium": 1, "hard": 2}


def recommend_chords(learned, songs=SONGS, chords=CHORDS) -> list[dict]:
    """Unlearned chords ranked by how many songs learning them would unlock.

    A song is "unlocked" by a chord when that chord is the only one from the
    song the learner is still missing. Ties break toward easier chords, then
    toward chords that appear in more songs overall.
    """
    learned = set(learned)
    recs = []
    for chord in chords:
        cid = chord["id"]
        if cid in learned:
            continue
        using = [s for s in songs if cid in s["chords_used"]]
        unlocks = sum(1 for s in using if set(s["chords_used"]) - learned == {cid})
        recs.append(
            {
                "chord": cid,
                "difficulty": chord["difficulty"],
                "unlocks": unlocks,
                "songs_using": len(using),
            }
        )
    recs.sort(key=lambda r: (-r["unlocks"], _DIFF_ORDER[r["difficulty"]], -r["songs_using"]))
    return recs


def weak_drills(switch_bests, drills=DRILLS) -> list[dict]:
    """Switch drills ranked weakest-first: never-attempted, then lowest best."""
    out = []
    for drill in drills:
        key = drill_key(drill["chords"])
        best = switch_bests.get(key)
        out.append({"drill": drill, "key": key, "best": best})
    out.sort(key=lambda r: (0 if r["best"] is None else 1, r["best"] or 0))
    return out


def songs_playable_now(learned, songs=SONGS, completed=()) -> list[dict]:
    """Songs whose chords are all learned and that aren't completed yet."""
    learned = set(learned)
    completed = set(completed)
    return [
        s for s in songs if set(s["chords_used"]) <= learned and s["id"] not in completed
    ]


def songs_one_away(learned, songs=SONGS) -> list[dict]:
    """Songs the learner could play after learning exactly one more chord."""
    learned = set(learned)
    result = []
    for song in songs:
        missing = set(song["chords_used"]) - learned
        if len(missing) == 1:
            result.append({"song": song, "missing": next(iter(missing))})
    return result
