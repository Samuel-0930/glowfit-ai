from pathlib import Path

from src.glowfit.artifacts import build_sample_artifacts, load_artifacts


def test_build_and_load_sample_artifacts(tmp_path: Path):
    artifact_dir = tmp_path / "artifacts"

    build_sample_artifacts(
        product_path=Path("sample_data/products.json"),
        review_path=Path("sample_data/reviews.json"),
        artifact_dir=artifact_dir,
    )
    artifacts = load_artifacts(artifact_dir)

    assert len(artifacts.products) == 3
    assert len(artifacts.reviews) == 5
    assert artifacts.evidence_index.search("p_glow_gel", ["dry skin"], limit=1)
