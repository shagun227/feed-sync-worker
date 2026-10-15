# Architecture

Feedlane keeps HTTP or CLI code away from the rules. The path is JSONL file → Transform → Runner → products.json.

See `images/architecture.svg`.
