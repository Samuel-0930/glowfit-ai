"""Generate an idempotent Supabase seed SQL file from a GlowFit catalog artifact."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.glowfit.supabase_seed import build_supabase_seed_from_artifact  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace all existing catalog rows in the same transaction.",
    )
    args = parser.parse_args()

    sql = build_supabase_seed_from_artifact(args.artifact_dir, replace=args.replace)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(sql, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
