# Smart City Analytics

Production-style starter implementation for a Smart City Analytics System with real-time MLOps pipeline.

## Included Components

1. Data ingestion service with schema validation, stream/batch ingest, and retries (`src/smart_city_analytics/ingestion.py`)
2. Stream processing with windowed aggregations and anomaly detection (`src/smart_city_analytics/processing.py`)
3. Model registry and versioning for traffic/air/energy/safety/anomaly models (`src/smart_city_analytics/models.py`)
4. FastAPI model-serving app (`src/smart_city_analytics/serving.py`)
5. Analytics engine with report generation (`src/smart_city_analytics/analytics.py`)
6. API gateway utilities for RBAC/rate-limiting (`src/smart_city_analytics/api_gateway.py`)
7. Frontend scaffold in React + TypeScript (`frontend/`)
8. Multi-database config abstraction (`src/smart_city_analytics/storage.py`)
9. Airflow DAG scaffold for retraining (`airflow/dags/retrain_pipeline.py`)
10. Docker/Kubernetes/Helm/Terraform infrastructure assets (`docker/`, `k8s/`, `helm/`, `terraform/`)
11. Monitoring configs for Prometheus/Grafana/alerts/Jaeger (`monitoring/`, `grafana-dashboards/`)
12. CI workflow for automated tests (`.github/workflows/ci.yml`)
13. Unit tests for ingestion, processing, registry, and analytics (`tests/`)
14. Architecture documentation (`docs/architecture.md`)

## Quickstart

```bash
python -m pip install -e .
python -m unittest discover -s tests -p 'test_*.py'
```
