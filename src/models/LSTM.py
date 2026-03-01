import torch
import torch.nn as nn

class AudioLSTM(nn.Module):
    def __init__(self, n_feature=128, out_feature=8, n_hidden=256, n_layers=2, drop_prob=0.3):
        super().__init__()

        self.n_hidden = n_hidden
        self.n_layers = n_layers

        # Самата LSTM мрежа
        self.lstm = nn.LSTM(
            n_feature,
            n_hidden,
            n_layers,
            dropout=drop_prob,
            batch_first=True,
            bidirectional=True # Чете звука и напред, и назад!
        )

        self.layer_norm = nn.LayerNorm(n_hidden * 2)
        self.dropout = nn.Dropout(drop_prob)

        self.fc1 = nn.Linear(n_hidden * 2, n_hidden)
        self.fc2 = nn.Linear(n_hidden, out_feature)

        self.relu = nn.ReLU()

    def forward(self, x):
        # ПРОМЯНА 2: Адаптираме формата на данните (от CNN към LSTM)
        # Вход x: (batch_size, 1, 128, time_steps)
        x = x.squeeze(1)             # Махаме канала: става (batch_size, 128, time_steps)
        x = x.permute(0, 2, 1)       # Разменяме осите: става (batch_size, time_steps, 128)

        # ПРОМЯНА 3: Инициализираме hidden state тук, за да не чупим тренировъчния цикъл
        batch_size = x.size(0)
        device = x.device
        h0 = torch.zeros(self.n_layers * 2, batch_size, self.n_hidden, device=device)
        c0 = torch.zeros(self.n_layers * 2, batch_size, self.n_hidden, device=device)
        hidden = (h0, c0)

        # Пускаме през LSTM
        l_out, hidden = self.lstm(x, hidden)

        # Взимаме само последния времеви момент (какво е разбрала мрежата в края на звука)
        last_out = l_out[:, -1, :]  # (batch, hidden*2)
        last_out = self.layer_norm(last_out)

        # Класификатор
        out = self.dropout(last_out)
        out = self.relu(self.fc1(out))
        out = self.fc2(out)

        # Връщаме само изхода (out), за да пасне перфектно на твоя код за Loss и Accuracy!
        return out