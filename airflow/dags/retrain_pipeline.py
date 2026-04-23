from datetime import datetime

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except Exception:  # pragma: no cover
    DAG = None


def retrain_models() -> None:
    print("Retraining triggered")


if DAG is not None:
    with DAG(
        dag_id="smart_city_model_retraining",
        start_date=datetime(2026, 1, 1),
        schedule="@daily",
        catchup=False,
    ) as dag:
        PythonOperator(task_id="retrain_models", python_callable=retrain_models)
