FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

COPY src ./src
COPY sample-data ./sample-data

RUN mkdir -p /data/in /data/out \
    && cp sample-data/products.jsonl /data/in/products.jsonl

ENTRYPOINT ["python", "-m", "feedlane"]
CMD ["--input", "/data/in/products.jsonl", "--output", "/data/out"]
