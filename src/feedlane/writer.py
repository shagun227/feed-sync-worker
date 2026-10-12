import json
from pathlib import Path

from feedlane.models import CleanProduct, RejectedRecord, RunReport


def write_outputs(
    destination: Path,
    accepted: list[CleanProduct],
    rejected: list[RejectedRecord],
    report: RunReport,
) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    _write_json(destination / "products.json", [item.as_dict() for item in accepted])
    _write_json(destination / "rejects.json", [item.as_dict() for item in rejected])
    _write_json(destination / "report.json", report.as_dict())


def _write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
