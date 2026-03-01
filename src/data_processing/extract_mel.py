import os
import glob
import librosa
import librosa.display
import numpy as np 

def extract_mel_spectrogram(file_path):
    # 1. Зареждаме аудиото твърдо на 22050 Hz
    y, sr = librosa.load(file_path, sr=22050)
    
    # 2. Изрязваме или допълваме с нули до ТОЧНО 4 секунди (88200 семпъла)
    target_samples = int(4.0 * sr)
    if len(y) > target_samples:
        y = y[:target_samples]
    else:
        y = np.pad(y, (0, target_samples - len(y)), mode='constant')
        
    # 3. МАГИЯТА: Генерираме Мел-спектрограмата
    S = librosa.feature.melspectrogram(
        y=y, 
        sr=sr, 
        n_fft=2048, 
        hop_length=512, 
        n_mels=128,       # Променено на 128
        fmin=0.0, 
        fmax=8000.0,      # Ограничено до 8000 Hz
        center=True       # ВАЖНО: Добавя падинга!
    )
    
    # 4. Преобразуване в Децибели (С фиксиран референс за Swift)
    S_db = librosa.power_to_db(S, ref=1.0)
    
    # Резултатът ще бъде матрица с размери точно (128, 173)
    return S_db