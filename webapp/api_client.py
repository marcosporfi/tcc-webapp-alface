"""
Cliente HTTP para a API do back-end (RF06, RF08 e Seção 6.2.6.7).

Centraliza todas as chamadas à API aqui — assim, quando o endpoint real
do back-end mudar de formato, só se ajusta este arquivo, sem mexer nas
páginas do Streamlit.

Troque BASE_URL para apontar para o back-end real quando ele estiver
pronto (ex: variável de ambiente ou st.secrets["api_base_url"]).
"""
import os
from typing import Any

import pandas as pd
import requests
import streamlit as st

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")
TIMEOUT = 5  # segundos


def _get(path: str, params: dict | None = None) -> Any:
    try:
        resp = requests.get(f"{BASE_URL}{path}", params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as exc:
        st.error(
            f"Não foi possível falar com a API em `{BASE_URL}{path}`.\n\n"
            f"Detalhe: {exc}\n\n"
            "Se estiver testando localmente, confira se o mock está rodando: "
            "`uvicorn mock_api:app --reload --port 8000`"
        )
        st.stop()


def get_latest_reading(estufa_id: int = 1) -> dict:
    return _get("/sensors/latest", {"estufa_id": estufa_id})


def get_sensor_history(estufa_id: int = 1, hours: int = 24) -> pd.DataFrame:
    data = _get("/sensors/history", {"estufa_id": estufa_id, "hours": hours})
    df = pd.DataFrame(data)
    if not df.empty:
        df["registrado_em"] = pd.to_datetime(df["registrado_em"])
    return df


def get_detections(estufa_id: int = 1, limit: int = 20) -> pd.DataFrame:
    data = _get("/detections", {"estufa_id": estufa_id, "limit": limit})
    df = pd.DataFrame(data)
    if not df.empty:
        df["detectado_em"] = pd.to_datetime(df["detectado_em"])
    return df


def get_alerts(estufa_id: int = 1, unread_only: bool = False) -> pd.DataFrame:
    data = _get("/alerts", {"estufa_id": estufa_id, "unread_only": unread_only})
    df = pd.DataFrame(data)
    if not df.empty:
        df["enviado_em"] = pd.to_datetime(df["enviado_em"])
    return df


def mark_alert_read(alerta_id: int) -> None:
    try:
        requests.post(f"{BASE_URL}/alerts/{alerta_id}/read", timeout=TIMEOUT)
    except requests.exceptions.RequestException as exc:
        st.warning(f"Não consegui marcar o alerta como lido: {exc}")