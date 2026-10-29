# CNN 필터 선택과 출력 변화 — D0 설계

2026-10-28 (한국 시간). Planner `/root/kernel_planner`가 원본 레퍼런스와 기준 문서를 분석해 구현 전에 작성했다. Builder와 Reviewer는 별도 Agent다. 이 문서와 초기 VALIDATION.md를 D0 별도 커밋으로 보존한 뒤 구현한다. 이후 조정은 끝의 개정 절에 추가하며 최초 판단을 소급 변경하지 않는다.

## 기준과 범위

- Repository: `sh0427-han/design-template-library`.
- 실제 기준 main: `b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442`. 원격 main·Open PR 확인 및 4차 PR #23 병합 확인은 조정자의 `review/baseline.json`으로 보존한다. 시작 시 Open PR 0건, PR #23은 해당 main에 병합됐다. 최신 main push CI40606333993 및 Pages40606333192는 모두 completed/success로 확인됐다.
- 작업 브랜치: `feat/interactive-generalization-validation`; 작업 경로: `examples/interactive-kernel/`.
- 대상: Vision AI·머신러닝 입문자. 기존 분류 평가와 다른 연산에서 사용자 조작→상태 계산→여러 표시 갱신을 읽는다.
- 산출물: 동일 콘텐츠·계산·상태를 사용하는 실습형 한 장의 Scroll/Slide HTML. 추가 장·다른 출력 형식·모델 학습·커널 직접 편집은 없다.
- 새 디자인의 원본은 공통 MD와 기존8종이다. 4차의 DESIGN/VALIDATION·실제 화면·독립 검토와 CI는 한계 분석 대상으로 읽었으며 전용 HTML/CSS/JS를 복제하지 않는다. 원본 #5 및 이전 사례 런타임은 보존한다.
- 일반 ‘개념 먼저’ 기본값과 달리 이번 사용자가 명시적으로 요청한 한 장의 실습이므로 실제 입력·계산값을 포함한다. 이 범위 예외를 모든 새 자료의 기본값으로 바꾸지 않는다.

## 학습 목표와 용어

1. 입력은 같은데 선택한 필터가 바뀌면 계산값과 출력 공간 패턴이 달라진다.
2. 커널(kernel)은 주변 픽셀에 곱할 가중치를 담은 작은 행렬이다. CNN(합성곱 신경망)에서 쓰는 국소 계산을 이 고정 필터들로 조작한다.
3. 입력의 3×3 영역과 커널의 같은 위치끼리 곱한 뒤 더한 값이 출력의 한 셀이 된다.
4. 필터 이름·3×3 커널·고정 위치의 계산·5×5 출력·역할 설명은 같은 선택 상태를 나타낸다.
5. 부호가 있는 실제 계산값과 시각화를 위한 색은 다르다. 음수는 제거하지 않으며 색 변환이 계산값을 바꾸지 않는다.

화면 제목은 ‘필터를 바꾸면 달라지는 출력’, 부제는 ‘같은 입력에 다른 가중치를 적용해 공간 특징의 변화를 확인’을 출발 문구로 한다. 제목은 명사구/짧은 구문, 부제는 제목에 대한 부연 설명이다. 기술 조건은 Figure 패널 안에 둔다.

## 선택한 패턴과 규칙 출처

카탈로그의8종 목적을 비교했다. #1은 확대·원본 대응, #2는 처리 흐름, #3은 비교, #4는 한 점의 곱셈/합산, #5는 조작과 동기 갱신, #6은 모델 구조, #7은 평가 지표, #8은 실행 요약이다. 이번 직접 재사용은 **#5의 조작/상태 계약**, 보조는 **#4의 입력 영역→곱합→출력 위치 대응**이다. #5의 임계값·GT·분류 행렬은 사용하지 않는다. #4의5×5 입력/숫자/커널은 복사하지 않는다. Planner는 두 원본 HTML/CSS/JS와 실제 `previews/html-interactive.jpg`, `previews/html-step-by-step.jpg`를 열어 확인했다. 4차의 개념/실습 대표 PNG도 한계 분석 목적으로 확인했다.

