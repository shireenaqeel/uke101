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
