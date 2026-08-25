import streamlit as st

from api_client import get_latest_reading

st.set_page_config(
    page_title="Estufa Inteligente — Dashboard",
    page_icon="🥬",
    layout="wide",
)

st.title("🥬 Estufa Inteligente — Monitoramento")
st.caption(
    "Detecção precoce de doenças foliares em alface (Xanthomonas / Bremia) "
    "com visão computacional (YOLOv11) e sensores IoT."
)

with st.sidebar:
    st.header("Estufa")
    estufa_id = st.number_input("ID da estufa", min_value=1, value=1, step=1)
    st.session_state["estufa_id"] = estufa_id
    st.divider()
    st.caption("Use o menu acima para navegar entre as páginas: "
               "Tempo Real, Detecções, Histórico e Alertas.")

leitura = get_latest_reading(estufa_id)

col1, col2, col3 = st.columns(3)
col1.metric("🌡️ Temperatura", f"{leitura['temperatura']} °C")
col2.metric("💧 Umidade", f"{leitura['umidade']} %")
col3.metric("☀️ Luminosidade", f"{leitura['luminosidade']}")

st.info(
    "Este painel se conecta à API definida em `API_BASE_URL` "
    "(atualmente configurada para o back-end real, quando disponível, "
    "ou para a API mock local durante o desenvolvimento)."
)