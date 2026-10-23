# Template Catalog · 8 HTML Reference Patterns

이 카탈로그는 **내용에 맞는 시각 패턴을 선택하는 지도**입니다. 정확한 데이터·수식·기하 조건은 [REFERENCE_PAGE_SPECS.md](docs/REFERENCE_PAGE_SPECS.md), 공통 토큰은 [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)를 따릅니다. 아래 설명은 현재 checkout의 HTML 원본을 기준으로 합니다. 초기 8종 통합의 출처·GitHub 이력은 [통합 보고서](docs/INTEGRATION_REPORT_2026-10-22.md)에 보존합니다.

| 번호 | 이름 | 선택할 때 | 실제 레이아웃 | 원본 · 최신 대표 프리뷰 |
| --- | --- | --- | --- | --- |
| 01 | Concept | 추상 개념을 구체적 사례와 숫자로 풀 때 | 사진/픽셀 카드 + RGB/Shape 카드 + 마지막 캡션 | [HTML](templates/html/concept.html) · [PNG](previews/html-concept.png) |
| 02 | Process | 입력에서 결과까지 역할과 순서를 설명할 때 | Input → Feature → Task → Output + 마지막 캡션 | [HTML](templates/html/process.html) · [PNG](previews/html-process.png) |
| 03 | Comparison | 판단 기준의 준비 방법과 예측 과정을 비교할 때 | 준비/예측 도식 + 같은 입력·3개 비교 행의 좌우 White 카드 | [HTML](templates/html/comparison.html) · [PNG](previews/html-comparison.png) |
| 04 | Step-by-Step | 하나의 연산을 초급자에게 풀어 보여줄 때 | 입력/커널/출력 대응 + 원소별 곱/전체 합 | [HTML](templates/html/step-by-step.html) · [JPG](previews/html-step-by-step.jpg) |
| 05 | Interactive | 변수를 조절하며 결과의 변화를 학습할 때 | 실제값별 샘플 그룹 + 혼동행렬/지표 | [HTML](templates/html/interactive.html) · [JPG](previews/html-interactive.jpg) |
| 06 | Architecture | 모델·시스템의 모듈과 데이터 차원을 설명할 때 | 6개 Stage, 반복 Conv Block, Feature Extractor/Classifier 범위 | [HTML](templates/html/architecture.html) · [JPG](previews/html-architecture.jpg) |
| 07 | Experiment | 평가 개수에서 분류 지표를 설명할 때 | Confusion Matrix + 4개 Metrics 카드 | [HTML](templates/html/experiment.html) · [JPG](previews/html-experiment.jpg) |
| 08 | Executive Summary | 수치 근거와 실행 항목을 한 장에 보고할 때 | 세 KPI의 그룹형 세로 막대 + Action 카드 | [HTML](templates/html/executive-summary.html) · [JPG](previews/html-executive-summary.jpg) |

모든 레퍼런스는 HTML Scroll/Slide에 재사용하는 패턴입니다. PPTX가 아니며 8개를 한 자료에 모두 넣어야 하는 것도 아닙니다.

## 01 Concept · 구체적 사례에서 숫자 구조로

