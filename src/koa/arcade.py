"""Strum Arcade scoring engine.

Pure timing logic, no UI or wall-clock of its own: the caller feeds it "the
game clock now reads t seconds" for every tap and on every frame. That keeps
the Perfect/Good/Miss judgment, combo and score fully unit-testable.
"""

from koa.metronome import interval_seconds

PERFECT_WINDOW = 0.08  # seconds of error still counted as a perfect hit
GOOD_WINDOW = 0.18  # beyond this, a note is missed
POINTS = {"perfect": 100, "good": 50, "miss": 0}


def judge(error: float) -> str:
    """Classify a timing error (seconds, sign-agnostic) into a hit grade."""
    e = abs(error)
    if e <= PERFECT_WINDOW:
        return "perfect"
    if e <= GOOD_WINDOW:
        return "good"
    return "miss"


def note_times(pattern: dict, bpm: float, loops: int) -> list[float]:
    """Ideal hit time (seconds from start) for every strum in the looped pattern."""
    eighth = interval_seconds(bpm) / 2
    slots = pattern["slots"]
    n = len(slots)
    times = []
    for loop in range(loops):
        for i, slot in enumerate(slots):
            if slot in ("D", "U"):
                times.append((loop * n + i) * eighth)
    return times


class ArcadeEngine:
    def __init__(self, times: list[float]):
        self.notes = [{"time": t, "hit": False} for t in times]
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.counts = {"perfect": 0, "good": 0, "miss": 0}

    @property
    def total_notes(self) -> int:
        return len(self.notes)

    def _register(self, grade: str) -> None:
        if grade == "miss":
            self.combo = 0
        else:
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            multiplier = 1 + (self.combo - 1) // 10
            self.score += POINTS[grade] * multiplier
        self.counts[grade] += 1

    def tap(self, now: float) -> str:
        """Register a player tap at game time ``now`` and return its grade.

        Matches the nearest not-yet-resolved note within the good window; a tap
        with no note nearby is a stray and breaks the combo.
        """
        best = None
        best_err = None
        for note in self.notes:
            if note["hit"]:
                continue
            err = now - note["time"]
            if abs(err) <= GOOD_WINDOW and (best_err is None or abs(err) < abs(best_err)):
                best, best_err = note, err
        if best is None:
            self._register("miss")
            return "miss"
        best["hit"] = True
        grade = judge(best_err)
        self._register(grade)
        return grade

    def expire(self, now: float) -> int:
        """Resolve notes whose window has fully passed as misses. Returns how many."""
        missed = 0
        for note in self.notes:
            if not note["hit"] and now - note["time"] > GOOD_WINDOW:
                note["hit"] = True
                self._register("miss")
                missed += 1
        return missed

    def is_finished(self, now: float) -> bool:
        return all(n["hit"] for n in self.notes) or (
            bool(self.notes) and now - self.notes[-1]["time"] > GOOD_WINDOW
        )

    def accuracy(self) -> float:
        """Fraction of notes hit at all (perfect or good), 0..1."""
        if not self.notes:
            return 0.0
        hits = self.counts["perfect"] + self.counts["good"]
        return hits / len(self.notes)
