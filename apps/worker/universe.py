from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List


@dataclass
class UniverseEntry:
    ticker: str
    avg_dollar_volume: float
    last_price: float
    spread: float


class UniverseBuilder:
    def __init__(self):
        self.last_refresh: datetime | None = None
        self.universe: List[UniverseEntry] = []

    def refresh_needed(self) -> bool:
        if not self.last_refresh:
            return True
        return datetime.utcnow() - self.last_refresh > timedelta(minutes=60)

    def build_universe(self, raw_universe: List[UniverseEntry]) -> List[UniverseEntry]:
        filtered = [
            entry
            for entry in raw_universe
            if 2 <= entry.last_price <= 500
        ]
        filtered = sorted(filtered, key=lambda item: item.avg_dollar_volume, reverse=True)
        top = filtered[:2000]
        self.universe = top
        self.last_refresh = datetime.utcnow()
        return top
