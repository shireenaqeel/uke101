"""Minimal ChordPro-style parser.

Turns lines like ``[C]Twinkle [F]little [C]star`` into the song data model's
``{"text": ..., "chords": [{"word", "chord"}]}`` shape, so a user can place
chords above words by typing, and the result plays in Song Mode exactly like a
curated song. Pure string logic — no UI — so it is easy to test.
"""


def parse_line(line: str, beats: int = 8) -> dict:
    """Parse one ChordPro line into a lyric line with word-indexed chords."""
    chords = []
    plain = ""
    i = 0
    n = len(line)
    while i < n:
        if line[i] == "[":
            j = line.find("]", i)
            if j == -1:
                plain += line[i]
                i += 1
                continue
            chord = line[i + 1 : j].strip()
            words_so_far = len(plain.split())
            if plain and not plain[-1].isspace():
                word_index = max(words_so_far - 1, 0)  # chord landed mid-word
            else:
                word_index = words_so_far
            if chord:
                chords.append({"word": word_index, "chord": chord})
            i = j + 1
        else:
            plain += line[i]
            i += 1

    text = " ".join(plain.split())
    word_count = len(text.split())
    # Clamp any chord that pointed past the end (e.g. a trailing [chord]).
    for change in chords:
        change["word"] = min(change["word"], max(word_count - 1, 0))
    return {"text": text, "chords": chords, "beats": beats}


def parse_song_lines(text: str, beats: int = 8) -> list[dict]:
    """Parse a multi-line ChordPro block, skipping blank lines."""
    return [parse_line(line, beats) for line in text.splitlines() if line.strip()]


def line_to_chordpro(line: dict) -> str:
    """Render a lyric line back to ChordPro text (used for chart export)."""
    words = line["text"].split(" ")
    chord_at: dict[int, list[str]] = {}
    for change in line.get("chords", []):
        chord_at.setdefault(change["word"], []).append(change["chord"])
    out = []
    for i, word in enumerate(words):
        for chord in chord_at.get(i, []):
            out.append(f"[{chord}]")
        out.append(word + " ")
    return "".join(out).rstrip()
