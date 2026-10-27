# 분류 임계값과 성능 변화

Vision AI·머신러닝 입문자를 위한 개념 1장과 임계값 실습 1장이다. 불량을 양성, 정상을 음성으로 정의하며 설명용 합성 점수를 사용한다. 보정된 확률이나 실제 생산 성능이 아니다.

- [Scroll](scroll.html) · [Slide](slides.html)
- [공통 콘텐츠](content.html) · [공통 상태와 표시](app.js) · [계산](model.js) · [합성 데이터](data.json)
- [D0 설계와 규칙 출처](DESIGN.md) · [D0/D1 재사용 검증](VALIDATION.md)

저장소 루트에서 `python -m http.server 8000`을 실행한 뒤 `http://localhost:8000/examples/threshold-metrics/scroll.html` 또는 `slides.html`을 연다. 폰트·CSS·콘텐츠·데이터를 같은 서버에서 읽으므로 HTML 파일을 `file:`로 직접 열지 않는다.

주소 예: `slides.html?v=1&dataset=default&threshold=50#practice`. 임계값은 정수0~100을100으로 나눠 표시한다. 임계값과 점수가 같으면 불량으로 예측한다. 조작·모드 전환·새로고침 시 데이터셋·임계값·현재 장을 URL로 복원한다. 데이터셋 교체는 샘플 자체를 바꾸는 조작이며 임계값 변경은 실제값·점수·샘플 위치를 바꾸지 않는다.

#5 Interactive에서 고정 실제값과 단일 상태의 예측·집계 갱신을, #7 Experiment에서 혼동행렬 축과 동일 개수로 계산한 네 지표의 뜻·일반식·대입 대응을 재사용했다. 원본6개 샘플 목록과2×2 지표 배치를 그대로 복제하지 않았다. 기존8종과 이전 세 예제는 변경하지 않는다.

백분율만 소수 첫째 자리로 반올림한다. 원래 분수를 계산에 사용하며 F1을 반올림한 Precision/Recall에서 다시 계산하지 않는다. 분모가0이면 `—`와 같은 지표 안의 조건을 표시한다. 빈 평가 집합도 모든 지표가 정의되지 않는다.

검증 명령은 `python scripts/verify_threshold_metrics.py --static` 및 `python scripts/verify_threshold_metrics.py`다. 실제 Chromium 검사·16개 PC 화면·상태 시나리오·독립 Reviewer 결과는 VALIDATION.md와 검증 보고서에 별도로 기록했다. 모바일/태블릿, 실제 모델 학습, 실제 스크린리더 청취와 독립 독자의 이해도 실험은 범위에 포함하지 않는다.

## 완성 프리뷰와 결과

기능 원본은 `cf17bdcc2d7961e2d3d1680bb3c5cbc6cb3dbb4a`로 고정했다. 두 보기는 같은 콘텐츠/계산/상태를 사용한다. 아래 CDN 링크의 외부 접속은 실행 환경의 CONNECT403 제한 때문에 직접 확인하지 못했으며, 실제 Chromium PNG와 저장소 원본/로컬 서버 경로를 함께 제공한다.

- [Scroll 브라우저](https://raw.githack.com/sh0427-han/design-template-library/cf17bdcc2d7961e2d3d1680bb3c5cbc6cb3dbb4a/examples/threshold-metrics/scroll.html) · [Slide 브라우저](https://raw.githack.com/sh0427-han/design-template-library/cf17bdcc2d7961e2d3d1680bb3c5cbc6cb3dbb4a/examples/threshold-metrics/slides.html)
- 개념 장: [Slide PNG](previews/slides-concept.png) · [Scroll PNG](previews/scroll-concept.png)
- 실습 장: [Slide PNG](previews/slides-practice.png) · [Scroll PNG](previews/scroll-practice.png)
- [16화면 contact](review/contact.jpg) · [로컬 Chromium/독립 계산 보고서](previews/validation.json) · [CI Chromium/과적합 회귀](review/ci-validation.json) · [전달 상태/CI](review/delivery.json)
- [독립 1차 지적](review/reviewer-round1.json) · [수정 후 독립 2차](review/reviewer-round2.json) · [PR #23](https://github.com/sh0427-han/design-template-library/pull/23)

화면은4PC×2모드×2장=16개이며, 임계값404상태·추가20상태는 별도 숫자다. 원해상도16개 PNG는 [전용 Actions](https://github.com/sh0427-han/design-template-library/actions/runs/40500963756)의 `threshold-metrics-browser-evidence` artifact에도 보관한다. 로컬 `review/screens/`는 재생성 산출물이므로 Git에서 제외한다.

이번 공통 MD 누락0·모순0·보완0건이며, 구현/문구 오류는 기존 규칙 적용 오류로 수정했다. 독립1차 중간 지적1건(오탐/미탐 절충의 직접 설명)을 수정하고2차에서 미해결0건을 확인했다. #5 상태·조작 계약과 #7 행렬·네 지표 계약 각각 범위 안에서 **충분**으로 평가한다. 이 예제는 네 번째 검증 산출물이며 아홉 번째 원본 템플릿이 아니다.
