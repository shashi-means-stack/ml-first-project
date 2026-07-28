FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml .
COPY src ./src
COPY config ./config
COPY templates ./templates
COPY tests ./tests

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["python", "-m", "first_ml_project.train", "--config", "config/train_config.yaml"]
