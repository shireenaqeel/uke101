import time
from html import escape

from nicegui import ui

from koa import db, gamification, songbook
from koa.data.chords import get_chord
from koa.data.songs import cumulative_times, primary_line_chords
from koa.fretboard import render_fretboard
from koa.pages.common import page_header

_DIFFICULTY_COLORS = {"easy": "green", "medium": "amber", "hard": "red"}


def _lyric_html(line: dict) -> str:
    words = line["text"].split(" ")
    chord_at = {c["word"]: c["chord"] for c in line.get("chords", [])}
    spans = []
    for i, word in enumerate(words):
        chord = chord_at.get(i, "")
        spans.append(
            '<span style="display:inline-flex;flex-direction:column;margin-right:10px">'
            f'<span style="height:18px;line-height:18px;color:#7c5cff;font-weight:700;'
            f'font-size:13px">{escape(chord)}</span>'
            f'<span style="font-size:18px">{escape(word)}</span></span>'
        )
    return '<div style="display:flex;flex-wrap:wrap;align-items:flex-end">' + "".join(spans) + "</div>"


# --------------------------------------------------------------------------- #
# Song list
# --------------------------------------------------------------------------- #
def build_song_list() -> None:
    page_header("/songs")
    completed = db.get_completed_songs()

    with ui.column().classes("w-full max-w-5xl mx-auto items-center gap-4 p-6"):
        with ui.row().classes("w-full max-w-5xl items-center justify-between"):
            ui.label("Songs").classes("text-3xl font-bold")
            ui.button(
                "Compose a song", icon="add", on_click=lambda: ui.navigate.to("/composer")
            ).props("outline")
        ui.label("Play a real song end to end — lyrics and chords scroll in time.").classes(
            "text-gray-500"
        )
        with ui.row().classes("w-full justify-center gap-4 flex-wrap"):
            for song in songbook.all_songs():
                with ui.card().classes("w-72 gap-2"):
                    with ui.row().classes("w-full items-center justify-between"):
                        ui.label(song["title"]).classes("text-lg font-bold")
                        ui.badge(song["difficulty"], color=_DIFFICULTY_COLORS[song["difficulty"]])
                    ui.label(song["artist"]).classes("text-sm text-gray-500 -mt-2")
                    with ui.row().classes("gap-1 flex-wrap items-center"):
                        for chord in song["chords_used"]:
                            ui.badge(chord, color="secondary")
                        if song.get("is_user_composed"):
                            ui.badge("My song", color="purple")
                    if not song["lyrics_included"]:
                        ui.label("Chord chart only").classes("text-xs text-gray-400")
                    with ui.row().classes("w-full items-center justify-between"):
                        if song["id"] in completed:
                            ui.label("✓ completed").classes("text-xs text-green-600")
                        else:
                            ui.space()
                        with ui.row().classes("gap-1"):
                            if song.get("is_user_composed"):
                                ui.button(
                                    icon="delete",
                                    on_click=lambda s=song: _delete_song(s["id"], s["title"]),
                                ).props("round flat size=sm color=grey").tooltip("Delete")
                            ui.button(
                                "Open", on_click=lambda s=song: ui.navigate.to(f"/song/{s['id']}")
                            ).props("size=sm")


def _delete_song(song_id: str, title: str) -> None:
    db.delete_composed_song(song_id)
    ui.notify(f"Deleted “{title}”.", type="warning")
    ui.navigate.to("/songs")


