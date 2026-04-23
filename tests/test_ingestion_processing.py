from datetime import datetime, timezone
import unittest

from smart_city_analytics.ingestion import DataIngestionService, SensorRecord, ValidationError
from smart_city_analytics.processing import StreamProcessor


class IngestionAndProcessingTests(unittest.TestCase):
    def test_ingestion_validates_and_publishes(self) -> None:
        published = []
        service = DataIngestionService(lambda record: published.append(record), retries=2)
        payload = {
            "source": "traffic_camera_1",
            "metric": "traffic_flow",
            "value": 12,
            "timestamp": "2026-01-01T00:00:00Z",
            "city_zone": "downtown",
        }
        records = service.ingest_batch([payload])
        self.assertEqual(len(records), 1)
        self.assertEqual(published[0].metric, "traffic_flow")

    def test_ingestion_rejects_invalid_schema(self) -> None:
        with self.assertRaises(ValidationError):
            SensorRecord.from_payload({"metric": "air_quality"})

    def test_window_aggregation(self) -> None:
        processor = StreamProcessor(window_seconds=60)
        base_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
        for index in range(3):
            record = SensorRecord(
                source="sensor",
                metric="air_quality",
                value=10 + index,
                timestamp=base_time,
                city_zone="zone-a",
            )
            aggregate = processor.process(record)
        self.assertEqual(aggregate.count, 3)
        self.assertEqual(aggregate.average, 11)


if __name__ == "__main__":
    unittest.main()
