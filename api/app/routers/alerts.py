"""
Endpoints de alertas (RF07 da tese).

GET  /alerts                    -> lista alertas de uma estufa
POST /alerts/{alerta_id}/read   -> marca um alerta como lido
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alerta, Deteccao
from app.schemas import AlertaOut

router = APIRouter(prefix="/alerts", tags=["alertas"])


@router.get("", response_model=list[AlertaOut])
def list_alerts(estufa_id: int = 1, unread_only: bool = False, db: Session = Depends(get_db)):
    query = (
        db.query(Alerta, Deteccao.classe)
        .join(Deteccao, Alerta.deteccao_id == Deteccao.id)
        .filter(Deteccao.estufa_id == estufa_id)
    )
    if unread_only:
        query = query.filter(Alerta.lido.is_(False))

    resultados = query.order_by(desc(Alerta.enviado_em)).all()

    return [
        AlertaOut(
            id=alerta.id,
            deteccao_id=alerta.deteccao_id,
            classe=classe.value if hasattr(classe, "value") else classe,
            enviado_em=alerta.enviado_em,
            lido=alerta.lido,
        )
        for alerta, classe in resultados
    ]


@router.post("/{alerta_id}/read")
def mark_read(alerta_id: int, db: Session = Depends(get_db)):
    alerta = db.query(Alerta).filter(Alerta.id == alerta_id).first()
    if alerta is None:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    alerta.lido = True
    db.commit()
    return {"id": alerta_id, "lido": True}