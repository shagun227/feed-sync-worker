import json
from pathlib import Path

from feedlane.runner import run

SAMPLE = Path(__file__).resolve().parents[1] / "sample-data" / "products.jsonl"


def test_run_splits_accepted_and_rejected(tmp_path: Path):
    report = run(SAMPLE, tmp_path)
    assert report.accepted == 2
    assert report.rejected == 3

    products = json.loads((tmp_path / "products.json").read_text())
    rejects = json.loads((tmp_path / "rejects.json").read_text())
    assert [item["sku"] for item in products] == ["FRAME-100", "LENS-200"]
    assert {item["reason"] for item in rejects} == {
        "missing name",
        "unknown category 'accessories'",
        "duplicate sku",
    }
