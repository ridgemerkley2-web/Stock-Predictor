from dataclasses import dataclass
from typing import Dict, Optional

from alpaca import AlpacaClient
from rate_limiter import with_retry


@dataclass
class ExecutionResult:
    order_id: Optional[str]
    status: str
    message: str


def build_bracket_order(
    ticker: str,
    qty: int,
    entry: float,
    stop: float,
    target: float,
) -> Dict[str, object]:
    return {
        "symbol": ticker,
        "qty": qty,
        "side": "buy",
        "type": "limit",
        "time_in_force": "day",
        "limit_price": entry,
        "order_class": "bracket",
        "take_profit": {"limit_price": target},
        "stop_loss": {"stop_price": stop},
    }


async def place_order(client: AlpacaClient, order: Dict[str, object]) -> ExecutionResult:
    try:
        response = await with_retry(client.submit_order, order)
        return ExecutionResult(response.get("id"), "submitted", "ok")
    except Exception as exc:
        return ExecutionResult(None, "error", str(exc))


async def flatten_all(client: AlpacaClient) -> ExecutionResult:
    try:
        response = await with_retry(client._request, "DELETE", "/v2/positions")
        response.raise_for_status()
        return ExecutionResult(None, "submitted", "flattened")
    except Exception as exc:
        return ExecutionResult(None, "error", str(exc))
