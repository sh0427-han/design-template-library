# 문서 역할과 규칙의 정본

## 제작자가 먼저 찾을 곳

이 지도는 기존 규칙의 **위치와 적용 범위**를 정리합니다. 새 디자인 규칙을 추가하지 않습니다. 분석 기준과 근거 한계는 [1단계 커버리지](REUSE_COVERAGE.md), 변경 대응·모순 검토는 [2단계 감사](DOCUMENTATION_AUDIT.md)를 참고합니다. 저장소 작업 지시인 [AGENTS](../AGENTS.md)와 사용자 요구의 우선순위는 그대로 유지합니다.

| 찾는 내용 | 정본 | 다른 문서의 역할 |
| --- | --- | --- |
| 공통 디자인·정보 위계·용어·폰트·색·행간 | [DESIGN_SYSTEM](../DESIGN_SYSTEM.md) | 체크리스트·프롬프트는 적용 여부를 확인하며 값을 재정의하지 않음 |
| 어떤 패턴을 선택할까 | [TEMPLATE_CATALOG](../TEMPLATE_CATALOG.md) | 8종의 역할·링크 요약, 모든 예제를 사용하라는 뜻이 아님 |
| 패턴별 계약·컴포넌트 조합·기본값 | [DESIGN_COMPONENT_RECIPES](DESIGN_COMPONENT_RECIPES.md) | 측정 표와 계약을 구분, 예제 수치를 새 주제에 고정하지 않음 |
| Figure의 기술적 정확성·기하·화살표 | [FIGURE_PRODUCTION_STANDARD](FIGURE_PRODUCTION_STANDARD.md) | 색·서체는 DESIGN_SYSTEM, 실행 순서는 워크플로 참조 |
| 원본 8종의 정확한 수식·데이터·배치 | [REFERENCE_PAGE_SPECS](REFERENCE_PAGE_SPECS.md) | #5/#7 상세 문서는 아래 범위에서 보충 |
| #5 상태·배포본·기존 분류 예제 계약 | [INTERACTIVE_PATTERN](INTERACTIVE_PATTERN.md) | 현재 원본의 고정 GT/임계값 규칙. 미병합 #24를 자동 적용하지 않음 |
| #7 혼동행렬·Metrics 상세 구성 | [EXPERIMENT_PATTERN](EXPERIMENT_PATTERN.md) | 축·0분모·F1·정렬에 관한 해당 분류 예제 상세 계약 |
| 제작 순서와 DESIGN.md 준비 | [REFERENCE_REUSE_WORKFLOW](REFERENCE_REUSE_WORKFLOW.md) | [USAGE](USAGE.md)는 실행 입구, [프롬프트](CONCEPT_REUSE_PROMPT.md)는 요청용 |
| Scroll/Slide의 콘텐츠·탐색 계약 | [MODES](../templates/dual-mode-learning/MODES.md) | [dual-mode DESIGN](../templates/dual-mode-learning/DESIGN.md)은 구현 설계, [재사용 기록](DUAL_MODE_REFERENCE_REUSE.md)은 사례 |
| 검토·명령·PC 화면·보고 | [REFERENCE_REVIEW_GUIDE](REFERENCE_REVIEW_GUIDE.md) | Figure §13의 고유 DOM 검사는 보충, 테스트 수치는 실행 JSON에서 확인 |
| D0/D1·문제 분류·입증 한계 | [TEMPLATE_REUSE_VALIDATION](TEMPLATE_REUSE_VALIDATION.md) | 개별 VALIDATION은 해당 실행 결과, 커버리지는 증거의 종합 |
| 새 주제 데이터·기호·좌표·예외 | 각 `examples/<topic>/DESIGN.md` | 그 사례의 설계 정본. 공통 디자인 규칙으로 역수입하지 않음 |
| 언제 무엇을 검증·승인했는가 | 각 `VALIDATION.md`, 리뷰 기록·JSON·SHA | 현행 규칙과 분리. 과거 통과가 변경 후 검증을 대신하지 않음 |

