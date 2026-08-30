import streamlit as st
from api_client import login, logout, get_latest_reading


st.set_page_config(
    page_title="Estufa Inteligente",
    page_icon="🥬",
    layout="wide"
)


def dashboard():
    with st.sidebar:
        st.title("🥬 Estufa Inteligente")
        st.divider()

        st.header("Estufa")

        estufa_id = st.number_input(
            "ID da estufa",
            min_value=1,
            value=1,
            step=1
        )

        st.session_state["estufa_id"] = estufa_id

        st.divider()

        st.caption(
            f"Usuário: {st.session_state.get('usuario_email', '')}"
        )

        if st.button("🚪 Sair", use_container_width=True):
            logout()
            st.rerun()

    st.title("🥬 Estufa Inteligente")

    st.caption(
        "Monitoramento da estufa e detecção precoce de doenças "
        "foliares em alface utilizando IoT e YOLOv11."
    )

    st.divider()

    leitura = get_latest_reading(estufa_id)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🌡️ Temperatura",
            f"{leitura['temperatura']} °C"
        )

    with col2:
        st.metric(
            "💧 Umidade",
            f"{leitura['umidade']} %"
        )

    with col3:
        st.metric(
            "☀️ Luminosidade",
            f"{leitura['luminosidade']}"
        )

    st.divider()

    st.subheader("📊 Status da Estufa")

    col4, col5 = st.columns(2)

    with col4:
        st.info(
            "📡 Sensores conectados\n\n"
            "Os dados estão sendo obtidos pela API da estufa."
        )

    with col5:
        st.success(
            "🤖 Sistema de monitoramento ativo\n\n"
            "A detecção de doenças utiliza o modelo YOLOv11."
        )


if not st.session_state.get("token"):

    navigation = st.navigation(
        [
            st.Page(
                "login.py",
                title="Login",
                icon="🔐"
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
                    title="Dashboard",
                    icon="🏠"
                ),
                st.Page(
                    "pages/1_Tempo_Real.py",
                    title="Tempo Real",
                    icon="📡"
                ),
                st.Page(
                    "pages/2_Deteccoes.py",
                    title="Detecções",
                    icon="🔬"
                ),
                st.Page(
                    "pages/3_Historico.py",
                    title="Histórico",
                    icon="📈"
                ),
                st.Page(
                    "pages/4_Alertas.py",
                    title="Alertas",
                    icon="🔔"
                )
            ]
        }
    )


navigation.run()