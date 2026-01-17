# Stock-Predictor

This project provides a simple stock price prediction workflow built with Python, pandas, and scikit-learn.
It downloads historical data, engineers return-based features, trains a model, and reports evaluation metrics.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Train a model

```bash
python src/stock_predictor.py train --symbol AAPL --start 2018-01-01 --end 2024-01-01 --horizon 1
```

## Backtest a strategy

```bash
python src/stock_predictor.py backtest --symbol AAPL --start 2018-01-01 --end 2024-01-01 --horizon 1
```

## Run the interactive assistant

```bash
python src/stock_predictor.py assist
```

### Optional configuration

- `--symbol`: Stock ticker symbol (default: `AAPL`).
- `--start`: Start date in `YYYY-MM-DD` format (default: `2018-01-01`).
- `--end`: End date in `YYYY-MM-DD` format (default: today).
- `--horizon`: Days ahead to predict (default: `1`).
- `--test-size`: Fraction of samples used for the test set (default: `0.2`).
- `--model`: Model type (`random_forest` or `gradient_boosting`).

## Notes

- The model predicts the next closing price using lagged returns and volatility features.
- The script relies on the `yfinance` package to fetch market data.
