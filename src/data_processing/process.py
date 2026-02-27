import os
import pandas as pd
from src.data_processing.audio_processor import preprocess_urbansound
from src.data_processing.splitting import split_data_by_folds
from src.data.urbansound_dataset import UrbanSoundDataset
from torch.utils.data import DataLoader

# --- КОНФИГУРАЦИЯ НА ПЪТИЩАТА ---
RAW_CSV = "data/raw/Urban8K/UrbanSound8K.csv"
RAW_AUDIO_DIR = "data/raw/Urban8K"  # Тук се очаква да са fold1, fold2...
PROCESSED_DIR = "data/processed_audio"
PROCESSED_CSV = "data/processed_audio_metadata.csv"
OUTPUT_SPLIT_DIR = "data"


def main():
    # 1. ПРЕДВАРИТЕЛНА ОБРАБОТКА (Resampling & Padding/Trimming)
    # Този процес създава нови .wav файлове с еднаква дължина (4.0 сек)
    print("--- Стъпка 1: Обработка на аудио файловете ---")
    if not os.path.exists(PROCESSED_DIR):
        preprocess_urbansound(
            csv_path=RAW_CSV,
            source_dir=RAW_AUDIO_DIR,
            output_dir=PROCESSED_DIR,
            output_csv_path=PROCESSED_CSV
        )
    else:
        print(f"Папката {PROCESSED_DIR} вече съществува. Пропускане...")

    # 2. РАЗДЕЛЯНЕ НА ДАННИТЕ (Train/Val/Test)
    # Използва логиката от splitting.py базирана на fold-овете
    print("\n--- Стъпка 2: Разделяне на данните по fold-ове ---")
    split_data_by_folds(PROCESSED_CSV, output_dir=OUTPUT_SPLIT_DIR)

    # 3. ТЕСТ НА DATASET КЛАСА
    # Проверка дали всичко се зарежда правилно като Mel-спектрограми
    print("\n--- Стъпка 3: Тестване на UrbanSoundDataset ---")
    try:
        train_dataset = UrbanSoundDataset(
            csv_file=os.path.join(OUTPUT_SPLIT_DIR, "train_split.csv"),
            audio_dir=PROCESSED_DIR
        )

        # Създаваме прост DataLoader, за да видим дали вади тензори
        train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)

        # Вземаме една мостра
        features, labels = next(iter(train_loader))

        print(f"Успешно зареден batch!")
        print(f"Форма на тензора (Batch, Channel, Mels, Time): {features.shape}")
        print(f"Етикети: {labels}")

    except Exception as e:
        print(f"Грешка при тестване на Dataset: {e}")


if __name__ == "__main__":
    main()