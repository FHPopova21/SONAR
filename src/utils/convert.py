import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

import torch
import coremltools as ct
from src.models.CNN_model import AudioCNN

# 1. Зареждаш модела
model = AudioCNN()
model_path = os.path.join(project_root, "models", "audio_CNN.pth")
model.load_state_dict(torch.load(model_path))
model.eval()

# 2. Примерен вход (dummy input)
example_input = torch.rand(1, 1, 128, 173)

# 3. Trace
traced_model = torch.jit.trace(model, example_input)

# 4. Конвертиране
mlmodel = ct.convert(
    traced_model,
    inputs=[ct.TensorType(shape=example_input.shape)]
)

mlmodel.save("SonarCNN.mlpackage")