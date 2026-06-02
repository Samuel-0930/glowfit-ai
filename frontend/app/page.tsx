"use client";

import { useState } from "react";

import { AppShell } from "../components/app-shell";
import { PreferenceForm } from "../components/preference-form";
import { ProductComparison } from "../components/product-comparison";
import { RecommendationReport } from "../components/recommendation-report";
import { fetchReport } from "../lib/api";
import { defaultPreferences, mockReport } from "../lib/mock-data";
import type { ReportResponse } from "../lib/types";

export default function Page() {
  const [report, setReport] = useState<ReportResponse>(mockReport);
  const [isLoading, setIsLoading] = useState(false);

  async function handleGenerate() {
    setIsLoading(true);
    const nextReport = await fetchReport(defaultPreferences);
    setReport(nextReport);
    setIsLoading(false);
  }

  return (
    <AppShell>
      <div className="workspace" id="recommend">
        <PreferenceForm
          preferences={defaultPreferences}
          onGenerate={handleGenerate}
          isLoading={isLoading}
        />
        <RecommendationReport report={report} />
      </div>
      <ProductComparison recommendations={report.recommendations} />
    </AppShell>
  );
}
