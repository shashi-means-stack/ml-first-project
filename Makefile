install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	python -m pip install -e .

train:
	python -m first_ml_project.train --config config/train_config.yaml

test:
	pytest -q

docker-build:
	docker build -t first-ml-project .

docker-run:
	docker compose up --build
