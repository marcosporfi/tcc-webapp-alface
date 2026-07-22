import streamlit as st

from api_client import get_sensor_history

st.set_page_config(page_title="Histórico", page_icon="📈", layout="wide")
st.title("📈 Histórico Climático")

estufa_id = st.session_state.get("estufa_id", 1)

periodo = st.select_slider(
    "Período",
    options=["6h", "12h", "24h", "48h", "7 dias"],
    value="24h",
)
horas_map = {"6h": 6, "12h": 12, "24h": 24, "48h": 48, "7 dias": 168}

df = get_sensor_history(estufa_id, hours=horas_map[periodo])

if df.empty:
    st.warning("Sem dados para o período selecionado.")
else:
    tab1, tab2, tab3 = st.tabs(["Temperatura", "Umidade", "Luminosidade"])
    with tab1:
        st.line_chart(df.set_index("registrado_em")["temperatura"])
    with tab2:
        st.line_chart(df.set_index("registrado_em")["umidade"])
    with tab3:
        st.line_chart(df.set_index("registrado_em")["luminosidade"])

    st.subheader("Resumo do período")
    c1, c2, c3 = st.columns(3)
    c1.metric("Temp. média", f"{df['temperatura'].mean():.1f} °C")
    c2.metric("Umid. média", f"{df['umidade'].mean():.1f} %")
    c3.metric("Luminosidade média", f"{df['luminosidade'].mean():.0f}")

    # RF10: exportação de relatório (CSV aqui; PDF pode vir depois, é
    # prioridade "Baixa" no requisito, então deixei o essencial primeiro)
    st.download_button(
        "⬇️ Baixar CSV do período",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"historico_estufa{estufa_id}_{periodo}.csv",
        mime="text/csv",
    )

    with st.expander("Ver dados brutos (tabela)"):
        st.dataframe(df, use_container_width=True)