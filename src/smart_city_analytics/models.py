from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class ModelVersion:
    name: str
    version: int
    framework: str
    created_at: str
    metrics: dict[str, float]


class ModelRegistry:
    """In-memory model registry compatible with experiment tracking metadata."""

    DEFAULT_MODELS = {
        "traffic_lstm": "tensorflow",
        "traffic_prophet": "prophet",
        "air_quality_xgboost": "xgboost",
        "air_quality_lightgbm": "lightgbm",
        "energy_neural_network": "tensorflow",
        "safety_gradient_boosting": "scikit-learn",
        "anomaly_isolation_forest": "scikit-learn",
        "anomaly_autoencoder": "tensorflow",
    }

    def __init__(self) -> None:
        self._versions: dict[str, list[ModelVersion]] = {name: [] for name in self.DEFAULT_MODELS}

    def register(self, name: str, metrics: dict[str, float], framework: str | None = None) -> ModelVersion:
        if name not in self._versions:
            self._versions[name] = []
        version = len(self._versions[name]) + 1
        model = ModelVersion(
            name=name,
            version=version,
            framework=framework or self.DEFAULT_MODELS.get(name, "unknown"),
            created_at=datetime.now(timezone.utc).isoformat(),
            metrics=metrics,
        )
        self._versions[name].append(model)
        return model

    def latest(self, name: str) -> dict:
        if not self._versions.get(name):
            raise KeyError(f"No versions registered for {name}")
        return asdict(self._versions[name][-1])

    def list_models(self) -> dict[str, list[dict]]:
        return {name: [asdict(v) for v in versions] for name, versions in self._versions.items()}
