import os
import pandas as pd
import librosa
import soundfile as sf
import numpy as np
from tqdm import tqdm

def preprocess_urbansound(csv_path, source_dir, output_dir, output_csv_path, target_sr=22050, target_duration=4.0):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    target_samples = int(target_sr * target_duration)
    
    processed_records = []
    print("Започва обработка на аудио файловете...")
    
    for index, row in tqdm(df.iterrows(), total=len(df)):
        file_name = row['slice_file_name']
        fold = row['fold']
        class_id = row['classID']
        class_name = row['class']
        
        source_path = os.path.join(source_dir, f"fold{fold}", file_name)
        if not os.path.exists(source_path):
            continue
            
        try:
            audio, sr = librosa.load(source_path, sr=target_sr)
            
            if len(audio) > target_samples:
                audio = audio[:target_samples]
            elif len(audio) < target_samples:
                padding = target_samples - len(audio)
                audio = np.pad(audio, (0, padding), mode='constant')
                
            output_file_path = os.path.join(output_dir, file_name)
            sf.write(output_file_path, audio, target_sr)
            
            processed_records.append({
                'slice_file_name': file_name,
                'classID': class_id,
                'class': class_name,
                'fold': fold,
                'processed_path': output_file_path
            })
            
        except Exception as e:
            print(f"Грешка при обработка на {file_name}: {e}")
            
    new_df = pd.DataFrame(processed_records)
    new_df.to_csv(output_csv_path, index=False)
    print(f"Обработката завърши! Новият CSV е запазен в: {output_csv_path}")