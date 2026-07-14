from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from collections.abc import Callable, Iterable
from io import TextIOWrapper
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen as default_urlopen

from src.glowfit.datasets import parse_amazon_metadata_record
from src.glowfit.huggingface_preview import _review_row_to_review
from src.glowfit.schemas import Product, Review

HUGGING_FACE_DATASET_BASE_URL = "https://huggingface.co/datasets"
FACE_SKINCARE_TERMS = (
    "skincare",
    "serum",
    "moisturizer",
    "sunscreen",
    "cleanser",
    "toner",
    "face cream",
    "facial",
    "retinol",
    "hyaluronic",
    "eye cream",
    "face mask",
    "face oil",
)
NON_FACE_SKINCARE_TERMS = (
    "hair",
    "conditioner",
    "shampoo",
    "dermaplaning",
    "razor",
    "nail",
    "tattoo",
    "hand",
    "body",
    "lip",
    "lipstick",
    "makeup",
    "cosmetic cooler",
    "bath bomb",
    "antiperspirant",
    "antiseptic",
    "foot",
    "eyelid",
    "soap",
    "beauty bar",
    "tool",
    "tools",
    "applicator",
    "mixing bowl",
    "scraper",
    "massage",
    "massager",
    "roller",
    "gua sha",
    "ice globes",
    "pedimask",
    "top coat",
    "gel polish",
    "soak off",
    "uv/led",
)
ATTRIBUTE_RULES = (
    ("fragrance free", ("fragrance-free", "fragrance free", "unscented", "without fragrance")),
    ("sensitive skin", ("sensitive skin", "gentle", "non-irritating", "hypoallergenic")),
    ("dry skin", ("dry skin", "hydrating", "hydration", "moisturizing")),
    ("oily skin", ("oily skin", "oil control", "non-greasy")),
    ("calming", ("calming", "soothing", "redness", "cica", "centella")),
    ("barrier care", ("skin barrier", "barrier repair", "ceramide")),
    ("light texture", ("lightweight", "light texture")),
    ("watery texture", ("watery", "water-based")),
    ("gel texture", ("gel", "jelly")),
    ("cream texture", ("cream",)),
    ("matte finish", ("matte",)),
    ("no white cast", ("no white cast", "clear sunscreen")),
    ("retinol", ("retinol",)),
    ("vitamin c", ("vitamin c",)),
)


class HuggingFaceHubUnavailable(RuntimeError):
    """Raised when a public Hugging Face Hub file cannot be streamed."""


def _dataset_file_url(dataset: str, filename: str) -> str:
    return (
        f"{HUGGING_FACE_DATASET_BASE_URL}/{quote(dataset, safe='/')}/resolve/main/"
        f"{quote(filename, safe='/')}?download=true"
    )


