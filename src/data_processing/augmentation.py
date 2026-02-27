import random

class SpecAugment:
    """
    Прилага Time Masking и Frequency Masking върху Мел-спектрограма.
    Очаква PyTorch тензор с форма (Channels, Mels, Time), напр. (1, 128, 173).
    """
    def __init__(self, freq_mask_param=15, time_mask_param=30):
        self.freq_mask_param = freq_mask_param
        self.time_mask_param = time_mask_param

    def __call__(self, tensor):
        # Клонираме тензора, за да не променяме оригиналните данни в паметта
        augmented = tensor.clone()
        channels, n_mels, n_steps = augmented.shape

        # 1. Frequency Masking (скрива случайна хоризонтална лента)
        f_mask_len = random.randint(0, self.freq_mask_param)
        f0 = random.randint(0, n_mels - f_mask_len)
        augmented[:, f0:f0 + f_mask_len, :] = 0

        # 2. Time Masking (скрива случайна вертикална лента)
        t_mask_len = random.randint(0, self.time_mask_param)
        if n_steps > t_mask_len: # Проверка за сигурност, ако аудиото е твърде кратко
            t0 = random.randint(0, n_steps - t_mask_len)
            augmented[:, :, t0:t0 + t_mask_len] = 0

        return augmented