import "@testing-library/jest-dom/vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import Page from "../app/page";
import { inferRecommendations } from "../lib/mock-data";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("recommendation flow", () => {
  it("starts empty and renders recommendations after the profile is configured", async () => {
    const report = inferRecommendations({
      skin_type: "oily",
      concerns: ["acne", "pores"],
      texture: "watery",
      fragrance_sensitivity: "medium",
      budget_max_usd: 25,
      avoid: []
    });
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, json: async () => report })
    );
    window.history.replaceState(null, "", "#recommend");
    render(<Page />);

    expect(screen.getByText(/나의 피부 조건을/)).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText("피부 타입"), { target: { value: "oily" } });
    fireEvent.change(screen.getByLabelText("선호 제형"), { target: { value: "watery" } });
    fireEvent.change(screen.getByLabelText("향 민감도"), { target: { value: "medium" } });
    fireEvent.click(screen.getByRole("button", { name: "트러블" }));
    fireEvent.click(screen.getByRole("button", { name: "모공" }));
    fireEvent.click(screen.getByRole("button", { name: "추천 받기" }));

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "Pore Reset Water Serum" })).toBeInTheDocument();
    });
    expect(screen.getByRole("heading", { name: "왜 Pore Reset Water Serum인가요?" })).toBeInTheDocument();
    expect(screen.getByText("랭킹 상세 보기")).toBeInTheDocument();
  });

  it("loads a recommendation from a quick demo profile", async () => {
    const report = inferRecommendations({
      skin_type: "oily",
      concerns: ["acne", "pores"],
      texture: "watery",
      fragrance_sensitivity: "medium",
      budget_max_usd: 25,
      avoid: ["sticky finish"]
    });
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, json: async () => report })
    );
    render(<Page />);

    fireEvent.click(screen.getByRole("button", { name: /지성 · 트러블/ }));

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "Pore Reset Water Serum" })).toBeInTheDocument();
    });
  });

  it("shows an API error instead of presenting a mock result", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        json: async () => ({ detail: "추천 카탈로그에 일시적으로 연결할 수 없습니다." })
      })
    );
    window.history.replaceState(null, "", "#recommend");
    render(<Page />);

    fireEvent.change(screen.getByLabelText("피부 타입"), { target: { value: "dry" } });
    fireEvent.change(screen.getByLabelText("선호 제형"), { target: { value: "light" } });
    fireEvent.change(screen.getByLabelText("향 민감도"), { target: { value: "high" } });
    fireEvent.click(screen.getByRole("button", { name: "붉은기" }));
    fireEvent.click(screen.getByRole("button", { name: "추천 받기" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("일시적으로 연결할 수 없습니다");
    expect(screen.getByText(/나의 피부 조건을/)).toBeInTheDocument();
    expect(screen.queryByRole("heading", { name: "상위 추천 3개" })).not.toBeInTheDocument();
  });

  it("shows an empty-result state when the API returns no recommendations", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          summary: "No recommendations were generated for the current profile.",
          recommendations: [],
          generation_mode: "api-hybrid-ranking",
          metadata: {
            data_source: "supabase",
            product_count: 0,
            review_count: 0,
            requested_limit: 3,
            returned_count: 0,
            top_product_id: null
          }
        })
      })
    );
    window.history.replaceState(null, "", "#recommend");
    render(<Page />);

    fireEvent.change(screen.getByLabelText("피부 타입"), { target: { value: "dry" } });
    fireEvent.change(screen.getByLabelText("선호 제형"), { target: { value: "light" } });
    fireEvent.change(screen.getByLabelText("향 민감도"), { target: { value: "high" } });
    fireEvent.click(screen.getByRole("button", { name: "붉은기" }));
    fireEvent.click(screen.getByRole("button", { name: "추천 받기" }));

    expect(await screen.findByText(/현재 조건에 맞는 추천 상품이 없습니다/)).toBeInTheDocument();
  });

  it("opens compare and insights tabs from hash navigation", async () => {
    window.history.replaceState(null, "", "#compare");
    render(<Page />);

    await waitFor(() => {
      expect(screen.getByText(/먼저 추천 탭에서 프로필/)).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: "리뷰 분석" }));

    expect(screen.getByRole("heading", { name: "리뷰 근거가 추천을 설명하는 방식" })).toBeInTheDocument();
  });

  it("scores products dynamically from the selected profile", () => {
    const report = inferRecommendations({
      skin_type: "sensitive",
      concerns: ["redness", "stinging"],
      texture: "cream",
      fragrance_sensitivity: "high",
      budget_max_usd: 30,
      avoid: ["essential oils"]
    });

    expect(report?.recommendations[0].product.name).toBe("Calm Cushion Repair Cream");
    expect(report?.recommendations).toHaveLength(3);
  });
});
