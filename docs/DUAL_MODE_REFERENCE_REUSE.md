# 기존 8개 원본을 Scroll / Slide 두 보기로 연결

## 역할과 최종 출력

디자인은 기존 `templates/html/`의 8개 레퍼런스가 담당하고, `templates/dual-mode-learning/`은 보기와 탐색만 담당합니다. 출력은 **Scroll과 Slide 두 개**입니다. 실습은 #5의 내용이며 세 번째 형식이 아닙니다.

별도의 5장 CNN 도식·스타일·고정 필터 계산 엔진을 제거했습니다. `dual-mode-process-slide.jpg`와 `dual-mode-lab-slide.jpg`는 필요하지 않습니다. 대표 프리뷰는 [Scroll](../previews/dual-mode-scroll.jpg), [Slide](../previews/dual-mode-slide.jpg) 두 개만 생성합니다. 모드 선택용 index 페이지도 제거했고 갤러리에서 두 보기로 직접 연결합니다.

## 하나의 디자인 원본

[lesson.js](../templates/dual-mode-learning/assets/js/lesson.js)는 아래 원본의 경로와 ID만 관리합니다. [공통 렌더러](../templates/dual-mode-learning/assets/js/render.js)는 같은 origin의 실제 HTML을 iframe으로 표시합니다. 화면에 JPG를 붙이거나 제목·카드·그림을 다른 CSS로 재구현하지 않습니다. 원본의 JS/Canvas/SVG도 그대로 실행합니다.

| 번호·ID | 같은 원본 | 그대로 유지하는 핵심 구성·계산 |
| --- | --- | --- |
| 01 `ref-concept` | [concept.html](../templates/html/concept.html) | 사과·4×4 픽셀·선택 RGB/HEX·H×W×3. 실제 이미지에서 계산 |
| 02 `ref-process` | [process.html](../templates/html/process.html) | INPUT→FEATURE→TASK→OUTPUT. 실제 고정 필터 맵과 별도 예시 확률 66.5/24.5/9.0% |
| 03 `ref-comparison` | [comparison.html](../templates/html/comparison.html) | 규칙 기반/머신러닝의 준비·예측 대칭, 동일 입력, 세 비교 행과 장점/한계 |
| 04 `ref-step-by-step` | [step-by-step.html](../templates/html/step-by-step.html) | 5×5·3×3·3×3, 원소별 곱 9개, 합 −6, 출력 위치 대응 |
| 05 `ref-interactive` | [interactive.html](../templates/html/interactive.html) | 실제값별 점수, 임계값, 판정·혼동행렬·Precision/Recall 동시 갱신 |
| 06 `ref-architecture` | [architecture.html](../templates/html/architecture.html) | Input 64×64×3→2개Conv Block→Flatten 8,192→FC 3 logits→Softmax |
| 07 `ref-experiment` | [experiment.html](../templates/html/experiment.html) | TP4 FP1 / FN2 TN5, 75.0/80.0/66.7/72.7%와 공식 |
| 08 `ref-executive-summary` | [executive-summary.html](../templates/html/executive-summary.html) | 세 지표의 원래 단위·정규화·감소율, 세 후속 조치 |

전체 수치·조건·의미는 [REFERENCE_PAGE_SPECS.md](REFERENCE_PAGE_SPECS.md), [TEMPLATE_CATALOG.md](../TEMPLATE_CATALOG.md)를 정본으로 봅니다. 이 문서에서 다른 버전의 데이터를 만들지 않습니다. #1 PR #15를 포함해 사용자 검토를 마친 8개 원본을 동일하게 재사용합니다. 원본의 배치·수치·그림을 보기 전용으로 다시 설계하지 않습니다. 최신 출처는 [검토 완료 상태](REFERENCE_RELEASE_STATUS.md)를 확인합니다.

## 원본 서식을 바꾸지 않는 배치

원본을 직접 1600×950에서 열면 캔버스는 1440×810입니다. 보기는 이 캔버스를 정확히 유지하고 부모가 가용 공간에 맞춰 균일 배율을 적용합니다.

iframe 안에서는 아래 바깥 배치만 보정합니다.

```css
html, body { min-height:0; width:1440px; height:810px; overflow:hidden; background:transparent; }
.reference-deck { padding:0; min-height:0; }
.reference-slide { zoom:1; }
```

이는 카드·제목·수식·행렬·화살표·푸터의 서식을 덮어쓰는 규칙이 아닙니다. 원본 49px 제목·21px 부제·54/66/30px 기본 패딩 및 페이지별 예외도 그대로 유지합니다. 앞서 추가했던 44px 제목·40/58/28px 패딩·별도 Footer 규격은 제거했습니다. 원본의 로컬 Pretendard와 전역−1pt를 그대로 사용합니다.

