# 사용 방법 · HTML 전용

이 문서는 빠른 실행·편집 요령입니다. 목적별 문서 지도는 [README](../README.md), 실제 패턴 선택은 [카탈로그](../TEMPLATE_CATALOG.md)를 참고합니다. 지원 결과물은 HTML Scroll / Slide이며 PPTX 파일·생성 경로는 없습니다.

## 실행

공통 CSS·사진·폰트의 경로를 유지하기 위해 **저장소 루트**에서 서버를 실행합니다.

```bash
python -m http.server 8000
```

- `http://localhost:8000/templates/html/index.html`: 8종 갤러리
- `http://localhost:8000/templates/dual-mode-learning/scroll.html`: 연속 읽기
- `http://localhost:8000/templates/dual-mode-learning/slides.html`: 페이지 전환

## 무엇을 편집하는가

- 내용·도형·수식: 해당 `templates/html/<type>.html`과 연결된 JS.
- 공통 색상·폰트·자간: `templates/html/styles.css`.
- 8종 프레임·반응형: `reference-layout.css`.
- 특정 페이지 보정: 그 페이지의 클래스 안에서 작성.
- 실제 데이터·계산 조건: [페이지 상세 명세](REFERENCE_PAGE_SPECS.md)와 함께 수정.

원본을 다른 프로젝트로 복사할 때 CSS·JS·사진뿐 아니라 `assets/fonts/pretendard`와 라이선스를 함께 가져갑니다. #5의 공유용 단일 HTML은 폰트까지 내장한 생성본이며, 수정은 원본에서 합니다.

## 검증·프리뷰

```bash
python -m pip install playwright
python -m playwright install chromium
python scripts/check_sources.py
python scripts/verify_character_spacing.py
python scripts/validate_references.py
python scripts/check_interactive.py
python scripts/verify_pretendard.py
python scripts/check_documentation.py
```

대표 프리뷰는 `previews/html-*`, 공통 결과는 [reference-validation.json](../previews/review/reference-validation.json), 화면별 PNG는 기본 `/tmp/reference-integration-review`입니다. [검토 가이드](REFERENCE_REVIEW_GUIDE.md)의 6개 화면과 직접 시각 확인을 수행합니다.

## 요청문 예시

> 이 저장소의 AGENTS, DESIGN_SYSTEM, Figure 제작 표준과 페이지 상세 명세를 읽고, 대상 독자를 위한 HTML Scroll/Slide 자료를 만들어줘. 내용에 맞는 패턴만 선택하고 편집 가능한 도형·수식으로 재구성해줘. 실제 데이터와 모식도를 구분하고, 로컬 Pretendard·전체 −1pt를 유지해줘. 독립 계산과 실제 글꼴·6개 화면을 검증하고 다른 데이터 구성에서도 재사용을 확인한 뒤 문서와 프리뷰를 갱신해줘.

## 다른 저장소에 적용

다른 프로젝트의 스타일·순서·콘텐츠 요구를 우선합니다. 이 저장소의 경로를 기재하는 것만으로 접근 권한이 생기는 것은 아닙니다. 다른 저장소 수정·배포는 사용자가 지시한 범위 안에서 진행합니다.

새 유형을 등록할 때는 목적·ID·원본·검증·대표 프리뷰·카탈로그·상세 명세를 함께 추가합니다. 절차는 [재사용 워크플로](REFERENCE_REUSE_WORKFLOW.md)를 따릅니다.
