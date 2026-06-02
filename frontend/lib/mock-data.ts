import type { ReportResponse, UserPreferences } from "./types";

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
