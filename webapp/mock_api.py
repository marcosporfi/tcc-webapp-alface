"""
Mock da API REST do sistema (ver Seção 6.2.6.3 e 6.2.6.7 do TCC).

Simula os endpoints que o back-end real (FastAPI/Python) vai expor:
  GET  /sensors/latest?estufa_id=1
  GET  /sensors/history?estufa_id=1&hours=24
  GET  /detections?estufa_id=1&limit=20
  GET  /alerts?estufa_id=1&unread_only=false
  POST /alerts/{alerta_id}/read

Isso permite desenvolver e testar o dashboard Streamlit sem depender do
back-end real estar pronto. Quando a API de verdade existir, só trocar a
BASE_URL no api_client.py — os formatos de resposta abaixo já seguem o
schema de banco definido na Seção 6.2.6.8 (tabelas leituras_sensores,
deteccoes, alertas).

Para rodar:
    uvicorn mock_api:app --reload --port 8000
"""
import random
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mock API - Estufa Inteligente")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CLASSES = ["saudavel", "bacteriano", "fungico"]
CLASS_WEIGHTS = [0.75, 0.13, 0.12]  # a maioria das leituras é planta saudável


def _fake_reading(ts: datetime) -> dict:
    return {
        "estufa_id": 1,
        "temperatura": round(random.uniform(18, 32), 1),
        "umidade": round(random.uniform(55, 90), 1),
        "luminosidade": random.randint(800, 3800),
        "registrado_em": ts.isoformat(),
    }


def _fake_detection(ts: datetime, i: int) -> dict:
    classe = random.choices(CLASSES, weights=CLASS_WEIGHTS)[0]
    return {
        "id": i,
        "estufa_id": 1,
        "classe": classe,
        "confianca": round(random.uniform(0.85, 0.99), 3),
        "bbox_x": round(random.uniform(0.2, 0.6), 4),
        "bbox_y": round(random.uniform(0.2, 0.6), 4),
        "bbox_w": round(random.uniform(0.15, 0.35), 4),
        "bbox_h": round(random.uniform(0.15, 0.35), 4),
        "imagem_url": f"https://picsum.photos/seed/leaf{i}/480/360",
        "detectado_em": ts.isoformat(),
    }


@app.get("/sensors/latest")
def sensors_latest(estufa_id: int = 1):
    return _fake_reading(datetime.now(timezone.utc))


@app.get("/sensors/history")
def sensors_history(estufa_id: int = 1, hours: int = 24):
    now = datetime.now(timezone.utc)
    n_points = max(1, (hours * 60) // 30)
    return [
        _fake_reading(now - timedelta(minutes=30 * i))
        for i in range(n_points)
    ][::-1]


@app.get("/detections")
def detections(estufa_id: int = 1, limit: int = 20):
    now = datetime.now(timezone.utc)
    return [
        _fake_detection(now - timedelta(minutes=45 * i), i)
        for i in range(limit)
    ]


@app.get("/alerts")
def alerts(estufa_id: int = 1, unread_only: bool = False):
    now = datetime.now(timezone.utc)
    items = []
    for i in range(8):
        classe = random.choices(["bacteriano", "fungico"], weights=[0.5, 0.5])[0]
        lido = i % 3 == 0
        if unread_only and lido:
            continue
        items.append({
            "id": i,
            "deteccao_id": i,
            "classe": classe,
            "enviado_em": (now - timedelta(hours=2 * i)).isoformat(),
            "lido": lido,
        })
    return items


@app.post("/alerts/{alerta_id}/read")
def mark_alert_read(alerta_id: int):
    if alerta_id < 0:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    return {"id": alerta_id, "lido": True}