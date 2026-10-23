# 프리뷰와 검증 증거

사용자 검토를 마친 8종 원본의 **현행 결과만** 보관합니다. 검토 완료 상태·소스 출처·정리 기준은 [현재 상태](../../docs/REFERENCE_RELEASE_STATUS.md), 데이터·수식은 [페이지 명세](../../docs/REFERENCE_PAGE_SPECS.md)를 확인합니다.

| 유지 파일 | 고유한 역할 | 재현 명령 |
| --- | --- | --- |
| [reference-validation.json](reference-validation.json) | 8종×6개 화면, 독립 계산·실제 폰트·정렬·오류·소스/프리뷰 SHA-256, #2 실패/재사용·#3 resize | `python scripts/validate_references.py` |
| [interactive-validation.json](interactive-validation.json) | #5 전체 임계값·변경 데이터·키보드·폰트 누락 예외·오프라인 공유본 | `python scripts/check_interactive.py` |
| [dual-mode-validation.json](dual-mode-validation.json) | 두 모드×8종×PC 4개, 원본과 서식/좌표 동일성·상태 복원 | `python scripts/verify_pretendard.py` |
| [interactive-live.html](interactive-live.html) | 현재 #5 원본의 CSS·JS·폰트·라이선스 내장 공유본 | `python scripts/check_interactive.py` |

## 대표 프리뷰

1600×950 창에서 원본 `.slide`를 캡처한 1440×810 이미지입니다. 원본 8개와 두 모드의 프리뷰를 구분합니다.

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
| Scroll 보기 | [JPG](../dual-mode-scroll.jpg) |
| Slide 보기 | [JPG](../dual-mode-slide.jpg) |

다른 화면의 PNG는 기본 `/tmp/reference-integration-review`, 두 모드 PNG는 `/tmp/dual-mode-review`에 저장합니다. CI는 실행별 artifact로 보관하며 모든 캡처를 Git에 중복 커밋하지 않습니다. 새 제작 대상은 PC 4개 크기이며 원본 검증의 작은 화면 2개는 기존 호환성 회귀입니다.

## 부분 검사와 보관 규칙

```bash
python scripts/validate_references.py --templates concept --report /tmp/concept-validation.json
```

부분 결과로 전체 통과 JSON을 덮어쓰지 않습니다. `--report`를 생략한 부분 결과는 `--evidence-dir` 아래 임시 경로에 생성합니다. 대표 이미지를 유지하며 재검사하려면 값 없이 `--update-previews`를 붙입니다.

이전 before 이미지 10개·오래된 `validation.json`·동일 실행의 파생 JSON 7개는 검토 완료 후 제거했습니다. 과거 소스·이미지는 Git 이력과 해당 PR에서 복구할 수 있습니다. 전체 검증기는 파생 JSON을 다시 만들지 않습니다. 프리뷰는 편집 가능한 원본의 대체물이 아닙니다.
