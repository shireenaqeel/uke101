"""Calm, cozy global theme — warm beige with muted slate-blue accents."""

from nicegui import ui

PRIMARY = "#4E6E8E"    # muted slate blue
SECONDARY = "#8FA68C"  # soft sage
ACCENT = "#CDA349"     # warm honey

_CSS = """
html, body {
  background:
    radial-gradient(1100px 600px at 12% -8%, #EEF1F3 0%, rgba(238,241,243,0) 55%),
    linear-gradient(170deg, #F8F4EC 0%, #F1EADB 60%, #ECE3D2 100%) fixed !important;
  font-family: 'Nunito', system-ui, sans-serif;
  color: #3E3A33;
}
.nicegui-content { padding: 0 !important; }
h1, h2, h3, .text-2xl, .text-3xl, .text-4xl, .text-5xl, .text-6xl {
  font-family: 'Fraunces', Georgia, serif; letter-spacing: .2px;
}
.text-gray-500 { color: #857b6c !important; }
.text-gray-400 { color: #a49a89 !important; }

.q-card {
  background: #FDFBF6 !important;
  border-radius: 18px !important;
  box-shadow: 0 6px 20px rgba(78,110,142,.09) !important;
  border: 1px solid rgba(78,110,142,.09);
  transition: transform .16s ease, box-shadow .16s ease;
}
.q-card:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(78,110,142,.15) !important; }
.q-btn { border-radius: 12px !important; text-transform: none !important; font-weight: 600; font-family: 'Nunito'; }

.koa-nav {
  position: sticky; top: 0; z-index: 50;
  backdrop-filter: blur(12px);
  background: rgba(248,244,236,.85);
  box-shadow: 0 2px 16px rgba(78,110,142,.10);
  border-bottom: 1px solid rgba(78,110,142,.10);
}
.koa-brand {
  color: #3E5C78;
  font-family: 'Fraunces', Georgia, serif; font-weight: 600; letter-spacing: .3px;
}
.koa-navlink { border-radius: 10px; padding: 4px 12px; font-size: 13px; font-weight: 600; text-decoration: none; color: #6b6152; }
.koa-navlink:hover { background: rgba(78,110,142,.12); }
.koa-navlink-active { background: #4E6E8E; color: white !important; }

.koa-hud { border-radius: 10px; padding: 4px 13px; font-weight: 700; color: white; font-size: 13px; white-space: nowrap; }

.koa-tile {
  border-radius: 20px; padding: 22px; color: white; cursor: pointer;
  box-shadow: 0 8px 20px rgba(60,70,80,.14);
  transition: transform .16s ease, box-shadow .16s ease;
}
.koa-tile:hover { transform: translateY(-4px); box-shadow: 0 16px 32px rgba(60,70,80,.20); }
.koa-tile .koa-emoji { font-size: 34px; line-height: 1; filter: drop-shadow(0 2px 3px rgba(0,0,0,.15)); }

.koala-bob { animation: koala-bob 3.4s ease-in-out infinite; filter: drop-shadow(0 8px 12px rgba(78,110,142,.18)); }
@keyframes koala-bob { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
"""


def apply_theme() -> None:
    ui.colors(
        primary=PRIMARY, secondary=SECONDARY, accent=ACCENT,
        positive="#5E9E6E", negative="#C25B4C", warning="#CDA349",
    )
    ui.add_head_html(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600'
        '&family=Nunito:wght@400;500;600;700&display=swap" rel="stylesheet">'
    )
    ui.add_css(_CSS)