def download_huggingface_dataset_file(
    dataset: str,
    filename: str,
    destination: Path,
    urlopen: Callable[..., Any] = default_urlopen,
) -> Path:
    """Download a Hub dataset file atomically without depending on Dataset Viewer."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    url = _dataset_file_url(dataset, filename)
    try:
        with urlopen(url, timeout=60) as response, NamedTemporaryFile(
            mode="wb", dir=destination.parent, delete=False
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            while chunk := response.read(1024 * 1024):
                temporary_file.write(chunk)
    except (HTTPError, TimeoutError, URLError) as error:
        raise HuggingFaceHubUnavailable(
            f"Hugging Face Hub file is unavailable for {dataset}/{filename}."
        ) from error
    except Exception:
        if "temporary_path" in locals():
            temporary_path.unlink(missing_ok=True)
        raise

    temporary_path.replace(destination)
    return destination


def load_parquet_rows(path: Path) -> list[dict[str, Any]]:
    """Read local Parquet metadata after the optional ingestion dependency is installed."""

    try:
        import pyarrow.parquet as parquet
    except ImportError as error:
        raise RuntimeError(
            "Hub ingestion requires the optional 'ingestion' dependency. "
            "Run with: uv run --extra ingestion python scripts/fetch_huggingface_hub_catalog.py"
        ) from error

    return parquet.read_table(path).to_pylist()


def _is_skincare_product(record: dict[str, Any]) -> bool:
    title = str(record.get("title") or record.get("name") or "").lower()
    supporting_text = " ".join(
        str(record.get(field) or "")
        for field in ("item_form", "skin_type", "categories")
    ).lower()
    is_face_skincare = any(
        _contains_term(title, term) or _contains_term(supporting_text, term)
        for term in FACE_SKINCARE_TERMS
    )
    return is_face_skincare and not any(
        _contains_term(title, term) for term in NON_FACE_SKINCARE_TERMS
    )


def _contains_term(text: str, term: str) -> bool:
    return re.search(rf"\b{re.escape(term)}\b", text) is not None


def _category_from_product_text(text: str) -> str:
    for category, terms in (
        ("sunscreen", ("sunscreen", "spf")),
        ("cleanser", ("cleanser", "cleansing", "makeup remover")),
        ("toner", ("toner",)),
        ("serum", ("serum", "ampoule")),
        ("mask", ("face mask", "facial mask")),
        ("eye care", ("eye cream", "eye serum")),
        ("moisturizer", ("moisturizer", "moisturising", "face cream", "facial cream")),
        ("face oil", ("face oil", "facial oil")),
    ):
        if any(_contains_term(text, term) for term in terms):
            return category
    return "skincare"


def _canonical_attributes(record: dict[str, Any]) -> list[str]:
    searchable_text = " ".join(
        str(record.get(field) or "") for field in ("title", "features", "description", "skin_type")
    ).lower()
    return [
        attribute
        for attribute, terms in ATTRIBUTE_RULES
        if any(_contains_term(searchable_text, term) for term in terms)
    ]


def _normalize_hub_product(record: dict[str, Any]) -> Product:
    product = parse_amazon_metadata_record(record)
    return product.model_copy(
        update={
            "category": _category_from_product_text(product.name.lower()),
            "attributes": _canonical_attributes(record),
        }
    )


def select_hub_products(
    metadata_rows: Iterable[dict[str, Any]], max_products: int | None
) -> list[Product]:
    candidates: list[Product] = []
    seen_ids: set[str] = set()
    for row in metadata_rows:
        if not _is_skincare_product(row):
            continue
        product = _normalize_hub_product(row)
        if not product.product_id or product.product_id in seen_ids:
            continue
        seen_ids.add(product.product_id)
        candidates.append(product)

    ranked_products = sorted(
        candidates,
        key=lambda product: (product.review_count, product.average_rating),
        reverse=True,
    )
    return ranked_products[:max_products] if max_products is not None else ranked_products


def collect_matching_reviews(
    review_rows: Iterable[dict[str, Any]],
    product_ids: set[str],
    min_reviews_per_product: int,
    max_reviews_per_product: int,
) -> list[Review]:
    reviews: list[Review] = []
    counts: defaultdict[str, int] = defaultdict(int)
    for index, row in enumerate(review_rows, start=1):
        product_id = str(row.get("parent_asin") or row.get("asin") or "").strip()
        if product_id not in product_ids or counts[product_id] >= max_reviews_per_product:
            continue
        review = _review_row_to_parent_product_review(row, product_id, index)
        if not review.text.strip() or review.rating < 1 or review.rating > 5:
            continue
        reviews.append(review)
        counts[product_id] += 1
        if all(counts[expected_id] >= min_reviews_per_product for expected_id in product_ids):
            break
    return reviews


def _review_row_to_parent_product_review(
    row: dict[str, Any], product_id: str, index: int
) -> Review:
    """Normalize a review variant ASIN to the metadata catalog's parent ASIN."""

    return _review_row_to_review({**row, "asin": product_id}, index)


def _collect_catalog_reviews(
    review_rows: Iterable[dict[str, Any]],
    products_by_id: dict[str, Product],
    max_products: int,
    min_reviews_per_product: int,
    max_reviews_per_product: int,
) -> tuple[set[str], list[Review], int]:
    reviews_by_product: defaultdict[str, list[Review]] = defaultdict(list)
    eligible_ids: set[str] = set()
    rows_scanned = 0

    for index, row in enumerate(review_rows, start=1):
        rows_scanned = index
        product_id = str(row.get("parent_asin") or row.get("asin") or "").strip()
        if product_id not in products_by_id:
            continue
        product_reviews = reviews_by_product[product_id]
        if len(product_reviews) >= max_reviews_per_product:
            continue
        review = _review_row_to_parent_product_review(row, product_id, index)
        if not review.text.strip() or review.rating < 1 or review.rating > 5:
            continue
        product_reviews.append(review)
        if len(product_reviews) == min_reviews_per_product:
            eligible_ids.add(product_id)
        if len(eligible_ids) >= max_products:
            break

    selected_ids = set(
        sorted(
            eligible_ids,
            key=lambda product_id: (
                products_by_id[product_id].review_count,
                products_by_id[product_id].average_rating,
            ),
            reverse=True,
        )[:max_products]
    )
    selected_reviews = [
        review for product_id in selected_ids for review in reviews_by_product[product_id]
    ]
    return selected_ids, selected_reviews, rows_scanned


