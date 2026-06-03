from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.glowfit.huggingface_joined_preview import (  # noqa: E402
    fetch_and_write_joined_huggingface_preview,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch a small ASIN-joined Hugging Face preview into GlowFit artifacts."
    )
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/hf_joined_preview"))
    parser.add_argument("--metadata-dataset", default="smartcat/Amazon_All_Beauty_2023")
    parser.add_argument("--reviews-dataset", default="jhan21/amazon-beauty-reviews-dataset")
    parser.add_argument("--config", default="default")
    parser.add_argument("--split", default="train")
    parser.add_argument("--review-offset", type=int, default=0)
    parser.add_argument("--target-matches", type=int, default=25)
    parser.add_argument("--review-page-size", type=int, default=25)
    parser.add_argument("--max-review-rows", type=int, default=250)
    parser.add_argument("--metadata-search-length", type=int, default=5)
    args = parser.parse_args()

    summary = fetch_and_write_joined_huggingface_preview(
        output_dir=args.output_dir,
        metadata_dataset=args.metadata_dataset,
        reviews_dataset=args.reviews_dataset,
        config=args.config,
        split=args.split,
        review_offset=args.review_offset,
        target_matches=args.target_matches,
        review_page_size=args.review_page_size,
        max_review_rows=args.max_review_rows,
        metadata_search_length=args.metadata_search_length,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
