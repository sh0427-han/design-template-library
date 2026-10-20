# Dual-mode Learning & Presentation Template

하나의 콘텐츠/디자인 시스템을 **Scroll(웹 교과서)** 및 **Slide(강의/발표)** 환경에서 공유하는 순수 HTML/CSS/JavaScript 템플릿입니다. 별도 빌드 시스템과 외부 CDN을 요구하지 않습니다.

## 시작하기

```bash
cd templates/dual-mode-learning
python -m http.server 8000
```

- 시작 페이지: http://localhost:8000/
- 웹 교과서: http://localhost:8000/scroll.html
- 발표 슬라이드: http://localhost:8000/slides.html

## 단일 소스 원칙

1. `assets/js/lesson.js`에서 콘텐츠를 작성합니다. 각 section은 `id`, `eyebrow`, `title`, `lead`, `body`, `kind`를 갖습니다.
2. 기존 `templates/html/styles.css`를 기준으로 색상과 `-1pt` 자간을 공통 사용합니다. `assets/css/tokens.css`에는 추가 의미적 별칭만 둡니다.
3. `assets/css/components.css`에서 공통 컴포넌트 스타일을 관리합니다.
4. 모드마다 **화면 배치와 탐색 방식만** 별도로 정의합니다. `scroll.css`/`slides.css`, `scroll.js`/`slides.js`를 참고하세요.
5. 실습(Interactive Figure)은 `assets/js/lab.js`에 작성하며 두 모드 모두 재사용합니다.

## 포함된 예제

CNN convolution의 원리·국소 연산·입출력 크기·실습·Feature Map 비교까지 이어지는 5개 예시 슬라이드를 사용합니다. Scroll 페이지에서는 문서형으로 연결하고, Slide 페이지에서는 5장 슬라이드로 표시합니다. 실습 컴포넌트는 실제 5×5 입력과 3×3 필터로 계산한 결과를 보여주며 필터 및 입력 영역 위치를 바꿀 수 있습니다. 1개 콘텐츠와 1개 계산 로직을 공유합니다.

> **주의**: 이 저장소는 디자인 시스템/화면 모드의 작동을 확인하는 독립 데모입니다. 실제 Vision AI 강의 55장을 이 템플릿으로 옮기거나 기존 공개 GitHub 저장소에 배포하지 않았습니다.

## 파일 구조

```
.
├── DESIGN.md                 # 공통 디자인 규칙 (AI 참고용)
├── MODES.md                  # Scroll / Slide 모드 규칙
├── index.html                # 두 모드 선택
├── scroll.html               # 웹 교과서 진입점
├── slides.html               # 발표 슬라이드 진입점
├── assets/
│   ├── css/
│   │   ├── tokens.css        # 공통 토큰
│   │   ├── components.css    # 공통 UI 컴포넌트
│   │   ├── scroll.css        # Scroll 전용
│   │   └── slides.css        # Slide 전용
│   └── js/
│       ├── lesson.js         # 공통 콘텐츠
│       ├── render.js         # 공통 콘텐츠 렌더러
│       ├── lab.js            # 공통 인터랙티브 실습
│       ├── scroll.js         # Scroll 탐색
│       └── slides.js         # Slide 탐색
└── tools/check.py            # 정적 검증
```

## 레퍼런스 개선 원칙

- 기존 `concept`, `process`, `comparison`과 새 Scroll/Slide 예제를 모두 디자인 예시로 관리하며 반복적으로 수정합니다.
- 슬라이드에 불필요한 제작 설명 문구를 표시하지 않습니다. 부제목은 가능한 한 한 줄로 배치합니다.
- Scroll Mode는 데스크톱 브라우저에서 왼쪽 목차 기준으로 본문을 정렬하며, 다이어그램이 가용 가로 공간을 사용합니다.
- PNG/JPG 미리보기는 검토 편의를 위한 결과물이며, 원본 텍스트/그래프/계산 로직은 HTML/CSS/JavaScript에 있습니다.

## 출처 및 디자인 참고

- 디자인 및 인터랙티브 설명 방식 참고: [AIBook - Attention](https://aibook.euiyun.com/chapters/attention.html#sim-editor)
- AIBook의 소스코드, 이미지 또는 저작물은 복제하지 않았습니다. 학습 목적의 레이아웃 패턴을 참고해 독립적으로 구현했습니다.

## 확인 상태

- Python 정적 구조 검증 및 Node.js JS 구문 검사를 실행할 수 있습니다.
- 브라우저 렌더링은 별도로 실행하여 `previews/`에 결과를 저장하고 검증합니다.
- 웹 UI는 독립적인 학습용 예제이며 실제 학습 모델 결과가 아닙니다.
