"""
Endpoints de detecção (RF01, RF02, RF06, RF07 da tese).

POST /detections/analyze   -> recebe uma imagem, roda o YOLOv11 e salva o resultado
GET  /detections           -> lista as últimas detecções de uma estufa
"""
import shutil
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.config import UPLOADS_DIR
from app.database import get_db
from app.models import Alerta, Deteccao
from app.schemas import DeteccaoOut

router = APIRouter(prefix="/detections", tags=["deteccoes"])


@router.post("/analyze", response_model=DeteccaoOut, status_code=201)
def analyze_image(
    estufa_id: int = 1,
    imagem: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Salva a imagem recebida (do ESP32-CAM ou de um upload manual de teste)
    extensao = imagem.filename.split(".")[-1] if "." in imagem.filename else "jpg"
    nome_arquivo = f"{uuid.uuid4()}.{extensao}"
    caminho = UPLOADS_DIR / nome_arquivo
    with open(caminho, "wb") as f:
        shutil.copyfileobj(imagem.file, f)

    # Import tardio: só carrega o modelo se essa rota for realmente chamada
    from ml.infer import classificar_imagem

    try:
        resultado = classificar_imagem(str(caminho))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    deteccao = Deteccao(
        estufa_id=estufa_id,
        classe=resultado["classe"],
        confianca=resultado["confianca"],
        imagem_url=str(caminho),
    )
    db.add(deteccao)
    db.commit()
    db.refresh(deteccao)

    # RF07: dispara alerta automaticamente quando não for "saudável"
    if resultado["classe"] != "saudavel":
        alerta = Alerta(deteccao_id=deteccao.id, usuario_id=None, lido=False)
        db.add(alerta)
        db.commit()

    return deteccao


@router.get("", response_model=list[DeteccaoOut])
def list_detections(estufa_id: int = 1, limit: int = 20, db: Session = Depends(get_db)):
    deteccoes = (
        db.query(Deteccao)
        .filter(Deteccao.estufa_id == estufa_id)
        .order_by(desc(Deteccao.detectado_em))
        .limit(limit)
        .all()
    )
    return deteccoes