# 기술 설명 Figure 제작 표준 — HTML / SVG 레퍼런스

> 적용 범위: Design Template Library의 8종 HTML 레퍼런스와 이를 재사용하는 Scroll / Slide 강의. 기술 그림의 **정확성·구조·정렬·가독성·재현성**을 위한 제작 계약이다. PPTX 지침이 아니다.
>
> 기준 문서: [`DESIGN_SYSTEM.md`](../DESIGN_SYSTEM.md) · [`AGENTS.md`](../AGENTS.md) · [`TEMPLATE_CATALOG.md`](../TEMPLATE_CATALOG.md). 실제 구현 레퍼런스: [`templates/html/architecture.html`](../templates/html/architecture.html), 프리뷰: [`previews/html-architecture.jpg`](../previews/html-architecture.jpg).

## 1. 목적과 완성 기준

**결과물은 단순한 예쁜 이미지가 아니라, 보이는 요소 하나하나가 기술적 의미와 대응하는 편집 가능한 도식이어야 한다.** 이후 CNN 이외의 개념(Perceptron, Transformer, Segmentation, 최적화, 센서 등)에도 같은 절차를 적용한다. #6의 도형을 무조건 복제하지 말고 **레이아웃 규칙과 검증 방식**을 복제한다.

1. 한 화면은 한 가지 핵심 개념을 설명한다. 도입 문장보다 **그림→변화→출력**이 먼저 읽혀야 한다.
2. 입력·중간 처리·출력은 **원인과 결과의 화살표**로 연결한다. 화살표나 색상에 장식 기능만 주지 않는다.
3. 연산 명칭, 출력 Shape, 값, 확률, 화살표 방향은 **한 데이터 정의**에서 유도한다. 그림이 수식과 다르면 오류로 처리한다.
4. 사진, Feature Map Stack, 벡터, 노드, 확률 등 **물리적으로 다른 형태**를 시각적으로 구분한다.
5. 제목·시각물 중심·출력 Shape·한 줄 설명을 하나의 **정렬 축**에 둔다. 가까운 작업은 가까이, 다른 단계는 명확히 떨어뜨린다.
6. 독립 16:9 슬라이드는 1440×810 기준으로 구성하고, 모바일은 단순 축소가 아니라 **읽기 가능한 반응형 재배치**를 사용한다.
7. 프리뷰 JPG/PNG는 HTML의 **실제 Chromium 출력**으로 갱신한다. SVG/HTML 원본을 버리고 이미지로 대체하지 않는다.

## 2. 사전 설계 시트: 각 새 그림마다 먼저 작성

기획자는 아래 표를 실제 값으로 채운 뒤 HTML 작성에 들어간다. 빈칸이 있으면 임의의 수치로 채우지 말고 요구사항을 검토한다.

| 필드 | 작성 내용 |
|---|---|
| 학습 목적 | 수강생이 화면을 보고 단 한 문장으로 말할 핵심 |
| 입력 | 원본 데이터 유형, 차원/단위, 실제 이미지 사용 여부 및 경로 |
| 처리 단계 | 순서, 함수/연산 이름, 매개변수, 반복 그룹(Block/Module) |
| 중간 데이터 | 각 단계 전후의 Shape, 그 Shape를 정하는 계산식 |
| 출력 | 숫자/벡터/공간 지도/범주 확률, 레이블과 의미 |
| 관계 | 화살표가 나타내는 흐름과 내부/외부 연결 구분 |
| 강조 | 꼭 보여줄 변화 하나 또는 두 개(예: H,W 축소 / C 증가) |
| 단순화 | 모식도 축약 지점과 오해 방지 설명(실제 채널 수 ≠ 그린 판 수) |
| 검증 기준 | 예상 Shape, 계산된 예시 값, 접근성/레이아웃 조건 |

**이 자료를 기준으로** 가독성, 색상, SVG 경로를 설계한다. 시각적 욕심 때문에 순서나 기술적 의미를 바꾸지 않는다.

## 3. #6 CNN Architecture 참조 계약

