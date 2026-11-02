# 4단계 · RAG 재사용 보완과 변형 조건 검증

## 세 가지 판정을 분리한다

| 판정 대상 | 결과 |
| --- | --- |
| 최초 공통 문서의 충분성 | 선택한 흐름·준비/사용·구조 패널 조합에는 충분. 공통 누락/모순과 규칙 탐색 실패는 입증되지 않음. #6 전체/8종 전체 충분성으로 확대하지 않음 |
| 이번 보완 | 예제 전용 제목 병렬 배치 class, 두 줄 노드 설명의 박스/화살표 재배치 시험, 분량 초과 거부 조건, 검증 코드의 기대값·측정 단위 오류 수정. 공통 규칙 추가0 |
| 현재 결과 | 6개 상태×PC4×2모드=48개 기대 결과 일치. 수용32개, 의도한 거부16개. 거부를 화면 통과로 집계하지 않음 |

기준은 PR #27 head `f368f77b11834c446cde9a69d3b355fdf7fdf48f`이며 main 병합 기준이 아닙니다. [첫 독립 리뷰](../fresh-builder-trial/review-first/REVIEW.md)와 [후속 리뷰](../fresh-builder-trial/review-final/REVIEW.md)를 읽고 범위를 정했습니다. 3단계 첫 결과09e824a, 최초 PASS, 선택적 검색 방식 문구 보완, 검증기 이식성 오류 기록을 그대로 보존합니다.

## A–E 원인·출처·처리

| ID / 분류 | 문제 또는 판단·원인 | 출처 | 처리 |
| --- | --- | --- | --- |
| A01 · 명시된 규칙 | 실제 글꼴·자간·위계·역할색·높이와 정렬 확인 | [DESIGN_SYSTEM](../../DESIGN_SYSTEM.md), [Figure 표준](../FIGURE_PRODUCTION_STANDARD.md) | 그대로 적용, 실제 Chromium/CDP/경계 검사. 새 규칙 추가 아님 |
| A02 · 명시된 규칙 | 내용량 증가 시 높이 재계산·배치 변경·분량 분리 | [Recipes §3](../DESIGN_COMPONENT_RECIPES.md), Figure §12/13 | 글자를 작게 만드는 대신 지역 재배치, 과다 설명은 거부 |
| B · 소스에만 있는 공통 기준 | 필요한 규칙이 소스에만 있어 문서 보완이 필요하다는 증거 없음 | 위 정본과 예제 DESIGN 비교 | 0건. 예제 고유 수치를 B 누락으로 승격하지 않음 |
| C01 · 주제 고유 | 의미 기반 검색 범위 문구 | 3단계 첫/최종 Reviewer | 이미 #27 반영됨. 원래 PASS를 실패로 바꾸지 않음 |
| C02 · 주제 고유 | 긴 제목의 선택적 병렬 트랙, 두 줄 설명용 노드·연결선 재배치 | [전용 DESIGN](../../examples/rag-architecture/DESIGN.md), [fixture 코드](verify_variants.py) | 전용 CSS class/검증 fixture. 전용 좌표·문구는 DESIGN에 기록 |
| C03 · 주제 고유 | 설명을 과도하게 추가하면 캡션/푸터/캔버스 높이 예산 초과 | 실제 overload-reject 8조건 | 자동 축소 없이 거부. 학습 목표에 맞게 줄이거나 승인된 범위에서 분리 필요 |
| D · 누락/모순 | 반복 적용할 공통 기준의 실제 부족은 확인되지 않음 | 3단계 리뷰·현재 규칙 대조 | 공통 MD 수정0. 숫자·좌표가 전용이라는 이유로 결함 처리하지 않음 |
| E01 · 구현 오류 이력 | 검증기가 격리 환경 manifest 경로만 가정 | 3단계 후속 Reviewer | #27에서 수정·통합 실행 완료. 이번 신규 결함으로 재집계하지 않음 |
| E02 · 이번 검증 코드 | 첫 기대값이 긴 제목은 반드시 실패한다고 잘못 가정 | 초기 시험에서 long-original 실제fit=true | 실제 기존 배치의 충분성을 보존하고 기대값 수정. 제목을 더 늘려 억지 실패를 만들지 않음 |
| E03 · 이번 검증 코드 | zoom된 높이를 원래 line-height로 나눠 줄 수가 축소 배율에 좌우됨 | 독립 Reviewer 초기 지적·실제 측정 | 높이를 scale로 되돌린 뒤 줄 수 계산. 제목/정의 상호 비겹침 검사도 추가 |

