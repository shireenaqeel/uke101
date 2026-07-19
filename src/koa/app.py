from nicegui import ui

from koa import __version__


def build_home() -> None:
    with ui.column().classes("w-full max-w-2xl mx-auto items-center gap-4 p-8"):
        ui.label("Koa").classes("text-4xl font-bold")
        ui.label("Learn ukulele from zero — chords, switching, strumming, songs.").classes(
            "text-lg text-gray-500"
        )
        ui.label(f"v{__version__} — scaffold ready. Phase 1 (Chord Library) is next.").classes(
            "text-sm text-gray-400"
        )


@ui.page("/")
def index() -> None:
    build_home()


def main() -> None:
    ui.run(title="Koa — Ukulele Learning", reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
