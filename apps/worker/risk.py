from dataclasses import dataclass


@dataclass
class RiskConfig:
    base_risk: float
    c_min: float
    max_positions: int
    max_gross_exposure: float
    sector_concentration: float
    daily_max_loss: float
    drawdown_max: float


@dataclass
class RiskDecision:
    allowed: bool
    qty: int
    stop: float
    target: float
    rationale: str


@dataclass
class CircuitBreakerState:
    tripped: bool
    reason: str


def risk_multiplier(certainty: float) -> float:
    return min(2.0, 0.5 + certainty * 1.5)


def reward_multiplier(certainty: float) -> float:
    return min(4.0, 1.5 + certainty * 2.0)


def compute_bracket(entry: float, atr: float, certainty: float) -> tuple[float, float]:
    stop = entry - (1 + certainty) * atr
    target = entry + reward_multiplier(certainty) * (entry - stop)
    return stop, target


def position_size(equity: float, entry: float, stop: float, risk_per_trade: float) -> int:
    per_share_risk = max(0.01, entry - stop)
    qty = int((equity * risk_per_trade) / per_share_risk)
    return max(0, qty)


def evaluate_trade(
    equity: float,
    entry: float,
    atr: float,
    certainty: float,
    config: RiskConfig,
) -> RiskDecision:
    if certainty < config.c_min:
        return RiskDecision(False, 0, 0.0, 0.0, "certainty below threshold")

    risk_per_trade = config.base_risk * risk_multiplier(certainty)
    stop, target = compute_bracket(entry, atr, certainty)
    qty = position_size(equity, entry, stop, risk_per_trade)
    allowed = qty > 0
    return RiskDecision(allowed, qty, stop, target, "risk sizing ok")


def check_circuit_breaker(daily_loss: float, drawdown: float, config: RiskConfig) -> CircuitBreakerState:
    if daily_loss <= -config.daily_max_loss:
        return CircuitBreakerState(True, "daily loss limit exceeded")
    if drawdown >= config.drawdown_max:
        return CircuitBreakerState(True, "drawdown limit exceeded")
    return CircuitBreakerState(False, "ok")
