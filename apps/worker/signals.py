from dataclasses import dataclass
from typing import List


@dataclass
class StrategySignal:
    name: str
    direction: int
    confidence: float
    rationale: str


def momentum_breakout(features: dict) -> StrategySignal:
    score = min(1.0, max(0.0, features.get("trend_alignment", 0)))
    return StrategySignal(
        name="momentum_breakout",
        direction=1,
        confidence=score,
        rationale="VWAP/MA alignment with volume surge",
    )


def mean_reversion(features: dict) -> StrategySignal:
    score = min(1.0, max(0.0, 1 - abs(features.get("gap_pct", 0))))
    return StrategySignal(
        name="mean_reversion",
        direction=1,
        confidence=score,
        rationale="Deviation from VWAP reversion potential",
    )


def volatility_breakout(features: dict) -> StrategySignal:
    score = min(1.0, max(0.0, features.get("volatility_expansion", 0)))
    return StrategySignal(
        name="volatility_breakout",
        direction=1,
        confidence=score,
        rationale="ATR/true range expansion",
    )


def ensemble_signals(features: dict) -> List[StrategySignal]:
    return [
        momentum_breakout(features),
        mean_reversion(features),
        volatility_breakout(features),
    ]
