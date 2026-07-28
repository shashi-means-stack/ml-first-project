from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any

import joblib
import mlflow
import pandas as pd
import yaml
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def train_model(config: dict[str, Any]) -> dict[str, Any]:
    iris = load_iris(as_frame=True)
    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config["test_size"], random_state=config["random_state"]
    )

    model = LogisticRegression(max_iter=config["max_iter"], random_state=config["random_state"])
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    metrics = {"accuracy": float(accuracy)}

    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / "model.joblib"
    joblib.dump(model, model_path)

    metrics_path = output_dir / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as fh:
        json.dump(metrics, fh, indent=2)

    return {"model_path": str(model_path), "metrics": metrics}


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a simple iris classifier")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config")
    args = parser.parse_args()

    config = load_config(args.config)
    os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")
    tracking_uri = config.get("mlflow_uri", "file://./mlruns")
    if tracking_uri.startswith("E:/"):
        tracking_uri = tracking_uri.replace("E:/", "file:///E:/")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(config.get("mlflow_experiment", "first-ml-project"))

    with mlflow.start_run(run_name=config.get("run_name", "baseline")):
        result = train_model(config)
        mlflow.log_params({
            "test_size": config["test_size"],
            "random_state": config["random_state"],
            "max_iter": config["max_iter"],
        })
        mlflow.log_metrics(result["metrics"])
        mlflow.log_artifact(str(Path(result["model_path"])))
        mlflow.log_artifact(str(Path(config["output_dir"]) / "metrics.json"))
        logger.info("Training complete with metrics: %s", result["metrics"])


if __name__ == "__main__":
    main()
