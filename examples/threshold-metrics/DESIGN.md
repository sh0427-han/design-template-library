# 분류 임계값과 성능 변화 — D0 설계

2026-10-27 · Planner `/root/threshold_planner`의 독립 분석·설계 결정을 조정자 `/root`가 문서화했다. Builder와 Reviewer는 별도 Agent다. 이 문서는 구현 전 D0 원본이며 이후 차이는 끝에 개정 절로 추적한다.

## 기준과 범위

- Repository `sh0427-han/design-template-library`, 기준 main `ef9783e910f07a5e2c9343da17573e1a7cf30225`, 작업 브랜치 `feat/threshold-metrics-template-validation`.
- [원격 확인 기록](review/baseline.json): 3차 PR #22 병합 완료, 해당 main push CI 40451004448 성공. 이번 라운드는 PR까지만 진행하며 main 병합 금지.
- 청중: Vision AI·머신러닝 입문자. 불량을 Positive(양성), 정상을 Negative(음성)로 정의한다. 합성 결함 점수이며 보정 확률이나 실측 모델 성능이 아니다.
- 산출물은 개념 1장과 실습 1장, Scroll/Slide HTML 두 보기다. 추가 장·별도 변환 출력·모델 학습은 없다.
- 설계 원본은 기준 커밋의 공통 Markdown과 원본 8종뿐이다. 이전 세 예제의 전용 HTML/CSS/JS/DESIGN은 설계·복제 원본으로 사용하지 않는다. 회귀 검사만 수행한다.

## 목표와 정확한 용어

1. 실제값은 검사로 확인한 정답이다. 모델 점수와 임계값으로 만든 최종 예측과 구별한다.
2. 같은 모델·같은 점수에서도 임계값을 바꾸면 예측이 바뀔 수 있다. 실제값·점수·식별자·샘플 위치는 고정된다.
3. 점수 ≥ 임계값이면 불량으로 예측한다. 정확히 같은 점수도 양성이다.
4. 오탐 FP(False Positive)는 실제 정상→예측 불량, 미탐 FN(False Negative)은 실제 불량→예측 정상이다. TP(True Positive)는 실제 불량→예측 불량, TN(True Negative)은 실제 정상→예측 정상이다.
5. Precision(정밀도)은 불량 예측 중 실제 불량, Recall(재현율)은 실제 불량 중 찾은 비율, Accuracy(정확도)는 전체 중 맞힌 비율, F1-score는 정밀도·재현율을 함께 요약하는 조화평균이다.
6. 고정 점수에서 임계값을 올리면 양성 예측·TP·FP는 같거나 감소하고 FN은 같거나 증가한다. Precision이나 Accuracy가 항상 좋아진다고 설명하지 않는다. 오탐·미탐 비용으로 최적 임계값을 결정하는 실험은 범위 밖이다.

## 공통 규칙과 원본 출처

| 결정 | 공통 Markdown 파일·절 | 확인할 원본 구현 | 분류 |
| --- | --- | --- | --- |
| 개념 먼저, 계산·실습 다음 | [디자인 시스템](../../DESIGN_SYSTEM.md) §개념 설명의 기본 순서·용어와 약어의 첫 등장 | 원본 8종의 목적·카탈로그 | A |
| 1440×810, 49px 제목, 21px 부제, Footer15px | 디자인 시스템 §16:9 프레임과 Typography·Header / Content / Footer, [규격표](../../docs/DESIGN_COMPONENT_RECIPES.md) §2–3 | `templates/html/styles.css`, `reference-types.css`, `reference-layout.css` | A |
| 카드 White·17px radius·24px 기본 padding | 디자인 시스템 §카드와 내부 정렬, 규격표 §2 | `interactive.html` `.live-card`, `experiment.html` `.experiment-card` | A |
| 자체 Blue 분류 / Navy 핵심 제목 | 디자인 시스템 §제목과 분류 라벨의 역할, 규격표 §제목/라벨 검사의 적용 단위 | #5 `.ref-k`+h2, #7 `.ref-k`+h2 | A |
| 고정 실제값 그룹·단일 상태 갱신·분모0 | [Interactive 규약](../../docs/INTERACTIVE_PATTERN.md) §승인된 내용과 재사용 계약·데이터와 판정 계약·지표·조작 | `interactive-reference.js`와 `interactive.html` | A |
| TP FP / FN TN, GT열·예측행, 중앙축·구분선 | [Experiment 규약](../../docs/EXPERIMENT_PATTERN.md) §3·6 | `experiment.html` 실제 table/Range 구분선 | A |
| 뜻→일반식→현재 대입·네 지표 | Experiment 규약 §4–5, 규격표 §지표와 수식 | #7 `.metric`·`.metric-calculation` | A |
| Pretendard / STIX Math / 전역−1pt | 디자인 시스템 §Pretendard와 전역 자간·본문과 수식의 서체 분리 | 공통 `math-typography.css`와 로컬 WOFF2 | A |
| Figure·연결·실제경계 | [Figure 표준](../../docs/FIGURE_PRODUCTION_STANDARD.md) §2·3·6·7·10·13 | #5 임계값 표시, #7 표의 실제 글자 경계 | A |
| 두 보기의 같은 원본·상태·키보드 | [두 보기 설계](../../templates/dual-mode-learning/DESIGN.md), [모드 계약](../../templates/dual-mode-learning/MODES.md) | 원본 보기의 URL·공통 프레임 원칙 | A |
| D0/D1·독립 검토·원인 구분 | [재사용 절차](../../docs/REFERENCE_REUSE_WORKFLOW.md), [검토 가이드](../../docs/REFERENCE_REVIEW_GUIDE.md), [재사용 검증](../../docs/TEMPLATE_REUSE_VALIDATION.md), [실행 프롬프트](../../docs/CONCEPT_REUSE_PROMPT.md) | 기존 검증기는 회귀 용도만 사용 | A |

