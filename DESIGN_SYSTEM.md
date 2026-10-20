# Design System v0.1

PPTX와 HTML 기술 강의자료의 공통 시각 설계 규칙입니다. 목표는 **기술적으로 정확하면서 읽기 쉬운 시각 설명**입니다.

## 설계 원칙

1. 슬라이드당 하나의 핵심 메시지를 다룹니다.
2. 입력 → 처리 → 출력, 비교, 수식 예시 등 정보의 논리 구조를 먼저 결정합니다.
3. 텍스트 나열보다는 도형, 관계, 화살표와 구체적인 수치 예시로 설명합니다.
4. 과장된 장식이나 의미가 없는 화살표·아이콘은 사용하지 않습니다.
5. 슬라이드 원본은 수정 가능한 텍스트·도형 중심으로 유지합니다.
6. 프로젝트의 기존 디자인과 사용자의 구체적인 요청이 이 문서보다 우선합니다.

## Canvas & grid

| 항목 | 규격 |
| --- | --- |
| 화면 비율 | 16:9 |
| PPTX | 13.333 × 7.5 in (wide) |
| HTML 기준 캔버스 | 1440 × 810 px |
| 안전 여백 | 좌우 72px 이상 / PPTX 0.68in 이상 |
| 제목 영역 | Category → Title → Subtitle |
| 본문 구성 | 2-column / flow / comparison |
| Footer | 형식 및 슬라이드 번호, 방해되지 않게 |

## Color tokens

| 역할 | 이름 | HEX |
| --- | --- | --- |
| Primary | Navy | `#12233F` |
| Secondary heading | Deep blue | `#1B3558` |
| Key process | Blue | `#3168C8` |
| Positive / output accent | Teal | `#26A6A1` |
| Contrast accent | Amber | `#E49A4D` |
| Text | Ink | `#1B2940` |
| Supporting text | Muted | `#64748B` |
| Canvas | Off-white | `#F6F8FC` |
| Card | White | `#FFFFFF` |
| Border | Light gray | `#DDE4EF` |

색의 의미는 사례마다 다를 수 있으므로 Blue/Teal/Amber를 정상·불량 클래스에 자동 매핑하지 않습니다.

## Typography

- 한국어: `Malgun Gothic` 또는 시스템 한글 산세리프
- 제목: HTML 52–58 px, PPT 30–36 pt
- 본문: HTML 21–26 px, PPT 16–20 pt
- 라벨: HTML 16–19 px, PPT 11–14 pt
- **모든 텍스트 문자 간격: 좁게 1.0pt (=-1.0pt)**. 제목·본문·부제목·라벨·각주·갤러리까지 예외 없이 공통 적용.
- **PPTX:** `templates/pptx/build_templates.py`의 `CHARACTER_SPACING_PT = -1.0`을 사용. 모든 `textbox()`의 텍스트 run에 OOXML `a:rPr@spc="-100"` 반영(100 = 1pt).
- **HTML:** `templates/html/styles.css`의 `--character-spacing: -1pt`를 `html`에 적용하고 모든 텍스트 요소가 상속하도록 구성. CSS 1pt는 표준 96dpi 환경에서 약 1.333px에 해당.
- 이후 새 템플릿에도 동일 규칙 적용. **별도 요청 없이 특정 제목·라벨에 다른 자간 설정 금지.**
- 강의 화면에서 읽기 힘든 작은 글자, 긴 문단, 강제 줄바꿈 최소화

## Components

- **Title / Subtitle**: 간결한 명사형 제목과 한 줄 설명
- **Card**: 흰 배경, 가는 border, 12–20px radius
- **Process node**: 단계별 동일한 기하 구조와 명확한 방향 화살표
- **Comparison**: 같은 비교 기준을 양쪽에 동일하게 적용
- **Highlight**: 한 페이지에서 주된 강조는 1~2곳으로 제한
- **Sources**: 외부 이미지/도표가 있으면 가까운 위치에 원문 URL 기재

## PPT · HTML 동기화

공통 디자인 값은 HTML의 `templates/html/styles.css`와 PPT 생성 스크립트의 `COLORS`를 통해 정의합니다. 두 형식의 레이아웃은 의미/계층/색을 일치시키되 픽셀 단위로 완전히 동일할 필요는 없습니다.

## 품질 점검

- [ ] 글자·도형이 잘리거나 겹치지 않음
- [ ] 16:9 캔버스와 일관된 간격
- [ ] 방향 화살표와 연결 관계가 기술적으로 정확함
- [ ] 예제와 수식에 오류가 없음
- [ ] 발표 화면에서 제목/본문 크기 및 대비가 적절함
- [ ] 재사용된 외부 시각자료는 출처 링크가 명시됨
- [ ] 수정된 원본과 프리뷰가 일치함
