import eel
import os
import sys
import time
import numpy as np
import sounddevice as sd
import torch
import librosa
import threading
import queue
import psutil
import socket

# Глобални променливи за управление на анализа
is_analyzing = False
analysis_thread = None
audio_q = queue.Queue()

# Настройки от Front-end (с подразбиране)
app_settings = {
    "notifications": True,
    "sound_recognition": True,
    "enabled_sounds": {
        "baby_cry": True, "car_horn": True, "construction": True,
        "dog_bark": True, "door_signal": True, "glass_break": True, "siren_alarm": True
    }
}

last_prediction_time = 0
COOLDOWN_SECONDS = 5.0 # КАТО В IOS (приблизително за UX)

# Добавяме основната папка на проекта към sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.models.mobilenet_model import AudioMobileNetV2

# 1. Зареждане на модела и теглата
LABELS = [
    "Baby_Cry", "Background", "Car_Horn", 
    "Construction", "Dog_Bark", "Door_Signal", 
    "Glass_Break", "Siren_Alarm"
]

LABEL_MAPPING = {
    "Baby_Cry": {"id": "baby_cry", "label": "Плачещо бебе", "type": "warning", "threshold": 0.40},
    "Background": {"id": "background", "label": "Фонов шум", "type": "info", "threshold": 1.00},
    "Car_Horn": {"id": "car_horn", "label": "Клаксон", "type": "danger", "threshold": 0.60},
    "Construction": {"id": "construction", "label": "Ремонтни дейности", "type": "warning", "threshold": 0.85},
    "Dog_Bark": {"id": "dog_bark", "label": "Кучешки лай", "type": "warning", "threshold": 0.85},
    "Door_Signal": {"id": "door_signal", "label": "Звънец / Чукане", "type": "info", "threshold": 0.45},
    "Glass_Break": {"id": "glass_break", "label": "Счупено стъкло", "type": "danger", "threshold": 0.45},
    "Siren_Alarm": {"id": "siren_alarm", "label": "Сирена / Аларма", "type": "danger", "threshold": 0.60}
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AudioMobileNetV2(n_classes=len(LABELS), pretrained=False)

weights_path = os.path.join(project_root, 'models', 'best_mobilenet.pth')
if os.path.exists(weights_path):
    print(f"Зареждане на тегла от: {weights_path}")
    model.load_state_dict(torch.load(weights_path, map_location=device))
else:
    print(f"ВНИМАНИЕ: Файлът с тегла не е намерен!")

model.to(device)
model.eval()

def preprocess_audio(y, sr=22050):
    y = librosa.effects.preemphasis(y, coef=0.97)
    target_samples = int(4.0 * sr)
    if len(y) > target_samples:
        y = y[:target_samples]
    else:
        y = np.pad(y, (0, target_samples - len(y)), mode='constant')
        
    rms = np.sqrt(np.mean(y**2))
    if rms > 0.0:
        target_rms = 0.05
        y = y * (target_rms / rms)
        
    S = librosa.feature.melspectrogram(
        y=y, sr=sr, n_fft=2048, hop_length=512, n_mels=128, fmin=0.0, fmax=8000.0, center=True
    )
    
    S_db = librosa.power_to_db(S, ref=np.max)
    top_db = 80.0
    S_norm = (S_db + top_db) / top_db
    S_norm = np.clip(S_norm, 0, 1)
    
    tensor = torch.from_numpy(S_norm).float()
    tensor = tensor.unsqueeze(0).unsqueeze(0)
    return tensor.to(device)

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Грешка в аудио потока: {status}")
    audio_q.put(indata.copy())

def analysis_loop():
    global is_analyzing, last_prediction_time
    print("🔄 Започвам непрекъснат анализ (Gapless + iOS Processing)...")
    
    sample_rate = 22050
    window_samples = int(4.0 * sample_rate)
    audio_buffer = np.zeros(window_samples)
    
    with sd.InputStream(samplerate=sample_rate, channels=1, callback=audio_callback):
        while is_analyzing:
            try:
                # Взимаме новите данни
                while not audio_q.empty():
                    chunk = audio_q.get().flatten()
                    audio_buffer = np.roll(audio_buffer, -len(chunk))
                    audio_buffer[-len(chunk):] = chunk
                
                # Ако сме в режим на пауза според настройките, само събираме аудио но не смятаме
                if not app_settings["sound_recognition"]:
                    time.sleep(0.1)
                    continue

                # Проверка за COOLDOWN (5 сек)
                current_time = time.time()
                if current_time - last_prediction_time < COOLDOWN_SECONDS:
                    time.sleep(0.1)
                    continue

                # Анализ
                processed_audio = preprocess_audio(audio_buffer, sr=sample_rate)
                
                with torch.no_grad():
                    outputs = model(processed_audio)
                    probabilities = torch.nn.functional.softmax(outputs, dim=1)
                    confidence, predicted_idx = torch.max(probabilities, 1)
                    
                class_name = LABELS[predicted_idx.item()]
                conf_value = int(confidence.item() * 100)
                
                result = LABEL_MAPPING[class_name]
                threshold_pct = result["threshold"] * 100

                # Филтриране на Фонов шум
                if class_name == "Background":
                    if conf_value > 50:
                        eel.update_ui_result({"status": "quiet"})
                    continue
                
                # Проверка дали звукът е активиран в настройките
                sound_id = result["id"]
                if not app_settings["enabled_sounds"].get(sound_id, True):
                    continue

                # Праг за конкретния клас
                if conf_value < threshold_pct:
                    continue
                
                print(f"📡 Засечено: {result['label']} ({conf_value}%)")
                last_prediction_time = current_time # Рестартираме таймера
                
                eel.update_ui_result({
                    "status": result["type"],
                    "sound_type": result["label"],
                    "confidence": conf_value
                })
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Грешка в цикъла: {e}")
                break

@eel.expose
def toggle_continuous_analysis(should_start):
    global is_analyzing, analysis_thread
    
    if should_start and not is_analyzing:
        is_analyzing = True
        analysis_thread = threading.Thread(target=analysis_loop, daemon=True)
        analysis_thread.start()
        print("✅ Анализът е стартиран.")
        return "Started"
    elif not should_start:
        is_analyzing = False
        print("✅ Анализът е спрян.")
        return "Stopped"
    return "No change"

@eel.expose
def get_device_info():
    try:
        battery = psutil.sensors_battery()
        percent = battery.percent if battery else 100
        is_charging = battery.power_plugged if battery else False
        device_name = socket.gethostname()
        
        return {
            "device_name": device_name,
            "battery_percent": percent,
            "is_charging": is_charging
        }
    except Exception as e:
        print(f"Error getting device info: {e}")
        return {"device_name": "Това устройство", "battery_percent": 100, "is_charging": False}

@eel.expose
def update_settings(new_settings):
    global app_settings
    app_settings.update(new_settings)
    print(f"⚙️ Настройките бяха обновени: {app_settings}")

# Eel Init
web_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')
eel.init(web_dir)

print("🚀 SONAR Windows е зареден и готов!")
try:
    eel.start('index.html', size=(400, 800))
except (SystemExit, MemoryError, KeyboardInterrupt):
    is_analyzing = False
