from dataclasses import dataclass
from typing import Dict

import torch
from torch import nn
from torch.utils.data import DataLoader


@dataclass(frozen=True)
class TrainConfig:
    epochs: int
    learning_rate: float
    batch_size: int


def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    config: TrainConfig,
    device: str = "cpu",
) -> Dict[str, float]:
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    loss_fn = nn.BCEWithLogitsLoss()

    for _ in range(config.epochs):
        model.train()
        for features, target in train_loader:
            features = features.to(device)
            target = target.to(device)
            optimizer.zero_grad()
            output = model(features)
            loss = loss_fn(output, target)
            loss.backward()
            optimizer.step()

    model.eval()
    total_loss = 0.0
    total = 0
    with torch.no_grad():
        for features, target in val_loader:
            features = features.to(device)
            target = target.to(device)
            output = model(features)
            loss = loss_fn(output, target)
            total_loss += loss.item() * features.size(0)
            total += features.size(0)

    return {"val_loss": total_loss / max(total, 1)}
