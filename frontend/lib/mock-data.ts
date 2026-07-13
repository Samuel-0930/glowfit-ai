import type {
  EvidenceSnippet,
  Product,
  PublicEvaluationReport,
  Recommendation,
  ReportResponse,
  UserPreferences
} from "./types";

export const defaultPreferences: UserPreferences = {
  skin_type: "",
  concerns: [],
  texture: "",
  fragrance_sensitivity: "",
  budget_max_usd: 30,
  avoid: []
};

type ProductRecord = Product & {
  match_tags: string[];
  avoid_tags: string[];
  reviews: EvidenceSnippet[];
};

export const concernOptions = [
  "barrier care",
  "redness",
  "acne",
  "pores",
  "oil control",
  "calming",
  "stinging"
];

export const textureOptions = ["light", "watery", "gel", "cream", "lotion"];
export const avoidOptions = ["strong scent", "sticky finish", "heavy cream", "comedogenic oils", "essential oils"];

export const productCatalog: ProductRecord[] = [
  {
    product_id: "p_glow_gel",
    name: "Glow Barrier Gel Cream",
    category: "moisturizer",
    brand: "Aster Lab",
    price_usd: 24,
    average_rating: 4.6,
    review_count: 1180,
    attributes: ["light texture", "fragrance free", "dry skin", "barrier care"],
    match_tags: ["dry", "barrier care", "redness", "light", "fragrance free", "calming"],
    avoid_tags: [],
    reviews: [
      {
        review_id: "r_001",
        product_id: "p_glow_gel",
        text: "Light gel texture but still moisturizing. My dry skin felt calm and the fragrance free formula did not sting.",
        sentiment: "positive",
        aspects: ["texture", "fragrance", "dry skin", "calming"],
        relevance: 2.2
      }
    ]
  },
  {
    product_id: "p_pore_reset",
    name: "Pore Reset Water Serum",
    category: "serum",
    brand: "Clear Theory",
    price_usd: 21,
    average_rating: 4.5,
    review_count: 920,
    attributes: ["watery texture", "oil control", "non comedogenic", "pores"],
    match_tags: ["oily", "acne", "pores", "oil control", "watery", "non comedogenic"],
    avoid_tags: [],
    reviews: [
      {
        review_id: "r_101",
        product_id: "p_pore_reset",
        text: "It sinks in fast and did not leave my T-zone shiny. My pores looked smoother after a few weeks.",
        sentiment: "positive",
        aspects: ["oil control", "pores", "watery", "fast absorbing"],
        relevance: 2.4
      }
    ]
  },
  {
    product_id: "p_calm_cushion",
    name: "Calm Cushion Repair Cream",
    category: "moisturizer",
    brand: "Mellow Derm",
    price_usd: 28,
    average_rating: 4.7,
    review_count: 1340,
    attributes: ["fragrance free", "calming", "barrier repair", "cream texture"],
    match_tags: ["sensitive", "dry", "redness", "stinging", "calming", "cream", "barrier care", "fragrance free"],
    avoid_tags: ["heavy cream"],
    reviews: [
      {
        review_id: "r_201",
        product_id: "p_calm_cushion",
        text: "My cheeks usually sting with creams, but this felt soft and helped the redness calm down overnight.",
        sentiment: "positive",
        aspects: ["stinging", "redness", "calming", "cream"],
        relevance: 2.5
      }
    ]
  },
  {
    product_id: "p_cica_gel",
    name: "Cica Clear Gel Cream",
    category: "moisturizer",
    brand: "Herb Index",
    price_usd: 18,
    average_rating: 4.3,
    review_count: 740,
    attributes: ["gel cream", "calming", "light finish", "budget friendly"],
    match_tags: ["oily", "sensitive", "acne", "calming", "gel", "light", "redness"],
    avoid_tags: [],
    reviews: [
      {
        review_id: "r_103",
        product_id: "p_cica_gel",
        text: "Good lightweight gel for breakouts. It calmed redness without feeling greasy.",
        sentiment: "positive",
        aspects: ["breakouts", "calming", "light finish"],
        relevance: 1.9
      }
    ]
  },
  {
    product_id: "p_dew_lotion",
    name: "Dew Lock Barrier Lotion",
    category: "moisturizer",
    brand: "North Bloom",
    price_usd: 20,
    average_rating: 4.4,
    review_count: 860,
    attributes: ["barrier care", "lotion texture", "dry skin", "low scent"],
    match_tags: ["dry", "barrier care", "lotion", "redness", "low scent"],
    avoid_tags: ["sticky finish"],
    reviews: [
      {
        review_id: "r_002",
        product_id: "p_dew_lotion",
        text: "Comfortable for dry cheeks and almost no scent, but it felt a little richer than a gel.",
        sentiment: "mixed",
        aspects: ["dry skin", "low scent", "rich texture"],
        relevance: 1.8
      }
    ]
  },
  {
    product_id: "p_milk_toner",
    name: "Oat Milk Recovery Toner",
    category: "toner",
    brand: "Kind Routine",
    price_usd: 19,
    average_rating: 4.4,
    review_count: 680,
    attributes: ["milky toner", "soothing", "fragrance free", "layering"],
    match_tags: ["sensitive", "calming", "redness", "watery", "fragrance free", "stinging"],
    avoid_tags: [],
    reviews: [
      {
        review_id: "r_203",
        product_id: "p_milk_toner",
        text: "A gentle first layer when my skin feels hot, but I need cream on top at night.",
        sentiment: "mixed",
        aspects: ["gentle", "heat", "layering", "needs cream"],
        relevance: 1.8
      }
    ]
  }
];

