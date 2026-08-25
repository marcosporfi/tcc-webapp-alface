"""
Carrega o modelo YOLOv11 treinado (ml/train.py gera esse arquivo) e roda
classificação numa imagem. Separado da API pra deixar claro o que é "parte
de ML" e o que é "parte de API" — mais fácil de testar cada um sozinho.
"""
from pathlib import Path

from app.config import YOLO_MODEL_PATH

_model = None  # carregado sob demanda (lazy) para a API subir rápido


def _get_model():
    global _model
    if _model is None:
        if not Path(YOLO_MODEL_PATH).exists():
            raise FileNotFoundError(
                f"Modelo treinado não encontrado em {YOLO_MODEL_PATH}. "
                "Rode `python ml/train.py` primeiro para treinar o modelo."
            )
        from ultralytics import YOLO  # import tardio: só precisa quando for usar

        _model = YOLO(str(YOLO_MODEL_PATH))
    return _model


def classificar_imagem(caminho_imagem: str) -> dict:
    """
    Roda o modelo treinado numa imagem e devolve a classe prevista e a
    confiança. Formato de saída pensado para bater com a tabela `deteccoes`.
    """
    model = _get_model()
    resultado = model(caminho_imagem, verbose=False)[0]

    top1_idx = resultado.probs.top1
    confianca = float(resultado.probs.top1conf)
    classe = resultado.names[top1_idx]

    return {"classe": classe, "confianca": round(confianca, 3)}