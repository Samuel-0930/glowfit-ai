import type { Recommendation } from "../lib/types";

export function EvidencePanel({ recommendation }: { recommendation: Recommendation }) {
  return (
    <aside className="evidence-panel">
      <h2>Review evidence</h2>
      {recommendation.evidence.map((snippet) => (
        <figure key={snippet.review_id} className="evidence-card">
          <blockquote>{snippet.text}</blockquote>
          <figcaption>
            {snippet.sentiment} · relevance {snippet.relevance.toFixed(1)}
          </figcaption>
          <div className="tag-row">
            {snippet.aspects.map((aspect) => (
              <span key={aspect} className="tag tag-soft">
                {aspect}
              </span>
            ))}
          </div>
        </figure>
      ))}
    </aside>
  );
}
