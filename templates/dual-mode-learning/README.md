# 같은 원본, Scroll / Slide 두 가지 보기

8개 디자인 레퍼런스의 **기존 HTML을 그대로 표시**합니다. 별도의 5장 CNN 도식이나 실습용 디자인을 다시 만들지 않습니다. 출력은 아래 두 개입니다.

| 출력 | HTML | 대표 프리뷰 |
| --- | --- | --- |
| Scroll | [scroll.html](scroll.html) | [dual-mode-scroll.jpg](../../previews/dual-mode-scroll.jpg) |
| Slide | [slides.html](slides.html) | [dual-mode-slide.jpg](../../previews/dual-mode-slide.jpg) |

Scroll은 목차와 함께 같은 8개 원본을 이어 읽고, Slide는 한 장씩 넘깁니다. #5 Interactive의 조작은 두 보기 안에서 동일하게 동작하며 별도 세 번째 출력이 아닙니다. 실습 전용 JPG와 모드 선택용 index 페이지는 제거했습니다.

## 실행

저장소 루트에서 정적 서버를 실행합니다. 두 모드와 원본 HTML은 같은 origin에서 제공합니다.

```bash
python -m http.server 8000
# http://localhost:8000/templates/dual-mode-learning/scroll.html
# http://localhost:8000/templates/dual-mode-learning/slides.html
```

## 원본 재사용 구조

- `assets/js/lesson.js`: 8개 원본의 ID·이름·경로 목록. 내용·공식·그림을 복사하지 않습니다.
- `assets/js/render.js`: 공통 iframe과 준비 상태·배율·키보드 연결. 실제 콘텐츠는 `../html/*.html`이 실행합니다.
- `assets/js/state.js`: 현재 레퍼런스와 #5 임계값을 URL로 전달합니다.
- `assets/js/scroll.js`, `slides.js`: 목차/연속 읽기와 이전·다음 탐색만 다릅니다.
- `assets/css/components.css`: 보기 전환 바·프레임·로딩 메시지. 원본 카드/제목/도식 서식은 정의하지 않습니다.
- `assets/css/scroll.css`, `slides.css`: 모드별 바깥 배치. 색·폰트·자간은 공통 `../html/styles.css`를 가져옵니다.

원본의 1440×810 캔버스 안쪽은 그대로 두고 원본 페이지의 바깥 gutter와 내부 zoom만 제거합니다. 창 크기에는 바깥 프레임 전체를 균일 배율로 맞춥니다. 자세한 적용 범위와 실제 동일성 검증은 [상세 명세](../../docs/DUAL_MODE_REFERENCE_REUSE.md)를 봅니다.

## 상태와 검증

`slides.html?threshold=80#ref-interactive`처럼 현재 예제와 #5의 임계값을 전달합니다. 모드 왕복·새로고침에서 같은 값과 계산 결과를 복원합니다. 레퍼런스 내부 입력에 포커스가 있으면 페이지 단축키가 입력을 가로채지 않습니다.

```bash
python templates/dual-mode-learning/tools/check.py
python scripts/check_sources.py
python scripts/verify_pretendard.py
```

PC 4개 창 크기 × 8개 원본 × 두 모드 = **64개 화면**에서 실제 원본의 서식과 정규화한 위치를 대조합니다. 실제 Pretendard/−1pt·기술 계산·경계·전환도 확인하며, 미리보기는 두 JPG만 생성합니다. #1을 포함한 8개 원본과 기존 개별 프리뷰는 변경하지 않습니다.
