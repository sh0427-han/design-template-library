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


## Rendering Modes (Scroll / Slide)

공통 색상·타이포그래피·-1pt 문자 간격은 **하나의 디자인 시스템**을 따릅니다. 문서의 길이와 탐색 방식만 모드별로 변경합니다.

- **Scroll**: 읽기 폭 제한, 목차/앵커, 세로 스크롤, 상세 설명, 긴 실험 패널.
- **Slide**: 16:9 화면, 페이지 단위 전환, 핵심 메시지 1개/장, 압축된 조작 패널.
- **Shared**: 콘텐츠, 용어, 예제 입력값·계산 로직, 색상, 폰트, 인터랙티브 컴포넌트의 의미.
- 디자인 규칙을 복제하지 않고 새 템플릿의 `assets/css/tokens.css`가 기존 `templates/html/styles.css`를 import합니다.

예시/구현: [Dual-mode Learning](templates/dual-mode-learning/) · [모드별 규칙](templates/dual-mode-learning/MODES.md).


## Iterative example guidelines

- 기존 3종 템플릿과 Dual-mode 예시 5장은 동등한 개선 대상입니다.
- 실제 계산 예제와 충분한 도식 크기로 정보 밀도를 보완하고, 불필요한 설명을 늘려 공간을 채우지 않습니다.
- 한 줄로 표현 가능한 부제목은 수동 줄바꿈을 넣지 않습니다.
- 제작 과정이나 AI 작성 여부를 설명하는 메타 문구는 학습자 화면에 넣지 않습니다.
- Scroll에서는 좌측 목차 오른쪽부터 본문을 정렬하고, 긴 문단은 읽기 폭을 별도로 제한합니다.

## 제목·그림 설명 작성 규칙

- **제목**: 핵심 개념을 함축한 짧은 명사형 또는 구문형 사용. 서술형 종결 `~다`, `~입니다` 지양.
- **부제목·Figure 캡션**: 짧고 구체적인 문구 사용. `~입니다`와 불필요한 문장형 표현 삭제.
- **화면용 텍스트**: `실제 완성 디자인은 아닙니다`, `교육용 직접 구현 예제입니다` 등 제작 방식에 관한 메타 설명 제외.
- **기술 정보**: 실제 계산값과 레이블의 일치 유지. 외부 이미지·Figure의 출처와 실험 조건처럼 필요한 정보는 생략하지 않음.
- **Concept 기준**: 직관적 시각 사례 → 요소 확대/분해 → 숫자·구조 → 한 줄 핵심 개념. 도식과 수치는 서로 대응하도록 구성.


## 8종 독립 HTML 레퍼런스 · 2026-10-21

- 최신 Concept을 기준으로 공통 프레임 통일: 1440×810, 제목 49px, 부제목 21px, 여백 위 54px / 좌우 66px / 아래 30px. 위 기본 규격에서 이 8종에만 적용하는 조정값입니다.
- 데스크톱은 너비와 높이를 모두 고려한 16:9 비례 축소, 900px 이하에서는 세로 읽기 배치.
- `templates/html/reference-layout.css`는 8종 HTML에서만 명시적으로 로드합니다. 갤러리·CNN 연속 강의·PPTX의 공통 토큰은 바꾸지 않습니다.
- 모든 텍스트는 기존 `--character-spacing: -1pt` 상속. 색상·패널 구조와 유형별 목적 유지.
- 검증 및 비교: [8종 검토 기록](docs/REFERENCE_REVIEW_2026-10-21.md).

### 줄바꿈과 하단 식별 문구

- 한글 어절 중간을 나누지 않습니다. 짧은 한두 글자만 마지막 줄에 남으면 문장 전체를 다음 줄로 옮깁니다. 8종 HTML은 `word-break: keep-all`과 문단의 `text-wrap: pretty`를 사용하며, 의미 단위 분리가 필요할 때 `.note-sentence`를 사용합니다.
- `Design Template Library · 유형명`은 레퍼런스 식별용 기본값입니다. 실제 자료에서는 강의명·프로젝트명·보고서명과 장/주제로 교체할 수 있습니다. 이번 수정에서는 기존 하단 문구를 유지합니다.
