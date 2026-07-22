import plotly.graph_objects as go
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from api_client import get_sensor_history

st.set_page_config(page_title="Tempo Real", page_icon="📡", layout="wide")
st.title("📡 Monitoramento em Tempo Real")

estufa_id = st.session_state.get("estufa_id", 1)

# RF06: exibir dados dos sensores em tempo real no dashboard.
# Streamlit não mantém socket aberto como o React (WebSocket citado na
# Seção 6.2.6.7); a alternativa prática aqui é reconsultar a API em
# intervalo curto — para RF06 isso já atende ("tempo real" percebido).
refresh_seconds = st.sidebar.slider("Atualizar a cada (segundos)", 5, 60, 30)
st_autorefresh(interval=refresh_seconds * 1000, key="auto_refresh_tempo_real")

df = get_sensor_history(estufa_id, hours=3)

if df.empty:
    st.warning("Sem leituras recentes para esta estufa.")
else:
    ultima = df.iloc[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("Temperatura", f"{ultima['temperatura']} °C")
    c2.metric("Umidade", f"{ultima['umidade']} %")
    c3.metric("Luminosidade", f"{ultima['luminosidade']}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["registrado_em"], y=df["temperatura"],
        name="Temperatura (°C)", mode="lines+markers",
    ))
    fig.add_trace(go.Scatter(
        x=df["registrado_em"], y=df["umidade"],
        name="Umidade (%)", mode="lines+markers", yaxis="y2",
    ))
    fig.update_layout(
        yaxis=dict(title="Temperatura (°C)"),
        yaxis2=dict(title="Umidade (%)", overlaying="y", side="right"),
        legend=dict(orientation="h", y=1.1),
        height=420,
        margin=dict(l=10, r=10, t=30, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.line_chart(df.set_index("registrado_em")["luminosidade"])