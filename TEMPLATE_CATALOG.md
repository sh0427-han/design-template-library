# Design Template Catalog · 8 Reference Types

**2026-10-21 Concept / Architecture 개선:** Concept은 별도 사진 프레임을 제거하고, 기존 실사형 사과 사진을 80×80 RGB로 리샘플링하여 선택 영역의 **실제 4×4 픽셀값**을 Canvas에서 읽어 표시합니다. 선택 셀의 RGB·HEX·채널 막대는 동일한 픽셀 데이터에 연결됩니다. Architecture는 Input → Conv16 → MaxPool → Conv32 → GAP32 → Linear3의 Tensor Shape를 시각적 Feature Map·Vector 변화로 표현하고, 하단에는 3개의 간결한 기술 설명만 배치했습니다. Chromium에서 **1500×950 / 1366×768 / 1280×720 / 390×844 (두 페이지 × 네 해상도)**를 검증했고 [검증 JSON](previews/review/concept-architecture-validation.json)과 두 HTML 프리뷰를 갱신했습니다. 다른 여섯 레퍼런스·CNN Scroll/Slide·PPTX는 유지했습니다.

**2026-10-21 검토 상태:** 8종 HTML 브라우저 검증 완료 · 05 문장 단위 줄바꿈 및 공통 어절 보호 반영 · 디자인 승인 대기. [유형별 결과](docs/REFERENCE_REVIEW_2026-10-21.md) · [Before / After](previews/review/README.md)

공통 디자인 시스템은 `DESIGN_SYSTEM.md`에서 관리합니다. 각 유형은 **한 장으로도 의도를 확인할 수 있는 독립 디자인 레퍼런스**입니다. 5장 CNN 예제는 별도의 연속 강의 사례입니다.

| ID | 자료 목적 | 레이아웃 패턴 | HTML · 실제 브라우저 이미지 | PPTX |
| --- | --- | --- | --- | --- |
| `concept` | 개념 소개·핵심 Figure | 실사형 입력·영역 색상 샘플·RGB 수치 | [원본](templates/html/concept.html) · ![Concept](previews/html-concept.png) | 기존 1장 |
| `process` | 단계/프로세스 설명 | Input → Process → Output | [원본](templates/html/process.html) · ![Process](previews/html-process.png) | 기존 2장 |
| `comparison` | A/B 접근법 비교 | 동일 지표의 두 패널 | [원본](templates/html/comparison.html) · ![Comparison](previews/html-comparison.png) | 기존 3장 |
| `step-by-step` | 수식·연산 강의 | 배열 × 커널 → 합계 | [원본](templates/html/step-by-step.html) · ![Step-by-step](previews/html-step-by-step.jpg) | 초안 확정 후 |
| `interactive` | 웹 실습·임계값 검증 | 슬라이더 + 계산 + 혼동행렬 | [원본](templates/html/interactive.html) · ![Interactive](previews/html-interactive.jpg) | 정적 버전 추후 |
| `architecture` | 모델·시스템 구조 | 논문형 Feature Map Stack·Tensor Shape | [원본](templates/html/architecture.html) · ![Architecture](previews/html-architecture.jpg) | 초안 확정 후 |
| `experiment` | 연구 결과·지표 비교 | Confusion Matrix + Metrics | [원본](templates/html/experiment.html) · ![Experiment](previews/html-experiment.jpg) | 초안 확정 후 |
| `executive-summary` | 경영·기술 보고 | KPI + 비교 + Action | [원본](templates/html/executive-summary.html) · ![Executive Summary](previews/html-executive-summary.jpg) | 초안 확정 후 |

## 유형별 적용 기준

- **Concept**: 직관적인 하나의 개념과 Figure를 나란히 배치합니다.
- **Process**: 실제 처리 순서와 화살표 방향이 일치해야 합니다.
- **Comparison**: 동일한 질문·측정 조건으로 비교합니다.
- **Step-by-step**: 계산식과 입력값, 결과가 실제로 일치해야 합니다.
- **Interactive**: 조작할 수 있는 변수와 화면에 표시하는 계산이 일치해야 합니다. 계산 예시는 정적 이미지로 대체하지 않습니다.
- **Architecture**: 각 텐서의 H/W/C와 stride·padding 관계를 확인합니다.
- **Experiment**: 수치 예시는 실제 실험 데이터와 구분합니다. 가상 12개 샘플로 TN=5, FP=1, FN=2, TP=4를 사용했습니다.
- **Executive Summary**: 개선 수치가 가상인 경우 명시하며, 숫자보다 의사결정 메시지를 우선합니다.

## 공통 규칙

- 네이비/블루/틸, Off-white/White 배경, 전체 글자 간격 `-1pt`.
- 16:9 슬라이드, 간결한 제목, 의미 있는 도식, 과도한 메타 문구 금지.
- HTML은 `templates/html/styles.css`를 공통 사용합니다. 기본 유형 스타일은 `reference-types.css`, 8종 전용 공통 프레임·세부 조정은 `reference-layout.css`에 작성합니다. 재사용할 때 HTML이 참조하는 CSS 파일을 함께 복사합니다.
- 모든 유형은 **수정 중인 레퍼런스 초안**이며, 기존 3종 PPTX 원본은 유지합니다.

## 연속 강의·웹 교과서

[Dual-mode Learning](templates/dual-mode-learning/)은 **위 8가지 유형의 수가 아닌 별도 통합 사용 사례**입니다.

| 모드 | 예제 | 규칙 |
| --- | --- | --- |
| Scroll | [CNN 웹 교과서](templates/dual-mode-learning/scroll.html) | 왼쪽 목차·세로 스크롤·상세 설명 |
| Slide | [CNN 발표 예제](templates/dual-mode-learning/slides.html) | 16:9 · 5장 · 키보드 전환 |

디자인 초안의 평가 방법은 [REFERENCE_REVIEW_GUIDE.md](docs/REFERENCE_REVIEW_GUIDE.md)를 참고합니다.

