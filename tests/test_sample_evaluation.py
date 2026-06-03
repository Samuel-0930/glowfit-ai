from pathlib import Path

from src.glowfit.sample_evaluation import build_sample_evaluation_report


def test_build_sample_evaluation_report_scores_default_profile():
    report = build_sample_evaluation_report(Path("sample_data"))

    assert report["profile"] == "default_dry_sensitive_profile"
    assert report["ranked_product_ids"][0] == "p_glow_gel"
    assert report["relevant_product_ids"] == ["p_glow_gel", "p_calm_ampoule"]
    assert report["metrics"]["precision@1"] == 1.0
    assert report["metrics"]["recall@3"] == 1.0
