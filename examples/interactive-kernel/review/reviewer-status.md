# 독립 Reviewer 인계 — PENDING

- 대상: 새 `examples/interactive-kernel/` 구현, D0 `286bee0`, 추후 Builder 최종 커밋.
- 본 세션에서는 Builder와 완전히 분리된 Agent/독립 세션 실행 기능이 제공되지 않았다. **독립 Reviewer는 실행하지 않았으며 PASS가 아니다.**
- Reviewer는 D0 DESIGN 수학/상태·실제 소스·변경 diff·공통 MD D01·원본 8종 회귀와 브라우저 실 URL을 직접 대조한다. 검토 주체/기준 SHA/테스트 명령·출력을 기록한다.
- 특히 경로 실패시 DOM/상태 삭제·복구, 잘못된 `selectKernel`, URL 비정상 입력, 두 viewer 왕복/새로고침, native 키보드 포커스, 정확 분모·Sobel 부호/색, Pretendard/STIX·−1pt, 출력25셀, 4×2 실제 화면을 확인한다.
- Chromium navigation 정책이 막힌 환경의 `set_content` 캡처는 시각 검토의 일부일 뿐 GitHub Pages HTTP 실행 증거가 아니다.
- 결함이 발견되면 최대 3회 Builder 재작업→서로 다른 세션 Reviewer 재검토; 그 전에는 최종 PASS·v1.0 준비를 주장하지 않는다.
