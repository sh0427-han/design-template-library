# Design Template Library

AI·ML 교육, 연구 발표, 엔지니어링 보고에 재사용할 **HTML / PPTX 디자인 레퍼런스** 저장소입니다. 현재 모든 예시는 최종 디자인이 아닌 **지속적으로 개선할 초안**입니다.

**공통 디자인:** [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) · Navy/Blue/Teal · 전체 글자 간격 **좁게 1.0pt (`-1pt`)**.

## 8가지 독립 레퍼런스

| 유형 | 적용 용도 | HTML | 구현 상태 |
| --- | --- | --- | --- |
| 01 Concept | 개념과 직관적 수치 예제 | [보기](templates/html/concept.html) | 기존 HTML + 편집 가능한 PPTX |
| 02 Process | 입력 → 처리 → 출력 | [보기](templates/html/process.html) | 기존 HTML + 편집 가능한 PPTX |
| 03 Comparison | 방법 및 조건 비교 | [보기](templates/html/comparison.html) | 기존 HTML + 편집 가능한 PPTX |
| 04 Step-by-step | 수식·계산 과정 | [보기](templates/html/step-by-step.html) | HTML 초안 |
| 05 Interactive | 조작 → 계산 → 결과 | [보기](templates/html/interactive.html) | HTML 초안 + 실시간 연산 |
| 06 Architecture | 모델 및 시스템 구조 | [보기](templates/html/architecture.html) | HTML 초안 |
| 07 Experiment | 그래프·평가 지표 | [보기](templates/html/experiment.html) | HTML 초안 |
| 08 Executive Summary | 보고 결론·근거·조치 | [보기](templates/html/executive-summary.html) | HTML 초안 |

**[8종 HTML 갤러리](templates/html/index.html)** · [유형별 사용 지침](TEMPLATE_CATALOG.md) · [검토 체크리스트](docs/REFERENCE_REVIEW_GUIDE.md)

## 별도: 연속 강의 예제 (Scroll / Slide)

[CNN 강의 예제](templates/dual-mode-learning/)는 **디자인 유형 8종의 일부가 아니라**, 하나의 콘텐츠를 두 방식으로 보여주는 구현 예시입니다.

- [Scroll 웹 교과서](templates/dual-mode-learning/scroll.html): 왼쪽 목차 + 세로 스크롤 + 상세 실습
- [Slide 발표 화면](templates/dual-mode-learning/slides.html): 16:9 · 5장 · 페이지 전환
- [공통 콘텐츠](templates/dual-mode-learning/assets/js/lesson.js) · [공통 계산 로직](templates/dual-mode-learning/assets/js/lab.js)

## 시작하기

저장소 루트에서 `python -m http.server 8000`을 실행한 후 브라우저에서 아래 경로를 엽니다.

- 갤러리: `http://localhost:8000/templates/html/index.html`
- 연속 강의: `http://localhost:8000/templates/dual-mode-learning/index.html`

현재 **3종 PPTX 원본**: [기존 PowerPoint](templates/pptx/technical-slide-templates.pptx) · [재생성 스크립트](templates/pptx/build_templates.py). 신규 5종은 디자인 초안 검토 후 PPTX 제작을 진행합니다. 기존 3종 PPTX는 변경하지 않았습니다.

## AI / Codex 활용

작업 전 [AGENTS.md](AGENTS.md), [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md), [TEMPLATE_CATALOG.md](TEMPLATE_CATALOG.md)를 순서대로 확인하고, 목적에 맞는 레퍼런스의 HTML을 실제로 읽은 뒤 적용합니다. 작업 대상 프로젝트의 기존 요구사항이 우선입니다.

외부 Figure를 포함하는 경우에는 해당 자료 가까이에 원문 URL을 기재합니다. 이 라이브러리는 별도 저장소이며 `sh0427-han-private`의 강의 프로젝트를 자동 수정하지 않습니다.
