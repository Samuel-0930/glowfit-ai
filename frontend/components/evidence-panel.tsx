import type { Recommendation } from "../lib/types";
import { presentLabel, presentReviewExcerpt } from "../lib/presentation";

export function EvidencePanel({ recommendation }: { recommendation: Recommendation }) {
  return (
    <aside className="evidence-panel">
      <p className="eyebrow">추천 근거</p>
      <h2>리뷰로 확인한 이유</h2>
      {recommendation.evidence.map((snippet) => (
        <figure key={snippet.review_id} className="evidence-card">
          <blockquote>{presentReviewExcerpt(snippet.text)}</blockquote>
          <figcaption>
            {snippet.sentiment === "positive" ? "긍정 리뷰" : "참고 리뷰"} · 사용자 경험 근거
          </figcaption>
          <div className="tag-row">
            {snippet.aspects.map((aspect) => (
              <span key={aspect} className="tag tag-soft">
                {presentLabel(aspect)}
              </span>
            ))}
          </div>
        </figure>
      ))}
    </aside>
  );
}
