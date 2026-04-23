from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from statistics import mean, pstdev

from .ingestion import SensorRecord


@dataclass(frozen=True)
class WindowAggregate:
    metric: str
    city_zone: str
    window_start: datetime
    window_end: datetime
    average: float
    count: int


class StreamProcessor:
    """Windowed aggregations and simple anomaly detection for stream records."""

    def __init__(self, window_seconds: int = 60, max_state: int = 1000) -> None:
        self.window = timedelta(seconds=max(1, window_seconds))
        self.state: dict[tuple[str, str], deque[SensorRecord]] = defaultdict(deque)
        self.max_state = max_state

    def process(self, record: SensorRecord) -> WindowAggregate:
        key = (record.metric, record.city_zone)
        queue = self.state[key]
        queue.append(record)

        threshold = record.timestamp - self.window
        while queue and queue[0].timestamp < threshold:
            queue.popleft()
        while len(queue) > self.max_state:
            queue.popleft()

        avg = mean([r.value for r in queue])
        return WindowAggregate(
            metric=record.metric,
            city_zone=record.city_zone,
            window_start=threshold,
            window_end=record.timestamp,
            average=avg,
            count=len(queue),
        )

    def detect_anomaly(self, record: SensorRecord, sigma: float = 3.0) -> bool:
        key = (record.metric, record.city_zone)
        values = [r.value for r in self.state.get(key, [])]
        if len(values) < 3:
            return False
        std = pstdev(values)
        if std == 0:
            return False
        return abs(record.value - mean(values)) > sigma * std
