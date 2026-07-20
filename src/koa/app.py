from nicegui import ui

from koa import db
from koa.pages.arcade import build_arcade
from koa.pages.coach import build_coach
from koa.pages.composer import build_composer
from koa.pages.dashboard import build_dashboard
from koa.pages.library import build_library
from koa.pages.notation import build_notation_home, build_notation_practice
from koa.pages.songs import build_song_list, build_song_player
from koa.pages.strumming import build_strumming
from koa.pages.switching import build_switching


@ui.page("/")
def index() -> None:
    build_library()


@ui.page("/switching")
def switching(a: str | None = None, b: str | None = None) -> None:
    build_switching(a, b)


@ui.page("/coach")
def coach() -> None:
    build_coach()


@ui.page("/strumming")
def strumming() -> None:
    build_strumming()


@ui.page("/arcade")
def arcade() -> None:
    build_arcade()


@ui.page("/songs")
def songs() -> None:
    build_song_list()


@ui.page("/song/{song_id}")
def song_player(song_id: str) -> None:
    build_song_player(song_id)


@ui.page("/composer")
def composer() -> None:
    build_composer()


@ui.page("/notation")
def notation() -> None:
    build_notation_home()


@ui.page("/notation/{track}")
def notation_practice(track: str) -> None:
    build_notation_practice(track)


@ui.page("/dashboard")
def dashboard() -> None:
    build_dashboard()


def main() -> None:
    db.init_db()
    ui.run(title="Koa — Ukulele Learning", reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
