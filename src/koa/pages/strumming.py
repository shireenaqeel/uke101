from nicegui import app, ui
from starlette.responses import Response

from koa.audio import synth
from koa.data.chords import CHORDS, get_chord
from koa.data.patterns import STRUMMING_PATTERNS, beat_labels, get_pattern
from koa.metronome import interval_seconds
from koa.pages.common import page_header

_CHORD_IDS = [c["id"] for c in CHORDS]
_ARROWS = {"D": "↓", "U": "↑", "rest": "·"}
_strum_cache: dict[tuple[str, str], bytes] = {}


@app.get("/audio/strum/{direction}")
def strum_audio(direction: str, chord: str = "C"):
    chord_obj = get_chord(chord)
    if chord_obj is None or direction not in ("D", "U"):
        return Response(status_code=404)
    key = (direction, chord)
    if key not in _strum_cache:
        _strum_cache[key] = synth.strum_wav(chord_obj["frets"], direction)
    return Response(content=_strum_cache[key], media_type="audio/wav")


def build_strumming() -> None:
    page_header("/strumming")

    state = {
        "pattern": STRUMMING_PATTERNS[0],
        "chord": "C",
        "playing": False,
        "index": 0,
        "timer": None,
        "slot_boxes": [],
        "down": None,
        "up": None,
    }

    audio_holder = ui.element("div").classes("hidden")

    with ui.column().classes("w-full max-w-4xl mx-auto items-center gap-4 p-6"):
        ui.label("Strumming Pattern Trainer").classes("text-3xl font-bold")
        ui.label(
            "Pick a pattern and a chord, set the tempo, and play along with the highlighted beat."
        ).classes("text-gray-500 text-center max-w-2xl")

        with ui.row().classes("items-center gap-4 flex-wrap justify-center"):
            pattern_select = ui.select(
                {p["id"]: p["name"] for p in STRUMMING_PATTERNS},
                value=state["pattern"]["id"],
                label="Pattern",
            ).props("dense").classes("w-48")
            chord_select = ui.select(_CHORD_IDS, value="C", label="Chord").props(
                "dense"
            ).classes("w-32")

        songs_label = ui.label("").classes("text-xs text-gray-400")

        # Pattern grid (arrows + beat counts), rebuilt when the pattern changes.
        grid = ui.row().classes("items-end justify-center gap-1 flex-wrap")

        with ui.row().classes("items-center gap-4"):
            play_btn = ui.button("Play", on_click=lambda: toggle()).props("size=lg")
        with ui.row().classes("items-center gap-4"):
            ui.label("Tempo")
            bpm_slider = ui.slider(min=40, max=160, value=80).props("label-always").classes("w-48")

    # --- behaviour -----------------------------------------------------------
    def set_audio_sources() -> None:
        audio_holder.clear()
        with audio_holder:
            state["down"] = ui.audio(f"/audio/strum/D?chord={state['chord']}").props("preload=auto")
            state["up"] = ui.audio(f"/audio/strum/U?chord={state['chord']}").props("preload=auto")

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
        songs_label.text = f"Often used in: {pattern['songs']}"
        highlight(-1)

    def highlight(active: int) -> None:
        for i, box in enumerate(state["slot_boxes"]):
            if i == active:
                box.classes(add="bg-primary text-white scale-110")
            else:
                box.classes(remove="bg-primary text-white scale-110")

    def tick() -> None:
        i = state["index"]
        slot = state["pattern"]["slots"][i]
        highlight(i)
        if slot == "D" and state["down"]:
            state["down"].seek(0)
            state["down"].play()
        elif slot == "U" and state["up"]:
            state["up"].seek(0)
            state["up"].play()
        state["index"] = (i + 1) % len(state["pattern"]["slots"])

    def start() -> None:
        state["playing"] = True
        state["index"] = 0
        play_btn.set_text("Stop")
        play_btn.props("color=red")
        eighth = interval_seconds(bpm_slider.value) / 2
        state["timer"] = ui.timer(eighth, tick)

    def stop() -> None:
        state["playing"] = False
        if state["timer"] is not None:
            state["timer"].cancel()
            state["timer"] = None
        play_btn.set_text("Play")
        play_btn.props("color=primary")
        highlight(-1)

    def toggle() -> None:
        stop() if state["playing"] else start()

    def on_pattern_change(e) -> None:
        stop()
        state["pattern"] = get_pattern(e.value)
        rebuild_grid()

    def on_chord_change(e) -> None:
        state["chord"] = e.value
        set_audio_sources()

    pattern_select.on_value_change(on_pattern_change)
    chord_select.on_value_change(on_chord_change)

    set_audio_sources()
    rebuild_grid()
