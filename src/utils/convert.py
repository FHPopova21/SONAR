import os
import sys
import torch
import coremltools as ct

# Пътища
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.models.mobilenet_model import AudioMobileNetV2

# 1. Дефиниране на класовете (точно в реда от Classification Report)
class_labels = [
    "Baby_Cry",      # 0
    "Background",    # 1
    "Car_Horn",      # 2
    "Construction",  # 3
    "Dog_Bark",      # 4
    "Door_Signal",   # 5
    "Glass_Break",   # 6
    "Siren_Alarm"    # 7
]

# 2. Инициализация на модела с 8 класа
model = AudioMobileNetV2(n_classes=8, pretrained=False) 
# Смени "best_mobilenet.pth" с "3_mobilenet.pth", ако това е името от лога ти
model_path = os.path.join(project_root, "models", "best_mobilenet.pth")

print(f"Зареждане на тегла от: {model_path}")
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

# 3. Подготовка на примерния вход (128 мел-филтъра x 173 времеви стъпки)
example_input = torch.rand(1, 1, 128, 173)
traced_model = torch.jit.trace(model, example_input)

# 4. Конвертиране към CoreML
print("Започва конвертиране към CoreML...")
mlmodel = ct.convert(
    traced_model,
    inputs=[ct.TensorType(name="audio_input", shape=example_input.shape)],
    classifier_config=ct.ClassifierConfig(class_labels), # Вграждаме етикетите
    convert_to="mlprogram" # По-модерен формат за iOS 15+
)

# 5. Добавяне на метаданни (полезно за Xcode)
mlmodel.author = "Sonar Project"
mlmodel.license = "MIT"
mlmodel.short_description = "MobileNetV2 модел за класификация на градски звуци (8 класа)"

# 6. Запазване
mlmodel.save("SonarMobileNetV2.mlpackage")
print("✅ Успешно запазен като SonarMobileNetV2.mlpackage!")
print(f"🎯 Вход: {example_input.shape} (Batch, Channel, Mels, Time)")
print(f"🏷️ Класове: {class_labels}")