| 결정 | 기준 MD·절 | 원본 구현 | 분류 |
| --- | --- | --- | --- |
| 1440×810, 제목49·부제21·Footer15px | DESIGN_SYSTEM §16:9 프레임과 Typography·Header / Content / Footer | `templates/html/reference-layout.css` | A |
| White 패널, border1·radius17·padding20px | DESIGN_COMPONENT_RECIPES §2 큰 패널, DESIGN_SYSTEM §카드와 내부 정렬 | #5 `.live-card` | A |
| 패널 자체 Blue 분류/ Navy 제목, 단계별 설명의 소유 관계 | DESIGN_SYSTEM §제목과 분류 라벨의 역할, RECIPES §제목/라벨 검사의 적용 단위 | #5 `.ref-k`/h2, #4 `.calc-panel` | A |
| 단일 계산 경로·고정 입력/DOM·바뀐 부분만 갱신 | INTERACTIVE_PATTERN §데이터와 판정 계약·화면의 읽는 순서, RECIPES §조작과 상태 | `interactive-reference.js`의 update·rows Map·전용 status | A |
| 입력 패치·출력 셀·원소별 곱합의 대응 | RECIPES §행렬·계산, REFERENCE_PAGE_SPECS §04 Step-by-Step | `step-by-step.html` input5/kernel3/focus-rf/focus-out | A |
| 연산 종류/flip/stride/padding·shape 명시 | FIGURE_PRODUCTION_STANDARD §2 기술적 정확성 검증 | #4 커널 반전 없음·Stride1/Padding0 | A |
| 원값·표시색·표시 반올림 분리 | DESIGN_SYSTEM §원본 데이터·표시색·확대의 관계·수치/수식/표/범례 | #1 색/수치 대응, #4 계산 | A |
| Pretendard Variable·−1pt·STIX MathML | DESIGN_SYSTEM §Pretendard와 전역 자간·본문과 수식의 서체 분리 | 공통 styles/math-typography CSS 및 동봉 WOFF2 | A |
| 화살표·도형 중심·실제 안쪽 경계 | FIGURE_PRODUCTION_STANDARD §6–7·10–13 | #4 도식/매핑·공통 검증 | A |
| Scroll/Slide 같은 원본과 URL 복원·native 입력 보호 | dual-mode DESIGN/MODES, REFERENCE_REUSE_WORKFLOW §Scroll / Slide 공통 원본 | canonical viewer의 입력 예외/URL/배율 계약 | A |
| 대기/실패에서 이전 성공 결과 제거·전용 알림 | RECIPES §5 상태와 실패, DESIGN_SYSTEM §조작 상태·이미지·접근성 | #1/#2 실패 표현, #5 native focus/status | A |
| 일반 역할과 임계값 예제 전용 계약의 범위 분리 | 카탈로그 #5·INTERACTIVE_PATTERN·REFERENCE_REUSE_WORKFLOW | 기준 가이드의 재사용 계약 전체가 분류 전용 | D01 사전 누락 |
| 새7×7 데이터/3커널/고정점/색 범위/내부 좌표·상태 API | 이번 학습 목표와 수학 조건 | 새 설계 | C |

AGENTS.md, DESIGN_SYSTEM.md, TEMPLATE_CATALOG.md, DESIGN_COMPONENT_RECIPES.md, FIGURE_PRODUCTION_STANDARD.md, REFERENCE_PAGE_SPECS.md, INTERACTIVE_PATTERN.md, EXPERIMENT_PATTERN.md, REFERENCE_REUSE_WORKFLOW.md, REFERENCE_REVIEW_GUIDE.md, TEMPLATE_REUSE_VALIDATION.md, CONCEPT_REUSE_PROMPT.md 및 두 보기 DESIGN/MODES를 관련 기준으로 확인했다. EXPERIMENT의 분류 평가 수식·행렬은 이번 자료에 적용하지 않는다.

## 디자인 재사용과 기능 재사용의 구분

**디자인 재사용**은 공통 토큰·폰트·설명 위계·패널·Figure/행렬·여백·정렬·native 조작·검증 관계의 적용이다. #5의 두 카드/6개 샘플 배치를 유지해야 성공하는 것이 아니다.

**기능 재사용**에서는 기존 #5의 update 경로, 안정된 DOM, 현재 조작값에서 파생값을 한 번 계산하고 한 번 갱신하는 순서, native 키보드, 전용 상태 알림, 모션 감소와 focus 유지라는 행동 계약을 옮긴다. 기존 소스는 IIFE 안에서 threshold DOM과 samples/TP/FP 계산에 결합돼 있으며 새 cross-correlation 계산 엔진을 제공하지 않는다. `pct`, GT 그룹, TP/FP/FN/TN, 예측 배지, 판정 문구, 행렬 구분선은 분류 문제 전용이다. 함수 이름만 바꾼 복사를 모듈 재사용 성공으로 세지 않는다.