바깥 UI의 공통 토큰은 [styles.css](../templates/html/styles.css)를 상속합니다. 보기 전환 바 44px, Slide 하단 컨트롤 44px, 프레임 16:9/radius10px/공통 shadow를 사용합니다. Scroll은 목차 200px·gap24px·외곽 24px·원본 사이 32px입니다. Slide 프레임 폭은 `min(1440px,100vw−40px,(100vh−112px)×16/9)`입니다. `ResizeObserver`는 프레임 폭/1440의 배율을 적용하며 개별 텍스트를 줄이지 않습니다.

## 조작·현재 위치·원본 갱신

모드와 원본을 같은 정적 서버에서 실행합니다. 상대 경로의 원본을 사용하므로 이미지·폰트·공통 JS의 URL을 복사하거나 재작성하지 않습니다. `python -m http.server 8000` 후 [Scroll](../templates/dual-mode-learning/scroll.html) 또는 [Slide](../templates/dual-mode-learning/slides.html)를 엽니다.

`?threshold=80#ref-interactive`는 현재 #5와 임계값 80을 나타냅니다. 원본 input 이벤트로 계산하며, 보기 쪽 코드는 정수 0–100의 선택값을 전달합니다. 모드 왕복/새로고침 시 같은 판정·행렬을 복원합니다. 별도 실습 엔진을 만들지 않습니다. 임계값의 기본 60·양성 조건score≥threshold·분모 0의 정의 불가 처리도 원본을 따릅니다.

본문/그림에 포커스가 있는 상태에서도 Slide 단축키가 동작하며, 입력/버튼/링크를 조작하는 키는 가로채지 않습니다. Scroll의 현재 섹션과 mode 링크, Slide의 현재 장과 진행 표시를 함께 갱신합니다. ID와 과거 anchor 매핑은 [MODES.md](../templates/dual-mode-learning/MODES.md)에 기록합니다.

## 실제 Chromium 검증

[verify_pretendard.py](../scripts/verify_pretendard.py)가 [verify_dual_mode.py](../scripts/verify_dual_mode.py)를 실행합니다.

1. 원본 8개를 직접 렌더링하고 모든 표시 요소의 글꼴·크기·굵기·행간·자간·색·배경·radius·padding 및 캔버스 기준 bounding box를 기준값으로 수집합니다.
2. PC 1600×950/1440×810/1366×768/1280×720 × 두 모드 ×8개 = **64개 화면**을 원본과 대조합니다. 동일 CSS라는 선언만으로 통과하지 않으며 실제 style과 상대 위치를 비교합니다. style은 정확히 일치해야 하며 HTML 위치 오차는0.3px 미만, 폰트의 실제 경계와 중앙 보정에 영향을 받는 SVG 위치 오차는 기존 도식 정렬 기준에 맞춰1px 미만입니다. 실제 최대 오차와 허용값을 JSON에 기록하며 글자 크기·padding 차이를 이 오차로 허용하지 않습니다.
3. 원본 내부의 잘림·Footer 겹침·화살표, 부모 프레임의 16:9·경계·가로 넘침을 검사합니다.
4. iframe 안의 실제 글리프를 CDP로 확인하고 `document.fonts`의 한글/영문 로딩, 모든 텍스트의−1pt를 확인합니다.
5. 기존 페이지별 기술 검산을 사용해 픽셀·맵·Softmax·−6 계산·슬라이더 21상태·CNN Shape·지표·KPI를 확인합니다. #2의 원본 전용 최소 크기 검사는 직접 렌더링에 적용하고, iframe에서는 실제 서식/위치 동일성과 독립 맵/확률 계산을 확인합니다.
6. #5의 비기본값 80을 유지한 두 모드 왕복·새로고침, 입력 포커스 보호, iframe 키보드 탐색, 목차에서 모드 전환, 잘못된 threshold 기본값을 검사합니다.
7. 갤러리·부모 UI도 네 PC 크기의 실제 폰트·가로 경계와 이미지 로딩을 검사합니다.

[검증 JSON](../previews/review/dual-mode-validation.json)에 결과와 실제 원본/보기 소스 해시를 기록합니다. 전체 검토 PNG는 `/tmp/dual-mode-review/`에 생성하여 CI artifact에 보관합니다. 저장소의 canonical JPG는 두 모드의 1600×950 캡처 두 개뿐입니다. 중간 #5 캡처는 QA evidence일 뿐 세 번째 출력이나 대표 preview가 아닙니다.

## 다른 개념으로 재사용

이 보기는 기존 8개 레퍼런스의 서식을 직접 비교하기 위한 예제입니다. 실제 새 강의는 [재사용 워크플로](REFERENCE_REUSE_WORKFLOW.md)에 따라 필요한 유형만 선택합니다. 모든 강의에 8장을 강제하거나 iframe을 유일한 구현법으로 강제하지 않습니다. 어떤 구성 방식을 쓰든 원본에서 승인된 Typography·간격·카드·도식 규칙을 사용하고, 콘텐츠·수식·계산의 단일 소스와 Scroll/Slide 두 출력을 유지합니다.
