
"""
Cliente HTTP para a API do back-end.

Centraliza todas as chamadas à API do projeto.
Inclui autenticação por JWT e configuração da URL
para execução local ou hospedada no Streamlit Cloud.
"""

import os
from typing import Any

import pandas as pd
import requests
import streamlit as st


# Usa a configuração do Streamlit Secrets quando disponível.
# Caso contrário, usa a variável de ambiente ou a URL online.
try:
    _secret_url = st.secrets.get("API_BASE_URL", "")
except Exception:
    _secret_url = ""

BASE_URL = (
    _secret_url
    or os.environ.get("API_BASE_URL")
    or "https://tcc-webapp-alface.onrender.com"
).rstrip("/")

TIMEOUT = 60


# ============================================================
# AUTENTICAÇÃO
# ============================================================

def login(email: str, senha: str) -> dict | None:
    """Faz login na API e salva o token na sessão do Streamlit."""

    try:
        resp = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": email,
                "senha": senha,
            },
            timeout=TIMEOUT,
        )

        if resp.status_code == 401:
            st.error("❌ E-mail ou senha incorretos.")
            return None

        resp.raise_for_status()
        dados = resp.json()

        token = dados.get("access_token")
        if not token:
            st.error("A API não retornou o token de autenticação.")
            return None

        st.session_state["token"] = token
        return dados

    except requests.exceptions.Timeout:
        st.error(
            "A API demorou para responder. "
            "Tente novamente em alguns instantes."
        )
        return None

    except requests.exceptions.RequestException as exc:
        st.error(
            f"Não foi possível conectar à API em `{BASE_URL}`.\n\n"
            f"Detalhe: {exc}"
        )
        return None


def logout() -> None:
    """Remove os dados de autenticação da sessão."""

    st.session_state.pop("token", None)
    st.session_state.pop("usuario_nome", None)
    st.session_state.pop("estufa_id", None)


def _headers() -> dict:
    """Retorna o cabeçalho de autenticação."""

    token = st.session_state.get("token")

    if not token:
        return {}

    return {"Authorization": f"Bearer {token}"}


# ============================================================
# REQUISIÇÕES GET
# ============================================================

def _get(path: str, params: dict | None = None) -> Any:
    """Executa uma requisição GET autenticada."""

    try:
        resp = requests.get(
            f"{BASE_URL}{path}",
            params=params,
            headers=_headers(),
            timeout=TIMEOUT,
        )

        if resp.status_code == 401:
            logout()
            st.error("🔐 Sua sessão expirou. Faça login novamente.")
            st.stop()

        resp.raise_for_status()
        return resp.json()

    except requests.exceptions.Timeout:
        st.error("A API demorou para responder. Tente novamente.")
        st.stop()

    except requests.exceptions.RequestException as exc:
        st.error(
            f"Não foi possível falar com a API em "
            f"`{BASE_URL}{path}`.\n\nDetalhe: {exc}"
        )
        st.stop()


# ============================================================
# SENSORES
# ============================================================

def get_latest_reading(estufa_id: int = 1) -> dict:
    return _get(
        "/sensors/latest",
        {"estufa_id": estufa_id},
    )


def get_sensor_history(
    estufa_id: int = 1,
    hours: int = 24,
) -> pd.DataFrame:
    data = _get(
        "/sensors/history",
        {
            "estufa_id": estufa_id,
            "hours": hours,
        },
    )

    df = pd.DataFrame(data)

    if not df.empty and "registrado_em" in df.columns:
        df["registrado_em"] = pd.to_datetime(
            df["registrado_em"],
            errors="coerce",
        )

    return df


# ============================================================
# DETECÇÕES
# ============================================================

def get_detections(
    estufa_id: int = 1,
    limit: int = 20,
) -> pd.DataFrame:
    data = _get(
        "/detections",
        {
            "estufa_id": estufa_id,
            "limit": limit,
        },
    )

    df = pd.DataFrame(data)

    if not df.empty and "detectado_em" in df.columns:
        df["detectado_em"] = pd.to_datetime(
            df["detectado_em"],
            errors="coerce",
        )

    return df


# ============================================================
# ALERTAS
# ============================================================

def get_alerts(
    estufa_id: int = 1,
    unread_only: bool = False,
) -> pd.DataFrame:
    data = _get(
        "/alerts",
        {
            "estufa_id": estufa_id,
            "unread_only": unread_only,
        },
    )

    df = pd.DataFrame(data)

    if not df.empty and "enviado_em" in df.columns:
        df["enviado_em"] = pd.to_datetime(
            df["enviado_em"],
            errors="coerce",
        )

    return df


def mark_alert_read(alerta_id: int) -> None:
    """Marca um alerta como lido."""

    try:
        resp = requests.post(
            f"{BASE_URL}/alerts/{alerta_id}/read",
            headers=_headers(),
            timeout=TIMEOUT,
        )

        if resp.status_code == 401:
            logout()
            st.error("🔐 Sua sessão expirou. Faça login novamente.")
            st.stop()

        resp.raise_for_status()

    except requests.exceptions.Timeout:
        st.warning("A API demorou para responder. Tente novamente.")

    except requests.exceptions.RequestException as exc:
        st.warning(f"Não consegui marcar o alerta como lido: {exc}")
