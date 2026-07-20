from nicegui import ui

from koa import db
from koa.pages.library import build_library
from koa.pages.switching import build_switching


@ui.page("/")
def index() -> None:
    build_library()


@ui.page("/switching")
def switching() -> None:
    build_switching()


def main() -> None:
    db.init_db()
    ui.run(title="Koa — Ukulele Learning", reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
