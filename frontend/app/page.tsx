"use client";

import { useEffect, useState } from "react";

import { AppShell } from "../components/app-shell";
import { PreferenceForm } from "../components/preference-form";
import { ProductComparison } from "../components/product-comparison";
import { RecommendationReport } from "../components/recommendation-report";
import { fetchCatalogHealth, fetchReport } from "../lib/api";
import { defaultPreferences } from "../lib/mock-data";
import { presentLabel, presentReviewExcerpt } from "../lib/presentation";
import type { CatalogHealth, ReportResponse, UserPreferences } from "../lib/types";

type TabId = "recommend" | "compare" | "insights" | "portfolio";

const tabs: TabId[] = ["recommend", "compare", "insights", "portfolio"];

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

      {activeTab === "portfolio" && (
        <main className="tab-page">
          <section className="content-panel">
            <p className="eyebrow">구성</p>
            <h1>추천 시스템을 제품 경험으로 연결한 구조</h1>
            <p className="summary portfolio-summary-copy">
              데이터 수집부터 랭킹, 리뷰 근거, 운영 검증까지 하나의 사용자 흐름으로 연결했습니다.
            </p>
            <div className="portfolio-overview" aria-label="프로젝트 핵심 구성">
              <div>
                <span>운영 카탈로그</span>
                <strong>{catalogHealth ? `${catalogHealth.product_count}개 제품` : "Supabase 카탈로그"}</strong>
                <p>{catalogHealth ? `리뷰 ${catalogHealth.review_count.toLocaleString()}개를 연결해 운영 중입니다.` : "제품과 리뷰를 연결해 운영합니다."}</p>
              </div>
              <div>
                <span>추천 경험</span>
                <strong>조건 → 근거</strong>
                <p>피부 프로필과 회피 조건을 순위와 리뷰 근거로 함께 설명합니다.</p>
              </div>
              <div>
                <span>신뢰성</span>
                <strong>배포 후 검증</strong>
                <p>Vercel 배포와 GitHub Actions smoke check로 사용자 흐름을 확인합니다.</p>
              </div>
            </div>
            <section className="portfolio-section" aria-labelledby="portfolio-strengths-title">
              <div>
                <p className="eyebrow">Portfolio focus</p>
                <h2 id="portfolio-strengths-title">이 프로젝트에서 확인할 수 있는 역량</h2>
              </div>
              <ul className="portfolio-checklist">
                <li><strong>데이터 파이프라인</strong><span>공개 상품·리뷰 데이터를 정제하고 Supabase 카탈로그로 적재</span></li>
                <li><strong>추천 시스템</strong><span>프로필·상품 태그·리뷰 신호·예산을 결합한 하이브리드 랭킹</span></li>
                <li><strong>제품화</strong><span>추천 이유와 주의 신호를 UI에 노출하고 배포 후 흐름을 자동 점검</span></li>
              </ul>
            </section>
            <div className="portfolio-grid">
              <a href="https://github.com/Samuel-0930/glowfit-ai" rel="noreferrer" target="_blank">
                <strong>GitHub README</strong>
                <span>데모 화면, 시스템 구조, 실행·검증 방법을 확인합니다.</span>
              </a>
              <a
                href="https://app.notion.com/p/3996f7e3d828811fa0d7e358a783d6f6"
                rel="noreferrer"
                target="_blank"
              >
                <strong>Notion case study</strong>
                <span>문제 정의, 데이터 파이프라인, 핵심 개념을 정리했습니다.</span>
              </a>
              <a
                href="https://github.com/Samuel-0930/glowfit-ai/blob/main/docs/architecture.md"
                rel="noreferrer"
                target="_blank"
              >
                <strong>Architecture</strong>
                <span>프론트엔드, API, 카탈로그 저장소, 랭킹 흐름을 확인합니다.</span>
              </a>
            </div>
          </section>
        </main>
      )}
    </AppShell>
  );
}
