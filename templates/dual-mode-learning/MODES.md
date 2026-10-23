# 두 모드의 변환 계약

| 항목 | Scroll | Slide |
| --- | --- | --- |
| 목적 | 스스로 읽고 실험하는 PC 학습 문서 | 발표자가 개념 단위로 진행 |
| 배치 | sticky 목차 + 세로로 이어지는 5개 섹션 | 1440×810 논리 캔버스의 5장 |
| 탐색 | 목차 앵커·스크롤 | 이전/다음·방향키·PageUp/Down·Home/End·Space |
| 공통 내용 | 제목·부제·Figure·계산·필수 조건·핵심 캡션 | 동일 |
| 심화 설명 | `scrollOnly`를 캡션 위에 표시 | `display:none` |
| 실습 | 같은 필터·위치·곱·출력 계산 | 동일 컨트롤과 결과 |
| 폰트/색/간격 | 정본 토큰 상속 | 동일 |

## 학습 블록과 상태

공통 `lesson.js`의 블록 한 개를 Scroll 섹션 한 개, Slide 한 장에 대응합니다. 안정적인 ID는 `motivation`, `locality`, `pipeline`, `experiment`, `takeaway`입니다. 기존 딥링크를 유지하며, 내용을 나눌 때 ID와 순서 변경의 영향을 검토합니다.

모드 전환 링크는 현재 블록을 hash로, 실습 선택을 query로 전달합니다.

```text
slides.html?filter=average&position=4#experiment
scroll.html?filter=average&position=4#experiment
```

- `filter`: `vertical`(기본), `average`, `identity`.
- `position`: 0–8, 행 우선 순서. 4는 가운데 위치(2행 2열).
- 잘못된 필터·범위 밖/비정수 위치는 기본 필터와 첫 위치로 해석합니다.
- 조작 시 현재 URL과 다른 모드 링크를 함께 갱신합니다. 새로고침·URL 공유도 같은 선택을 복원합니다.
- Scroll은 뷰포트 상단 150px을 지난 마지막 섹션을 현재 읽는 블록으로 취급합니다. 목차의 `aria-current`와 모드 링크를 갱신합니다.
- Slide의 버튼·키보드·hashchange는 현재 장과 진행 표시, 모드 링크를 함께 갱신합니다.
- input/select/textarea/button/link/contenteditable에 포커스가 있거나 modifier 키가 눌렸으면 발표 단축키가 입력을 가로채지 않습니다.
- 새 학습 파일의 출발점인 선택 페이지는 기존 두 진입점을 연결합니다. 별도 저장소나 서버 상태는 필요하지 않습니다.

## 캔버스와 PC 창 크기

발표 UI의 상단 바 60px, 하단 컨트롤 64px을 제외한 stage를 기준으로 배율을 계산합니다. `min((stageWidth−32)/1440, (stageHeight−24)/810)`을 전체 캔버스에 적용합니다. `ResizeObserver`가 창 크기 변경을 반영하므로 긴 문장만 임의로 축소하지 않습니다. Slide의 fixed tracks와 Scroll의 읽기 배치를 서로 덮어쓰지 않습니다.

Scroll에서는 문단을 이어 읽고, 좁은 PC 창에서는 계산표를 Figure 아래로 내립니다. Slide는 한 장에 핵심 메시지 하나를 유지합니다. 정보가 넘치면 숨김 처리로 통과시키지 말고 중복 설명 제거·구성 분할을 우선합니다.

구체적인 5장 명세·수치·검수 스크립트는 [재사용 상세 명세](../../docs/DUAL_MODE_REFERENCE_REUSE.md)를 봅니다.
