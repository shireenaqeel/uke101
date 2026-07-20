import time

from nicegui import ui

from koa import db
from koa.arcade import ArcadeEngine, note_times
from koa.data.chords import CHORDS
from koa.data.patterns import STRUMMING_PATTERNS, beat_labels, get_pattern
from koa.metronome import interval_seconds
from koa.pages.common import page_header

_CHORD_IDS = [c["id"] for c in CHORDS]
_ARROWS = {"D": "↓", "U": "↑", "rest": "·"}
_GRADE_COLORS = {"perfect": "#16a34a", "good": "#d97706", "miss": "#dc2626"}


def build_arcade() -> None:
    page_header("/arcade")

    state = {
        "pattern": STRUMMING_PATTERNS[2],  # Island strum — a fun default
        "loops": 4,
        "running": False,
        "engine": None,
        "start": 0.0,
        "end": 0.0,
        "eighth": 0.0,
        "quarter": 0.0,
        "n": 0,
        "last_beat": -1,
        "timer": None,
        "countdown": 0,
        "countdown_timer": None,
        "slot_boxes": [],
    }

    click_audio = ui.audio("/audio/metronome").props("preload=auto").classes("hidden")

    with ui.column().classes("w-full max-w-4xl mx-auto items-center gap-4 p-6"):
        ui.label("Strum Arcade").classes("text-3xl font-bold")
        ui.label(
            "Tap in time with each stroke — press Space or the Strum button. "
            "Nail the timing for Perfect hits, keep the combo alive."
        ).classes("text-gray-500 text-center max-w-2xl")

        with ui.row().classes("items-center gap-4 flex-wrap justify-center"):
            pattern_select = ui.select(
                {p["id"]: p["name"] for p in STRUMMING_PATTERNS},
                value=state["pattern"]["id"],
                label="Pattern",
            ).props("dense").classes("w-48")
            length_select = ui.select(
                {2: "2 bars", 4: "4 bars", 8: "8 bars"}, value=4, label="Length"
            ).props("dense").classes("w-28")
            metronome_switch = ui.switch("Metronome", value=True)

        with ui.row().classes("items-center gap-6"):
            ui.label("Tempo")
            bpm_slider = ui.slider(min=40, max=140, value=80).props("label-always").classes("w-48")

        # scoreboard
        with ui.row().classes("items-center gap-10"):
            with ui.column().classes("items-center gap-0"):
                score_label = ui.label("0").classes("text-5xl font-bold text-primary")
                ui.label("score").classes("text-xs text-gray-400")
            with ui.column().classes("items-center gap-0"):
                combo_label = ui.label("0").classes("text-5xl font-bold")
                ui.label("combo").classes("text-xs text-gray-400")

        judgment = ui.label("").classes("text-2xl font-bold h-8")

        # beat grid (one measure) with the playhead
        grid = ui.row().classes("items-end justify-center gap-1 flex-wrap")

        with ui.row().classes("items-center gap-4"):
            start_btn = ui.button("Play", on_click=lambda: arm()).props("size=lg")
            ui.button("Strum", on_click=lambda: on_tap()).props("size=lg color=secondary")

        result = ui.column().classes("items-center gap-1")
        best_label = ui.label("").classes("text-sm text-gray-500")

    # --- helpers -------------------------------------------------------------
    def rebuild_grid() -> None:
        pattern = state["pattern"]
        labels = beat_labels(pattern)
        grid.clear()
        state["slot_boxes"] = []
        with grid:
            for i, slot in enumerate(pattern["slots"]):
                with ui.column().classes("items-center gap-1"):
                    box = ui.label(_ARROWS[slot]).classes(
                        "text-3xl w-10 h-12 flex items-center justify-center rounded transition-all "
                        + ("text-gray-300" if slot == "rest" else "text-gray-700")
                    )
                    ui.label(labels[i]).classes("text-xs text-gray-400")
                state["slot_boxes"].append(box)
        highlight(-1)

    def highlight(active: int) -> None:
        for i, box in enumerate(state["slot_boxes"]):
            if i == active:
                box.classes(add="bg-primary text-white scale-110")
            else:
                box.classes(remove="bg-primary text-white scale-110")

    def flash(grade: str) -> None:
        judgment.text = grade.upper()
        judgment.style(f"color: {_GRADE_COLORS[grade]}")

    def refresh_best() -> None:
        best = db.get_arcade_best(state["pattern"]["id"])
        best_label.text = f"Best score on {state['pattern']['name']}: {best}" if best else "No score yet"

    def update_scoreboard() -> None:
        eng = state["engine"]
        score_label.text = str(eng.score)
        combo_label.text = str(eng.combo)

    # --- game loop -----------------------------------------------------------
    def arm() -> None:
        if state["running"] or state["countdown_timer"]:
            return
        result.clear()
        judgment.text = ""
        state["countdown"] = 3
        judgment.text = "3"
        judgment.style("color: #6b7280")
        state["countdown_timer"] = ui.timer(0.7, countdown_tick)

    def countdown_tick() -> None:
        state["countdown"] -= 1
        if state["countdown"] > 0:
            judgment.text = str(state["countdown"])
        elif state["countdown"] == 0:
            judgment.text = "GO"
        else:
            state["countdown_timer"].cancel()
            state["countdown_timer"] = None
            judgment.text = ""
            start_game()

    def start_game() -> None:
        pattern = state["pattern"]
        bpm = bpm_slider.value
        loops = length_select.value
        state["engine"] = ArcadeEngine(note_times(pattern, bpm, loops))
        state["eighth"] = interval_seconds(bpm) / 2
        state["quarter"] = interval_seconds(bpm)
        state["n"] = len(pattern["slots"])
        state["end"] = loops * state["n"] * state["eighth"] + 0.4
        state["last_beat"] = -1
        state["running"] = True
        state["start"] = time.time()
        start_btn.set_text("Playing…")
        start_btn.props("color=grey")
        update_scoreboard()
        state["timer"] = ui.timer(0.03, tick)

    def tick() -> None:
        eng = state["engine"]
        now = time.time() - state["start"]
        if eng.expire(now):
            flash("miss")
            update_scoreboard()
        highlight(int(now / state["eighth"]) % state["n"])
        if metronome_switch.value:
            beat = int(now / state["quarter"])
            if beat != state["last_beat"]:
                state["last_beat"] = beat
                click_audio.seek(0)
                click_audio.play()
        if eng.is_finished(now) or now >= state["end"]:
            finish()

    def on_tap() -> None:
        if not state["running"]:
            return
        now = time.time() - state["start"]
        flash(state["engine"].tap(now))
        update_scoreboard()

    def finish() -> None:
        if not state["running"]:
            return
        state["running"] = False
        if state["timer"]:
            state["timer"].cancel()
            state["timer"] = None
        highlight(-1)
        eng = state["engine"]
        db.record_arcade_score(state["pattern"]["id"], eng.score, eng.max_combo)
        start_btn.set_text("Play again")
        start_btn.props("color=primary")
        judgment.text = ""
        result.clear()
        with result:
            ui.label(f"Final score: {eng.score}").classes("text-2xl font-bold")
            ui.label(
                f"Perfect {eng.counts['perfect']}  ·  Good {eng.counts['good']}  ·  "
                f"Miss {eng.counts['miss']}  ·  Max combo {eng.max_combo}"
            ).classes("text-gray-600")
            ui.label(f"Accuracy: {eng.accuracy() * 100:0.0f}%").classes("text-gray-600")
        refresh_best()

    def on_pattern_change(e) -> None:
        if state["running"] or state["countdown_timer"]:
            return
        state["pattern"] = get_pattern(e.value)
        rebuild_grid()
        refresh_best()
        result.clear()

    pattern_select.on_value_change(on_pattern_change)
    ui.keyboard(lambda e: on_tap() if e.action.keydown and not e.action.repeat and e.key == " " else None)

    rebuild_grid()
    refresh_best()
