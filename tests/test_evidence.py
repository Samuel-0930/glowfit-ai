from src.glowfit.evidence import EvidenceIndex
from src.glowfit.schemas import Review


def test_evidence_index_returns_relevant_review_snippets():
    reviews = [
        Review(
            review_id="r1",
            user_id="u1",
            product_id="p1",
            rating=5,
            text="Fragrance free and gentle for dry skin.",
            timestamp="2025-01-01",
        ),
        Review(
            review_id="r2",
            user_id="u2",
            product_id="p2",
            rating=4,
            text="Matte sunscreen for oily skin.",
            timestamp="2025-01-02",
        ),
    ]

    index = EvidenceIndex.from_reviews(reviews)
    snippets = index.search(product_id="p1", query_terms=["fragrance", "dry skin"], limit=2)

    assert len(snippets) == 1
    assert snippets[0].review_id == "r1"
    assert snippets[0].sentiment == "positive"
    assert snippets[0].relevance > 0
