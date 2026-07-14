import type { CSSProperties } from "react";
import { presentBrand, presentLabel, presentPrice } from "../lib/presentation";
import type { Recommendation } from "../lib/types";

export function ProductComparison({ recommendations }: { recommendations: Recommendation[] }) {
  if (!recommendations.length) {
    return <section className="empty-state">먼저 추천 탭에서 프로필을 입력해 주세요.</section>;
  }

  const [top, challenger] = recommendations;

  return (
    <section className="comparison-panel">
      <div className="panel-heading">
        <p className="eyebrow">비교</p>
        <h1>왜 이 순서로 추천됐을까</h1>
        <p className="summary">
          프로필 적합도, 리뷰 근거, 예산 조건을 함께 반영해 각 후보의 순위를 비교합니다.
        </p>
      </div>

      <div className="decision-strip">
        <div>
          <span>가장 높은 후보</span>
          <strong>{top.product.name}</strong>
        </div>
        <div>
          <span>주요 근거</span>
          <strong>{top.reasons.slice(0, 2).join(" + ")}</strong>
        </div>
        <div>
          <span>가장 가까운 대안</span>
          <strong>{challenger?.product.name ?? "없음"}</strong>
        </div>
      </div>

      <div className="comparison-grid">
        {recommendations.map((item) => (
          <article key={item.product.product_id} className="comparison-card">
            <div>
              {presentBrand(item.product.brand) && <p className="eyebrow">{presentBrand(item.product.brand)}</p>}
              <h2>{item.product.name}</h2>
              <p className="muted">
                {presentLabel(item.product.category)} · {presentPrice(item.product.price_usd)} · 평점 {item.product.average_rating.toFixed(1)}
              </p>
            </div>
            <div className="score-pair">
              <div className="score-circle large" style={{ "--score": item.fit_score } as CSSProperties}>
                <strong>{Math.round(item.fit_score * 100)}</strong>
                <span>적합도</span>
              </div>
              <div className="score-circle large" style={{ "--score": item.evidence_strength } as CSSProperties}>
                <strong>{Math.round(item.evidence_strength * 100)}</strong>
                <span>근거 강도</span>
              </div>
            </div>
            <div className="mini-section">
              <span>근거</span>
              <div className="tag-row">
                {item.reasons.map((reason) => (
                  <span className="tag" key={reason}>
                    {presentLabel(reason)}
                  </span>
                ))}
              </div>
            </div>
            <div className="mini-section">
              <span>주의</span>
              <p className="muted">{item.cautions[0] ?? "큰 주의 신호 없음"}</p>
            </div>
            <div className="signal-bars">
              {Object.entries(item.model_scores).map(([model, score]) => (
                <div className="metric-row" key={model}>
                  <span>{model}</span>
                  <meter max={1} min={0} value={score} />
                  <strong>{score.toFixed(2)}</strong>
                </div>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
