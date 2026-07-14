from src.glowfit.schemas import Product, Review
from src.glowfit.supabase_seed import build_supabase_seed_sql


def test_build_supabase_seed_sql_escapes_content_and_replaces_catalog() -> None:
    sql = build_supabase_seed_sql(
        [
            Product(
                product_id="p_1",
                name="O'Brien's serum",
                category="serum",
                brand="Glow",
                price_usd=18.5,
                average_rating=4.2,
                review_count=4,
                attributes=["light texture", "light texture"],
            )
        ],
        [
            Review(
                review_id="r_1",
                user_id="u_1",
                product_id="p_1",
                rating=5,
                text="Didn't sting.",
                timestamp="2026-01-02",
            )
        ],
        replace=True,
    )

    assert sql.startswith("begin;")
    assert "delete from public.product_tags;" in sql
    assert "O''Brien''s serum" in sql
    assert "Didn''t sting." in sql
    assert sql.count("'light texture'") == 1
    assert sql.endswith("commit;\n")


def test_build_supabase_seed_sql_rejects_orphan_reviews() -> None:
    review = Review(
        review_id="r_1",
        user_id="u_1",
        product_id="missing",
        rating=5,
        text="Nice.",
        timestamp="2026-01-02",
    )

    try:
        build_supabase_seed_sql([], [review])
    except ValueError as error:
        assert "r_1" in str(error)
    else:
        raise AssertionError("Expected orphan review validation to fail")
