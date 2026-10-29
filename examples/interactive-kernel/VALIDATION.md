# 5차 Interactive 범용성 검증 — D0 기록

2026-10-28 (한국 시간). 이 절은 구현·공통 MD 보완 전 Planner 판단이다. 이후 구현 결과로 최초 판단을 소급 변경하지 않는다. 구현 전 DESIGN.md와 함께 별도 D0 커밋으로 보존한다.

## 기준·확인 범위

- 기준 main `b4fdef24b1c6567fd81e9ab4e9b20ad1295d8442`, 브랜치 `feat/interactive-generalization-validation`, 경로 `examples/interactive-kernel/`.
- 조정자가 실제 원격 main/Open PR을 확인했다. 4차 PR #23 병합 완료(같은 main SHA), Open PR 0. `review/baseline.json`이 실제 확인 증거다.
- Planner `/root/kernel_planner`; Builder/독립 Reviewer 분리. 구현은 D0 커밋 이후 진행한다.
- 4차 DESIGN/VALIDATION·대표 개념/실습 PNG·최종 승인/리뷰 기록과 승인 CI 성공을 검토했다. 4차는 같은 분류 평가 재구성까지만 충분하고 다른 개념의 범용성은 ‘일부 보완 필요’로 남겼다. 당시 공통 MD 누락0이라는 사실을 이번 분석으로 소급 변경하지 않는다.
- 직접 디자인/구현 원본: canonical #5 HTML/CSS/interactive-reference.js, #4 HTML의 계산/행렬/매핑. 관련 공통 MD와 카탈로그의8종 목적을 확인했다. 이전 사례의 전용 runtime은 새 원본으로 사용하지 않는다.

## D0 사전 충분성 판정

**A. 디자인 재사용성:** 프레임·글꼴·색·패널·간격·중앙 정렬·행렬/식/도형 대응·반올림/표시색·PC 검증 규칙은 이미 충분하다. 새7×7 입력·세 커널·고정 출력 좌표·색 범위·Select 배치·한 장 높이 예산은 C이며 공통 MD 결함이 아니다.

**B. 기능 재사용성:** ‘고정 입력/안정된 DOM → 하나의 계산 경로 → 관련 표시 동시 갱신 → native 키보드/status/변경 강조’는 원본/기존 MD에서 찾을 수 있다. 그러나 `interactive-reference.js`는 threshold·분류 데이터·GT/TP/FP/행렬 DOM에 결합된 IIFE다. 다른 도메인의 계산 엔진이나 공통 Select 모듈을 이미 제공하지 않는다. 주제별 순수 계산/상태/렌더 구현이 필요하며 이를 함수 이름만 바꾼 코드 복사로 대체하지 않는다.

**공통 역할 정의는 일부 보완 필요(D01 1건).** #5라는 이름/카탈로그 사용 목적은 일반 조작형 학습인데 상세 규약은 임계값 전용 계약을 ‘재사용 계약’ 전체로 제시한다. Select/Slider/Toggle 선택 기준 및 입력→상태 계산→결과 갱신→시각 피드백/해석의 일반 계약과 원본 예제 계약의 경계가 부족하다. 실습 결과를 보기 전에 발견했고 아래 세 위치에 같은 문제를 연결한다. 세 파일을 수정해도 문제3건으로 세지 않는다.

## 사전 문제·결정 추적표

