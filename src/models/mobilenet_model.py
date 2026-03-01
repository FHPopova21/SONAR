import torch
import torch.nn as nn
from torchvision import models

class AudioMobileNetV2(nn.Module):
    def __init__(self, n_classes=8, pretrained=True):
        super(AudioMobileNetV2, self).__init__()
        
        # 1. Зареждаме готовия MobileNetV2
        # Използваме 'DEFAULT' (най-добрите тегла) ако pretrained=True
        weights = models.MobileNet_V2_Weights.DEFAULT if pretrained else None
        self.model = models.mobilenet_v2(weights=weights)
        
        # 2. Адаптираме входа (Защото нашите спектрограми са 1-канални)
        # Взимаме оригиналния първи слой
        original_first_layer = self.model.features[0][0]
        
        # Създаваме нов слой, който очаква 1 канал (in_channels=1)
        new_first_layer = nn.Conv2d(
            in_channels=1, 
            out_channels=original_first_layer.out_channels,
            kernel_size=original_first_layer.kernel_size,
            stride=original_first_layer.stride,
            padding=original_first_layer.padding,
            bias=original_first_layer.bias
        )
        
        # Копираме теглата от първия канал на оригиналния слой
        # Така не губим това, което моделът вече е научил!
        with torch.no_grad():
            new_first_layer.weight[:, 0:1, :, :] = original_first_layer.weight[:, 0:1, :, :]
            
        # Заменяме слоя в модела
        self.model.features[0][0] = new_first_layer
        
        # 3. Адаптираме изхода (Класификатора)
        # Увеличаваме Dropout-а на 0.5 за по-добра регуляризация
        in_features = self.model.classifier[1].in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(p=0.5, inplace=False),
            nn.Linear(in_features, n_classes)
        )

    def forward(self, x):
        return self.model(x)