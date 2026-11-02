# 2단계 · 공통 Markdown 역할 및 의미 보존 감사

## 기준과 범위

- 확인일: 2026-10-29 (한국 시간). 1단계 [REUSE_COVERAGE](REUSE_COVERAGE.md)의 분석 기준을 계승합니다.
- 분석 main: `b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442`.
- 작업 시작점: 1단계 `bfeb7c6cb19a0373f6d4d1a8d54647988c79eebc`, `docs/reuse-coverage`, [PR #25](https://github.com/sh0427-han/design-template-library/pull/25) OPEN. 이번 브랜치는 그 위의 `docs/document-contracts`이며 PR base도 `docs/reuse-coverage`입니다.
- [PR #24](https://github.com/sh0427-han/design-template-library/pull/24): OPEN, 미병합, head `c6c922847656cc883aaf1114ff7b67b0c05ced57`. 범용 Interactive D01 보완은 이번 정본에 합치지 않습니다.
- HTML/CSS/JS, 예제 DESIGN/VALIDATION, 화면, 실행 결과, 과거 승인 JSON은 수정하지 않습니다. 기존 규칙 원문을 보존하고 문서 입구에 역할/정본 링크를 추가합니다.

## 변경 전후 대응표

공통 규칙의 위치는 [문서 지도 R01–R19](DOCUMENTATION_MAP.md#규칙군별-찾기-표)에 대응합니다. 아래 '본문 동일'은 역할 배너를 제거하면 기준 커밋 파일과 **바이트 단위 동일**하다는 뜻입니다. 행 단위 상세 삽입 문자열은 [migration manifest](document-role-migration.json)에서 확인합니다.

| 변경 전 문서 | 변경 후 역할/참조 | 원문 보존·대응 |
| --- | --- | --- |
| README | 문서 지도로 연결하는 입구 | 본문 동일 |
| DESIGN_SYSTEM | 공통 디자인 정본 (R02–R07) | 본문 동일; 강제값·기본값·예제값 설명을 지도에서 구분 |
| TEMPLATE_CATALOG | 선택 지도, 원본 요약 | 본문 동일; 수치의 새 주제 강제 적용 방지 |
| DESIGN_COMPONENT_RECIPES | 패턴 계약·시작값 (R08–R10) | 본문 동일; 측정표·계약·역사 절 역할 구분 |
| FIGURE_PRODUCTION_STANDARD | 기하·기술 정확성 (R11–R13) | 본문 동일; §13 다중 DOM/Scroll 고유 검사 보존 |
| REFERENCE_PAGE_SPECS | 원본 8종 재구현 (R14) | 본문 동일; 공통 규칙과 예제 데이터 분리 |
| INTERACTIVE_PATTERN | #5 분류 예제 상세 (R15) | 본문 동일; 미병합 #24와 원본 폰트 범위 표시 |
| EXPERIMENT_PATTERN | #7 분류 지표 상세 (R15) | 본문 동일; 원본 서체와 신규 수식 범위 표시 |
| REFERENCE_REUSE_WORKFLOW | 제작 순서 (R16) | 본문 동일; 체크리스트 반복은 절차상 참조 |
| REFERENCE_REVIEW_GUIDE | 검사·명령·PC4·보고 (R17) | 본문 동일; 공통 명령 정본 지정 |
| TEMPLATE_REUSE_VALIDATION | D0/D1·증거 분류 (R18) | 본문 동일; 사례 교훈과 현재 규칙 구분 |
| CONCEPT_REUSE_PROMPT | 정본을 호출하는 요청문 | 본문 동일; 별도 규칙 정의 문서가 아님 |
| REFERENCE_RELEASE_STATUS | 시점별 상태·승인 이력 | 본문 동일; 신규 승인으로 승계 금지 |
| DUAL_MODE_REFERENCE_REUSE | 구현·검증 사례 | 본문 동일; 모드 계약 R19로 연결 |
| USAGE | 빠른 실행 안내 | 역할 배너 + 아래의 유일한 본문 중복 제거 |

**USAGE의 유일한 본문 변경:** 설치 명령 2개는 유지합니다. `check_sources`, `verify_character_spacing`, `validate_references`, `check_interactive`, `verify_pretendard`, `check_documentation` 6개 실행 명령을 삭제하고 동일한 명령이 있는 REFERENCE_REVIEW_GUIDE의 '필수 PC 화면' 절 링크로 대체했습니다. 검사 의무·순서·명령 내용은 변경하지 않았습니다.

AGENTS, MODES, 예제 DESIGN/VALIDATION, 날짜별 보고서·CHANGELOG·커버리지 원문은 변경하지 않았습니다. 역사 문서를 정본처럼 다시 쓰지 않고 지도에서 역할을 구분합니다. 여러 위치의 체크리스트는 현장에서 필요한 확인용 반복이므로 전부 삭제하지 않았습니다. 정본 링크를 가진 적용 요약으로 유지합니다.

## 모순·중복·범위 혼동 판정

| ID | 근거·겉보기 문제 | 판정 | 해결 및 남은 범위 |
| --- | --- | --- | --- |
| A01 | #5/#7 상세 폰트 절은 수식도 Pretendard, DESIGN_SYSTEM '본문과 수식의 서체 분리'는 새/수정 수식 STIX/MathML | 원본 보존과 신규 제작의 적용 범위 차이. 같은 대상의 실제 충돌로 집계하지 않음 | 역할 배너에서 원본 범위를 명시. 신규 수식은 공통 서체 절을 참조. 원본 일괄 변경 없음 |
| A02 | 과거 결과 48 cases/6화면, 새 자료는 PC4 | 회귀 범위와 현재 제작 범위 차이 | 지도 R17·이력 구분에 명시. 과거 검사를 삭제하거나 모바일을 신규 필수로 만들지 않음 |
| A03 | Recipes 측정 높이/원본 수치와 공통 기본값 혼재 | 숫자의 규칙 강도 혼동 | R05/R08/R14와 강도 정의로 측정값을 예제 범위에 둠. 계산 정확성은 필수 유지 |
| A04 | Figure/Review/USAGE에서 검사 명령 반복 | 중복, 모순 아님 | USAGE만 정본 링크로 대체. Figure의 고유 검사는 보존 |
| A05 | 여러 문서의 색·폰트·용어·정렬 체크리스트 반복 | 적용 요약과 정의의 역할 혼동 | 정의는 DESIGN_SYSTEM, 검사는 Review, 기하는 Figure. 원문 삭제 없이 정본 지도/역할 링크 추가 |
| A06 | #5 분류 계약과 #24 범용 Interactive 제안 | 미병합 제안과 현재 원본 범위 차이 | #24 미채택. 일반화된 계약의 정식 반영은 해당 PR에서 처리 |
| A07 | Concept 원본은 실제 RGB 예제, 신규 개념 장은 일반 관계 중심 | 원본 패턴 보존과 새 수업 구성의 범위 차이 | R02/R14에 적용 대상을 표시. 원본을 바꾸거나 모든 개념 장에 수치 허용으로 해석하지 않음 |

조사한 기준에서 **동일 적용 대상·동일 조건의 상반된 의무로 확정한 모순은 0건**입니다. 위 7건은 범위 명료화/중복입니다. **신규 디자인 규칙 0건**, 삭제한 디자인 규칙 0건, 실제 명령 중복 제거 1곳입니다. 문서 분류와 링크 추가를 새 디자인 계약으로 집계하지 않습니다.

## 검증과 한계

- `python scripts/check_document_roles.py`: manifest의 15개 파일을 기준 커밋과 비교. 14개는 배너만 추가, USAGE 1개는 명시한 명령→링크 치환만 허용합니다. 정본에 원래 6개 명령이 그대로 있는지도 검사합니다.
- `python scripts/check_documentation.py`: 기존 로컬 문서 링크·원본/프리뷰 해시·승인 문서 본문·역사 보존 검사를 유지합니다. 새 배너만 정확히 제거한 본문의 기존 승인 해시를 검사합니다. 과거 승인 JSON은 수정하지 않았고 이번 배너가 과거에 승인되었다고 주장하지 않습니다.
- 변경된 문서의 로컬 링크·앵커 검사와 `git diff --check`도 실행합니다. 외부 URL의 접근 가능성이나 모든 과거 Markdown의 앵커까지 새로 보장하지 않습니다.
- 이번 문서 수정으로 Chromium을 재실행하지 않습니다. HTML/CSS/JS/프리뷰는 기준과 동일하며 과거 렌더 기록을 신규 검증으로 집계하지 않습니다.
- 독립 Reviewer의 의미 보존·탐색 검토와 실제 명령 결과는 [검토 기록](reviews/document-contracts-review.md)에 남깁니다. 독립 문서 리뷰는 새 제작자의 처음부터 제작 시험이 아닙니다.
