# Hugging Face Hub 직접 카탈로그 수집

## 목적

GlowFit의 공개 데이터 파이프라인은 Hugging Face Dataset Viewer를 빠른 preview 수단으로 사용한다. 다만 Viewer는 데이터셋별 인덱스 상태와 별개로 일시적인 503을 반환할 수 있다.

이 경로는 Viewer API를 거치지 않고 공개 Hugging Face Hub 원본 파일을 직접 사용한다.

- 메타데이터: `smartcat/Amazon_All_Beauty_2023`의 Parquet 파일
- 리뷰: `jhan21/amazon-beauty-reviews-dataset`의 CSV 파일
- 조인 키: 리뷰의 `parent_asin`과 메타데이터의 `parent_asin`

## 실행

```bash
uv run --extra ingestion python scripts/fetch_huggingface_hub_catalog.py \
  --max-products 25 \
  --min-reviews-per-product 3 \
  --max-reviews-per-product 20 \
  --max-review-rows 100000
```

기본 경로는 다음과 같다.

- 원본 메타데이터 캐시: `data/raw/huggingface/`
- 정제 카탈로그: `data/processed/hf_hub_catalog/`

두 경로 모두 Git에서 제외된다. 원본 메타데이터 Parquet만 캐시하고, 232MB 리뷰 CSV는 스트리밍 중 필요한 행까지만 읽는다.

## 산출물

- `products.json`: 스킨케어 관련 신호가 있고 최소 리뷰 수를 충족한 상품
- `reviews.json`: 부모 ASIN 기준으로 연결된 리뷰
- `summary.json`: 후보 상품 수, 실제 스캔한 리뷰 행 수, 생성된 상품·리뷰 수

`min_reviews_per_product`를 충족하지 못한 상품은 산출물에서 제외한다. 따라서 평가·리뷰 근거 화면에 상품만 있고 연결된 리뷰가 없는 상태를 만들지 않는다.

## 스킨케어 정제 규칙

원본 All Beauty 데이터는 스킨케어와 핸드·바디·립·네일·뷰티 도구를 함께 포함한다. GlowFit은 얼굴
스킨케어 추천을 목표로 하므로 제목 및 보조 메타데이터에 serum, moisturizer, sunscreen, cleanser,
toner, face mask, face oil 등의 신호가 있는 상품만 후보로 삼는다. 핸드·바디·립·네일, 화장품, 도구,
마사지기, 풋케어 등은 제목 기준으로 제외한다.

긴 원문 feature를 그대로 태그로 저장하지 않는다. `sensitive skin`, `fragrance free`, `calming`,
`barrier care`, `light texture`처럼 제한된 canonical tag로 정규화하고, 제품 유형도 sunscreen,
cleanser, serum 등으로 분류한다. 이 규칙은 추천 근거를 사람이 읽을 수 있는 짧은 표현으로 유지하기
위한 데이터 품질 계약이다.

## 확인한 장애와 대체 원칙

2026-07-14에 Dataset Viewer의 `is-valid`, `splits`, `rows` 요청은 두 공개 데이터셋에서 모두 HTTP 503을 반환했다. 반면 Hugging Face Hub API와 원본 파일 다운로드는 정상 동작했다.

Viewer는 편의 기능이고 데이터 원본이 아니다. 수집 파이프라인은 Viewer 실패를 데이터가 없다는 뜻으로 해석하지 않고, 원본 파일 경로를 대체 수단으로 사용한다.

## 다음 단계

이 스크립트가 만든 `products.json`과 `reviews.json`을 검토한 뒤 Supabase seed 형식으로 변환하고, 배포 API가 `sample_data` 대신 그 카탈로그를 읽도록 전환한다. 그 전에는 작은 산출물의 점수를 모델 성능으로 주장하지 않는다.
