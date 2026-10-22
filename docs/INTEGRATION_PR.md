현재 분리된 HTML 레퍼런스를 최종 검증된 파일 기준으로 통합합니다. #2·#3은 PR #9, #4는 PR #11, #6은 PR #10, #5·#7은 로컬 승인본을 선택하고 #1·#8의 정상 구성을 보존했습니다. #6은 두 Conv/ReLU/MaxPool Block → Flatten 8192 → FC → Softmax입니다.

공통 로컬 Pretendard와 실제 글꼴 검사, SVG 기호와 폰트 로딩 후 정렬, 8종 공통 검증·읽기 전용 CI를 적용했습니다. README·카탈로그·디자인 시스템·Figure 제작 표준·페이지 상세 명세·재사용/검토 문서를 현재 구현에 맞췄습니다.

검증: 8종×6개 Chromium 화면, 독립 행렬·필터·Shape·확률·분류 지표·막대 비율, 실제 Pretendard/−1pt, 카드 패딩·화살표·오버플로·Footer·이미지·JS 오류. #5는 126개 기본·42개 변경 데이터·12개 폰트 누락 상태와 오프라인 공유본도 확인합니다. source/preview 해시와 개별 결과는 `previews/review/reference-validation.json`, `interactive-validation.json`에 있습니다.

범위와 출처·충돌 해결은 `docs/INTEGRATION_REPORT_2026-10-22.md`와 `docs/integration-sources.json`을 참고합니다. #8 사전 검토의 새 디자인 제안과 구버전 로컬 #4 실험은 포함하지 않았습니다. PPTX는 생성하지 않습니다.

통합 후 실제 main 상태를 확인한 다음, 같은 head인 PR #9·#10·#11에 이 PR 링크를 남기고 정리합니다. 새 커밋이 추가된 PR은 별도 검토합니다.
