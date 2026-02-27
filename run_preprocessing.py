import os
import sys

# Добавяме текущата директория към пътя, за да може Python да види пакета 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.data_processing.audio_processor import preprocess_urbansound
from src.data_processing.splitting import split_data_by_folds

def main():
    # Настройки на пътищата (коригирай ги, ако е необходимо)
    raw_csv = "data/raw/Urban8K/UrbanSound8K.csv"
    raw_audio_dir = "data/raw/Urban8K" # Папката, съдържаща fold1, fold2...
    processed_dir = "data/processed_audio"
    processed_csv = "data/processed_audio_metadata.csv"

    # 1. Обработка на аудиото (ресемплиране и уеднаквяване на дължината)
    print("Стартиране на аудио обработката...")
    preprocess_urbansound(
        csv_path=raw_csv,
        source_dir=raw_audio_dir,
        output_dir=processed_dir,
        output_csv_path=processed_csv,
        target_sr=22050,    #
        target_duration=4.0 #
    )

    # 2. Разделяне на данните на Train, Val и Test
    print("\nРазделяне на данните по фолдове...")
    split_data_by_folds(
        csv_path=processed_csv,
        output_dir="data" #
    )

    print("\nВсички данни са подготвени успешно!")

if __name__ == "__main__":
    main()