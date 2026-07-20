from nicegui import ui

from koa import db, gamification
from koa.ml import adaptive
from koa.pages.common import page_header

# (title, subtitle, emoji, path, gradient)
_TILES = [
    ("Chord Library", "Learn every chord", "🎸", "/library", "linear-gradient(135deg,#7C5CFF,#5B8DEF)"),
    ("Coach", "What to practise next", "🧭", "/coach", "linear-gradient(135deg,#00C2A8,#00A3FF)"),
    ("Switching", "Change chords fast", "🔀", "/switching", "linear-gradient(135deg,#5B8DEF,#7C5CFF)"),
    ("Strumming", "Lock in the rhythm", "🎵", "/strumming", "linear-gradient(135deg,#FF8A00,#FF5CA8)"),
    ("Strum Arcade", "Score, combo, win", "🕹️", "/arcade", "linear-gradient(135deg,#FF5CA8,#FF3D77)"),
    ("Songs", "Play real songs", "🎶", "/songs", "linear-gradient(135deg,#22C55E,#00C2A8)"),
    ("Ear Trainer", "The app listens", "👂", "/listen", "linear-gradient(135deg,#8B5CF6,#6366F1)"),
    ("Compose", "Write your own", "✍️", "/composer", "linear-gradient(135deg,#F43F5E,#FB7185)"),
    ("Notation", "Read the dots", "🎼", "/notation", "linear-gradient(135deg,#475569,#64748B)"),
    ("Dashboard", "Your progress", "🏆", "/dashboard", "linear-gradient(135deg,#F59E0B,#FBBF24)"),
]


def _tile(title: str, subtitle: str, emoji: str, path: str, gradient: str) -> None:
    with ui.element("div").classes("koa-tile w-52").style(f"background:{gradient}").on(
        "click", lambda: ui.navigate.to(path)
    ):
        ui.label(emoji).classes("koa-emoji")
        ui.label(title).classes("text-lg font-bold mt-2")
        ui.label(subtitle).classes("text-sm opacity-90")


def build_home() -> None:
    page_header("/")

    level = gamification.level_info(db.get_total_xp())
    streak = db.get_streak()["current"]
    snapshot = gamification.build_snapshot()
    earned = gamification.earned_badge_ids(snapshot)
    learned = db.get_learned()

    with ui.column().classes("w-full max-w-6xl mx-auto items-center gap-6 p-6"):
        ui.label("Koa").classes("koa-brand text-6xl")
        ui.label("Learn ukulele the fun way — chords, games, songs, and more.").classes(
            "text-gray-500 text-lg -mt-2"
        )

        # HUD -----------------------------------------------------------------
        with ui.card().classes("w-full max-w-3xl gap-3 p-5"):
            with ui.row().classes("w-full items-center justify-between flex-wrap gap-3"):
                with ui.column().classes("gap-0"):
                    ui.label(f"Level {level['level']}").classes("text-3xl font-bold")
                    ui.label(f"{level['total_xp']} XP").classes("text-sm text-gray-500")
                ui.label(f"🔥 {streak}-day streak").classes("text-xl font-semibold")
                ui.label(f"🏅 {len(earned)}/{len(gamification.BADGES)} badges").classes(
                    "text-xl font-semibold"
                )
            ui.linear_progress(
                value=level["into_level"] / level["next_level_xp"], show_value=False
            ).props("rounded size=12px")
            ui.label(
                f"{level['into_level']} / {level['next_level_xp']} XP to level {level['level'] + 1}"
            ).classes("text-xs text-gray-400")

        # Jump back in --------------------------------------------------------
        recs = adaptive.recommend_chords(learned)
        if recs:
            top = recs[0]
            with ui.card().classes("w-full max-w-3xl items-center gap-2 p-4"):
                ui.label("👉 Suggested next").classes("text-sm text-gray-400")
                msg = (
                    f"Learn {top['chord']} — unlocks {top['unlocks']} new song"
                    + ("s" if top["unlocks"] != 1 else "")
                    if top["unlocks"] > 0
                    else f"Learn {top['chord']} next"
                )
                ui.label(msg).classes("text-lg font-semibold")
                with ui.row().classes("gap-2"):
                    ui.button("Learn it", on_click=lambda: ui.navigate.to("/library")).props(
                        "color=primary"
                    )
                    ui.button("Coach", on_click=lambda: ui.navigate.to("/coach")).props("outline")

        # Mode tiles ----------------------------------------------------------
        with ui.row().classes("w-full justify-center gap-4 flex-wrap"):
            for tile in _TILES:
                _tile(*tile)
