# Design System · HTML Scroll / Slide

이 문서는 현재 구현의 **공통 시각 규격**입니다. 계산·데이터와 페이지별 배치는 [상세 명세](docs/REFERENCE_PAGE_SPECS.md), 제작 절차와 SVG 기하는 [Figure 표준](docs/FIGURE_PRODUCTION_STANDARD.md)을 따릅니다. 결과물은 편집 가능한 HTML/CSS/SVG/JavaScript이며 PPTX를 만들지 않습니다.

## 원칙과 정보 위계

- 한 슬라이드에 하나의 핵심 메시지. 사진·도형·행렬·수치가 설명에 기여해야 합니다.
- 제목 → 핵심 Figure → 연결된 데이터·수식 → 짧은 해석 → 마지막 핵심 캡션 순서로 읽히게 합니다.
- 실제값과 예측, tensor와 vector, logits와 probability처럼 다른 의미를 같은 모양으로 뭉치지 않습니다.
- 반복 설명은 첫 반복 블록에 모으고 이후에는 차이를 설명합니다. 빈 공간을 채우기 위해 문단을 늘리지 않습니다.
- 사용자·프로젝트의 구체적인 조건이 기본값보다 우선합니다. 변경 이유와 검증을 기록합니다.

## 단일 토큰과 색의 의미

공통 토큰은 [styles.css](templates/html/styles.css)에 있습니다. 페이지별 보정은 클래스 범위 안에서 작성하며 전체 갤러리·다른 유형에 새 전역 스타일을 흘리지 않습니다.

| 토큰 | 값 | 사용 의미 |
| --- | --- | --- |
| `--navy` | `#12233F` | 제목·핵심 숫자·중요한 구조 |
| `--deep` | `#1B3558` | 보조 제목·공식·주요 라벨 |
| `--blue` | `#3168C8` | 외부 처리 흐름·조작·선택·예측 이상 |
| `--teal` | `#26A6A1` | 내부 변환·결과·핵심 해석의 가는 강조선 |
| `--amber` | `#E49A4D` | 임계값 위치·오류 판정·대조 조건 |
| `--ink` | `#1B2940` | 본문 |
| `--muted` | `#64748B` | 조건·짧은 보조 설명·예측 정상 |
| `--canvas` | `#F6F8FC` | 캔버스 |
| `--white` | `#FFFFFF` | 일반 콘텐츠 카드 |
| `--border` | `#DDE4EF` | 구조 구분선·카드 경계 |
| `--pale-blue` / `--pale-teal` | `#EAF1FF` / `#E3F6F3` | 의미가 있는 작은 처리·결과 영역 |

색은 문맥 안에서 정의합니다. Teal이 모든 정상 클래스, Amber가 모든 이상 클래스를 뜻하는 것은 아닙니다. #5·#7은 **TP/TN=Teal, FP/FN=Amber**이며, #5의 예측 클래스는 별도 Blue/Muted 배지입니다. 문자와 위치를 함께 사용해 색만으로 의미를 전달하지 않습니다.

## Pretendard와 전역 자간

```css
@font-face {
  font-family: "Pretendard Variable";
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url("assets/fonts/pretendard/PretendardVariable.woff2") format("woff2");
}
:root {
  --font-sans: "Pretendard Variable", "Pretendard", "Malgun Gothic",
               "Apple SD Gothic Neo", system-ui, sans-serif;
  --character-spacing: -1pt;
  font-family: var(--font-sans);
}
html { letter-spacing: var(--character-spacing); }
```

공식 Pretendard v1.3.9 WOFF2를 [폰트 폴더](templates/html/assets/fonts/pretendard/README.md)에 동봉합니다. 외부 폰트 CDN이 필요하지 않습니다. CSS를 다른 위치로 복사하면 WOFF2의 상대 URL과 라이선스도 함께 유지합니다.

