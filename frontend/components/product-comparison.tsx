import type { Recommendation } from "../lib/types";

export function ProductComparison({ recommendations }: { recommendations: Recommendation[] }) {
  return (
    <section className="comparison-panel" id="compare">
      <h2>Product comparison</h2>
      <div className="comparison-table">
        {recommendations.map((item) => (
          <div key={item.product.product_id} className="comparison-row">
            <span>{item.product.name}</span>
            <span>{Math.round(item.fit_score * 100)}% fit</span>
            <span>{item.product.attributes.slice(0, 2).join(", ")}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
