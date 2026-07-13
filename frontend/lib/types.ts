export type Product = {
  product_id: string;
  name: string;
  category: string;
  brand: string;
  price_usd: number;
  average_rating: number;
  review_count: number;
  attributes: string[];
};

export type EvidenceSnippet = {
  review_id: string;
  product_id: string;
  text: string;
  sentiment: "positive" | "mixed" | "negative";
  aspects: string[];
  relevance: number;
};

export type Recommendation = {
  product: Product;
  fit_score: number;
  confidence: number;
  reasons: string[];
  cautions: string[];
  evidence: EvidenceSnippet[];
  model_scores: Record<string, number>;
};

export type UserPreferences = {
  skin_type: string;
  concerns: string[];
  texture: string;
  fragrance_sensitivity: string;
  budget_max_usd: number;
  avoid: string[];
};

export type ReportResponse = {
  summary: string;
  recommendations: Recommendation[];
  generation_mode: string;
  metadata?: {
    data_source: string;
    product_count: number;
    review_count: number;
    requested_limit: number;
    returned_count: number;
    top_product_id: string | null;
  };
};

export type PublicEvaluationModel = {
  ranked_product_ids: string[];
  metrics: Record<string, number>;
};

export type PublicEvaluationReport = {
  artifact_dir: string;
  product_count: number;
  review_count: number;
  relevance_rule: string;
  relevant_product_ids: string[];
  coverage: {
    relevant_product_count: number;
    relevant_product_rate: number;
  };
  comparative_ready: boolean;
  warnings: string[];
  k_values: number[];
  models: Record<string, PublicEvaluationModel>;
};
