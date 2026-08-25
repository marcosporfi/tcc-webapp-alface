"""
Configurações centrais da API. Lê o arquivo .env (que você cria a partir
do .env.example) para não deixar a senha do banco escrita direto no código.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/estufa_db",
)

# Caminho do modelo YOLOv11 treinado (gerado pelo ml/train.py).
# Antes de treinar, esse arquivo não existe — o endpoint de análise avisa
# isso com uma mensagem clara em vez de quebrar.
YOLO_MODEL_PATH = BASE_DIR / "ml" / "runs" / "classify" / "train" / "weights" / "best.pt"

# Onde as imagens enviadas para análise são salvas
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)