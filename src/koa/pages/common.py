from nicegui import ui

_NAV = [("Chord Library", "/"), ("Switching Trainer", "/switching")]


def page_header(active_path: str) -> None:
    with ui.row().classes("w-full max-w-6xl mx-auto items-center gap-6 p-4 border-b"):
        ui.label("🎵 Koa").classes("text-xl font-bold")
        for label, path in _NAV:
            link = ui.link(label, path).classes("no-underline")
            if path == active_path:
                link.classes("text-primary font-bold")
            else:
                link.classes("text-gray-500")
