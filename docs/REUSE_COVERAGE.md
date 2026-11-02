# 재사용 검증 범위와 v1.0 완료 기준 초안

## 감사 기준 · 2026-10-29 (한국 시간)

이 문서는 기존 기록을 조사한 커버리지 감사다. 이번 작업에서 예제·디자인 규칙을 변경하거나 Chromium을 새로 실행하지 않았다. 아래 통과 수치는 연결된 실행/리뷰 기록의 범위이며 이번 감사의 신규 실행 수가 아니다.

- 원격 최신 main 및 분석 worktree: `b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442`. PR #23 병합 커밋이다.
- 감사 시작 시 Open PR은 [#24](https://github.com/sh0427-han/design-template-library/pull/24) 하나. 상태 OPEN, mergedAt/mergeCommit 없음. 분석 head `c6c922847656cc883aaf1114ff7b67b0c05ced57`, 브랜치 `feat/interactive-generalization-validation`.
- #24의 실제 기능 검증 커밋은 `cbf2ec93ac4921c484e56c5900cb013300b7c7c8`. 최종 head는 문서/검토 증거 마감과 구분한다. 조회 당시 head의 statusCheckRollup은 빈 배열이므로 head 자체 CI 성공으로 읽지 않는다.
- #24의 코드·문서 보완·Reviewer 결과는 **미병합 후보 증거**다. main 지원 범위에 자동 포함하거나 이번 감사에서 병합하지 않는다.
- PR #20→#21→#22→#23의 병합 SHA는 각각 `878b9f0fe75723bb74f0a2180fdf6dfb7effd437`, `ba7fb1e1f4c5fd851da796e0b321925382b042b2`, `ef9783e910f07a5e2c9343da17573e1a7cf30225`, 위 main이다. 병합 커밋은 보관 위치이고, 각 JSON의 실행 소스 해시/기능 커밋이 기술 검증 대상을 결정한다.

## 판정 단위

| 증거 종류 | 입증하는 것 | 입증하지 않는 것 |
| --- | --- | --- |
| 원본 회귀 통과 | 이미 존재하는 원본의 계산·폰트·배치·조작 보존 | 다른 주제를 새로 설계하는 능력 |
| 새 주제 재사용 | 특정 패턴/규칙이 명시한 새 내용·변형에 적용됨 | 선택하지 않은 패턴, 모든 데이터/조작으로의 일반화 |
| 독립 Reviewer | Builder와 분리된 검토자가 코드/화면 또는 별도 계산·브라우저로 오류를 찾고 수정 확인 | Reviewer가 문서만으로 새 자료를 처음부터 제작했다는 증거 |
| 새 제작자의 처음부터 재현 | 이전 구현·대화 없이 지정한 입력 자료로 설계→구현→검증을 수행한 별도 시험 | 제작 역할을 나눴다는 사실만으로 자동 성립하지 않음 |

수학의 독립 검산, Reviewer의 독립성, 제작자의 독립 재현은 서로 다른 축이다. Planner/Builder/Reviewer 분리도 무맥락 제작 시험의 입력 통제·인계 기록을 대신하지 않는다. **1~5차에서 새 제작자의 처음부터 재현을 완료했다는 증거는 확인하지 못했다.**

## 패턴별 커버리지

아래 R1~R5는 뒤의 고정 커밋 증거 색인을 가리킨다. 원본 8종 모두 원본 회귀 근거가 있으나 그 사실을 새 주제 재사용 열에 합산하지 않는다.

| 패턴·목적 | 새 주제에 직접 적용한 범위 | 실제 규칙·변형 검증 | 독립 검토/제작 재현 | 아직 입증하지 않은 범위 |
| --- | --- | --- | --- | --- |
| #1 Concept: 개념의 시각적 관계 | R1 로지스틱 개념 구성, R2 단일 White 패널/그림 우선/최종 캡션 | 기호의 소속·서체 분리·일반식·한 장 범위·PC/두 모드 | R1 사용자 반복 검토; R2 후속 개정 Reviewer. 새 제작 재현 없음 | 원본 RGB/동일 ROI 확대 계약 전체의 다른 자료형 전이. R1은 현대 D0/D1 절차의 사전 분리 시험이 아님 |
| #2 Process: 단계별 역할과 흐름 | R2 역할별 제목·설명 트랙의 부분 적용 | 기울기 확인→갱신→반복, 접선/갱신 방향, 짧은 연결과 설명 대응 | R2 후속 개정 Reviewer; 제작 재현 없음 | 원본 네 카드/중간 출력 연결 전체의 새로운 프로세스, 분기/합류/단계 수 변화 |
| #3 Comparison: 같은 기준으로 두 대상을 비교 | R3 과적합·일반화의 주요 패턴 | 동등 White·대응 시작선·정의/그림 소유·손실축·변경 데이터/오류. 후속 사용자 개정도 별도 검증 | R3 별도 Reviewer 여러 차수 및 실제 화면 검토; 제작 재현 없음 | 긴 비대칭 설명·3개 이상 대상·다른 분야의 비교 |
| #4 Step-by-Step: 중간 연산과 출력 위치 연결 | R5 입력 patch→9개 곱→합→출력 셀의 보조 적용, 미병합 | 다른 입력/3필터·분수/반올림·미반전 방향·행렬/화살표 정렬 | R5 Reviewer 독립 Fraction/브라우저; 제작 재현 없음 | 합성곱 밖의 단계별 계산, 가변 차원/연산 수. 같은 연산 계열의 행렬 적용을 전 분야 전이로 세지 않음 |
| #5 Interactive: 조작→상태→연관 출력 동기화 | main R4는 같은 분류 평가 분야 재구성; R5 Select 필터는 다른 연산으로 직접 전이, 미병합 | R4 Slider 404상태/분모0 등. R5 Select/Reset·고정 셀·URL/모드·실패/복구·대체 입력 | R4/R5 별도 Reviewer; 제작 재현 없음 | Toggle 및 복합 제어, 모든 실패×화면, 임계값 JS의 범용 엔진 재사용 |
| #6 Architecture: 모듈·차원·구조 관계 | 확인된 직접 새 주제 적용 없음 | 원본 CNN Shape·Flatten/FC/Softmax·배치 회귀만 | 원본 검토를 재사용 검토로 세지 않음; 제작 재현 없음 | CNN 밖의 구조, 분기·skip 연결·모듈 수/shape 변화 |
| #7 Experiment: 같은 데이터에서 근거·지표 도출 | R4 행렬/네 지표를 동일 분류 평가 도메인에서 재현 | GT/예측 분리·TP/FP/FN/TN·정밀도/재현율/F1/정확도·경계/분모0 | R4 독립 Reviewer; 제작 재현 없음 | 회귀 오차/실험 비교/불확실성 등 다른 평가 도메인 전이 |
| #8 Executive Summary: 수치 근거와 실행 판단 | R2/R3 축·단위·데이터 대응 원칙 일부만 | 곡선 좌표·같은 측정 기준·예시/실측 경계·변경 데이터 | 해당 사례 Reviewer 범위만; 제작 재현 없음 | KPI 정규화+실행 항목 전체 구조의 새 보고 주제 전이 |

R1의 패턴 연결은 개념 구성의 관찰 수준이다. 기록에 없는 정밀한 패턴별 성공률을 소급 부여하지 않는다. 사용하지 않은 패턴을 0점 실패로 평가하지 않고 미검증으로 표시한다.


### 원본 소스·화면 색인

- #1: [HTML](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/templates/html/concept.html) · [실제 프리뷰](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/html-concept.png)
- #2: [HTML](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/templates/html/process.html) · [실제 프리뷰](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/html-process.png)
- #3: [HTML](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/templates/html/comparison.html) · [실제 프리뷰](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/html-comparison.png)
- #4: [HTML](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/templates/html/step-by-step.html) · [실제 프리뷰](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/html-step-by-step.jpg)
- #5: [HTML](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/templates/html/interactive.html) · [실제 프리뷰](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/html-interactive.jpg)
- #6: [HTML](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/templates/html/architecture.html) · [실제 프리뷰](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/html-architecture.jpg)
- #7: [HTML](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/templates/html/experiment.html) · [실제 프리뷰](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/html-experiment.jpg)
- #8: [HTML](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/templates/html/executive-summary.html) · [실제 프리뷰](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/html-executive-summary.jpg)

## 사례별 증거와 버전 경계

### R1 · 로지스틱 회귀

[DESIGN](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/logistic-regression/DESIGN.md) · [공통 검증 기록 (개별 VALIDATION.md 없음)](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/docs/TEMPLATE_REUSE_VALIDATION.md) · [실제 검증 JSON](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/logistic-regression/previews/validation.json)

[대표 화면](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/logistic-regression/review/concept.png)

PR #20에 병합. 현재는 개념 한 장/PC8화면·시그모이드161점·실제 서체/기호·모드/기존 URL 검증이다. 삭제한 계산 장·부록의 과거40화면/606·404상태를 현행 한 장에 합산하지 않는다. 같은 제작자와 사용자 피드백을 가진 첫 파일럿이며 엄격한 무맥락 재현 또는 사전 D0 통제 실험으로 세지 않는다. 교훈이 공통 문서에 반영됐지만 그 모든 항목을 최초 누락 건수로 소급 집계하지 않는다.

### R2 · 경사하강법

[DESIGN](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/gradient-descent/DESIGN.md) · [VALIDATION](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/gradient-descent/VALIDATION.md) · [실제 검증 JSON](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/gradient-descent/previews/validation.json)

[대표 화면](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/gradient-descent/previews/slide.png)

PR #21 병합 이후 #22에서 그래프 폭/높이·기호 배치도 개정됐다. 최초 d27789f 설계 선행 기록과 당시 문서 누락0 판정은 역사적 사실이다. 현행 해시/화면은 main의 JSON을 따른다. 독립 미분·곡선161점/6상태·접선·갱신 방향·PC8화면·실제 서체/겹침/실패 검증. 후속233d80c 개정의 독립 Reviewer 근거는 R3의 revision-3이며 최초 제작과 분리한다.

[후속 독립 검토](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/overfitting-generalization/review/revision-3.md)

### R3 · 과적합·일반화

[DESIGN](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/overfitting-generalization/DESIGN.md) · [VALIDATION](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/overfitting-generalization/VALIDATION.md) · [실제 검증 JSON](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/overfitting-generalization/previews/validation.json)

[대표 화면](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/overfitting-generalization/previews/slide.png) · [최종 문서 감사](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/heading-review/documentation-finalization.json)

PR #22 병합. 초기 #3/#8 일부 D0/D1의 공통 부족0 판정을 최종 전체 기간의 부족0으로 확대하면 안 된다. 이후 사용자 요구에서 U2 및 D-H1/D-H2가 기록됐고, 공통 검증 문서는 누적3건으로 설명한다. 같은 규칙을 여러 파일에서 고친 파일 수와 결함 건수는 다르다. 제목/분류 라벨/소유 관계 감사72화면·184쌍은 그 계약의 적용 증거다.

초기 두 손실 곡선 구성, 중간 두 SVG 구성, 최종 왼쪽 손실 그림/오른쪽 학습→새 이미지 예측 구성을 구분한다. 이전82/164좌표·후속 수정 수치를 하나의 현행 화면 결과로 합치지 않는다. 현행 JSON은 변경 데이터/기하와8화면 결과를 포함하며 사용자 확정 시안은 ce840a68b423ae7508381dc2745e3e7e12ebd41a다. 정적 Reviewer만으로 시각 승인했던 것이 아니라 실제 캡처를 확보한 뒤 반복 검토했다.

### R4 · 분류 임계값과 성능 변화

[DESIGN](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/threshold-metrics/DESIGN.md) · [VALIDATION](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/threshold-metrics/VALIDATION.md) · [실제 검증 JSON](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/threshold-metrics/previews/validation.json)

[최종 승인/CI](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/threshold-metrics/review/final-approval.json) · [최신 정렬 Reviewer](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/threshold-metrics/review/alignment-review.json)

[개념 화면](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/threshold-metrics/previews/slides-concept.png) · [실습 화면](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/examples/threshold-metrics/previews/slides-practice.png)

PR #23 병합. 승인 runtime e3b1d3e4f6a5a7444eabebbdf7fd44f74c593313의 전용 CI40603117006 및 전체 CI40603117070 성공 기록을 최종 근거로 사용한다. 개념+실습2장, PC16화면,404임계값 상태와 별도 특수/오류 시나리오. 최신 정렬 자체8화면/Reviewer4대표화면을 별도 집계한다. 중간 정렬 수정 때404상태를 재실행하지 않았다는 이력을 최종 승인 CI와 혼동하지 않는다.

최종 평가는 일부 보완 필요: #5/#7 계약의 같은 분야 재현은 충분하지만 범용 Interactive 전이는 입증하지 못했다. GT 문구/왼쪽 정렬/범위 과장 수정은 E이며 공통 누락·모순·보완은0이다.

### R5 · 필터 선택과 출력 변화

[DESIGN](https://github.com/sh0427-han/design-template-library/blob/c6c922847656cc883aaf1114ff7b67b0c05ced57/examples/interactive-kernel/DESIGN.md) · [VALIDATION](https://github.com/sh0427-han/design-template-library/blob/c6c922847656cc883aaf1114ff7b67b0c05ced57/examples/interactive-kernel/VALIDATION.md) · [실제 검증 JSON](https://github.com/sh0427-han/design-template-library/blob/c6c922847656cc883aaf1114ff7b67b0c05ced57/examples/interactive-kernel/previews/validation.json)

[기능 CI 기록](https://github.com/sh0427-han/design-template-library/blob/c6c922847656cc883aaf1114ff7b67b0c05ced57/examples/interactive-kernel/review/final-ci.json) · [독립 Reviewer 2차](https://github.com/sh0427-han/design-template-library/blob/c6c922847656cc883aaf1114ff7b67b0c05ced57/examples/interactive-kernel/review/resume-review-round2.json) · [산술 검산](https://github.com/sh0427-han/design-template-library/blob/c6c922847656cc883aaf1114ff7b67b0c05ced57/examples/interactive-kernel/review/arithmetic-validation.json) · [실제 브라우저](https://github.com/sh0427-han/design-template-library/blob/c6c922847656cc883aaf1114ff7b67b0c05ced57/examples/interactive-kernel/review/runtime-validation.json) · [대표 화면](https://github.com/sh0427-han/design-template-library/blob/c6c922847656cc883aaf1114ff7b67b0c05ced57/examples/interactive-kernel/previews/slides.png)

#24 미병합. 기능 cbf2ec9의 전용 CI40662049712/전체 CI40662049459 성공 및 Reviewer PASS/미해결0을 확인했다. 초기 set_content 주입·폰트 미검증·Reviewer PENDING 기록은 당시 한계로 남아 있고, 최종 실제 HTTP/CDP/복구 검증이 이를 보완했다. 초안 이미지를 최종 두 모드 검증으로 세지 않는다.

PC8고유화면, 기본24필터 상태, 대체 입력12상태, 예외7종은 서로 다른 집계다. 별도 Fraction5입력×3필터=15상태/375셀과 비대칭 커널의 미반전 교차상관, 원값/표시색·분수/반올림을 검증했다. Reviewer는 별도 Fraction,8화면×3필터 및5종 fault/복구·CDP·키보드를 실행했다.

D01은 일반 Interactive 계약과 임계값 전용 로직의 경계 누락1건, 모순0건이다. TEMPLATE_CATALOG/INTERACTIVE_PATTERN/REFERENCE_REUSE_WORKFLOW 3개 파일의 보완은 모두 후보 브랜치에만 있다. 최초 문서 기준은 일부 보완 필요, 보완한 D1은 검증한 디자인/행동 계약 범위에서 충분이다. threshold JavaScript를 범용 코드로 재사용한 것이 아니며 별도 공통 Interaction Engine의 필요성은 입증되지 않았다.

## 원본 회귀와 실제 지원 범위

정본은 8종 HTML 패턴과 공통 Markdown이며 출력은 PC 웹의 Scroll/Slide 두 모드다. 일반 텍스트는 Pretendard Variable, 수학은 해당 역할의 STIX Two Math, 전역 −1pt, 편집 가능한 HTML/CSS/SVG/JS를 사용한다. 공통 프레임·간격·행간·제목 역할·수식/기호 대응·경계·폰트/로드 오류 검사가 실제 사례에 적용됐다. 모든 색/모든 콘텐츠 조합의 접근성 인증은 아니다.

[원본48화면/기술·폰트·변형 검사](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/review/reference-validation.json) · [두 모드 검사](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/review/dual-mode-validation.json) · [Interactive 경계/변경 데이터](https://github.com/sh0427-han/design-template-library/blob/b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442/previews/review/interactive-validation.json)

원본8종×6크기=48화면과 원본8종×PC4×두모드=64배치 검증은 보존 증거다. 기존900×900/390×844 검사가 있다고 새 자료의 모바일 지원을 선언하지 않는다. 새 사례 PC4는1600×950/1440×810/1366×768/1280×720이다. 보고서 생성 커밋과 실행 대상/소스 해시를 구분하며 과거 보고서를 현재 실행 결과처럼 날짜만 바꾸지 않는다.

## 다음 검증의 우선순위

| 순위 | 부족한 증거 | 권장 시험과 통과 조건 |
| --- | --- | --- |
| P0 | 새 제작자의 처음부터 재현이 전무 | 고정한8종/공통MD만 받은 별도 제작자에게 사전 합의한 새 주제를 부여. 이전 사례 소스·대화·Builder 도움을 차단/기록하고 DESIGN 선행, 질문·추가 가정·규칙 누락·구현 오류를 보존. 별도 Reviewer가 독립 계산/실제 화면을 검증. 한 성공을 모든 패턴으로 확대하지 않음 |
| P0 | #24 증거와 main 제공 범위가 다름 | 사용자 검토·별도 병합 결정 또는 보류를 확정하고 채택할 기능 SHA/문서/화면/CI를 묶음으로 고정. 이 감사는 병합 승인이 아님 |
| P1 | #6와 #8 전체 구조의 직접 전이 증거 없음 | #6은 CNN 밖의 모듈/차원/분기 관계, #8은 다른 보고 주제의 KPI 단위·정규화·근거→실행 판단을 각각 시험. 주제 수가 아니라 각 누락 계약의 검증을 목표로 함 |
| P1 | #2/#4 부분 적용, #7 같은 분야 재현에 편중 | #2 단계 수/분기·중간 산출물 변화, #4 다른 연산의 중간값 대응, #7 분류 밖의 지표/단위/분모 조건. 각 사용 패턴을 별도로 판정 |
| P2 | Interactive 조작 종류/조합의 경계 | Slider/Select 외 Toggle 또는 연동 제어가 실제 설명에 필요할 때만 채택. 고정 상태/변경 상태·키보드/URL·오류 복구를 먼저 명세. 새 UI 수를 늘리려고 엔진을 추출하지 않음 |
| P2 | 학습자 이해·접근성 사용자 증거 없음 | 초급자의 기호/흐름 오해를 관찰하고 키보드·스크린리더 실제 사용을 평가. 자동 경계 검사와 별도 결과로 기록 |

## v1.0 완료 기준 초안 · 승인 전

v1.0의 제안 명칭은 **PC HTML 디자인 레퍼런스와 제작 가이드**다. 모든 주제의 범용 자동 생성기·검증된 공통 계산 엔진·모바일 자료 제작을 지원한다고 선언하지 않는다. 아래는 완료 선언이 아닌 출시 판정 체크리스트다.

| 완료 조건 | 현재 근거/남은 결정 |
| --- | --- |
| 제공 범위 고정:8종/PC/Scroll·Slide, 역할별 서체/자간/편집 원본 | main에 근거 있음. 출시 문구에 부분 재사용과 미검증 범위를 함께 표시 |
| 릴리스 후보 SHA에서 문서·소스·프리뷰·검증 해시 일치 및 전체 회귀 성공 | 과거 고정 실행 증거 있음. 실제 v1.0 후보 SHA에서 실행/최종 확인 필요. 이번 문서 감사가 재실행을 대신하지 않음 |
| 선택 패턴별 실측 근거 색인과 실패 이력 보존 | 이 문서 초안 제공. #24 채택 여부에 따라 main/후보 증거 경계 갱신 |
| 독립 Reviewer의 중대 미해결 결함0, 수정·재검토 대상 SHA 일치 | R3~R5 등 사례별 근거 존재. 출시 묶음의 최신 판정 필요 |
| 새로운 제작자1명 이상이 통제된 입력으로 최소1개 새 과제를 처음부터 제작 | 미충족. 범위를 정해 P0 재현 시험 후 판정. 실패도 문서·실행·개념 원인으로 분리 |
| 사용자 디자인/릴리스 승인, PR 상태와 실제 main 확인 | #24는 미승인/미병합 후보로 취급. v1.0 승인도 별도 필요 |

출시를 위해8종 모두의 새 주제 전이를 무조건 추가할 필요는 없다. 대신 미검증 패턴은 '원본 회귀 확인, 타주제 전이 미검증'으로 제공한다. **8종 모두의 범용 재사용 검증 완료**라는 더 강한 명칭을 쓰려면 #6/#8 전체 구조와 #2/#4/#7 등의 빈 증거를 먼저 채워야 한다. 독립 제작 시험의 최소1회는 제한된 제작 절차의 재현 근거이지 모든 패턴의 보증이 아니다.

## 감사 방법과 한계

공통 디자인 시스템·카탈로그·컴포넌트/도식/재사용/검토 문서,8종 HTML 구조, 사례별 설계·검증·리뷰 및 JSON을 조사했다. R1 개별 VALIDATION 부재는 공통 기록으로 연결했으며 추정 파일을 만들지 않았다. 과거 사용자 대화는 근거로 소급 복원하지 않고 저장소 기록/PR 상태에 의존했다. 화면 링크는 기존 실제 캡처의 증거 위치이며 이번 감사에서 모든 과거 화면을 새로 육안 승인한 뜻이 아니다. 사용자 이해도·무맥락 제작·모든 조작/오류 조합·다른 브라우저는 기록에 없는 한 미검증이다.