이번에는 순수 주제별 계산과 상태/렌더 경계를 새로 작성한다. 공통 Interaction Engine이나 Select 컴포넌트 패키지는 제공하지 않는다. 공통 모듈 추출은 이번에 불필요하다는 초기 판단이며 실제 중복/독립 테스트 이점이 발견되면 근거와 영향을 먼저 기록한다.

## Figure와 정보 위계

한 장, 큰 White 패널 하나를 기본 설명 단위로 선언한다. 직접 소유 Blue `.panel-label`과 Navy `.panel-title`은 각각1개다. 페이지 Kicker로 패널 라벨을 대체하지 않는다. 내부 세 Figure는 같은 단계 제목/행렬 슬롯/조건 트랙이며 불필요한 큰 카드로 다시 감싸지 않는다.

읽는 순서는 다음과 같다.

1. 제목/부제로 고정 입력과 바뀌는 가중치의 관계를 예고한다.
2. 패널 헤더: ‘FILTER → OUTPUT’ 분류와 ‘같은 입력, 달라지는 필터 반응’ 제목. 오른쪽 native Select(필터 선택), 초기화 버튼을 둔다.
3. 같은 가로선: 입력7×7 → 현재 커널3×3 → 출력5×5. 짧은 Blue 연결은 Figure 경계 사이에만 놓고 행렬/문구를 가로지르지 않는다.
4. 입력의 고정 3×3 영역과 대응 출력 셀(3행,2열)을 같은 focus 의미로 강조한다. 입력 행렬/위치/셀 DOM은 Select 변경으로 움직이지 않는다.
5. 패널 하단: 교차상관 일반 관계와 조건, 선택 위치의 현재 곱합/정확 분수/표시값, 현재 필터 역할. 식/출력 셀은 같은 계산에서 생성한다.

입력은 회색조 밝기0–9, 출력은 부호·크기를 표현하는 고정 발산 색이라는 별도 의미를 범례에 밝힌다. 항등 필터의 ‘유지’는 valid 영역 원값의 유지이며 입력/출력의 표시색까지 같다는 뜻이 아니다. 입력7×7이 출력5×5가 되는 크기 변화는 패딩0 때문이며 항등에서도 동일하다.

## 수학·데이터 계약 — 예제 고유 C

입력은 단일 채널7×7, 값0–9의 정수 행렬이다. 출처는 본 학습을 위해 정한 합성 밝기 데이터이며 실제 학습 모델의 추론이 아니다. 이 조건은 문서에 남기고 화면에 제작 부가 설명을 반복하지 않는다. 연산에 필수인 조건·색/숫자 구분은 화면에서 유지한다.

```text
0 0 1 1 1 0 0
0 1 2 6 2 1 0
1 2 6 9 6 2 1
1 2 6 9 6 2 1
1 2 6 9 6 2 1
0 1 2 6 2 1 0
0 0 1 1 1 0 0
```

| ID | 이름·역할 | 가중치의 정수 분자 / 분모 |
| --- | --- | --- |
| identity | 항등 필터 · 중앙 픽셀의 원값 유지 | `[[0,0,0],[0,1,0],[0,0,0]] / 1` |
| mean | 평균 블러 · 주변9개 값을 평균내 국소 변화를 완화 | `[[1,1,1],[1,1,1],[1,1,1]] / 9` |
| edge | 세로 에지 · Sobel-x, 좌우 밝기 변화에 반응 | `[[-1,0,1],[-2,0,2],[-1,0,1]] / 1` |

mean의 화면3×3 커널은9개의 `1/9`로 표시한다. 정수1만 보여 실제 가중치라고 설명하지 않는다. 내부 계산은 정수 분자·공통 분모를 유지한다.

딥러닝에서 통상 쓰는 **교차상관(cross-correlation)**: 커널을 뒤집지 않고 `Y[r,c] = Σ(i=0..2)Σ(j=0..2) X[r+i,c+j] N[i,j] / d`로 계산한다. 수학적 convolution의 180° 커널 반전은 수행하지 않는다. stride1, padding0(valid), dilation1, bias0, 채널1이다. 출력 shape는 `(7−3)/1+1=5`로5×5다. ReLU·절댓값·추가 정규화·가중치 학습을 계산 경로에 넣지 않는다.

