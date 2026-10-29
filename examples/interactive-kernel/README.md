# CNN 필터 선택과 출력 변화 — #5 Interactive 범용성 검증

한 장의 실습을 **Scroll / Slide**로 제공한다. 두 보기는 같은 콘텐츠·상태·계산을 공유한다. 기존 8종과 이전 네 검증 사례는 보존했다.

- [Scroll](scroll.html) · [Slide](slides.html) · [설계 명세](DESIGN.md) · [D0/D1 검증](VALIDATION.md)
- 현재 실제 HTTP Chromium 프리뷰: [Scroll](previews/scroll.png) · [Slide · 항등](previews/slides.png) · [평균](previews/slides-mean.png) · [에지](previews/slides-edge.png)
- [독립 Reviewer 기록](review/reviewer-status.md) · [화면·상태 결과](review/runtime-validation.json) · [독립 수학 검산](review/arithmetic-validation.json)

7×7 입력과 3×3 커널을 뒤집지 않는 valid cross-correlation이다. Stride1, Padding0, Dilation1, Bias0, ReLU 없음 → 출력5×5. 고정 출력3행2열은 항등6, 평균51/9 ≈5.67, Sobel-x28이다. 원값 계산과 소수2자리 표시·고정±36 색 변환은 구분한다.

`model.js`는 주제별 계산, `app.js`는 단일 상태와 동기 렌더, `viewer.js`는 모드·배율·오류 복구를 담당한다. 원본 임계값 JavaScript를 범용 엔진으로 제공한다고 주장하지 않는다.

## 검증과 실행

기능 커밋 `cbf2ec93ac4921c484e56c5900cb013300b7c7c8`에서 [새 예제·이전 두 사례 CI](https://github.com/sh0427-han/design-template-library/actions/runs/40662049712)와 [원본8종·나머지 사례 전체 CI](https://github.com/sh0427-han/design-template-library/actions/runs/40662049459)가 성공했다.

로컬에서는 저장소 루트를 HTTP 서버로 제공해 위 HTML을 연다. 검증에는 Node, Python Playwright와 Chromium이 필요하다.

```sh
python examples/interactive-kernel/verify_kernel.py
python examples/interactive-kernel/verify_runtime.py
```

수학15상태/375셀, 화면8개와 필터24상태·대체입력12상태·예외7종은 서로 다른 집계다. 모든 화면은 실제 HTTP/iframe을 사용한다. `previews/validation.json`과 `*-draft.jpg`는 Chat 단계의 주입 검증 이력이며 현재 검증기가 아니다. `*-real-ci.jpg`는 이전 `c542d30`의 실제 URL 캡처로 보존한다. 당시 독립 검토 불가 기록은 현재 검토 상태와 구분한다.

독립 2차 검토 **PASS**: 1차 지적7건 모두 해결, 미해결0건. 최초 문서 충분성은 **일부 보완 필요**, D01 보완 후 검증한#5 범위에서는 충분하다.

## 재사용 범위

공통 누락D01은 일반적인 상호작용 계약과 임계값 전용 규칙의 구분1건이며, 공통 Markdown3개를 보완했다. 모순0건. 화면 배치·서체·색과 단일 상태/계산/동기화 계약을 재사용했고 필터 계산은 새로 구현했다. 기존 임계값 예제를 유지하며 별도 범용 Interaction Engine은 만들지 않았다.

Select 필터와 기존 Slider 분류 범위의 검증이다. Toggle 전이, 모바일, 다른 브라우저, 실제 스크린리더 청취, 독자 이해도·무맥락 제작자 재현은 미검증이다. main 병합과 사용자 디자인 승인은 수행하지 않았다.
