# 문서 역할 정리 · 독립 검토 결과

- 날짜: 2026-10-29 (한국 시간).
- 대상: `docs/document-contracts`, 기준 `bfeb7c6cb19a0373f6d4d1a8d54647988c79eebc` 대비 2단계 문서/검사 변경.
- Reviewer: 제작 담당과 분리된 `/root/doc_reviewer` 에이전트. 읽기 전용으로 diff·정본 지도·감사표·manifest·검사 코드를 검토하고 별도로 명령을 실행했습니다. 이 기록은 그 결과를 제작 담당이 옮긴 것입니다.
- 최종 판정: **PASS, blocking issue 0건**. 신규 디자인 규칙 0건.

## 의미 보존과 탐색

1. 14개 문서는 역할 배너 제외 본문이 기준과 바이트 단위 동일합니다. USAGE는 6개 명령의 정본 링크 치환만 있고 명령은 목적지에 그대로 있습니다.
2. 지도 R01–R19는 공통 디자인·패턴 계약·제작·검토·예제 설계·이력의 경계를 찾을 수 있게 합니다. 역할 배너에서 지도로, 지도에서 정본으로 이동할 수 있습니다.
3. R04/R05는 −1pt·실제 폰트·토큰 적용 의무를 기본 크기·여백과 구분하며 원문의 조건을 보존합니다. 권장값을 필수로 승격하거나 필수 규칙을 낮추지 않았습니다.
4. #5/#7 원본 서체와 신규 수식 서체, legacy6과 신규 PC4, 원본 측정값과 공통 시작값의 적용 범위 구분이 타당합니다. #24는 미병합 후보로 표시되고 범용 계약은 가져오지 않았습니다.
5. Figure §13의 다중 DOM·가시 요소·Scroll 끝단 고유 검사가 유지됩니다. 역사적 승인 JSON도 변경하지 않았습니다.
6. 정규화 후에도 원문 변경은 검출되고 배너 변조는 거부됩니다. 역할 안내를 제거하는 검사가 임의 본문 변경을 숨기지 않음을 확인했습니다.

## 실행 결과

| 검사 | 결과 | 실행 주체/범위 |
| --- | --- | --- |
| `python scripts/check_document_roles.py` | PASS: 15 mappings, 2 navigation fragments | 제작 담당·독립 Reviewer |
| `python scripts/check_documentation.py` | PASS: 54 Markdown, 635 local links, 기존 소스/프리뷰/문서 본문 해시 | 제작 담당·독립 Reviewer; 이 기록 작성 전 수치이며 이후 링크 추가 없음 |
| `git diff --check` | PASS | 제작 담당·독립 Reviewer |
| `templates/`, `examples/`, `previews/` 기준 대비 diff | 0 | 제작 담당·독립 Reviewer |
| `python scripts/check_sources.py` | PASS: 23 JS sources/inline scripts, Pretendard/STIX 해시 | 제작 담당; 새 브라우저 실행 아님 |
| `python scripts/verify_character_spacing.py` | PASS | 제작 담당; 정적 선언 검사 |
| `python templates/dual-mode-learning/tools/check.py` | PASS | 제작 담당; 두 진입점·8종·공유 renderer 구조 |
| 본문 변조/배너 누락 부정 검사 | PASS: 두 경우 거부 | 제작 담당은 격리 복사본, Reviewer는 메모리상 검증 |

## 검증하지 않은 것

새 제작자가 문서만으로 처음부터 만드는 시험, Chromium 신규 렌더, 외부 URL 접근, 모든 역사 문서의 앵커는 이번 문서 리뷰의 범위 밖입니다. 1단계 커버리지의 입증 한계를 확장하지 않습니다.

PR은 미병합 #25 위에 쌓으므로 현재 main-base 전용 Actions의 자동 실행 대상이 아닙니다. CI 성공이나 main 반영으로 보고하지 않습니다. main 및 #24/#25를 병합하지 않았습니다.