AGENTS.md, TEMPLATE_CATALOG.md, docs/REFERENCE_PAGE_SPECS.md의 전체 8종 목적·규격도 검토한다. #1 표현 확대, #2 처리 흐름, #3 비교, #4 연산, #6 모델 구조, #8 실행 요약은 이번 주제의 주 패턴으로 선택하지 않는다. #5는 조작→판정→집계의 상태 계약 때문에, #7은 같은 행렬→네 지표의 해석·계산·축 계약 때문에 선택한다. 원본의 6개/12개 데이터와 배치 자체를 복사하지 않는다.

## 두 장의 읽는 순서와 Figure

### 1 — 임계값의 의미 (`#concept`)

제목은 임계값과 판정의 관계를 직접 예고한다. 부제는 같은 점수에서도 기준을 바꾸면 예측이 달라진다는 부연 설명이다.

큰 White 설명 단위 하나에 자체 분류 라벨·Navy 제목을 둔다. 검사 이미지→모델 결함 점수→임계값 비교→불량/정상 예측을 편집 가능한 SVG/HTML로 보여준다. 점수의 0~1 범위와 ≥ / < 일반 관계만 사용하고 예제 샘플의 숫자 대입이나 지표 계산은 넣지 않는다. 실제값은 검사로 확인하는 별도 고정 정보로 표시하여 예측 출력과 연결 의미를 구별한다. 아래에는 FP/FN의 실제·예측 조합을 짧게 풀이한다. 마지막 핵심 캡션은 기준을 바꾸어도 점수와 실제값은 바뀌지 않는다는 내용이다.

### 2 — 임계값을 변경하는 실습 (`#practice`)

가로 전체 White 패널 하나 안에 공유 조작부→샘플과 행렬→네 지표를 놓는다. 원본 #5의 6행 점수 목록과 #7의 2×2 지표 카드 배치를 복제하지 않는다.

- 상단: 자체 Blue 분류·Navy 제목과 데이터셋 선택, 임계값 숫자·native slider. 판정 규칙과 Amber 점선 범례는 별도 요소다.
- 위쪽 행: 왼쪽 약740px에 실제 불량 그룹을 위, 실제 정상 그룹을 아래에 고정한 식별 타일. 샘플 ID·점수·예측·유형을 문자로 제공한다. 타일 위치/점수 막대 길이는 임계값으로 바꾸지 않는다. 오른쪽 약480px에는 의미 있는 HTML table로 혼동행렬과 FP/FN 풀이를 둔다.
- 아래쪽 행: Precision, Recall, Accuracy, F1-score를 같은 폭의 네 열로 배치한다. 이름과 현재 수치→짧은 뜻→MathML 일반 분수→현재 정수 대입값과 백분율 순서다. 관련 설명을 다른 카드에서 찾게 하지 않는다.
- 내부 구역은 불필요한 큰 카드로 중첩하지 않는다. 지표 구분선/작은 그룹은 필요한 역할만 사용한다.

### 정보 위계와 높이 예산

