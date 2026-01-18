from typing import List

import torch
from torch import nn


class TemporalTransformer(nn.Module):
    def __init__(self, feature_dim: int, d_model: int, n_heads: int, layers: int, dropout: float):
        super().__init__()
        self.input_proj = nn.Linear(feature_dim, d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dropout=dropout,
            batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=layers)
        self.head = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.input_proj(x)
        encoded = self.encoder(x)
        pooled = encoded[:, -1, :]
        return self.head(pooled).squeeze(-1)


class TemporalFusionTransformer(nn.Module):
    def __init__(self, feature_dim: int, hidden_size: int, attention_heads: int, dropout: float):
        super().__init__()
        self.proj = nn.Linear(feature_dim, hidden_size)
        self.gate = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Sigmoid(),
        )
        self.attn = nn.MultiheadAttention(hidden_size, attention_heads, dropout=dropout, batch_first=True)
        self.out = nn.Sequential(
            nn.LayerNorm(hidden_size),
            nn.Linear(hidden_size, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        proj = self.proj(x)
        gated = proj * self.gate(proj)
        attn_out, _ = self.attn(gated, gated, gated)
        pooled = attn_out[:, -1, :]
        return self.out(pooled).squeeze(-1)


class LSTMModel(nn.Module):
    def __init__(self, feature_dim: int, hidden_size: int, layers: int, dropout: float):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=feature_dim,
            hidden_size=hidden_size,
            num_layers=layers,
            dropout=dropout if layers > 1 else 0.0,
            batch_first=True,
        )
        self.head = nn.Linear(hidden_size, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        _, (hidden, _) = self.lstm(x)
        return self.head(hidden[-1]).squeeze(-1)


class TemporalBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int, dilation: int, dropout: float):
        super().__init__()
        padding = (kernel_size - 1) * dilation
        self.conv1 = nn.Conv1d(
            in_channels,
            out_channels,
            kernel_size,
            padding=padding,
            dilation=dilation,
        )
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
        self.conv2 = nn.Conv1d(
            out_channels,
            out_channels,
            kernel_size,
            padding=padding,
            dilation=dilation,
        )
        self.downsample = nn.Conv1d(in_channels, out_channels, 1) if in_channels != out_channels else None

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.conv1(x)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.conv2(out)
        res = x if self.downsample is None else self.downsample(x)
        return self.relu(out + res)


class TCNModel(nn.Module):
    def __init__(self, feature_dim: int, channels: List[int], kernel_size: int, dropout: float):
        super().__init__()
        layers = []
        in_channels = feature_dim
        dilation = 1
        for out_channels in channels:
            layers.append(TemporalBlock(in_channels, out_channels, kernel_size, dilation, dropout))
            in_channels = out_channels
            dilation *= 2
        self.network = nn.Sequential(*layers)
        self.head = nn.Linear(channels[-1], 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.transpose(1, 2)
        out = self.network(x)
        pooled = out[:, :, -1]
        return self.head(pooled).squeeze(-1)
