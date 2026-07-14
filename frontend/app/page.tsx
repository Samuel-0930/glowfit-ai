"use client";

import { useEffect, useState } from "react";

import { AppShell } from "../components/app-shell";
import { PreferenceForm } from "../components/preference-form";
import { ProductComparison } from "../components/product-comparison";
import { RecommendationReport } from "../components/recommendation-report";
import { fetchCatalogHealth, fetchReport } from "../lib/api";
import { defaultPreferences } from "../lib/mock-data";
import { presentLabel, presentReviewExcerpt } from "../lib/presentation";
import { samplePublicEvaluation } from "../lib/sample-public-evaluation";
import type { CatalogHealth, ReportResponse, UserPreferences } from "../lib/types";

type TabId = "recommend" | "compare" | "insights" | "experiments" | "portfolio";

const tabs: TabId[] = ["recommend", "compare", "insights", "experiments", "portfolio"];

const evaluationWarningCopy: Record<string, string> = {
  "Catalog has fewer than 10 products; do not compare model quality from this run.":
    "카탈로그가 10개 미만이라 모델 간 우열을 판단하기에는 표본이 작습니다.",
  "Every catalog product satisfies the relevance rule; ranking metrics cannot distinguish models.":
    "모든 제품이 relevance 기준을 충족해 현재 지표만으로 모델 간 차이를 구분할 수 없습니다.",
  "At least one k value exceeds the catalog size; interpret those metrics cautiously.":
    "일부 k 값이 카탈로그 크기보다 커서 해당 지표는 참고용으로만 해석해야 합니다."
};

