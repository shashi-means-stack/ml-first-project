from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="iris_training",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    train_task = BashOperator(
        task_id="train_model",
        bash_command="python -m first_ml_project.train --config config/train_config.yaml",
    )
