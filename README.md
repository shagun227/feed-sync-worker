# Feedlane

Portfolio project by Shagun Sharma. A Docker-first Python worker that reads a raw JSONL product feed, normalizes it, and writes a clean catalog file plus a reject file. This is original sample code, not an employer pipeline.

## Stack

Python 3.11, Docker, Docker Compose, pytest. The image has no third-party runtime dependencies.

## Run locally

```bash
export PYTHONPATH=src
python3 -m feedlane --input sample-data/products.jsonl --output out
python3 -m pytest
```

`make test` and `make run` do the same thing.

## Run with Docker

```bash
docker compose up --build
```

The container reads `sample-data/products.jsonl` and writes:

- `out/products.json` for accepted rows
- `out/rejects.json` for rows that failed a rule
- `out/report.json` for counts

## What the worker checks

- Required fields: `sku`, `name`, `category`, `price`, `currency`
- SKU is trimmed, uppercased, and must not contain spaces
- Category must exist in the map (`eyewear` becomes `frames`, `contacts` becomes `lenses`)
- Price is stored in cents
- `on_hand` cannot be negative
- A second row with the same SKU is rejected

Pass a custom map with `--category-map categories.json`.

## Layout

```
src/feedlane/reader.py      JSONL input
src/feedlane/transform.py   field rules
src/feedlane/runner.py      dedupe and report
src/feedlane/writer.py      products, rejects, report
Dockerfile                  python:3.11-slim entrypoint
```
