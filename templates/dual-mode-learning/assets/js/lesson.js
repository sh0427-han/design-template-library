// One content source; figures and numbers come from lab.js in both modes.
export const lesson = {
  topic: 'CNN의 Convolution 이해하기',
  subtitle: '입력 영역, 필터 계산, Feature Map으로 이어지는 다섯 단계',
  sections: [
    {
      id: 'motivation', eyebrow: '01 · CONCEPT', kind: 'motivation',
      title: '주변 픽셀에서 패턴 찾기',
      lead: '한 픽셀의 값보다 이웃한 픽셀의 관계를 함께 살펴보는 이유',
      detail: '단일 채널의 설명용 5×5 수치 배열입니다. 실제 사진의 픽셀을 측정한 값은 아닙니다.',
      scrollOnly: '사진은 일반적으로 R·G·B 세 채널을 갖습니다. 여기서는 국소 연산에 집중하도록 한 채널만 다룹니다. 숫자는 밝기의 관계를 설명하기 위한 예시이며, 실습 결과는 이 배열에서 직접 계산합니다.',
      takeaway: '작은 입력 영역을 함께 계산하면 주변의 밝기 변화에 반응할 수 있습니다.',
    },
    {
      id: 'locality', eyebrow: '02 · STEP-BY-STEP', kind: 'locality',
      title: '필터의 곱셈과 합산',
      lead: '입력의 좌상단 3×3 영역과 같은 크기의 커널을 곱해 출력 한 칸을 계산',
      detail: 'Stride 1 · Padding 0 · Bias 0 · 커널 반전 없음. 오른쪽으로 한 칸 이동한 다음 출력값은 9입니다.',
      scrollOnly: 'CNN 라이브러리에서 흔히 쓰는 cross-correlation 관례로 계산합니다. 대응하는 원소 9쌍을 곱한 뒤 더하며, 가중치가 0인 항도 계산에 포함됩니다. 모든 위치에 같은 커널을 적용하는 것이 가중치 공유입니다.',
      takeaway: '입력의 선택 영역과 출력의 선택 셀은 같은 위치의 계산으로 연결됩니다.',
    },
    {
      id: 'pipeline', eyebrow: '03 · PROCESS', kind: 'flow',
      title: '입력에서 Feature Map까지',
      lead: '5×5 입력에 3×3 커널을 한 칸씩 적용하면 3×3 결과를 생성',
      detail: '선택 영역은 왼쪽에서 오른쪽으로, 다음 행으로 이동합니다. 각 출력 셀에는 해당 영역의 곱셈·합산 결과를 기록합니다.',
      scrollOnly: '출력 한 변의 크기는 (N + 2P − K) / S를 아래 정수로 내림한 뒤 1을 더한 값입니다. N은 입력 크기, P는 zero-padding 폭, K는 커널 크기, S는 stride입니다. 이번 예제는 (N,P,K,S)=(5,0,3,1)이므로 출력은 3×3입니다.',
      takeaway: '커널을 바꾸지 않고 입력 전체를 훑어 하나의 Feature Map을 만듭니다.',
    },
    {
      id: 'experiment', eyebrow: '04 · INTERACTIVE', kind: 'lab',
      title: '필터와 위치에 따른 계산 변화',
      lead: '필터 또는 입력 위치를 바꾸며 원소별 곱, 합계, 출력 셀을 함께 확인',
      detail: '파란 테두리는 현재 입력 영역, 진한 셀은 대응하는 출력입니다. Stride 1 · Padding 0 · Bias 0.',
      scrollOnly: '평균 필터는 원소별 곱의 합을 9로 나누며, 세로 경계 필터와 중앙 픽셀 필터는 나누지 않습니다. 이 실습은 선택한 고정 필터의 계산이며 학습된 CNN의 추론 결과가 아닙니다.',
      takeaway: '위치를 바꾸면 입력 영역이, 필터를 바꾸면 계산에 쓰는 가중치가 달라집니다.',
    },
    {
      id: 'takeaway', eyebrow: '05 · COMPARISON', kind: 'summary',
      title: '같은 입력, 서로 다른 응답',
      lead: '같은 5×5 입력에 평균·세로 경계·중앙 픽셀 필터를 각각 적용한 결과',
      detail: '세 결과는 모두 고정 필터의 실제 계산입니다. 색은 양수 Blue / 음수 Amber / 0 Muted이며 각 셀의 수치로 비교합니다.',
      scrollOnly: '평균은 주변 값의 평균을, 세로 경계 필터는 좌우 값의 차이를, 중앙 픽셀 필터는 선택 영역의 중앙 값을 반환합니다. 중앙 픽셀 통과는 median(중앙값) 필터와 다릅니다. 실제 CNN에서는 여러 입력 채널의 응답을 합산하며 필터의 가중치를 학습으로 결정합니다.',
      takeaway: '필터의 가중치가 달라지면 같은 입력에서도 서로 다른 Feature Map이 나옵니다.',
    },
  ],
};
