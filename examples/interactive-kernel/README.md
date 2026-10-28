# CNN 필터 선택과 출력 변화 — #5 Interactive 범용성 검증

실습형 1장, **Scroll** / **Slide** 두 보기. 기존 8종 레퍼런스와 분류 임계값 원본은 변경하지 않는다.

- [Scroll](scroll.html) · [Slide](slides.html) · [D0 설계](DESIGN.md) · [D0/D1 검증](VALIDATION.md)
- 수학 모듈: `model.js` (`KernelModel` UMD), 상태 및 렌더: `app.js` (`KernelInteractive`), 입력: `data.json`. 단일 원본 `content.html`을 두 보기의 iframe으로 실행한다.
- 기준: 7×7 입력, 3×3 커널, valid cross-correlation, Stride1 Padding0 Dilation1 Bias0 ReLU 없음 → 5×5. 선택 출력 `[2][1]`은 Identity 6, Mean 51/9, Sobel-x 28.
- **실제 URL Chromium 확인본:** [Slide](previews/slides-real-ci.jpg) · [Scroll](previews/scroll-real-ci.jpg). [성공한 실행 및 8개 PC 증거](https://github.com/sh0427-han/design-template-library/actions/runs/40625146466) · 브라우저/폰트/상태 검사에 사용한 구현 커밋은 `c542d30`. 이 확인만으로 독립 Reviewer PASS 또는 디자인 승인으로 간주하지 않는다.
- Chromium 주입 기반 초기 초안 캡처: [Slide draft](previews/slides-draft.jpg), [Scroll draft](previews/scroll-draft.jpg). 실제 두 viewer 주소 및 폰트 렌더 검증 완료 프리뷰가 아니며 최종 승인은 보류한다.
- 로컬 검증: `python examples/interactive-kernel/verify_kernel.py` (Python Playwright, Node, Chromium 필요). 해당 검증은 Python 독립 계산 + 데이터 주입 기반 Chromium 실행이며 실 URL 네트워크/글꼴 로딩 여부를 대체하지 않는다.
- [Independent Reviewer 인계](review/reviewer-status.md): PENDING. 사용자의 명시적 Merge 승인 전 main에 병합하지 않는다.
