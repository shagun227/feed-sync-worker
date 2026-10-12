import argparse
import json
from pathlib import Path

from feedlane.runner import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize a raw product feed.")
    parser.add_argument("--input", required=True, type=Path, help="JSONL feed path")
    parser.add_argument("--output", required=True, type=Path, help="Directory for clean files")
    parser.add_argument(
        "--category-map",
        type=Path,
        help="Optional JSON object mapping source categories to catalog slugs",
    )
    args = parser.parse_args()

    category_map = None
    if args.category_map:
        category_map = json.loads(args.category_map.read_text(encoding="utf-8"))

    report = run(args.input, args.output, category_map)
    print(json.dumps(report.as_dict()))


if __name__ == "__main__":
    main()
