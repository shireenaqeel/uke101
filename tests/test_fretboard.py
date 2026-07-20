import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from koa.data.chords import get_chord
from koa.fretboard import render_fretboard


def test_renders_svg():
    svg = render_fretboard(get_chord("C"))
    assert svg.startswith("<svg")
    assert svg.rstrip().endswith("</svg>")


def test_dot_count_matches_fingered_strings():
    chord = get_chord("G7")  # three fretted strings
    svg = render_fretboard(chord)
    fretted = sum(1 for f in chord["frets"].values() if f and f > 0)
    assert svg.count('fill="#7c5cff"') == fretted


def test_open_string_marker_present():
    # C major has three open strings -> three open-circle markers.
    svg = render_fretboard(get_chord("C"))
    assert svg.count("fill=\"none\"") == 3
