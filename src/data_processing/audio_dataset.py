import os
import torch
import numpy as np
import pandas as pd
import glob
from torch.utils.data import Dataset
from src.data_processing.extract_mel import extract_mel_spectrogram
from src.data_processing.format_for_mel import format_for_mel

class AudioFolderDataset(Dataset):
    def __init__(self, root_dir, csv_file=None, augment=False, transform=None):
        """
        Зарежда аудио файлове. Ако е подаден csv_file, филтрира само описаните в него файлове.
        Ако не - зарежда всичко от подпапките на root_dir.
        Args:
            root_dir (str): Път до главната папка (напр. data/Dataset_Final)
            csv_file (str, optional): Път до CSV файл със сплит (напр. data/test_split.csv)
            augment (bool): Дали да се прилага data augmentation
            transform (callable, optional): Допълнителни трансформации.
        """
        self.root_dir = root_dir
        self.augment = augment
        self.transform = transform
        
        # Динамично създаване на класовете от папките (винаги от root_dir за консистенция на индексите)
        if not os.path.exists(root_dir):
            # Опит за корекция на пътя, ако се стартира от notebooks/
            alt_root = os.path.join("..", root_dir)
            if os.path.exists(alt_root):
                root_dir = alt_root
        
        self.classes = sorted([d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))])
        self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.classes)}
        
        self.filepaths = []
        self.labels = []
        
        if csv_file:
            # Опит за корекция на пътя до CSV, ако се стартира от notebooks/
            if not os.path.exists(csv_file):
                alt_csv = os.path.join("..", csv_file)
                if os.path.exists(alt_csv):
                    csv_file = alt_csv
            
            print(f"Зареждане на данни от сплит файл: {csv_file}")
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                path = row['file_path']
                # Корекция на пътищата вътре в CSV (ако са относителни спрямо root на проекта)
                if not os.path.exists(path):
                    alt_path = os.path.join("..", path)
                    if os.path.exists(alt_path):
                        path = alt_path
                
                self.filepaths.append(path)
                self.labels.append(row['label'])
        else:
            print(f"Зареждане на всички данни от директория: {root_dir}")
            for cls_name in self.classes:
                cls_dir = os.path.join(root_dir, cls_name)
                for file in glob.glob(os.path.join(cls_dir, "*.wav")):
                    self.filepaths.append(file)
                    self.labels.append(self.class_to_idx[cls_name])

    def __len__(self):
        return len(self.filepaths)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
            
        audio_path = self.filepaths[idx]
        label = self.labels[idx]
        
        # Извличане на мел-спектрограма
        mel_spec = extract_mel_spectrogram(audio_path, augment=self.augment)
        
        # Форматиране (нормализация и добавяне на канал)
        mel_tensor_np = format_for_mel(mel_spec)
        
        # Преобразуване към PyTorch Tensor (float32)
        mel_tensor = torch.tensor(mel_tensor_np, dtype=torch.float32)
        
        if self.transform:
            mel_tensor = self.transform(mel_tensor)

        return mel_tensor, label
