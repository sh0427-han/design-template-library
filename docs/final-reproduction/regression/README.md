# 기존 8종 회귀 · 최종 재현 시험과 별도 증거

실행 명령:

```bash
python scripts/validate_references.py --evidence-dir /tmp/final-reproduction-reference-regression --report docs/final-reproduction/regression/reference-validation.json --update-previews
```

`--update-previews`의 빈 목록으로 기존 대표 프리뷰를 갱신하지 않았다. [실제 보고서](reference-validation.json)의 source_sha256는 실행한 원본8종의 정확한 입력이며 현재 원본과 다시 비교한다. 새 시험의 예제 파일은 이 검사의 대상이 아니다.

결과: 기존8종×6화면=48조건 PASS. PC4의32조건과 기존900×900/390×844 호환회귀16조건을 구분한다. 후자의 성공으로 새 제작 범위를 모바일로 확대하지 않는다. 실제 로컬 Pretendard/CDP, 기술 계산, DOM/SVG 경계, 콘솔/요청 오류, Process 실패/복구, Comparison 크기 변경 검사를 포함한다. canonical_preview_updates는 빈 목록이다.

이는 원본 회귀이며 새 주제 재사용 성공이나 8종 모두의 새 제작자 재현을 뜻하지 않는다. 새로 생성한 원본48캡처 모두에 별도의 사용자/사람 시각 승인을 받은 것도 아니다. 새 과제의 화면·기술 검산·독립 검토는 별도 예제/리뷰 증거로 판정한다.
