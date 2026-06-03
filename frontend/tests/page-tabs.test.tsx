import "@testing-library/jest-dom/vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Page from "../app/page";

describe("Page tabs", () => {
  it("shows recruiter testing guidance and switches to portfolio content", () => {
    render(<Page />);

    expect(screen.getByText(/채용자가 바로 테스트할 수 있는 것/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Portfolio" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Portfolio" }));

    expect(screen.getByText(/포트폴리오 검토 순서/)).toBeInTheDocument();
    expect(screen.getByText(/GitHub README/)).toBeInTheDocument();
  });

  it("opens the matching tab from the URL hash", async () => {
    window.history.replaceState(null, "", "#experiments");

    render(<Page />);

    await waitFor(() => {
      expect(screen.getByText(/모델별 ranking을 어떻게 비교했는가/)).toBeInTheDocument();
    });
  });

  it("shows public evaluation artifact output in experiments", async () => {
    window.history.replaceState(null, "", "#experiments");

    render(<Page />);

    await waitFor(() => {
      expect(screen.getByText(/public_evaluation.json 예시/)).toBeInTheDocument();
    });
    expect(screen.getByText("hybrid")).toBeInTheDocument();
    expect(screen.getByText(/python scripts\/evaluate_public_artifacts.py/)).toBeInTheDocument();
  });
});
