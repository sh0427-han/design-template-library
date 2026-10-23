# Scroll / Slide 두 보기

| 항목 | Scroll | Slide |
| --- | --- | --- |
| 콘텐츠 | `templates/html/`의 같은 8개 원본 | 동일 |
| 화면 | 목차 옆에 원본을 연속 배치 | 원본 한 장씩 표시 |
| 입력·계산 | 원본 #5 슬라이더와 JavaScript | 동일 |
| 탐색 | 스크롤·목차 앵커 | 이전/다음·방향키·PageUp/Down·Home/End·Space |
| 대표 프리뷰 | `dual-mode-scroll.jpg` | `dual-mode-slide.jpg` |

실습 전용 출력과 별도의 5장 CNN 강의는 없습니다. HTML 진입점·대표 JPG는 각각 두 개입니다.

## URL과 상태

```text
scroll.html?threshold=80#ref-interactive
slides.html?threshold=80#ref-interactive
```

레퍼런스 ID는 `ref-concept`, `ref-process`, `ref-comparison`, `ref-step-by-step`, `ref-interactive`, `ref-architecture`, `ref-experiment`, `ref-executive-summary`입니다.

- 현재 레퍼런스는 hash, #5의 임계값은 정수 query `threshold=0…100`입니다. 기본값은 원본과 같은 60, 잘못된 값은 60으로 해석합니다.
- 조작은 원본 슬라이더의 input 이벤트/계산을 그대로 사용합니다. 보기 코드는 선택값을 URL과 반대 모드 링크에 전달합니다.
- 모드 왕복·새로고침·공유 링크에서 현재 예제와 임계값을 복원합니다.
- Scroll은 위쪽 140px을 지난 마지막 섹션을 현재 읽는 예제로 취급합니다. 목차 `aria-current`와 Slide 링크를 갱신합니다.
- Slide는 버튼·키보드·해시로 바꾼 예제와 진행 표시를 함께 갱신합니다.
- iframe 안에 포커스가 있어도 탐색키가 동작합니다. input/select/textarea/button/link/contenteditable과 modifier 키는 가로채지 않습니다.

이전 5장 데모의 `#motivation`, `#locality`, `#pipeline`, `#experiment`, `#takeaway`는 각각 Concept, Step-by-Step, Process, Interactive, Comparison으로 연결합니다. 새 #7 지표는 `#ref-experiment`로 구분합니다. 제거한 고정 필터 실습의 filter/position query는 새 슬라이더의 의미로 바꾸지 않습니다.

## 배율·준비 상태

원본은 1440×810 내부 뷰포트에서 실행하며 캔버스 바깥 gutter/zoom만 제거합니다. 부모가 전체 iframe에 동일 배율을 적용합니다. 각 텍스트나 그림의 폰트·간격·크기를 보기별로 바꾸지 않습니다. `ResizeObserver`가 실제 프레임 폭을 반영합니다.

Scroll의 원본은 lazy loading, Slide는 선택한 장을 처음 방문할 때 로드하고 이후 같은 iframe을 유지합니다. 폰트와 이미지를 기다린 뒤 준비 상태를 표시합니다. 두 모드와 원본은 같은 정적 서버/origin에서 실행합니다.

구체적인 source 경로·기술 검증·서식 비교는 [재사용 명세](../../docs/DUAL_MODE_REFERENCE_REUSE.md)에 있습니다.
