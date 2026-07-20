import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import importlib

import pytest


@pytest.fixture
def db(tmp_path, monkeypatch):
    monkeypatch.setenv("KOA_DB_PATH", str(tmp_path / "test.db"))
    from koa import db as db_module

    importlib.reload(db_module)
    db_module.init_db()
    return db_module


def test_mark_and_unmark(db):
    assert db.get_learned() == set()
    db.mark_learned("C")
    db.mark_learned("Am")
    assert db.is_learned("C")
    assert db.get_learned() == {"C", "Am"}
    db.unmark_learned("C")
    assert not db.is_learned("C")
    assert db.get_learned() == {"Am"}


def test_mark_is_idempotent(db):
    db.mark_learned("F")
    db.mark_learned("F")
    assert db.get_learned() == {"F"}


def test_persists_across_connections(db, tmp_path):
    # A fresh reload pointed at the same file must still see the data.
    db.mark_learned("G")
    from koa import db as reopened

    importlib.reload(reopened)
    assert reopened.is_learned("G")


def test_switch_best_tracks_maximum(db):
    assert db.get_switch_best("Am-C") is None
    db.record_switch_score("Am-C", 20, 60.0)
    db.record_switch_score("Am-C", 34, 60.0)
    db.record_switch_score("Am-C", 28, 60.0)
    assert db.get_switch_best("Am-C") == 34


def test_switch_history_and_bests(db):
    db.record_switch_score("Am-C", 20, 60.0)
    db.record_switch_score("C-F", 15, 60.0)
    assert len(db.get_switch_history("Am-C")) == 1
    assert db.get_switch_bests() == {"Am-C": 20, "C-F": 15}


def test_arcade_best_and_bests(db):
    assert db.get_arcade_best("island") is None
    db.record_arcade_score("island", 1200, 14)
    db.record_arcade_score("island", 1800, 20)
    db.record_arcade_score("folk", 900, 8)
    assert db.get_arcade_best("island") == 1800
    assert db.get_arcade_bests() == {"island": 1800, "folk": 900}


def test_song_completion(db):
    assert db.get_completed_songs() == set()
    db.mark_song_completed("twinkle")
    db.mark_song_completed("twinkle")  # idempotent
    db.mark_song_completed("saints")
    assert db.get_completed_songs() == {"twinkle", "saints"}
