# 과적합과 일반화 · 개념 한 장

머신러닝 입문자를 위한 HTML Scroll / Slide. 과적합은 학습 데이터의 특성·잡음에 지나치게 맞춰 새 데이터 성능이 저하되는 현상, 일반화는 학습에 쓰지 않은 데이터에서도 잘 동작하는 능력으로 설명한다. 검증 손실은 일반화 성능을 살펴보는 단서이며 독립 테스트 결과와 구분한다.

- [Scroll 원본](scroll.html) · [Slide 원본](slides.html) · [두 모드 공통 콘텐츠](content.html)
- [설계 명세와 규칙 출처](DESIGN.md) · [D0/D1 재사용성 판정](VALIDATION.md)
- [독립 검토 1차](review/round-1.md) · [2차](review/round-2.md) · [3차 최종](review/round-3.md)

설명용 41점 곡선이며 실제 실험 결과가 아니다. 두 곡선은 같은 손실 정의·단위·표본별 평균·평가 조건을 사용한다. 학습 손실 감소가 검증 손실 상승을 항상 뜻하지 않으며, 격차만으로 과적합을 확정하지 않는다. 모델 학습·알고리즘 구현·계산 장·실습은 포함하지 않는다.

## 실행과 검증

저장소 루트에서 `python -m http.server 8000` 실행 후 `/examples/overfitting-generalization/scroll.html` 또는 `slides.html`로 연다. `content.html`을 iframe 안의 1440×810 공통 원본으로 사용하고 뷰어는 전체 배율과 탐색만 담당한다. 폰트·공통 CSS는 `templates/html/`의 로컬 자산을 그대로 참조한다.

```bash
python scripts/verify_overfitting.py --static
python scripts/verify_overfitting.py
```

PC 1600×950/1440×810/1366×768/1280×720의 두 모드, 실제 Pretendard/STIX 글리프와−1pt, 카드 패딩/대응행, SVG 경계/좌표, 콘솔·요청 오류, 모드 서식 동일성, 다른 설명용 데이터와 잘못된 데이터 거부를 검사한다. 로컬 sandbox의 소켓/Chromium 제한이 있으면 [전용 Actions](../../.github/workflows/validate-overfitting.yml)에서 실행한다. 실행 결과를 확인하기 전에는 통과로 보지 않는다.

#3 Comparison의 대칭 White/대응행을 주요 재사용하고 #8의 동일 기준/축/범례 원칙만 일부 적용했다. 나머지 패턴의 타주제 재사용은 검증하지 않았다. 공통 시각 지침과 원본 8종을 수정하지 않는다. 실제 결과·프리뷰 링크는 VALIDATION의 D1 기록에 연결한다.


## 실제 프리뷰

- [Slide 이미지](previews/slide.png) · [Scroll 이미지](previews/scroll.png) · [PC8화면](review/contact.jpg)
- [실제Chromium 검증보고서](previews/validation.json) · [실행/원해상도 artifact](https://github.com/sh0427-han/design-template-library/actions/runs/40254384669)
- [브라우저 Slide](https://raw.githack.com/sh0427-han/design-template-library/9f49042e0ddfdc76eea6bf2e3e555869462b2d83/examples/overfitting-generalization/slides.html) · [브라우저 Scroll](https://raw.githack.com/sh0427-han/design-template-library/9f49042e0ddfdc76eea6bf2e3e555869462b2d83/examples/overfitting-generalization/scroll.html)

브라우저 링크는 동일콘텐츠의 불변 구현커밋을 보여주는 외부CDN 보기다. CDN 접근이 제한되면 위의 실제PNG와 로컬서버 진입점을 사용한다. PNG는 실제 Chromium155 렌더링이며 HTML에 붙여넣은 대체그림이 아니다.