def stream_huggingface_csv_rows(
    dataset: str,
    filename: str,
    max_rows: int,
    urlopen: Callable[..., Any] = default_urlopen,
) -> Iterable[dict[str, str]]:
    """Yield a bounded number of CSV rows and close the remote stream early."""

    url = _dataset_file_url(dataset, filename)
    try:
        response = urlopen(url, timeout=60)
    except (HTTPError, TimeoutError, URLError) as error:
        raise HuggingFaceHubUnavailable(
            f"Hugging Face Hub file is unavailable for {dataset}/{filename}."
        ) from error

    with response, TextIOWrapper(response, encoding="utf-8", newline="") as text_stream:
        for index, row in enumerate(csv.DictReader(text_stream), start=1):
            yield row
            if index >= max_rows:
                break


def write_hub_catalog(
    metadata_rows: Iterable[dict[str, Any]],
    review_rows: Iterable[dict[str, Any]],
    output_dir: Path,
    max_products: int,
    min_reviews_per_product: int,
    max_reviews_per_product: int,
) -> dict[str, str | int]:
    candidates = select_hub_products(metadata_rows, max_products=None)
    products_by_id = {product.product_id: product for product in candidates}
    ready_ids, reviews, review_rows_scanned = _collect_catalog_reviews(
        review_rows,
        products_by_id=products_by_id,
        max_products=max_products,
        min_reviews_per_product=min_reviews_per_product,
        max_reviews_per_product=max_reviews_per_product,
    )
    ready_products = sorted(
        (products_by_id[product_id] for product_id in ready_ids),
        key=lambda product: (product.review_count, product.average_rating, product.product_id),
        reverse=True,
    )
    reviews.sort(key=lambda review: (review.product_id, review.timestamp, review.review_id))

    output_dir.mkdir(parents=True, exist_ok=True)
    products_path = output_dir / "products.json"
    reviews_path = output_dir / "reviews.json"
    summary_path = output_dir / "summary.json"
    products_path.write_text(
        json.dumps([product.model_dump() for product in ready_products], indent=2), encoding="utf-8"
    )
    reviews_path.write_text(
        json.dumps([review.model_dump() for review in reviews], indent=2), encoding="utf-8"
    )
    result = {
        "products_written": len(ready_products),
        "reviews_written": len(reviews),
        "metadata_candidates": len(candidates),
        "review_rows_scanned": review_rows_scanned,
        "products_path": str(products_path),
        "reviews_path": str(reviews_path),
        "summary_path": str(summary_path),
    }
    summary_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def fetch_and_write_huggingface_hub_catalog(
    output_dir: Path,
    cache_dir: Path,
    max_products: int = 25,
    min_reviews_per_product: int = 3,
    max_reviews_per_product: int = 20,
    max_review_rows: int = 100_000,
    metadata_dataset: str = "smartcat/Amazon_All_Beauty_2023",
    metadata_filename: str = "data/train-00000-of-00001.parquet",
    reviews_dataset: str = "jhan21/amazon-beauty-reviews-dataset",
    reviews_filename: str = "amazon_beauty_reviews_dataset.csv",
) -> dict[str, str | int]:
    metadata_path = cache_dir / metadata_dataset.replace("/", "__") / Path(metadata_filename).name
    if not metadata_path.exists():
        download_huggingface_dataset_file(metadata_dataset, metadata_filename, metadata_path)

    result = write_hub_catalog(
        metadata_rows=load_parquet_rows(metadata_path),
        review_rows=stream_huggingface_csv_rows(
            reviews_dataset, reviews_filename, max_rows=max_review_rows
        ),
        output_dir=output_dir,
        max_products=max_products,
        min_reviews_per_product=min_reviews_per_product,
        max_reviews_per_product=max_reviews_per_product,
    )
    return {
        **result,
        "metadata_cache_path": str(metadata_path),
        "review_rows_scanned_limit": max_review_rows,
    }
