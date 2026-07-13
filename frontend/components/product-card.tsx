import type { CSSProperties } from "react";
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

  return (
    <article className={`product-card${isTop ? " product-card-top" : ""}`}>
      <div className="product-image" aria-hidden="true">
        {rank}
      </div>
      <div className="product-card-main">
        <p className="eyebrow">{product.brand}</p>
        <h3>{product.name}</h3>
        <p className="muted">
          {product.category} · ${product.price_usd} · {product.average_rating.toFixed(1)}점 · 리뷰{" "}
          {product.review_count.toLocaleString()}개
        </p>
      </div>
      <div className="score-circle" style={{ "--score": recommendation.fit_score } as CSSProperties}>
        <strong>{Math.round(recommendation.fit_score * 100)}</strong>
        <span>fit</span>
      </div>
      <div className="product-reasons" aria-label={`${product.name} 추천 근거`}>
        {recommendation.reasons.slice(0, 3).map((reason) => (
          <span key={reason} className="tag">
            {reason}
          </span>
        ))}
      </div>
      {recommendation.cautions[0] && <p className="product-caution">확인: {recommendation.cautions[0]}</p>}
    </article>
  );
}
