import time

from nicegui import app, ui
from starlette.responses import Response

from koa import db
from koa.audio import synth
from koa.data.chords import CHORDS, get_chord
from koa.data.drills import DRILLS, drill_key
from koa.fretboard import render_fretboard
from koa.metronome import interval_seconds, switches_per_minute
from koa.pages.common import page_header

_CHORD_IDS = [c["id"] for c in CHORDS]
_metronome_cache: dict[bool, bytes] = {}


@app.get("/audio/metronome")
def metronome_audio():
    if False not in _metronome_cache:
        _metronome_cache[False] = synth.metronome_wav(accent=False)
    return Response(content=_metronome_cache[False], media_type="audio/wav")


def build_switching() -> None:
    page_header("/switching")

    state = {
        "chords": list(DRILLS[0]["chords"]),
        "index": 0,
        "count": 0,
        "running": False,
        "start": 0.0,
        "duration": 60,
        "pulse": False,
        "countdown": None,
        "metro": None,
        "cards": [],
    }

    click_audio = ui.audio("/audio/metronome").props("preload=auto").classes("hidden")

    with ui.column().classes("w-full max-w-4xl mx-auto items-center gap-4 p-6"):
        ui.label("Chord Switching Trainer").classes("text-3xl font-bold")
        ui.label(
            "Pick two chords, then change between them as many times as you can in the time "
            "limit. Tap Switched (or press Space) after every clean change."
        ).classes("text-gray-500 text-center max-w-2xl")

        # --- drill selection -------------------------------------------------
        with ui.card().classes("w-full items-stretch gap-3"):
            for group in ["Beginner pairs", "Three-chord loops", "Four-chord loops"]:
                with ui.row().classes("items-center gap-2 flex-wrap"):
                    ui.label(group).classes("text-xs text-gray-400 w-32")
                    for drill in DRILLS:
                        if drill["group"] == group:
                            ui.button(
                                drill["label"],
                                on_click=lambda d=drill: set_drill(list(d["chords"])),
                            ).props("outline size=sm")
            with ui.row().classes("items-center gap-2"):
                ui.label("Custom pair").classes("text-xs text-gray-400 w-32")
                sel_a = ui.select(_CHORD_IDS, value="C").props("dense")
                sel_b = ui.select(_CHORD_IDS, value="Am").props("dense")
                ui.button(
                    "Use pair", on_click=lambda: set_drill([sel_a.value, sel_b.value])
                ).props("outline size=sm")

        # --- diagrams --------------------------------------------------------
        title = ui.label().classes("text-xl font-semibold")
        diagram_row = ui.row().classes("items-center justify-center gap-6 flex-wrap")

        # --- live readout ----------------------------------------------------
        with ui.row().classes("items-center gap-8"):
            with ui.column().classes("items-center gap-0"):
                counter = ui.label("0").classes("text-5xl font-bold text-primary")
                ui.label("switches").classes("text-xs text-gray-400")
            with ui.column().classes("items-center gap-0"):
                time_label = ui.label("60s").classes("text-5xl font-bold")
                ui.label("remaining").classes("text-xs text-gray-400")
            beat_dot = ui.element("div").classes(
                "w-6 h-6 rounded-full bg-gray-300 transition-all"
            )

        # --- controls --------------------------------------------------------
        with ui.row().classes("items-center gap-4"):
            start_btn = ui.button("Start", on_click=lambda: toggle()).props("size=lg")
            switch_btn = ui.button("Switched", on_click=lambda: on_switch()).props(
                "size=lg color=secondary"
            )
        with ui.row().classes("items-center gap-6"):
            ui.label("Tempo")
            bpm_slider = ui.slider(min=40, max=160, value=70).props("label-always").classes("w-48")
            metronome_switch = ui.switch("Metronome", value=True)
            duration_select = ui.select(
                {30: "30 sec", 60: "60 sec"}, value=60, label="Length"
            ).props("dense").classes("w-28")

        result = ui.label("").classes("text-lg")
        best_label = ui.label("").classes("text-sm text-gray-500")

    # --- behaviour -----------------------------------------------------------
    def rebuild_diagrams() -> None:
        diagram_row.clear()
        state["cards"] = []
        with diagram_row:
            for chord_id in state["chords"]:
                chord = get_chord(chord_id)
                with ui.card().classes("items-center transition-all") as card:
                    ui.label(chord["name"]).classes("text-lg font-bold")
                    ui.html(render_fretboard(chord))
                state["cards"].append(card)
        update_highlight()

    def update_highlight() -> None:
        for i, card in enumerate(state["cards"]):
            if i == state["index"] and state["running"]:
                card.classes(add="ring-4 ring-primary", remove="opacity-40")
            elif i == state["index"]:
                card.classes(add="ring-2 ring-primary", remove="opacity-40")
            else:
                card.classes(add="opacity-40", remove="ring-4 ring-2 ring-primary")

    def refresh_best() -> None:
        best = db.get_switch_best(drill_key(state["chords"]))
        best_label.text = f"Best for this drill: {best} switches" if best else "No score yet"

    def set_drill(chords: list[str]) -> None:
        if state["running"]:
            finish()
        state["chords"] = chords
        state["index"] = 0
        title.text = "  →  ".join(chords)
        rebuild_diagrams()
        refresh_best()
        result.text = ""

    def stop_timers() -> None:
        for key in ("countdown", "metro"):
            timer = state.get(key)
            if timer is not None:
                timer.cancel()
                state[key] = None

    def tick_time() -> None:
        remaining = max(0.0, state["duration"] - (time.time() - state["start"]))
        time_label.text = f"{remaining:0.0f}s"
        if remaining <= 0:
            finish()

    def tick_metronome() -> None:
        click_audio.seek(0)
        click_audio.play()
        state["pulse"] = not state["pulse"]
        if state["pulse"]:
            beat_dot.classes(add="bg-primary scale-125", remove="bg-gray-300")
        else:
            beat_dot.classes(add="bg-gray-300", remove="bg-primary scale-125")

    def start() -> None:
        state.update(running=True, count=0, index=0, start=time.time())
        counter.text = "0"
        result.text = ""
        update_highlight()
        start_btn.set_text("Stop")
        start_btn.props("color=red")
        state["countdown"] = ui.timer(0.1, tick_time)
        if metronome_switch.value:
            state["metro"] = ui.timer(interval_seconds(bpm_slider.value), tick_metronome)

    def finish() -> None:
        if not state["running"]:
            return
        state["running"] = False
        stop_timers()
        elapsed = min(time.time() - state["start"], state["duration"])
        count = state["count"]
        db.record_switch_score(drill_key(state["chords"]), count, elapsed)
        spm = switches_per_minute(count, elapsed)
        result.text = f"{count} clean switches in {elapsed:0.0f}s  (≈ {spm:0.0f} / min)"
        start_btn.set_text("Start")
        start_btn.props("color=primary")
        beat_dot.classes(add="bg-gray-300", remove="bg-primary scale-125")
        time_label.text = f"{state['duration']}s"
        update_highlight()
        refresh_best()

    def toggle() -> None:
        finish() if state["running"] else start()

    def on_switch() -> None:
        if not state["running"]:
            return
        state["count"] += 1
        state["index"] = (state["index"] + 1) % len(state["chords"])
        counter.text = str(state["count"])
        update_highlight()

    def on_key(e) -> None:
        if e.action.keydown and not e.action.repeat and e.key == " ":
            on_switch()

    ui.keyboard(on_key)
    duration_select.on_value_change(lambda e: state.update(duration=e.value))
    set_drill(state["chords"])
