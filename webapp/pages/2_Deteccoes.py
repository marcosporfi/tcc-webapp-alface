import streamlit as st

from api_client import get_detections

st.set_page_config(page_title="Detecções", page_icon="🔬", layout="wide")
st.title("🔬 Últimas Detecções")

estufa_id = st.session_state.get("estufa_id", 1)

CLASSE_LABEL = {
    "saudavel": "🟢 Saudável",
    "bacteriano": "🟠 Bacteriano (Xanthomonas)",
    "fungico": "🔴 Fúngico (Bremia)",
}

col_filtro, col_limite = st.columns([2, 1])
filtro_classe = col_filtro.multiselect(
    "Filtrar por classe", options=list(CLASSE_LABEL.keys()),
    format_func=lambda c: CLASSE_LABEL[c],
)
limite = col_limite.slider("Quantidade", 4, 40, 12, step=4)

df = get_detections(estufa_id, limit=limite)

if df.empty:
    st.info("Nenhuma detecção registrada ainda.")
else:
    if filtro_classe:
        df = df[df["classe"].isin(filtro_classe)]

    st.caption(f"{len(df)} detecção(ões) exibida(s).")

    cols = st.columns(4)
    for i, row in df.iterrows():
        col = cols[i % 4]
        with col:
            st.image(row["imagem_url"], use_container_width=True)
            st.markdown(f"**{CLASSE_LABEL.get(row['classe'], row['classe'])}**")
            st.caption(
                f"Confiança: {row['confianca']:.0%}  \n"
                f"{row['detectado_em'].strftime('%d/%m/%Y %H:%M')}"
            )
            st.divider()

    with st.expander("Ver dados brutos (tabela)"):
        st.dataframe(df, use_container_width=True)