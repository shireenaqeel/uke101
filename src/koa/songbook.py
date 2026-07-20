"""Composition layer that merges curated and user-composed songs.

Keeps ``koa.data.songs`` a pure content module while giving the UI one place to
resolve any song id (curated or composed) and to build/export composed songs.
"""

from uuid import uuid4

from koa import chordpro, db
from koa.data.chords import CHORDS_BY_ID
from koa.data.songs import SONGS as CURATED
from koa.data.songs import SONGS_BY_ID as CURATED_BY_ID

_DIFF_ORDER = {"easy": 0, "medium": 1, "hard": 2}
_ORDER_DIFF = {0: "easy", 1: "medium", 2: "hard"}


def all_songs() -> list[dict]:
    return list(CURATED) + db.get_composed_songs()


def get_song(song_id: str) -> dict | None:
    if song_id in CURATED_BY_ID:
        return CURATED_BY_ID[song_id]
    return db.get_composed_song(song_id)


def hardest_difficulty(chord_ids: list[str]) -> str:
    known = [_DIFF_ORDER[CHORDS_BY_ID[c]["difficulty"]] for c in chord_ids if c in CHORDS_BY_ID]
    return _ORDER_DIFF[max(known)] if known else "easy"


def _unique(seq: list[str]) -> list[str]:
    seen: dict[str, None] = {}
    for item in seq:
        seen.setdefault(item, None)
    return list(seen)


def new_song_id() -> str:
    return "user-" + uuid4().hex[:8]


def build_composed_song(
    title: str,
    artist: str,
    tempo: int,
    pattern_id: str,
    progression: list[str],
    lyrics_text: str = "",
    song_id: str | None = None,
) -> dict:
    """Assemble a composed song dict in the same shape as curated songs."""
    if lyrics_text.strip():
        lines = chordpro.parse_song_lines(lyrics_text)
        chords_used = _unique([c["chord"] for line in lines for c in line["chords"]])
        lyrics_included = True
        prog: list[str] = []
    else:
        lines = []
        chords_used = _unique(progression)
        lyrics_included = False
        prog = list(progression)

    return {
        "id": song_id or new_song_id(),
        "title": title.strip() or "Untitled",
        "artist": artist.strip() or "Me",
        "difficulty": hardest_difficulty(chords_used),
        "tempo": tempo,
        "chords_used": chords_used,
        "strumming_pattern_id": pattern_id,
        "lyrics_included": lyrics_included,
        "is_user_composed": True,
        "source_url": None,
        "progression": prog,
        "lines": lines,
    }


def chord_chart_text(song: dict) -> str:
    """A plain-text chord chart, for export/printing."""
    out = [song["title"], f"by {song['artist']}", ""]
    out.append("Chords: " + " ".join(song["chords_used"]))
    out.append(f"Tempo: {song['tempo']} bpm")
    out.append("")
    if song["lyrics_included"]:
        for line in song["lines"]:
            out.append(chordpro.line_to_chordpro(line))
    else:
        out.append("Progression: " + " | ".join(song.get("progression", [])))
    return "\n".join(out) + "\n"
