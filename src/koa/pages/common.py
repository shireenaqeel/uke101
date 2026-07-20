from nicegui import ui

from koa import db, gamification
from koa.pages.theme import apply_theme

_NAV = [
    ("Home", "/"),
    ("Chords", "/library"),
    ("Coach", "/coach"),
    ("Switching", "/switching"),
    ("Strumming", "/strumming"),
    ("Arcade", "/arcade"),
    ("Songs", "/songs"),
    ("Ear", "/listen"),
    ("Compose", "/composer"),
    ("Notation", "/notation"),
    ("Dashboard", "/dashboard"),
]


def page_header(active_path: str) -> None:
    apply_theme()

    level = gamification.level_info(db.get_total_xp())
    streak = db.get_streak()["current"]

    with ui.row().classes(
        "koa-nav w-full items-center gap-2 px-4 py-2 flex-wrap justify-between"
    ):
        with ui.row().classes("items-center gap-3 flex-wrap"):
            ui.label("🎸 Koa").classes("koa-brand text-xl")
            with ui.row().classes("items-center gap-1 flex-wrap"):
                for label, path in _NAV:
                    cls = "koa-navlink" + (" koa-navlink-active" if path == active_path else "")
                    ui.link(label, path).classes(cls)
        with ui.row().classes("items-center gap-2"):
            ui.label(f"⭐ Lv {level['level']}").classes("koa-hud").style(
                "background:linear-gradient(90deg,#7C5CFF,#9C7BFF)"
            )
            ui.label(f"🔥 {streak}").classes("koa-hud").style(
                "background:linear-gradient(90deg,#FF8A00,#FF5CA8)"
            )
