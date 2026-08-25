"""
Organiza o dataset do Kaggle (Lettuce plant Disease Dataset) no formato
que o YOLOv11 (modo classificação) exige:

    dataset/
    ├── train/
    │   ├── saudavel/*.jpg
    │   ├── bacteriano/*.jpg
    │   └── fungico/*.jpg
    ├── val/
    │   ├── saudavel/*.jpg
    │   ├── bacteriano/*.jpg
    │   └── fungico/*.jpg
    └── test/
        ├── saudavel/*.jpg
        ├── bacteriano/*.jpg
        └── fungico/*.jpg

Como baixar o dataset:
1. Acesse https://www.kaggle.com/datasets/santoshshaha/lettuce-plant-disease-dataset
2. Clique em "Download" (pode pedir login no Kaggle)
3. Extraia o .zip baixado
4. Ajuste RAW_DATASET_DIR abaixo para apontar para a pasta extraída

Este script assume que a pasta extraída já vem separada por classe
(bacterial/fungal/healthy ou nomes parecidos) e apenas: (a) renomeia as
classes para o padrão da tese (saudavel/bacteriano/fungico) e (b) faz a
divisão 70/15/15 (treino/validação/teste) definida na Seção 6.1.1.

Rodar com:
    python ml/prepare_dataset.py
"""
import random
import shutil
from pathlib import Path

random.seed(42)

# --- AJUSTE AQUI depois de baixar e extrair o dataset do Kaggle ---
RAW_DATASET_DIR = Path("ml/raw_dataset")
OUTPUT_DIR = Path("ml/dataset")

# Mapeia os nomes de pasta que podem vir no dataset original para o padrão
# da tese. Se o dataset baixado usar nomes diferentes, ajuste aqui.
CLASS_NAME_MAP = {
    "healthy": "saudavel",
    "bacterial": "bacteriano",
    "fungal": "fungico",
}

SPLIT_RATIOS = {"train": 0.70, "val": 0.15, "test": 0.15}


def main():
    if not RAW_DATASET_DIR.exists():
        print(
            f"❌ Pasta '{RAW_DATASET_DIR}' não encontrada.\n"
            f"   Baixe o dataset do Kaggle, extraia, e coloque (ou aponte "
            f"RAW_DATASET_DIR) para a pasta extraída."
        )
        return

    pastas_encontradas = [p for p in RAW_DATASET_DIR.iterdir() if p.is_dir()]
    print(f"Pastas de classe encontradas: {[p.name for p in pastas_encontradas]}")

    for pasta_classe in pastas_encontradas:
        nome_original = pasta_classe.name.lower()
        classe_padronizada = CLASS_NAME_MAP.get(nome_original)
        if classe_padronizada is None:
            print(
                f"⚠️  Pasta '{pasta_classe.name}' não reconhecida — "
                f"adicione o mapeamento em CLASS_NAME_MAP se for uma das 3 "
                f"classes (saudável/bacteriano/fúngico)."
            )
            continue

        imagens = list(pasta_classe.glob("*.*"))
        random.shuffle(imagens)

        n_total = len(imagens)
        n_train = int(n_total * SPLIT_RATIOS["train"])
        n_val = int(n_total * SPLIT_RATIOS["val"])

        splits = {
            "train": imagens[:n_train],
            "val": imagens[n_train:n_train + n_val],
            "test": imagens[n_train + n_val:],
        }

        for split_name, arquivos in splits.items():
            destino = OUTPUT_DIR / split_name / classe_padronizada
            destino.mkdir(parents=True, exist_ok=True)
            for arquivo in arquivos:
                shutil.copy2(arquivo, destino / arquivo.name)

        print(
            f"✅ {pasta_classe.name} -> {classe_padronizada}: "
            f"{n_train} treino / {n_val} validação / {n_total - n_train - n_val} teste"
        )

    print(f"\nDataset organizado em: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()