from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Iterable


class ValidationError(ValueError):
    """Raised when sensor payloads fail schema validation."""


@dataclass(frozen=True)
class SensorRecord:
    source: str
    metric: str
    value: float
    timestamp: datetime
    city_zone: str

    @classmethod
    def from_payload(cls, payload: dict) -> "SensorRecord":
        required = {"source", "metric", "value", "timestamp", "city_zone"}
        missing = required - payload.keys()
        if missing:
            raise ValidationError(f"Missing required keys: {sorted(missing)}")

        try:
            ts = datetime.fromisoformat(str(payload["timestamp"]).replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValidationError("timestamp must be ISO-8601") from exc

        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)

        return cls(
            source=str(payload["source"]),
            metric=str(payload["metric"]),
            value=float(payload["value"]),
            timestamp=ts,
            city_zone=str(payload["city_zone"]),
        )


class DataIngestionService:
    """Validates and ingests IoT payloads with retry support."""

    def __init__(self, publish_func: Callable[[SensorRecord], None], retries: int = 3) -> None:
        self._publish = publish_func
        self.retries = max(1, retries)

    def ingest_stream(self, payloads: Iterable[dict]) -> list[SensorRecord]:
        records: list[SensorRecord] = []
        for payload in payloads:
            record = SensorRecord.from_payload(payload)
            self._publish_with_retry(record)
            records.append(record)
        return records

    def ingest_batch(self, payloads: list[dict]) -> list[SensorRecord]:
        return self.ingest_stream(payloads)

    def _publish_with_retry(self, record: SensorRecord) -> None:
        last_error: Exception | None = None
        for _ in range(self.retries):
            try:
                self._publish(record)
                return
            except Exception as exc:  # noqa: BLE001
                last_error = exc
        raise RuntimeError(f"Failed to publish record after {self.retries} retries") from last_error
