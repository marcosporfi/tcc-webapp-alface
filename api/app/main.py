"""
Ponto de entrada da API. Para rodar:
    uvicorn app.main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, SessionLocal, engine
from app.models import Estufa
from app.routers import alerts, detections, sensors

# Cria as tabelas no banco automaticamente se ainda não existirem
# (equivalente a rodar as migrações na primeira vez)
Base.metadata.create_all(bind=engine)


def seed_estufa_padrao():
    """
    Garante que exista uma estufa com id=1 assim que a API sobe — sem
    isso, qualquer insert de leitura/detecção falha com erro de chave
    estrangeira (a leitura precisa apontar para uma estufa que existe).
    """
    db = SessionLocal()
    try:
        if db.query(Estufa).count() == 0:
            db.add(Estufa(nome="Estufa Principal", localizacao="Protótipo TCC"))
            db.commit()
    finally:
        db.close()


seed_estufa_padrao()

app = FastAPI(title="API - Estufa Inteligente (Detecção de Doenças em Alface)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensors.router)
app.include_router(detections.router)
app.include_router(alerts.router)


@app.get("/")
def raiz():
    return {"status": "ok", "mensagem": "API da Estufa Inteligente no ar"}