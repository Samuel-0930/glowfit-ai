import { EvidencePanel } from "./evidence-panel";
import { ProductCard } from "./product-card";
import { presentLabel } from "../lib/presentation";
import type { CatalogHealth, ReportResponse } from "../lib/types";

const modelLabels: Record<string, string> = {
  profile: "프로필 적합도",
  review: "리뷰 근거",
  budget: "예산 적합도",
  hybrid: "종합 점수",
  popularity: "인기도",
  rating: "평점",
  review_average: "리뷰 평균 평점",
  content: "조건 적합도",
  hash_similarity: "해시 텍스트 유사도"
};

export function RecommendationReport({
  report,
  catalogHealth
}: {
  report: ReportResponse | null;
  catalogHealth: CatalogHealth | null;
}) {
  if (!report) {
    return (
      <section className="empty-state">
        <div className="empty-state-content">
          <p className="eyebrow">근거 기반 스킨케어 추천</p>
          <h1>나의 피부 조건을<br />추천 근거로 바꿔보세요.</h1>
          <p>
            피부 타입과 고민을 고르면, 제품 순위뿐 아니라 선택된 리뷰 근거와 확인할 점까지 함께 보여드립니다.
          </p>
          <div className="empty-steps" aria-label="추천 흐름">
            <span>01 프로필 입력</span>
            <span>02 근거 기반 랭킹</span>
            <span>03 리뷰로 결과 확인</span>
          </div>
          {catalogHealth && (
            <p className="catalog-status" role="status">
              운영 데이터 연결됨 · {catalogHealth.product_count}개 제품 · 리뷰 {catalogHealth.review_count.toLocaleString()}개
            </p>
          )}
        </div>
      </section>
    );
  }

  if (!report.recommendations.length) {
    return (
      <section className="empty-state">
        <p>현재 조건에 맞는 추천 상품이 없습니다. 예산이나 피부 고민 조건을 조정해 다시 시도해 주세요.</p>
      </section>
    );
  }

  const top = report.recommendations[0];
  const sourceLabel = report.metadata?.data_source === "supabase" ? "Supabase 카탈로그" : "내장 샘플 데이터";

  return (
    <section className="report-grid">
      <main className="report-main">
        <p className="eyebrow">추천 결과</p>
        <h1>상위 추천 3개</h1>
        <p className="data-source" aria-label={`데이터 출처: ${sourceLabel}`}>
          데이터 출처: {sourceLabel}
        </p>
        <section className="why-panel" aria-labelledby="why-title">
          <div>
            <p className="eyebrow">1위 추천 이유</p>
            <h2 id="why-title">왜 {top.product.name}인가요?</h2>
            <p className="why-summary">선택한 피부 조건과 가장 많이 맞는 제품입니다.</p>
          </div>
          <div className="reason-list" aria-label="추천 핵심 근거">
            {top.reasons.map((reason) => (
              <span className="reason-tag" key={reason}>
                {presentLabel(reason)}
              </span>
            ))}
          </div>
          {top.cautions.length > 0 && (
            <p className="decision-caution">확인할 점: {top.cautions.join(" · ")}</p>
          )}
        </section>

        <div className="recommendation-list">
          {report.recommendations.map((recommendation, index) => (
            <ProductCard
              isTop={index === 0}
              key={recommendation.product.product_id}
              recommendation={recommendation}
              rank={index + 1}
            />
          ))}
        </div>

        <details className="model-panel">
          <summary>랭킹 상세 보기</summary>
          <p className="model-note">
            이 값은 현재 추천에서 각 신호가 반영된 정도이며, 모델 성능이나 정확도를 뜻하지 않습니다.
          </p>
          {Object.entries(top.model_scores).map(([model, score]) => (
            <div key={model} className="metric-row">
              <span>{modelLabels[model] ?? model}</span>
              <meter max={1} min={0} value={score} />
              <strong>{score.toFixed(2)}</strong>
            </div>
          ))}
        </details>
      </main>

      <EvidencePanel recommendation={top} />
    </section>
  );
}
