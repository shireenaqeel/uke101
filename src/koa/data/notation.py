"""Notation drill content — an optional, self-contained skill track.

Three sub-tracks taught in order: rhythm (note/rest durations) → staff (reading
notes on the treble clef) → tab (reading 4-line ukulele tab). Each drill is a
multiple-choice "read this and identify it" question with a rendered prompt.
"""

NOTATION_TRACKS = [
    {
        "id": "rhythm",
        "name": "Rhythm",
        "desc": "Note and rest durations — the beats behind every strum.",
    },
    {
        "id": "staff",
        "name": "Staff",
        "desc": "Reading notes on the treble clef, starting with the open strings.",
    },
    {
        "id": "tab",
        "name": "Tab",
        "desc": "Reading 4-line ukulele tab — one line per string, numbers are frets.",
    },
]

NOTATION_DRILLS = {
    "rhythm": [
        {"id": "r1", "level": 1, "render": {"type": "rhythm", "symbol": "quarter"},
         "question": "How many beats does this note last (in 4/4)?",
         "choices": ["1 beat", "2 beats", "4 beats"], "answer": "1 beat"},
        {"id": "r2", "level": 1, "render": {"type": "rhythm", "symbol": "half"},
         "question": "How many beats does this note last (in 4/4)?",
         "choices": ["1 beat", "2 beats", "4 beats"], "answer": "2 beats"},
        {"id": "r3", "level": 1, "render": {"type": "rhythm", "symbol": "whole"},
         "question": "How many beats does this note last (in 4/4)?",
         "choices": ["2 beats", "3 beats", "4 beats"], "answer": "4 beats"},
        {"id": "r4", "level": 2, "render": {"type": "rhythm", "symbol": "eighth"},
         "question": "Which note is this?",
         "choices": ["Quarter note", "Eighth note", "Half note"], "answer": "Eighth note"},
        {"id": "r5", "level": 2, "render": {"type": "rhythm", "symbol": "quarter_rest"},
         "question": "What is this symbol?",
         "choices": ["Quarter note", "Quarter rest", "Eighth rest"], "answer": "Quarter rest"},
        {"id": "r6", "level": 3, "render": {"type": "rhythm", "symbol": "whole_rest"},
         "question": "What is this symbol?",
         "choices": ["Whole rest", "Half rest", "Whole note"], "answer": "Whole rest"},
    ],
    "staff": [
        {"id": "s1", "level": 1, "render": {"type": "staff", "note": "E4"},
         "question": "Which note is this (bottom line of the treble staff)?",
         "choices": ["C", "E", "G"], "answer": "E"},
        {"id": "s2", "level": 1, "render": {"type": "staff", "note": "G4"},
         "question": "Which open ukulele string is this note?",
         "choices": ["G", "C", "A"], "answer": "G"},
        {"id": "s3", "level": 2, "render": {"type": "staff", "note": "C4"},
         "question": "Which note sits on the ledger line below the staff (middle C)?",
         "choices": ["A", "C", "E"], "answer": "C"},
        {"id": "s4", "level": 2, "render": {"type": "staff", "note": "A4"},
         "question": "Which note is this?",
         "choices": ["G", "A", "B"], "answer": "A"},
        {"id": "s5", "level": 3, "render": {"type": "staff", "note": "C5"},
         "question": "Which note is this (third space)?",
         "choices": ["A", "C", "E"], "answer": "C"},
    ],
    "tab": [
        {"id": "t1", "level": 1, "render": {"type": "tab", "string": "C", "fret": 0},
         "question": "Which string and fret is shown?",
         "choices": ["C string, open", "G string, open", "A string, 3rd fret"],
         "answer": "C string, open"},
        {"id": "t2", "level": 1, "render": {"type": "tab", "string": "A", "fret": 3},
         "question": "Which string and fret is shown?",
         "choices": ["A string, 3rd fret", "C string, 3rd fret", "A string, open"],
         "answer": "A string, 3rd fret"},
        {"id": "t3", "level": 2, "render": {"type": "tab", "string": "E", "fret": 1},
         "question": "Which string and fret is shown?",
         "choices": ["E string, 1st fret", "C string, 1st fret", "E string, open"],
         "answer": "E string, 1st fret"},
        {"id": "t4", "level": 2, "render": {"type": "tab", "string": "G", "fret": 2},
         "question": "Which string and fret is shown?",
         "choices": ["G string, 2nd fret", "A string, 2nd fret", "G string, open"],
         "answer": "G string, 2nd fret"},
    ],
}


def get_track_drills(track: str) -> list[dict]:
    return NOTATION_DRILLS.get(track, [])
