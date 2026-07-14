import { describe, expect, it } from "vitest";

import { presentBrand, presentPrice, presentReviewExcerpt } from "../lib/presentation";

describe("presentation helpers", () => {
  it("hides placeholder brands and unavailable prices", () => {
    expect(presentBrand("Unknown")).toBeNull();
    expect(presentPrice(0)).toBe("가격 정보 없음");
    expect(presentPrice(20.99)).toBe("$20.99");
  });

  it("turns HTML-like review text into a compact readable excerpt", () => {
    expect(presentReviewExcerpt("First line.<br /><br />Second line.")).toBe("First line. Second line.");
    expect(presentReviewExcerpt("a".repeat(12), 10)).toBe("aaaaaaaaaa…");
  });
});
