# Shared Design System (AI Instructions)

## Goal

기술적 정확성이 필요한 강의, 논문 발표, 보고 및 웹 교과서를 **HTML Scroll/Slide 두 방식**으로 제작한다. AIBook처럼 설명·시각화·직접 조작·결과 확인이 연결되는 교육 경험을 목표로 하되 기존 콘텐츠와 기능을 존중한다. **PPTX는 제작·변환 대상이 아니다.**

## Single Source of Truth

- Content: `assets/js/lesson.js`
- Canonical design tokens & global character spacing: `../html/styles.css`
- Semantic token aliases: `assets/css/tokens.css` (imports canonical file; colors must not diverge)
- Shared Components: `assets/css/components.css`
- Interactive Math/Logic: `assets/js/lab.js`
- Presentation Adaptors: `assets/css/{scroll,slides}.css`, `assets/js/{scroll,slides}.js`
- 콘텐츠/수식을 모드별 파일에 중복 작성하지 않는다.

## Visual System

- 배경: 밝고 차분한 neutral palette, 본문 텍스트는 높은 대비
- 글꼴: 공유 HTML 기본 폰트 **Pretendard Variable**. 수치/코드 영역의 monospace 설정은 기존과 동일
- **모든 텍스트에 -1pt 좁은 자간을 적용**하며 기존 `templates/html/styles.css`의 `--character-spacing`을 상속한다.
- 색상은 semantic token으로 지정: `--ink`, `--muted`, `--accent`, `--line`, `--surface`, `--surface-soft`
- 설명은 좁은 읽기 폭을 유지하고, 시각화는 필요한 너비를 사용한다.
- 컴포넌트: concept card, callout, step flow, figure, lab, source citation
- 수식과 도식은 정확해야 하며 Input → Process → Output이 눈에 보여야 한다.
- 불필요한 gradient/shadow/장식, 밀집된 텍스트는 피한다.
- 외부 자산을 실제로 쓸 때는 Figure 가까이에 출처를 명시한다.
- 효과/상호작용은 지식 전달에 기여하는 것만 추가한다.

## Typography & Rhythm

- 공통 기본 spacing token은 `--space-*`를 사용한다.
- 제목/리드/본문/캡션의 계층은 각 모드에서 일관되게 유지한다.
- 모바일 Scroll에서는 1열, desktop Scroll에서는 왼쪽 sticky TOC + 본문으로 구성한다.
- Slide에서는 16:9 한 화면에 핵심 메시지 하나. 글자 축소보다 콘텐츠 분할을 우선한다.

## Interaction & Semantics

- 입력 라벨과 계산값을 항상 연결한다.
- Reset이나 기본값으로 되돌릴 수 있는 수단을 제공한다.
- 키보드 포커스 가능 요소는 명확한 focus 스타일을 갖는다.
- Slide 페이지 전환 단축키는 편집 가능한 입력 요소를 방해하지 않는다.
- 정상적인 새로고침/딥링크 동작을 지원한다.

## Reference and Scope

- Common source: [`../../DESIGN_SYSTEM.md`](../../DESIGN_SYSTEM.md).
- AIBook Attention: https://aibook.euiyun.com/chapters/attention.html#sim-editor (interaction/layout inspiration, no code copied).
- This example implements both HTML Scroll and Slide modes; the eight standalone HTML references are reusable visual patterns, not output formats. Legacy PPTX assets were removed; do not recreate them.

## Acceptance Criteria

1. 공통 토큰 변경 시 두 모드의 주요 시각적 변화가 동일하다.
2. 같은 `lesson.js` 텍스트가 두 모드에 동일하게 나타난다.
3. 같은 `lab.js`의 수치 계산 결과가 두 모드에서 동일하다.
4. Scroll에서는 페이지 전체가 자연스럽게 세로 스크롤된다.
5. Slide에서는 화살표/버튼/해시로 전환되고 뷰포트 내 내용이 잘리지 않는다.
6. 로컬 정적 서버에서 기능이 동작하며, 웹 폰트(Pretendard CDN)가 로딩되지 않아도 폴백 폰트로 콘텐츠와 인터랙션을 사용할 수 있다.

## Avoid

- 각 모드마다 색상, 글꼴, 컴포넌트를 따로 복사해서 관리하기
- Scroll에 맞춘 긴 문단을 축소해서 Slide 한 장에 몰아 넣기
- CSS가 다른 모드의 스타일을 오염시키는 전역 선택자
- 실제 계산값과 그림의 표시 숫자가 다른 교육용 모형

## Reference-gallery refinement criteria (2026-10-20)

- 8종 HTML 구성 패턴과 이 5장 HTML 실습은 **모두 함께 다듬는 레퍼런스 예시**입니다. 어떤 예시도 최종 확정 디자인으로 취급하지 않습니다.
- 빈 여백을 무조건 글로 채우지 않습니다. 각 화면에서 **계산 가능한 그림, 수치 비교, 처리 단계**가 충분한 크기로 보이도록 배치합니다.
- 핵심 부제목은 공간이 허용하는 한 문장으로 표시합니다. 수동 `<br>`를 넣지 않으며 필요한 경우 영역을 넓힙니다.
- 슬라이드·웹 교과서의 사용자 본문에서는 구현·제작 과정에 대한 메타 설명을 삭제합니다. 수치·가정·용어에 관한 필수 설명만 남깁니다.
- Scroll에서는 왼쪽 TOC 바로 오른편에 본문을 정렬하며 브라우저 가로 공간을 넓게 사용합니다. 긴 문단의 읽기 폭만 별도로 제한합니다.
- Slide에서는 16:9 고정비로 모든 슬라이드를 렌더링하여 도식 크기, 정보 밀도, 잘림/겹침을 **각 장별로** 검토합니다.
