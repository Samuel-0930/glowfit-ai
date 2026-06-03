import "@testing-library/jest-dom/vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Page from "../app/page";
import { inferRecommendations } from "../lib/mock-data";

describe("recommendation flow", () => {
  it("starts empty and renders recommendations after the profile is configured", async () => {
    window.history.replaceState(null, "", "#recommend");
    render(<Page />);

    expect(screen.getByText(/피부 타입, 고민, 제형/)).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText("피부 타입"), { target: { value: "oily" } });
    fireEvent.change(screen.getByLabelText("선호 제형"), { target: { value: "watery" } });
    fireEvent.change(screen.getByLabelText("향 민감도"), { target: { value: "medium" } });
    fireEvent.click(screen.getByRole("button", { name: "acne" }));
    fireEvent.click(screen.getByRole("button", { name: "pores" }));

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "Pore Reset Water Serum" })).toBeInTheDocument();
    });
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
