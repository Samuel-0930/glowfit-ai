import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { RecommendationReport } from "../components/recommendation-report";
import { mockReport } from "../lib/mock-data";

describe("RecommendationReport", () => {
  it("renders summary, product, evidence, and model score labels", () => {
    render(<RecommendationReport report={mockReport} />);

    expect(screen.getByText(/Glow Barrier Gel Cream/)).toBeInTheDocument();
    expect(screen.getByText(/strongest match/)).toBeInTheDocument();
    expect(screen.getByText(/Review evidence/)).toBeInTheDocument();
    expect(screen.getByText(/two_tower/)).toBeInTheDocument();
  });
});
