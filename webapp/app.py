from datetime import datetime

import streamlit as st
from api_client import login, logout, get_latest_reading, get_alerts
from theme import (
    apply_theme, topbar, hero_card, last_send, section, metric_card,
    empty_state, alert_row, icon, APP_NAME,
)


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🥬",
    layout="wide"
)


def _hora(iso):
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone().strftime("%H:%M")
    except Exception:
        return ""


def _data_completa(iso):
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone()
        return d.strftime("%d/%m/%Y às %H:%M:%S")
    except Exception:
        return "—"


def dashboard():
    with st.sidebar:
        _hdr = (
            '<div style="display:inline-flex;align-items:center;gap:6px;background:#0A4C36;'
            'color:#fff;padding:6px 12px;border-radius:999px;font-size:13px;font-weight:600">'
            f'{icon("leaf", 16, "#fff")}{APP_NAME}</div>'
        )
        st.markdown(_hdr, unsafe_allow_html=True)
        st.write("")

        estufa_id = st.number_input("ID da estufa", min_value=1, value=1, step=1)
        st.session_state["estufa_id"] = estufa_id

        st.divider()
        st.caption(f"Usuário: {st.session_state.get('usuario_email', '')}")

        if st.button("Sair", use_container_width=True):
            logout()
            st.rerun()

    leitura = get_latest_reading(estufa_id)
    nao_lidos = get_alerts(estufa_id, unread_only=True)
    n_unread = len(nao_lidos)
    saudavel = n_unread == 0

    email = st.session_state.get("usuario_email", "")
    nome = st.session_state.get("usuario_nome") or (email.split("@")[0].title() if email else "Produtor")

    topbar(nome, n_unread)

    hero_card(
        titulo=f"Estufa {estufa_id}",
        subtitulo=(
            "Todos os sensores dentro do ideal."
            if saudavel
            else "Detecções de doença requerem sua atenção."
        ),
        healthy=saudavel,
        texto_status="Safra Saudável" if saudavel else f"{n_unread} alerta{'s' if n_unread > 1 else ''}",
        atualizado=f"atualizado {_hora(leitura.get('registrado_em', ''))}",
    )

    section("Sensores")
    last_send(_data_completa(leitura.get("registrado_em", "")))

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("thermo", "#E85D3D", "Temperatura", leitura.get("temperatura"), "°C", (18, 25))
    with c2:
        metric_card("water", "#2E7CD6", "Umidade do Ar", leitura.get("umidade"), "%", (55, 75))
    with c3:
        metric_card("sun", "#D97706", "Luminosidade", leitura.get("luminosidade"), "lux")

    section("Alertas Recentes", link="Ver todos →")
    if nao_lidos.empty:
        empty_state("shield", "", "Sua estufa está segura.")
    else:
        for _, row in nao_lidos.sort_values("enviado_em", ascending=False).head(3).iterrows():
            alert_row(
                f"Patógeno {row['classe']}",
                row["enviado_em"].strftime("%d/%m/%Y %H:%M"),
                severity="error" if row["classe"] == "fungico" else "warning",
                unread=True,
            )


apply_theme()

if not st.session_state.get("token"):

    navigation = st.navigation(
        [
            st.Page(
                "login.py",
                title="Login",
                icon=":material/lock:"
            )
        ],
        position="hidden"
    )

else:

    navigation = st.navigation(
        {
            "Aplicativo": [
                st.Page(
                    dashboard,
                    title="Estufa",
                    icon=":material/eco:"
                ),
                st.Page(
                    "pages/1_Tempo_Real.py",
                    title="Tempo Real",
                    icon=":material/sensors:",
                    url_path="tempo-real"
                ),
                st.Page(
                    "pages/2_Deteccoes.py",
                    title="Detecções",
                    icon=":material/biotech:",
                    url_path="deteccoes"
                ),
                st.Page(
                    "pages/3_Historico.py",
                    title="Histórico",
                    icon=":material/show_chart:",
                    url_path="historico"
                ),
                st.Page(
                    "pages/4_Alertas.py",
                    title="Alertas",
                    icon=":material/notifications:",
                    url_path="alertas"
                )
            ]
        }
    )


navigation.run()