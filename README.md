# First ML Project

A compact, production-oriented machine learning starter project that includes:

- a reproducible training pipeline
- DVC pipeline definitions
- MLflow experiment tracking
- Docker and Docker Compose support
- Airflow orchestration
- GitHub Actions CI

## Project structure

- `src/first_ml_project/` — training code and package
- `config/` — YAML configuration
- `data/` — datasets tracked by DVC
- `artifacts/` — model and metrics outputs
- `airflow/` — example DAG
- `.github/workflows/` — CI pipeline

## Quick start

1. Create and activate a Python environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Install the package in editable mode: `pip install -e .`
4. Run training: `python -m first_ml_project.train --config config/train_config.yaml`
5. Inspect MLflow runs in `mlruns/`.

For a full step-by-step guide, see [RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md).

## Commands

- `make install`
- `make train`
- `make test`
- `docker compose up --build`
- `dvc repro`
