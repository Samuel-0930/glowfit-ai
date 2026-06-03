"use client";

import { useEffect, useState } from "react";

import { AppShell } from "../components/app-shell";
import { PreferenceForm } from "../components/preference-form";
import { ProductComparison } from "../components/product-comparison";
import { RecommendationReport } from "../components/recommendation-report";
import { fetchReport } from "../lib/api";
import { defaultPreferences, mockReport } from "../lib/mock-data";
import type { ReportResponse } from "../lib/types";

type TabId = "recommend" | "compare" | "insights" | "experiments" | "portfolio";

export default function Page() {
  const [report, setReport] = useState<ReportResponse>(mockReport);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<TabId>("recommend");

  useEffect(() => {
    const hashTab = window.location.hash.replace("#", "") as TabId;
    if (["recommend", "compare", "insights", "experiments", "portfolio"].includes(hashTab)) {
      setActiveTab(hashTab);
    }
  }, []);

  async function handleGenerate() {
    setIsLoading(true);
    const nextReport = await fetchReport(defaultPreferences);
    setReport(nextReport);
    setIsLoading(false);
  }

  function handleTabChange(tab: string) {
    const nextTab = tab as TabId;
    setActiveTab(nextTab);
    window.history.replaceState(null, "", `#${nextTab}`);
  }

  return (
    <AppShell activeTab={activeTab} onTabChange={handleTabChange}>
      {activeTab === "recommend" && (
        <>
          <section className="guide-panel">
            <div>
              <p className="eyebrow">Recruiter walkthrough</p>
              <h2>채용자가 바로 테스트할 수 있는 것</h2>
            </div>
            <ol className="guide-list">
              <li>왼쪽 profile 조건을 확인하고 Generate report를 눌러 API/report fallback 흐름을 봅니다.</li>
              <li>추천 카드에서 fit score, reasons, caution을 확인합니다.</li>
              <li>오른쪽 Review evidence에서 추천 근거 리뷰와 aspect tag를 확인합니다.</li>
            </ol>
          </section>
          <div className="workspace" id="recommend">
            <PreferenceForm
              preferences={defaultPreferences}
              onGenerate={handleGenerate}
              isLoading={isLoading}
            />
            <RecommendationReport report={report} />
          </div>
        </>
      )}

      {activeTab === "compare" && (
        <main className="tab-page">
          <ProductComparison recommendations={report.recommendations} />
        </main>
      )}

      {activeTab === "insights" && (
        <main className="tab-page">
          <section className="content-panel">
            <p className="eyebrow">Review Insights</p>
            <h1>리뷰 근거가 추천을 설명하는 방식</h1>
            <p className="summary">
              Evidence retrieval은 추천 상품과 사용자 조건에 관련 있는 리뷰 snippet을 찾아서
              설명 가능한 리포트로 연결합니다.
            </p>
            {report.recommendations[0].evidence.map((snippet) => (
              <article className="evidence-card" key={snippet.review_id}>
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
          </section>
        </main>
      )}

      {activeTab === "experiments" && (
        <main className="tab-page">
          <section className="content-panel">
            <p className="eyebrow">Experiments</p>
            <h1>모델별 ranking을 어떻게 비교했는가</h1>
            <div className="metrics-grid">
              {[
                ["precision@1", "1.0000"],
                ["recall@3", "1.0000"],
                ["ndcg@3", "0.9197"],
                ["python tests", "31 passed"]
              ].map(([label, value]) => (
                <div className="metric-card" key={label}>
                  <span>{label}</span>
                  <strong>{value}</strong>
                </div>
              ))}
            </div>
            <p className="muted">
              Public artifact evaluator는 products.json과 reviews.json을 읽고 popularity, rating,
              collaborative, content, two_tower, hybrid ranker를 같은 metric으로 비교합니다.
            </p>
          </section>
        </main>
      )}

      {activeTab === "portfolio" && (
        <main className="tab-page">
          <section className="content-panel">
            <p className="eyebrow">Portfolio</p>
            <h1>포트폴리오 검토 순서</h1>
            <div className="portfolio-grid">
              <a href="https://github.com/Samuel-0930/glowfit-ai" rel="noreferrer" target="_blank">
                <strong>GitHub README</strong>
                <span>데모 GIF, 모델 스택, 평가 지표, 실행 방법을 먼저 봅니다.</span>
              </a>
              <a
                href="https://app.notion.com/p/3746f7e3d82881919c76e7340a8a508a"
                rel="noreferrer"
                target="_blank"
              >
                <strong>Notion case study</strong>
                <span>문제 정의, 데이터 파이프라인, 핵심 개념 페이지를 확인합니다.</span>
              </a>
              <a href="https://github.com/Samuel-0930/glowfit-ai/pulls" rel="noreferrer" target="_blank">
                <strong>Pull requests</strong>
                <span>기능이 단계별로 어떻게 쌓였는지 구현 흐름을 확인합니다.</span>
              </a>
            </div>
          </section>
        </main>
      )}
    </AppShell>
  );
}