| ID / 시점 | 분류 | 기존 출처·수정 전 관찰 | 보완 필요성·계획 | D0 상태 |
| --- | --- | --- | --- | --- |
| D01 / 구현 전 문서 분석 | D | INTERACTIVE_PATTERN 제목·§승인된 내용과 재사용 계약·§목적과 파일은 임계값/분류 전용. TEMPLATE_CATALOG #5는 일반 목적과 분류 배치를 함께 제시. REFERENCE_REUSE_WORKFLOW §그대로 유지할 원칙과 바꿀 내용은 #5의 고정 실제값 그룹을 범용 재사용 관계처럼 서술 | 일반 행동 계약/조작 선택 기준과 원본 임계값 구현 범위를 구분하고, 범용 엔진을 제공한다고 주장하지 않도록 보완. 같은 문제의 세 연결 문서만 수정 예정 | 신규 공통 누락1건, 모순0건. 보완 전 |
| A01 / 구현 전 | A | DESIGN_SYSTEM 프레임/폰트/색/정렬, COMPONENT_RECIPES 행렬/조작/실패, FIGURE 표준 조건/좌표/원값/색 | 새 Figure에도 그대로 적용 | 구현/브라우저 확인 예정 |
| A02 / 구현 전 | A | #5 update의 단일 계산/갱신, 안정 rows DOM, native 입력/status/reduced-motion; MD에도 명시 | 임계값 수식 대신 필터 계산을 연결하되 같은 행동 관계 검증 | 실제 module 이식과 계약 적용을 구분할 예정 |
| C01 / 구현 전 | C | 사용자 필터 Select 실습 한 장 요구.7×7 새 입력/identity·mean·Sobel-x/valid/cross-correlation/고정focus/표시색 | 새 DESIGN에 데이터·분자/분모·수학·높이 예산·상태 API 기록. 공통 MD에 전용 수치 추가 안 함 | 설계 확정, 아직 구현 안 함 |
| C02 / 구현 전 | C | 사용자는 실습을 명시했다. 공통 기본은 개념 먼저 | 실제 숫자를 쓰는 한 장 실습은 이번 범위에 한정. Select 선택은 범주형3개라는 주제 조건 | 일반 자료를 모두 실습으로 바꾸지 않음 |
| MAINT01 / 구현 전 원본 검증기 분석 | E 후보 / 검증기 유지보수 | `scripts/check_documentation.py`는 과거 승인 문서 해시를 현행 문서와 고정 비교한다. 이번에 승인된 카탈로그/Interactive 가이드 범위 확장도 실패할 수 있음 | 과거 승인 스냅샷/해시는 보존하고 이번 정당한 수정의 범위·현재 해시를 별도 추적하도록 최소 호환 보완. 계산/브라우저 검증 약화 금지 | 공통 MD 충분성 결함이나 기존 런타임 오류로 집계하지 않음 |

소스에만 있는 필수 일반 규칙 B는 현재0건이다. 원본을 읽은 뒤 발견한 모든 세부 CSS를 B로 세지 않는다. 기존 규칙을 놓친 구현 E는 아직 구현 전이라0건이며 이후 실제 발견 시 그대로 추가한다. D01의 범위 보완 후 결과를 D0에 원래 있던 규칙으로 기록하지 않는다.

## 디자인/기능 재사용 판정 방법

| 평가 | 성공 근거 | 성공으로 세지 않을 것 |
| --- | --- | --- |
| 디자인 A | 기존 토큰/폰트/소유 라벨·제목/행렬·계산 대응/입력·출력 정렬/PC 실제 화면에서 같은 품질 재현 | #5의6개 행·2카드·임계값 점선 그대로 복사 |
| 기능 B | 입력 하나에서 선택 커널·원분수 계산·25셀 출력·색·역할/status가 한 상태로 일치. 고정 입력/DOM·native focus·복원/실패 경계 검증 | threshold를kernel로 이름만 바꾼 코드, 제약 없는 공통엔진 제공 주장 |
| 문서 충분성 | D0에서 적용된 A와 이번 역할 정의 D01 보완을 분리 | 결과가 보기 좋아진 뒤 초기 누락을0건으로 변경 |

초기 결론은 임계값 예제 유지 가능, 일반 역할 명세 보완 필요, 기존 소스의 도메인 독립 JS module 제공은 입증되지 않음, 디자인/행동 계약 재사용 가능, 범용 Interaction Engine 개발 필요 근거 없음이다. 구현 및 독립 검토를 마친 뒤 D1에서 각각 다시 평가한다.

