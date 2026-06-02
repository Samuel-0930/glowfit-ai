import { EvidencePanel } from "./evidence-panel";
import { ProductCard } from "./product-card";
import type { ReportResponse } from "../lib/types";

export function RecommendationReport({ report }: { report: ReportResponse }) {
  const top = report.recommendations[0];

  return (
    <section className="report-grid">
      <main className="report-main">
        <p className="eyebrow">Recommendation report</p>
        <h1>GlowFit AI</h1>
        <p className="summary">{report.summary}</p>

        <div className="recommendation-list">
          {report.recommendations.map((recommendation) => (
            <ProductCard key={recommendation.product.product_id} recommendation={recommendation} />
          ))}
        </div>

        <section className="model-panel">
          <h2>Model signals</h2>
          {Object.entries(top.model_scores).map(([model, score]) => (
            <div key={model} className="metric-row">
              <span>{model}</span>
              <strong>{score.toFixed(2)}</strong>
            </div>
          ))}
        </section>
      </main>

      <EvidencePanel recommendation={top} />
    </section>
  );
}
