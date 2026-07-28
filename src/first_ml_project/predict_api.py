from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

import joblib
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from first_ml_project.auth import require_api_token
from first_ml_project.database import load_predictions, save_prediction

app = FastAPI(title="First ML Project API", version="1.0.0")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "templates"))

MODEL_PATH = PROJECT_ROOT / "artifacts" / "model.joblib"
METRICS_PATH = PROJECT_ROOT / "artifacts" / "metrics.json"

if not MODEL_PATH.exists():
    raise FileNotFoundError("Model artifact not found. Train the model first.")

model = joblib.load(MODEL_PATH)


class PredictionRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class PredictionResponse(BaseModel):
    prediction: int
    prediction_name: str
    model_path: str
    metrics: dict[str, Any]


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/auth-status")
def auth_status() -> dict[str, str]:
    return {"status": "public"}


@app.get("/history")
def history(_: Annotated[None, Depends(require_api_token)]) -> list[dict[str, Any]]:
    return load_predictions()


@app.get("/metrics")
def get_metrics() -> dict[str, Any]:
    if not METRICS_PATH.exists():
        raise HTTPException(status_code=404, detail="Metrics not found")
    with open(METRICS_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


@app.post("/predict", response_model=PredictionResponse)
def predict(
    request: PredictionRequest,
    _: Annotated[None, Depends(require_api_token)],
) -> PredictionResponse:
    features = [[
        request.sepal_length,
        request.sepal_width,
        request.petal_length,
        request.petal_width,
    ]]
    prediction = int(model.predict(features)[0])
    class_names = ["setosa", "versicolor", "virginica"]
    metrics = get_metrics()
    record = save_prediction({
        "prediction": prediction,
        "prediction_name": class_names[prediction],
        "model_path": str(MODEL_PATH),
        "metrics": metrics,
        "features": {
            "sepal_length": request.sepal_length,
            "sepal_width": request.sepal_width,
            "petal_length": request.petal_length,
            "petal_width": request.petal_width,
        },
    })
    return PredictionResponse(
        prediction=prediction,
        prediction_name=class_names[prediction],
        model_path=str(MODEL_PATH),
        metrics=metrics,
    )
