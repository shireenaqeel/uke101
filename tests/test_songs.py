import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from koa.data.chords import CHORDS_BY_ID
from koa.data.patterns import PATTERNS_BY_ID
from koa.data.songs import (
    SONGS,
    cumulative_times,
    get_song,
    primary_line_chords,
)

_CHORD_IDS = set(CHORDS_BY_ID)


def test_at_least_four_songs():
    assert len(SONGS) >= 4


def test_song_shapes_and_references():
    ids = set()
    for song in SONGS:
        assert {"id", "title", "artist", "difficulty", "tempo", "chords_used",
                "strumming_pattern_id", "lyrics_included", "is_user_composed"} <= set(song)
        assert song["strumming_pattern_id"] in PATTERNS_BY_ID
        for chord in song["chords_used"]:
            assert chord in _CHORD_IDS, (song["id"], chord)
        ids.add(song["id"])
    assert len(ids) == len(SONGS)


def test_lyric_chord_references_are_valid():
    for song in SONGS:
        for line in song["lines"]:
            words = line["text"].split(" ")
            for change in line.get("chords", []):
                assert change["chord"] in _CHORD_IDS
                assert 0 <= change["word"] < len(words), (song["id"], change)


def test_chart_only_songs_link_out_without_lyrics():
    for song in SONGS:
        if not song["lyrics_included"]:
            assert song["source_url"]
            assert song["progression"]
            assert song["lines"] == []


def test_primary_line_chords_carries_previous():
    song = get_song("saints")
    chords = primary_line_chords(song)
    assert len(chords) == len(song["lines"])
    # second line has no chord change, so it carries the first line's chord
    assert chords[1] == chords[0]


def test_cumulative_times():
    starts, total = cumulative_times([8, 8, 8], bpm=120)
    # 120 bpm -> 0.5s per beat -> 4s per 8-beat line
    assert starts == [0.0, 4.0, 8.0]
    assert total == 12.0
