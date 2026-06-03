import type { PublicEvaluationReport, ReportResponse, UserPreferences } from "./types";

export const defaultPreferences: UserPreferences = {
  skin_type: "dry",
  concerns: ["redness", "barrier care"],
  texture: "light",
  fragrance_sensitivity: "high",
  budget_max_usd: 25,
  avoid: ["strong scent", "sticky finish"]
};

export const mockReport: ReportResponse = {
  summary:
    "Glow Barrier Gel Cream is the strongest match for a dry, fragrance-sensitive profile because it pairs light texture with barrier care evidence.",
  generation_mode: "mock",
  recommendations: [
    {
      product: {
        product_id: "p_glow_gel",
        name: "Glow Barrier Gel Cream",
        category: "moisturizer",
        brand: "Aster Lab",
        price_usd: 24,
        average_rating: 4.6,
        review_count: 1180,
        attributes: ["light texture", "fragrance free", "dry skin", "barrier care"]
      },
      fit_score: 0.94,
      confidence: 0.85,
      reasons: ["light texture", "fragrance free", "barrier care"],
      cautions: [],
      evidence: [
        {
          review_id: "r_001",
          product_id: "p_glow_gel",
          text:
            "Light gel texture but still moisturizing. My dry skin felt calm and the fragrance free formula did not sting.",
          sentiment: "positive",
          aspects: ["texture", "fragrance", "dry skin", "calming"],
          relevance: 2.2
        }
      ],
      model_scores: {
        popularity: 1,
        rating: 1,
        content: 1,
        two_tower: 0.86
      }
    }
  ]
};

export const mockPublicEvaluation: PublicEvaluationReport = {
  artifact_dir: "data/processed/hf_joined_preview",
  product_count: 25,
  review_count: 25,
  relevance_rule: "review_rating >= 4",
  relevant_product_ids: ["B001", "B002", "B003"],
  k_values: [1, 3, 5],
  models: {
    popularity: {
      ranked_product_ids: ["B001", "B004", "B002"],
      metrics: {
        "precision@1": 1,
        "recall@3": 0.6667,
        "ndcg@3": 0.9197
      }
    },
    content: {
      ranked_product_ids: ["B002", "B001", "B006"],
      metrics: {
        "precision@1": 1,
        "recall@3": 0.6667,
        "ndcg@3": 0.871
      }
    },
    two_tower: {
      ranked_product_ids: ["B003", "B002", "B001"],
      metrics: {
        "precision@1": 1,
        "recall@3": 1,
        "ndcg@3": 1
      }
    },
    hybrid: {
      ranked_product_ids: ["B001", "B003", "B002"],
      metrics: {
        "precision@1": 1,
        "recall@3": 1,
        "ndcg@3": 1
      }
    }
  }
};
