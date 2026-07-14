import type { CSSProperties } from "react";
import { presentBrand, presentLabel, presentPrice } from "../lib/presentation";
import type { Recommendation } from "../lib/types";

export function ProductCard({
  recommendation,
  rank,
  isTop = false
}: {
  recommendation: Recommendation;
  rank: number;
  isTop?: boolean;
}) {
  const { product } = recommendation;
  const brand = presentBrand(product.brand);

  return (
    <article className={`product-card${isTop ? " product-card-top" : ""}`}>
      <div className="product-image" aria-hidden="true">
        {rank}
      </div>
      <div className="product-card-main">
        {brand && <p className="eyebrow">{brand}</p>}
        <h3>{product.name}</h3>
        <p className="muted">
          {presentLabel(product.category)} · {presentPrice(product.price_usd)} · 평점 {product.average_rating.toFixed(1)} · 리뷰{" "}
          {product.review_count.toLocaleString()}개
        </p>
      </div>
      <div className="score-circle" style={{ "--score": recommendation.fit_score } as CSSProperties}>
        <strong>{Math.round(recommendation.fit_score * 100)}</strong>
        <span>적합도</span>
      </div>
      <div className="product-reasons" aria-label={`${product.name} 추천 근거`}>
        {recommendation.reasons.slice(0, 3).map((reason) => (
          <span key={reason} className="tag">
            {presentLabel(reason)}
          </span>
        ))}
      </div>
      {recommendation.cautions[0] && <p className="product-caution">확인: {recommendation.cautions[0]}</p>}
    </article>
  );
}
