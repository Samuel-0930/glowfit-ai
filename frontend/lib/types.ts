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
};