- 제목·본문·라벨·SVG 텍스트·각주·푸터·입력 UI 모두 `−1pt`를 상속합니다. CSS 기준 약 `−1.3333px`입니다.
- 특정 라벨의 자간만 0이나 양수로 바꾸지 않습니다. 폭이 부족하면 구조·줄바꿈·간격을 먼저 조정합니다.
- 제목 700–800, 본문 400–600, 핵심 수치 750–850 등 의미에 맞는 가변 굵기를 사용합니다.
- `font-family` 이름이나 `document.fonts.check`만으로 실제 글꼴을 보장하지 않습니다. `document.fonts.load/ready`와 CDP `CSS.getPlatformFontsForNode`를 함께 검사합니다.
- #4의 원소별 곱 기호는 원본 폰트가 해당 글리프를 제공하지 않아 동일 모양의 SVG 원·점을 사용합니다. 기호를 표시하려고 다른 텍스트 폰트를 섞지 않습니다.
- `font-display: swap`의 초기 폴백은 가능하지만 최종 프리뷰는 로딩 완료 후 실제 Pretendard로만 생성합니다.

## 16:9 프레임과 Typography

[reference-layout.css](templates/html/reference-layout.css)는 8종에만 명시적으로 로드합니다.

| 요소 | 기준 규격 | 역할·주의 |
| --- | --- | --- |
| 캔버스 | 1440×810 | 데스크톱 16:9 |
| 바깥 여백 | 위 54 / 좌우 66 / 아래 30px | 페이지별 검증된 작은 보정 허용 |
| Category | 17px, Blue, 800 | 유형 식별, 제작자용 칩 추가 금지 |
| Title | 49px | 간결한 한국어 명사구·핵심 구문 |
| Subtitle | 21px, 1.38 | 가능한 한 줄, 불필요한 강제 개행 금지 |
| Content 상단 | 기본 25px | 개별 예제의 정보 밀도에 맞춘 보정 가능 |
| 카드 제목 | 보통 24–29px | 같은 역할은 같은 크기·굵기 |
| 주요 본문 | 보통 19–26px | 데이터 밀도와 발표 거리에 맞춤 |
| 기술 라벨·조건 | 보통 14–19px | 작은 상세 연산 라벨은 #4·#6 검증값 참고 |
| Footer | 15px, 상단 선, margin-top 15px | 마지막 콘텐츠와 겹치지 않음 |

#4의 9개 곱 설명처럼 정보 밀도가 높은 영역은 더 작은 글자를 사용할 수 있습니다. 이를 모든 새 자료의 본문 기본 크기로 복사하지 않습니다. 길거나 많은 설명은 Scroll 또는 별도 슬라이드로 분리합니다. 전체 요소를 작게 줄이는 방식으로 초과 내용을 숨기지 않습니다.

데스크톱의 프레임 축소는 다음과 같습니다.

```css
zoom: min(1, calc((100vw - 40px) / 1440px),
             calc((100vh - 40px) / 810px));
```

너비뿐 아니라 높이도 고려합니다. 1280×720에서 원래 810px 캔버스를 그대로 남겨 화면 밖으로 밀어내지 않습니다.

## Header / Content / Footer

Header는 Category·Title·Subtitle 순서이며 청중에게 필요한 정보만 둡니다. Content는 개념의 순서에 따라 흐름·비교·계산·구조·평가 등으로 구성합니다. Footer는 자료명과 장 번호를 최소한으로 표시합니다.

- 본문이 Footer를 덮지 않도록 `min-height:0`과 실제 콘텐츠 높이를 함께 점검합니다.
- 마지막 핵심 캡션은 **콘텐츠의 마지막**, Footer 앞에 둡니다. 아래에 회색 설명을 별도 흘리지 않습니다. 필수 조건은 관련 카드 안에 포함합니다.
- 현재 #1·#2·#5에 있는 캡션은 `.ref-takeaway`를 사용합니다. 다른 페이지에 의미 없는 결론을 억지로 추가하지 않습니다.
- `.ref-takeaway`: 흰색 바탕·왼쪽 Teal 선. 카드 전체를 초록 배경으로 채우지 않습니다.

