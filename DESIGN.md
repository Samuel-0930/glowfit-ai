# GlowFit Design System — Montage-inspired

## 1. 방향

GlowFit은 피부 조건을 입력하면 제품 순위뿐 아니라 선택 근거와 리뷰 문장까지 설명하는 스킨케어 추천 워크스페이스다. 첫인상은 차분한 커머스 서비스여야 하고, 사용자가 더 깊이 들어갈수록 데이터·모델의 투명성이 드러나야 한다.

- 소비자 화면: 추천 결과와 이유를 빠르게 읽는 중간 밀도 UI
- 분석 화면: 리뷰 신호와 평가 결과를 비교하는 높은 밀도 UI
- 시각 언어: 흰색 중심, 절제된 녹색 강조, 명확한 타이포 위계, 목적 있는 여백
- 피해야 할 것: 장식용 그라데이션, AI를 암시하는 추상 그래픽, 과도한 카드 중첩, 설명 없는 점수

이 시스템은 Wanted Montage의 그리드, 타이포그래피, 시멘틱 토큰 원칙을 참고하되 GlowFit의 정보 구조와 브랜드 색상에 맞춰 재구성한다. Montage 컴포넌트 소스나 패키지를 직접 복제하지 않는다.

참고 문서:

- [Getting Started](https://montage.wanted.co.kr/docs/getting-started)
- [Grid](https://montage.wanted.co.kr/docs/foundations/base-material/grid)
- [Typography](https://montage.wanted.co.kr/docs/foundations/base-material/typography)
- [Color](https://montage.wanted.co.kr/docs/foundations/base-material/color)

직접적인 Montage 소스 사용이 추가될 경우 MIT 라이선스와 저작권 고지를 함께 포함한다.

## 2. 토큰

### Color

원시 색상 이름보다 사용 목적을 나타내는 시멘틱 이름을 우선한다.

| Token | Value | Role |
| --- | --- | --- |
| `background-normal` | `#ffffff` | 주요 패널과 입력 배경 |
| `background-alternative` | `#f7f8f6` | 앱 캔버스와 낮은 위계 영역 |
| `label-normal` | `#171719` | 제목과 핵심 본문 |
| `label-neutral` | `#46474c` | 설명과 메타데이터 |
| `label-alternative` | `#70737c` | 캡션과 보조 정보 |
| `line-normal` | `#e1e2e4` | 일반 구분선 |
| `line-strong` | `#c9cbd0` | 입력 경계와 강조 구분선 |
| `primary-normal` | `#0f7b3e` | CTA, 선택, 핵심 적합 근거 |
| `primary-subtle` | `#e9f7ed` | 선택 배경과 추천 요약 |
| `status-danger` | `#b4233c` | 주의 및 오류 |
| `status-positive` | `#176b38` | 연결 및 정상 상태 |

규칙:

- 녹색은 선택, 주요 CTA, 추천 근거에만 사용한다.
- 상태는 색상만으로 전달하지 않고 텍스트와 함께 표시한다.
- 패널 구분은 그림자보다 배경 차이와 1px 선을 우선한다.

### Typography

기본 서체는 `Pretendard Variable`, 대체 서체는 Pretendard와 시스템 산세리프다. 한국어 서비스이므로 Montage의 Pretendard JP 선택을 한국어용 Pretendard로 조정했다.

| Token | Size / Line height | Weight | Use |
| --- | --- | --- | --- |
| `display-2` | `40 / 52px` | 700 | 비어 있는 추천 결과의 핵심 문장 |
| `title-1` | `32 / 44px` | 700 | 페이지·리포트 제목 |
| `title-3` | `24 / 32px` | 700 | 패널 제목 |
| `heading-1` | `22 / 30px` | 700 | 추천 이유와 근거 패널 제목 |
| `heading-2` | `20 / 28px` | 700 | 카드·분석 섹션 제목 |
| `headline-1` | `18 / 26px` | 700 | 제품명 |
| `body-1-reading` | `16 / 26px` | 400 | 주요 설명과 리뷰 본문 |
| `label-1` | `14 / 20px` | 600 | 필드명과 버튼 |
| `label-2` | `13 / 18px` | 500 | 메타데이터와 칩 |
| `caption-1` | `12 / 16px` | 600 | eyebrow와 상태 캡션 |

폰트 크기는 뷰포트에 따라 유동적으로 확대하지 않는다. 모바일에서는 display만 한 단계 낮추고 본문은 16px을 유지한다.

### Spacing

4px 원자 단위를 사용하고, 일반 배치는 4의 배수로 구성한다. 반복 컴포넌트 사이의 기본 거터는 20px이다.

| Token | Value |
| --- | --- |
| `space-1` | 4px |
| `space-2` | 8px |
| `space-3` | 12px |
| `space-4` | 16px |
| `space-5` | 20px |
| `space-6` | 24px |
| `space-8` | 32px |
| `space-10` | 40px |
| `space-12` | 48px |
| `space-16` | 64px |

2px과 1px은 아이콘과 테두리의 시각 보정에만 사용한다.

### Shape

| Token | Value | Use |
| --- | --- | --- |
| `radius-xs` | 4px | 작은 브랜드 배지 |
| `radius-sm` | 6px | 소형 컨트롤 |
| `radius-md` | 8px | 입력, 버튼, 내부 패널 |
| `radius-lg` | 12px | 주요 작업 패널 |
| `radius-full` | 9999px | 태그와 원형 점수 |

## 3. Grid와 반응형

Montage의 20px column gap과 12/3/2 column 원칙을 따른다.

| Range | Layout |
| --- | --- |
| `0–767px` | 2열 개념, 실제 작업 패널은 1열 스택 |
| `768–991px` | 3열 개념, 입력 필드는 2열 |
| `992–1279px` | 좌측 입력 320px + 결과 1열, 근거 패널은 결과 아래 |
| `1280px+` | 좌측 입력 320px + 중앙 결과 + 우측 근거 340px |

- 앱 최대 너비는 1440px, 좌우 페이지 패딩은 20px이다.
- 1440px는 3개 작업 영역을 동시에 보여주기 위한 GlowFit 전용 확장 규칙이다.
- 데이터 분석 화면은 최대 너비 안에서 12열 그리드처럼 구성하되, 표는 작은 화면에서 가로 스크롤을 허용한다.
- 모바일 순서는 프로필 → 추천 결과 → 리뷰 근거다.

## 4. 컴포넌트 원칙

### App shell

- 72px 상단 내비게이션을 사용한다.
- 활성 탭은 텍스트 굵기와 2px primary indicator로 구분한다.
- 모바일 탭은 줄바꿈하지 않고 가로 스크롤한다.

### Controls

- select와 주요 버튼은 48px 높이를 사용한다.
- 선택 칩은 최소 36px, 내비게이션과 주요 액션은 최소 44px 터치 영역을 확보한다.
- 입력 이름은 시각적으로 표시하고 control과 연결한다.
- 비활성 버튼은 색 대비를 낮추되 상태를 텍스트로 이해할 수 있어야 한다.

### Recommendation report

- 1위 이유 → 상위 3개 제품 → 랭킹 상세 순서로 읽힌다.
- 적합도는 사용자 입력과 제품·리뷰 신호의 일치 정도이며 모델 정확도가 아니다.
- 근거 강도와 적합도는 같은 시각 언어를 사용하되 라벨을 항상 표시한다.
- 주의 신호는 제품 근거 바로 아래에 둔다.

### Product card

- 순위 블록, 제품명·메타데이터, 적합도, 핵심 근거 순으로 배치한다.
- 실제 이미지가 없는 상태에서는 장식 이미지 대신 중립적인 순위 블록을 사용한다.
- 제품명은 줄임표로 숨기지 않고 자연스럽게 줄바꿈한다.
- 1위만 상단 3px 선으로 강조하고 나머지 카드와 구조는 동일하게 유지한다.

### Evidence panel

- 데스크톱에서는 화면에 고정해 추천 결과와 함께 비교할 수 있게 한다.
- 리뷰 본문은 최소 14/22px, 핵심 설명은 16/26px 이상으로 유지한다.
- 리뷰 문장, 출처 성격, aspect 태그 순으로 읽힌다.

### Comparison and analysis

- 비교 항목의 순서와 라벨을 모든 후보에서 동일하게 유지한다.
- 카드 자체보다 항목 간 구분선과 타이포 위계로 비교 가능성을 만든다.
- 1.0 값은 모델 성능으로 표현하지 않고 현재 샘플에서 계산된 랭킹 신호임을 설명한다.
- 평가 탭은 일반화 성능을 주장할 수 있는 데이터 규모와 분리 기준이 갖춰졌는지 먼저 보여준다.

## 5. 접근성·모션

- 모든 인터랙션에 `:focus-visible`을 제공한다.
- 동적 오류는 `role="alert"`, 데이터 연결 상태는 `role="status"`로 전달한다.
- 선택 칩은 `aria-pressed`, 현재 탭은 `aria-current="page"`를 사용한다.
- 본문과 주요 컨트롤은 WCAG AA 대비를 목표로 한다.
- `prefers-reduced-motion: reduce`에서는 등장 애니메이션과 transition을 사실상 제거한다.
- hover만으로 의미를 전달하지 않는다.

## 6. 완료 전 시각 QA

- 1440px: 입력, 추천 결과, 근거 패널이 겹치거나 불필요하게 늘어나지 않는가
- 1024px: 근거 패널이 결과 아래로 자연스럽게 이동하는가
- 390px: 탭, 긴 제품명, 칩, 점수 원이 잘리거나 타원형으로 늘어나지 않는가
- 키보드: 탭 순서와 focus indicator가 명확한가
- 텍스트: 200% 확대에서도 내용이 유실되지 않는가
- 상태: 로딩, 오류, 빈 결과, 데이터 연결 상태가 색상 없이도 이해되는가
