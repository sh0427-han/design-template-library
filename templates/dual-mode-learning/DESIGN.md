# Scroll / Slide 공유 디자인 규격

## 적용 순서와 단일 소스

[공통 디자인](../../DESIGN_SYSTEM.md) → [컴포넌트 설계 규격](../../docs/DESIGN_COMPONENT_RECIPES.md) → 적합한 편집 가능 HTML 레퍼런스 → 두 모드의 실제 렌더링 순서로 적용합니다. 8개 패턴은 선택할 구성 방식이며 필수 8장이 아닙니다. 제작 대상은 PC 웹페이지입니다.

- 콘텐츠: `assets/js/lesson.js`. 공통 header/detail/takeaway와 Scroll 전용 `scrollOnly`.
- 계산: `assets/js/lab.js`. 동일 입력·커널·곱셈·합산·출력과 실습.
- Figure: `assets/js/render.js`. 두 모드에서 동일한 DOM 생성.
- 정본 토큰: `../html/styles.css`. `tokens.css`에는 의미 별칭만 둡니다.
- 공유 컴포넌트: `components.css`. 모드별 파일은 배치·탐색·설명 밀도만 담당합니다.

## 글꼴·간격·색

숫자와 코드형 라벨도 **실제 로컬 Pretendard Variable**, 모든 텍스트 **−1pt**입니다. 별도 monospace 예외·수동 tracking을 만들지 않습니다. 제목/부제/본문/보조/숫자 셀은 공통 line-height 토큰을 사용합니다. 요소 간격은 관련 요소 8px, 구역 16px, 주요 Figure 24px를 출발점으로 합니다. 글자 크기 변경과 줄 높이 변경, 요소 간 margin/gap 변경은 서로 다른 조정입니다.

Navy는 제목·주요 결과, Blue는 입력 선택·처리·양수 응답, Amber는 이 예제의 음수 응답, Muted는 0/조건, Teal은 마지막 핵심 캡션의 가는 강조선입니다. 출력의 현재 선택 셀은 Navy/White이며 숫자와 행·열로도 연결합니다. 외부 흐름 화살표는 Blue SVG 한 path로 몸통과 화살촉을 연결합니다.

## 카드·Figure·마지막 캡션

- 일반 White 카드: 1px border, 17px radius, 24px padding. 실습은 컨트롤 공간을 위해 20px padding.
- 캔버스: Canvas 배경, 10px radius. 큰 그림을 담는 슬롯과 문장 사이에 충분한 간격을 둡니다.
- 입력/커널/출력은 같은 흐름 영역. 행렬의 실제 bounding box 중앙 y좌표와 SVG 화살표 중앙을 맞춥니다.
- 비교는 세 카드의 제목·행렬·결과 구분선 높이를 일치시킵니다. 특정 결과 카드 전체를 우월한 방법처럼 강조하지 않습니다.
- 조건·필수 기술 caveat는 Figure 다음 White 설명 영역 안에 넣습니다. Scroll 심화 해설도 마지막 캡션보다 위입니다.
- 마지막 핵심 캡션: White, Teal 4px 왼쪽 선, padding 12px/17px, gap 15px, 본문 19px/1.45. 그 아래에는 페이지 번호·기본 조건의 Footer만 허용합니다.
- 긴 내용을 숨겨 맞추지 않습니다. 실제 위치·텍스트 경계를 검사하고 크기·중복 설명·간격을 조정합니다.

## 모드별 배치

Slide는 1440×810 논리 캔버스를 전체 배율로 축소/확대하며 label만 별도로 줄이지 않습니다. 상단 40px, 좌우 58px, 하단 28px. header 안 8px, header 뒤 주요 구역 24px, content→caption→footer는 각각 16px입니다. 자세한 크기와 낮은 PC 창에서의 배율은 [상세 명세](../../docs/DUAL_MODE_REFERENCE_REUSE.md)에 기록합니다.

Scroll은 sticky 목차 220px + gap 32px + 가변 본문이며 1399px 이하 PC 창에서는 목차 180px/gap 24px입니다. 1280–1366px 창에서는 계산표를 행렬 흐름 아래로 내려 가독성을 보존합니다. 문단의 폭과 Figure의 폭을 별도로 관리합니다.

## 검수와 확장

[모드 규격](MODES.md)에 따라 URL 상태·키보드·딥링크·초기화를 유지합니다. `python scripts/verify_pretendard.py`로 PC 4개 크기의 전체 5개 블록, 실제 글리프, −1pt, 정렬·텍스트 경계·caption/footer·독립 수치·모드 간 선택 유지를 검증합니다. 프리뷰는 이 최종 HTML에서 생성합니다. 모바일 전용 제작은 필수 대상이 아닙니다.

새 개념에서는 [상세 명세](../../docs/DUAL_MODE_REFERENCE_REUSE.md)의 현재 CNN 숫자를 무작정 복제하지 말고, 적합한 8개 패턴을 선택한 뒤 콘텐츠·계산 데이터와 검증 기준을 함께 바꿉니다. [Figure 제작 표준](../../docs/FIGURE_PRODUCTION_STANDARD.md)과 [재사용 절차](../../docs/REFERENCE_REUSE_WORKFLOW.md)를 따릅니다.