function isProfileReady(preferences: UserPreferences) {
  return Boolean(
    preferences.skin_type &&
      preferences.texture &&
      preferences.fragrance_sensitivity &&
      preferences.concerns.length > 0
  );
}

function scoreProduct(product: ProductRecord, preferences: UserPreferences) {
  let score = 0.18;
  const reasons: string[] = [];
  const cautions: string[] = [];

  if (product.match_tags.includes(preferences.skin_type)) {
    score += 0.18;
    reasons.push(`${preferences.skin_type} skin match`);
  }

  preferences.concerns.forEach((concern) => {
    if (product.match_tags.includes(concern)) {
      score += 0.12;
      reasons.push(concern);
    }
  });

  if (product.match_tags.includes(preferences.texture)) {
    score += 0.14;
    reasons.push(`${preferences.texture} texture`);
  }

  if (preferences.fragrance_sensitivity === "high" && product.match_tags.includes("fragrance free")) {
    score += 0.14;
    reasons.push("fragrance free");
  } else if (preferences.fragrance_sensitivity === "low") {
    score += 0.04;
  }

  if (product.price_usd <= preferences.budget_max_usd) {
    score += 0.08;
    reasons.push("within budget");
  } else {
    score -= 0.16;
    cautions.push(`budget보다 $${product.price_usd - preferences.budget_max_usd} 높음`);
  }

  preferences.avoid.forEach((avoid) => {
    if (product.avoid_tags.includes(avoid)) {
      score -= 0.14;
      cautions.push(`${avoid} 관련 주의`);
    }
  });

  score += Math.min(product.average_rating / 5, 1) * 0.08;
  score += Math.min(product.review_count / 1500, 1) * 0.06;

  return {
    cautions,
    reasons: Array.from(new Set(reasons)).slice(0, 4),
    score: Math.max(0.2, Math.min(score, 0.98))
  };
}

export function inferRecommendations(preferences: UserPreferences): ReportResponse | null {
  if (!isProfileReady(preferences)) {
    return null;
  }

  const recommendations: Recommendation[] = productCatalog
    .map((product) => {
      const result = scoreProduct(product, preferences);
      const evidence = product.reviews.map((review) => ({
        ...review,
        relevance: review.relevance + result.score
      }));

      return {
        product,
        fit_score: result.score,
        confidence: Math.min(0.94, 0.58 + result.score * 0.36),
        reasons: result.reasons.length ? result.reasons : ["balanced rating", "review evidence"],
        cautions: result.cautions,
        evidence,
        model_scores: {
          profile: Math.min(1, result.score + 0.03),
          review: Math.min(1, evidence[0].relevance / 3.3),
          budget: product.price_usd <= preferences.budget_max_usd ? 1 : 0.45,
          hybrid: result.score
        }
      };
    })
    .sort((a, b) => b.fit_score - a.fit_score)
    .slice(0, 3);

  const top = recommendations[0];
  return {
    summary: `${top.product.name}이 현재 프로필에서 가장 높은 적합도를 보입니다. ${top.reasons
      .slice(0, 3)
      .join(", ")} 조건이 리뷰 근거와 가장 잘 맞았습니다.`,
    generation_mode: "client-inference",
    recommendations
  };
}

export const mockReport = inferRecommendations({
  skin_type: "dry",
  concerns: ["redness", "barrier care"],
  texture: "light",
  fragrance_sensitivity: "high",
  budget_max_usd: 25,
  avoid: ["strong scent", "sticky finish"]
}) as ReportResponse;

export const mockPublicEvaluation: PublicEvaluationReport = {
  artifact_dir: "data/processed/hf_joined_preview",
  product_count: 25,
  review_count: 25,
  relevance_rule: "review_rating >= 4",
  relevant_product_ids: ["B001", "B002", "B003"],
  coverage: {
    relevant_product_count: 3,
    relevant_product_rate: 0.12
  },
  comparative_ready: true,
  warnings: [],
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
