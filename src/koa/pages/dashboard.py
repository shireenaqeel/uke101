from nicegui import ui

from koa import db
from koa.data.chords import CHORDS
from koa.data.drills import drill_labels
from koa.data.patterns import PATTERNS_BY_ID, STRUMMING_PATTERNS
from koa.data.songs import SONGS, SONGS_BY_ID
from koa.pages.common import page_header


def build_dashboard() -> None:
    page_header("/dashboard")

    learned = db.get_learned()
    switch_bests = db.get_switch_bests()
    arcade_bests = db.get_arcade_bests()
    completed_songs = db.get_completed_songs()
    labels = drill_labels()

    with ui.column().classes("w-full max-w-4xl mx-auto items-stretch gap-6 p-6"):
        ui.label("Progress Dashboard").classes("text-3xl font-bold self-center")

        # --- chords learned --------------------------------------------------
        with ui.card().classes("w-full gap-3"):
            with ui.row().classes("w-full items-baseline justify-between"):
                ui.label("Chords learned").classes("text-xl font-semibold")
                ui.label(f"{len(learned)} / {len(CHORDS)}").classes("text-lg text-primary")
            ui.linear_progress(
                value=len(learned) / len(CHORDS) if CHORDS else 0, show_value=False
            ).props("rounded")
            with ui.row().classes("gap-2 flex-wrap"):
                for chord in CHORDS:
                    is_learned = chord["id"] in learned
                    ui.badge(chord["name"], color="green" if is_learned else "grey-4").classes(
                        "" if is_learned else "text-gray-500"
                    )

        # --- switch-drill speeds --------------------------------------------
        with ui.card().classes("w-full gap-3"):
            ui.label("Chord switching — best clean switches").classes("text-xl font-semibold")
            if switch_bests:
                rows = [
                    {"drill": labels.get(key, key), "best": best}
                    for key, best in sorted(
                        switch_bests.items(), key=lambda kv: kv[1], reverse=True
                    )
                ]
                ui.table(
                    columns=[
                        {"name": "drill", "label": "Drill", "field": "drill", "align": "left"},
                        {"name": "best", "label": "Best switches", "field": "best"},
                    ],
                    rows=rows,
                    row_key="drill",
                ).classes("w-full")
            else:
                ui.label(
                    "No switching scores yet — try the Switching Trainer to start tracking."
                ).classes("text-gray-500")

        # --- strum arcade high scores ---------------------------------------
        with ui.card().classes("w-full gap-3"):
            ui.label("Strum Arcade — high scores").classes("text-xl font-semibold")
            if arcade_bests:
                rows = [
                    {
                        "pattern": PATTERNS_BY_ID[pid]["name"] if pid in PATTERNS_BY_ID else pid,
                        "score": score,
                    }
                    for pid, score in sorted(
                        arcade_bests.items(), key=lambda kv: kv[1], reverse=True
                    )
                ]
                ui.table(
                    columns=[
                        {"name": "pattern", "label": "Pattern", "field": "pattern", "align": "left"},
                        {"name": "score", "label": "High score", "field": "score"},
                    ],
                    rows=rows,
                    row_key="pattern",
                ).classes("w-full")
            else:
                ui.label("No arcade scores yet — play the Strum Arcade to set one.").classes(
                    "text-gray-500"
                )

        # --- songs completed -------------------------------------------------
        with ui.card().classes("w-full gap-3"):
            with ui.row().classes("w-full items-baseline justify-between"):
                ui.label("Songs completed").classes("text-xl font-semibold")
                ui.label(f"{len(completed_songs)} / {len(SONGS)}").classes("text-lg text-primary")
            if completed_songs:
                with ui.row().classes("gap-2 flex-wrap"):
                    for sid in completed_songs:
                        title = SONGS_BY_ID[sid]["title"] if sid in SONGS_BY_ID else sid
                        ui.badge(title, color="green")
            else:
                ui.label("No songs completed yet — play one end to end in Song Mode.").classes(
                    "text-gray-500"
                )

        # --- strumming patterns ---------------------------------------------
        with ui.card().classes("w-full gap-2"):
            ui.label("Strumming patterns available to practice").classes("text-xl font-semibold")
            with ui.row().classes("gap-2 flex-wrap"):
                for pattern in STRUMMING_PATTERNS:
                    ui.badge(pattern["name"], color="secondary")
