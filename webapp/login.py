import streamlit as st
from api_client import login


st.title("🥬 Estufa Inteligente")
st.subheader("🔐 Login")

st.write("Entre com sua conta para acessar o sistema.")

with st.form("form_login"):

    email = st.text_input(
        "E-mail",
        placeholder="Digite seu e-mail"
    )

    senha = st.text_input(
        "Senha",
        type="password",
        placeholder="Digite sua senha"
    )

    entrar = st.form_submit_button(
        "🔐 Entrar",
        use_container_width=True
    )

    if entrar:

        if not email or not senha:
            st.warning("Preencha o e-mail e a senha.")

        else:

            dados = login(email, senha)

            if dados:
                st.session_state["usuario_email"] = email
                st.rerun()