고정 focus는 **출력(3행,2열)**, 0-based `[2][1]`이다. 입력3–5행/2–4열, 0-based rows2..4/cols1..3의 `[[2,6,9],[2,6,9],[2,6,9]]`와 대응한다. 기본 항등은6, mean은 분자51/분모9=`17/3`이며 화면에서 `51/9 ≈ 5.67`, edge는28이다. 등호와 근사기호를 구분한다. 셀 숫자는 정수이면 정수, 비정수이면 소수2자리이며 원값/원분수를 계산에 사용한다. edge 전체의 실제 범위는−28..28이므로 음수와 양수가 모두 나타난다. mean 분자 행렬은 `[[13,28,34,28,13],[21,43,52,43,21],[27,51,63,51,27],[21,43,52,43,21],[13,28,34,28,13]]`다. 이 값은 독립 Python 검산의 예상 답과 다시 대조한다.

출력 색은 모든 필터에 같은 고정 범위 **−36..+36**을 쓴다. Sobel의 양수 계수합4/음수 절댓값합4와 입력0..9에서 가능한 이론 범위다. `t=min(1,abs(raw)/36)`으로 중립 White에서 음수 Teal/양수 Blue 쪽으로 선형 보간한다. 0은 중립이다. 색 변환에 쓰는 범위 제한은 표시 계층뿐이며 raw/numerator/분모를 바꾸지 않는다. 필터마다 min/max를 다시 맞추지 않는다. 표시 RGB 각 채널은 `Math.round(255+(anchor−255)×t)`로 반올림한다. 입력 회색조는 `Math.round(value/9×255)`로0=검정/9=흰색이며 출력 발산색과 별도 범례다. 셀 숫자는 배경 상대휘도에 따라 검정/흰색으로 대비를 확보하는 데이터 도형 전용 C 예외를 사용하며 제목/일반 본문의 색과 수학 서체·자간은 바꾸지 않는다. 화면 숫자와 접근성 이름은 실제 계산값을 나타내며 색깔만으로 부호를 설명하지 않는다.

## 상태와 인터랙션 계약

- 데이터는 입력 행렬과 kernel ID별 이름/정수 분자/분모/역할 설명이다. 기본 선택은 `identity`다. 입력이 바뀌지 않는 한 input/cell identity/focus 좌표는 고정이다.
- 허용 선택은 `identity`, `mean`, `edge` 세 개. native Select `#kernel-select`와 초기화 `#reset-kernel`을 사용한다. 연속 수치가 아니라 의미가 다른 세 범주이므로 Slider/Toggle 대신 Select를 고른다. 이 선택 기준을 원본에 이미 있는 범용 구현으로 주장하지 않는다.
- 주소는 버전1과 선택 kernel ID를 보존한다. 예: `?v=1&kernel=mean#kernel`. Scroll/Slide 전환과 새로고침에서 선택을 복원한다. 잘못된 ID/버전/값은 명시적 안내와 기본 identity로 정규화한다. URL의 임계값/분류/GT 상태를 새 예제에 남기지 않는다.
- 초기화는 identity·초기 데이터·정상 표시로 돌아간다. Select의 change/키보드 조작은 하나의 상태 전이로 처리하며 모든 파생값·역할·색·status를 같은 render에서 갱신한다. 한 항목만 이전 필터를 가리키는 중간 성공 상태를 노출하지 않는다.
- 순수 계산 API: UMD `KernelModel`의 `validateData`, `correlate(input,numerators,divisor=1)`, `evaluate(data,kernelId)`, `colorFor(value)`, `formatValue(value)`.
- 브라우저 API: `window.KernelInteractive`의 `ready`, `getState()`(deep clone), `selectKernel(id)`, `reset()`. 잘못된 `selectKernel(id)` 호출은 throw하며 직전 유효 상태와 화면을 유지한다. 초기 URL 오류의 기본값 정규화와 구별한다. `ready` Promise는 정상 또는 명시적 error 상태로 settle하여 비처리 rejection/콘솔 오류를 만들지 않는다.
- 상태: `status`, `kernelId`, `input`, `kernelNumerators`, `divisor`, `outputNumerators`, `output`, `focus {patch,products,numerator,denominator,raw,display}`, `error`. `focus.products`는 곱의 정수 분자이며 공통 분모를 별도 유지한다.
- 유효하지 않은 데이터는 원자적으로 실패한다. 이전 성공 행렬/결과를 현재 계산처럼 남기지 않고 입력을 비활성화하고 오류/복구 경로를 제공한다. 기본 데이터 재시도 후 정상 상태를 재구성한다. 데이터 로드 실패 시 Select/Reset을 disabled하고 retry를 제공한다. 초기 스크립트/콘텐츠 실패도 명시적 retry로 구분한다. 폰트 누락은 안내와 사용 가능한 fallback을 제공하되 실제 Pretendard/STIX 성공 검증과 구분한다.
- Select와 버튼의 포커스를 재생성하지 않는다. native 방향키/Home/End/Tab/Enter를 지원하며 viewer 탐색이 입력 키를 가로채지 않는다. 전용 `role=status`에 현재 필터·focus 결과를 알린다. 전체 패널을 live region으로 만들지 않는다. 모션은 필수 아님; 사용하면 달라진 결과만 강조하며 reduced-motion에서 생략한다.

