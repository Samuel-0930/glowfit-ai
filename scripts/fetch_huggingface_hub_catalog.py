from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.glowfit.huggingface_hub_catalog import (  # noqa: E402
    HuggingFaceHubUnavailable,
    fetch_and_write_huggingface_hub_catalog,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build a joined GlowFit catalog from Hugging Face Hub files without Dataset Viewer."
        )
    )
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/hf_hub_catalog"))
    parser.add_argument("--cache-dir", type=Path, default=Path("data/raw/huggingface"))
    parser.add_argument("--max-products", type=int, default=25)
    parser.add_argument("--min-reviews-per-product", type=int, default=3)
    parser.add_argument("--max-reviews-per-product", type=int, default=20)
    parser.add_argument("--max-review-rows", type=int, default=100_000)
    args = parser.parse_args()

    try:
        summary = fetch_and_write_huggingface_hub_catalog(
            output_dir=args.output_dir,
            cache_dir=args.cache_dir,
            max_products=args.max_products,
            min_reviews_per_product=args.min_reviews_per_product,
            max_reviews_per_product=args.max_reviews_per_product,
            max_review_rows=args.max_review_rows,
        )
    except (HuggingFaceHubUnavailable, RuntimeError) as error:
        parser.exit(2, f"Data fetch failed: {error}\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
