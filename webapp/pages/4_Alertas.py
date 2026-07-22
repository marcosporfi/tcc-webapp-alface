import streamlit as st

from api_client import get_alerts, mark_alert_read

st.set_page_config(page_title="Alertas", page_icon="🔔", layout="wide")
st.title("🔔 Log de Alertas Fitossanitários")

estufa_id = st.session_state.get("estufa_id", 1)

so_nao_lidos = st.checkbox("Mostrar apenas não lidos", value=False)
df = get_alerts(estufa_id, unread_only=so_nao_lidos)

if df.empty:
    st.success("Nenhum alerta pendente. 🎉")
else:
    for _, row in df.sort_values("enviado_em", ascending=False).iterrows():
        icone = "🔴" if row["classe"] == "fungico" else "🟠"
        status = "✅ lido" if row["lido"] else "🆕 não lido"
        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(
                f"{icone} **Patógeno {row['classe']}** detectado — "
                f"{row['enviado_em'].strftime('%d/%m/%Y %H:%M')} ({status})"
            )
        with c2:
            if not row["lido"]:
                if st.button("Marcar lido", key=f"read_{row['id']}"):
                    mark_alert_read(int(row["id"]))
                    st.rerun()
        st.divider()