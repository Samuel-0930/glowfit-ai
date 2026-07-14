const labels: Record<string, string> = {
  dry: "건성",
  oily: "지성",
  combination: "복합성",
  sensitive: "민감성",
  light: "가벼운 제형",
  watery: "워터리",
  gel: "젤",
  cream: "크림",
  lotion: "로션",
  low: "낮음",
  medium: "보통",
  high: "높음",
  "barrier care": "장벽 케어",
  redness: "붉은기",
  acne: "트러블",
  pores: "모공",
  "oil control": "유분 조절",
  calming: "진정",
  stinging: "따가움",
  "strong scent": "강한 향",
  "sticky finish": "끈적이는 마무리",
  "heavy cream": "무거운 크림",
  "comedogenic oils": "모공 막힘 우려 오일",
  "essential oils": "에센셜 오일",
  "fragrance free": "무향",
  "sensitive skin": "민감성 피부",
  "dry skin": "건조한 피부",
  "oily skin": "지성 피부",
  "light texture": "가벼운 사용감",
  "watery texture": "워터리 제형",
  "gel texture": "젤 제형",
  "cream texture": "크림 제형",
  texture: "사용감",
  fragrance: "향",
  "matte finish": "보송한 마무리",
  "no white cast": "백탁 적음",
  sunscreen: "선크림",
  cleanser: "클렌저",
  toner: "토너",
  serum: "세럼",
  mask: "마스크",
  moisturizer: "보습제",
  "face oil": "페이스 오일",
  skincare: "스킨케어"
};

export function presentLabel(value: string) {
  return labels[value.toLowerCase()] ?? value;
}

export function presentBrand(brand: string) {
  return brand.trim().toLowerCase() === "unknown" ? null : brand;
}

export function presentPrice(priceUsd: number) {
  if (!Number.isFinite(priceUsd) || priceUsd <= 0) return "가격 정보 없음";

  return `$${new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(priceUsd)}`;
}

export function presentReviewExcerpt(text: string, maxLength = 260) {
  const normalized = text.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
  if (normalized.length <= maxLength) return normalized;

  return `${normalized.slice(0, maxLength).trimEnd()}…`;
}
