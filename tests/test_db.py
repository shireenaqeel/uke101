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
