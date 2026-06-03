from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from src.glowfit.data import load_products, load_reviews
from src.glowfit.evidence import EvidenceIndex
from src.glowfit.schemas import Product, Review


@dataclass(frozen=True)
class Artifacts:
    products: list[Product]
    reviews: list[Review]
    evidence_index: EvidenceIndex


def build_sample_artifacts(product_path: Path, review_path: Path, artifact_dir: Path) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    products = load_products(product_path)
    reviews = load_reviews(review_path)
    with (artifact_dir / "products.json").open("w", encoding="utf-8") as file:
        json.dump([product.model_dump() for product in products], file, indent=2)
    with (artifact_dir / "reviews.json").open("w", encoding="utf-8") as file:
        json.dump([review.model_dump() for review in reviews], file, indent=2)


def load_artifacts(artifact_dir: Path) -> Artifacts:
    products = load_products(artifact_dir / "products.json")
    reviews = load_reviews(artifact_dir / "reviews.json")
    return Artifacts(
        products=products,
        reviews=reviews,
        evidence_index=EvidenceIndex.from_reviews(reviews),
    )
