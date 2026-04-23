from dataclasses import dataclass


@dataclass(frozen=True)
class Metric:
    name: str
    value: float
    labels: dict[str, str]


def to_prometheus_line(metric: Metric) -> str:
    label_blob = ",".join(f'{k}="{v}"' for k, v in sorted(metric.labels.items()))
    return f"{metric.name}{{{label_blob}}} {metric.value}"
