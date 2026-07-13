import type { PublicEvaluationReport } from "./types";

// Generated from `python3 scripts/evaluate_public_artifacts.py --artifact-dir artifacts/sample`.
export const samplePublicEvaluation: PublicEvaluationReport = {
  artifact_dir: "artifacts/sample",
  product_count: 3,
  review_count: 5,
  relevance_rule: "review_rating >= 4",
  relevant_product_ids: ["p_calm_ampoule", "p_glow_gel", "p_velvet_sunscreen"],
  k_values: [1, 3, 5],
  models: {
    popularity: {
      ranked_product_ids: ["p_glow_gel", "p_calm_ampoule", "p_velvet_sunscreen"],
      metrics: { "precision@1": 1, "recall@3": 1, "ndcg@3": 1 }
    },
    rating: {
      ranked_product_ids: ["p_glow_gel", "p_calm_ampoule", "p_velvet_sunscreen"],
      metrics: { "precision@1": 1, "recall@3": 1, "ndcg@3": 1 }
    },
    collaborative: {
      ranked_product_ids: ["p_glow_gel", "p_calm_ampoule", "p_velvet_sunscreen"],
      metrics: { "precision@1": 1, "recall@3": 1, "ndcg@3": 1 }
    },
    content: {
      ranked_product_ids: ["p_glow_gel", "p_calm_ampoule", "p_velvet_sunscreen"],
      metrics: { "precision@1": 1, "recall@3": 1, "ndcg@3": 1 }
    },
    two_tower: {
      ranked_product_ids: ["p_glow_gel", "p_velvet_sunscreen", "p_calm_ampoule"],
      metrics: { "precision@1": 1, "recall@3": 1, "ndcg@3": 1 }
    },
    hybrid: {
      ranked_product_ids: ["p_glow_gel", "p_velvet_sunscreen", "p_calm_ampoule"],
      metrics: { "precision@1": 1, "recall@3": 1, "ndcg@3": 1 }
    }
  }
};
