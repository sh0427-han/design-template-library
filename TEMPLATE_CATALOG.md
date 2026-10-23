# Template Catalog · 8 HTML Reference Patterns

이 카탈로그는 **내용에 맞는 시각 패턴을 선택하는 지도**입니다. 정확한 데이터·수식·기하 조건은 [REFERENCE_PAGE_SPECS.md](docs/REFERENCE_PAGE_SPECS.md), 공통 토큰은 [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)를 따릅니다. 아래 설명은 현재 checkout의 HTML 원본을 기준으로 합니다. 초기 8종 통합의 출처·GitHub 이력은 [통합 보고서](docs/INTEGRATION_REPORT_2026-10-22.md)에 보존합니다.

| 번호 | 이름 | 선택할 때 | 실제 레이아웃 | 원본 · 최신 대표 프리뷰 |
| --- | --- | --- | --- | --- |
| 01 | Concept | 추상 개념을 구체적 사례와 숫자로 풀 때 | 단일 카드: 사진 → RGB 행렬 ROI → 4×4 확대 → 1픽셀 RGB 값 | [HTML](templates/html/concept.html) · [PNG](previews/html-concept.png) |
| 02 | Process | 입력에서 결과까지 역할과 순서를 설명할 때 | Input → Feature → Task → Output + 마지막 캡션 | [HTML](templates/html/process.html) · [PNG](previews/html-process.png) |
| 03 | Comparison | 동일한 과제에서 두 접근을 같은 기준으로 비교할 때 | 같은 입력·같은 3개 비교 행의 좌우 카드 | [HTML](templates/html/comparison.html) · [PNG](previews/html-comparison.png) |
| 04 | Step-by-Step | 하나의 연산을 초급자에게 풀어 보여줄 때 | 입력/커널/출력 대응 + 원소별 곱/전체 합 | [HTML](templates/html/step-by-step.html) · [JPG](previews/html-step-by-step.jpg) |
| 05 | Interactive | 변수를 조절하며 결과의 변화를 학습할 때 | 실제값별 샘플 그룹 + 혼동행렬/지표 | [HTML](templates/html/interactive.html) · [JPG](previews/html-interactive.jpg) |
| 06 | Architecture | 모델·시스템의 모듈과 데이터 차원을 설명할 때 | 6개 Stage, 반복 Conv Block, Feature Extractor/Classifier 범위 | [HTML](templates/html/architecture.html) · [JPG](previews/html-architecture.jpg) |
| 07 | Experiment | 평가 개수에서 분류 지표를 설명할 때 | Confusion Matrix + 4개 Metrics 카드 | [HTML](templates/html/experiment.html) · [JPG](previews/html-experiment.jpg) |
| 08 | Executive Summary | 수치 근거와 실행 항목을 한 장에 보고할 때 | 세 KPI의 그룹형 세로 막대 + Action 카드 | [HTML](templates/html/executive-summary.html) · [JPG](previews/html-executive-summary.jpg) |

모든 레퍼런스는 HTML Scroll/Slide에 재사용하는 패턴입니다. PPTX가 아니며 8개를 한 자료에 모두 넣어야 하는 것도 아닙니다.

## 01 Concept · 사진에서 RGB 3차원 배열까지