| 시각 단계 | 정확한 연산 | 출력(H×W×C 또는 1D) | 그림 |
|---|---|---|---|
| Input | RGB 이미지 한 장 | `64×64×3` | 단일 이미지 노드 1개. 프레임·중첩 실루엣·불필요한 그림자 금지 |
| Conv Block 1 | Conv `3×3,S1,P1,16ch` → ReLU → MaxPool `2×2,S2` | Conv 후 `64×64×16`, Block 후 `32×32×16` | 큰 Feature Map Stack → 작은 Stack, 블록 안 짧은 화살표 |
| Conv Block 2 | Conv `3×3,S1,P1,32ch` → ReLU → MaxPool `2×2,S2` | Conv 후 `32×32×32`, Block 후 `16×16×32` | 첫 블록과 구조 동일, 단 출력 채널 증가·해상도 감소 |
| Flatten | 원소 순서만 재배열 | `16×16×32 = 8,192D` | 3D Stack → **세로 1D Vector**. 실제 모든 값을 그리지 않으면 생략 기호 |
| FC Layer | `z = Wx + b` | **3 logits** | 1D Vector → 출력 노드 3개. 로그잇은 확률이 아님 |
| Softmax | `p_i = exp(z_i)/Σ_j exp(z_j)` | `P(class0/1/2)` | 확률 막대 및 수치. `[2,1,0]` 예시는 약 66.5%/24.5%/9.0% |

- 이 예제에서 Conv는 `S1,P1`이므로 H/W를 유지하고 출력 채널을 바꾼다. 크기 축소는 `2×2,S2` MaxPool이 수행한다. **모든 CNN의 보편 규칙이라는 표현은 금지**한다. Strided Conv 등 다른 구현이 있다.
- Conv·ReLU·MaxPool은 서로 다른 연산이지만, 교육용 반복 단위로 **Conv Block**이라 묶는다. 블록 안에서 진행 순서를 표현한다.
- Softmax 확률 수치는 **설명용 logits**에서 계산한 것이며 입력 사진에 대한 실제 추론 결과로 주장하지 않는다. 학습 시 `CrossEntropyLoss`에 logits을 직접 주는 경우가 많다.
- `H×W×C`와 Batch 차원 생략은 Shape 설명에 필요한 경우에만 명시한다. 도식 주변에 제작자용 메타 정보 반복 금지.

## 4. 사진·Feature Map·벡터 시각화 규칙

### 입력은 **한 장**

- 실제 입력 파일 경로는 `templates/html/assets/concept-apple-photo.jpg`(HTML에서는 `assets/concept-apple-photo.jpg`). SVG `<image>` **한 개**만 그린다.
- 입력에 `rect` 프레임을 여러 개 덧그리거나 Apple 윤곽 `path`, 색을 입힌 `circle` 등 중첩하지 않는다. 입력 이미지의 보이는 경계는 **한 번만** 생긴다.
- `<image>` 속성에 `preserveAspectRatio="xMidYMid slice"`를 사용하면 입력 프레임의 크기와 이미지 영역의 관계가 예측 가능하다. 원본에서 그 자체로 선이 있는 경우 먼저 원본을 확인한다.
- 이미지를 `z-stack`으로 중복 그리지 않는다. RGB의 3채널은 **사진 뒤 3개의 이미지**가 아니라 `64×64×3` 텍스트로 표현한다.

### Feature Map Stack은 개수를 암시하되 사실과 혼동하지 않음

- Conv 출력은 실제로 `[H,W,C]`. 각 채널의 그림 면은 한 개의 2D Feature Map을 나타낸다.
- C가 16/32라도 화면 안에서 16/32장을 모두 그릴 필요는 없다. 예: 7개 **대표 평면**을 그리되, 표기 Shape는 실제 C를 유지한다.
- 학습된 실제 feature activation을 가지지 않은 시각적 패턴은 **개념용 모식도**이며 실제 추론 결과라고 하지 않는다.
- MaxPool 이후의 면은 Conv 면보다 **공간 크기가 눈에 띄게 작아야** 한다. Pool로 채널 수는 감소하지 않는다.

### Flatten은 독립 표현

- 입력 Tensor = 3D Stack, 출력 = **1열로 정렬된 scalar 벡터**. 2D Feature Map처럼 그리지 않는다.
- 모든 scalar(8,192개)를 표시하는 대신 대표 셀, 중간 생략점으로 구조를 정직하게 축약한다.
- `Flat → FC` 연결은 벡터와 클래스 점수가 **서로 다른 객체**임을 보인다.

## 5. SVG 좌표, 그룹화, 정렬 — 재발 방지 규칙

### 두 종류의 화살표를 구별

| 종류 | 의미 | 색 | 배치 |
|---|---|---|---|
| Stage connector | INPUT → BLOCK1 등 **독립 단계 사이** | Primary Blue `#3168C8` | CSS grid 칼럼 간 동일 수평축, 여백에 배치 |
| Internal connector | Conv → MaxPool, 3D Stack → 1D Vector 등 **한 단계 내부** | Teal `#26A6A1` | 양쪽 실제 도형 bounding box 사이 중앙에 배치 |

내부 화살표는 외부 화살표와 **같은 굵기와 축 기준**을 쓰되 색만 역할에 맞게 달리한다. 색으로만 구별하지 않고, 블록 제목/공간적 묶음으로도 구별한다.

