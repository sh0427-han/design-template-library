# 새 Agent 재현 시험 결과 · RAG 개념 한 장

## 결론과 범위

이전 대화를 상속하지 않은 새 Builder가 고정 공통 Markdown과 기존 8종에서 **새 주제의 한 장짜리 흐름 구성을 제작했고, 외부 디자인 교정 전 첫 결과가 독립 리뷰를 통과**했습니다. 정보 위계·색 의미·서체·정렬·기술 관계의 제한된 재현 근거입니다. 모든 8종 패턴이나 모든 새 개념의 재현 가능성을 입증한 결과는 아닙니다.

사전 목표는 커버리지 P0(새 제작자)와 P1(#6의 타주제 전이)을 함께 조사하는 것이었습니다. 실제 산출물은 #2 흐름, #3 준비/사용 구분, #6 단일 구조 패널의 일부 아이디어를 조합했습니다. **#6의 표현별 Figure·Shape·연산 트랙 전체 전이는 여전히 미검증**입니다. 과제에 디자인 답안을 주지 않았기 때문에 이 차이를 실패로 숨기거나 목표 패턴의 완전 성공으로 바꾸지 않습니다.

## 기준·과제·입력

- 기준 SHA: `ff689f9a63b0aa350036b12a01695c8c52c7bda8`, 2단계 [PR #26](https://github.com/sh0427-han/design-template-library/pull/26). main에 병합되지 않은 기준입니다.
- 사전 분석: [1단계 커버리지](../REUSE_COVERAGE.md). 그 문서는 당시 기록으로 유지하고 이 시험 결과를 소급 덮어쓰지 않았습니다.
- [과제](TASK.md): 성인 초급자, RAG의 문서 준비와 질문 응답 및 한계 이해, 개념 한 장, Scroll/Slide. 색·패턴 번호·좌표·노드 수·배치 답안 없음.
- [입력 manifest](input-manifest.json): 공통 Markdown·8종 원본/프리뷰·공통 모드 계약 50개 파일의 원본/제공 SHA-256. 과거 사례 이력 두 절을 제외한 내역을 명시했습니다. 현재 규칙에 내장된 설명용 예는 남았으며, 축적된 공통 지침까지 제거한 실험은 아닙니다.
- [프로토콜](PROTOCOL.md), [Coordinator 이력](COORDINATION.md), [Builder 열람 기록](../../examples/rag-architecture/READ_LOG.md)에 입력 제한·질문·가정·도구·출처를 남겼습니다.

`spawn_agent(fork_turns="none")`로 부모 대화 없는 Builder와 별도 Reviewer context를 실제 생성했습니다. 이전 사례의 전용 HTML/CSS/JS·DESIGN·사용자 피드백을 입력 사본에 넣지 않았습니다. 동일 호스트와 도구를 공유하므로 OS 권한으로 경로 외 열람을 차단한 시험은 아닙니다. 열람 준수는 Agent 보고와 작업 기록 범위의 증거이며, 모델의 일반 사전학습 경험 부재를 뜻하지 않습니다.

## 첫 결과와 후속 변경을 구분한 이력

| 단계 | 보존 근거 | 판정 |
| --- | --- | --- |
| 한도로 중단된 최초 시도 | [설계만 남은 시도](interrupted-attempt/D0.md), `170b4ef`, 별도 bundle | 구현·화면 없음. 성공/실패 집계 제외. 재시작 Builder에게 설계 미전달 |
| 재시작 구현 전 DESIGN/D0 | `c396c6b1ca7d4778c30e44461cb7231d81cdc54b` (Builder `c0410a6`) | 코드 구현 전 별도 커밋. 규칙 충분성·주제 판단·가정 기록 |
| 외부 교정 전 첫 구현·실제 화면8개 | `09e824a6fe00abc98e70f00c26af9979d5487534` (Builder `93ec54e`) | Builder Chromium8/8, 입력50 해시 불변. 자체 수정은 허용하되 외부 교정과 구분 |
| 첫 독립 검토 | [보고서](review-first/REVIEW.md), [별도 실행 JSON](review-first/audit.json) | 실제 Chromium8/8, 첫 화면8개 직접 확인, PASS/차단0. 패턴 범위 한계 명시 |
| 후속 선택 보완 | `9b0cd05c5ec5b0ad15fb7b9f934048e9e20425cf` (Builder `01d9995`) | 의미 기반 검색의 예임을 표시, 단어·혼합 검색 가능성 표시. 첫 PASS 유지 |
| 검증기 이식성 보완 | 같은 후속 커밋의 verify.py | 격리 입력에서는 provided 해시, 통합 저장소에서는 source 해시 선택. Coordinator가 통합 환경 Chromium8/8 확인 |
| 최종 독립 재검토 | [보고서](review-final/REVIEW.md), [실행 JSON](review-final/audit.json), [manifest 검사](review-final/manifest-check.json) | 실제 Chromium8/8 PASS. 새 문구 폰트·비겹침과 원본 해시50개 확인 |

원래 Builder 커밋은 [builder-output.bundle](builder-output.bundle)에 첫 인계 시점까지 보존했고, [FIRST_SNAPSHOT.json](FIRST_SNAPSHOT.json)은 첫 결과 파일별 해시와 원본→작업 브랜치 커밋 대응을 보존합니다. 이 bundle은 **출력 이력**이며 공통 입력을 포함한 독립 실행 패키지는 아닙니다. 첫 화면은 아래 고정 SHA 링크에서, 최종 화면은 현재 예제 경로에서 봅니다. 현재 DESIGN의 후속 부록은 원래 선행 설계를 삭제하지 않습니다.

## 문제 분류

| 분류 | 확인 내용 | 처리·해석 |
| --- | --- | --- |
| 문서 누락/모순 | 선택한 구성에서 입증된 결함 0건 | 범용 좌표/전용 RAG 답안이 없다는 이유로 결함 처리하지 않음 |
| 규칙 탐색 실패 | 제공된 현행 규칙에서 관찰된 실패 0건 | 의도적으로 제공하지 않은 과거 사례/스크립트 링크는 차단된 입력으로 기록, 규칙 부재로 집계하지 않음 |
| Coordinator 입력 포장 오류 | 공통 MODES/DESIGN 2개 누락 1건 | 재시작 D0/구현 전에 동일 SHA 원문 추가. 이전 설계 답안 제공 아님 |
| 구현 오류 E | 검증기에서 격리 폴더의 manifest 위치만 가정한 이식성 문제 1건 | 통합 저장소용 경로/해시 분기를 추가하고 실제 실행 확인. 최초 격리 환경의 8/8 결과를 취소하는 오류는 아님 |
| 주제 고유 판단 C | 2개 과정, 9개 노드, 질문 우회 연결, 문서 저장소 연결, 단일 장의 설명 밀도 | Builder가 스스로 결정. 첫 설계 높이 추정은 자체 측정 후 보정했고 이력을 남김 |
| 후속 주제 범위 명료화 C | 의미 기반 검색이라는 예시 조건 | 선택적 Reviewer 권고를 반영. 공통 규칙 추가나 소급 최초 실패 아님 |

공통 Markdown/8종 원본 수정 0개, 신규 공통 디자인 규칙 0건, 범용 엔진 생성 없음. 새 예제의 viewer·검증기는 이 한 과제의 전용 코드입니다.

## 실제 검증과 품질 판단

- 화면 조건은 PC 1600×950 / 1440×810 / 1366×768 / 1280×720 × Scroll/Slide의 **8개 고유 조합**입니다. Builder·Reviewer의 반복 실행을 서로 다른 지원 환경 수로 합산하지 않습니다.
- 로컬 Pretendard를 CDP 실제 글리프 폰트로 확인하고, −1pt·DOM/SVG 경계·화살표 연결·푸터·콘솔/요청 오류·키보드/포인터 모드 왕복·해시 복원 등을 검사했습니다.
- 구조를 보여주는 편집 가능한 HTML/SVG입니다. 준비한 문서가 검색으로 연결되고, 원래 질문과 검색된 원문이 함께 생성 모델로 들어갑니다. 검색과 재학습을 구분하며 정확성 비보장을 표시합니다.
- 최초·최종 모두 수식/실측 성능·실제 검색 시스템을 주장하지 않습니다. 기술 판정은 과제와 독립 도메인 검토에 기반하며 외부 전문가 또는 실제 RAG 서버 실험은 아닙니다.
- 최소 Slide에서 보조 설명은 축소 후 약14px 수준으로 조밀합니다. PC에서 확인한 가독성과 강의실 투사·저시력 사용자 가독성은 구분합니다. 초급자 이해도 사용자 시험은 하지 않았습니다.

## 확인할 화면과 실행 방법

- [최초 Slide · 고정 커밋](https://github.com/sh0427-han/design-template-library/blob/09e824a6fe00abc98e70f00c26af9979d5487534/examples/rag-architecture/slides-1440x810.png)
- [최종 Slide](../../examples/rag-architecture/slides-1440x810.png) · [최종 Scroll](../../examples/rag-architecture/scroll-1440x810.png)
- [편집 원본 Slide](../../examples/rag-architecture/slides.html) · [Scroll](../../examples/rag-architecture/scroll.html)

저장소 루트에서 `python -m http.server 8000` 실행 후 `/examples/rag-architecture/slides.html` 또는 `scroll.html`을 엽니다. 검증에는 Python Playwright와 현재 스크립트가 사용하는 `/usr/bin/chromium`이 필요합니다.

```bash
python docs/fresh-builder-trial/check_inputs.py
python examples/rag-architecture/verify.py
python docs/fresh-builder-trial/review-final/audit.py
python docs/fresh-builder-trial/check_evidence.py
python scripts/check_documentation.py
```

첫 Reviewer의 audit.py는 현재 checkout을 검사하므로 첫 화면을 다시 만들려면 첫 구현 커밋의 별도 worktree에서 실행해야 합니다. 현재에서 실행해 첫 증거 파일을 덮어쓰지 마세요. 과거 화면은 그대로 보존하고 최종 재검토는 별도 review-final 폴더에 남깁니다.

## 커버리지에 추가된 증거와 다음 우선순위

이번 결과는 '대화 없는 새 제작자가 통제된 입력으로 최소 한 과제를 설계→구현→검증한 사례'를 추가합니다. 반복적인 사용자 디자인 교정 없이 첫 결과가 통과했다는 근거가 생겼지만, 별도 보안 환경의 무접근 증명·모든 패턴의 전이·학습자 이해도까지 충족한 것은 아닙니다.

다음은 같은 종류의 예제를 늘리기보다 **#6의 서로 다른 표현·차원·분기 관계 전체 계약**, **#8의 KPI 단위·정규화·근거→행동 연결**, 그리고 실제 초급자 이해 확인 중 부족한 증거를 목표로 정해야 합니다. 이번 결과만으로 v1.0 출시 완료나 main 반영을 선언하지 않습니다. 미병합 #24의 계약은 이번 시험에 도입하지 않았습니다.
