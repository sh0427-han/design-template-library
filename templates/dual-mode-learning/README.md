# Scroll / Slide 공통 콘텐츠 데모

CNN의 국소 연산을 다섯 학습 블록으로 설명하는 편집 가능한 HTML/CSS/JavaScript 예제입니다. 8개 독립 레퍼런스의 최신 시각 규격을 사용하고, 콘텐츠·수치 계산은 한 소스에서 공유합니다. 별도 빌드·CDN·PPTX가 필요하지 않습니다.

## 실행과 검증

저장소 루트에서 실행합니다.

```bash
python -m http.server 8000
# 브라우저: http://localhost:8000/templates/dual-mode-learning/index.html
python templates/dual-mode-learning/tools/check.py
python scripts/check_sources.py
python scripts/verify_pretendard.py
```

- [Scroll 원본](scroll.html): 왼쪽 목차와 세로 학습 문서.
- [Slide 원본](slides.html): 1440×810 논리 캔버스와 이전·다음·키보드 탐색.
- 두 모드의 링크는 현재 학습 단계와 필터·입력 위치를 전달합니다. 예: `slides.html?filter=average&position=4#experiment`.
- 새로고침·딥링크도 같은 선택을 복원합니다. 초기화는 세로 경계 필터와 첫 위치로 돌아갑니다.

## 파일의 역할

| 파일 | 역할 |
| --- | --- |
| `assets/js/lesson.js` | 공통 제목·부제·조건·심화 설명·마지막 핵심 캡션 |
| `assets/js/lab.js` | #4와 같은 5×5 입력, 3종 커널, 원소별 곱·합·출력 계산, 실습 조작 |
| `assets/js/render.js` | 같은 데이터의 행렬·흐름·비교 Figure와 섹션 구조 |
| `assets/js/state.js` | URL의 필터·위치 읽기/검사/저장 및 모드 링크 |
| `assets/js/scroll.js` | 목차·현재 읽는 단계·모드 전환 링크 |
| `assets/js/slides.js` | 슬라이드·해시·키보드·전체 캔버스 배율 |
| `assets/css/tokens.css` | 공통 `../html/styles.css`를 가져오는 의미 별칭 |
| `assets/css/components.css` | 모드가 공유하는 Figure·행렬·계산표·캡션 |
| `assets/css/scroll.css`, `slides.css` | 배치·설명 밀도·탐색 UI의 차이 |

## 레퍼런스 재사용

#4의 행렬과 계산, #2의 처리 흐름, #3의 동등한 비교, #5의 조작/결과 연결, #7의 수식 대응을 참고합니다. #6의 전체 CNN 분류기를 국소 연산 예제에 복제하지 않으며 #8의 보고용 KPI도 넣지 않습니다. 별도 검토 중인 #1 원본은 변경하지 않습니다.

전체 입력·커널·출력, 5개 블록의 구조와 크기, 색·정렬, 모드 상태, 검증 및 미리보기 정리 근거는 [재사용 상세 명세](../../docs/DUAL_MODE_REFERENCE_REUSE.md)에 기록합니다. [공통 디자인](../../DESIGN_SYSTEM.md), [컴포넌트 규격](../../docs/DESIGN_COMPONENT_RECIPES.md), [Figure 표준](../../docs/FIGURE_PRODUCTION_STANDARD.md)을 함께 봅니다.

## 프리뷰와 적용 범위

- [Scroll](../../previews/dual-mode-scroll.jpg), [Slide 첫 장](../../previews/dual-mode-slide.jpg), [Slide 실습](../../previews/dual-mode-lab-slide.jpg).
- 종전 `dual-mode-process-slide.jpg`는 첫 Concept 장을 담은 잘못된 이름이어서 삭제하고 `dual-mode-slide.jpg`로 교체했습니다. 갤러리와 생성 스크립트도 새 경로를 사용합니다.
- JPG는 QA/탐색용입니다. 실제 전환·탐색·계산은 HTML/JS로 동작하며 JPG를 입력으로 사용하지 않습니다.
- PC 4개 창 크기에서 전체 5개 블록의 두 모드를 검증합니다. 기존 390px 폰트/가로 경계 검사는 호환 기록으로 유지하며 새로운 모바일 디자인 요구사항은 아닙니다.
- 모든 숫자·라벨까지 로컬 Pretendard Variable 및 −1pt를 사용합니다. monospace 예외는 제거했습니다.
- 고정 필터 계산을 학습된 CNN 추론이나 실제 사진의 측정 결과로 설명하지 않습니다.

디자인/학습 인터랙션 참고: [AIBook Attention](https://aibook.euiyun.com/chapters/attention.html#sim-editor). 소스·이미지 복제 없이 독립 구현했습니다.
