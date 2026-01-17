from apps.worker.alpaca import AlpacaClient
from apps.worker.config import Settings


def test_idempotent_order_key_stable():
    settings = Settings(
        alpaca_api_key="key",
        alpaca_api_secret="secret",
        alpaca_base_url="https://paper-api.alpaca.markets",
        alpaca_data_url="https://data.alpaca.markets",
        alpaca_stream_url="wss://stream.data.alpaca.markets/v2/iex",
        alpaca_trade_stream_url="wss://paper-api.alpaca.markets/stream",
        enable_live_trading=False,
        admin_secret="",
        enable_auto_promote=False,
        postgres_url="",
        redis_url="redis://localhost:6379/0",
        base_risk=0.0025,
        c_min=0.55,
        max_positions=10,
        max_gross_exposure=1.5,
        sector_concentration=0.25,
        daily_max_loss=0.03,
        drawdown_max=0.1,
    )
    client = AlpacaClient(settings)
    order = {"symbol": "AAPL", "qty": 10, "side": "buy", "type": "market"}
    assert client.build_idempotency_key(order) == client.build_idempotency_key(order)
