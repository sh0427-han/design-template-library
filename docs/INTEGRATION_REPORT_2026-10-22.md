# HTML 레퍼런스 최종 통합 기록 · 2026-10-22

## 상태

최종 설계·출처·검증을 [통합 PR #12](https://github.com/sh0427-han/design-template-library/pull/12)로 묶었습니다. #5·#7의 원본 브랜치와 통합 브랜치는 원격 Push를 완료했습니다. 처음 발생한 쓰기 권한 문제는 collaborator 등록 후 `push=true`로 해결됐습니다.

main 반영 여부·Merge SHA·CI 결과는 위 PR의 실제 상태와 [main 커밋 기록](https://github.com/sh0427-han/design-template-library/commits/main)을 기준으로 확인합니다. 이 보고서와 아래 8개 소스·폰트·프리뷰·명세는 같은 통합 PR에 포함됩니다.

- 저장소: `sh0427-han/design-template-library`
- 기준 main: `9ad6c458665ffd7ed83318ad20f04d68a22218f0`
- 통합 브랜치: `integration/finalize-html-references-20261022`
- 기계 판독 가능한 출처: [integration-sources.json](integration-sources.json)
- 전체 원격 브랜치·PR별 33개 커밋·변경 파일·충돌 목록: [integration-inventory.json](integration-inventory.json)
- 통합 PR 게시문: [INTEGRATION_PR.md](INTEGRATION_PR.md)
- 게시·검증·Merge·기존 PR 정리 명령: `python scripts/publish_integration.py --merge`

## 8개 페이지의 최종 선택과 main 통합 단위

| 페이지 | 선택한 출처 | 실제 통합 내용 | 검증 | main 통합 PR |
| --- | --- | --- | --- | --- |
| 01 Concept | 기존 main | 사진·선택 픽셀·RGB/HEX/HWC 유지, 공통 로컬 폰트 | 래스터 16셀·선택 RGB·막대·6화면 | #12 |
| 02 Process | PR #9 | 사진 기반 고정 필터 특징 모티프와 4단계 역할 | 독립 필터 샘플·맵 색·사진·6화면 | #12 |
| 03 Comparison | PR #9 | 같은 입력·규칙/학습·3개 비교 기준 | 사진 동일성·계산 모티프·6화면 | #12 |
| 04 Step-by-Step | PR #11 | 5×5/3×3/3×3, 9개 곱, 합 −6, 구분선 | 전체 출력 독립 계산·기호/실제 글꼴·6화면 | #12 |
| 05 Interactive | `ae26ba0`, 원본 Push 완료 | 이상 우선 그룹·범례 분리·예측·행렬·대입식·공유본 | 126 기본+42 재사용+12 폰트 예외·입력·오프라인 | #12 |
| 06 Architecture | PR #10 | 두 Conv/ReLU/Pool Block→Flatten 8192→FC→Softmax | Shape·확률·사진 1개·화살표·축·6화면 | #12 |
| 07 Experiment | `3ad7079`, 원본 Push 완료 | 승인된 TP FP / FN TN와 4개 지표·구분선 | 독립 분수·두 F1 식·정렬·6화면 | #12 |
| 08 Executive Summary | 기존 main | 기존 정상 레이아웃·KPI/단위/정규화 유지 | 변화율·막대 비율·축·기준선·6화면 | #12 |

대표 파일은 [카탈로그](../TEMPLATE_CATALOG.md)에 8개 소스·프리뷰별로 연결되어 있습니다. 이 표의 검증 근거는 [공통 JSON](../previews/review/reference-validation.json)과 [Interactive JSON](../previews/review/interactive-validation.json)입니다. 페이지별 승인 상태와 기술 검사 통과, 원격 반영 상태를 구분합니다.

## 충돌 처리

PR을 main에 순서대로 Merge하지 않았습니다. 기준 main의 별도 worktree에서 최종 파일 스냅샷을 선택하고 공통 문서·스타일·검사를 조합했습니다. 선택한 PR head를 manifest에 고정했습니다.

- PR #9의 Process·Comparison·사진 기반 특징 엔진·갤러리·재사용 규칙은 반영했습니다. 이전 Architecture는 제외했습니다.
- PR #10의 최종 Architecture와 Figure 제작 기준을 사용했습니다. 구조는 Input→Block1→Block2→Flatten→FC→Softmax입니다.
- PR #11의 기본 연산 예제를 사용했습니다. 원본 폰트에 없는 원소별 곱 기호는 같은 모양의 SVG로 바꿔 글리프 폴백을 제거했습니다. 390px 화면에서 합산식이 카드 내부 패딩에 걸쳐 보이는 문제도 줄바꿈으로 수정하고 실제 글자 경계를 검사합니다.
- #5 최종 수정본은 원격에 없었고 로컬 커밋으로 확인했습니다. 해당 소스·폰트·검사·상세 문서를 포함했습니다. Push 차단을 이유로 기존 main #5를 최종본으로 취급하지 않았습니다.
- #7 승인본도 로컬 브랜치에서 가져왔습니다.
- 예전 #4 미커밋 실험 15개 파일은 원래 작업 위치를 바꾸지 않고 `archive/step-local-experiment-20261022`의 `1e03306`으로 별도 보존했습니다. PR #11을 덮어쓰거나 main에 포함하지 않습니다. #8 사전 검토의 디자인 제안은 실제 수정으로 넣지 않았습니다.

## 공통 보강

공식 Pretendard v1.3.9 WOFF2를 공통 CSS에서 직접 로드합니다. 폰트·라이선스·출처·SHA-256을 포함하고, CSS 이름뿐 아니라 실제 렌더링 폰트를 확인합니다. 모든 텍스트의 −1pt를 검사합니다.

#6은 폰트 로딩 후 실제 SVG 텍스트 경계로 다시 중앙 정렬합니다. #2·#3의 엔진에서는 더 이상 사용하지 않는 이전 Architecture 전용 처리·출력 코드를 제거했습니다. 현재 모티프의 고정 방향성 필터·ReLU·색상은 독립 계산과 비교합니다.

#5는 모바일 마지막 강조 문구의 줄바꿈을 허용해 폭이 넓은 시스템 대체 글꼴에도 대응합니다. GitHub 실행 환경의 폰트 누락 예외 검사를 위해 실패 지점·실제 경계를 Checks API의 진단에 남기며, 이 예외 경로를 정상 Pretendard 검증과 구분합니다.

검증은 `validate_references.py` / `reference_validation.py`로 공통화했고 기존 페이지별 명령은 호환 진입점으로 남겼습니다. PR별로 preview를 자동 Commit/Push하던 워크플로는 읽기 전용 공통 CI로 정리해 브랜치 경쟁과 오래된 도식 검사를 막았습니다.

## Markdown 정리

| 문서 | 현재 역할·정리 |
| --- | --- |
| README | 목적·모드 관계·구조·실행·검증·프리뷰·문서 지도 |
| TEMPLATE_CATALOG | 8개 목적·적합한 주제·배치·데이터·주의·경로 |
| DESIGN_SYSTEM | 실제 폰트·−1pt·색·Header/Content/Footer·카드·축·반응형 |
| FIGURE_PRODUCTION_STANDARD | 15개 항목의 기획→기술→기하→검증 절차 |
| REFERENCE_PAGE_SPECS | 8개를 재구현할 데이터·식·요소·의미·삭제 금지 정보 |
| REFERENCE_REUSE_WORKFLOW / USAGE | 작업 순서·선택·복사·실행, 중복 기준은 링크로 연결 |
| INTERACTIVE_PATTERN / EXPERIMENT_PATTERN | 승인된 페이지별 상세 계약·공통 폰트/검사로 최신화 |
| REFERENCE_REVIEW_GUIDE / previews/review README | 48개 화면의 현재 증거와 과거 기록 구분 |
| CHANGELOG / 과거 검토 / dual-mode 문서 | 삭제된 출력 지침 제거·로컬 폰트와 실제 실행 루트 정정 |

이전 전체 CNN 구조 설명, 삭제된 PPTX 경로·재생성 명령, 현재 상태처럼 보이는 오래된 승인 대기 기록을 정리했습니다. 2026-10-21 자료는 역사적 검토로 명확히 구분합니다.

## 검증 명령과 증거

```bash
python scripts/check_sources.py
python scripts/verify_character_spacing.py
python scripts/validate_references.py
python scripts/check_interactive.py
python scripts/verify_pretendard.py
python templates/dual-mode-learning/tools/check.py
python scripts/check_documentation.py
```

공통 검증은 8개×6개 실제 화면, source/preview SHA-256, 한글·영문·숫자·SVG 글자 실제 폰트, 이미지와 JS 오류, 수학·기하·카드 패딩을 확인합니다. [reference-validation.json](../previews/review/reference-validation.json)의 `status`와 `cases`를 확인합니다. 최종 캡처는 실제 원본에서 생성하며 일부 화면 또는 대체 폰트의 이전 통과 결과로 완료 처리하지 않습니다.

로컬 결과는 **48/48 통과**, 모든 화면의 폴백·미표시 텍스트·자간 오류·JS/요청 오류 0개입니다. #5 기본 126·변경 데이터 42·폰트 누락 예외 12개 상태, 갤러리/두 모드 6개 화면, JavaScript 소스·inline script 11개, 정적 스타일·구조·문서 링크 검사도 통과했습니다. 1600×950·390×844 원본 캡처와 나머지 네 크기의 모음 캡처를 직접 확인했습니다. 발견한 모바일 #4 합산식 패딩 문제는 수정 후 48개를 다시 렌더링했습니다.

#5의 단일 HTML은 CSS·JS·폰트와 라이선스를 내장합니다. 관리형 Chromium의 file origin 차단 때문에 오프라인 검증은 생성된 실제 HTML 바이트를 별도 offline context에 로드하는 방식입니다. file origin 자체를 검사했다는 주장은 하지 않습니다.

## GitHub 게시와 원격 결과 확인

초기 CLI 사용자 조회는 `sh0427-han-private`, repository permissions는 `pull=true / push=false / admin=false`였고 #5 Push가 403으로 거절됐습니다. collaborator 등록 후 같은 계정으로 `push=true`를 확인하고 #5·#7·통합 브랜치를 정상 Push했습니다. 이 초기 차단은 해결됐으며 현재 미해결 문제로 취급하지 않습니다.

통합 PR은 [#12](https://github.com/sh0427-han/design-template-library/pull/12)입니다. 공통 GitHub Actions의 `validate` 성공과 최종 head 일치를 확인한 뒤 Merge합니다. 게시 명령은 다음과 같습니다.

```bash
python scripts/publish_integration.py --merge
```

이 명령은 현재 계정/권한·검증 상태·소스 해시·#5 커밋 존재를 확인한 후 #5/#7 원본 브랜치와 통합 브랜치를 정상 Push하고, 통합 PR 생성/조회·CI 확인·head 고정 Merge·main 확인을 수행합니다. Force Push는 하지 않습니다. Merge 후 PR #9/#10/#11의 head가 manifest와 같은 경우에만 통합 PR 링크를 남기고 닫습니다. 새 커밋이 있는 PR은 자동 정리하지 않습니다.

실제 PR URL·Merge commit·최종 main SHA·기존 PR 처리 결과는 게시 명령의 `/tmp/design-template-integration-publish.json`과 최종 작업 보고에 기록합니다. 저장소의 확정 Merge 기록은 다음 명령으로 다시 조회할 수 있습니다.

```bash
gh pr view 12 --repo sh0427-han/design-template-library --json url,state,mergedAt,mergeCommit,statusCheckRollup
git fetch origin main
git rev-parse origin/main
```

문서에 미래의 Merge SHA를 임의로 적지 않습니다. main 반영은 PR의 `MERGED` 상태와 통합 head의 main 포함 여부, 최종 파일 비교로 확인합니다. PR #9·#10·#11 정리도 실제 Merge 이후에만 실행합니다.
