import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from koa import chordpro, songbook


# --- ChordPro parser ------------------------------------------------------- #
def test_parse_line_places_chords_by_word():
    line = chordpro.parse_line("[C]Twinkle twinkle [F]little [C]star")
    assert line["text"] == "Twinkle twinkle little star"
    assert line["chords"] == [
        {"word": 0, "chord": "C"},
        {"word": 2, "chord": "F"},
        {"word": 3, "chord": "C"},
    ]


def test_parse_line_midword_chord_attaches_to_word():
    line = chordpro.parse_line("Twin[C]kle")
    assert line["text"] == "Twinkle"
    assert line["chords"] == [{"word": 0, "chord": "C"}]


def test_parse_line_without_chords():
    line = chordpro.parse_line("just some words")
    assert line["text"] == "just some words"
    assert line["chords"] == []


def test_parse_song_lines_skips_blanks():
    lines = chordpro.parse_song_lines("[C]one\n\n[F]two\n")
    assert len(lines) == 2
    assert lines[1]["text"] == "two"


def test_line_to_chordpro_roundtrip():
    original = "[C]Twinkle twinkle [F]little [C]star"
    line = chordpro.parse_line(original)
    assert chordpro.line_to_chordpro(line) == original


# --- composition ----------------------------------------------------------- #
def test_build_chart_song_from_progression():
    song = songbook.build_composed_song(
        title="Loop", artist="Me", tempo=100, pattern_id="island",
        progression=["C", "Am", "F", "G"], lyrics_text="",
    )
    assert song["is_user_composed"] is True
    assert song["lyrics_included"] is False
    assert song["progression"] == ["C", "Am", "F", "G"]
    assert song["chords_used"] == ["C", "Am", "F", "G"]
    assert song["lines"] == []
    assert song["id"].startswith("user-")


def test_build_lyric_song_derives_chords_and_difficulty():
    song = songbook.build_composed_song(
        title="Hard One", artist="Me", tempo=90, pattern_id="basic_down",
        progression=[], lyrics_text="[C]easy then [Em]hard chord",
    )
    assert song["lyrics_included"] is True
    assert song["chords_used"] == ["C", "Em"]
    assert song["difficulty"] == "hard"  # Em is hard -> song is hard
    assert song["lines"][0]["text"] == "easy then hard chord"


def test_hardest_difficulty():
    assert songbook.hardest_difficulty(["C", "Am"]) == "easy"
    assert songbook.hardest_difficulty(["C", "G"]) == "medium"
    assert songbook.hardest_difficulty(["C", "Bb"]) == "hard"
    assert songbook.hardest_difficulty([]) == "easy"


def test_chord_chart_text_for_chart_and_lyric_songs():
    chart = songbook.build_composed_song(
        title="Loop", artist="Me", tempo=100, pattern_id="island",
        progression=["C", "F"], lyrics_text="",
    )
    text = songbook.chord_chart_text(chart)
    assert "Loop" in text and "Progression: C | F" in text

    lyric = songbook.build_composed_song(
        title="Song", artist="Me", tempo=90, pattern_id="basic_down",
        progression=[], lyrics_text="[C]hello [F]world",
    )
    assert "[C]hello [F]world" in songbook.chord_chart_text(lyric)


# --- persistence + resolution --------------------------------------------- #
@pytest.fixture
def fresh_db(tmp_path, monkeypatch):
    monkeypatch.setenv("KOA_DB_PATH", str(tmp_path / "test.db"))
    from koa import db as db_module

    importlib.reload(db_module)
    importlib.reload(songbook)
    db_module.init_db()
    return db_module


def test_save_and_resolve_composed_song(fresh_db):
    song = songbook.build_composed_song(
        title="Mine", artist="Me", tempo=100, pattern_id="island",
        progression=["C", "Am"], lyrics_text="",
    )
    fresh_db.save_composed_song(song)
    # resolvable by id alongside curated songs
    assert songbook.get_song(song["id"])["title"] == "Mine"
    assert songbook.get_song("twinkle")["title"].startswith("Twinkle")  # curated still works
    assert any(s["id"] == song["id"] for s in songbook.all_songs())
    fresh_db.delete_composed_song(song["id"])
    assert songbook.get_song(song["id"]) is None
