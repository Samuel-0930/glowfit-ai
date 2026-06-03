from __future__ import annotations

import math
from collections.abc import Iterable


def _top_k(ranked_product_ids: list[str], k: int) -> list[str]:
    if k <= 0:
        raise ValueError("k must be greater than zero")
    return ranked_product_ids[:k]


def precision_at_k(ranked_product_ids: list[str], relevant_product_ids: set[str], k: int) -> float:
    top = _top_k(ranked_product_ids, k)
    if not top:
        return 0.0
    hits = sum(product_id in relevant_product_ids for product_id in top)
    return round(hits / len(top), 4)


def recall_at_k(ranked_product_ids: list[str], relevant_product_ids: set[str], k: int) -> float:
    if not relevant_product_ids:
        return 0.0
    top = _top_k(ranked_product_ids, k)
    hits = sum(product_id in relevant_product_ids for product_id in top)
    return round(hits / len(relevant_product_ids), 4)


def ndcg_at_k(ranked_product_ids: list[str], relevant_product_ids: set[str], k: int) -> float:
    top = _top_k(ranked_product_ids, k)
    dcg = sum(
        1.0 / math.log2(rank + 2)
        for rank, product_id in enumerate(top)
        if product_id in relevant_product_ids
    )
    ideal_hits = min(len(relevant_product_ids), k)
    ideal_dcg = sum(1.0 / math.log2(rank + 2) for rank in range(ideal_hits))
    return round(dcg / ideal_dcg, 4) if ideal_dcg else 0.0


def evaluate_ranked_product_ids(
    ranked_product_ids: list[str],
    relevant_product_ids: Iterable[str],
    k_values: list[int],
) -> dict[str, float]:
    relevant = set(relevant_product_ids)
    metrics: dict[str, float] = {}
    for k in k_values:
        metrics[f"precision@{k}"] = precision_at_k(ranked_product_ids, relevant, k)
        metrics[f"recall@{k}"] = recall_at_k(ranked_product_ids, relevant, k)
        metrics[f"ndcg@{k}"] = ndcg_at_k(ranked_product_ids, relevant, k)
    return metrics
