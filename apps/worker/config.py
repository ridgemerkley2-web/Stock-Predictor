import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    alpaca_api_key: str
    alpaca_api_secret: str
    alpaca_base_url: str
    alpaca_data_url: str
    alpaca_stream_url: str
    alpaca_trade_stream_url: str
    enable_live_trading: bool
    admin_secret: str
    enable_auto_promote: bool
    postgres_url: str
    redis_url: str
    base_risk: float
    c_min: float
    max_positions: int
    max_gross_exposure: float
    sector_concentration: float
    daily_max_loss: float
    drawdown_max: float


def load_settings() -> Settings:
    return Settings(
        alpaca_api_key=os.getenv("ALPACA_API_KEY", ""),
        alpaca_api_secret=os.getenv("ALPACA_API_SECRET", ""),
        alpaca_base_url=os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets"),
        alpaca_data_url=os.getenv("ALPACA_DATA_URL", "https://data.alpaca.markets"),
        alpaca_stream_url=os.getenv("ALPACA_STREAM_URL", "wss://stream.data.alpaca.markets/v2/iex"),
        alpaca_trade_stream_url=os.getenv(
            "ALPACA_TRADE_STREAM_URL", "wss://paper-api.alpaca.markets/stream"
        ),
        enable_live_trading=os.getenv("ENABLE_LIVE_TRADING", "false").lower() == "true",
        admin_secret=os.getenv("ADMIN_SECRET", ""),
        enable_auto_promote=os.getenv("ENABLE_AUTO_PROMOTE", "false").lower() == "true",
        postgres_url=os.getenv("POSTGRES_URL", ""),
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        base_risk=float(os.getenv("BASE_RISK", "0.0025")),
        c_min=float(os.getenv("C_MIN", "0.55")),
        max_positions=int(os.getenv("MAX_POSITIONS", "10")),
        max_gross_exposure=float(os.getenv("MAX_GROSS_EXPOSURE", "1.5")),
        sector_concentration=float(os.getenv("SECTOR_CONCENTRATION", "0.25")),
        daily_max_loss=float(os.getenv("DAILY_MAX_LOSS", "0.03")),
        drawdown_max=float(os.getenv("DRAWDOWN_MAX", "0.1")),
    )
