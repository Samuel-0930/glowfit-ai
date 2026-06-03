import type { CSSProperties } from "react";
import type { Recommendation } from "../lib/types";

export function ProductCard({ recommendation, rank }: { recommendation: Recommendation; rank: number }) {
  const { product } = recommendation;

  return (
    <article className="product-card">
      <div className="product-image" aria-hidden="true">
        {rank}
      </div>
      <div>
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
      <div className="tag-row">
        {product.attributes.map((attribute) => (
          <span key={attribute} className="tag">
            {attribute}
          </span>
        ))}
      </div>
    </article>
  );
}
