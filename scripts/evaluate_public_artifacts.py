from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.glowfit.public_evaluation import write_public_artifact_evaluation_report  # noqa: E402


def _parse_k_values(raw_value: str) -> list[int]:
    return [int(value.strip()) for value in raw_value.split(",") if value.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate GlowFit rankings from processed public-data artifacts."
    )
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("artifacts/public_evaluation.json"))
    parser.add_argument("--relevant-rating-threshold", type=int, default=4)
    parser.add_argument("--k-values", default="1,3,5")
    args = parser.parse_args()

    report = write_public_artifact_evaluation_report(
        artifact_dir=args.artifact_dir,
        output_path=args.output,
        relevant_rating_threshold=args.relevant_rating_threshold,
        k_values=_parse_k_values(args.k_values),
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
