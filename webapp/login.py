import streamlit as st

from api_client import login
from theme import login_hero

_, centro, _ = st.columns([1, 2.2, 1])

with centro:
    login_hero()

    with st.form("form_login"):
        email = st.text_input("E-mail", placeholder="voce@exemplo.com")
        senha = st.text_input("Senha", type="password", placeholder="Sua senha")
        entrar = st.form_submit_button("Entrar", use_container_width=True)

        if entrar:
            if not email or not senha:
                st.warning("Preencha e-mail e senha")
            else:
                dados = login(email.strip(), senha)
                if dados:
                    st.session_state["usuario_email"] = email.strip()
                    st.rerun()