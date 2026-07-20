"""XP, levels, streaks and badges.

Sits on top of the progress data the rest of the app already stores. The math
(levels, streak transitions, badge rules) is pure and testable; only
``record_activity`` and ``build_snapshot`` touch the database.
"""

from datetime import date, timedelta

from koa import db

# XP awarded per kind of practice action.
XP = {
    "chord_learned": 10,
    "switch_drill": 15,
    "arcade_game": 20,
    "song": 30,
    "composed_song": 25,
    "notation_session": 15,
}


def level_info(xp: int) -> dict:
    """Level, XP into the current level, and XP needed to reach the next.

    Level L costs L*100 XP to clear, so levels get progressively longer.
    """
    level = 1
    floor = 0
    while xp >= floor + level * 100:
        floor += level * 100
        level += 1
    return {
        "level": level,
        "into_level": xp - floor,
        "next_level_xp": level * 100,
        "total_xp": xp,
    }


def next_streak(last_date: str | None, today: str, current: int) -> int:
    """New streak-day count given the last active date and today (ISO strings)."""
    if last_date is None or current <= 0:
        return 1
    if last_date == today:
        return current
    if date.fromisoformat(today) - date.fromisoformat(last_date) == timedelta(days=1):
        return current + 1
    return 1  # a gap (or clock going backwards) resets the streak


def record_activity(source: str, xp: int | None = None) -> None:
    """Award XP for a practice action and keep the daily streak up to date."""
    amount = XP.get(source, 0) if xp is None else xp
    db.add_xp(source, amount)
    today = date.today().isoformat()
    streak = db.get_streak()
    db.set_streak(next_streak(streak["last_date"], today, streak["current"]), today)


# --------------------------------------------------------------------------- #
# Badges
# --------------------------------------------------------------------------- #
BADGES = [
    {"id": "first_chord", "name": "First Steps", "icon": "🎸",
     "desc": "Learn your first chord", "predicate": lambda s: s["learned"] >= 1},
    {"id": "chord_collector", "name": "Chord Collector", "icon": "📚",
     "desc": "Learn 8 chords", "predicate": lambda s: s["learned"] >= 8},
    {"id": "chord_master", "name": "Chord Master", "icon": "👑",
     "desc": "Learn every chord", "predicate": lambda s: s["learned"] >= 12},
    {"id": "quick_switch", "name": "Quick Switch", "icon": "⚡",
     "desc": "20 clean switches in a drill", "predicate": lambda s: s["switch_best"] >= 20},
    {"id": "lightning_hands", "name": "Lightning Hands", "icon": "🔥",
     "desc": "40 clean switches in a drill", "predicate": lambda s: s["switch_best"] >= 40},
    {"id": "arcade_star", "name": "Arcade Star", "icon": "🌟",
     "desc": "Score 1000 in the Strum Arcade", "predicate": lambda s: s["arcade_best"] >= 1000},
    {"id": "first_song", "name": "First Song", "icon": "🎵",
     "desc": "Finish a song end to end", "predicate": lambda s: s["songs"] >= 1},
    {"id": "performer", "name": "Performer", "icon": "🎤",
     "desc": "Finish 5 songs", "predicate": lambda s: s["songs"] >= 5},
    {"id": "songwriter", "name": "Songwriter", "icon": "✍️",
     "desc": "Compose your own song", "predicate": lambda s: s["composed"] >= 1},
    {"id": "note_reader", "name": "Note Reader", "icon": "🎼",
     "desc": "Reach level 1 in a notation track", "predicate": lambda s: s["notation"] >= 1},
    {"id": "on_a_roll", "name": "On a Roll", "icon": "📅",
     "desc": "Practice 3 days in a row", "predicate": lambda s: s["streak"] >= 3},
    {"id": "week_warrior", "name": "Week Warrior", "icon": "🏆",
     "desc": "Practice 7 days in a row", "predicate": lambda s: s["streak"] >= 7},
]


def build_snapshot() -> dict:
    """Collect the progress figures the badge rules test against."""
    return {
        "learned": len(db.get_learned()),
        "switch_best": max(db.get_switch_bests().values(), default=0),
        "arcade_best": max(db.get_arcade_bests().values(), default=0),
        "songs": len(db.get_completed_songs()),
        "composed": len(db.get_composed_songs()),
        "notation": max(db.get_notation_progress().values(), default=0),
        "streak": db.get_streak()["current"],
    }


def earned_badge_ids(snapshot: dict) -> set[str]:
    return {b["id"] for b in BADGES if b["predicate"](snapshot)}
