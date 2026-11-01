# 서비스 변경 실험 요약

가상 관측값의 효율 개선과 실패율 손실을 함께 보여 주는 한 장. [Scroll](scroll.html) · [Slide](slides.html). 같은 [content.html](content.html)을 실행한다.

저장소 루트에서 `python -m http.server 8000` 실행 후 `/examples/service-summary/scroll.html` 또는 `slides.html`을 연다. 공통 자산은 `../../templates/html/styles.css`, `math-typography.css`와 로컬 Pretendard·STIX Two Math 폰트/라이선스를 유지한다. 외부 CDN 없음.

검증: `python examples/service-summary/verify.py`. 실행 cwd와 무관하며 저장소 이름/절대 경로를 하드코딩하지 않는다. Python playwright와 Chromium이 필요하며 선택적으로 `CHROMIUM_PATH`를 지정한다. 다른 저장소에서도 동일 `examples/service-summary`·`templates/html` 구조를 유지하면 실행한다. INPUT_MANIFEST.json이 있으면 제공 입력 전체 해시도 검사하며 없으면 해당 검사는 명시적으로 미검증 처리한다.

[설계](DESIGN.md) · [사전판정](D0.md) · [읽기 기록](READ_LOG.md) · [검증](VALIDATION.md) · [검증 JSON](previews/validation.json) · [대표 Slide](previews/slides-1600x950.png).

이 산출물은 사용자 시각 승인이나 실제 독자 이해도 평가를 받지 않았다. Coordinator의 통합 검증·GitHub 처리 상태는 [최종 재현 보고서](../../docs/final-reproduction/REPORT.md)를 따른다.
