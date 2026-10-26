# 과적합과 일반화 · 개념 한 장

머신러닝 입문자를 위한 HTML Scroll / Slide. 과적합은 학습 데이터의 특성·잡음에 지나치게 맞춰 새 데이터 성능이 저하되는 현상, 일반화는 학습에 쓰지 않은 새 데이터에서도 잘 동작하는 능력으로 설명한다.

- [Scroll](scroll.html) · [Slide](slides.html) · [두 모드의 공통 원본](content.html)
- [설계와 규칙 출처](DESIGN.md) · [D0/D1 및 사용자 개정 기록](VALIDATION.md)
- [현재 Chromium 보고서](previews/validation.json) · [Slide PNG](previews/slide.png) · [Scroll PNG](previews/scroll.png) · [PC 8화면](review/contact.jpg)

왼쪽은 검증 손실 최소의 **Best model**과 이후 학습 손실 감소·검증 손실 상승의 **과적합 구간**을 보여준다. 선택은 표시한 체크포인트의 검증 기준이며 독립 테스트 최적을 보장하지 않는다. 오른쪽은 학습 이미지와 외양이 다른 새 이미지의 예측 관계다. 손실의 뜻은 그래프 안에서 설명하고, 부제·볼드는 과도 적합에 따른 새 데이터 성능 저하와 일반화를 대비한다. 일반화 정의는 한 줄이다. 정의 카드 제목/본문의 실제 서식은 #3 원본과 대조한다.

그래프는 설명용 41점·2계열이며 실제 실험 결과가 아니다. 두 계열은 같은 손실 정의·단위·표본별 평균·평가 조건을 사용한다. 학습 손실 감소가 항상 검증 손실 상승을 뜻하지 않으며, 격차만으로 과적합을 확정하지 않는다. 이미지 그림도 학습·추론을 실행한 결과가 아닌 개념도다. 학습 이미지3개와 새 A(노란색·기울어진 사과)/B(굴곡·기울어진 토마토), 같은 모델, 예측 라벨을 편집 가능한 SVG로 연결한다. y축 이름은 축 중앙 왼쪽에−90° 회전하고, x축 이름은 중앙 아래에 두며 실제 글자 경계 간격8px를 유지한다.

## 실행 및 검증

저장소 루트에서 `python -m http.server 8000` 실행 후 `/examples/overfitting-generalization/scroll.html` 또는 `slides.html`을 연다. 두 보기 모두 같은 1440×810 원본을 전체 배율만 바꾸어 표시한다. 공통 CSS와 로컬 Pretendard/STIX 폰트는 `templates/html/`를 참조한다.

```bash
python scripts/verify_overfitting.py --static
python scripts/verify_overfitting.py
```

PC 1600×950/1440×810/1366×768/1280×720 × 두 모드를 검사한다. 실제 글리프·−1pt·패딩·SVG 경계·82개 곡선 좌표·그림의 입력/예측 대응·연결·축 이름의 공통 정렬·모드 동일성·콘솔/요청 오류·변경/오류 데이터를 확인한다. 로컬 소켓 제한이 있으면 [전용 Actions](../../.github/workflows/validate-overfitting.yml)에서 실행한다.

#3 Comparison의 대칭 및 준비/적용 관계, #8의 동일 기준·축 원칙 일부를 사용한다. 사용하지 않은 패턴의 타주제 재사용은 검증하지 않았다. 기존 8종 원본은 보존한다. 축 이름의 정렬은 사용자 요청에 따라 [Figure 표준 §6](../../docs/FIGURE_PRODUCTION_STANDARD.md#그래프-축-이름의-공통-정렬)과 공통 [graph-annotations.js](../../templates/html/graph-annotations.js)에 명시했다. 종전 D0/D1의 공통 보완 0건은 당시 범위의 기록이며, 이번 확장 기준에서는 공통 문서 1건을 보완했다.

[현재 전용 Chromium 실행](https://github.com/sh0427-han/design-template-library/actions/runs/40272864640) · [전체 회귀](https://github.com/sh0427-han/design-template-library/actions/runs/40272864649)

[브라우저 Scroll](https://raw.githack.com/sh0427-han/design-template-library/d09aa69265225658f1ca2943396410c820ee66af/examples/overfitting-generalization/scroll.html) · [브라우저 Slide](https://raw.githack.com/sh0427-han/design-template-library/d09aa69265225658f1ca2943396410c820ee66af/examples/overfitting-generalization/slides.html)

브라우저 링크는 같은 원본을 제공하는 외부 CDN이다. 접속이 제한되면 실제 PNG 또는 위 로컬 서버 진입점을 사용할 수 있다. 원해상도 화면은 Actions artifact에 보관한다. 이전 버전의 검토 기록은 Git 이력과 VALIDATION에 구분하여 남긴다.