- **사용 목적·청중:** 이미지·데이터 구조를 처음 접하는 학습자, 변수나 센서 값을 소개하는 기술 설명.
- **핵심 Figure:** 저장소의 사과 사진 한 장 → 선택한 4×4 픽셀 확대 → 선택 셀의 RGB/HEX → `H×W×3`.
- **현재 예제:** 80×80 리샘플 Canvas의 `(52,38)`부터 4×4를 읽고 0-based index 6의 실제 픽셀을 모든 표시값에 연결합니다. 기준 Chromium에서는 RGB `(223,54,56)`, HEX `#DF3638`입니다.
- **주의:** 새 사진을 쓰면 픽셀·색상·채널 막대·HEX를 실제 래스터에서 다시 계산합니다. 예전 숫자나 장식 색상을 남기지 않습니다. 사진 자체에 불필요한 추가 프레임·그림자를 붙이지 않습니다.
- **가이드:** [상세 명세](docs/REFERENCE_PAGE_SPECS.md#01-concept), [Figure 제작](docs/FIGURE_PRODUCTION_STANDARD.md).

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

## 03 Comparison · 판단 기준의 준비와 새 이미지 예측

- **사용 목적·청중:** 규칙 기반과 지도학습 이미지 분류를 처음 비교하는 학습자. 기준을 만드는 방법과 이미지를 처리하는 방법을 분리해 설명하는 강의·기술 자료에 적합합니다.
- **현재 구조:** 같은 크기의 White 카드 2개에 Label/Title/소개 → 01 준비 → 02 예측 → 판단 기준/기준 변경/적용 조건 → 장점/한계를 같은 높이로 배치합니다. 큰 중첩 카드는 추가하지 않습니다.
- **RULE-BASED:** 사람이 붉은색 영역·둥근 윤곽 조건을 설정하고 AND로 조합해 판단 규칙을 만드는 도식입니다. 준비된 규칙을 Teal 연결선으로 조건 검사에 연결하고, 사과 사진 → 조건 검사 → `사과 판정 / 예시`를 보여줍니다. 조건·임계값을 실제 측정하거나 규칙 엔진을 실행한 결과가 아닙니다.
- **MACHINE LEARNING:** 서로 다른 붉은 사과/초록 사과/토마토 **일러스트 3개와 정답 라벨** → 학습 → 파라미터가 최적화된 모델의 모식도입니다. 이후 같은 사과 사진 → 학습된 CNN의 상징 → `사과 예측 / 예시`를 보여줍니다. 이번 예제는 지도학습이며 모든 머신러닝에 라벨이 필수라고 일반화하지 않습니다.
- **CNN 표현의 제한:** 대표 맵 0/3/6/9는 #2와 같은 사진·고정 방향성 필터·ReLU의 실제 계산입니다. #2/#6과 같은 오른쪽 위 Stack 방향·Blue 경계로 표시하지만 학습된 CNN의 실측 활성화가 아닙니다. 화면에 `맵: 고정 필터 설명용`, 접근성 설명과 명세에 전체 조건을 기록합니다. 모델 학습·추론·성능 비교를 실행했다고 주장하지 않습니다.
- **대칭·색상:** 입력 사진 파일·크기·기준선, 준비/예측 라벨과 구분선, 표의 세 행, 장점/한계 위치를 맞춥니다. 카드 상단의 방법 Label·제목·소개 사이는 각각 공통 8px, 소개→준비는 구역 간격 16px입니다. 데스크톱에서는 캔버스 위 패딩과 카드 위 여백을 재배분해 Figure 크기와 푸터 위치를 유지합니다. [공통 행간·간격 기준](DESIGN_SYSTEM.md#행간과-요소-사이-간격)을 따릅니다. Amber는 사람의 조건, Blue는 흐름·학습·CNN, Teal은 준비된 체계의 적용 연결과 예시 결과입니다. 두 카드 전체는 모두 White입니다.
- **반응형·검증:** 900px 이하 카드 1열, 650px 이하 Figure·표를 읽기 배치로 조정합니다. `python scripts/check_comparison.py`가 6개 화면의 실제 Pretendard/−1pt·독립 맵 계산·대칭·화살표·실시간 리사이즈를 검사합니다. [전용 검증 JSON](previews/review/comparison-validation.json), [공통 회귀 JSON](previews/review/reference-validation.json)을 확인합니다.
- **구현·가이드·프리뷰:** [HTML](templates/html/comparison.html), [전용 CSS](templates/html/comparison-reference.css), [전용 JS](templates/html/comparison-reference.js), [상세 명세](docs/REFERENCE_PAGE_SPECS.md#03-comparison), [Figure 표준](docs/FIGURE_PRODUCTION_STANDARD.md), [수정 전 PNG](previews/review/comparison-before.png), [최신 PNG](previews/html-comparison.png).

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

새 제작 대상은 PC 웹페이지이며 PC 4개 크기의 검토를 기준으로 합니다. 아래 링크의 예제별 작은 화면 동작·6개 크기 검증은 기존 구현 기록입니다.

모든 페이지는 실제 Pretendard, 전체 −1pt, 편집 가능한 소스, 실제 계산과 도식의 일치를 요구합니다. 프리뷰는 [공통 검증](previews/review/reference-validation.json)과 같은 원본이어야 합니다. 다른 데이터로 재사용한 경우 숫자만 바꾸지 말고 공식·Shape·색상 의미·설명 조건·반응형을 함께 확인합니다.

[컴포넌트 설계 규격](docs/DESIGN_COMPONENT_RECIPES.md)은 #2–#8의 카드·간격·행간·도식 높이·수식·상태·반응형 수치를 대조하고 새 개념의 설계 기록표를 제공합니다. 공통값과 예제별 예외를 구분해 적용합니다.
