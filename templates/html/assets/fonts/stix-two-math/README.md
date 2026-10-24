# STIX Two Math · 수식 전용 서체

본문 Pretendard와 분리하여 변수·계수·수식·수식의 수치에 사용하는 로컬 웹폰트입니다. 분수·지수·아래첨자는 Native MathML이 조판하고 폰트의 OpenType `MATH` 테이블을 사용합니다.

- Family: **STIX Two Math**, Regular 400, Version **2.12 b168a**.
- 제작: [STIX Fonts Project](https://github.com/stipub/stixfonts).
- 배포 원본: [Google Fonts의 고정 Commit TTF](https://github.com/google/fonts/blob/76d97cb481958f9bb0976a453f8126f8e2ea87ab/ofl/stixtwomath/STIXTwoMath-Regular.ttf).
- 원본 TTF SHA-256: `562551b15b836e6e01d1b7350909baf3c8c8d83260c1190fbf4544333e6936de`.
- 로컬 [WOFF2](STIXTwoMath-Regular.woff2) SHA-256: `d18b6ab10cd6670ec5d4067f3ad2678a156b6b6642d9a0985243a1da729e6a95`.
- [SIL Open Font License 1.1](OFL.txt). 라이선스와 저작권을 폰트와 함께 유지합니다.

TTF의 전체 글리프와 `MATH` 테이블을 유지하고 fontTools 4.61.1의 WOFF2 형식으로 변환했습니다. 서브셋·글리프 수정·시각적 굵기 합성은 하지 않습니다. 변환에는 `brotli` 패키지가 필요합니다.

```python
from fontTools.ttLib import TTFont
font = TTFont("STIXTwoMath-Regular.ttf", recalcTimestamp=False)
assert "MATH" in font
font.flavor = "woff2"
font.save("STIXTwoMath-Regular.woff2")
```

[math-typography.css](../../../math-typography.css)를 필요한 페이지에서 명시적으로 로드합니다. 이 파일은 기존 8종에 자동 적용되지 않습니다. `math.math`와 `.math-number`는 STIX Two Math, 한글과 일반 영문·UI는 Pretendard를 사용하고 모든 텍스트의 전역 −1pt 자간을 유지합니다. CSS family만 검사하지 않고 CDP로 각 역할의 실제 글리프 폰트를 확인합니다.
