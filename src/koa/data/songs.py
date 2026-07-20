"""Song content layer.

Two kinds of song share one model:

* ``lyrics_included`` songs are public-domain / traditional, so full lyrics are
  stored with chord changes placed by word index (``chords: [{word, chord}]``).
* Copyrighted starters store only the chord progression plus a ``source_url``
  to link out to lyrics — no verbatim lyrics embedded.

A user-composed song (Phase 6) will reuse this exact structure with
``is_user_composed = True``.
"""

from koa.metronome import interval_seconds

SONGS = [
    {
        "id": "twinkle",
        "title": "Twinkle, Twinkle, Little Star",
        "artist": "Traditional",
        "difficulty": "easy",
        "tempo": 90,
        "chords_used": ["C", "F", "G7"],
        "strumming_pattern_id": "basic_down",
        "lyrics_included": True,
        "is_user_composed": False,
        "source_url": None,
        "lines": [
            {"text": "Twinkle, twinkle, little star", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}, {"word": 2, "chord": "F"}, {"word": 3, "chord": "C"}]},
            {"text": "How I wonder what you are", "beats": 8,
             "chords": [{"word": 0, "chord": "F"}, {"word": 1, "chord": "C"}, {"word": 3, "chord": "G7"}, {"word": 5, "chord": "C"}]},
            {"text": "Up above the world so high", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}, {"word": 2, "chord": "F"}, {"word": 4, "chord": "C"}]},
            {"text": "Like a diamond in the sky", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}, {"word": 2, "chord": "G7"}, {"word": 5, "chord": "C"}]},
            {"text": "Twinkle, twinkle, little star", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}, {"word": 2, "chord": "F"}, {"word": 3, "chord": "C"}]},
            {"text": "How I wonder what you are", "beats": 8,
             "chords": [{"word": 0, "chord": "F"}, {"word": 1, "chord": "C"}, {"word": 3, "chord": "G7"}, {"word": 5, "chord": "C"}]},
        ],
    },
    {
        "id": "amazing_grace",
        "title": "Amazing Grace",
        "artist": "Traditional",
        "difficulty": "easy",
        "tempo": 84,
        "chords_used": ["C", "F", "G7"],
        "strumming_pattern_id": "waltz",
        "lyrics_included": True,
        "is_user_composed": False,
        "source_url": None,
        "lines": [
            {"text": "Amazing grace how sweet the sound", "beats": 6,
             "chords": [{"word": 0, "chord": "C"}, {"word": 3, "chord": "F"}, {"word": 5, "chord": "C"}]},
            {"text": "That saved a wretch like me", "beats": 6,
             "chords": [{"word": 0, "chord": "C"}, {"word": 5, "chord": "G7"}]},
            {"text": "I once was lost but now am found", "beats": 6,
             "chords": [{"word": 0, "chord": "C"}, {"word": 5, "chord": "F"}, {"word": 7, "chord": "C"}]},
            {"text": "Was blind but now I see", "beats": 6,
             "chords": [{"word": 0, "chord": "C"}, {"word": 3, "chord": "G7"}, {"word": 5, "chord": "C"}]},
        ],
    },
    {
        "id": "saints",
        "title": "When the Saints Go Marching In",
        "artist": "Traditional",
        "difficulty": "easy",
        "tempo": 100,
        "chords_used": ["C", "F", "G7"],
        "strumming_pattern_id": "basic_down",
        "lyrics_included": True,
        "is_user_composed": False,
        "source_url": None,
        "lines": [
            {"text": "Oh when the saints go marching in", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}, {"word": 6, "chord": "G7"}]},
            {"text": "Oh when the saints go marching in", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}]},
            {"text": "Oh how I want to be in that number", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}, {"word": 5, "chord": "F"}, {"word": 8, "chord": "C"}]},
            {"text": "When the saints go marching in", "beats": 8,
             "chords": [{"word": 0, "chord": "G7"}, {"word": 5, "chord": "C"}]},
        ],
    },
    {
        "id": "oh_susanna",
        "title": "Oh! Susanna",
        "artist": "Stephen Foster",
        "difficulty": "medium",
        "tempo": 108,
        "chords_used": ["C", "F", "G7"],
        "strumming_pattern_id": "island",
        "lyrics_included": True,
        "is_user_composed": False,
        "source_url": None,
        "lines": [
            {"text": "I come from Alabama with my banjo on my knee", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}, {"word": 6, "chord": "G7"}, {"word": 9, "chord": "C"}]},
            {"text": "I'm going to Louisiana my true love for to see", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}, {"word": 8, "chord": "G7"}, {"word": 9, "chord": "C"}]},
            {"text": "Oh Susanna oh don't you cry for me", "beats": 8,
             "chords": [{"word": 0, "chord": "F"}, {"word": 2, "chord": "C"}, {"word": 5, "chord": "G7"}, {"word": 7, "chord": "C"}]},
            {"text": "For I come from Alabama with my banjo on my knee", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}, {"word": 9, "chord": "G7"}, {"word": 10, "chord": "C"}]},
        ],
    },
    {
        "id": "this_little_light",
        "title": "This Little Light of Mine",
        "artist": "Traditional",
        "difficulty": "easy",
        "tempo": 96,
        "chords_used": ["C", "F", "G7"],
        "strumming_pattern_id": "island",
        "lyrics_included": True,
        "is_user_composed": False,
        "source_url": None,
        "lines": [
            {"text": "This little light of mine I'm gonna let it shine", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}]},
            {"text": "This little light of mine I'm gonna let it shine", "beats": 8,
             "chords": [{"word": 0, "chord": "F"}, {"word": 4, "chord": "C"}]},
            {"text": "This little light of mine I'm gonna let it shine", "beats": 8,
             "chords": [{"word": 0, "chord": "G7"}, {"word": 4, "chord": "C"}]},
            {"text": "Let it shine let it shine let it shine", "beats": 8,
             "chords": [{"word": 0, "chord": "C"}, {"word": 3, "chord": "G7"}, {"word": 6, "chord": "C"}]},
        ],
    },
    {
        "id": "riptide",
        "title": "Riptide",
        "artist": "Vance Joy",
        "difficulty": "easy",
        "tempo": 102,
        "chords_used": ["Am", "G", "C"],
        "strumming_pattern_id": "island",
        "lyrics_included": False,
        "is_user_composed": False,
        "source_url": "https://www.ultimate-guitar.com/search.php?search_type=title&value=Riptide%20Vance%20Joy",
        "progression": ["Am", "G", "C"],
        "lines": [],
    },
    {
        "id": "im_yours",
        "title": "I'm Yours",
        "artist": "Jason Mraz",
        "difficulty": "easy",
        "tempo": 76,
        "chords_used": ["C", "G", "Am", "F"],
        "strumming_pattern_id": "island",
        "lyrics_included": False,
        "is_user_composed": False,
        "source_url": "https://www.ultimate-guitar.com/search.php?search_type=title&value=I%27m%20Yours%20Jason%20Mraz",
        "progression": ["C", "G", "Am", "F"],
        "lines": [],
    },
]


