from datetime import datetime, timezone
import unittest

from smart_city_analytics.analytics import AnalyticsEngine
from smart_city_analytics.ingestion import SensorRecord
from smart_city_analytics.models import ModelRegistry


class ModelAndAnalyticsTests(unittest.TestCase):
    def test_model_registry_versions(self) -> None:
        registry = ModelRegistry()
        first = registry.register("traffic_lstm", {"rmse": 0.2})
        second = registry.register("traffic_lstm", {"rmse": 0.15})
        self.assertEqual(first.version, 1)
        self.assertEqual(second.version, 2)

    def test_analytics_report(self) -> None:
        engine = AnalyticsEngine()
        records = [
            SensorRecord("sensor-a", "energy", 100.0, datetime(2026, 1, 1, tzinfo=timezone.utc), "z1"),
            SensorRecord("sensor-b", "energy", 80.0, datetime(2026, 1, 1, tzinfo=timezone.utc), "z1"),
        ]
        report = engine.generate_report(datetime(2026, 1, 2, tzinfo=timezone.utc), records)
        self.assertEqual(report["record_count"], 2)
        self.assertEqual(report["trends"][0]["average"], 90.0)


if __name__ == "__main__":
    unittest.main()
