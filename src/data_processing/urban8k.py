import os
import pandas as pd
import librosa
import soundfile as sf
import numpy as np
from tqdm import tqdm

def preprocess_urbansound(csv_path, source_dir, output_dir, output_csv_path, target_sr=22050, target_duration=4.0):
    # Създаване на основната изходна папка, ако не съществува
    os.makedirs(output_dir, exist_ok=True)
    
    # Четене на оригиналния CSV
    df = pd.read_csv(csv_path)
    
    # Изчисляване на необходимия брой семпли (4 секунди * sample_rate)
    target_samples = int(target_sr * target_duration)
    
    processed_records = []

    print("Започва обработка на аудио файловете...")
    for index, row in tqdm(df.iterrows(), total=len(df)):
        file_name = row['slice_file_name']
        fold = row['fold']
        class_id = row['classID']
        class_name = row['class']
        
        # Път до оригиналния файл (UrbanSound8K организира оригиналите по папки fold1, fold2...)
        source_path = os.path.join(source_dir, f"fold{fold}", file_name)
        
        # Проверка дали файлът съществува
        if not os.path.exists(source_path):
            continue
            
        try:
            # Зареждане на аудиото (ако е стерео, librosa автоматично го прави моно; ресемплира до target_sr)
            audio, sr = librosa.load(source_path, sr=target_sr)
            
            # Стандартизиране до точно 4.0 секунди
            if len(audio) > target_samples:
                # Изрязване, ако е по-дълго
                audio = audio[:target_samples]
            elif len(audio) < target_samples:
                # Допълване с нули (zero-padding), ако е по-късо
                padding = target_samples - len(audio)
                audio = np.pad(audio, (0, padding), mode='constant')
                
            # Запазване в новата папка (без подпапки за фолдове, за по-лесно, или с тях - тук е обща папка)
            output_file_path = os.path.join(output_dir, file_name)
            sf.write(output_file_path, audio, target_sr)
            
            # Добавяне на обновения запис в списъка
            processed_records.append({
                'slice_file_name': file_name,
                'classID': class_id,
                'class': class_name,
                'fold': fold,
                'processed_path': output_file_path
            })
            
        except Exception as e:
            print(f"Грешка при обработка на {file_name}: {e}")
            
    # Генериране на нов CSV файл с обновените пътища
    new_df = pd.DataFrame(processed_records)
    new_df.to_csv(output_csv_path, index=False)
    print(f"Обработката завърши! Новият CSV е запазен в: {output_csv_path}")

def split_data_by_folds(csv_path):
    df = pd.read_csv(csv_path)
    
    # Train: 60% (Folds 1 до 6 включително)
    train_df = df[df['fold'].isin([1, 2, 3, 4, 5, 6])]
    
    # Validation: 20% (Folds 7 и 8)
    val_df = df[df['fold'].isin([7, 8])]
    
    # Test: 20% (Folds 9 и 10)
    test_df = df[df['fold'].isin([9, 10])]
    
    # Запазваме ги като отделни CSV файлове за лесно подаване към Dataset класа
    train_df.to_csv('data/train_split.csv', index=False)
    val_df.to_csv('data/val_split.csv', index=False)
    test_df.to_csv('data/test_split.csv', index=False)
    
    print(f"Train: {len(train_df)} записа, Val: {len(val_df)} записа, Test: {len(test_df)} записа")

# Пример за стартиране
if __name__ == "__main__":
    processed_csv = "data/urbansound_processed.csv"
    preprocess_urbansound(
        csv_path="data/raw/Urban8k/UrbanSound8K.csv",            # Път до оригиналния CSV
        source_dir="data/raw/Urban8k",                           # Папка с оригиналните фолдове
        output_dir="data/processed_audio",                       # Нова папка за стандартизираните файлове
        output_csv_path=processed_csv                            # Път за новия CSV
    )
    
    print("\nРазделяне на данните по folds...")
    split_data_by_folds(processed_csv)
