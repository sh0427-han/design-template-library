# Design Template Library

AI·ML 교육자료, 논문·기술 발표, 엔지니어링 보고를 위한 **편집 가능한 HTML 시각 설명 패턴**입니다. 결과물은 **HTML Scroll / Slide**이며 PPTX 생성·변환·동기화는 지원하지 않습니다.

제작 대상은 PC에서 보는 웹페이지입니다. 새 자료의 필수 검토 크기는 1600×950 / 1440×810 / 1366×768 / 1280×720이며 모바일 전용 제작·검수는 요구하지 않습니다.

정확한 수식과 데이터, 읽기 쉬운 Figure, 실제 브라우저 검증을 함께 재사용합니다. 프리뷰 이미지를 새 자료에 붙여 넣는 방식 대신 HTML/CSS/SVG/JavaScript 원본을 수정합니다.

## Scroll와 Slide, 8개 패턴의 관계

| 구분 | 역할 |
| --- | --- |
| Scroll Mode | 연속 문서·목차·상세 설명·직접 조작하는 실습 |
| Slide Mode | 16:9·페이지 단위 탐색·한 장에 한 개념 |
| 8개 레퍼런스 | 두 모드에서 필요한 부분을 선택·조합하는 설명 패턴 |
| Scroll / Slide 보기 | 기존 8개 원본을 연속 읽기/한 장씩 보기로 연결. 별도 디자인 없음 |

8종을 모든 자료에 순서대로 넣지 않습니다. 청중과 학습 목표를 먼저 정한 뒤 가장 적합한 표현을 선택합니다. 두 모드에서는 콘텐츠·연산·색상·폰트를 공유하고 배치·탐색·설명 밀도만 구분합니다.

## 8개 레퍼런스

| 번호 | 패턴 | 핵심 표현 | 원본 |
| --- | --- | --- | --- |
| 01 | Concept | 사진 → 실제 채널 → 같은 ROI 확대 → RGB/HEX | [HTML](templates/html/concept.html) |
| 02 | Process | 이미지 → 특징 추출 → Task Head → 결과 | [HTML](templates/html/process.html) |
| 03 | Comparison | 같은 입력에서 규칙 지정 / 데이터 학습 비교 | [HTML](templates/html/comparison.html) |
| 04 | Step-by-Step | 5×5 입력·3×3 커널·9개 곱·합 −6 | [HTML](templates/html/step-by-step.html) |
| 05 | Interactive | 임계값 → 예측 배지 → 행렬·실시간 지표 | [HTML](templates/html/interactive.html) |
| 06 | Architecture | 두 Conv Block → Flatten 8,192 → FC → Softmax | [HTML](templates/html/architecture.html) |
| 07 | Experiment | TP FP / FN TN 행렬과 4개 지표 | [HTML](templates/html/experiment.html) |
| 08 | Executive Summary | 지표별 기존/개선안 막대와 실행 항목 | [HTML](templates/html/executive-summary.html) |

[갤러리](templates/html/index.html) · [카탈로그와 사용 조건](TEMPLATE_CATALOG.md) · [페이지별 상세 명세](docs/REFERENCE_PAGE_SPECS.md)

## 로컬 실행

저장소 루트에서 실행합니다. 공통 CSS·폰트·사진의 상대 경로가 필요하므로 하위 폴더만 서버 루트로 지정하지 않습니다.

```bash
python -m http.server 8000
```

- 갤러리: `http://localhost:8000/templates/html/index.html`
- Scroll: `http://localhost:8000/templates/dual-mode-learning/scroll.html`
- Slide: `http://localhost:8000/templates/dual-mode-learning/slides.html`

기본 폰트는 **Pretendard Variable v1.3.9**, 자간은 모든 텍스트 **−1pt**입니다. 공식 WOFF2와 라이선스를 저장소에 포함해 CDN 연결 없이 로드합니다. [폰트 출처·해시·라이선스](templates/html/assets/fonts/pretendard/README.md)

