import argparse
from datetime import datetime

from bundle import create_bundle, save_bundle


def ingest() -> None:
    print("Ingesting market data...")


def research() -> None:
    print("Running walk-forward optimization...")
    bundle = create_bundle(
        bundle_id=f"bundle-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        name="baseline",
        parameters={"c_min": 0.55},
        metrics={"sharpe": 1.1, "max_drawdown": 0.08, "trades": 120, "win_rate": 0.52},
        holdout_metrics={"sharpe": 0.9, "max_drawdown": 0.1, "trades": 30, "win_rate": 0.5},
        metadata={"universe": "top2000", "commit": "dev"},
    )
    path = save_bundle(bundle)
    print(f"Saved bundle to {path}")


def run_live() -> None:
    print("Starting live worker (paper default)...")


def promote(bundle_id: str) -> None:
    print(f"Promoting bundle {bundle_id}")


def select_bundle(bundle_id: str) -> None:
    print(f"Selecting bundle {bundle_id} for trading")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stock Predictor CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("ingest")
    sub.add_parser("research")
    sub.add_parser("run-live")

    promote_parser = sub.add_parser("promote")
    promote_parser.add_argument("--bundle-id", required=True)

    select_parser = sub.add_parser("select-bundle")
    select_parser.add_argument("--bundle-id", required=True)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "ingest":
        ingest()
    elif args.command == "research":
        research()
    elif args.command == "run-live":
        run_live()
    elif args.command == "promote":
        promote(args.bundle_id)
    elif args.command == "select-bundle":
        select_bundle(args.bundle_id)


if __name__ == "__main__":
    main()
