from src.glowfit.datasets import parse_amazon_metadata_record, parse_amazon_review_record


def test_parse_amazon_metadata_record_maps_catalog_fields():
    record = {
        "asin": "B001",
        "title": "Barrier Gel Cream",
        "brand": "Aster Lab",
        "price": "$24.00",
        "average_rating": 4.6,
        "rating_number": 1180,
        "features": ["Fragrance free", "Light texture", "Dry skin"],
        "categories": [["Beauty", "Skin Care", "Face", "Moisturizers"]],
    }

    product = parse_amazon_metadata_record(record)

    assert product.product_id == "B001"
    assert product.name == "Barrier Gel Cream"
    assert product.category == "moisturizers"
    assert product.price_usd == 24.0
    assert product.review_count == 1180
    assert product.attributes == ["fragrance free", "light texture", "dry skin"]


def test_parse_amazon_review_record_maps_review_fields():
    record = {
        "reviewerID": "A1",
        "asin": "B001",
        "overall": 5,
        "reviewText": "Light texture and soothing for dry skin.",
        "unixReviewTime": 1735689600,
    }

    review = parse_amazon_review_record(record, fallback_index=7)

    assert review.review_id == "amazon_B001_7"
    assert review.user_id == "A1"
    assert review.product_id == "B001"
    assert review.rating == 5
    assert review.timestamp == "2025-01-01"
