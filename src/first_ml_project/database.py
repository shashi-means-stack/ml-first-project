from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "predictions.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            prediction INTEGER NOT NULL,
            prediction_name TEXT NOT NULL,
            model_path TEXT NOT NULL,
            metrics TEXT NOT NULL,
            features TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def load_predictions() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, timestamp, prediction, prediction_name, model_path, metrics, features FROM predictions ORDER BY id DESC"
        ).fetchall()
        return [
            {
                "id": row["id"],
                "timestamp": row["timestamp"],
                "prediction": row["prediction"],
                "prediction_name": row["prediction_name"],
                "model_path": row["model_path"],
                "metrics": json.loads(row["metrics"]),
                "features": json.loads(row["features"]),
            }
            for row in rows
        ]


def save_prediction(payload: dict[str, Any]) -> dict[str, Any]:
    timestamp = datetime.utcnow().isoformat() + "Z"
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO predictions (timestamp, prediction, prediction_name, model_path, metrics, features)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                payload["prediction"],
                payload["prediction_name"],
                payload["model_path"],
                json.dumps(payload["metrics"]),
                json.dumps(payload["features"]),
            ),
        )
        conn.commit()
        return {
            "id": cursor.lastrowid,
            "timestamp": timestamp,
            **payload,
        }
