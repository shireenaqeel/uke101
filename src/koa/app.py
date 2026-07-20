from nicegui import ui

from koa import db
from koa.pages.arcade import build_arcade
from koa.pages.dashboard import build_dashboard
from koa.pages.library import build_library
from koa.pages.strumming import build_strumming
from koa.pages.switching import build_switching


@ui.page("/")
def index() -> None:
    build_library()


@ui.page("/switching")
def switching() -> None:
    build_switching()


@ui.page("/strumming")
def strumming() -> None:
    build_strumming()


@ui.page("/arcade")
def arcade() -> None:
    build_arcade()


@ui.page("/dashboard")
def dashboard() -> None:
    build_dashboard()


def main() -> None:
    db.init_db()
    ui.run(title="Koa — Ukulele Learning", reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
