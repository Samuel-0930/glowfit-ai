from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.glowfit.ingestion import ingest_amazon_beauty_jsonl  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Amazon Beauty-style metadata and review JSONL into GlowFit artifacts."
    )
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--reviews", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/amazon_beauty"))
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    summary = ingest_amazon_beauty_jsonl(
        metadata_path=args.metadata,
        reviews_path=args.reviews,
        output_dir=args.output_dir,
        limit=args.limit,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
