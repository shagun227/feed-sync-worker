PYTHONPATH := src
export PYTHONPATH

.PHONY: test run docker

test:
	python3 -m pytest

run:
	python3 -m feedlane --input sample-data/products.jsonl --output out

docker:
	docker compose up --build
