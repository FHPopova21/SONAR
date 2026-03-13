import numpy as np
import sounddevice as sd
import librosa
import torch
import queue
from config import SAMPLE_RATE

class AudioHandler:
    def __init__(self, device):
        self.sample_rate = SAMPLE_RATE
        self.audio_q = queue.Queue()
        self.device = device

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Грешка в аудио потока: {status}")
        self.audio_q.put(indata.copy())

    def preprocess_audio(self, y):
        # Pre-emphasis
        y = librosa.effects.preemphasis(y, coef=0.97)
        
        # Target samples (4.0 seconds)
        target_samples = int(4.0 * self.sample_rate)
        if len(y) > target_samples:
            y = y[:target_samples]
        else:
            y = np.pad(y, (0, target_samples - len(y)), mode='constant')
            
        # Normalization
        rms = np.sqrt(np.mean(y**2))
        if rms > 0.0:
            target_rms = 0.05
            y = y * (target_rms / rms)
            
        # Mel-Spectrogram
        S = librosa.feature.melspectrogram(
            y=y, sr=self.sample_rate, n_fft=2048, hop_length=512, n_mels=128, fmin=0.0, fmax=8000.0, center=True
        )
        
        # Log-scale
        S_db = librosa.power_to_db(S, ref=np.max)
        top_db = 80.0
        S_norm = (S_db + top_db) / top_db
        S_norm = np.clip(S_norm, 0, 1)
        
        # To tensor
        tensor = torch.from_numpy(S_norm).float()
        tensor = tensor.unsqueeze(0).unsqueeze(0)
        return tensor.to(self.device)
