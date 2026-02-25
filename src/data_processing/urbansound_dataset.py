import os
import pandas as pd
import librosa
import torch
import numpy as np
from torch.utils.data import Dataset

from src.data_processing.extract_mel import extract_mel_spectrogram
from src.data_processing.format_for_mel import format_for_mel

class UrbanSoundDataset(Dataset):
    def __init__(self, csv_file, audio_dir, transform=None):
        """
        Args:
            csv_file (str): Път до обработения CSV файл.
            audio_dir (str): Път до папката с обработените аудио файлове.
            transform (callable, optional): Допълнителни трансформации.
        """
        self.data_frame = pd.read_csv(csv_file)
        self.audio_dir = audio_dir
        self.transform = transform

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        file_name = self.data_frame.iloc[idx]['slice_file_name']
        label = int(self.data_frame.iloc[idx]['classID'])
        
        audio_path = os.path.join(self.audio_dir, file_name)
        
        # Зареждане на аудиото (вече е точно 4.0 секунди на 22050 Hz)
        audio, sr = librosa.load(audio_path, sr=None) 
        
        # Извличане на мел-спектрограма
        mel_spec = extract_mel_spectrogram(audio, sr=sr)
        
        # Форматиране (нормализация и добавяне на канал)
        mel_tensor_np = format_for_mel(mel_spec)
        
        # Преобразуване към PyTorch Tensor (float32)
        mel_tensor = torch.tensor(mel_tensor_np, dtype=torch.float32)
        
        if self.transform:
            mel_tensor = self.transform(mel_tensor)

        return mel_tensor, label
