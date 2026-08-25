"""
Endpoints de sensores (RF04, RF05, RF08 da tese).

GET  /sensors/latest         -> última leitura de uma estufa
GET  /sensors/history        -> histórico de leituras (com filtro por horas)
POST /sensors/readings       -> registra uma nova leitura (usado pelo firmware
                                 do ESP32 via MQTT->HTTP bridge, ou para testes manuais)
"""
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import LeituraSensor
from app.schemas import LeituraSensorIn, LeituraSensorOut

router = APIRouter(prefix="/sensors", tags=["sensores"])


@router.get("/latest", response_model=LeituraSensorOut)
def get_latest(estufa_id: int = 1, db: Session = Depends(get_db)):
    leitura = (
        db.query(LeituraSensor)
        .filter(LeituraSensor.estufa_id == estufa_id)
        .order_by(desc(LeituraSensor.registrado_em))
        .first()
    )
    if leitura is None:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma leitura encontrada para esta estufa ainda. "
            "Envie uma leitura de teste via POST /sensors/readings.",
        )
    return leitura


@router.get("/history", response_model=list[LeituraSensorOut])
def get_history(estufa_id: int = 1, hours: int = 24, db: Session = Depends(get_db)):
    desde = datetime.now(timezone.utc) - timedelta(hours=hours)
    leituras = (
        db.query(LeituraSensor)
        .filter(
            LeituraSensor.estufa_id == estufa_id,
            LeituraSensor.registrado_em >= desde,
        )
        .order_by(LeituraSensor.registrado_em)
        .all()
    )
    return leituras


@router.post("/readings", response_model=LeituraSensorOut, status_code=201)
def create_reading(leitura: LeituraSensorIn, db: Session = Depends(get_db)):
    # Validação básica de faixa física, igual definido na Seção 6.1.2 da tese
    if not (-10 <= leitura.temperatura <= 70):
        raise HTTPException(400, "Temperatura fora da faixa física esperada.")
    if not (0 <= leitura.umidade <= 100):
        raise HTTPException(400, "Umidade fora da faixa esperada (0-100%).")

    nova = LeituraSensor(**leitura.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova