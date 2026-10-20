# Two Rendering Modes

| 속성 | Scroll Mode | Slide Mode |
|---|---|---|
| 목표 | 독자가 자신의 속도로 학습 | 발표자가 개념 단위로 안내 |
| 레이아웃 | 본문 너비 제한 + sticky TOC | 16:9 화면, 한 블록/슬라이드 |
| Navigation | 앵커 링크/브라우저 스크롤 | 화살표, PageUp/Down, Home/End, 하단 버튼 |
| Section 단위 | 하나의 긴 문서의 장/절 | 한 슬라이드의 단일 메시지 |
| 보충 설명 | 상세 Note 노출 | Note는 숨기거나 발표자 노트로 전환 |
| 인터랙티브 Lab | 폭 넓게, 가이드 자세히 | 조작 가능한 핵심 컨트롤 위주 |
| Design Tokens | 공통 | 공통 |
| Content/Logic | 공통 | 공통 |

## Content splitting

공통 콘텐츠는 작은 학습 블록들의 시퀀스로 작성합니다. Scroll은 블록을 연속 배치하고, Slide는 학습 블록을 화면별로 배치합니다. 긴 설명은 `scrollOnly` 영역으로 구분하고 핵심 설명은 공통 `lead`/`body`에 둡니다. 본 데모는 각 블록을 한 슬라이드로 대응합니다.

## Integration strategy

이미 제작한 콘텐츠를 전환할 때 원본을 일괄 변경하지 않습니다. 먼저 공통 토큰과 컴포넌트의 스타일 일치를 검증한 뒤 일부 챕터에 Scroll 렌더러를 추가합니다. 기존 Deep Link, 진행 순서, 발표 동작을 보존합니다.
