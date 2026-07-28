# Run and Component Guide

This document explains how to run the project and what each component does.

## 1. Prerequisites

Install the following tools:

- Python 3.10+
- pip
- Docker (optional, for containerized runs)
- Docker Compose (optional)
- Git

## 2. Clone and enter the project

```bash
git clone <your-repo-url>
cd first-ml-project
```

## 3. Create a virtual environment

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## 5. Run tests

```bash
pytest -q
```

## 6. Train the model

```bash
python -m first_ml_project.train --config config/train_config.yaml
```

This creates:

- artifacts/model.joblib
- artifacts/metrics.json
- MLflow tracking logs under mlruns/

## 7. Run with DVC

Initialize DVC if needed:

```bash
dvc init
```

Run the pipeline:

```bash
dvc repro
```

## 8. Run the prediction API

Start the API server:

```bash
uvicorn first_ml_project.predict_api:app --reload
```

Then open:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

Example request body:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

## 9. Run with Docker

Build and run:

```bash
docker compose up --build
```

## 9. Run with Airflow

Airflow example DAG is available in:

- airflow/iris_dag.py

To use it, place the DAG file into your Airflow DAGs folder and start Airflow.

## 10. CI/CD

GitHub Actions workflows are already configured in:

- .github/workflows/ci.yml
- .github/workflows/docker.yml

These run tests and Docker build automatically on push and pull request.

## Project components

### Python package
- src/first_ml_project/train.py: training pipeline entry point
- src/first_ml_project/__init__.py: package marker

### Configuration
- config/train_config.yaml: training parameters

### Data
- data/: folder for datasets

### Artifacts
- artifacts/: output model and metrics

### Experiment tracking
- MLflow logs are stored in mlruns/

### Pipeline orchestration
- dvc.yaml: DVC pipeline definition
- airflow/iris_dag.py: Airflow example DAG

### Automation
- Makefile: common commands
- .github/workflows/: CI automation
