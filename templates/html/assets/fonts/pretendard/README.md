# Pretendard Variable v1.3.9

이 폴더는 #5 Interactive의 CDN 연결 여부에 따른 글꼴 변경을 막기 위해 원본 배포 파일을 보관합니다. 폰트 바이트는 변경하지 않았습니다. 기존 `--font-sans`와 `Pretendard Variable` family 이름을 유지합니다.

- 배포 원본: https://github.com/orioncactus/pretendard/tree/v1.3.9/packages/pretendard/dist/web/variable
- 다운로드 URL: https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/packages/pretendard/dist/web/variable/woff2/PretendardVariable.woff2
- 버전: Pretendard v1.3.9
- 파일 크기: 2,057,688 bytes
- SHA-256: `9599f12fd42fc0bce1cd50b47a0c022e108d7aa64dd0d1bb0ed44f3282d900b4`
- 라이선스: [SIL Open Font License 1.1](LICENSE), Copyright (c) 2021 Kil Hyung-jin, Reserved Font Name Pretendard
- 라이선스 원본: https://github.com/orioncactus/pretendard/blob/v1.3.9/LICENSE

`interactive.html`은 이 WOFF2를 직접 참조합니다. 공통 CSS나 다른 슬라이드의 로딩 방식은 바꾸지 않습니다. #5를 다른 위치로 복사할 때 HTML·JS·공통 CSS와 함께 이 폴더를 복사합니다.

`scripts/check_interactive.py`는 공유용 `previews/review/interactive-live.html`에 이 폰트를 data URL로 포함하고 라이선스 전문을 HTML 주석으로 함께 보존합니다. 이 파일 하나를 열면 네트워크 없이 같은 폰트를 사용할 수 있습니다. 생성 HTML은 원본보다 약 2.7MB 커지는 대신 별도 폰트 설치와 CDN 연결이 필요하지 않습니다.

검증은 CSS family 이름뿐 아니라 Chromium `CSS.getPlatformFontsForNode`의 실제 렌더링 글꼴을 확인합니다. 배포 파일 교체 시 해시·라이선스·검증 결과를 함께 갱신합니다.