## 공간·폰트·색·정렬 예산

1440×810 source canvas. 공통 토큰/폰트/−1pt를 상속한다. 페이지 padding40px 66px 28px는 이번 밀도에 맞춘 C 소폭 예외이며 다른 예제의 전용 CSS를 복사한 규칙이 아니다. 기본54/66/30에서 조정 가능하다는 공통 프레임 규정을 사용한다.

- 페이지: 높이810−padding68−header118−content gap20−footer45=content559px.
- 패널: 높이550 = border2 + padding20×2 + header66 + gap16 + Figure316 + gap16 + 계산/해석94. Content에 남는9px는 여유다. 외부 마지막 카드/캡션을 추가하지 않는다.
- Figure 공통 트랙: 제목22 + gap8 + 행렬 슬롯256 + gap10 + 범례20 =316px. 행렬 슬롯의 양축 중앙을 맞춘다.
- 입력7×7: cell34/gap3 →256px, 숫자17px. 커널3×3: cell46/gap4 →146px, 숫자/분수22px. 출력5×5: cell44/gap3 →232px, 숫자18px. 각 크기는 C이며 #4의 역할별 셀/중앙정렬 관계를 적용한다.
- Figure 열은 `1fr 36px .9fr 36px 1fr`, gap12px 출발값이다. 화살표 중심은 공통 행렬 슬롯의 중앙이며 경계 사이에만 둔다. 긴 식은 항/행 합 단위로 배치한다.
- 패널 라벨16/20px Blue, 패널 제목25/30px Navy, 단계 제목19–22px Navy, 설명17–19px, 기술 조건/범례16px를 출발값으로 한다. 행렬 숫자·수식은 STIX MathML, 일반 제목/본문은 Pretendard다.
- 입력 grayscale, 커널 Teal 면, 선택 영역 Blue 경계, 출력 양수/음수의 Blue/Teal과 중립 White는 범례로 구별한다. 선택 셀의 테두리는 값의 부호/색을 덮어 원값을 숨기지 않는다.
- PC1600×950/1440×810/1366×768/1280×720의 Scroll/Slide를 같은 내부 좌표와 서식으로 비례 축소한다. 폭과 높이를 모두 고려하고 viewer/notice가 차지하는 높이를 실제로 차감한다. 작은 PC에서 폰트를 개별 축소하거나 overflow:hidden으로 결과를 숨기지 않는다.

공간/문구/상태 구현에서 이 명세를 바꾸면 구현 후의 합리화가 아니라 발견 시점·원인·변경값·검증을 별도 개정 절에 남긴다.

## D0 검증 계획과 완료 기준

화면은4크기×두 모드×한 장=**8개 고유 화면**이다. Select 세 상태의 렌더 확인과 추가 데이터 시나리오는 별도 수로 기록한다. 동일 화면을 세 필터로 캡처해도8개 고유 화면을24개 viewport로 부풀리지 않는다.

Python 정수/Fraction의 별도 이중 루프로 기대 출력을 만들고 JavaScript의 원분자/분모/전체 출력/선택 patch/products/원값과 대조한다. JavaScript 답을 읽어 Python 기대값을 구성하지 않는다. 기본3필터 외 상수0·상수9·ramp/다른 입력, 잘못된 shape/NaN/범위/분모/ID를 검사한다. 비대칭 커널의 별도 계산 fixture와 Sobel 부호를 통해 커널 미반전도 확인한다.

