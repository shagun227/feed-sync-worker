import json
from pathlib import Path

from feedlane.models import RawRecord


class FeedReadError(ValueError):
    pass


def read_jsonl(path: Path) -> list[RawRecord]:
    if not path.is_file():
        raise FeedReadError(f"Input file not found: {path}")

    records: list[RawRecord] = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise FeedReadError(f"Line {index} is not valid JSON: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise FeedReadError(f"Line {index} must be a JSON object")
        records.append(RawRecord(line_number=index, payload=payload))
    return records