새 자료의 수식·변수·계수는 **STIX Two Math + Native MathML**로 분리합니다. 일반 영문은 Pretendard를 유지합니다. [적용 규격](DESIGN_SYSTEM.md#본문과-수식의-서체-분리) · [수학 폰트·라이선스](templates/html/assets/fonts/stix-two-math/README.md). 기존 8종의 폰트를 자동 변경하는 규칙은 아닙니다.

## 디렉터리 구조

```text
templates/html/                  # 8개 원본과 갤러리
  styles.css                     # 색상·로컬 폰트·전역 -1pt·행간/간격 토큰
  reference-layout.css           # 8종 전용 16:9/반응형 프레임
  reference-types.css            # 유형별 기본 컴포넌트
  assets/                        # 사진·고정 필터 예제·Pretendard
  interactive-reference.js       # #5 단일 계산 경로
templates/dual-mode-learning/    # 기존 8개 원본의 Scroll / Slide 보기
previews/                       # 실제 Chromium 대표 이미지
  review/                        # 검증 JSON·#5 공유용 단일 HTML
scripts/                        # 공통 검증·프리뷰 생성·문서 검사
docs/                           # 제작 기준·명세·재사용·통합 기록
.github/workflows/              # PR에서 실행하는 검증
```

## 검증과 프리뷰 생성

Python 3.11 이상, Node.js, Python Playwright와 Chromium이 필요합니다. 시스템 Chromium을 쓰면 `CHROMIUM_EXECUTABLE`로 경로를 지정할 수 있습니다. CI에서는 Playwright가 설치한 Chromium을 사용합니다.

```bash
python -m pip install playwright
python -m playwright install chromium
python scripts/check_sources.py
python scripts/verify_character_spacing.py
python scripts/validate_references.py
python scripts/check_interactive.py
python scripts/verify_pretendard.py
python scripts/verify_logistic_reuse.py
python templates/dual-mode-learning/tools/check.py
python scripts/check_documentation.py
```

현재 저장소의 `validate_references.py`는 기존 호환성 회귀 검사로 원본 8종을 **1600×950 / 1440×810 / 1366×768 / 1280×720 / 900×900 / 390×844**, 총 48개 조합에서 검증합니다. 수식·사진·특징 맵·행렬·실시간 판정·도형 정렬·화살표·오버플로·푸터·자간을 검사하고 대표 프리뷰를 갱신합니다. `document.fonts` 로딩뿐 아니라 CDP의 **실제 렌더링 글꼴**도 확인합니다. 이 도구의 6개 실행 크기와 새 자료의 PC 4개 필수 제작 범위는 구분합니다.

- 대표 이미지: `previews/html-*` — 1600×950 창 안의 1440×810 슬라이드 캡처
- 전체 결과: [reference-validation.json](previews/review/reference-validation.json)
- 화면별 PNG: 기본 `/tmp/reference-integration-review`
- #5 추가 검증: [interactive-validation.json](previews/review/interactive-validation.json), 데이터 변경 재사용·경계값·키보드·오프라인 공유본
- 공유용 #5: [interactive-live.html](previews/review/interactive-live.html), CSS·JS·폰트 내장

부분 검증 예:

```bash
python scripts/validate_references.py --templates architecture step-by-step --evidence-dir /tmp/selected-review
```

검증 명령은 `validate_references.py`로 통일했습니다. 부분 검증은 `--report /tmp/selected-validation.json`처럼 임시 경로를 지정하며 전체 통과 기록을 대체하지 않습니다. 기존 대표 프리뷰를 갱신하지 않고 검사하려면 값 없이 `--update-previews`를 붙입니다. 현재 원본 검증 결과와 프리뷰 해시는 JSON에 함께 기록됩니다.

## 새 슬라이드 제작

1. [AGENTS.md](AGENTS.md)와 [디자인 시스템](DESIGN_SYSTEM.md)을 읽습니다.
2. 청중·한 줄 학습 목표·입력·출력·수식·단순화 조건을 정합니다.
3. [카탈로그](TEMPLATE_CATALOG.md)에서 패턴을 고르고 [상세 명세](docs/REFERENCE_PAGE_SPECS.md)를 확인합니다.
4. [개념→상세 기본 순서](DESIGN_SYSTEM.md#개념-설명의-기본-순서)에 따라 개념 장은 그림·키워드·일반 관계로 완결하고, 상세 장은 요청된 경우에만 실제 입력·계산·사례를 배치합니다. 중간 출력과 다음 입력을 연결하고 필요하면 같은 계산값을 그래프의 축·교점에 표시합니다. [컴포넌트 설계 규격](docs/DESIGN_COMPONENT_RECIPES.md)의 기록표에 카드·행간/간격·도식·수식·상태·PC 창 대응·높이 예산을 정하고, [Figure 제작 표준](docs/FIGURE_PRODUCTION_STANDARD.md)에 따라 편집 가능한 도형과 데이터 흐름을 설계합니다.
5. [재사용 워크플로](docs/REFERENCE_REUSE_WORKFLOW.md)에 따라 실제 과제 데이터로 바꾸고 다른 데이터 구성으로도 확인합니다.
6. 수학·실제 폰트·PC 4개 화면·실제 캡처를 검증하고 관련 문서·카탈로그·프리뷰를 동기화합니다.

외부 Figure를 쓸 때는 가까이에 원문 URL을 표시합니다. 고정 필터, 모식도, 설명용 logits, 예시 KPI를 실제 학습 모델의 성능으로 주장하지 않습니다.

### 새 개념으로 재사용 검증

**기존8종 + 공통 Markdown → 새 개념 제작 → 누락/문제 검토 → 공통 Markdown 보완 → 다른 새 개념으로 재검증**의 순환입니다. 새 슬라이드는 템플릿과 문서의 재현 가능성을 검증하는 산출물입니다.

[로지스틱 회귀 개념 한 장](examples/logistic-regression/README.md)은 첫 검토 사례입니다. 수학 서체·기호 정의·입력 패딩/중앙축·설명과 Figure 정렬·분량·연결선·전달 방식 등의 교훈을 [검증 기록과 기준](docs/TEMPLATE_REUSE_VALIDATION.md)에 정리해 공통 문서로 연결했습니다. 로지스틱 회귀를 새 정본으로 복제하지 않습니다. 현재 한 장의8개 PC 화면/161곡선점 통과와8종 전체의 재사용 성공을 구분합니다.

다음 라운드는 **기존8종과 갱신한 공통 Markdown**만을 기준으로 새 주제를 제작하고, `DESIGN.md`의 규칙 출처와 `VALIDATION.md`의 문서 누락·고유 설계·구현 오류·검증/미검증 범위를 남깁니다. [복사 가능한 검증 프롬프트](docs/CONCEPT_REUSE_PROMPT.md)를 사용합니다.

추가 검증 사례: [경사하강법 개념 한 장](examples/gradient-descent/README.md). 기존8종과 공통 지침만을 설계 입력으로 사용했으며, [D0/D1 평가](examples/gradient-descent/VALIDATION.md)에서 재사용 범위·문서 부족·개념 고유 설계·구현 오류를 구분합니다. 검증은 `python scripts/verify_gradient_descent.py`로 재현합니다.

## 문서 지도와 통합 상태

- [사용 방법](docs/USAGE.md): 실행·복사·편집 요령
- [컴포넌트 설계 규격](docs/DESIGN_COMPONENT_RECIPES.md): #1–#8 전체에서 대조한 실제 수치·변형·예외와 새 개념의 설계 기록표
- [Figure 제작 표준](docs/FIGURE_PRODUCTION_STANDARD.md): 개념에서 실제 도식까지의 실무 절차
- [페이지 상세 명세](docs/REFERENCE_PAGE_SPECS.md): 8개 페이지를 재구현할 수 있는 데이터·수식·구성
- [Interactive 상세 패턴](docs/INTERACTIVE_PATTERN.md) · [Experiment 상세 패턴](docs/EXPERIMENT_PATTERN.md)
- [검토 체크리스트](docs/REFERENCE_REVIEW_GUIDE.md) · [프리뷰와 증거](previews/review/README.md)
- [8종 검토 완료 상태·최신 출처·유지보수](docs/REFERENCE_RELEASE_STATUS.md)
- [2026-10-22 초기 통합 이력](docs/INTEGRATION_REPORT_2026-10-22.md)

8종 모두 사용자 디자인 검토를 마쳤습니다. #1 PR #15, #2 PR #13/#18, #3 PR #14와 두 모드 PR #17까지 반영한 출처는 [현재 상태](docs/REFERENCE_RELEASE_STATUS.md)에서 확인합니다. PR #12는 초기 통합의 역사적 기록입니다. 로컬 검증·사용자 디자인 승인·원격 게시·main 반영은 실제 증거로 구분합니다.

## Scroll / Slide 전환 예제의 재사용

[Scroll](templates/dual-mode-learning/scroll.html)과 [Slide](templates/dual-mode-learning/slides.html)는 같은 8개 원본 HTML을 직접 표시합니다. 별도 5장 CNN 디자인과 실습 전용 출력은 제거했습니다. 대표 프리뷰도 [Scroll](previews/dual-mode-scroll.jpg), [Slide](previews/dual-mode-slide.jpg) 두 개입니다. #5의 조작은 두 모드 안에서 같은 원본 JS로 동작합니다.

[재사용 상세 명세](docs/DUAL_MODE_REFERENCE_REUSE.md)는 원본 경로·서식 경계·배율·URL 상태와 검증을 기록합니다. `python scripts/verify_pretendard.py`로 두 모드의 64개 PC 화면을 원본과 직접 대조하고 계산·실제 글리프·전환 상태를 확인합니다.