- **학습 목적:** RGB 사진 → 동일한 높이와 너비의 R/G/B 숫자 행렬 3장 → 선택 4×4 영역 → 선택 픽셀의 세 숫자 → H×W×3 배열을 하나의 Figure로 이해. CNN/Kernel/Feature Map/Classification 제외.
- **Figure:** 원본 사과 사진, 실제 채널별 값으로 그린 R/G/B 평면 3개(H/W/C=3 축), 같은 이미지에서 얻은 4×4 확대, 선택 index 6의 RGB/HEX 및 3채널 막대. 평면은 색칠한 가짜 행렬이 아니라 같은 원본의 80×80 리샘플에서 각 채널 강도를 별도 Canvas에 그린 것으로, 깊이 방향 3개 판은 채널 축의 도식입니다.
- **격자 표시:** 각 채널 판 위에 8×8 얇은 안내선을 겹쳐 수치 행렬임을 나타냅니다. 이는 설명용 격자이며 실제 픽셀 데이터는 채널당 80×80로 동일합니다.
- **확대 영역의 채널 깊이:** 동일 ROI `(52,38,4,4)`에서 얻은 `[R,G,B]` 16개를 공유합니다. 전면은 실제 RGB 합성 4×4(순수 R 평면이 아님), 중간 G와 후면 B는 기존 채널 윤곽에 사용하던 초록 `#279467`/파랑 `#427ec5`를 **단일 기준색**으로 사용합니다. CSS `outlineColor`를 JS가 직접 읽어 표시색 `t=0.22+0.78v/255`, `display=Math.round(255+(base−255)×t)`로 보간합니다. 밝은 표시색만 보정하며 실제 0~255 채널값·선택 RGB/HEX·막대는 그대로 둡니다. DOM·시각적 깊이는 B→G→RGB이며 데스크톱 오프셋은 G(+17px,−17px)/B(+34px,−34px), 520px 이하 모바일은 G(+14px,−14px)/B(+28px,−28px)입니다. R/G/B 각 레이어의 우상단 15px 배지(모바일 12px)는 앞 레이어에 가려지지 않도록 전면/중간/후면 높이차를 확보합니다. 전면은 교육용 실제 RGB 합성색이지만 `R` 배지를 대표 표기로 사용합니다. RGB 전면 격자 너비는 데스크톱 130px(31px×4+2px×3), 모바일 122px(29px×4+2px×3)로 축소합니다. 일부 영역 확대의 가로·세로선과 C=3 표기를 삭제합니다. **H=4는 전면 RGB 격자 왼쪽 중앙**, **W=4는 후면 B 채널의 가로 중앙에 맞춘 확대 격자 아래**에 텍스트로만 표시합니다. R/G/B 우상단 배지와 아래 `4×4×3 = 48개 값` 캡션은 유지합니다. 4단계 Figure는 이미지별 시각 중심으로 가운데 배치하되 하단 라벨·설명 위치는 유지합니다. 선택한 1픽셀의 Swatch 및 수치 Figure도 함께 축소합니다. 확대 격자 좌하단의 `RGB` 표기와 확대 Figure의 `C=3`은 표시하지 않습니다. 왼쪽 전체 R/G/B 행렬의 `C=3`는 유지하며, 채널 수 3은 각 픽셀의 RGB 세 성분을 뜻합니다. 선택 index 6 선택은 전면에만 흰색 2px Halo와 Navy 5px 외곽선을 사용합니다. 16개 셀은 숫자 대신 실제 합성색 블록을 유지합니다. `4×4×3=48개 값`은 16픽셀×3성분입니다.
- **수치 계약:** 리샘플 80×80, ROI x=52/y=38/width=4/height=4, 표시 ROI left 65%/top 47.5%/width 5%/height 5%. 선택 index 6 = 로컬 (2,1), 전체 (54,39). Chromium 검산 RGB 223/54/56, HEX #DF3638. 원본 사진과 추출 조건은 변경하지 않았습니다. 4×4 ROI의 원소 수는 4×4×3=48, 전체 이미지가 48값이라는 뜻은 아닙니다. 채널 막대 = value/255×100%.
- **배치·디자인:** 한 개의 White 패널 안에서 입력 사진 → 3개 채널 행렬 → 해당 행렬에서 4×4 ROI 확대 → 선택한 1픽셀의 RGB/HEX/채널 막대까지 화살표 3개로 연결합니다. ROI는 원본 사진에 표시하지 않고 **앞쪽 R 채널 행렬 위에만** 표시합니다(세 채널의 같은 위치를 대표). 행렬 밖 위쪽에 C=3을 배치하고 H=4 가이드·선 간격을 분리합니다. Navy/Blue/Teal, 로컬 Pretendard Variable, −1pt 유지. 모바일에서는 4단계를 세로로 배치하며 실제 계산은 동일합니다.
- **하단의 역할:** 가로 구분선 아래에는 H×W×3 정의를 재반복하지 않고 `같은 위치의 R/G/B를 조합 → 한 픽셀의 RGB 색상`을 보여줍니다. R/G/B 숫자, 합성 Swatch는 선택 index 6의 실제 Canvas 결과를 공유합니다. 산술 합산이 아니라 채널별 성분의 조합입니다. 최종 하단 핵심 개념에만 전체 H×W×3 배열을 남깁니다.
- **소스·검증:** [HTML](templates/html/concept.html) · [사진](templates/html/assets/concept-apple-photo.jpg) · [PNG 프리뷰](previews/html-concept.png) · [상세 명세](docs/REFERENCE_PAGE_SPECS.md#01-concept). [검증 스크립트](scripts/validate_references.py)로 실제 이미지에서 채널별 6400개 픽셀, 확대 RGB/G/B의 각각 16개 셀·채널 성분·위치·index 6·RGB/HEX, B 기준 W·전면 기준 H 텍스트 중심/충분한 여백 및 가이드선 부재·G/B 채널 프레임 색상과 통일한 밝은 표시색 및 원본 수치 분리·선택 Halo/Navy·반응형 6화면·로컬 Pretendard를 검증합니다.

## 02 Process · 입력 이미지에서 클래스별 예측 확률로

- **사용 목적·청중:** CNN 예측을 처음 배우는 학습자. 입력→특징 추출→목적별 처리→출력의 역할을 한 장으로 설명하는 강의·기술 자료에 적합합니다. #6 Architecture의 내부 Conv/ReLU/Pool/Flatten/FC/Softmax 설명과 구분합니다.
- **현재 구조:** 같은 크기의 INPUT / FEATURE / TASK / OUTPUT 카드 4개. Stage Label → 독립 Figure → Title → Description의 행을 맞추고 Blue 화살표 3개로 연결합니다. 마지막 흰색/Teal 캡션은 CNN과 Task Head의 역할을 요약합니다.
- **배경 정책:** 학습 주제인 **FEATURE만 Pale Blue/Blue 경계**로 강조합니다. INPUT/TASK/OUTPUT은 White/일반 Border이며 네 카드 모두 2px 경계·같은 높이입니다. Output의 최대 확률 막대에만 Teal을 강조색으로 씁니다. 이 규칙은 `.process-slide` 안에서만 적용합니다.
- **INPUT:** 기존 사과 사진 한 장, 제목 `입력 이미지`, 설명 `RGB 픽셀 데이터`. #6처럼 추가 프레임·배경·그림자 없이 정사각형으로 표시합니다. 64×64 리샘플 조건은 슬라이드의 별도 각주 대신 상세 명세에 둡니다.
- **FEATURE:** 같은 사진의 휘도·고정 3×3 방향성 필터 16개·ReLU에서 대표 채널 0/3/6/9를 계산합니다. Blue 활성화 맵 4장의 정사각형 평면을 오른쪽 위 방향으로 겹칩니다. #6의 Stack 방향·평면 테두리 스타일을 따르되 설명용 패턴을 복사하지 않습니다. 제목 `CNN`, 설명 `이미지에서 특징 추출` 외에 문장형 각주는 추가하지 않습니다. 계산 조건·한계는 aria-label/코드/명세에 둡니다.
- **TASK:** 짧은 특징 벡터 → 분류 Head → 예시 점수 3개의 기존 그림을 사용합니다. 7개 셀은 차원을 뜻하지 않는 요약 기호이며, 점수 `[2,1,0]`은 Output 예시 확률과 같은 데이터입니다. 내부 화살표는 Teal입니다. 제목 `Task Head`, 설명 `특징을 목적에 맞게 처리`와 White 카드 배경은 유지합니다. Flatten 계산·복잡한 FC 연결·Softmax 수식은 #6과 문서에서 설명합니다. 이번 예시는 분류이며 Task Head의 일반적 역할을 분류에 한정하지 않습니다.
- **OUTPUT:** 사과 66.5% / 토마토 24.5% / 기타 9.0%의 수평 막대. 별도 예시 logits `[2,1,0]`의 Softmax이며 합은 100.0%입니다. 길이는 반올림 전 확률에 비례하고 최대 클래스는 Teal, 나머지는 낮은 채도입니다. White 카드 안에 작은 `예시 확률`을 표시합니다.
- **주의:** 사진→고정 필터 맵은 실제 계산이지만 예시 확률은 그 맵에서 직접 계산된 학습 모델의 추론 결과가 아닙니다. #2에는 전체 역할 흐름만, #6에는 내부 연산·차원만 설명합니다. 모델 정확도나 성능이라고 표현하지 않습니다.
- **정렬·반응형:** 1440×810 원본에서 카드 높이 376px, Figure 슬롯 176px. 실제 Figure 경계의 중심과 Blue 화살표를 맞춥니다. Label/Title/Description은 독립 행입니다. 900px 이하에서는 카드 1열·아래 방향 화살표·같은 단계 순서를 사용합니다.
- **구현·검증:** 공통 `assets/cnn-feature-maps.js`는 그대로 유지하며 #2 표시만 `process-reference.js`에서 처리합니다. `python scripts/check_process.py`는 6개 화면의 독립 계산·색상·정렬·실제 Pretendard/−1pt와 12개 실패/재사용 사례를 검사합니다. 결과는 [전용 JSON](previews/review/process-validation.json), #3 포함 전체 회귀는 [공통 JSON](previews/review/reference-validation.json)에 기록합니다.
- **가이드·프리뷰:** [HTML](templates/html/process.html), [상세 명세](docs/REFERENCE_PAGE_SPECS.md#02-process), [재사용 워크플로](docs/REFERENCE_REUSE_WORKFLOW.md), [main 기준 이전 PNG](previews/review/process-before.png), [최신 PNG](previews/html-process.png).

## 03 Comparison · 같은 문제의 두 접근

- **사용 목적·청중:** 알고리즘·설계·도입 방법을 동일한 조건과 기준으로 비교하는 강의·기술 보고.
- **현재 구조:** 왼쪽 규칙 기반 / 오른쪽 머신러닝. 양쪽에 같은 사과 사진을 놓고 판단 기준·기준 변경·적용 조건을 같은 행에 배치합니다.
- **현재 Figure:** 색상·형태 조건을 직접 지정하는 방식과 사진 기반 대표 특징 맵을 나란히 보여줍니다. 특징 모티프는 #2와 같은 고정 필터 엔진입니다.
- **주의:** 데이터 기반 방법이 무조건 우월하다는 결론을 만들지 않습니다. 대표성·편향·환경 변화에 따른 검증 조건을 유지합니다. 한쪽에만 다른 난이도의 입력을 쓰지 않습니다.
- **가이드:** [상세 명세](docs/REFERENCE_PAGE_SPECS.md#03-comparison), [비교 설계 절차](docs/FIGURE_PRODUCTION_STANDARD.md).

## 04 Step-by-Step · 원소별 곱과 전체 합

- **선택한 구현:** PR #11 최종 버전 기반. 이전 로컬 반응형 가중치 실험은 이 기본 예제를 대체하지 않습니다.
- **사용 목적·청중:** 합성곱·행렬 연산·손실 계산 등 한 계산을 단계별로 이해할 초급자.
- **현재 구조:** 왼쪽에 5×5 입력·3×3 커널·3×3 출력, 오른쪽에 선택된 3×3·같은 커널·9개 원소별 곱·전체 합·출력 위치.
- **수치:** 가중치는 각 행 `[1,0,−1]`, 선택 영역은 1–9. `1+0−3+4+0−6+7+0−9 = −6`. 전체 출력은 `[[-6,9,16],[-2,5,11],[-1,4,8]]`.
- **조건:** stride 1, padding 0, 단일 채널, bias 0, 커널 반전 없음. CNN 라이브러리의 cross-correlation 관례입니다.
- **주의:** 입력 좌상단 3×3과 출력 좌상단 셀의 대응, 곱 9개, 합과 커널 이동 설명, 좌우 카드 하단 구분선 정렬을 삭제하지 않습니다. 원소별 곱 기호는 SVG로 표시해 글꼴 폴백을 막습니다.
- **가이드:** [상세 명세와 전체 행렬](docs/REFERENCE_PAGE_SPECS.md#04-step-by-step).

## 05 Interactive · 조작과 판정의 연결

- **선택한 구현:** 로컬 최종 승인본 `ae26ba0` 기반. 실제 이상 그룹이 위, 실제 정상 그룹이 아래입니다.
- **사용 목적·청중:** threshold·파라미터 조절이 개별 판정과 전체 지표에 미치는 영향을 직접 보는 실습.
- **현재 구조:** 왼쪽 임계값·점수·예측 배지·유형·예측 개수, 오른쪽 TP FP / FN TN 행렬과 Precision·Recall의 뜻/일반식/대입식.
- **데이터:** 6개 점수 0.15/0.32/0.48/0.67/0.82/0.94, 실제값 정상/이상/정상/이상/이상/정상. `score ≥ threshold`가 양성(이상)입니다.
- **기본값:** 0.60 → TP=2, FP=1, FN=1, TN=2, 두 지표 66.7%. 분모가 0이면 `정의 불가`입니다.
- **주의:** 그룹·점수·샘플 위치는 고정합니다. 판정이 바뀐 배지만 강조하고 집계·수식을 함께 갱신합니다. 판정 규칙과 점선 범례를 분리하고 예측 개수까지 카드 패딩 안에 담습니다. 마지막 Teal 캡션은 임계값의 뜻과 영향을 설명합니다.
- **공유본:** [폰트 내장 단일 HTML](previews/review/interactive-live.html).
- **가이드:** [상세 패턴](docs/INTERACTIVE_PATTERN.md), [페이지 명세](docs/REFERENCE_PAGE_SPECS.md#05-interactive).

## 06 Architecture · 차원과 모듈의 관계

- **선택한 구현:** PR #10 최종 CNN. PR #9의 이전 Architecture로 되돌리지 않습니다.
- **사용 목적·청중:** 모델 구조·모듈 경계·차원 변화를 읽는 학습자와 기술 검토자.
- **최종 흐름:** **Input → Conv Block 1 → Conv Block 2 → Flatten → FC Layer → Softmax**.
- **정확한 차원:** `64×64×3 → 32×32×16 → 16×16×32 → 8,192 → 3 logits → 3 probabilities`.
- **각 Block:** Conv 3×3 S1 P1 → ReLU → MaxPool 2×2 S2. Conv가 공간 크기를 유지하고 이 예제의 Pool이 절반으로 줄입니다. 첫 Conv 후 64×64×16, 두 번째 Conv 후 32×32×32입니다.
- **Figure:** 사진 한 장, 대표 Feature Map Stack, 세로 1D Flatten 벡터와 생략점, 3개 logit 노드, 클래스별 확률 막대. 설명용 logits `[2,1,0]` → 약 66.5/24.5/9.0%.
- **주의:** 그림 속 평면 개수는 실제 채널 수와 다릅니다. 맵 패턴과 logits는 설명용이며 사진의 학습 모델 추론이 아닙니다. 외부 Blue / 내부 Teal 화살표, 실제 bounding box 중앙축을 유지합니다.
- **가이드:** [Figure 제작 표준](docs/FIGURE_PRODUCTION_STANDARD.md), [상세 명세](docs/REFERENCE_PAGE_SPECS.md#06-architecture).

## 07 Experiment · 개수에서 지표로

- **선택한 구현:** 로컬 사용자 승인본 `3ad7079` 기반.
- **사용 목적·청중:** 분류 평가의 오탐·미탐과 Accuracy/Precision/Recall/F1을 이해할 학습자.
- **행렬 방향:** GT 실제 이상/정상 열, 모델 예측 이상/정상 행. **TP=4 FP=1 / FN=2 TN=5**입니다.
- **12개 평가 샘플:** 실제 이상 6·정상 6, 양성 클래스는 이상입니다.
- **계산:** Accuracy=9/12=75.0%, Precision=4/5=80.0%, Recall=4/6=66.7%, F1=8/11=72.7%. F1 조화평균식도 함께 표시합니다.
- **주의:** 축·행 순서·셀 위치를 임의로 바꾸지 않습니다. FP/FN 짧은 해설을 카드 안에 유지합니다. 모델 예측 옆 세로선과 GT 아래 가로선, 숫자/라벨 중앙 정렬을 실측합니다.
- **가이드:** [상세 패턴](docs/EXPERIMENT_PATTERN.md), [페이지 명세](docs/REFERENCE_PAGE_SPECS.md#07-experiment).

## 08 Executive Summary · 근거와 실행 항목

- **선택한 구현:** 기존 main의 정상 레이아웃을 유지합니다. 사전 검토의 새 디자인 제안은 승인된 수정으로 간주하지 않습니다.
- **사용 목적·청중:** 운영 지표의 변화와 후속 확인 사항을 한 장으로 읽는 기술·경영 보고.
- **현재 구조:** 왼쪽 세 KPI 각각의 기존/개선안 세로 막대·원래 수치와 단위·감소율, 오른쪽 우선순위/동일 조건 집계/확대 판단.
- **계산:** 월간 수동 점검 120→80건 −33.3%, 평균 처리 시간 45→30분/건 −33.3%, 월말 미처리 20→8건 −60.0%.
- **축:** 지표별 기존값=100%, 개선안 높이는 66.67/66.67/40%. 서로 다른 단위의 원래 수치를 같은 절대 축에서 비교하지 않습니다.
- **주의:** 수치는 예시이며 실측 성과나 도입 안전성의 근거로 사용하지 않습니다. 실제 보고로 재사용할 때 집계 기간·측정 조건·출처·판단 기준을 확보해야 합니다. 제공되지 않은 미검출 허용 기준을 만들지 않습니다.
- **가이드:** [상세 명세](docs/REFERENCE_PAGE_SPECS.md#08-executive-summary), [재사용 워크플로](docs/REFERENCE_REUSE_WORKFLOW.md).

## 공통 확인

모든 페이지는 실제 Pretendard, 전체 −1pt, 편집 가능한 소스, 실제 계산과 도식의 일치를 요구합니다. 프리뷰는 [공통 검증](previews/review/reference-validation.json)과 같은 원본이어야 합니다. 다른 데이터로 재사용한 경우 숫자만 바꾸지 말고 공식·Shape·색상 의미·설명 조건·반응형을 함께 확인합니다.
