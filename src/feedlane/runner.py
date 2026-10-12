from pathlib import Path

from feedlane.models import CleanProduct, RejectedRecord, RunReport
from feedlane.reader import read_jsonl
from feedlane.transform import normalize
from feedlane.writer import write_outputs

DEFAULT_CATEGORY_MAP = {
    "eyewear": "frames",
    "frames": "frames",
    "frame": "frames",
    "contacts": "lenses",
    "lens": "lenses",
    "lenses": "lenses",
}


def run(source: Path, destination: Path, category_map: dict[str, str] | None = None) -> RunReport:
    mapping = category_map or DEFAULT_CATEGORY_MAP
    accepted: list[CleanProduct] = []
    rejected: list[RejectedRecord] = []
    report = RunReport()
    seen: set[str] = set()

    for record in read_jsonl(source):
        result = normalize(record, mapping)
        if isinstance(result, RejectedRecord):
            rejected.append(result)
            report.add_reject(result.reason)
            continue
        if result.sku in seen:
            duplicate = RejectedRecord(record.line_number, "duplicate sku", record.payload)
            rejected.append(duplicate)
            report.add_reject(duplicate.reason)
            continue
        seen.add(result.sku)
        accepted.append(result)
        report.accepted += 1

    write_outputs(destination, accepted, rejected, report)
    return report
