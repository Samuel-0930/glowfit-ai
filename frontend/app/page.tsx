"use client";

import { useEffect, useState } from "react";

import { AppShell } from "../components/app-shell";
import { PreferenceForm } from "../components/preference-form";
import { ProductComparison } from "../components/product-comparison";
import { RecommendationReport } from "../components/recommendation-report";
import { fetchReport } from "../lib/api";
import { defaultPreferences } from "../lib/mock-data";
import { samplePublicEvaluation } from "../lib/sample-public-evaluation";
import type { ReportResponse, UserPreferences } from "../lib/types";

type TabId = "recommend" | "compare" | "insights" | "experiments" | "portfolio";

const tabs: TabId[] = ["recommend", "compare", "insights", "experiments", "portfolio"];

export default function Page() {
  const [preferences, setPreferences] = useState<UserPreferences>(defaultPreferences);
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [requestError, setRequestError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<TabId>("recommend");

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

  async function handleGenerate() {
    setIsLoading(true);
    setRequestError(null);
    const result = await fetchReport(preferences);
    setReport(result.report);
    setRequestError(result.error);
    setIsLoading(false);
  }

  function handlePreferenceChange(nextPreferences: UserPreferences) {
    setPreferences(nextPreferences);
    setReport(null);
    setRequestError(null);
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
          <PreferenceForm
            preferences={preferences}
            onChange={handlePreferenceChange}
            onGenerate={handleGenerate}
            isLoading={isLoading}
          />
          {requestError && (
            <p className="request-error" role="alert">
              {requestError}
            </p>
          )}
          <RecommendationReport report={currentReport} />
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
                        <span>{aspect}</span>
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
                  <blockquote>{snippet.text}</blockquote>
                  <figcaption>
                    {snippet.sentiment} · relevance {snippet.relevance.toFixed(1)}
                  </figcaption>
                  <div className="tag-row">
                    {snippet.aspects.map((aspect) => (
                      <span className="tag tag-soft" key={aspect}>
                        {aspect}
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
                ["precision@1", "1.0000"],
                ["recall@3", samplePublicEvaluation.models.hybrid.metrics["recall@3"].toFixed(4)],
                ["ndcg@3", samplePublicEvaluation.models.hybrid.metrics["ndcg@3"].toFixed(4)]
              ].map(([label, value]) => (
                <div className="metric-card" key={label}>
                  <span>{label}</span>
                  <strong>{value}</strong>
                </div>
              ))}
            </div>
            <p className="muted">
              `artifacts/sample`의 products.json과 reviews.json을 기준으로 재생성한 오프라인
              평가입니다. 작은 샘플에서는 지표가 과도하게 높게 나올 수 있어, 모델 성능의 일반화
              근거로 해석하지 않습니다.
            </p>
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