1440×810 설계, 공통 크기·색·행간 토큰을 그대로 상속하고 전체 캔버스만 동일 배율로 축소한다. PC4개 크기×2모드×2장=16화면이다. Scroll도 장별 source 크기·서식을 바꾸지 않는다. 보기 UI는 원본 바깥에 둔다.

실습의 시작 예산(C): 페이지 padding top40/좌우66/bottom28, 헤더117.35, content gap20, Footer45로 본문559.65px를 확보한다. 패널554 = padding20×2 + control60 + 위행226 + 지표행202 + gap12×2 + border2. 패널의 라벨·제목은 control 영역에 포함하고 별도 높이를 가산하지 않는다. 개념 장도 같은 페이지 프레임을 사용하되 내용의 분포에 맞게 본문 여백을 둔다. 글자/그림을 겹치게 하거나 잘못된 높이를 overflow로 숨기지 않는다. 실제 렌더링에서 조정한 값은 개정 절로 기록한다.

기본 제목49px·부제21px·패널 제목25px·분류16px·일반 본문19px, 조밀한 타일/기술 라벨16–18px를 출발점으로 한다. 같은 역할은 같은 크기·정렬을 쓴다. label/title/description은 독립 행을 기본으로 한다. 바탕/예측 정상은 Muted, 예측 불량은 Blue, 정분류 TP/TN은 Teal, 오분류 FP/FN은 Amber다. Positive를 좋은 결과의 의미로 색칠하지 않는다. 카드 자체 설명 단위는 `#concept .teaching-panel`, `#practice .teaching-panel` 각1개이며 직접 소유 `.panel-label`+`.panel-title` 각1개를 검사한다. 내부 구역/지표는 하위 제목이며 또 다른 큰 카드 소유 쌍으로 중복 집계하지 않는다.

## 데이터 계약 — 이번 예제 고유 값 C

`data.json`은 `{version:1,datasets:{default:{label,samples},shifted:{label,samples}}}`다. 각 샘플은 `{id,scoreUnits,truth}`. ID는 비어 있지 않고 유일하며 `scoreUnits`는 0~100 정수, `truth`는 숫자0/1이다. 점수는 `scoreUnits/100`; 정수 비교로 경계 오차를 피한다. 각 데이터셋 안의 모든 점수는 서로 다르다. 두 데이터셋 사이에는 같은 점수가 있을 수 있다.

기본값 `threshold=50`, 기본 데이터14개:

| 실제 불량 ID | 점수 단위 | 실제 정상 ID | 점수 단위 |
| --- | ---: | --- | ---: |
| D01 | 18 | N01 | 6 |
| D02 | 41 | N02 | 12 |
| D03 | 50 | N03 | 25 |
| D04 | 64 | N04 | 33 |
| D05 | 79 | N05 | 57 |
| D06 | 86 | N06 | 72 |
| D07 | 97 | N07 | 92 |

기준0.50: TP5 FP3 FN2 TN4, Precision5/8=62.5%, Recall5/7=71.4%, Accuracy9/14=64.3%, F1=10/15=66.7%. D03의 같은 점수0.50은 Positive다.

두 번째 데이터셋도14개이며 불량4·정상10으로 비율을 바꾼다. ID S01..S14의 점수 단위는 순서대로4,11,16,23,29,37,46,50,58,66,74,81,89,96이며 S03/S08/S11/S14만 실제 불량이다. 임계값0.50에서 TP3 FP4 FN1 TN6, Precision42.9%, Recall75.0%, Accuracy64.3%, F1=54.5%다. 별도 테스트 데이터에는 실제 양성0·실제 음성0·빈 데이터·점수0/100·중복ID·범위 밖 점수 등도 포함한다. 이 데이터 값과 타일 수는 공통 MD에 추가하지 않는다.

## 계산과 표시 계약

`predicted_positive = scoreUnits >= thresholdUnits`. 실제 불량+예측불량 TP, 실제정상+예측불량 FP, 실제불량+예측정상 FN, 실제정상+예측정상 TN. 혼동행렬은 열=GT 실제 불량/정상, 행=모델 예측 불량/정상, 순서 TP FP / FN TN이다. 합계와 실제·예측 개수는 같은 samples에서 유도한다.

- Precision = TP/(TP+FP)
- Recall = TP/(TP+FN)
- Accuracy = (TP+TN)/N
- F1 = 2TP/(2TP+FP+FN)

