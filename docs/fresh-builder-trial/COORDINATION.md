# 새 제작자 재현 시험 · Coordinator 기록

## 사전 고정

- 날짜: 2026-10-29 (한국 시간).
- 기준 커밋: `ff689f9a63b0aa350036b12a01695c8c52c7bda8` (2단계 PR #26 head). main으로 병합된 기준이 아니다.
- main 조회: `b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442`. PR #24/#25/#26 OPEN. 이 시험에서 병합하지 않는다.
- 작업 브랜치: `validation/fresh-builder-architecture`, PR base 예정 `docs/document-contracts`.
- 선택 근거: REUSE_COVERAGE의 P0 새 제작자 시험과 P1 #6의 CNN 밖 구조 관계 전이 공백을 함께 조사한다. 대상 주제는 RAG의 문서 준비와 질문 응답. 기존 1~5차 주제와 다르다.
- Builder의 선택 자유를 보존하기 위해 TASK에는 #6 사용 지시, 배치·색·좌표·노드 수·디자인 답안을 넣지 않았다. 실제로 어떤 패턴을 선택했는지 별도로 평가하며 목표 패턴의 성공을 미리 확정하지 않는다.

## 역할과 입력 통제

- Coordinator: `/root`. 기준·내용 과제·입력 사본·결과 보존·PR 담당.
- Fresh Builder: `/root/fresh_builder_rag`, `spawn_agent(fork_turns="none")`. 부모 대화와 이전 제작 문맥을 상속하지 않은 별도 Agent context.
- Independent Reviewer: 첫 결과 보존 후 별도 Agent로 요청한다. Builder와 다른 역할·context에서 평가한다.
- Builder 입력 사본: `/workspace/fresh-builder-rag`. 이전 `examples/`, 리뷰·사용자 피드백·Git 이력을 복사하지 않았다. 제공 경로/원본 해시는 input-manifest.json에 고정했다.
- 공통 TEMPLATE_REUSE_VALIDATION의 두 과거 사례 이력 절은 입력에서 제외했다. 명시된 현재 규칙의 출처는 원본 공통 Markdown이며 별도 신규 규칙을 보충하지 않았다. 이 절차는 **전체 저장소 무제한 열람 시험이 아니라 고정 공통 문서의 현행 규칙·8종을 허용한 입력 시험**이다.
- 공통 문서에 이미 포함된 설명용 예/과거 사례 링크는 남아 있다. 미제공 링크를 따라가지 않도록 지시했다. 공통 규칙에 축적된 교훈 자체를 제거한 시험은 아니다.
- 입력 외 기술 사실 확인은 허용하며 디자인 출처와 분리한다. OS/브라우저 도구 사용은 허용한다.
- 도구와 호스트 파일시스템은 공유한다. 경로 밖 접근을 OS 수준에서 차단한 sandbox나 별도 사용자 계정은 아니다. 이전 경험은 이 저장소의 대화/산출물 입력 부재를 의미하며 모델의 일반 사전학습 경험 부재를 뜻하지 않는다. 열람 제한 준수는 Agent 로그/보고의 범위에서 평가한다.

## 교정 방화벽

Builder가 DESIGN/D0 선행 커밋, 구현·자체 검사·실제 화면 첫 결과를 보존할 때까지 Coordinator는 디자인 교정 메시지를 보내지 않는다. Builder 자체 수정은 허용하며 외부 Reviewer 수정과 구분한다. 이후 피드백과 수정 결과는 첫 커밋을 대체하지 않고 별도로 보존한다.

## 평가 기준 사전 고정

1. 과제 내용의 완결성·초급자 용어 설명·문서 준비/질문 응답의 기술적 구분.
2. 공통 문서 기반 정보 위계·색 의미·타이포그래피·정렬·가독성 재현. 픽셀/원본 레이아웃 일치율로 평가하지 않는다.
3. 실제 Chromium PC4 (1600×950, 1440×810, 1366×768, 1280×720) × Scroll/Slide, 실제 폰트·런타임·경계와 화면 직접 확인.
4. 문서 누락 / 규칙 탐색 실패 / 구현 오류 / 주제 고유 판단을 분리. 원문에 있으나 못 찾은 것은 문서 누락으로 세지 않는다.
5. 최초 무교정 결과와 수정 후 결과를 분리한다. 한 과제 성공을 8종 전체·무제한 주제·학습자 이해 실험으로 확대하지 않는다.

최종 결과와 Reviewer 인계·수정 시점은 후속 기록으로 추가한다.

## 한도 중단과 재시작 · 2026-10-30

첫 Builder 세션은 D0 설계 커밋 `170b4ef`만 남기고 종료됐다. 구현·Chromium·첫 결과 없음. 중단된 설계는 interrupted-attempt 및 Git bundle에 보존하며 재현 성공/실패로 판정하지 않는다. 이전 Agent context를 복구할 수 없어 새 Builder에 동일한 48개 입력 파일·TASK·PROTOCOL만 제공하여 처음부터 재시작한다. 이전 Builder DESIGN/D0는 제공하지 않는다. 새 경로는 `/workspace/fresh-builder-rag-rerun`이다. Reviewer도 새 context로 재생성한다. 외부 디자인 피드백은 어느 Builder에도 아직 제공하지 않았다.

재시작 입력 패키지 정정: AGENTS가 필수로 지시한 공통 모드 계약 `templates/dual-mode-learning/DESIGN.md`와 `MODES.md`가 첫 입력 사본에서 빠져 있었음을 Coordinator가 확인했다. 같은 고정 SHA의 두 Markdown을 재시작 구현 전에 추가하여 입력 50개로 정정했다. 이는 라이브러리 문서 누락이나 새 디자인 규칙이 아닌 Coordinator의 자료 포장 오류다. 중단된 시도의 48개 manifest도 별도 보존한다. 이전 Builder의 설계·판단은 재시작 Builder에게 전달하지 않는다.

## 재시작 첫 결과와 첫 독립 리뷰

- 새 Fresh Builder: `/root/fresh_builder_rag_run2`, `fork_turns="none"`; Independent Reviewer: `/root/rag_reviewer_run2`, 별도 `fork_turns="none"` context.
- 설계/D0 원본 `c0410a6e6f76edfbc61276d381a096b30ca414dc` → 작업 브랜치 `c396c6b1ca7d4778c30e44461cb7231d81cdc54b`.
- 외부 피드백 전 첫 결과 원본 `93ec54e5a4e9e71e53233aa9296e37cc68de3581` → 작업 브랜치 `09e824a6fe00abc98e70f00c26af9979d5487534`. 원본 코드·화면을 변경하지 않고 cherry-pick했다. 첫 화면8개와 소스 해시는 FIRST_SNAPSHOT.json, 원래 Git 이력은 builder-output.bundle에 보존한다.
- Builder의 인계 기록 원본 `1b23b935453f92dd870a2b1c7e206994a9075871` → 작업 브랜치 `634669422253b24637e1929b98bbc092c1bd79eb`.
- 첫 결과 보존 후 Reviewer에게 고정 SHA를 전달했다. Reviewer가 직접 화면8개를 확인하고 별도 Chromium8조건을 실행하여 PASS/차단0으로 판정했다. 구체적인 결과는 review-first/REVIEW.md와 audit.json에 있다.
- **이 시점까지 디자인 교정 피드백 0회**. 환경/패키징 정정과 진행 상태 질문만 있었다. Builder 자체 높이 조정과 브라우저 경로 수정은 첫 결과 이전 자체 검사이며 외부 교정이 아니다.
- 이후 첫 외부 피드백: RAG 전체가 의미 기반 검색만 한다고 읽히지 않도록 '의미 기반 검색의 예'라는 범위를 화면에 드러내는 선택적 보완 권고. 첫 결과는 PASS 그대로 유지하며, 새 공통 규칙 또는 소급 D0 실패로 집계하지 않는다. Builder에게 현재 시험의 Reviewer 보고서만 전달하고 문구 보완/8화면 재검증을 요청했다. 수정 후 독립 재검토는 별도 폴더에 보존한다.
