from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class FeatureSnapshot:
    ticker: str
    volume_surge: float
    gap_pct: float
    volatility_expansion: float
    trend_alignment: float


@dataclass
class ScanCandidate:
    ticker: str
    score: float
    features: FeatureSnapshot
    timestamp: datetime


def compute_score(features: FeatureSnapshot) -> float:
    return (
        0.35 * features.volume_surge
        + 0.25 * features.gap_pct
        + 0.25 * features.volatility_expansion
        + 0.15 * features.trend_alignment
    )


def rank_candidates(features: List[FeatureSnapshot]) -> List[ScanCandidate]:
    ranked = [
        ScanCandidate(
            ticker=item.ticker,
            score=compute_score(item),
            features=item,
            timestamp=datetime.utcnow(),
        )
        for item in features
    ]
    ranked.sort(key=lambda item: item.score, reverse=True)
    return ranked[:200]
