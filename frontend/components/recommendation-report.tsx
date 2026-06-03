import { EvidencePanel } from "./evidence-panel";
import { ProductCard } from "./product-card";
import type { ReportResponse } from "../lib/types";

export function RecommendationReport({ report }: { report: ReportResponse | null }) {
  if (!report) {
    return (
      <section className="empty-state">
        <p>피부 타입, 고민, 제형, 예산을 선택하면 맞춤 추천 결과가 이곳에 표시됩니다.</p>
      </section>
    );
  }

  const top = report.recommendations[0];

  return (
    <section className="report-grid">
      <main className="report-main">
        <p className="eyebrow">추천 결과</p>
        <h1>상위 추천 3개</h1>
        <p className="summary">{report.summary}</p>

        <div className="recommendation-list">
          {report.recommendations.map((recommendation, index) => (
            <ProductCard
              key={recommendation.product.product_id}
              recommendation={recommendation}
              rank={index + 1}
            />
          ))}
        </div>

        <section className="model-panel">
          <h2>랭킹 신호</h2>
          {Object.entries(top.model_scores).map(([model, score]) => (
            <div key={model} className="metric-row">
              <span>{model}</span>
              <meter max={1} min={0} value={score} />
              <strong>{score.toFixed(2)}</strong>
            </div>
          ))}
        </section>
      </main>

      <EvidencePanel recommendation={top} />
    </section>
  );
}