## 카드와 내부 정렬

일반 콘텐츠 카드는 White, 가는 Border, 약 12–20px radius입니다. 기본 패딩은 약 20–26px이며 좁은 화면에서 검증된 값으로 줄입니다.

- 좌우 카드는 위·아래 경계가 맞아야 합니다. 서로 비교하는 제목·행·기준선도 맞춥니다.
- 카드 안의 마지막 문구·숫자까지 **안쪽 패딩 경계 안**에 들어가야 합니다. 테두리 안이라는 이유로 패딩 침범을 허용하지 않습니다.
- `overflow:hidden`으로 잘못된 높이를 가려 검증을 통과시키지 않습니다.
- #4의 좌우 설명 구역은 두 `.calc-footnote` 구분선의 Y좌표 차이를 1px 이하로 맞춥니다.
- #5의 실제값 그룹은 고정, 예측 배지와 집계만 바뀝니다. 판정 규칙과 점선 범례는 별도 구역입니다.
- #7의 행렬 라벨·숫자는 중앙 정렬합니다. 모델 예측 옆 세로선은 **실제 제목 글자와 행 라벨 사이 중앙**에 둡니다.

## Figure의 중심축·간격·화살표

제목·실제 그림 경계·Shape·설명의 공통 축을 확인합니다. SVG `viewBox` 중앙만 맞추고 실제 그림은 한쪽으로 치우치게 두지 않습니다. `getBBox()`로 실제 도형을 측정하고, 폰트 로딩 후 텍스트 경계가 바뀌면 다시 정렬합니다.

- 반복 블록 내부는 가깝게, 다른 단계 사이는 더 넓게 배치합니다.
- 단계 사이 외부 화살표는 Blue, 블록 내부 변환은 Teal을 사용합니다. 배치와 그룹 제목으로도 구분합니다.
- 화살촉과 선의 종점을 같은 좌표로 계산한 단일 SVG path를 사용합니다. 도형과는 경계 기준 약 3.5px 간격을 둡니다.
- #6의 내부 최소 간격은 화살표를 넣기 전에 확보합니다. 단순히 화살촉 크기를 줄이지 않습니다.
- 실제 좌표 계산과 코드 예시는 [Figure 제작 표준](docs/FIGURE_PRODUCTION_STANDARD.md)에 있습니다.

## 반응형

| 화면 | 기본 동작 |
| --- | --- |
| 900px 초과 | 창 너비·높이를 고려한 16:9 비례 축소 |
| 900px 이하 | 세로 읽기 배치, 높이 자동, 자연스러운 문서 스크롤 |
| 520px 이하 | 복잡한 카드·지표를 1열로, 짧은 행렬·비교 항목의 의미 유지 |

#6은 태블릿에서 3열, 모바일에서 단계별 1열·그림 왼쪽/텍스트 오른쪽으로 바뀝니다. #8은 모바일에서도 세 KPI의 가로 그룹을 유지하되 숫자와 단위를 세로로 배치합니다. 하나의 반응형 규칙을 모든 도식에 강제하지 않습니다.

한국어는 `word-break:keep-all`, 문단은 `text-wrap:pretty`를 기본 사용합니다. 화살표는 읽는 방향에 맞추고 모바일 가로 스크롤을 만들지 않습니다. 모션 감소 설정은 #5의 배지 강조를 생략합니다.

## 검증과 재사용

`python scripts/validate_references.py`는 8×6 조합의 실제 폰트·자간·수학·사진·기하·카드·푸터를 검사합니다. `python scripts/check_interactive.py`는 경계값과 변경 데이터 재사용을 추가로 확인합니다. 자동 수치 검사 후 데스크톱과 모바일 캡처를 직접 확인합니다.

프리뷰는 검토 증거이며 도형·텍스트·계산 소스의 대체물이 아닙니다. [재사용 워크플로](docs/REFERENCE_REUSE_WORKFLOW.md)와 [페이지 상세 명세](docs/REFERENCE_PAGE_SPECS.md)를 함께 사용합니다.