# --------------------------------------------------------------------------- #
# Song player
# --------------------------------------------------------------------------- #
def build_song_player(song_id: str) -> None:
    page_header("/songs")
    song = songbook.get_song(song_id)
    if song is None:
        with ui.column().classes("w-full max-w-3xl mx-auto items-center gap-4 p-6"):
            ui.label("Song not found").classes("text-2xl")
            ui.button("Back to songs", on_click=lambda: ui.navigate.to("/songs"))
        return

    # Build the ordered "steps" the playhead moves through.
    steps: list[dict] = []
    if song["lyrics_included"]:
        chords = primary_line_chords(song)
        for line, chord in zip(song["lines"], chords):
            steps.append({"kind": "lyric", "line": line, "chord": chord, "beats": line.get("beats", 8)})
    else:
        for chord in song["progression"]:
            steps.append({"kind": "chord", "chord": chord, "beats": 4})

    state = {
        "playing": False,
        "start": 0.0,
        "active": -1,
        "timer": None,
        "starts": [],
        "total": 0.0,
        "step_elems": [],
    }

    with ui.column().classes("w-full max-w-5xl mx-auto items-stretch gap-4 p-6"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-0"):
                ui.label(song["title"]).classes("text-3xl font-bold")
                ui.label(f"{song['artist']} · {'/'.join(song['chords_used'])}").classes(
                    "text-gray-500"
                )
            ui.button("← Songs", on_click=lambda: ui.navigate.to("/songs")).props("flat")

        if not song["lyrics_included"]:
            if song.get("source_url"):
                ui.label(
                    "Lyrics aren't included for this song (copyrighted). Play along with the chord "
                    "progression below and follow the full lyrics at the link."
                ).classes("text-sm text-gray-500")
                ui.link("Open lyrics ↗", song["source_url"], new_tab=True).classes("text-sm")
            else:
                ui.label("Your chord chart — play along with the progression below.").classes(
                    "text-sm text-gray-500"
                )

        with ui.row().classes("w-full gap-6 items-start"):
            # scrolling steps
            steps_box = ui.column().classes(
                "flex-1 gap-2 h-96 overflow-auto p-2 border rounded"
            )
            with steps_box:
                for i, step in enumerate(steps):
                    if step["kind"] == "lyric":
                        el = ui.html(_lyric_html(step["line"]))
                    else:
                        el = ui.html(
                            f'<div style="font-size:28px;font-weight:700;color:#7c5cff">'
                            f'{escape(step["chord"])}</div>'
                        )
                    el.classes("rounded px-2 py-1 transition-all").props(f"id=step-{i}")
                    state["step_elems"].append(el)

            # sidebar: current chord + controls
            with ui.column().classes("w-64 items-center gap-3"):
                chord_name = ui.label("—").classes("text-2xl font-bold")
                diagram = ui.html("")
                with ui.row().classes("items-center gap-2"):
                    play_btn = ui.button("Play", on_click=lambda: toggle()).props("size=md")
                    ui.button(icon="replay", on_click=lambda: restart()).props("round flat").tooltip(
                        "Restart"
                    )
                with ui.column().classes("items-center gap-1 w-full"):
                    ui.label("Tempo").classes("text-xs text-gray-400")
                    bpm_slider = ui.slider(min=50, max=160, value=song["tempo"]).props(
                        "label-always"
                    ).classes("w-full")
                complete_btn = ui.button(
                    "Mark completed", on_click=lambda: mark_complete()
                ).props("outline size-sm")
                ui.button("Export chart", icon="download", on_click=lambda: export_chart()).props(
                    "flat size-sm"
                )

    # --- behaviour -----------------------------------------------------------
    def set_active(idx: int) -> None:
        state["active"] = idx
        for i, el in enumerate(state["step_elems"]):
            if i == idx:
                el.classes(add="bg-amber-100 ring-1 ring-amber-400")
            else:
                el.classes(remove="bg-amber-100 ring-1 ring-amber-400")
        chord = steps[idx]["chord"] if 0 <= idx < len(steps) else None
        chord_obj = get_chord(chord) if chord else None
        if chord_obj:
            chord_name.text = chord
            diagram.set_content(render_fretboard(chord_obj))
        elif chord:
            chord_name.text = chord  # unknown chord (custom label): show name, no diagram
            diagram.set_content("")
        if 0 <= idx < len(steps):
            ui.run_javascript(
                f"var e=document.getElementById('step-{idx}');"
                "if(e)e.scrollIntoView({behavior:'smooth',block:'center'});"
            )

    def tick() -> None:
        now = time.time() - state["start"]
        idx = 0
        for i, start in enumerate(state["starts"]):
            if now >= start:
                idx = i
        if idx != state["active"]:
            set_active(idx)
        if now >= state["total"]:
            finish()

    def start() -> None:
        state["starts"], state["total"] = cumulative_times(
            [s["beats"] for s in steps], bpm_slider.value
        )
        state["playing"] = True
        state["start"] = time.time()
        play_btn.set_text("Pause")
        play_btn.props("color=red")
        set_active(0)
        state["timer"] = ui.timer(0.1, tick)

    def stop() -> None:
        state["playing"] = False
        if state["timer"]:
            state["timer"].cancel()
            state["timer"] = None
        play_btn.set_text("Play")
        play_btn.props("color=primary")

    def toggle() -> None:
        stop() if state["playing"] else start()

    def restart() -> None:
        stop()
        set_active(0 if steps else -1)

    def _complete() -> None:
        if song["id"] not in db.get_completed_songs():
            db.mark_song_completed(song["id"])
            gamification.record_activity("song")

    def finish() -> None:
        stop()
        _complete()
        ui.notify("Song complete — nice work! Marked as completed.", type="positive")

    def mark_complete() -> None:
        _complete()
        ui.notify("Marked as completed.", type="positive")

    def export_chart() -> None:
        text = songbook.chord_chart_text(song)
        ui.download(text.encode("utf-8"), f"{song['id']}.txt")

    if steps:
        set_active(0)
