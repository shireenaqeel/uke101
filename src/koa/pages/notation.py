from nicegui import ui

from koa import db, gamification
from koa.data.notation import NOTATION_DRILLS, NOTATION_TRACKS, get_track_drills
from koa.notation import render_notation
from koa.pages.common import page_header

_TRACKS_BY_ID = {t["id"]: t for t in NOTATION_TRACKS}


def _max_level(track: str) -> int:
    drills = get_track_drills(track)
    return max((d["level"] for d in drills), default=0)


# --------------------------------------------------------------------------- #
# Track overview
# --------------------------------------------------------------------------- #
def build_notation_home() -> None:
    page_header("/notation")
    progress = db.get_notation_progress()

    with ui.column().classes("w-full max-w-4xl mx-auto items-center gap-4 p-6"):
        ui.label("Notation Reading").classes("text-3xl font-bold")
        ui.label(
            "An optional track for going beyond chord charts. Short drills — read a symbol, "
            "identify it, get instant feedback. Practice in quick isolated reps."
        ).classes("text-gray-500 text-center max-w-2xl")

        with ui.row().classes("w-full justify-center gap-4 flex-wrap"):
            for track in NOTATION_TRACKS:
                level = progress.get(track["id"], 0)
                top = _max_level(track["id"])
                with ui.card().classes("w-72 gap-2"):
                    ui.label(track["name"]).classes("text-xl font-bold")
                    ui.label(track["desc"]).classes("text-sm text-gray-500")
                    ui.linear_progress(
                        value=level / top if top else 0, show_value=False
                    ).props("rounded")
                    ui.label(f"Level {level} of {top}").classes("text-xs text-gray-400")
                    ui.button(
                        "Practice",
                        on_click=lambda t=track: ui.navigate.to(f"/notation/{t['id']}"),
                    ).props("size=sm")


# --------------------------------------------------------------------------- #
# Practice session
# --------------------------------------------------------------------------- #
def build_notation_practice(track: str) -> None:
    page_header("/notation")
    if track not in NOTATION_DRILLS:
        with ui.column().classes("w-full max-w-3xl mx-auto items-center gap-4 p-6"):
            ui.label("Unknown track").classes("text-2xl")
            ui.button("Back to notation", on_click=lambda: ui.navigate.to("/notation"))
        return

    drills = get_track_drills(track)
    state = {"idx": 0, "correct": 0, "best_level": 0, "answered": False}

    with ui.column().classes("w-full max-w-2xl mx-auto items-center gap-4 p-6"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(f"{_TRACKS_BY_ID[track]['name']} practice").classes("text-2xl font-bold")
            ui.button("← Notation", on_click=lambda: ui.navigate.to("/notation")).props("flat")

        progress_label = ui.label("").classes("text-sm text-gray-400")
        prompt = ui.html("").classes("border rounded p-4 bg-white")
        question = ui.label("").classes("text-lg text-center")
        choices_box = ui.column().classes("items-stretch gap-2 w-72")
        feedback = ui.label("").classes("text-lg font-semibold h-7")
        next_btn = ui.button("Next", on_click=lambda: advance()).props("size=lg")
        next_btn.visible = False
        summary = ui.column().classes("items-center gap-2")

    def show_drill() -> None:
        drill = drills[state["idx"]]
        state["answered"] = False
        progress_label.text = f"Question {state['idx'] + 1} of {len(drills)}"
        prompt.set_content(render_notation(drill["render"]))
        question.text = drill["question"]
        feedback.text = ""
        next_btn.visible = False
        choices_box.clear()
        with choices_box:
            for choice in drill["choices"]:
                ui.button(choice, on_click=lambda c=choice: answer(c)).props("outline").classes(
                    "w-full"
                )

    def answer(choice: str) -> None:
        if state["answered"]:
            return
        state["answered"] = True
        drill = drills[state["idx"]]
        for btn in choices_box:
            btn.disable()
        if choice == drill["answer"]:
            state["correct"] += 1
            state["best_level"] = max(state["best_level"], drill["level"])
            feedback.text = "Correct!"
            feedback.style("color: #16a34a")
        else:
            feedback.text = f"Not quite — it's {drill['answer']}"
            feedback.style("color: #dc2626")
        next_btn.visible = True

    def advance() -> None:
        state["idx"] += 1
        if state["idx"] < len(drills):
            show_drill()
        else:
            finish()

    def finish() -> None:
        if state["best_level"] > 0:
            db.set_notation_level(track, state["best_level"])
        if state["correct"] > 0:
            gamification.record_activity("notation_session")
        prompt.visible = False
        question.visible = False
        choices_box.visible = False
        feedback.visible = False
        next_btn.visible = False
        progress_label.visible = False
        summary.clear()
        with summary:
            ui.label(f"You got {state['correct']} of {len(drills)} correct.").classes(
                "text-2xl font-bold"
            )
            ui.label(f"Reached level {state['best_level']} on this track.").classes("text-gray-600")
            with ui.row().classes("gap-3"):
                ui.button("Practice again", on_click=lambda: ui.navigate.to(f"/notation/{track}"))
                ui.button("Back to notation", on_click=lambda: ui.navigate.to("/notation")).props(
                    "outline"
                )

    show_drill()