문서에 있는 규칙을 못 찾아 잘못 구현했다는 사례는 이번 범위에서 관찰되지 않았습니다. 따라서 위치/표현을 임의로 옮기지 않았습니다. 예제 VALIDATION/README에는 기존 정본과 새 검증 결과를 연결해 현재 결과와 과거 기록의 탐색 경계를 명시했습니다. 이는 신규 디자인 규칙이 아닙니다.

## 제한된 변형과 결과

정확한 텍스트·좌표·노드 높이는 [전용 DESIGN](../../examples/rag-architecture/DESIGN.md)에 있습니다. 변형은 브라우저에서 해당 원본에 주입하는 시험 자료이며 실제 사용자 페이지에 별도 메뉴/장/자동 엔진을 추가하지 않았습니다.

| 상태 | 각 PC4×2 결과 | 의미 |
| --- | --- | --- |
| baseline | 8/8 수용 | 기존 기본 페이지 회귀 |
| long-original | 8/8 수용 | 시험한 긴 제목은 원래 전체 폭에서도 들어감 |
| long-reflow | 8/8 수용 | 제목/정의를 병렬 배치한 선택적 대안. 위 사례를 고치는 데 필수는 아님 |
| description-original | 8/8 거부 검출 | 기존 박스에 두 번째 설명 줄만 추가하면 텍스트가 박스를 벗어남 |
| description-reflow | 8/8 수용 | 준비 단계 박스 높이와 연결선을 함께 재배치. 글자 크기 동일 |
| overload-reject | 8/8 거부 검출 | 한 장을 초과하는 설명량은 분량 편집/다른 배치/범위 분리 대상 |

기존 Slide의 창 크기별 비례 배율은 유지하되 내용량에 따른 추가 zoom/font-size 축소는 하지 않았습니다. 분량이 많다고 Figure나 필수 정의를 숨기거나 잘라내지 않습니다. 지원하는 문자열 길이의 보편적 최대값을 발견했다고 주장하지 않습니다. 제목과 설명 증가의 조합, 단계 수 변화, 다른 콘텐츠/언어/브라우저는 미검증입니다.

첫 두 줄 배치 시도에서는 기존 높이 안의 기준선만 옮겨 상단 패딩이 부족했습니다. 최종안은 노드 전체 높이를 늘리고 해당 준비 행과 연결선을 함께 조정했습니다. 이 중간 시도는 전용 좌표 가설의 검증·수정이며 공통 지침 누락이 아닙니다.

## 실제 증거와 실행

- [48개 상태 결과](evidence/validation.json), [변형 검사](verify_variants.py)
- [긴 제목 재배치 화면](evidence/long-reflow-slides.png), [두 줄 설명 재배치 화면](evidence/description-reflow-slides.png)
- [기존 배치의 두 줄 설명 실패 화면](evidence/description-original-slides.png), [분량 초과 화면](evidence/overload-reject-slides.png)
- [독립 Reviewer 보고서](review/REVIEW.md): 현재 baseline8/8, 독립 변형40/40 기대 결과 일치. 독립 화면18개 직접 열람, 지원 fixture의 차단 결함0. 첫/최종 3단계 Reviewer 폴더는 변경하지 않았습니다.
- [증거 해시](EVIDENCE.json)는 현재 runtime·fixture 코드·실제 캡처·JSON을 연결합니다. 기록을 수정하면 check_results.py가 실패합니다.

```bash
python docs/rag-hardening/verify_variants.py
python docs/rag-hardening/review/audit.py
python docs/rag-hardening/review/variants.py
python docs/rag-hardening/check_results.py
python scripts/check_documentation.py
python scripts/check_sources.py
python scripts/verify_character_spacing.py
python templates/dual-mode-learning/tools/check.py
```

과거 `docs/fresh-builder-trial/check_evidence.py`는 PR #27의 고정 소스 해시 검사입니다. 현재 CSS 대안을 과거 해시에 억지로 맞추지 않습니다. 이번에는 f368f77 worktree에서 그 검사와 check_inputs.py를 실행해 과거 증거 무결성을 확인했고, 현재 baseline/변형은 새 Chromium 증거로 검증했습니다. 기존8종 HTML/CSS/JS와 공통 Markdown은 변경하지 않았습니다. 원본8종 전체 Chromium 재렌더는 이번 범위에서 재실행하지 않았으며, 정적 검사·기존 원본/프리뷰 해시와 현재 RAG의 실제 브라우저 회귀를 구분합니다.
