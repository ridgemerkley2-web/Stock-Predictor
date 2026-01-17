"""Train and evaluate a simple stock price prediction model."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import yfinance as yf


@dataclass
class ModelConfig:
    symbol: str
    start: str
    end: str
    horizon_days: int
    test_size: float
    random_state: int
    model_name: str


FEATURE_COLUMNS = [
    "return_1d",
    "return_5d",
    "return_10d",
    "volatility_5d",
    "volatility_10d",
    "volume_change_1d",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train and backtest stock prediction models.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--symbol", default="AAPL", help="Ticker symbol to download.")
    common.add_argument("--start", default="2018-01-01", help="Start date (YYYY-MM-DD).")
    common.add_argument("--end", default=datetime.now().strftime("%Y-%m-%d"))
    common.add_argument("--horizon", type=int, default=1, help="Days ahead to predict.")
    common.add_argument(
        "--model",
        choices=["random_forest", "gradient_boosting"],
        default="random_forest",
        help="Model type to train.",
    )
    common.add_argument("--random-state", type=int, default=42)

    train_parser = subparsers.add_parser("train", parents=[common], help="Train a model.")
    train_parser.add_argument("--test-size", type=float, default=0.2)

    backtest_parser = subparsers.add_parser("backtest", parents=[common], help="Run a backtest.")
    backtest_parser.add_argument("--test-size", type=float, default=0.2)
    backtest_parser.add_argument("--initial-cash", type=float, default=10000)
    backtest_parser.add_argument("--position-size", type=float, default=1.0)

    subparsers.add_parser("assist", help="Interactive assistant for running the workflow.")

    return parser.parse_args()


def build_config(args: argparse.Namespace) -> ModelConfig:
    return ModelConfig(
        symbol=args.symbol,
        start=args.start,
        end=args.end,
        horizon_days=args.horizon,
        test_size=args.test_size,
        random_state=args.random_state,
        model_name=args.model,
    )


def load_data(config: ModelConfig) -> pd.DataFrame:
    data = yf.download(config.symbol, start=config.start, end=config.end, progress=False)
    if data.empty:
        raise ValueError("No data returned for the given ticker/date range.")
    return data


def engineer_features(data: pd.DataFrame, horizon_days: int) -> pd.DataFrame:
    df = data.copy()
    df["return_1d"] = df["Close"].pct_change()
    df["return_5d"] = df["Close"].pct_change(5)
    df["return_10d"] = df["Close"].pct_change(10)
    df["volatility_5d"] = df["Close"].pct_change().rolling(5).std()
    df["volatility_10d"] = df["Close"].pct_change().rolling(10).std()
    df["volume_change_1d"] = df["Volume"].pct_change()
    df["target"] = df["Close"].shift(-horizon_days)
    df = df.dropna()
    return df


def split_features_targets(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    X = df[FEATURE_COLUMNS]
    y = df["target"]
    return X, y


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_name: str,
    random_state: int,
) -> RandomForestRegressor | GradientBoostingRegressor:
    if model_name == "gradient_boosting":
        model = GradientBoostingRegressor(random_state=random_state)
    else:
        model = RandomForestRegressor(
            n_estimators=300,
            random_state=random_state,
            n_jobs=-1,
        )
    model.fit(X_train, y_train)
    return model


def evaluate_model(
    model: RandomForestRegressor | GradientBoostingRegressor,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> Tuple[float, float]:
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    return mae, rmse


def backtest_strategy(
    data: pd.DataFrame,
    features: pd.DataFrame,
    model_name: str,
    horizon_days: int,
    initial_cash: float,
    position_size: float,
    random_state: int,
) -> Dict[str, float]:
    X, y = split_features_targets(features)
    split_index = int(len(features) * 0.8)
    X_train, y_train = X.iloc[:split_index], y.iloc[:split_index]
    X_test, y_test = X.iloc[split_index:], y.iloc[split_index:]
    model = train_model(X_train, y_train, model_name, random_state)

    predictions = model.predict(X_test)
    actual_prices = data.loc[features.index, "Close"].iloc[split_index:]
    current_prices = actual_prices.shift(horizon_days).dropna()
    predicted_prices = pd.Series(predictions, index=actual_prices.index)
    predicted_returns = (predicted_prices - current_prices) / current_prices
    predicted_returns = predicted_returns.reindex(actual_prices.index).fillna(0)

    cash = initial_cash
    holdings = 0.0
    equity_curve: List[float] = []

    for date, price in actual_prices.items():
        signal = predicted_returns.loc[date]
        if signal > 0:
            target_value = cash * position_size
            shares_to_buy = target_value / price
            holdings += shares_to_buy
            cash -= shares_to_buy * price
        elif signal < 0 and holdings > 0:
            cash += holdings * price
            holdings = 0.0

        total_value = cash + holdings * price
        equity_curve.append(total_value)

    equity_series = pd.Series(equity_curve, index=actual_prices.index)
    returns = equity_series.pct_change().fillna(0)
    total_return = equity_series.iloc[-1] / initial_cash - 1
    volatility = returns.std() * np.sqrt(252)
    sharpe = (returns.mean() * 252) / volatility if volatility > 0 else 0.0
    max_drawdown = ((equity_series / equity_series.cummax()) - 1).min()

    mae, rmse = evaluate_model(model, X_test, y_test)

    return {
        "total_return": total_return,
        "annualized_volatility": volatility,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_drawdown,
        "mae": mae,
        "rmse": rmse,
    }


def run_assistant() -> argparse.Namespace:
    print("Welcome to the Stock Predictor Assistant!")
    symbol = input("Ticker symbol (default: AAPL): ").strip() or "AAPL"
    start = input("Start date YYYY-MM-DD (default: 2018-01-01): ").strip() or "2018-01-01"
    default_end = datetime.now().strftime("%Y-%m-%d")
    end_prompt = f"End date YYYY-MM-DD (default: {default_end}): "
    end = input(end_prompt).strip() or default_end
    horizon = int(input("Prediction horizon in days (default: 1): ").strip() or "1")
    model = input("Model [random_forest|gradient_boosting] (default: random_forest): ").strip() or "random_forest"
    mode = input("Choose action [train|backtest] (default: train): ").strip() or "train"
    test_size = float(input("Test size (default: 0.2): ").strip() or "0.2")

    args = argparse.Namespace(
        command=mode,
        symbol=symbol,
        start=start,
        end=end,
        horizon=horizon,
        model=model,
        random_state=42,
        test_size=test_size,
        initial_cash=10000.0,
        position_size=1.0,
    )
    return args


def main() -> None:
    args = parse_args()
    if args.command == "assist":
        args = run_assistant()

    config = build_config(args)
    data = load_data(config)
    features = engineer_features(data, config.horizon_days)

    if args.command == "train":
        X, y = split_features_targets(features)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=config.test_size, random_state=config.random_state, shuffle=False
        )
        model = train_model(X_train, y_train, config.model_name, config.random_state)
        mae, rmse = evaluate_model(model, X_test, y_test)
        print("Model trained successfully!")
        print(f"Mean Absolute Error: {mae:.4f}")
        print(f"Root Mean Squared Error: {rmse:.4f}")
        return

    if args.command == "backtest":
        results = backtest_strategy(
            data=data,
            features=features,
            model_name=config.model_name,
            horizon_days=config.horizon_days,
            initial_cash=args.initial_cash,
            position_size=args.position_size,
            random_state=config.random_state,
        )
        print("Backtest results:")
        for metric, value in results.items():
            print(f"- {metric.replace('_', ' ').title()}: {value:.4f}")
        return

    raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
