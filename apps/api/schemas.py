from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Side(str, Enum):
    buy = "buy"
    sell = "sell"


class Candidate(BaseModel):
    ticker: str
    side: Side = Side.buy
    entry_hint: float
    stop: float
    target: float
    ev: float = Field(description="Expected value after costs")
    certainty: float = Field(ge=0, le=1)
    rationale: List[str]
    timestamp: datetime


class Position(BaseModel):
    ticker: str
    qty: float
    avg_entry: float
    unrealized_pl: float
    side: Side = Side.buy


class OrderStatus(str, Enum):
    new = "new"
    filled = "filled"
    partially_filled = "partially_filled"
    canceled = "canceled"
    rejected = "rejected"


class Order(BaseModel):
    order_id: str
    ticker: str
    side: Side
    qty: float
    order_type: str
    status: OrderStatus
    submitted_at: datetime
    filled_qty: float = 0


class RiskState(BaseModel):
    equity: float
    gross_exposure: float
    max_positions: int
    daily_loss_limit: float
    drawdown_limit: float
    circuit_breaker_tripped: bool


class BundleMetrics(BaseModel):
    sharpe: float
    max_drawdown: float
    trades: int
    win_rate: float
    brier_score: Optional[float] = None


class Bundle(BaseModel):
    bundle_id: str
    name: str
    created_at: datetime
    active: bool
    parameters: dict
    metrics: BundleMetrics
    holdout_metrics: BundleMetrics
    metadata: dict
