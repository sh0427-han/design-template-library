# Design Template Library

AI·ML 교육자료, 논문·기술 발표, 엔지니어링 보고를 위한 **HTML 전용 디자인 레퍼런스 라이브러리**입니다. 최종 제작물은 브라우저에서 실행되는 **Scroll Mode 또는 Slide Mode**의 HTML 자료이며, **PPTX를 제작하지 않습니다.**

현재 8종 레이아웃은 지속적으로 개선하는 재사용 가능한 **시각적 구성 패턴**입니다. 이 8종은 출력 포맷이나 독립된 렌더링 모드가 아니라, Scroll·Slide 양쪽에서 활용할 수 있는 레퍼런스입니다.

**공통 디자인:** [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) · Pretendard Variable · Navy/Blue/Teal · 전체 자간 `-1pt`.

## 출력 모드

| 모드 | 사용 목적 | 화면·탐색 방식 |
| --- | --- | --- |
| **Scroll** | 웹 교과서, 기술 문서, 상세 설명, 인터랙티브 실습 | 연속 문서·세로 스크롤·목차/앵커 |
| **Slide** | 강의, 논문 발표, 기술 발표, 엔지니어링 보고 | 16:9 화면·한 장에 한 개념·페이지/키보드 전환 |

가능하면 **콘텐츠·수식·계산 로직·디자인 토큰은 공유**하고, 모드마다 화면 배치·탐색·설명 밀도만 구분합니다.

## 8가지 독립 디자인 레퍼런스

| 유형 | 적용 용도 | HTML |
| --- | --- | --- |
| 01 Concept | 개념과 직관적 수치 예제 | [보기](templates/html/concept.html) |
| 02 Process | 입력 → 처리 → 출력 | [보기](templates/html/process.html) |
| 03 Comparison | 방법 및 조건 비교 | [보기](templates/html/comparison.html) |
| 04 Step-by-step | 수식·계산 과정 | [보기](templates/html/step-by-step.html) |
| 05 Interactive | 조작 → 계산 → 결과 | [보기](templates/html/interactive.html) |
| 06 Architecture | 모델 및 시스템 구조 | [보기](templates/html/architecture.html) |
| 07 Experiment | 그래프·평가 지표 | [보기](templates/html/experiment.html) |
| 08 Executive Summary | 보고 결론·근거·조치 | [보기](templates/html/executive-summary.html) |

**[8종 HTML 갤러리](templates/html/index.html)** · [유형별 사용 지침](TEMPLATE_CATALOG.md) · [검토 체크리스트](docs/REFERENCE_REVIEW_GUIDE.md)

## Scroll / Slide 통합 구현 예제

[CNN 강의 예제](templates/dual-mode-learning/)는 별도의 디자인 유형이 아니라, **동일한 콘텐츠를 두 HTML 렌더링 모드로 제공하는 실제 구현 사례**입니다.

- [Scroll 웹 교과서](templates/dual-mode-learning/scroll.html): 왼쪽 목차 + 연속 스크롤 + 상세 실습
- [Slide 발표 화면](templates/dual-mode-learning/slides.html): 16:9 · 5장 · 키보드/버튼 전환
- [공통 콘텐츠](templates/dual-mode-learning/assets/js/lesson.js) · [공통 계산 로직](templates/dual-mode-learning/assets/js/lab.js)

## 시작하기

저장소 루트에서 `python -m http.server 8000`을 실행하고 브라우저에서 열 수 있습니다.

- 갤러리: `http://localhost:8000/templates/html/index.html`
- Scroll / Slide 강의: `http://localhost:8000/templates/dual-mode-learning/index.html`

## AI / Codex 작업 원칙

작업 전 [AGENTS.md](AGENTS.md), [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md), [TEMPLATE_CATALOG.md](TEMPLATE_CATALOG.md)를 확인하고 관련 HTML·CSS·JavaScript를 검토합니다. **새 결과물은 HTML로만 제작**하며 PPTX 생성·변환·동기화·프리뷰 갱신 작업은 하지 않습니다.

외부 Figure를 활용하면 Figure 가까이에 원문 URL을 기재합니다. 실제 브라우저로 레이아웃과 인터랙션을 검증하며, 별도 프로젝트인 `sh0427-han-private`은 명시적인 요청 없이 수정하지 않습니다.

기존 PPTX 파일 및 생성 스크립트, PPTX 전용 프리뷰는 저장소에서 삭제했습니다. 현재 제공 형식은 HTML Scroll/Slide뿐입니다.
