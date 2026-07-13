import type { ReportResponse, UserPreferences } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type FetchReportResult =
  | { report: ReportResponse; error: null }
  | { report: null; error: string };

export async function fetchReport(preferences: UserPreferences): Promise<FetchReportResult> {
  try {
    const response = await fetch(`${API_BASE_URL}/recommendations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ preferences, limit: 3 })
    });
    if (!response.ok) {
      const body = (await response.json().catch(() => null)) as { detail?: string } | null;
      return {
        report: null,
        error: body?.detail ?? "추천 결과를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요."
      };
    }
    return { report: (await response.json()) as ReportResponse, error: null };
  } catch {
    return {
      report: null,
      error: "추천 API에 연결할 수 없습니다. 서버 상태를 확인한 뒤 다시 시도해 주세요."
    };
  }
}
