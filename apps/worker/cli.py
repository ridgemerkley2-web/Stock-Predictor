import argparse
from datetime import datetime

import torch
from torch.utils.data import DataLoader, random_split

from bundle import create_bundle, save_bundle
from models import list_model_specs
from neural.dataset import SequenceConfig, load_sequence_csv
from neural.models import LSTMModel, TCNModel, TemporalFusionTransformer, TemporalTransformer
from neural.trainer import TrainConfig, train_model


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


def train_model_cli(args: argparse.Namespace) -> None:
    specs = {spec.name: spec for spec in list_model_specs()}
    if args.model_name not in specs:
        raise ValueError(f"Unknown model {args.model_name}. Available: {', '.join(specs)}")

    config = SequenceConfig(
        feature_cols=args.feature_cols.split(","),
        target_col=args.target_col,
        sequence_length=args.sequence_length,
    )
    dataset = load_sequence_csv(args.data_path, config)
    train_size = int(len(dataset) * 0.8)
    val_size = len(dataset) - train_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size)

    feature_dim = len(config.feature_cols)
    params = specs[args.model_name].default_params
    model_map = {
        "temporal_transformer": TemporalTransformer(
            feature_dim, params["d_model"], params["n_heads"], params["layers"], params["dropout"]
        ),
        "temporal_fusion_transformer": TemporalFusionTransformer(
            feature_dim, params["hidden_size"], params["attention_heads"], params["dropout"]
        ),
        "lstm": LSTMModel(feature_dim, params["hidden_size"], params["layers"], params["dropout"]),
        "tcn": TCNModel(feature_dim, params["channels"], params["kernel_size"], params["dropout"]),
    }
    model = model_map[args.model_name]

    train_config = TrainConfig(
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
    )
    metrics = train_model(model, train_loader, val_loader, train_config, device=args.device)
    torch.save(model.state_dict(), args.output_path)
    print(f"Saved model to {args.output_path} with metrics {metrics}")


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

    train_parser = sub.add_parser("train-model")
    train_parser.add_argument("--data-path", required=True)
    train_parser.add_argument("--feature-cols", required=True)
    train_parser.add_argument("--target-col", required=True)
    train_parser.add_argument("--sequence-length", type=int, default=20)
    train_parser.add_argument("--model-name", default="temporal_transformer")
    train_parser.add_argument("--epochs", type=int, default=5)
    train_parser.add_argument("--learning-rate", type=float, default=1e-3)
    train_parser.add_argument("--batch-size", type=int, default=128)
    train_parser.add_argument("--device", default="cpu")
    train_parser.add_argument("--output-path", default="trained_model.pt")

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
    elif args.command == "train-model":
        train_model_cli(args)


if __name__ == "__main__":
    main()