def _chart_song(song_id, title, artist, difficulty, tempo, progression, pattern="island"):
    query = f"{title} {artist}".replace(" ", "%20")
    return {
        "id": song_id,
        "title": title,
        "artist": artist,
        "difficulty": difficulty,
        "tempo": tempo,
        "chords_used": list(dict.fromkeys(progression)),
        "strumming_pattern_id": pattern,
        "lyrics_included": False,
        "is_user_composed": False,
        "source_url": f"https://www.ultimate-guitar.com/search.php?search_type=title&value={query}",
        "progression": progression,
        "lines": [],
    }


# Bollywood & pop hits as chord charts (lyrics are copyrighted — link out instead).
SONGS += [
    _chart_song("kal_ho_naa_ho", "Kal Ho Naa Ho", "Sonu Nigam", "medium", 90, ["C", "Em", "F", "G"]),
    _chart_song("pehla_nasha", "Pehla Nasha", "Udit Narayan", "easy", 92, ["C", "Am", "F", "G"]),
    _chart_song("sunshine", "Give Me Some Sunshine", "3 Idiots", "easy", 96, ["C", "G", "Am", "F"]),
    _chart_song("ilahi", "Ilahi", "Arijit Singh", "medium", 108, ["G", "D", "Em", "C"]),
    _chart_song("tum_hi_ho", "Tum Hi Ho", "Arijit Singh", "easy", 84, ["Am", "F", "C", "G"]),
    _chart_song("perfect", "Perfect", "Ed Sheeran", "medium", 95, ["G", "Em", "C", "D"]),
    _chart_song("let_it_be", "Let It Be", "The Beatles", "easy", 72, ["C", "G", "Am", "F"]),
]

SONGS_BY_ID = {s["id"]: s for s in SONGS}


def get_song(song_id: str) -> dict | None:
    return SONGS_BY_ID.get(song_id)


def primary_line_chords(song: dict) -> list[str | None]:
    """The chord to display for each lyric line: the line's first chord change,
    or the previous line's carried-over chord if the line starts mid-chord."""
    result = []
    current = None
    for line in song["lines"]:
        changes = line.get("chords", [])
        if changes:
            current = changes[0]["chord"]
        result.append(current)
    return result


def cumulative_times(beats: list[int], bpm: float) -> tuple[list[float], float]:
    """Start time (seconds) of each step and the total duration, at a tempo."""
    beat = interval_seconds(bpm)
    starts = []
    t = 0.0
    for b in beats:
        starts.append(t)
        t += b * beat
    return starts, t