## 규칙 강도를 읽는 방법

이 분류는 기존 문장의 의미를 설명합니다. 표에 이름이 없는 개별 조항도 원래 문장의 조건·예외를 보존합니다. 모든 수치를 필수로 승격하거나 모든 권장값을 임의 선택으로 낮추지 않습니다.

- **필수 규칙:** 기존 정본이 유지·검증·금지를 요구한 계약. 예: 편집 가능한 HTML Scroll/Slide, 전체 −1pt, 실제 폰트 로딩, 계산과 표시의 일치, 첫 등장 용어 설명, 동일 의미의 정렬, 새 개념 장의 일반 관계 중심 구성. 특정 패턴을 선택한 경우에만 적용되는 필수 계약도 있습니다.
- **권장 기본값:** 정본의 기본·시작값·우선 사용 표현. 예: 기본 Typography·간격 토큰과 프레임 배분, 짧은 인접 화살표. 기본값을 조정할 때는 기존 문서대로 이유·적용 범위·실제 검증을 기록합니다. 전역 −1pt 같은 명시적 고정 계약과 혼동하지 않습니다.
- **주제별 설계 판단:** 학습 목표에 맞는 패턴 선택, 단계 수·내용·데이터·계수·좌표, 필요한 경우 상세 장 추가, 명시된 예외의 선택. 개별 DESIGN.md에 근거를 남깁니다. 계산의 정확성 자체는 선택 사항이 아닙니다.

## 규칙군별 찾기 표

각 행은 원문을 대체하는 축약 규칙이 아니라 정본을 찾는 색인입니다. 상세 조건은 연결된 원문에서 읽습니다.

