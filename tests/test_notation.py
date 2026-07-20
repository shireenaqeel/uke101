import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from koa.data.notation import NOTATION_DRILLS, NOTATION_TRACKS, get_track_drills
from koa.notation import render_notation


def test_tracks_and_drills_present():
    track_ids = {t["id"] for t in NOTATION_TRACKS}
    assert track_ids == {"rhythm", "staff", "tab"}
    for tid in track_ids:
        assert get_track_drills(tid), tid


def test_drill_shape_and_answer_in_choices():
    ids = set()
    for track, drills in NOTATION_DRILLS.items():
        for drill in drills:
            assert {"id", "level", "render", "question", "choices", "answer"} <= set(drill)
            assert drill["answer"] in drill["choices"], drill["id"]
            assert drill["level"] >= 1
            assert drill["render"]["type"] in {"rhythm", "staff", "tab"}
            ids.add(drill["id"])
    assert len(ids) == sum(len(d) for d in NOTATION_DRILLS.values())  # unique ids


def test_every_drill_renders_to_svg():
    for drills in NOTATION_DRILLS.values():
        for drill in drills:
            svg = render_notation(drill["render"])
            assert svg.startswith("<svg")
            assert svg.rstrip().endswith("</svg>")


def test_staff_middle_c_gets_a_ledger_line():
    # middle C (C4) sits below the staff, so it needs a ledger line;
    # a staff note that is on the staff (G4) should have fewer horizontal lines.
    c_lines = render_notation({"type": "staff", "note": "C4"}).count("<line")
    g_lines = render_notation({"type": "staff", "note": "G4"}).count("<line")
    assert c_lines > g_lines


def test_unknown_render_type_raises():
    with pytest.raises(ValueError):
        render_notation({"type": "nope"})