## 예정 검증과 기록 원칙

- 고유 화면은4PC크기×두 모드×한 장=8개. 필터3개 상태/다른 데이터/키보드/모드·새로고침/실패·복구 시나리오는 별도 숫자로 기록한다.
- 독립 Python 정수/Fraction으로 전체3필터와 선택 patch/products/분자/분모/원값·표시 반올림을 검산한다. 표시 소스에서 기대 답을 가져오지 않는다.
- 기본 focus 출력(3행,2열), 입력3–5행/2–4열: identity6, mean51/9≈5.67, Sobel-x28. 전체 edge에−28..28의 부호가 모두 존재하며 커널 미반전도 별도 검증한다.
- 실제 Chromium: 전체 출력 동기화·필터별 구별·native Select/focus·초기화/URL/모드 복원·대기/오류 및 DOM/SVG/MathML/실제 Pretendard/STIX/−1pt/패딩/푸터/콘솔·요청 검사.
- 기존 #5 및4차 실습을 포함해 원본8종/모든 이전 사례를 회귀 검사한다. 회귀 화면·상태 숫자를 새 자료 화면 수에 합산하지 않는다.
- 독립 Reviewer는 분류/임계값 흔적, 기술·디자인 정확성, 독립 계산, 실제 화면, 문서 충분성 판단을 검토한다. 최대3회 수정·재검토 후 미해결은 남긴다.
- D1에는 실제 문제 E/B/D·해결·재검증·개념 고유 C와 수정 공통 파일을 보완 전/후로 기록한다. main에는 병합하지 않는다.

## 미검증·제한 사항 (D0)

아직 구현/화면/시나리오/회귀/독립 Reviewer가 수행되지 않았다. 실제 청중 이해도·스크린리더 청취·모바일/태블릿·다른 브라우저·학습된 CNN 성능은 범위 밖이다. 이번 Select 실습이 통과해도 Slider/Toggle의 새로운 주제 전이, 모든8종의 새 주제 재사용, 무맥락 독립 제작자 재현, 범용 컴포넌트/공통 엔진의 제공까지 검증된 것으로 주장하지 않는다.


---

# D1 구현 결과 및 미완료 검증 (2026-10-28)

> 이 절은 D0 작성 이후의 작업 기록이다. 최초 분석·판정을 소급 변경하지 않는다. **독립 Reviewer PASS가 아직 없으며 최종 판정은 PENDING**이다.

## 구현 범위

- 동일한 `content.html`, `model.js`, `app.js`, `data.json`, `lesson.css`를 Scroll/Slide viewer에서 사용한다. 원본 8종과 4차 임계값 예제는 변경하지 않았다.
- `KernelModel`은 입력 검증, 커널별 cross-correlation, 출력 25개 원분자 및 공통 분모, 선택 3×3의 9개 원소곱, 서식/표시색을 계산한다. DOM 및 URL에 의존하지 않는 UMD 모듈이다.
- `KernelInteractive`는 상태 변경, native Select/Reset, URL/모드 동기화, aria-live 전용 알림, fetch 실패/재시도를 관리한다. `getState`는 deep clone, 허용되지 않는 `selectKernel` 호출은 `RangeError`로 실패하고 이전 유효 상태를 보존한다.
- 범주형 필터3종이므로 Select를 선택했다. 연속 수치 Slider나 이진 Toggle은 사용하지 않았다. 공통 Interaction Engine은 새로 만들지 않았다.

## D0/D1 규칙 추적

