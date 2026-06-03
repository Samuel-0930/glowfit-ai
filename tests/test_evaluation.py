from src.glowfit.evaluation import (
    evaluate_ranked_product_ids,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)


def test_precision_recall_and_ndcg_reward_relevant_top_results():
    ranked = ["p_glow_gel", "p_velvet_sunscreen", "p_calm_ampoule"]
    relevant = {"p_glow_gel", "p_calm_ampoule"}

    assert precision_at_k(ranked, relevant, k=2) == 0.5
    assert recall_at_k(ranked, relevant, k=2) == 0.5
    assert round(ndcg_at_k(ranked, relevant, k=3), 4) == 0.9197


def test_evaluate_ranked_product_ids_returns_named_metrics():
    metrics = evaluate_ranked_product_ids(
        ranked_product_ids=["p_glow_gel", "p_velvet_sunscreen", "p_calm_ampoule"],
        relevant_product_ids={"p_glow_gel", "p_calm_ampoule"},
        k_values=[1, 3],
    )

    assert metrics == {
        "precision@1": 1.0,
        "recall@1": 0.5,
        "ndcg@1": 1.0,
        "precision@3": 0.6667,
        "recall@3": 1.0,
        "ndcg@3": 0.9197,
    }