export default function Page() {
  const [preferences, setPreferences] = useState<UserPreferences>(defaultPreferences);
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [requestError, setRequestError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<TabId>("recommend");
  const [catalogHealth, setCatalogHealth] = useState<CatalogHealth | null>(null);

  const currentReport = report;
  const recommendations = currentReport?.recommendations ?? [];
  const allEvidence = recommendations.flatMap((recommendation) =>
    recommendation.evidence.map((snippet) => ({ ...snippet, productName: recommendation.product.name }))
  );
  const topAspects = Object.entries(
    allEvidence.reduce<Record<string, number>>((counts, snippet) => {
      snippet.aspects.forEach((aspect) => {
        counts[aspect] = (counts[aspect] ?? 0) + 1;
      });
      return counts;
    }, {})
  )
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6);

  useEffect(() => {
    function syncTabFromHash() {
      const hashTab = window.location.hash.replace("#", "") as TabId;
      if (tabs.includes(hashTab)) {
        setActiveTab(hashTab);
      }
    }

    syncTabFromHash();
    window.addEventListener("hashchange", syncTabFromHash);
    return () => window.removeEventListener("hashchange", syncTabFromHash);
  }, []);

  useEffect(() => {
    void fetchCatalogHealth().then(setCatalogHealth);
  }, []);

  async function handleGenerate(nextPreferences = preferences) {
    setIsLoading(true);
    setRequestError(null);
    const result = await fetchReport(nextPreferences);
    setReport(result.report);
    setRequestError(result.error);
    setIsLoading(false);
  }

  function handlePreferenceChange(nextPreferences: UserPreferences) {
    setPreferences(nextPreferences);
    setReport(null);
    setRequestError(null);
  }

  function handleDemoSelect(nextPreferences: UserPreferences) {
    setPreferences(nextPreferences);
    setReport(null);
    void handleGenerate(nextPreferences);
  }

  function handleTabChange(tab: string) {
    const nextTab = tab as TabId;
    setActiveTab(nextTab);
    window.history.replaceState(null, "", `#${nextTab}`);
  }

  return (
    <AppShell activeTab={activeTab} onTabChange={handleTabChange}>
      {activeTab === "recommend" && (
        <main className="workspace">
          <div className="workspace-sidebar">
            <PreferenceForm
              preferences={preferences}
              onChange={handlePreferenceChange}
              onDemoSelect={handleDemoSelect}
              onGenerate={handleGenerate}
              isLoading={isLoading}
            />
            {requestError && (
              <p className="request-error" role="alert">
                {requestError}
              </p>
            )}
          </div>
          <RecommendationReport catalogHealth={catalogHealth} report={currentReport} />
        </main>
      )}

      {activeTab === "compare" && (
        <main className="tab-page">
          <ProductComparison recommendations={recommendations} />
        </main>
      )}

      {activeTab === "insights" && (
        <main className="tab-page">
          <section className="insights-layout">
            <div className="content-panel">
              <p className="eyebrow">리뷰 분석</p>
              <h1>리뷰 근거가 추천을 설명하는 방식</h1>
              <p className="summary">
                추천 후보와 연결된 리뷰 문장을 aspect 단위로 모아 어떤 조건이 랭킹에 영향을
                주었는지 확인합니다.
              </p>
              {currentReport && recommendations.length ? (
                <>
                  <div className="insight-summary-grid">
                    <div className="metric-card">
                      <span>추천 후보</span>
                      <strong>{recommendations.length}</strong>
                    </div>
                    <div className="metric-card">
                      <span>리뷰 근거</span>
                      <strong>{allEvidence.length}</strong>
                    </div>
                    <div className="metric-card">
                      <span>1순위</span>
                      <strong>{recommendations[0].product.name}</strong>
                    </div>
                  </div>
                  <section className="aspect-panel">
                    <h2>Aspect coverage</h2>
                    {topAspects.map(([aspect, count]) => (
                      <div className="metric-row" key={aspect}>
                        <span>{presentLabel(aspect)}</span>
                        <meter max={Math.max(...topAspects.map(([, value]) => value))} min={0} value={count} />
                        <strong>{count}</strong>
                      </div>
                    ))}
                  </section>
                </>
              ) : (
                <p className="empty-inline">
                  {currentReport
                    ? "현재 조건에 맞는 추천 상품이 없습니다."
                    : "추천 프로필을 먼저 입력해 주세요."}
                </p>
              )}
            </div>
            <div className="content-panel">
              <p className="eyebrow">Evidence audit</p>
              <h2>선택된 리뷰 근거</h2>
              {allEvidence.map((snippet) => (
                <article className="evidence-card" key={snippet.review_id}>
                  <p className="eyebrow">{snippet.productName}</p>
                  <blockquote>{presentReviewExcerpt(snippet.text)}</blockquote>
                  <figcaption>
                    {snippet.sentiment} · relevance {snippet.relevance.toFixed(1)}
                  </figcaption>
                  <div className="tag-row">
                    {snippet.aspects.map((aspect) => (
                      <span className="tag tag-soft" key={aspect}>
                        {presentLabel(aspect)}
                      </span>
                    ))}
                  </div>
                </article>
              ))}
            </div>
          </section>
        </main>
      )}

      {activeTab === "experiments" && (
        <main className="tab-page">
          <section className="content-panel">
            <p className="eyebrow">실험</p>
            <h1>랭킹 모델 비교</h1>
            <div className="metrics-grid">
              {[
                ["평가 카탈로그", `${samplePublicEvaluation.product_count}개 제품`],
                [
                  "relevance coverage",
                  `${Math.round(samplePublicEvaluation.coverage.relevant_product_rate * 100)}%`
                ],
                ["recall@3", samplePublicEvaluation.models.hybrid.metrics["recall@3"].toFixed(4)],
                ["ndcg@3", samplePublicEvaluation.models.hybrid.metrics["ndcg@3"].toFixed(4)]
              ].map(([label, value]) => (
                <div className="metric-card" key={label}>
                  <span>{label}</span>
                  <strong>{value}</strong>
                </div>
              ))}
            </div>
            <section className="evaluation-status" aria-label="Evaluation integrity">
              <strong>
                {samplePublicEvaluation.comparative_ready ? "비교 가능" : "탐색용 평가"}
              </strong>
              <p>
                {samplePublicEvaluation.comparative_ready
                  ? "동일한 데이터와 기준으로 모델 변경을 비교할 수 있습니다."
                  : "현재 결과는 평가 파이프라인의 재현성을 확인하기 위한 샘플이며, 모델 성능의 일반화 근거로 사용하지 않습니다."}
              </p>
              {!samplePublicEvaluation.comparative_ready && (
                <ul>
                  {samplePublicEvaluation.warnings.map((warning) => (
                    <li key={warning}>{evaluationWarningCopy[warning] ?? warning}</li>
                  ))}
                </ul>
              )}
            </section>
            <section className="evaluation-status" aria-label="Temporal evaluation integrity">
              <strong>
                시간 분리 평가: {samplePublicEvaluation.temporal_user_holdout.comparative_ready ? "비교 가능" : "준비 중"}
              </strong>
              <p>
                사용자별 마지막 긍정 상호작용을 보류하고, 그 시점 이전의 리뷰만으로 순위를 계산합니다.
              </p>
              {!samplePublicEvaluation.temporal_user_holdout.comparative_ready && (
                <p>
                  현재 샘플은 적격 사용자가 {samplePublicEvaluation.temporal_user_holdout.eligible_user_count}명으로,
                  비교 기준인 {samplePublicEvaluation.temporal_user_holdout.minimum_holdouts}명에 미달합니다.
                </p>
              )}
            </section>
            <div className="evaluation-table" role="table" aria-label="Public evaluation metrics">
              <div className="evaluation-row evaluation-head" role="row">
                <span>model</span>
                <span>precision@1</span>
                <span>recall@3</span>
                <span>ndcg@3</span>
                <span>top ids</span>
              </div>
              {Object.entries(samplePublicEvaluation.models).map(([model, result]) => (
                <div className="evaluation-row" key={model} role="row">
                  <strong>{model}</strong>
                  <span>{result.metrics["precision@1"].toFixed(4)}</span>
                  <span>{result.metrics["recall@3"].toFixed(4)}</span>
                  <span>{result.metrics["ndcg@3"].toFixed(4)}</span>
                  <span>{result.ranked_product_ids.slice(0, 3).join(", ")}</span>
                </div>
              ))}
            </div>
          </section>
        </main>
      )}

      {activeTab === "portfolio" && (
        <main className="tab-page">
          <section className="content-panel">
            <p className="eyebrow">구성</p>
            <h1>프로젝트 구조</h1>
            <div className="portfolio-grid">
              <a href="https://github.com/Samuel-0930/glowfit-ai" rel="noreferrer" target="_blank">
                <strong>GitHub README</strong>
                <span>데모, 모델 스택, 평가 지표, 실행 방법을 확인합니다.</span>
              </a>
              <a
                href="https://app.notion.com/p/3996f7e3d828811fa0d7e358a783d6f6"
                rel="noreferrer"
                target="_blank"
              >
                <strong>Notion case study</strong>
                <span>문제 정의, 데이터 파이프라인, 핵심 개념을 정리했습니다.</span>
              </a>
              <a href="https://github.com/Samuel-0930/glowfit-ai/pulls" rel="noreferrer" target="_blank">
                <strong>Pull requests</strong>
                <span>기능이 어떤 순서로 쌓였는지 볼 수 있습니다.</span>
              </a>
            </div>
          </section>
        </main>
      )}
    </AppShell>
  );
}
