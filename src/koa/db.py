"""SQLite persistence for user progress.

Phase 1 only needs "which chords are marked learned", but the schema is the
seed of the wider UserProgress model (switch speeds, scores, streak) added in
later phases. One SQLite file, no server to run.
"""

import os
import sqlite3
from pathlib import Path

_DEFAULT_PATH = Path(__file__).resolve().parents[2] / "koa.db"


def db_path() -> Path:
    return Path(os.environ.get("KOA_DB_PATH", _DEFAULT_PATH))


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS learned_chords (
                chord_id   TEXT PRIMARY KEY,
                learned_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS switch_scores (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                drill_key        TEXT NOT NULL,
                switches         INTEGER NOT NULL,
                duration_seconds REAL NOT NULL,
                recorded_at      TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS arcade_scores (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id  TEXT NOT NULL,
                score       INTEGER NOT NULL,
                max_combo   INTEGER NOT NULL,
                recorded_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS songs_completed (
                song_id      TEXT PRIMARY KEY,
                completed_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )


def mark_learned(chord_id: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO learned_chords (chord_id) VALUES (?)", (chord_id,)
        )


def unmark_learned(chord_id: str) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM learned_chords WHERE chord_id = ?", (chord_id,))


def is_learned(chord_id: str) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM learned_chords WHERE chord_id = ?", (chord_id,)
        ).fetchone()
        return row is not None


def get_learned() -> set[str]:
    with _connect() as conn:
        rows = conn.execute("SELECT chord_id FROM learned_chords").fetchall()
        return {row["chord_id"] for row in rows}


def record_switch_score(drill_key: str, switches: int, duration_seconds: float) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO switch_scores (drill_key, switches, duration_seconds) VALUES (?, ?, ?)",
            (drill_key, switches, duration_seconds),
        )


def get_switch_best(drill_key: str) -> int | None:
    """Best clean-switch count recorded for a drill, or None if never attempted."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT MAX(switches) AS best FROM switch_scores WHERE drill_key = ?", (drill_key,)
        ).fetchone()
        return row["best"] if row and row["best"] is not None else None


def get_switch_history(drill_key: str, limit: int = 20) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT switches, duration_seconds, recorded_at
            FROM switch_scores WHERE drill_key = ?
            ORDER BY recorded_at DESC LIMIT ?
            """,
            (drill_key, limit),
        ).fetchall()
        return [dict(row) for row in rows]


def get_switch_bests() -> dict[str, int]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT drill_key, MAX(switches) AS best FROM switch_scores GROUP BY drill_key"
        ).fetchall()
        return {row["drill_key"]: row["best"] for row in rows}


def record_arcade_score(pattern_id: str, score: int, max_combo: int) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO arcade_scores (pattern_id, score, max_combo) VALUES (?, ?, ?)",
            (pattern_id, score, max_combo),
        )


def get_arcade_best(pattern_id: str) -> int | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT MAX(score) AS best FROM arcade_scores WHERE pattern_id = ?", (pattern_id,)
        ).fetchone()
        return row["best"] if row and row["best"] is not None else None


def get_arcade_bests() -> dict[str, int]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT pattern_id, MAX(score) AS best FROM arcade_scores GROUP BY pattern_id"
        ).fetchall()
        return {row["pattern_id"]: row["best"] for row in rows}


def mark_song_completed(song_id: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO songs_completed (song_id) VALUES (?)", (song_id,)
        )


def get_completed_songs() -> set[str]:
    with _connect() as conn:
        rows = conn.execute("SELECT song_id FROM songs_completed").fetchall()
        return {row["song_id"] for row in rows}
