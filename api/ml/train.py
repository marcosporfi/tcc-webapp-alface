""""
Treina o YOLOv11 em modo classificação nas 3 classes de doença da alface
(Seção 6.1.1 e 5.3.4 da tese). Requer que ml/prepare_dataset.py já tenha
sido rodado antes (gera a pasta ml/dataset/ com train/val/test).

Rodar com:
    python ml/train.py
"""
from pathlib import Path

from ultralytics import YOLO

DATASET_DIR = Path("ml/dataset")


def main():
    if not DATASET_DIR.exists():
        print(
            f"❌ Pasta '{DATASET_DIR}' não encontrada.\n"
            f"   Rode primeiro: python ml/prepare_dataset.py"
        )
        return

    model = YOLO("yolo11n-cls.pt")

    model.train(
        data=str(DATASET_DIR.resolve()),
        epochs=25,      # reduzido de 50 para 25
        imgsz=224,      # reduzido de 640 para 224 (padrão para classificação)
        patience=8,
        project="ml/runs/classify",
        name="train",
    )

    print(
        "\n✅ Treino concluído. O modelo final está em: "
        "ml/runs/classify/train/weights/best.pt"
    )


if __name__ == "__main__":
    main()