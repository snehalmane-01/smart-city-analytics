from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from statistics import mean

from .ingestion import SensorRecord


@dataclass(frozen=True)
class Trend:
    metric: str
    city_zone: str
    average: float
    minimum: float
    maximum: float
    samples: int


class AnalyticsEngine:
    def calculate_trends(self, records: list[SensorRecord]) -> list[Trend]:
        grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
        for record in records:
            grouped[(record.metric, record.city_zone)].append(record.value)

        trends: list[Trend] = []
        for (metric, city_zone), values in grouped.items():
            trends.append(
                Trend(
                    metric=metric,
                    city_zone=city_zone,
                    average=mean(values),
                    minimum=min(values),
                    maximum=max(values),
                    samples=len(values),
                )
            )
        return sorted(trends, key=lambda trend: (trend.metric, trend.city_zone))

    def generate_report(self, generated_at: datetime, records: list[SensorRecord]) -> dict:
        return {
            "generated_at": generated_at.isoformat(),
            "record_count": len(records),
            "trends": [trend.__dict__ for trend in self.calculate_trends(records)],
        }
