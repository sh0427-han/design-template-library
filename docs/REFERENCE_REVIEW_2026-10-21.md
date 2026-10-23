# 2026-10-21 검토 이력

**역사적 기록입니다. 현재 구현 명세는 [REFERENCE_PAGE_SPECS.md](REFERENCE_PAGE_SPECS.md), 최종 통합 출처와 상태는 [8종 검토 완료 상태](REFERENCE_RELEASE_STATUS.md)를 따릅니다.** 당시 승인 대기 상태·이전 그림 설명을 현재 설계로 적용하지 않습니다.

당시 작업에서는 8종의 프레임과 자간, 작은 데스크톱에서의 16:9 축소, 모바일 읽기 배치, 사진과 RGB의 정합성, 비교 기준·단위·수치 계산을 점검했습니다. 당시 비교용 캡처는 검토 완료 후 제거했습니다. 필요한 이전 버전은 Git 이력에서 확인합니다.

## 당시 검토에서 초기 통합으로 이어진 변경

| 유형 | 현재 확인할 기준 |
| --- | --- |
| 01 Concept | 실제 사진의 80×80 리샘플·선택 4×4 픽셀·RGB/HEX |
| 02 Process | PR #9의 사진 기반 고정 필터 특징 모티프와 역할 흐름 |
| 03 Comparison | 같은 입력·세 비교 기준·조건과 한계 |
| 04 Step-by-Step | PR #11의 5×5/3×3/3×3·곱 9개·합 −6 |
| 05 Interactive | 승인된 이상 우선 그룹·실시간 대입식·내장 폰트 |
| 06 Architecture | PR #10의 두 Conv/ReLU/Pool Block·Flatten 8192·FC·Softmax |
| 07 Experiment | 승인된 TP FP / FN TN 축과 4개 지표 |
| 08 Executive Summary | 지표별 기준 100%·원래 수치/단위·실행 항목 |

기술적 정확성과 현재 프리뷰의 판정은 최신 [공통 검증 JSON](../previews/review/reference-validation.json)을 사용합니다. 과거 40개 화면 기록이나 before 이미지는 현재 48개 조합을 대신하지 않습니다. 현재 제작·검토 절차는 [Figure 표준](FIGURE_PRODUCTION_STANDARD.md)과 [검토 가이드](REFERENCE_REVIEW_GUIDE.md)에 있습니다.
