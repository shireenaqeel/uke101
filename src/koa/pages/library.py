from nicegui import app, ui
from starlette.responses import Response

from koa import db
from koa.audio import synth
from koa.pages import fx
from koa.data.chords import CHORDS, fingering_text, get_chord
from koa.fretboard import render_fretboard
from koa.pages.common import page_header

_DIFFICULTY_COLORS = {"easy": "green", "medium": "amber", "hard": "red"}
_audio_cache: dict[str, bytes] = {}


@app.get("/audio/chord/{chord_id}")
def chord_audio(chord_id: str):
    if chord_id not in _audio_cache:
        chord = get_chord(chord_id)
        if chord is None:
            return Response(status_code=404)
        _audio_cache[chord_id] = synth.chord_wav(chord["frets"])
    return Response(content=_audio_cache[chord_id], media_type="audio/wav")


def chord_card(chord: dict, learned: set[str], on_change) -> None:
    with ui.card().classes("w-64 items-center gap-2"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(chord["name"]).classes("text-2xl font-bold")
            ui.badge(chord["difficulty"], color=_DIFFICULTY_COLORS[chord["difficulty"]])
        ui.label(chord["full_name"]).classes("text-sm text-gray-500 -mt-2")

        ui.html(render_fretboard(chord))

        with ui.column().classes("gap-0 items-center"):
            for line in fingering_text(chord):
                ui.label(line).classes("text-xs text-gray-500")

        audio = ui.audio(f"/audio/chord/{chord['id']}").props("preload=none").classes("hidden")
        with ui.row().classes("w-full items-center justify-between"):
            ui.button(icon="play_arrow", on_click=audio.play).props("round flat").tooltip("Hear it")
            ui.switch(
                "Learned",
                value=chord["id"] in learned,
                on_change=lambda e, cid=chord["id"]: on_change(cid, e.value),
            )


def build_library() -> None:
    page_header("/library")
    learned = db.get_learned()

    with ui.column().classes("w-full max-w-6xl mx-auto items-center gap-4 p-6"):
        ui.label("Chord Library").classes("text-3xl font-bold")
        ui.label("Browse every chord, hear it, and mark the ones you've learned.").classes(
            "text-gray-500"
        )
        counter = ui.label().classes("text-sm text-gray-400")

        def refresh_counter() -> None:
            counter.text = f"{len(db.get_learned())}/{len(CHORDS)} chords learned"

        def on_change(chord_id: str, value: bool) -> None:
            if value:
                newly = chord_id not in db.get_learned()
                db.mark_learned(chord_id)
                if newly:
                    fx.award("chord_learned")
            else:
                db.unmark_learned(chord_id)
            refresh_counter()

        refresh_counter()

        with ui.row().classes("w-full justify-center gap-4 flex-wrap"):
            for chord in CHORDS:
                chord_card(chord, learned, on_change)
