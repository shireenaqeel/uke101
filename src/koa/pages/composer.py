import time

from nicegui import ui

from koa import db, gamification, songbook
from koa.data.chords import CHORDS
from koa.data.patterns import STRUMMING_PATTERNS
from koa.metronome import interval_seconds
from koa.pages.common import page_header

_CHORD_IDS = [c["id"] for c in CHORDS]


def build_composer() -> None:
    page_header("/composer")

    state = {"progression": [], "preview_timer": None, "preview_idx": 0, "chips": []}
    preview_audio = ui.audio("").props("preload=auto").classes("hidden")

    with ui.column().classes("w-full max-w-4xl mx-auto items-stretch gap-4 p-6"):
        ui.label("Song Composer").classes("text-3xl font-bold self-center")
        ui.label(
            "Build a chord progression, add optional lyrics, then save it — it plays back in "
            "Song Mode just like the built-in songs."
        ).classes("text-gray-500 self-center text-center max-w-2xl")

        with ui.row().classes("gap-4 flex-wrap"):
            title_input = ui.input("Title", value="My Song").props("dense").classes("w-56")
            artist_input = ui.input("Artist", value="Me").props("dense").classes("w-40")

        with ui.row().classes("gap-4 flex-wrap items-center"):
            pattern_select = ui.select(
                {p["id"]: p["name"] for p in STRUMMING_PATTERNS},
                value=STRUMMING_PATTERNS[0]["id"],
                label="Strumming pattern",
            ).props("dense").classes("w-52")
            with ui.column().classes("gap-0"):
                ui.label("Tempo").classes("text-xs text-gray-400")
                bpm_slider = ui.slider(min=50, max=160, value=90).props("label-always").classes(
                    "w-48"
                )

        # --- progression builder --------------------------------------------
        with ui.card().classes("w-full gap-3"):
            ui.label("Chord progression").classes("text-lg font-semibold")
            with ui.row().classes("gap-1 flex-wrap"):
                for cid in _CHORD_IDS:
                    ui.button(cid, on_click=lambda c=cid: add_chord(c)).props("outline size=sm")
            ui.separator()
            chips_row = ui.row().classes("gap-2 flex-wrap items-center min-h-12")
            with ui.row().classes("gap-2"):
                preview_btn = ui.button("Preview", icon="play_arrow", on_click=lambda: preview())
                ui.button("Clear", icon="clear", on_click=lambda: clear_progression()).props("flat")

        # --- optional lyrics -------------------------------------------------
        with ui.card().classes("w-full gap-2"):
            ui.label("Lyrics (optional)").classes("text-lg font-semibold")
            ui.label(
                "Type lyrics with chords in brackets before the word, e.g. "
                "“[C]Twinkle [F]little [C]star”. Leave blank to save a chord-chart song."
            ).classes("text-xs text-gray-400")
            lyrics_input = ui.textarea(placeholder="[C]Twinkle twinkle [F]little [C]star").props(
                "outlined autogrow"
            ).classes("w-full font-mono")

        with ui.row().classes("self-center gap-3"):
            ui.button("Save song", icon="save", on_click=lambda: save()).props("size=lg")

    # --- behaviour -----------------------------------------------------------
    def rebuild_chips() -> None:
        chips_row.clear()
        state["chips"] = []
        with chips_row:
            if not state["progression"]:
                ui.label("No chords yet — click chords above to add them.").classes(
                    "text-gray-400 text-sm"
                )
            for i, cid in enumerate(state["progression"]):
                with ui.element("div").classes(
                    "flex items-center gap-1 rounded bg-gray-100 px-2 py-1 transition-all"
                ) as chip:
                    ui.button(icon="chevron_left", on_click=lambda i=i: move(i, -1)).props(
                        "round flat dense size=sm"
                    )
                    ui.label(cid).classes("font-bold")
                    ui.button(icon="chevron_right", on_click=lambda i=i: move(i, 1)).props(
                        "round flat dense size=sm"
                    )
                    ui.button(icon="close", on_click=lambda i=i: remove(i)).props(
                        "round flat dense size=sm color=grey"
                    )
                state["chips"].append(chip)

    def add_chord(cid: str) -> None:
        stop_preview()
        state["progression"].append(cid)
        rebuild_chips()

    def remove(i: int) -> None:
        stop_preview()
        del state["progression"][i]
        rebuild_chips()

    def move(i: int, delta: int) -> None:
        stop_preview()
        j = i + delta
        prog = state["progression"]
        if 0 <= j < len(prog):
            prog[i], prog[j] = prog[j], prog[i]
            rebuild_chips()

    def clear_progression() -> None:
        stop_preview()
        state["progression"] = []
        rebuild_chips()

    # --- preview playback ----------------------------------------------------
    def stop_preview() -> None:
        if state["preview_timer"]:
            state["preview_timer"].cancel()
            state["preview_timer"] = None
        preview_btn.set_text("Preview")
        preview_btn.props("color=primary")
        for chip in state["chips"]:
            chip.classes(remove="ring-2 ring-primary")

    def preview() -> None:
        if state["preview_timer"]:
            stop_preview()
            return
        if not state["progression"]:
            ui.notify("Add some chords first.", type="warning")
            return
        state["preview_idx"] = 0
        state["preview_step"] = interval_seconds(bpm_slider.value) * 2  # ~2 beats per chord
        state["preview_start"] = time.time()
        state["preview_last"] = -1
        preview_btn.set_text("Stop")
        preview_btn.props("color=red")
        state["preview_timer"] = ui.timer(0.05, preview_tick)

    def preview_tick() -> None:
        prog = state["progression"]
        elapsed = time.time() - state["preview_start"]
        idx = int(elapsed / state["preview_step"])
        if idx >= len(prog):
            stop_preview()
            return
        if idx != state["preview_last"]:
            state["preview_last"] = idx
            for k, chip in enumerate(state["chips"]):
                chip.classes(add="ring-2 ring-primary") if k == idx else chip.classes(
                    remove="ring-2 ring-primary"
                )
            preview_audio.set_source(f"/audio/chord/{prog[idx]}")
            preview_audio.play()

    def save() -> None:
        if not state["progression"] and not lyrics_input.value.strip():
            ui.notify("Add a progression or some lyrics first.", type="warning")
            return
        stop_preview()
        song = songbook.build_composed_song(
            title=title_input.value,
            artist=artist_input.value,
            tempo=int(bpm_slider.value),
            pattern_id=pattern_select.value,
            progression=list(state["progression"]),
            lyrics_text=lyrics_input.value,
        )
        if not song["chords_used"]:
            ui.notify("Couldn't find any chords — check your lyrics or progression.", type="warning")
            return
        db.save_composed_song(song)
        gamification.record_activity("composed_song")
        ui.notify(f"Saved “{song['title']}”!", type="positive")
        ui.navigate.to(f"/song/{song['id']}")

    rebuild_chips()
