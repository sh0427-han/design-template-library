# Scroll / Slide 보기의 디자인 계약

## 두 출력과 하나의 원본

출력은 `scroll.html`, `slides.html` 두 개이며 대표 프리뷰도 `dual-mode-scroll.jpg`, `dual-mode-slide.jpg` 두 개입니다. 실습은 #5 Interactive 원본 안의 기능입니다. 실습용 보기·별도 디자인·세 번째 canonical JPG를 추가하지 않습니다.

8개 원본은 [카탈로그](../../TEMPLATE_CATALOG.md)와 [페이지 명세](../../docs/REFERENCE_PAGE_SPECS.md)를 따릅니다. `lesson.js`는 원본 경로 목록만 관리하고 `render.js`가 같은 origin의 실제 HTML을 iframe으로 표시합니다. 이미지나 스크린샷으로 대체하지 않습니다. 원본을 수정하면 두 보기에 같은 변경이 적용됩니다.

## 원본 서식의 경계

[DESIGN_SYSTEM.md](../../DESIGN_SYSTEM.md), [컴포넌트 규격](../../docs/DESIGN_COMPONENT_RECIPES.md), [Figure 표준](../../docs/FIGURE_PRODUCTION_STANDARD.md)에 있는 원본의 제목·부제·행간·카드·수식·캡션·푸터·SVG/CSS/JS가 그대로 실행됩니다.

보기 쪽에서 제목 44px, 패딩 40/58/28px 등 또 다른 슬라이드 규격을 만들지 않습니다. 원본의 49px 제목, 21px 부제, 기본 54/66/30px 패딩 및 #3·#5·#7 등 검증된 예외도 원본을 그대로 따릅니다. 실제 Pretendard Variable과 전체 −1pt도 각 원본의 같은 로컬 CSS/WOFF2를 사용합니다.

iframe 안에서 허용하는 변경은 페이지 바깥 배치뿐입니다.

```css
html, body { min-height:0; width:1440px; height:810px; overflow:hidden; background:transparent; }
.reference-deck { padding:0; min-height:0; }
.reference-slide { zoom:1; }
```

캔버스 내부의 텍스트·카드·도식 속성은 덮어쓰지 않습니다. 바깥 프레임을 가용 폭에 맞춰 `width/1440` 배율로 확대·축소하므로 레이아웃과 비율을 유지합니다. 프레임은 원본과 같은 16:9, radius10px, 공통 shadow입니다.

## 보기 전용 구성

- 상단 보기 전환 바 44px. Scroll/Slide 두 선택과 갤러리 링크만 둡니다.
- Scroll: 목차 200px + gap24px, 바깥 패딩 24px, 원본 사이 32px. 1100px 이하 창에서는 목차 170px/gap16px/패딩 20px.
- Slide: 상단 44px/하단 44px을 제외한 영역 중앙. 프레임 폭은 `min(1440px,100vw−40px,(100vh−112px)×16/9)`. 이전·다음·이름·현재/전체 표시만 둡니다.
- 로딩 완료 전 상태 표시와 실패 시 메시지를 제공합니다. 원본 폰트와 이미지 로딩 후 콘텐츠를 노출합니다.
- 키보드와 URL 상태는 [MODES.md](MODES.md)를 따릅니다.

## 실제 동일성 검증

[검증 스크립트](../../scripts/verify_dual_mode.py)는 원본을 직접 열어 얻은 각 요소의 font-family/size/weight/line-height/tracking/color/background/radius/padding과 1440×810 기준 상대 bounding box를 두 보기와 비교합니다. style은 정확한 일치, HTML 위치는0.3px 미만, SVG의 폰트 경계·중앙 보정 위치는 기존 정렬 검사와 같은1px 미만을 요구하며 실제 최대 오차를 기록합니다. CSS를 가져왔다는 이유만으로 통과하지 않습니다. 네 PC 크기에서 실제 글리프·독립 계산·잘림·iframe 크기·전환을 검사합니다. [검증 결과](../../previews/review/dual-mode-validation.json)에 기록합니다.

이 구현은 레퍼런스 8개의 디자인을 정확히 비교하기 위한 보기입니다. 새 강의에는 필요한 패턴만 선택합니다. 모든 주제에 8개를 강제하거나, 이 보기의 iframe 구조를 모든 신규 자료의 유일한 구현 방식으로 강제하지 않습니다.
