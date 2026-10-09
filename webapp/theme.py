"""
Visual do dashboard (inspirado no app AlfaceAI / APP-Estufa).

Paleta, raios e espaçamentos copiados de frontend/src/theme.ts do app.
Uso: chame apply_theme() uma vez no app.py e use os helpers abaixo.
"""

import re

import streamlit as st

APP_NAME = "Estufa Inteligente"   # troque por "AlfaceAI" se quiser igual ao app

C = {
    "surface": "#FFFFFF",
    "on_surface": "#1A2C21",
    "surface2": "#F4F7F5",
    "on_surface2": "#2D4A3E",
    "brand": "#0A4C36",
    "primary": "#158348",
    "brand_tertiary": "#EAF2ED",
    "brand_secondary": "#D8E6DE",
    "warning": "#D97706",
    "error": "#C84C31",
    "success": "#158348",
    "border": "#E7EFEA",
    "border_strong": "#C5D6CC",
    "muted": "#6B7A72",
}

HERO_LOGIN = (
    "https://images.pexels.com/photos/37861016/pexels-photo-37861016.jpeg"
    "?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
)
HERO_DASH = (
    "https://images.pexels.com/photos/89267/pexels-photo-89267.jpeg"
    "?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
)

# Ícones SVG (traço) para usar dentro do HTML
_ICONS = {
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "thermo": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
    "water": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7Z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "alert": '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
    "check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "warn": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4M12 17h.01"/>',
}


def icon(name: str, size: int = 18, color: str = "currentColor") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="flex-shrink:0">{_ICONS[name]}</svg>'
    )


def _html(s: str) -> None:
    """Renderiza HTML sem que o markdown trate a indentação como código."""
    s = re.sub(r"\n\s*", "", s.strip())
    st.markdown(s, unsafe_allow_html=True)


