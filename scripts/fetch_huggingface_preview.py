from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.glowfit.huggingface_preview import fetch_and_write_huggingface_preview  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch a small Hugging Face Dataset Viewer preview into GlowFit artifacts."
    )
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/hf_preview"))
    parser.add_argument("--metadata-dataset", default="smartcat/Amazon_All_Beauty_2023")
    parser.add_argument("--reviews-dataset", default="jhan21/amazon-beauty-reviews-dataset")
    parser.add_argument("--config", default="default")
    parser.add_argument("--split", default="train")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--length", type=int, default=25)
    args = parser.parse_args()

    summary = fetch_and_write_huggingface_preview(
        output_dir=args.output_dir,
        metadata_dataset=args.metadata_dataset,
        reviews_dataset=args.reviews_dataset,
        config=args.config,
        split=args.split,
        offset=args.offset,
        length=args.length,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
