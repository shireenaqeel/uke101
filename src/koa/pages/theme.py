"""Global playful theme — applied on every page via page_header."""

from nicegui import ui

PRIMARY = "#7C5CFF"
SECONDARY = "#FF5CA8"
ACCENT = "#00C2A8"

_CSS = """
html, body {
  background: linear-gradient(160deg, #EEF2FF 0%, #FDECFF 45%, #FFF3E9 100%) fixed !important;
  font-family: 'Poppins', system-ui, sans-serif;
}
.nicegui-content { padding: 0 !important; }
h1, h2, h3, .text-2xl, .text-3xl, .text-4xl, .text-5xl { font-family: 'Fredoka', sans-serif; }

.q-card {
  border-radius: 22px !important;
  box-shadow: 0 10px 30px rgba(124,92,255,.10) !important;
  border: 1px solid rgba(124,92,255,.07);
  transition: transform .15s ease, box-shadow .15s ease;
}
.q-card:hover { transform: translateY(-3px); box-shadow: 0 16px 40px rgba(124,92,255,.18) !important; }
.q-btn { border-radius: 999px !important; text-transform: none !important; font-weight: 600; }

.koa-nav {
  position: sticky; top: 0; z-index: 50;
  backdrop-filter: blur(12px);
  background: rgba(255,255,255,.72);
  box-shadow: 0 4px 24px rgba(0,0,0,.06);
}
.koa-brand {
  background: linear-gradient(90deg, #7C5CFF, #FF5CA8);
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
  font-family: 'Fredoka', sans-serif; font-weight: 700;
}
.koa-navlink { border-radius: 999px; padding: 4px 12px; font-size: 13px; font-weight: 600; text-decoration: none; }
.koa-navlink:hover { background: rgba(124,92,255,.12); }
.koa-navlink-active { background: linear-gradient(90deg, #7C5CFF, #9C7BFF); color: white !important; }

.koa-hud { border-radius: 999px; padding: 4px 14px; font-weight: 700; color: white; font-size: 13px; white-space: nowrap; }

.koa-tile {
  border-radius: 26px; padding: 22px; color: white; cursor: pointer;
  box-shadow: 0 12px 28px rgba(0,0,0,.14);
  transition: transform .16s ease, box-shadow .16s ease;
}
.koa-tile:hover { transform: translateY(-5px) scale(1.02); box-shadow: 0 20px 40px rgba(0,0,0,.20); }
.koa-tile .koa-emoji { font-size: 34px; line-height: 1; }
"""

_applied = False


def apply_theme() -> None:
    ui.colors(
        primary=PRIMARY, secondary=SECONDARY, accent=ACCENT,
        positive="#22C55E", negative="#EF4444", warning="#F59E0B",
    )
    ui.add_head_html(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700'
        '&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">'
    )
    ui.add_css(_CSS)