| 항목 | D0 출발점 | D1 결과 / 평가 |
| --- | --- | --- |
| A 디자인 | 8종 공통 프레임·폰트·색·소유 라벨, #4의 행렬 대응 | CSS·HTML 원칙을 구현. `set_content` 방식 Chromium 캡처를 눈으로 확인했으나 원격 Pretendard/STIX 실제 글리프 및 viewer URL 렌더는 미검증 |
| B 행동 | 한 선택으로 연관 출력 동시 갱신, native focus, 상태 알림 | 동기화/원값/URL API를 구현. 실제 코드를 재사용한 것이 아니라 행동 계약을 재현 |
| D01 문서 | #5의 임계값 계약이 범용 재사용 계약처럼 섞여 있음 | 일반 조작→상태 계산→출력 동기화→피드백 계약을 별도 표기하고 원본 임계값 전용 규칙과 분리. 공통 누락 1건 |
| C 고유 설계 | 7×7·3커널·선택 `[2][1]`, 색 구간 | D0 명세대로 구현. 공통 규칙으로 승격하지 않음 |
| E 구현 오류 | 초기 없음 | 독립 Reviewer 전 미확정. 추가 브라우저 회귀 검증 필요 |

## 실측 가능한 결과와 경계

- 독립 Python `Fraction`과 JavaScript를 비교한 3필터×25셀=**75개 셀** 결과 일치. Identity=6, Mean=51/9≈5.67, Sobel-x=28. Sobel-x 전체 −28..28 확인. 데이터는 설명용 고정 값이며 학습 모델의 출력이 아니다.
- Chromium의 `page.set_content()`에 실제 편집 HTML·CSS·JS를 주입한 **8개 뷰포트/모드 지정 샘플**에서 Select→Mean→Sobel-x→Reset과 수치/셀 업데이트를 검증했다. 기본 화면과 Mean/Sobel-x 화면을 생성해 육안 검토했다.
- 환경이 HTTP/`file://` navigation을 `ERR_BLOCKED_BY_ADMINISTRATOR`로 차단한다. 따라서 캡처는 실 URL의 Scroll/Slide viewer 실행이 아닌 **주입 기반 원본 콘텐츠 캡처**다. 프리뷰 링크에도 draft를 명시한다. 콘텐츠의 시각 배치를 확인한 것이지 모드/경로/스크립트 CDN/폰트 모두가 통과한 것은 아니다.
- 현재 로컬 검증 공간에는 정본 `templates/html/assets/fonts`가 없어 Pretendard Variable·STIX Two Math의 실제 렌더 글리프 검증은 보류한다. 공통 CSS를 상속하는지 소스상 확인할 수 있어도 글꼴 실적용으로 간주하지 않는다.
- 기존 8종·4차 예제의 소스를 이번 작업에서 수정하지 않았으나, 전체 회귀 스크립트·CI는 이 세션에서 아직 재실행하지 않았다. 특히 `scripts/check_documentation.py`의 과거 승인 해시 고정값은 합법적 변경과 구분해 처리해야 한다.
- 독립적인 Reviewer Agent/독립 세션은 실행할 수 없는 환경이므로 검토 PASS를 기록하지 않는다. `review/reviewer-status.md`에 인계 항목을 남긴다.

## 다섯 질문의 D1 잠정 답변

1. **기존 임계값 예제 유지 가능:** Yes. #5의 의미 있는 이진 분류 도메인 예제로 유지한다. 새 연산은 별도 예제로 확장한다.
2. **#5 범용 Interactive 설명 규칙:** D01의 역할 경계 보완 후 개념 설명은 충분한 방향. 실 사용·독립 리뷰 전까지 최종 판정 보류.
3. **실제 재사용 부분:** 토큰/소유 라벨/행렬 연결과 하나의 변경→계산→동기 렌더·native focus·status라는 **디자인/행동 계약**. 기존 threshold JS는 도메인 결합이 강해 실제 코드 모듈을 재사용하지 않았다.
4. **공통 규칙 구현 여부:** #5 및 #4 계약을 결합해 구현했고, 75셀 독립 계산과 콘텐츠 주입 화면은 확인했다. 정본 폰트·실 URL·회귀의 완성 확인은 별도 필요.
5. **범용 Interaction Engine 필요 여부:** 불필요. 두 도메인만으로 일반 엔진 API의 안정성/반복 이득이 아직 입증되지 않는다.

