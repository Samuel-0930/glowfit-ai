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
    fetch_huggingface_search_rows,
)
from src.glowfit.huggingface_preview import (  # noqa: E402
    HuggingFaceDatasetUnavailable,
    fetch_huggingface_rows,
)


def _log(message: str, quiet: bool) -> None:
    if not quiet:
        print(message, file=sys.stderr, flush=True)


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
    parser.add_argument("--min-reviews-per-product", type=int, default=3)
    parser.add_argument("--metadata-search-length", type=int, default=5)
    parser.add_argument("--metadata-search-timeout", type=int, default=5)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    _log(
        "Fetching ASIN-joined Hugging Face preview "
        f"(target={args.target_matches}, max_review_rows={args.max_review_rows})",
        args.quiet,
    )

    def fetch_rows_with_progress(
        dataset: str, config: str, split: str, offset: int, length: int
    ) -> list[dict]:
        _log(f"Fetching review rows offset={offset} length={length}", args.quiet)
        rows = fetch_huggingface_rows(dataset, config, split, offset, length)
        _log(f"Fetched {len(rows)} review rows", args.quiet)
        return rows

    def search_rows_with_progress(
        dataset: str, config: str, split: str, query: str, offset: int, length: int
    ) -> list[dict]:
        _log(f"Searching metadata ASIN={query}", args.quiet)
        rows = fetch_huggingface_search_rows(
            dataset=dataset,
            config=config,
            split=split,
            query=query,
            offset=offset,
            length=length,
            timeout=args.metadata_search_timeout,
        )
        status = "match candidates" if rows else "no candidates/timeout"
        _log(f"Metadata search ASIN={query}: {len(rows)} {status}", args.quiet)
        return rows

    try:
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
            min_reviews_per_product=args.min_reviews_per_product,
            metadata_search_length=args.metadata_search_length,
            fetch_rows=fetch_rows_with_progress,
            search_rows=search_rows_with_progress,
        )
    except HuggingFaceDatasetUnavailable as error:
        parser.exit(2, f"Data fetch failed: {error}\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
