# 레퍼런스 검토 가이드

검토 대상은 HTML Scroll/Slide에 재사용하는 8개의 **설명 패턴**입니다. 가장 예쁜 한 장보다 새 데이터와 다른 주제에서도 정확하게 표현할 수 있는 원본·명세·검증을 평가합니다.

## 검토 순서

1. 사용자 목표·청중·실측/예시 구분과 학습 목표 한 문장.
2. 입력·처리·출력·비교 행·상호작용의 기술적 의미.
3. 실제 데이터·수식·Shape·단위·확률·축과 독립 계산의 일치.
4. 제목·실제 Figure 중심·설명의 축, 도형 간격, 내부/외부 화살표.
5. White 카드·의미 색상·텍스트 위계·전체 −1pt·실제 Pretendard.
6. 카드 패딩·구분선·본문과 Footer·가로 폭·이미지 로드.
7. 조작·키보드·경계값·분모 0과 다른 데이터의 재사용.
8. 실제 캡처와 소스·명세·카탈로그가 같은 최종 상태인지 확인.

## 필수 화면

| 1600×950 | 1440×810 | 1366×768 | 1280×720 | 900×900 | 390×844 |
| --- | --- | --- | --- | --- | --- |
| 기준 캡처 | 16:9 | 작은 데스크톱 | 높이 제한 | 세로 읽기 | 모바일 |

```bash
python scripts/check_sources.py
python scripts/verify_character_spacing.py
python scripts/validate_references.py
python scripts/check_interactive.py
python scripts/verify_pretendard.py
python scripts/check_documentation.py
```

공통 48개 조합의 수치·기하·실제 글꼴 검사를 통과한 뒤 데스크톱과 모바일 이미지를 직접 엽니다. 폰트 이름만 CSS에 적힌 상태, 일부 화면만 검사한 상태, 생성 이미지로 원본을 대체한 상태를 완료로 취급하지 않습니다.

## 결과 보고

변경한 페이지와 파일, 기술 검증·폰트·레이아웃 결과, 실제 대표 프리뷰, 재사용 검증 범위, 남은 제한을 기록합니다. #6의 Shape 계약이나 #7의 축 방향 같은 핵심 기준은 [페이지 명세](REFERENCE_PAGE_SPECS.md)를 따릅니다.

자동 검사·사용자 승인·Push·PR·main 반영은 각각 별도 상태입니다. 역사적 검토 문서를 현재 설계 명세로 사용하지 않습니다. [통합 보고서](INTEGRATION_REPORT_2026-10-22.md)와 [프리뷰 증거](../previews/review/README.md)를 확인합니다.
