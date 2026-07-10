import { inferRecommendations, mockReport } from "./mock-data";
import type { ReportResponse, UserPreferences } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function fetchReport(preferences: UserPreferences): Promise<ReportResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/recommendations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ preferences, limit: 3 })
    });
    if (!response.ok) {
      return inferRecommendations(preferences) ?? mockReport;
    }
    return (await response.json()) as ReportResponse;
  } catch {
    return inferRecommendations(preferences) ?? mockReport;
  }
}