# ------------------------------------------------------------------
# CSS global
# ------------------------------------------------------------------
_CSS = f"""
<style>
html, body, [class*="css"], .stApp {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: {C['on_surface']};
}}
#MainMenu, footer, [data-testid="stDecoration"] {{ visibility: hidden; height: 0; }}
header[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ max-width: 920px; padding-top: 1.5rem; padding-bottom: 4rem; }}

/* títulos */
h1, h2, h3 {{ letter-spacing: -0.4px; color: {C['on_surface']}; font-weight: 700; }}
h1 {{ font-size: 26px !important; }}
h2 {{ font-size: 20px !important; }}
h3 {{ font-size: 16px !important; }}
hr {{ border-color: {C['border']} !important; }}
[data-testid="stCaptionContainer"] {{ color: {C['muted']}; }}

/* sidebar */
[data-testid="stSidebar"] {{ background: {C['surface']}; border-right: 1px solid {C['border']}; }}
[data-testid="stSidebarNav"] a {{
  border-radius: 12px; font-weight: 600; font-size: 14px; color: {C['on_surface']};
}}
[data-testid="stSidebarNav"] a[aria-current="page"] {{
  background: {C['brand_tertiary']}; color: {C['primary']};
}}

/* botões */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {{
  background: {C['primary']}; color: #fff; border: none; border-radius: 12px;
  height: 54px; font-size: 16px; font-weight: 600; letter-spacing: .2px;
  transition: opacity .15s;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {{
  background: {C['primary']}; color: #fff; opacity: .85; border: none;
}}
.stButton > button:focus:not(:active) {{ color: #fff; border: none; box-shadow: none; }}
.btn-small .stButton > button {{ height: 38px; font-size: 13px; }}

/* inputs */
div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="textarea"] {{
  background: {C['surface2']} !important; border-radius: 12px !important;
  border: 1px solid {C['border']} !important;
}}
div[data-baseweb="input"] input {{ background: transparent !important; font-size: 15px; height: 40px; }}
div[data-baseweb="input"]:focus-within {{ border-color: {C['primary']} !important; }}
[data-testid="stWidgetLabel"] p {{ font-size: 13px; font-weight: 600; color: {C['on_surface2']}; }}
[data-testid="stForm"] {{ border: none; padding: 0; }}

/* st.metric vira card */
[data-testid="stMetric"] {{
  background: {C['surface2']}; border-radius: 12px; padding: 14px 16px;
  border: 1px solid {C['border']};
}}
[data-testid="stMetricLabel"] p {{ font-size: 12px; color: {C['muted']}; }}
[data-testid="stMetricValue"] {{ font-size: 24px; font-weight: 700; letter-spacing: -0.5px; }}

/* tabs */
[data-baseweb="tab-list"] {{ gap: 6px; background: {C['surface2']}; padding: 4px; border-radius: 12px; }}
[data-baseweb="tab"] {{ border-radius: 9px; height: 36px; font-weight: 600; color: {C['muted']}; padding: 0 14px; }}
[data-baseweb="tab"][aria-selected="true"] {{ background: {C['surface']}; color: {C['primary']}; }}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{ display: none; }}

/* alerts / expander / imagens */
[data-testid="stAlert"] {{ border-radius: 12px; border: none; }}
[data-testid="stExpander"] {{ border: 1px solid {C['border']}; border-radius: 12px; background: {C['surface2']}; }}
[data-testid="stImage"] img {{ border-radius: 12px; }}
[data-testid="stCheckbox"] label p {{ font-size: 14px; font-weight: 500; }}

/* ---------- componentes próprios ---------- */
.sec-row {{ display:flex; justify-content:space-between; align-items:flex-end; margin: 24px 0 12px; }}
.sec-title {{ font-size:16px; font-weight:700; letter-spacing:-.2px; }}
.sec-hint {{ font-size:12px; color:{C['muted']}; }}
.sec-link {{ font-size:13px; font-weight:600; color:{C['primary']}; }}

.topbar {{ display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px; }}
.hello {{ font-size:13px; color:{C['muted']}; }}
.uname {{ font-size:20px; font-weight:700; letter-spacing:-.3px; }}
.bell {{ position:relative; width:42px; height:42px; border-radius:999px; background:{C['surface2']};
        display:flex; align-items:center; justify-content:center; color:{C['on_surface']}; }}
.bell .badge {{ position:absolute; top:4px; right:4px; min-width:18px; height:18px; padding:0 4px;
        border-radius:9px; background:{C['error']}; color:#fff; font-size:10px; font-weight:700;
        display:flex; align-items:center; justify-content:center; }}

.hero {{ position:relative; border-radius:20px; overflow:hidden; height:160px; color:#fff; }}
.hero-inner {{ position:absolute; inset:0; padding:16px; display:flex; flex-direction:column; justify-content:space-between; }}
.hero-top {{ display:flex; justify-content:space-between; align-items:center; }}
.pill {{ display:inline-flex; align-items:center; gap:6px; padding:5px 10px; border-radius:999px; font-size:12px; font-weight:700; }}
.hero-time {{ font-size:11px; opacity:.85; }}
.hero-title {{ font-size:22px; font-weight:700; letter-spacing:-.3px; }}
.hero-sub {{ font-size:13px; opacity:.85; margin-top:2px; }}

.lastsend {{ display:flex; align-items:center; gap:8px; padding:12px; background:{C['surface2']}; border-radius:12px; margin-bottom:12px; }}
.lastsend .lbl {{ font-size:11px; color:{C['muted']}; }}
.lastsend .val {{ font-size:13px; font-weight:700; margin-top:2px; }}
.devbadge {{ margin-left:auto; font-size:10px; font-weight:700; color:{C['primary']}; background:{C['brand_tertiary']}; padding:3px 8px; border-radius:999px; }}

.mcard {{ background:{C['surface2']}; border:1px solid {C['border']}; border-radius:12px; padding:14px; height:100%; }}
.mcard .iw {{ width:36px; height:36px; border-radius:12px; background:{C['brand_tertiary']}; display:flex; align-items:center; justify-content:center; margin-bottom:8px; }}
.mcard .lbl {{ font-size:12px; color:{C['muted']}; margin-bottom:2px; }}
.mcard .val {{ font-size:24px; font-weight:700; letter-spacing:-.5px; }}
.mcard .unit {{ font-size:12px; color:{C['muted']}; font-weight:500; margin-left:4px; }}
.mstatus {{ margin-top:8px; display:inline-flex; align-items:center; gap:6px; padding:3px 8px; border-radius:999px; font-size:11px; font-weight:700; }}
.mstatus i {{ width:6px; height:6px; border-radius:3px; display:inline-block; }}

.empty {{ padding:24px; display:flex; flex-direction:column; align-items:center; gap:8px; background:{C['surface2']}; border-radius:12px; color:{C['muted']}; font-size:13px; text-align:center; }}
.empty .t {{ font-size:16px; font-weight:700; color:{C['on_surface']}; }}

.arow {{ display:flex; align-items:center; gap:12px; padding:12px; background:{C['surface2']}; border-radius:12px; margin-bottom:8px; }}
.arow .aw {{ width:40px; height:40px; border-radius:12px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }}
.arow .at {{ font-size:14px; font-weight:700; }}
.arow .as {{ font-size:12px; color:{C['muted']}; margin-top:2px; }}
.arow .dot {{ width:8px; height:8px; border-radius:4px; background:{C['error']}; margin-left:auto; }}

.page-title {{ font-size:26px; font-weight:700; letter-spacing:-.5px; margin:0; }}
.page-sub {{ font-size:15px; color:{C['muted']}; margin:4px 0 20px; }}

/* login */
.login-hero {{ position:relative; height:320px; border-radius:20px; overflow:hidden; margin-bottom:8px; }}
.logo-pill {{ position:absolute; top:28px; left:24px; display:inline-flex; align-items:center; gap:6px;
              background:{C['brand']}; color:#fff; padding:6px 12px; border-radius:999px; font-size:13px; font-weight:600; letter-spacing:.3px; }}
.login-title {{ font-size:26px; font-weight:700; letter-spacing:-.5px; margin-top:8px; }}
.login-sub {{ font-size:15px; color:{C['muted']}; line-height:22px; margin:8px 0 8px; }}
</style>
"""