모든 계산은 정수 개수와 반올림 전 비율을 사용한다. 백분율만 소수1자리로 표시하며 반올림한 P/R에서 F1을 계산하지 않는다. 일반식·현재 대입식은 MathML/STIX를 사용한다. 지표 이름·설명은 Pretendard다. F1의 조화평균식 `2PR/(P+R)`은 P와R이 정의되고 P+R>0일 때의 동치임을 밝힌다. 개수식으로 정의되는0과 분모0으로 정의되지 않는 상태를 구별한다.

분모0이면 `—` 또는 `정의되지 않음`, 관련 분모 조건을 같은 지표에 표시한다. NaN/Infinity/가짜0%는 없다. 빈 데이터에서는 모든 지표를 정의 불가로 표시한다. 부정한 데이터는 정상 계산으로 처리하지 않는다.

## 상태·인터랙션·DOM 계약

단일 상태는 version/dataset/thresholdUnits/samples/status/error와 한 번 계산한 predictions/counts/metrics를 가진다. 슬라이더 input 한 번에 숫자·예측·유형·집계·행렬·네 지표·대입·강조·상태 알림을 같은 동기 렌더 경로에서 갱신한다. 기존 타일 DOM은 임계값 변경 때 유지하고 바뀐 예측만 짧게 강조한다. reduced-motion이면 강조 애니메이션을 생략한다.

URL은 `?v=1&dataset=default&threshold=50#concept` 또는 `#practice`; threshold는 정수0..100의 단위다. 유효한 URL이 기본 초기화보다 우선한다. 조작·현재 장은 URL과 반대 모드 링크에 반영하고 전환/새로고침/공유로 복원한다. 잘못된 version/dataset/threshold/hash는 안전한 기본값으로 정규화하고 짧게 안내한다. 로컬 저장소의 오래된 상태가 URL을 덮지 않는다. Scroll은 현재 읽는 장과 hash를 맞추며 마지막 장 경계도 검사한다. Slide는 버튼과 비편집 요소에서의 탐색키를 지원하되 range/select/button/link의 키를 가로채지 않는다.

테스트/독립 검증 API `window.ThresholdMetrics`:

- `ready`: 데이터·콘텐츠·폰트 준비 Promise. 실패도 처리된 오류 상태로 관측할 수 있다.
- `getState()`: 외부 변경이 내부 상태를 바꾸지 않는 깊은 복사. `thresholdUnits`는 정수, `threshold`는0..1, `counts`는 소문자 tp/fp/tn/fn, `metrics`는 null가능 비율이며 `fractions`는 지표별 numerator/denominator를 제공한다.
- `setThreshold(integer)`, `setDataset('default'|'shifted')`: 같은 제품 입력 경로를 사용.
- `loadSamples(array)`: 테스트 전용 원자적 검증·교체. 유효하지 않으면 화면에 과거 성공 집계/지표를 남기지 않는다. 사용자 화면에는 개발용 조작을 노출하지 않는다. 교체한 테스트 배열의 공유/새로고침 복원은 제품 기능으로 주장하지 않는다.

DOM: 장 루트 `#concept.slide`, `#practice.slide` 및 `.page-frame`; `.sample-tile[data-sample][data-truth][data-score-units][data-prediction][data-type]`; `#threshold`, `#threshold-value`; `#cm-tp/#cm-fp/#cm-fn/#cm-tn`; `[data-metric=precision|recall|accuracy|f1] .metric-value/.metric-calculation`. 추가 선택자는 Builder/검산 담당이 합의하되 명세 차이를 기록한다.

native range의 label·aria-valuetext, select 이름, focus-visible, 전용 role=status, 색 외의 예측/오류 유형 문자를 제공한다. table은 caption/th scope/headers를 사용한다. 전체 카드 aria-live는 쓰지 않는다. fetch/JS 실패 시 정상처럼 보이는 기존 결과 대신 안내와 재시도 경로를 제공하고, no-JS에도 안내한다. 폰트 폴백은 별도 실패 시나리오이며 정상 폰트 검증 성공으로 간주하지 않는다.

## 검증과 재사용성 판정 계획

화면 검증은 1600×950·1440×810·1366×768·1280×720 × Scroll/Slide × 두 장의16개로 기록한다. 별도로 데이터·상태 시나리오 수를 기록하고 화면 개수에 합산하지 않는다. 실제 CDP 글리프·Pretendard/STIX·전역−1pt, 실제 DOM/SVG/MathML 경계, 카드 안쪽 padding, 행렬 중앙축·구분선, 텍스트 줄바꿈·겹침·Footer, 콘솔·파일 실패를 확인한다.

