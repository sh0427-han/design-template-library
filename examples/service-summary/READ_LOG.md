# 독립 제작 읽기·출처 기록

범위: /workspace/fresh-service-summary. 2026-10-31. 작업은 새 builder context에서 시작했으며 외부 디자인/계산 피드백 없이 첫 결과 보존까지 진행했다. coordinator의 진행 확인/중단 후 재개 지시만 받았다.

## 디자인 입력
- TASK.md, PROTOCOL.md, INPUT_MANIFEST.json, AGENTS.md: 범위·데이터·출처 경계·우선순위·commit 절차.
- DESIGN_SYSTEM.md: 전반 읽기 및 색/서체/행간/프레임/높이/수치 절 집중 재조회. TEMPLATE_CATALOG.md: 8종 목적·선택 기준. 긴 도구 출력 일부가 잘려 관련 절을 다시 조회했다. 잘린 출력 전체를 완독했다고 주장하지 않는다.
- docs/DOCUMENTATION_MAP.md, REFERENCE_REUSE_WORKFLOW.md, TEMPLATE_REUSE_VALIDATION.md: 정본 위치/순서/A–E/D0·D1·판정 한계.
- docs/DESIGN_COMPONENT_RECIPES.md, FIGURE_PRODUCTION_STANDARD.md, REFERENCE_REVIEW_GUIDE.md: 역할·패널·높이·실제 폰트/기하/PC4 검사.
- docs/REFERENCE_PAGE_SPECS.md: 목적 목차와 §08 상세 정규화/원래 값·단위/판단 조건.
- docs/CONCEPT_REUSE_PROMPT.md, USAGE.md, INTERACTIVE_PATTERN.md, EXPERIMENT_PATTERN.md: 제공된 범위에서 요청 예/로컬 실행/데이터 의미·재사용 검사 확인. #5/#7의 특정 분류 설정은 이 보고에 적용하지 않았다. 최종 대조 중 일부를 재확인했고 선행 설계의 기준을 새 사례로 바꾸지 않았다.
- templates/dual-mode-learning/DESIGN.md, MODES.md: 하나의 콘텐츠, 보기별 외부 배율, 한 장 해시/왕복/로딩 상태.
- templates/html/styles.css, reference-layout.css: 실제 로컬 폰트/토큰/프레임 구현.
- templates/html/executive-summary.html: 전체 소스 상세 검토; 3그룹 정규화·원래 값·실행항목 구조 선택.
- templates/html/{concept,process,comparison,step-by-step,interactive,architecture,experiment}.html: source 구조·제목/라벨·카드/그림 역할을 검색해 개관. 각각 전체 코드를 새 주제로 실행/검증한 것은 아니다. 8종의 목적은 카탈로그와 함께 비교했다.
- previews/html-concept.png, html-process.png, html-comparison.png, html-step-by-step.jpg, html-interactive.jpg, html-architecture.jpg, html-experiment.jpg, html-executive-summary.jpg: 8개 모두 view_image로 열어 직접 시각 검토했다. 스크린샷을 보고서의 원본/배경으로 사용하지 않았다.

입력 파일별 해시는 INPUT_MANIFEST의 provided_sha256과 재검증. source_sha256과 다르게 제공된 검증 이력 두 절은 복원하거나 읽지 않았다.

## 차단/미열람
공통 문서에 링크된 다른 examples(로지스틱/경사하강법/과적합), 원격 GitHub/PR/이전 대화, 제공되지 않은 docs/DUAL_MODE_REFERENCE_REUSE.md, release/status/audit, 공통 scripts 및 review 증거를 열지 않았다. 문서 자체의 설명용 예는 프로토콜이 허용한 범위로만 읽었다. 이 링크들은 제공목록 밖이라 접근하지 않는다는 결정을 D0에 기록했다. 다른 workspace/tmp 프로젝트 조회 없음.

## 기술·환경 출처 (디자인 출처와 구분)
- cloud-environment-runtime SKILL.md와 environment_status: 사용 가능한 관리 환경/네트워크 상태 점검. 이것을 디자인 규칙으로 사용하지 않았다. 외부 네트워크 조회/설치 없음.
- 설치된 Python playwright, /usr/bin/chromium, PIL 가용성 확인. 실제 렌더는 로컬 HTTP. `file://` 진단 시도는 Chromium 관리정책 ERR_BLOCKED_BY_ADMINISTRATOR로 차단되어 로컬 HTTP로 전환했다. 파일 권한 우회/네트워크 정책 변경 없음.
- 계산: TASK의 원시 숫자와 Python fractions.Fraction. 브라우저 JS 구현과 독립. 백분위수는 관측값 분포의95% 지점을 뜻한다는 기본 수학 지식 사용; 실측 분포/백분위 알고리즘/통계 검정 자료를 얻었다고 주장하지 않는다.
- 최종 산출 캡처8장 및 자체 실패 캡처를 직접 시각검토했다. 첫 결과 보존 전 외부 교정0건.

규칙 밖 디자인 열람은 없었다. 호스트 공유 환경이며 OS 보안 격리 증명은 아니다.
