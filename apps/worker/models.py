from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class ModelSpec:
    name: str
    description: str
    default_params: Dict[str, object]
    class_path: str


MODEL_SPECS: List[ModelSpec] = [
    ModelSpec(
        name="temporal_transformer",
        description="Transformer encoder for sequence-to-one market direction scoring.",
        default_params={"d_model": 128, "n_heads": 4, "layers": 4, "dropout": 0.1},
        class_path="neural.models.TemporalTransformer",
    ),
    ModelSpec(
        name="temporal_fusion_transformer",
        description="TFT-style architecture with variable selection and gating layers.",
        default_params={"hidden_size": 64, "attention_heads": 4, "dropout": 0.1},
        class_path="neural.models.TemporalFusionTransformer",
    ),
    ModelSpec(
        name="lstm",
        description="Stacked LSTM for next-bar probability estimation.",
        default_params={"hidden_size": 128, "layers": 2, "dropout": 0.2},
        class_path="neural.models.LSTMModel",
    ),
    ModelSpec(
        name="tcn",
        description="Temporal Convolutional Network for fast sequence modeling.",
        default_params={"channels": [32, 64, 128], "kernel_size": 3, "dropout": 0.1},
        class_path="neural.models.TCNModel",
    ),
]


def list_model_specs() -> List[ModelSpec]:
    return MODEL_SPECS
