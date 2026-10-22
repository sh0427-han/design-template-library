# 프리뷰와 검증 증거

## 현재 최종 소스 검증

- [reference-validation.json](reference-validation.json): 8종×6개 화면의 기술·실제 폰트·기하 검사, 렌더링 소스 SHA-256.
- [interactive-validation.json](interactive-validation.json): #5 전체 임계값·변경 데이터 재사용·입력 조작·폰트 예외·오프라인 공유본.
- [interactive-live.html](interactive-live.html): 현재 #5 원본에서 생성한 CSS·JS·폰트 내장 HTML.
- 유형별 호환 명령은 선택 검증 JSON을 생성할 수 있으며 전체 통과 기록을 대체하지 않습니다.

대표 프리뷰는 아래 링크입니다. 현재 캡처는 1600×950 창에서 `.slide`를 1440×810 크기로 촬영합니다. 다른 5개 화면의 PNG는 `python scripts/validate_references.py` 실행 시 기본 `/tmp/reference-integration-review`에 저장되고 CI artifact로 업로드됩니다.

| 유형 | 현재 대표 프리뷰 |
| --- | --- |
| 01 Concept | [PNG](../html-concept.png) |
| 02 Process | [PNG](../html-process.png) |
| 03 Comparison | [PNG](../html-comparison.png) |
| 04 Step-by-Step | [JPG](../html-step-by-step.jpg) |
| 05 Interactive | [JPG](../html-interactive.jpg) |
| 06 Architecture | [JPG](../html-architecture.jpg) |
| 07 Experiment | [JPG](../html-experiment.jpg) |
| 08 Executive Summary | [JPG](../html-executive-summary.jpg) |

## 과거 자료와 구분

`before/`와 기존 `validation.json`은 2026-10-21 당시 비교용 스냅샷입니다. 현재 main의 최종 구현을 설명하는 자료로 사용하지 않습니다. 과거 before와 현재 이미지는 폰트·캡처 시점이 달라 동일 조건의 단일 변경 비교라고 주장할 수 없습니다.

현재 데이터·공식·예제의 범위는 [페이지 명세](../../docs/REFERENCE_PAGE_SPECS.md), 원격 반영 상태는 [통합 보고서](../../docs/INTEGRATION_REPORT_2026-10-22.md)를 확인합니다. 프리뷰는 편집 원본의 대체물이 아닙니다.
