from nicegui import ui

from koa import db
from koa.data.chords import CHORDS
from koa.data.drills import drill_labels
from koa.data.patterns import STRUMMING_PATTERNS
from koa.pages.common import page_header


def build_dashboard() -> None:
    page_header("/dashboard")

    learned = db.get_learned()
    switch_bests = db.get_switch_bests()
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

        # --- strumming patterns ---------------------------------------------
        with ui.card().classes("w-full gap-2"):
            ui.label("Strumming patterns available to practice").classes("text-xl font-semibold")
            with ui.row().classes("gap-2 flex-wrap"):
                for pattern in STRUMMING_PATTERNS:
                    ui.badge(pattern["name"], color="secondary")
