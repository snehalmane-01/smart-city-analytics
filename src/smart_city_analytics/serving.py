from __future__ import annotations

from typing import Any

from .models import ModelRegistry

try:
    from fastapi import FastAPI, HTTPException
except Exception:  # noqa: BLE001
    FastAPI = None
    HTTPException = RuntimeError


def create_app(model_registry: ModelRegistry | None = None):
    if FastAPI is None:
        raise RuntimeError("FastAPI is required to run the serving API")

    registry = model_registry or ModelRegistry()
    app = FastAPI(title="Smart City Analytics Model Serving", version="1.0.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/models")
    def models() -> dict[str, list[dict[str, Any]]]:
        return registry.list_models()

    @app.post("/predict/{model_name}")
    def predict(model_name: str, payload: dict[str, float]) -> dict[str, Any]:
        try:
            model = registry.latest(model_name)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        score = sum(payload.values())
        return {"model": model_name, "version": model["version"], "prediction": score}

    return app
