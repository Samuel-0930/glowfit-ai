from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.glowfit.sample_evaluation import build_sample_evaluation_report  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate GlowFit sample recommendation ranking.")
    parser.add_argument("--sample-data-dir", type=Path, default=Path("sample_data"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/sample_evaluation.json"))
    args = parser.parse_args()

    report = build_sample_evaluation_report(args.sample_data_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
