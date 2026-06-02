import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.glowfit.artifacts import build_sample_artifacts

if __name__ == "__main__":
    build_sample_artifacts(
        product_path=Path("sample_data/products.json"),
        review_path=Path("sample_data/reviews.json"),
        artifact_dir=Path("artifacts/sample"),
    )
    print("Built sample artifacts in artifacts/sample")