독립 Python 검산기는 JS 계산 함수를 기대값으로 부르지 않고 JSON의 실제값·정수 점수에서 진리표와 Fraction으로 기대값을 만든다. 0..100 전 임계값에서 두 데이터셋의 샘플별 예측/유형·개수·표·백분율·대입을 검사한다. 같은 점수/바로±1, 모든/0양성예측, 실제0양성/0음성, 빈/잘못된 데이터, 모드전환·새로고침, 키보드/포인터·motion감소·폰트실패·로드실패도 분리한다. 고정 데이터에서 양성예측·TP 단조감소를 검사하되 Precision 증가를 가정하지 않는다.

원본8종과 이전3개 예제의 source는 기준 커밋과 byte 보존 검사하고 기존 검증기를 실제 실행한다. Builder 자체 검사 뒤 별도 Reviewer가 소스/명세/독립 검산/실제 이미지와 보고서를 검토한다. 수정·재검토는 최대3회, 미해결은 임의 통과시키지 않는다.

#5는 조작→개별예측→동일 상태 집계·지표, 실제값 고정, 경계·실패·상태복원에 대한 재사용성으로 평가한다. #7은 같은 혼동행렬에서 네 지표 유도, 의미/수식/대입 대응, 정의 불가와 축/정렬 재현으로 별도 평가한다. 원본 회귀를 나머지 패턴의 새 주제 재사용 성공으로 확대하지 않는다. 독립 제작자의 무맥락 재현, 실제 학습/생산성능, 모바일·태블릿, 실제 스크린리더 청취는 미검증이다.

## D0 사전 판단

현재 공통 문서 누락0·명시적 모순0·코드에만 있는 필수 규칙0으로 잠정 판단한다. 필요한 핵심 계약은 위 출처에 있다. 합성 데이터/14타일/두 장 분배/정수URL/API/554px높이 예산은 C 고유 설계다. 구현·검토 후 실제 결함을 찾으면 당시 시점과 근거를 [VALIDATION](VALIDATION.md)에 추가하며 이 D0 판단을 소급 고치지 않는다. 구현/실제 화면 검증/독립 최종 승인은 아직 수행 전이다.

## Builder 개정 명세 — D0 이후, 첫 Chromium 실행 전

D0 별도 커밋은 `91cc46f1175efaa2a9d10a3929e3e842ee079ce7`이다. 위 원문은 그대로 보존한다. Builder는 그 계획을 기준으로 다음 C 재구성을 적용했다. 이후 실제 이미지·자동 검증에서 최종값을 확인하며 미검증 상태를 통과로 표현하지 않는다.

- 개념 흐름은200px, 부품 SVG는128×96px로 조정했다. 실제값 고정 설명과 FP/FN은 하단의 같은 가로 구역에 배치하여 세로 중복을 줄였다. 일반 관계와 본문 폰트 크기를 유지한다.
- 실습 예측 개수 요약은 두 번째 데이터셋의 타일3행 높이를 확보하려고 공유 조작부의 판정 규칙 옆에 놓는다. 실제값 그룹 위아래 순서·ID·점수·타일 유지 계약은 같다.
- F1 동치식은 작은 P/R 별칭 대신 전체 Precision/Recall을 MathML 정자체로 표시하고 조건문은16px로 키웠다. 정의 불가 상태에서는 해당 분모 조건을 명시한다. 정상/정의 불가에 따라 중복 설명 노출을 조절해 의미를 유지한다.
- 두 모드 모두 `min(1440, viewportWidth−40, (viewportHeight−112)×16/9)`의 프레임 폭으로 전체 배율을 정한다. Scroll의 연속 배치와 Slide 탐색만 다르고 원본 내부 서식·계산은 같다.
- 데이터 실패와 폰트 실패는 분리한다. 데이터 실패는 과거 성공 판정·지표를 지우고 조작을 막는다. 의도적 폰트 실패 시에는 폴백 안내와 계산을 유지하되 정상 폰트 검증 성공으로 세지 않는다. 콘텐츠/스크립트 로드 실패와 no-JS에도 안내·재시도 경로를 둔다.
- 테스트 전용 `loadSamples`는 최대16개,15~16개는8타일 열을 사용한다. 기본 두14개 데이터셋은7열이다. 이 확장값도 예제 전용이다.

이 조정은 공통 Markdown의 새 누락으로 세지 않는다. 소형 기술 라벨은 역할에 따라14–18px를 쓰며 원본 규격의 예외 범위와 실제 PC 가독성을 함께 검토한다. 실제 스크린리더 청취나 초보자 이해도 실험으로 확대 해석하지 않는다.
