# 8종 HTML 레퍼런스 재사용 워크플로

이 라이브러리는 **Scroll/Slide HTML 자료 제작용 디자인 시스템**입니다. 8종은 렌더링 형식이 아닌 **재사용할 수 있는 설명 패턴**입니다. 모든 자료에 8장을 순서대로 넣거나, 프리뷰 이미지를 캡처하여 붙여넣는 방식이 아닙니다.

## 무엇을 보고 만드는가?

| 우선순위 | 자료 | 역할 |
| --- | --- | --- |
| 1 | `AGENTS.md`, `DESIGN_SYSTEM.md` | 제약과 정식 디자인 토큰: Pretendard Variable, -1pt 자간, Navy/Blue/Teal, 여백, 카드·타이포그래피 |
| 2 | `TEMPLATE_CATALOG.md` | **내용에 맞는** 8종 표현 방식 선택 (Concept / Process / Comparison / Step-by-step / Interactive / Architecture / Experiment / Executive Summary) |
| 3 | `templates/html/<type>.html`, `styles.css`, `reference-layout.css` | 실제 수정 가능한 HTML·SVG·CSS·JS 레이아웃 및 연산 예제. 필요한 부분만 구조적으로 재구성 |
| 4 | `previews/html-*.png`, `previews/html-*.jpg` | 시각적 품질 비교 및 검수용 스냅샷. 구현 원본이나 계산 로직을 대체하지 않음 |

**사용자가 요청한 실제 콘텐츠와 설명 목적을 우선합니다.** 사진·도표를 억지로 끼워 넣거나 기계적으로 8개 유형을 모두 채우지 않습니다.

## 새 HTML Scroll/Slide 자료 제작 순서

1. 대상 청중과 목적을 확인하고 문단·그림·수치의 의미를 먼저 설계합니다.
2. Scroll(연속 문서/목차/실습) 또는 Slide(16:9/페이지 전환/한 장 한 메시지)를 결정합니다.
3. `TEMPLATE_CATALOG.md`에서 표현 유형을 선택합니다. 한 자료에서 여러 패턴을 사용할 수 있습니다.
4. 원본 HTML에서 필요한 카드·Figure·계산 로직을 재활용하되, 실제 과제 데이터에 맞춰 코드와 레이블을 변경합니다.
5. 공통 CSS 토큰을 상속하고 스크린샷과 비교해 여백·색상·도식의 일관성을 점검합니다.
6. Chromium에서 데스크톱·모바일의 글자 넘침, 수식/차원 정합성, 실제 상호작용을 검증합니다.

## CNN 시각자료 예시: #06 → #02 → #03

- `06 Architecture`: `templates/html/assets/cnn-feature-maps.js`에서 **동일한 사과 사진**을 RGB 64×64로 리샘플링하고 고정 3×3 경계 검출 필터 + ReLU(16채널), 2×2 MaxPool(32×32×16), 후속 고정 합성곱 + ReLU(32채널), GAP(32값)을 계산합니다.
- `02 Process`: 이 공통 JS에서 추출한 대표 Feature Map 이미지를 간단히 표시합니다. #06과 **입력 이미지·특징 시각화가 대응**합니다.
- `03 Comparison`: 같은 사진을 두 방식으로 해석하는 **규칙 직접 지정 vs 학습 데이터로 특징·분류 기준 학습** 비교 구조를 사용합니다.
- **기술적 구분:** 이 스크립트는 구조를 시각화하기 위한 *미리 지정된 합성곱 가중치*를 사용합니다. 학습된 CNN의 추론 출력이나 예측 확률을 생성하지 않습니다. 따라서 고정 특징 맵을 학습 결과라고 설명하면 안 됩니다.
- Figure 코드와 배열 차원은 재사용 가능하나, 실제 자료의 모델 설정을 설명할 때에는 해당 모델의 입력 크기·커널·Stride·Padding·채널 수에 맞게 수정해야 합니다.

## 작업 범위

- 최종 결과물: **HTML Scroll / Slide**. PPTX 제작 없음.
- 8종 디자인 레퍼런스를 우선 개선하는 동안 `templates/dual-mode-learning/scroll.html`, `slides.html`, `assets/js/lesson.js`는 변경하지 않습니다.
- 외부 이미지·논문 Figure를 사용할 때는 가능한 원문 출처를 표시합니다. 자체 생성한 SVG/Canvas 다이어그램은 원본 소스와 계산 정합성을 유지합니다.
- 신규 자료 제작 시 별도 브랜치와 검증 결과를 남기고 승인 없이 `main` 병합하지 않습니다.
