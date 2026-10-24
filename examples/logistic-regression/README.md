# 로지스틱 회귀 · 첫 재사용 검증 산출물

이 자료는 **기존8종과 공통 Markdown의 충분성을 확인하기 위해 제작한 첫 검증 산출물**입니다. 다음 제작의 정본이나 아홉 번째 템플릿이 아닙니다. [검토 교훈과 다음 라운드 판정](../../docs/TEMPLATE_REUSE_VALIDATION.md)에 공통 기준으로 반영한 내용과 한계를 기록합니다.

현재 자료는 **#1 개념 슬라이드 한 장**입니다. 입력 x의 기호/설명 → 가중치 w·절편 b와 일반식/설명 → 시그모이드 식·일반 곡선 → 양성 확률의 관계를 그림과 키워드로 설명합니다. 계산 슬라이드와 임계값 부록은 제거했습니다.

- [설계 명세](DESIGN.md): 목적·용어·일반식·그림·서체·배치·검증을 재현할 구체적인 기준
- [다음 라운드의 템플릿 검증 프롬프트](../../docs/CONCEPT_REUSE_PROMPT.md): 새 개념을 입력해 Markdown부터 제작하는 요청문
- [Scroll](scroll.html) / [Slide](slides.html): 같은 한 장의 두 보기
- [Scroll JPG](previews/scroll.jpg) / [Slide JPG](previews/slide.jpg) / [개념 PNG](review/concept.png)
- [현재 검증 JSON](previews/validation.json)

## 실행과 재사용

저장소 루트에서 `python -m http.server 8000`을 실행하고 `http://localhost:8000/examples/logistic-regression/scroll.html` 또는 `slides.html`을 엽니다. 페이지는1/1, 목차는 항목 하나이며 이전/다음은 비활성입니다. 과거 계산/부록 URL도 개념 장으로 정규화합니다.

다음 검증은 기존8종과 공통 Markdown을 기준으로 새 개념을 정하고 `examples/<새-개념>/DESIGN.md`에 목표·정보 위계·일반 관계·Figure 구조를 작성합니다. 원본8종과 현재 검증 산출물은 보존하고 새 경로에서 제작하며 문서 충분성을 VALIDATION.md에 남깁니다. 현재 네 단계와 시그모이드를 다른 개념에 그대로 복제하지 않습니다.

`lesson.js`는 한 장의 편집 가능한 HTML/MathML/SVG, `lesson.css`는 전용 Figure, `viewer.js`는 보기 프레임·탐색을 담당합니다. 화면에 실제 입력·계수·결과·선택 점은 없으며 샘플/판정 모델 모듈도 없습니다. 수학은 STIX Two Math/MathML, 본문·일반 영문은 Pretendard Variable이며 둘 다 전역−1pt를 유지합니다.

## 현재 검증 범위

```bash
python scripts/check_sources.py
python scripts/verify_logistic_reuse.py
python scripts/check_documentation.py
```

PC4개 크기×2모드의 **8개 화면**, 독립 함수 계산으로 곡선161개 점, 실제 Pretendard/STIX 글리프·−1pt·중앙축·분수·패딩·Footer·두 모드 서식/상대 경계·한 장 탐색과 과거 URL을 검증합니다. 기존8종의48화면/두 모드64화면 검사는 별도 회귀로 유지합니다. 삭제한 계산/부록의40화면·606/404판정 수치를 현재 결과로 인용하지 않습니다.

대표 JPG 두 개와 검토 PNG 한 개만 보관하며 다른 화면 캡처는 `/tmp/logistic-reuse-review`·CI artifact에 둡니다. 검증 JSON은 설계·소스·공통 CSS/폰트·프리뷰 해시를 기록합니다. 변경 후 예전 통과 보고서를 재사용하지 않습니다.

## 검토 이미지를 전달하는 방법

로컬 `/tmp`·`/workspace` 링크는 외부 공유 주소가 아닙니다. 공개 저장소의 Commit에 고정한 HTTPS 이미지 주소로 정상 응답·이미지 형식·원본 바이트 일치를 확인한 뒤 채팅 본문에 Markdown 이미지로 삽입합니다. 도구가 읽은 이미지를 사용자에게도 첨부했다고 간주하지 않습니다. [이미지 모음](review/README.md)도 함께 제공합니다.

이 자료는 같은 제작자가 Markdown을 먼저 작성하고 구현·검토한 재사용 사례입니다. 별도 제작자의 독립 재현 시험과 사용자 시각 승인은 구분합니다. 원본8종의 승인 상태와 신규 자료의 상태도 별도로 기록합니다.