**최종 판정:** 일부 보완 필요 / PENDING independent review. D01 자체는 문서 보완안이 마련됐지만 원격 승인·전체 회귀와 독립 검토를 마쳐야 해결 완료라고 선언할 수 있다. 템플릿 v1.0 최종 검증으로 바로 넘어가는 것은 보류한다.


---

## D1 후속 검증 증거 — 실제 HTTP Chromium (2026-10-28)

기존 D1의 브라우저·폰트 미검증 기록은 당시 구현 단계의 사실로 **보존**하고, 그 이후 실행한 실 URL 검증 결과를 다음과 같이 추가한다.

- **검증 대상 소스 커밋:** `c542d30f8c74052a31ec4d6888a742643626e717` (스크립트 오류 시 reload 복구까지 포함).
- **CI:** [Validate Interactive Kernel Real-URL · run 40625146466](https://github.com/sh0427-han/design-template-library/actions/runs/40625146466) — `completed/success`.
- **검증 실행:** 로컬 HTTP 서버에서 실제 `scroll.html` 및 `slides.html`의 iframe 콘텐츠를 Chromium으로 열었다. Scroll/Slide 각각 1600×950, 1440×810, 1366×768, 1280×720 = **8개 고유 화면**. 출처 코드는 `verify_runtime.py`, 증거는 CI artifact `cnn-interactive-kernel-real-url-browser-evidence`의 PNG 8장과 `runtime-validation.json`이다.
- **수학·상태:** 3필터×출력25셀의 독립 Fraction 비교, 평균 분모9를 포함한 선택 위치 계산, Select·Reset·모드 왕복·새로고침·잘못된 URL/ID·키보드 포커스·데이터 실패와 재시도가 CI에서 PASS. 초기 브라우저 주입 검사 `verify_kernel.py`도 별도 PASS.
- **서체·레이아웃:** 실제 HTTP에서 Pretendard Variable / STIX Two Math가 `loaded`인 사실과 전체 −1pt 계산 스타일을 확인했다. 8개 화면의 브라우저 기하 검사 PASS. CI에서 받은 전체 8개 PNG를 검토용 montage로 열고 대표 1280×720 Slide 이미지도 개별적으로 확인했으며, 해당 검토 범위에서 카드·행렬·계산·Footer의 명백한 겹침·잘림이 없었다. 사용자의 최종 디자인 승인이나 별도 Reviewer PASS로 간주하지 않는다.
- **GitHub 프리뷰:** [Scroll 실제 CI](previews/scroll-real-ci.jpg) · [Slide 실제 CI](previews/slides-real-ci.jpg). 이 이미지 두 개는 **위 소스 커밋의 실제 URL Chromium 실행에서 생성된 증거**의 JPG 축소본이다. 기존 `*-draft.jpg`는 초기 주입 기반 상태를 설명하기 위해 보존한다.
- **전체 공통 회귀:** 기존 8종 통합 `Validate Final HTML References`는 이 기록 작성 시점에 최신 커밋에서 아직 종료되지 않았으므로 PASS를 주장하지 않는다. 본 사용자 요청의 독립 Reviewer는 여전히 **PENDING**이다. 재사용성 잠정 판정 **일부 보완 필요** 및 v1.0 최종 승인을 보류하는 결정은 유지한다.


## Codex 재개 — Chat 진행분 보존 및 독립 검토

[이어받기 기준](review/resume-baseline.json): 원격 PR #24의 `ab713e7`까지 fast-forward했다. D0 이후 Chat 커밋·초안 캡처·실제 URL CI와 당시 Reviewer PENDING은 이력으로 보존한다. 이전 로컬 미커밋 구현은 tar/git stash에 백업했으며 새 committed 구현을 덮어쓰지 않았다. main은 `b4fdef2` 그대로이고 이번 PR의 병합은 금지다.

새 독립 Reviewer `/root/kernel_resume_reviewer`의 [1차 기록](review/resume-review-round1.json)은 ab713e7을 고정해 **수정 필요**로 판정했다. 정상8화면/24필터, 별도 Fraction 계산, 실제 CDP Pretendard/STIX·−1pt는 통과했지만 다음 적용 누락을 발견했다.

| 항목 | 분류·심각도 / 수정 전 | 수정 내용 |
| --- | --- | --- |
| R1-01 | E·P1 콘텐츠 실패에서 영구 로딩/재시도 없음 | iframe 접근/응답 실패와 제한시간을 명시 오류로 처리하고 parent native 재시도 제공 |
| R1-02 | E·P2 D0의 가시 연산/색/기호/좌표 계약 누락 | 미반전·단일채널·교차상관 식/커널 정의·출력3행2열·원값/색±36 명시 |
| R1-03 | E·P2 화살표가 행렬 중앙보다14.5px 낮음 | matrix와 같은22/256/20px 트랙의 중앙으로 연결선 정렬 |
| R1-04 | E·P2 invalid URL 안내 시1280×720 Slide 문서높이755 | 실제 notice/bar/footer/loading 높이를 stage와 scale에서 함께 차감 |
| R1-05 | E·P2 새 분수가 일반 텍스트, 합성 bold 방지 누락 | 커널·현재분수·곱합을 MathML로 생성, 수학 서체 합성 방지 |
| R1-06 | E·P2 폰트404에서도 정상처럼 보이며 안내 없음 | fallback 상태/가시 안내와 사용 가능한 배치; 정상 CDP 검증과 분리 |
| R1-07 | E·P2 기존 QA의 실제 글리프/내부경계/다른입력/실패 검증 부족 | 독립 Fraction·CDP·안쪽 padding·SVG/Range·24필터·대체데이터·예외를 명시적으로 검증하도록 보강 |
| E-CONTRAST | E·Builder 자체 QA: 출력28의 흰 숫자 대비3.458, 다른 입력5도 낮은 대비 | 입력/출력 셀의 원값·배경 매핑은 유지하고 검정/흰색 중 최대 sRGB 대비를 선택 |

실제 Runtime 오류와 검증기 자체 오류는 구분한다. `review/verifier-corrections.json`의 V-E 항목은 자기 패널 포함 검사, fixture callback 인자, iframe URL 전파 대기, fault route 패턴과 같은 검증기 보정이며 공통 MD 누락이나 새 Runtime 결함으로 부풀리지 않는다.

[기존 사례 회귀](review/regression-validation.json)는 4차 임계값16화면/404상태와 과적합8화면의 로컬 재실행 성공을 따로 보존한다. 원본 보고서 gzip도 보존하고 생성된 기존 프리뷰/보고서는 Git 원본으로 복원했다. 원본8종/#5/로지스틱/경사하강법은 ab713e7의 전체 CI40625533308 성공 이력이 있으며 최종 수정 기능 커밋에서도 CI를 다시 확인한다.

D01은 신규 공통 누락1건/모순0건/공통 MD3개 보완이다. Chat 단계에서 추가한 일반 행동 계약을 보존하고 헤더/카탈로그에서 일반 목적과 임계값 예제 범위를 더 분명하게 표시했다. `documentation-delta.json`은3개 허용 문서의 실제 baseline 스냅샷/현재 Git blob을 검사하고 과거 승인 JSON은 bytes 그대로 보존한다. 이는 MAINT01 검증기 호환 보완이며 공통 지침 누락을 추가로 세지 않는다.

이 표는 수정 작업을 기록한 것으로 독립 재검토 완료를 뜻하지 않는다. 최종 자동 검증과 2차 독립 판정은 아래 D1 결과에서 별도로 확정한다.


후속 자동 QA의 E-FONT02: WOFF2 의도적404에서 대체 Noto의 Figure 제목 실제 글리프27px가 기존22px line box를 침범했다. `review/font-fallback-initial-failure.json`에 보존하고 fallback 상태의3개 Figure 제목만 min-height/line-height30px·중앙정렬로 보정했다. 정상 폰트와 행렬 트랙/화살표 좌표는 변경하지 않는다. 이는 새 공통 규칙 누락이 아니라 실패 상태의 기존 경계 규칙 적용 보정이다.


초기 로드 C-INIT: HTML의 bare `content.html`과 viewer의 versioned URL을 연속 탐색하면서 초기 문서의 스크립트/폰트가 취소되는 현상을 확인했다. 실제 최종 문서 로드 실패와 구분해 진단한 뒤 placeholder를 `about:blank`로 두고 versioned 콘텐츠를 한 번만 요청하도록 단순화했다. 초기 빈 프레임의 load만 무시하고 실제 응답 실패/제한시간/재시도는 그대로 검사한다. JavaScript가 없을 때는 부모 보기의 기존 noscript 안내를 제공한다. 새로운 공통 엔진이나 도메인 계산 변경이 아니다.


## D1 수정본 자동 검증 완료 (2차 독립 검토 전)

[실제 HTTP/iframe Chromium](review/runtime-validation.json): 고유 화면8개(4PC×두모드), 필터 상태24개, 대체 입력 상태12개, 예외7종을 별도로 검사해 통과했다. 실제 CDP Pretendard/STIX·−1pt, MathML/원분수·동일 source 배치·셀 식별자 유지·색/숫자 대비·패널 안쪽 padding·텍스트/SVG/화살표/푸터·Select 키보드/포커스·초기화/모드/새로고침/비정상 API·URL을 확인했다. 정상 콘솔/요청/HTTP 오류와 초기 문서 교체 취소는 모두0건이다. 폰트 실패의 대체 글꼴 사용 가능성은 정상 글리프 성공과 분리했다.

[독립 Python/Node 수학 검산](review/arithmetic-validation.json):5개 입력×3필터=15상태/375셀, 비대칭 커널로 미반전 방향 확인, 고정 signed색·클리핑7조건 및 invalid 검증을 수행했다. 기대값은 production 계산에서 만들지 않았다. 기본 입력에서 세 필터 출력은 구별되고 상수 입력에서 일부 필터의 값이 같아지는 것은 정상 결과로 처리했다.

[Viewer 복구 자체 검증](review/viewer-fix-validation.json)과 [이전 사례 회귀](review/regression-validation.json)도 별도 기록이다. 검증기 자체 보정은 Runtime 오류에 합산하지 않았고, 폰트 실패 경계의 실제 오류 E-FONT02와 초기 탐색 C-INIT은 위에 그대로 남겼다. 2차 독립 검토와 최종 CI 결과는 기능 커밋 고정 후 추가한다. 사용자 디자인 승인이나 main 병합 완료를 뜻하지 않는다.


## D1 최종 CI 확인 — 2026-10-29

기능 기준은 `cbf2ec93ac4921c484e56c5900cb013300b7c7c8`이다. [전용 CI40662049712](https://github.com/sh0427-han/design-template-library/actions/runs/40662049712)와 [전체 CI40662049459](https://github.com/sh0427-han/design-template-library/actions/runs/40662049459)가 모두 completed/success임을 GitHub API의 job/step까지 확인했다.

- 전용 CI: 독립 수학, 실제 HTTP8화면/24필터·대체입력·실패, 4차 임계값 및 과적합 회귀가 성공했다.
- 전체 CI: 원본8종·실제 폰트·6화면크기, 기존#5 경계상태, 갤러리/두모드, 로지스틱 회귀, 경사하강법, 문서링크, 제목계층 회귀가 성공했다.
- 기존 자료의 성공은 보존 증거이며, 새 필터 주제로8종을 모두 재사용 검증한 것은 아니다. 직접 검증은#5이며 #4의 행렬 표현은 보조 적용이다.
- 최종 보고서 커밋이 문서·검토 증거만 바꿀 경우 위 기능 커밋의 CI와 구분한다. 소스 SHA와 프리뷰 SHA는 실제 실행 보고서에 남긴다.

### 다섯 질문의 범위별 판정

1. **기존 임계값 예제 유지:** 가능. 분류 도메인의 Slider 예제로 보존했고 실제 동작 회귀를 통과했다.
2. **범용 설명 보완:** 필요했다. D0의 D01(일반 계약/임계값 로직 경계)1건을 공통MD3개에서 보완했다. 이미 존재한 키보드·단일상태·실패 규칙을 신규 누락으로 중복 집계하지 않았다.
3. **코드 재사용 한계:** 공통 토큰과 디자인·상태 행동 계약을 재사용했다. 기존 임계값의 계산/DOM 코드는 결합돼 있어 범용 모듈 재사용 성공으로 판정하지 않는다. 필터 계산과 렌더는 별도 구현이다.
4. **기존 규칙만으로 재현 여부:** 카드·행렬·서체·기하·수학·상호작용 원칙은 기존 규칙A와 주제값C로 재현했다. 다만 일반 역할 설명D01을 보완했으므로 최초 문서가 완전했다고 소급하지 않는다.
5. **범용 엔진 필요:** 현재 근거로 불필요. 두 도메인의 계산·표시 차이는 크며 공통 엔진을 추출할 반복 이득이 확인되지 않았다. 디자인 패턴과 동작 명세로 충분하다.

D0 평가는 **일부 보완 필요**다. D1 자동 검증은 통과했으며 최종 독립 판정은 별도 기록한다. Toggle·모바일·다른브라우저·실제 스크린리더 청취·학습된CNN성능·독자 이해도·무맥락 제작자 재현은 미검증이다. 모든 실패×모든 화면의 전수 조합도 주장하지 않는다.


## D1 독립 재검토 및 최종 판정 — 2026-10-29

새 독립 세션 `/root/kernel_final_reviewer`의 [2차 검토](review/resume-review-round2.json)는 `cbf2ec93ac4921c484e56c5900cb013300b7c7c8`에 대해 **PASS**, 미해결0건이다. 1차의 P1 1건·P2 6건은 모두 해결했다. Reviewer는 별도 hardcoded Fraction 계산과8화면×3필터,5종 별도 fault/복구, invalid URL 높이, 실제 CDP 글리프, 키보드/모드와 두 이미지를 직접 확인했다. 기존 자동 검증 결과를 다시 읽기만 한 자체 검토가 아니다. 상세 실행 범위·검증기 timeout 보정·정상 오류와 주입 fault의 구분·미검증 한계도 보고서에 남겼다.

**최종 재사용성 평가: 일부 보완 필요.** 최초 공통 Markdown만으로 일반 Interactive 역할을 명확히 설명하기에는 D01이 부족했다. 해당1건을3개 공통MD에 보완한 D1은 **검증한#5 디자인/행동 계약 범위에서 충분**하다. 기존 Slider 분류 사례와 새 Select 필터 사례를 함께 유지할 근거가 생겼지만, 범용 코드 엔진이나 모든 UI·8종 전체의 재사용 성공은 입증하지 않았다. D0 누락과 이후E 오류를 D1 성공으로 지우지 않는다.

[납품 무결성](review/delivery-validation.json)에 D0 원문 prefix, 보호 대상 source diff0, 기능 소스 해시와 집계/한계를 기록했다. [최종 CI job/step](review/final-ci.json)은 기능 커밋 기준이다. 마지막 정리 커밋은 문서와 검토증거만 변경하며, 사용자 디자인 검토를 위해 PR을 제공하고 main에는 병합하지 않는다.