### 화살촉과 직선이 틈 없이 이어져야 함

두 개의 개별 SVG 객체나 CSS border 삼각형을 어림으로 맞추지 않는다. **한 `<path>`**에 shaft/arrowhead 좌표를 동일 종점 `tip`으로 연결한다. 예:

```js
const y = (centerA + centerB) / 2;
const fromX = bboxA.right + 3.5;
const tipX = bboxB.left - 3.5;
const d = `M${fromX} ${y} H${tipX} M${tipX-5} ${y-3.8} L${tipX} ${y} L${tipX-5} ${y+3.8}`;
// SVG attrs: fill='none', stroke=colors.teal, stroke-width=2,
// stroke-linecap='round', stroke-linejoin='round'.
```

단계 사이 Arrow 역시 동일 방식으로 하나의 경로를 사용한다. **화살표가 첫 도형과 마지막 도형에 접촉하거나 겹치지 않게** 양 끝을 3.5px 정도 띄운다(도형 크기에 비례하여 조정 가능). 실제 간격이 11px 미만이면 먼저 레이아웃을 조정한다. 크기를 억지로 줄이거나 화살촉만 도형 위에 덧대지 않는다.

### Stack → Stack의 중앙좌표 계산

Z Stack이 `x,y,size,n,dx,dy`로 정의되고, 뒤로 갈수록 `x+k*dx, y-k*dy`에 놓일 때 **그림 전체** 경계는:

```text
left   = x
right  = x + size + (n - 1) * dx
top    = y - (n - 1) * dy
bottom = y + size
centerY = (top + bottom) / 2
```

화살표의 높이는 `(centerYA + centerYB)/2`. 길이는 `bboxB.left - bboxA.right`에 기반한다. Conv Block 1/2나 Flatten의 도형 위치가 변경되어도 이 계산식을 재사용하므로 **하드코딩된 화살표가 허공에 남지 않는다**.

### 단계 정렬

- `arch-stage`에는 제목, `arch-graphic`, Shape, 연산 조건, 한 줄 설명의 **공통 중심축**이 있다.
- `viewBox` 중앙과 실제 모형 내용의 중앙은 다를 수 있다. SVG `getBBox()`로 내용 그룹의 실제 경계를 구해 중앙에 정렬한다. (`svg`의 `<title>`은 그림 bbox 계산에서 제외)
- 지면을 맞춘다며 장식용 빈 요소를 추가하지 않는다. 적절한 정렬은 CSS Grid/Flex 또는 SVG transform으로 구현한다.
- Conv Block **내부** Conv/Pool은 서로 더 가깝게, Block1/Block2 등 **다른 단계** 사이는 더 넓게. Flatten Stack→Vector도 내부 변환이므로 가까이 둔다.
- 반복 블록 제목에는 **같은 길이·두께의 미세한 밑줄**을 사용한다. 큰 외부 카드로 각 단계를 중첩하여 감싸지 않는다.

## 6. 콘텐츠 배치·밀도·반복 설명

1. 제목은 명사구로 간결하게: `CNN 아키텍처`, `CONV BLOCK 1`, `SOFTMAX` 등.
2. 원리나 사용처는 **해당 도형 바로 아래**에 위치: 출력 Shape(굵게) → 연산/조건(강조색) → 짧은 설명(회색).
3. 동일 연산이 반복되는 Conv Block 1/2 같은 경우, 자세한 `Conv/ReLU/MaxPool` 설명은 **첫 블록에서만** 제공하고 2번째는 Shape와 설정 차이 위주로 남긴다.
4. 하단에 관계없는 요약 카드 세 칸, `Layer vs Block` 같은 갑작스러운 용어풀이, `Tensor Shape / Vector` 제작자 주석을 임의로 늘리지 않는다.
5. Feature Extractor와 Classifier처럼 구조적으로 중요한 영역은 상단의 선/단계 범위로 표현한다.
6. 그림에 들어간 모든 숫자와 레이블을 입력 정의 시트와 대조한다. 모델의 실제 산출값과 *교육용 예시*를 구별한다.

## 7. 시각 시스템과 반응형

