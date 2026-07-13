"""Validate the configured Supabase catalog without printing credentials."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def load_env_file(path: Path) -> None:
    for line in path.read_text().splitlines():
        key, separator, value = line.strip().partition("=")
        if separator and key and not key.startswith("#"):
            os.environ.setdefault(key, value)


def main() -> None:
    from src.glowfit.catalog import get_catalog_repository

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    args = parser.parse_args()

    if args.env_file.exists():
        load_env_file(args.env_file)
    os.environ["GLOWFIT_CATALOG_SOURCE"] = "supabase"

    catalog = get_catalog_repository().load()
    if catalog.source != "supabase" or not catalog.products or not catalog.reviews:
        raise SystemExit("Supabase catalog validation failed: expected products and reviews.")

    print(
        "Supabase catalog ready: "
        f"{len(catalog.products)} products, {len(catalog.reviews)} reviews."
    )


if __name__ == "__main__":
    main()