def apply_theme() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


# ------------------------------------------------------------------
# Componentes
# ------------------------------------------------------------------
def page_header(title: str, subtitle: str = "") -> None:
    _html(f'<div class="page-title">{title}</div><div class="page-sub">{subtitle}</div>')


def section(title: str, hint: str = "", link: str = "") -> None:
    right = f'<span class="sec-hint">{hint}</span>' if hint else ""
    right = f'<span class="sec-link">{link}</span>' if link else right
    _html(f'<div class="sec-row"><span class="sec-title">{title}</span>{right}</div>')


def topbar(nome: str, unread: int) -> None:
    badge = f'<span class="badge">{unread}</span>' if unread > 0 else ""
    _html(
        f'<div class="topbar"><div><div class="hello">Olá,</div>'
        f'<div class="uname">{nome}</div></div>'
        f'<div class="bell">{icon("bell", 22)}{badge}</div></div>'
    )


def hero_card(titulo: str, subtitulo: str, healthy: bool, texto_status: str, atualizado: str = "") -> None:
    pill_bg = "rgba(216,230,222,.9)" if healthy else "rgba(200,76,49,.9)"
    pill_fg = C["brand"] if healthy else "#fff"
    ic = icon("check" if healthy else "warn", 14, pill_fg)
    _html(
        f'<div class="hero" style="background:url(\'{HERO_DASH}\') center/cover">'
        f'<div style="position:absolute;inset:0;background:linear-gradient(rgba(10,76,54,.55),rgba(10,76,54,.85))"></div>'
        f'<div class="hero-inner"><div class="hero-top">'
        f'<span class="pill" style="background:{pill_bg};color:{pill_fg}">{ic}{texto_status}</span>'
        f'<span class="hero-time">{atualizado}</span></div>'
        f'<div><div class="hero-title">{titulo}</div><div class="hero-sub">{subtitulo}</div></div>'
        f'</div></div>'
    )


def last_send(texto: str, device: str = "ESP32") -> None:
    _html(
        f'<div class="lastsend">{icon("clock", 18, C["primary"])}<div>'
        f'<div class="lbl">Último Envio de Telemetria</div><div class="val">{texto}</div></div>'
        f'<span class="devbadge">{device}</span></div>'
    )


def status_of(v, ideal):
    if v is None:
        return "—", C["muted"]
    if v < ideal[0]:
        return "Baixo", C["warning"]
    if v > ideal[1]:
        return "Alto", C["error"]
    return "Ideal", C["success"]


def metric_card(ic: str, tint: str, label: str, value, unit: str, ideal=None) -> None:
    val = f"{value:.1f}" if isinstance(value, (int, float)) else "—"
    status = ""
    if ideal is not None:
        txt, col = status_of(value if isinstance(value, (int, float)) else None, ideal)
        status = (
            f'<div class="mstatus" style="background:{col}22;color:{col}">'
            f'<i style="background:{col}"></i>{txt}</div>'
        )
    _html(
        f'<div class="mcard"><div class="iw">{icon(ic, 18, tint)}</div>'
        f'<div class="lbl">{label}</div>'
        f'<div><span class="val">{val}</span><span class="unit">{unit}</span></div>{status}</div>'
    )


def empty_state(ic: str, titulo: str, texto: str, color: str = None) -> None:
    color = color or C["primary"]
    t = f'<div class="t">{titulo}</div>' if titulo else ""
    _html(f'<div class="empty">{icon(ic, 36, color)}{t}<div>{texto}</div></div>')


def alert_row(titulo: str, sub: str, severity: str = "warning", unread: bool = False) -> None:
    col = C["error"] if severity == "error" else C["warning"]
    dot = '<span class="dot"></span>' if unread else ""
    _html(
        f'<div class="arow"><div class="aw" style="background:{col}22">{icon("alert", 20, col)}</div>'
        f'<div><div class="at">{titulo}</div><div class="as">{sub}</div></div>{dot}</div>'
    )


def login_hero() -> None:
    _html(
        f'<div class="login-hero" style="background:url(\'{HERO_LOGIN}\') center/cover">'
        f'<div style="position:absolute;inset:0;background:linear-gradient(rgba(10,76,54,.15),rgba(255,255,255,0),#fff)"></div>'
        f'<span class="logo-pill">{icon("leaf", 16, "#fff")}{APP_NAME}</span></div>'
        f'<div class="login-title">Bem-vindo à sua estufa</div>'
        f'<div class="login-sub">Monitore sua safra e receba alertas de doenças em tempo real.</div>'
    )