- 공유 스타일 **`templates/html/styles.css`**를 기본 사용. 나머지 공통 CSS는 `reference-types.css`, `reference-layout.css`.
- Font: `Pretendard Variable`(Fallback 시스템 폰트), 전체 문자 간격 **`-1pt`**. 제목과 SVG 내부 텍스트도 같은 시각 밀도로 맞춘다.
- 색: Navy `#12233F` (핵심 텍스트), Blue `#3168C8` (독립 단계 간 흐름), Teal `#26A6A1` (블록 내부 변환·출력), Muted `#64748B` (설명), Off-white `#F6F8FC` 배경, White 카드.
- 단일 Figure에는 진한 실선/화살표로 나타내는 **정보 위계가 한 종류씩** 있어야 한다. 반복 색상을 무작위로 변경하지 않는다.
- 1440×810 기본 슬라이드에서는 시각요소와 설명의 좌우 여백, 상하 공간을 실측한다. 900px 이하에서는 3열 등 자연스러운 Grid 재배치, 520px 이하에서는 **1열 단계 + 좌측 그림/우측 텍스트**를 사용한다.
- 좁아질 때 외부 커넥터를 모바일용 아래 방향으로 바꾸되 원인→결과 순서를 지킨다. 의미 없는 가로 스크롤과 2px짜리 텍스트는 금지한다.

## 8. 필수 렌더링·수치 검증

**수정마다** 소스만 검토하지 말고 **Chromium/Playwright로 렌더링** 후 스크린샷을 확인한다.

권장 검사 viewport (CSS pixel):

```text
1600×950, 1440×810, 1366×768, 1280×720, 900×900, 390×844
```

검사 항목:

- [ ] DOM에 **입력 사진 SVG `<image>` 한 개**만 존재하며 추가 외곽 `rect`, 중첩 사과 실루엣, 색 덮개가 없음.
- [ ] Block 2에 Block 1의 Conv/ReLU/Pool 역할 설명이 반복되지 않음.
- [ ] 외부 5개 Connector와 내부 3개 Arrow가 유효한 SVG 경로로 렌더링됨.
- [ ] 내부 3개 Arrow의 선분과 화살촉이 하나의 path이며 도형과 겹치지 않고 두 도형 사이에 위치함.
- [ ] Stage 제목/중앙 SVG 시각물/Shape/설명 중심좌표 차이가 허용 오차(권장 2px) 안.
- [ ] 이미지 경계, Shape, 장식 선, 화살표가 화면 밖으로 잘리거나 서로 겹치지 않음.
- [ ] `document.documentElement.scrollWidth <= innerWidth`, 콘솔 JS 오류 0건.
- [ ] Conv/Pool 출력 Shape, Flatten 곱셈, Softmax 확률/합계 독립적으로 계산 검증.
- [ ] PPTX 만들지 않고 **HTML 소스와 `previews/...` 출력 파일**을 함께 갱신.
- [ ] 기본 asset, 공유 CSS를 실제 로딩해 다시 확인. 테스트용 Placeholder를 **원본 자산처럼 주장하지 않기**.

## 9. 재현 작업 절차 — 다음 개념 제작 시

1. `AGENTS.md` → `DESIGN_SYSTEM.md` → 이 문서 → `TEMPLATE_CATALOG.md` 순으로 읽는다.
2. 사용자의 컨셉, 입력/출력, 기술적 계산을 먼저 확정한다. **위 2절 설계 시트**를 채운다.
3. 8종 레퍼런스 중 가장 가까운 레이아웃을 선택하고, 기존 제목/본문 레벨과 색상 토큰을 재사용한다.
4. HTML 요소(텍스트/이미지)와 SVG(Feature Map, Vector, 화살표)를 컴포넌트별로 구현한다. Shape와 label은 한 데이터 정의에서 나온다.
5. SVG 도형을 먼저 배치한 후 경계(bounding box)를 측정해서 화살표를 **나중에** 그린다. 절대 위치를 추측하지 않는다.
6. 반복 단계 설명은 첫 예시에만 붙이고, 나머지 반복은 값이나 변화만 표현한다.
7. 6개 viewport에서 렌더링 검증하고, 실제 이미지와 텍스트 가독성을 눈으로 확인한 뒤 프리뷰 생성.
8. 작업별 별도 GitHub branch/PR에서 변경 범위를 좁혀 커밋한다. HTML, README/카탈로그, 프리뷰를 동기화한다.
9. 기술 오류, 화면 깨짐, 프리뷰 불일치가 있으면 '완료'로 표시하지 않는다. 제한사항을 PR과 답변에 적는다.

## 10. 새로운 개념에서도 달라지지 않을 원칙

**복제하는 것은 일관된 완성도이며, 사과 그림·두 Conv Block·3분류 같은 도메인 전용 콘텐츠가 아니다.** 예를 들어 Sensor Comparison이면 RGB/IR/LiDAR 데이터의 단위와 시각화가 중심이고, Optimizer라면 손실 함수 변화와 파라미터 업데이트가 중심이다. 어떤 주제든 **정확한 연산, 실제 값과 모식도 구분, 콘텐츠 바로 옆의 짧은 설명, 수학적으로 계산한 도형 배치, 여러 화면에서 검증한 소스·프리뷰 쌍**이라는 검수 기준을 유지한다.