실제 Chromium에서 모든 필터의 이름/커널9셀/출력25셀/고정 위치 결과/역할 설명/색/전용 status의 동기화와 고정 입력·DOM을 확인한다. Select 키보드/포인터/focus/초기화, 모드 왕복/새로고침/invalid URL, 대기/실패/복구와 reduced-motion을 검사한다. 실제 Pretendard/STIX/−1pt, MathML·SVG·text Range·카드 안쪽 padding·arrow 경계·Footer·가로/세로 잘림·정상 콘솔/네트워크도 확인한다. 다른 필터의25개 출력이 실제로 구별돼야 한다.

기존8종/#5의126·42 상태/갤러리와 두 보기, 로지스틱·경사하강법·과적합·4차 임계값의 회귀를 기존 검증기로 실행한다. 회귀 통과는 기존 자료 보존의 증거이며 새 주제의8종 전체 재사용 성공은 아니다. 별도 Reviewer는 원본/설계/실제 소스/브라우저/독립 계산과 D0/D1 원인 분류를 검토하고 지적은 최대3회 수정·재검토한다.

D1에서 디자인 재사용과 기능 재사용을 별도로 판정하고, 임계값 예제 유지 여부/일반 역할 문서 보완 필요/현재 코드 재사용 한계/기존 규칙만으로 재현된 부분/공통 Engine 필요 여부를 각각 답한다. 실제 스크린리더 청취·독자 이해도 실험·모바일/태블릿/다른 브라우저·학습된 CNN 성능·다른 UI 종류의 실제 구현·무맥락 독립 제작자 재현은 미검증이다. main에는 병합하지 않는다.


## D1 실제 구현과 D0 차이 — 이어받기 검토

D0 `286bee0`는 그대로 보존했다. 중단 이후 Chat 모드에서 작성한 `ab713e7`의 구현·초안/실 URL 프리뷰·CI 이력을 이어받았으며 로컬 미커밋 초안은 별도 백업했다. 최초 Chat의 주입 검사는 실제 viewer/독립 Reviewer를 대체하지 않았고, 후속 HTTP CI 성공과도 구분한다.

- C-UI: 두 보기는 같은 `content.html`을 iframe으로 표시한다. `viewer.js`가 URL·외부 배율·오류 안내를 담당하고 `app.js`는 단일 주제 상태를 계산/표시한다. 원본#5나 4차 runtime을 공통 엔진으로 추출하지 않았다.
- C-UI: Figure 트랙은22/256/20px와 gap9/9px로 구현한다(초기8/10px에서 총 높이316은 동일). 화살표를 같은 grid의 두 번째 트랙 중앙에 배치한다. 하단 간격은 margin12/padding8px로 조정해 원소곱/분수와 패널 안쪽 여백을 확보한다.
- A/E: 화면 조건에 커널 미반전·단일채널·valid/stride/dilation/bias/ReLU를 표시하고 `Y=Σ(X×K)`의3×3 이웃 범위를 설명한다. 좌표는 출력3행2열로 표시하고 API에서는0-based `[2][1]`을 유지한다. 커널1/9·선택점51/9·곱합의분모는 native MathML이며 수치/색은 원값과 표시 계층으로 구분한다.
- A/E: 공통 `styles.css`의 폰트·팔레트 토큰을 상속하고 전용 CSS의 중복 root 토큰 선언을 제거했다. 계산값·고정±36색 매핑은 바꾸지 않고 셀 숫자는 sRGB 상대휘도 기준 검정/흰색 중 대비가 큰 색을 선택한다. 데이터 그리드의 검정/흰색 예외는 D0에 이미 명시한 C다.
- A/E: 콘텐츠 로드 실패는 접근 불가 iframe/503/잘못된 응답을 명시적 오류와 재시도로 처리한다. 정상/URL오류/대기 안내 높이를 실제 배율과 stage 가용 높이에서 함께 차감한다. 폰트 실패는 계산 오류로 오인하지 않고 대체 글꼴 상태와 별도 안내를 제공한다.

초기 Chat 화면에 빠진 위 항목은 기존 MathML·Figure 정렬·실패/폰트 계약의 적용 오류(E)이며 공통 지침 신규 누락으로 세지 않는다. 일반 역할과 임계값 전용 계약의 구분 D01은 그대로1건이다.