| ID | 규칙군 | 정본 안의 위치 | 강도·범위 |
| --- | --- | --- | --- |
| R01 | 출력·편집 가능성·외부 출처·사용자 범위 | [AGENTS](../AGENTS.md) Repository scope/Core rules | 필수 작업 계약 |
| R02 | 개념/선택 상세 장·기호와 설명의 역할·최소 설명 | [DESIGN_SYSTEM](../DESIGN_SYSTEM.md) 개념 설명의 기본 순서 | 새 개념 필수, 상세 장은 요청 범위 판단; 원본 8종 일괄 개편 아님 |
| R03 | 첫 용어·약어·독립 학습 단위 | DESIGN_SYSTEM 용어와 약어의 첫 등장 | 필수; 선수 지식 예외는 기록 |
| R04 | 색·제목/역할 라벨·본문과 수식 서체·자간 | DESIGN_SYSTEM 단일 토큰 / Pretendard / 본문과 수식 | 필수 적용 범위와 기본값을 원문대로 구분 |
| R05 | 행간·그룹 간격·16:9·Header/Content/Footer | DESIGN_SYSTEM 행간과 요소 사이 간격 ~ Header / Content / Footer | 토큰 사용 계약 + 권장 기본값; 글자 크기×행간은 변경 전후 값이 아님 |
| R06 | 카드·반복 정렬·높이·상태·접근성·CSS 적용 순서 | DESIGN_SYSTEM 카드와 내부 정렬 이후 해당 절 | 역할·정렬·범위 계약은 필수, 개별 높이는 설계 판단 |
| R07 | 원본 데이터/표시색/확대·단위·수식·범례 | DESIGN_SYSTEM 수치·수식·표·범례 / 원본 데이터·표시색·확대 | 필수 의미 일치 |
| R08 | 실제 측정값·8종 제목/라벨 검사 단위 | [Recipes](DESIGN_COMPONENT_RECIPES.md) §2 | 해당 원본의 검증된 값; 새 주제 공통 강제값 아님 |
| R09 | 동일 ROI, 흐름/구조, 대칭 비교 | Recipes §4 동일 데이터 / 흐름과 구조 / 대칭 비교 | 선택한 패턴의 계약; 단계·데이터는 주제 판단 |
| R10 | 행렬·계산·지표·조작·그래프·마지막 캡션 | Recipes §4 나머지 항목 및 §5 | 해당 의미의 패턴 계약. #5 분류 사례를 모든 조작에 강제하지 않음 |
| R11 | 기술 검산·도형·Tensor·중앙축·SVG bbox·이미지 | [Figure 표준](FIGURE_PRODUCTION_STANDARD.md) §1–8 | 정확성·연결은 필수, 도형 선택은 주제 판단 |
| R12 | 색·서체·문구·PC의 Figure 적용 | Figure 표준 §9–12 → DESIGN_SYSTEM | 공통 정본의 적용 설명, 별도 규칙 추가 아님 |
| R13 | 다중 DOM audit ID·가시 요소/조작부·Scroll 끝단 | Figure 표준 §13 | 해당 구조의 검증 필수; 공통 명령 링크로 대체하면 안 되는 고유 검사 |
| R14 | 원본 8종 데이터·수식·삭제 금지 정보 | [Page Specs](REFERENCE_PAGE_SPECS.md) §01–08 | 원본 재현 계약. −6·8,192·12샘플 등을 새 개념에 강제하지 않음 |
| R15 | 분류 임계값·양성/축·TP FP / FN TN·0분모·F1 | [#5](INTERACTIVE_PATTERN.md), [#7](EXPERIMENT_PATTERN.md) 상세 절 | 해당 분류 예제의 필수 계약, 원본/새 데이터 구분 |
| R16 | 제작 단계·설계 기록·변형 데이터·Git 상태 | [워크플로](REFERENCE_REUSE_WORKFLOW.md) 새 자료 / 문서와 Git 작업 | 절차 계약, 실행과 승인과 병합을 구분 |
| R17 | PC4·실제 폰트·검사·보고 | [검토 가이드](REFERENCE_REVIEW_GUIDE.md) 필수 PC 화면 / 결과 보고 | 현재 신규 제작 기준; legacy6은 과거/원본 회귀 범위 |
| R18 | D0/D1·A–E 분류·독립성·미검증 보고 | [재사용 검증](TEMPLATE_REUSE_VALIDATION.md) 다음 라운드 이후 | 검증 절차 계약; 예제 합격≠새 제작자 재현 |
| R19 | 두 모드 동일 콘텐츠·탐색·공통 원본 | [MODES](../templates/dual-mode-learning/MODES.md) | 모드 계약; 별도 제3 출력 만들지 않음 |

## 현행과 이력을 구분하기

- 현행: 이 브랜치가 기준으로 삼은 main의 공통 규칙과 원본 계약. 체크리스트의 반복 문장은 정본의 적용 요약이며 독립적인 수정 지점이 아닙니다. 정본과 요약을 함께 검토해 불일치를 발견하면 근거를 기록합니다.
- 원본 고유: Page Specs와 #5/#7 상세 계약. 승인된 원본의 데이터와 모양을 재현할 때 읽습니다. 새 주제에서 그대로 복사해야 한다는 뜻은 아닙니다.
- 이력: 날짜가 붙은 검토/통합 보고서, release status, CHANGELOG, `review/`, 실행 JSON, VALIDATION의 실행 결과. 공통 문서 안의 '반영한 내용', '보완한 항목', '교훈'도 출처 이력으로 읽고 연결된 현행 절을 적용합니다.
- 미병합 후보: [PR #24](https://github.com/sh0427-han/design-template-library/pull/24)의 범용 Interactive 보완. 이번 단계에 도입하지 않았습니다. [커버리지](REUSE_COVERAGE.md)의 입증 범위와 상태도 그대로 보존합니다.

규칙을 수정할 때는 위 정본을 먼저 수정하고 요약/체크리스트의 대응을 점검합니다. 역사적 실행 JSON이나 승인 해시를 최신 문서에 맞춰 덮어쓰지 않습니다. 이번 역할 안내의 무손실 확인 방법은 [감사 기록](DOCUMENTATION_AUDIT.md)에 있습니다.
