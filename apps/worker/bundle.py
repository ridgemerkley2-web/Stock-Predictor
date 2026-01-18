import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict


@dataclass
class Bundle:
    bundle_id: str
    name: str
    parameters: Dict[str, object]
    metrics: Dict[str, object]
    holdout_metrics: Dict[str, object]
    metadata: Dict[str, object]
    created_at: str


def save_bundle(bundle: Bundle, folder: str = "bundles") -> Path:
    path = Path(folder)
    path.mkdir(parents=True, exist_ok=True)
    bundle_path = path / f"{bundle.bundle_id}.json"
    bundle_path.write_text(json.dumps(asdict(bundle), indent=2))
    return bundle_path


def create_bundle(
    bundle_id: str,
    name: str,
    parameters: Dict[str, object],
    metrics: Dict[str, object],
    holdout_metrics: Dict[str, object],
    metadata: Dict[str, object],
) -> Bundle:
    return Bundle(
        bundle_id=bundle_id,
        name=name,
        parameters=parameters,
        metrics=metrics,
        holdout_metrics=holdout_metrics,
        metadata=metadata,
        created_at=datetime.utcnow().isoformat(),
    )
