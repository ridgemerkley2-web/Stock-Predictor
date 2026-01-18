from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


@dataclass(frozen=True)
class SequenceConfig:
    feature_cols: List[str]
    target_col: str
    sequence_length: int


class SequenceDataset(Dataset):
    def __init__(self, features: np.ndarray, targets: np.ndarray):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.targets = torch.tensor(targets, dtype=torch.float32)

    def __len__(self) -> int:
        return len(self.targets)

    def __getitem__(self, idx: int):
        return self.features[idx], self.targets[idx]


def load_sequence_csv(path: str, config: SequenceConfig) -> SequenceDataset:
    data = pd.read_csv(path)
    features = data[config.feature_cols].to_numpy(dtype=np.float32)
    targets = data[config.target_col].to_numpy(dtype=np.float32)

    sequences = []
    labels = []
    for idx in range(config.sequence_length, len(features)):
        sequences.append(features[idx - config.sequence_length : idx])
        labels.append(targets[idx])
    return SequenceDataset(np.stack(sequences), np.array(labels))
