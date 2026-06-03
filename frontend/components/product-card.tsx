import type { Recommendation } from "../lib/types";

export function ProductCard({ recommendation }: { recommendation: Recommendation }) {
  const { product } = recommendation;
  return (
    <article className="product-card">
      <div className="product-image" aria-hidden="true" />
      <div>
        <p className="eyebrow">{product.brand}</p>
        <h3>{product.name}</h3>
        <p className="muted">
          {product.category} · ${product.price_usd} · {product.average_rating.toFixed(1)} stars
        </p>
      </div>
      <div className="score">{Math.round(recommendation.fit_score * 100)}%</div>
      <div className="tag-row">
        {product.attributes.slice(0, 4).map((attribute) => (
          <span key={attribute} className="tag">
            {attribute}
          </span>
        ))}
      </div>
    </article>
  );
}
