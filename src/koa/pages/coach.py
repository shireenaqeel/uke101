from nicegui import ui

from koa import db
from koa.data.chords import get_chord
from koa.ml import adaptive
from koa.pages.common import page_header

_DIFFICULTY_COLORS = {"easy": "green", "medium": "amber", "hard": "red"}


def build_coach() -> None:
    page_header("/coach")

    learned = db.get_learned()
    switch_bests = db.get_switch_bests()
    completed = db.get_completed_songs()

    chord_recs = adaptive.recommend_chords(learned)
    weak = adaptive.weak_drills(switch_bests)
    playable = adaptive.songs_playable_now(learned, completed=completed)
    one_away = adaptive.songs_one_away(learned)

    with ui.column().classes("w-full max-w-4xl mx-auto items-stretch gap-6 p-6"):
        ui.label("What to practice next").classes("text-3xl font-bold self-center")
        ui.label(
            "Personalised from your progress — weak spots first, and the chords that open up "
            "the most new songs."
        ).classes("text-gray-500 self-center text-center max-w-2xl")

        # --- learn next chord -----------------------------------------------
        with ui.card().classes("w-full gap-3"):
            ui.label("Learn this chord next").classes("text-xl font-semibold")
            top = [r for r in chord_recs][:3]
            if top:
                with ui.row().classes("gap-4 flex-wrap"):
                    for rec in top:
                        with ui.card().classes("w-56 gap-1 items-start"):
                            with ui.row().classes("w-full items-center justify-between"):
                                ui.label(rec["chord"]).classes("text-xl font-bold")
                                ui.badge(rec["difficulty"], color=_DIFFICULTY_COLORS[rec["difficulty"]])
                            if rec["unlocks"] > 0:
                                ui.label(
                                    f"Unlocks {rec['unlocks']} new song"
                                    + ("s" if rec["unlocks"] != 1 else "")
                                ).classes("text-sm text-primary")
                            else:
                                ui.label(f"Used in {rec['songs_using']} songs").classes(
                                    "text-sm text-gray-500"
                                )
                ui.button("Open Chord Library", on_click=lambda: ui.navigate.to("/")).props(
                    "outline size=sm"
                )
            else:
                ui.label("You've learned every chord. 🎉").classes("text-gray-500")

        # --- weak switch drills ---------------------------------------------
        with ui.card().classes("w-full gap-3"):
            ui.label("Focus your chord switching").classes("text-xl font-semibold")
            ui.label("Drills you haven't practised, or where your best is lowest.").classes(
                "text-sm text-gray-400"
            )
            for row in weak[:3]:
                drill = row["drill"]
                with ui.row().classes("w-full items-center justify-between"):
                    label = drill["label"]
                    best = "not tried yet" if row["best"] is None else f"best {row['best']}"
                    ui.label(f"{label} — {best}")
                    ui.button(
                        "Practise", on_click=lambda d=drill: _open_drill(d)
                    ).props("size=sm outline")

        # --- songs you can play now -----------------------------------------
        with ui.card().classes("w-full gap-3"):
            ui.label("Songs you can play now").classes("text-xl font-semibold")
            if playable:
                with ui.row().classes("gap-2 flex-wrap"):
                    for song in playable:
                        ui.button(
                            song["title"], on_click=lambda s=song: ui.navigate.to(f"/song/{s['id']}")
                        ).props("outline size=sm")
            else:
                ui.label(
                    "Learn a few more chords and songs will start showing up here."
                ).classes("text-gray-500")

        # --- one chord away -------------------------------------------------
        if one_away:
            with ui.card().classes("w-full gap-3"):
                ui.label("One chord away").classes("text-xl font-semibold")
                for item in one_away:
                    song = item["song"]
                    with ui.row().classes("w-full items-center justify-between"):
                        ui.label(f"{song['title']} — learn {item['missing']}")
                        ui.button(
                            f"Learn {item['missing']}", on_click=lambda: ui.navigate.to("/")
                        ).props("size=sm flat")


def _open_drill(drill: dict) -> None:
    chords = drill["chords"]
    if len(chords) == 2:
        ui.navigate.to(f"/switching?a={chords[0]}&b={chords[1]}")
    else:
        ui.navigate.to("/switching")
