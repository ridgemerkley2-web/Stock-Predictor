from dataclasses import dataclass
from typing import List

from signals import StrategySignal


@dataclass
class CertaintyInputs:
    model_margin: float
    liquidity_penalty: float
    regime_score: float
    calibration_score: float


def ensemble_agreement(signals: List[StrategySignal]) -> float:
    if not signals:
        return 0.0
    avg_conf = sum(signal.confidence for signal in signals) / len(signals)
    return min(1.0, avg_conf)


def certainty_score(signals: List[StrategySignal], inputs: CertaintyInputs) -> float:
    agreement = ensemble_agreement(signals)
    score = (
        0.35 * inputs.model_margin
        + 0.25 * agreement
        + 0.15 * inputs.regime_score
        + 0.15 * inputs.calibration_score
        - 0.10 * inputs.liquidity_penalty
    )
    return max(0.0, min(1.0, score))


def expected_value(edge: float, costs: float) -> float:
    return edge - costs
