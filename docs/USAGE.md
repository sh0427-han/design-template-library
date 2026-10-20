# How to use this library

## 1. HTML 미리보기

`templates/html/index.html`을 브라우저에서 열면 각 디자인 샘플로 이동할 수 있습니다. HTML 내용은 각 페이지에서, 색·간격·글꼴은 `styles.css`에서 수정합니다.

## 2. PowerPoint 수정·재생성

`templates/pptx/technical-slide-templates.pptx`는 편집 가능한 슬라이드 3장입니다. PPT 프로그램에서 텍스트와 도형을 직접 수정할 수 있습니다.

재생성 시:

```bash
python -m pip install -r templates/pptx/requirements.txt
python templates/pptx/build_templates.py
```

생성 코드는 동일한 이름의 PPTX를 새로 저장하므로 직접 수정한 PPTX는 미리 백업해야 합니다.

## 3. ChatGPT 요청 예시

> `https://github.com/sh0427-han/design-template-library`의 `process` 템플릿과 `DESIGN_SYSTEM.md`를 참조하여 CNN 아키텍처 설명 슬라이드 2장을 만들어줘. 기존 강의자료의 스타일·순서를 우선하고, 템플릿을 적용하기 전에 실제 파일을 확인해줘.

## 4. Codex 연동

다른 프로젝트의 `AGENTS.md`에 다음 부분을 넣을 수 있습니다.

```md
## Slide design reference

Reference repo: https://github.com/sh0427-han/design-template-library
Read DESIGN_SYSTEM.md and TEMPLATE_CATALOG.md (if accessible) before adding
PPT/HTML slide designs. Preserve this project's existing layout and content
requirements. Do not edit the reference repo unless asked.
```

**참고:** 경로를 기재하는 것만으로 다른 계정/저장소 접근 권한이 자동 부여되지는 않습니다.

## 5. 신규 템플릿 등록

1. 사용 목적과 ID(`kebab-case`) 확정
2. 원본 HTML/PPT 작성
3. 16:9 화면 렌더링 및 텍스트 잘림 검사
4. `previews/`에 실제 PNG 캡처 반영
5. `TEMPLATE_CATALOG.md`의 목록과 선택 기준 갱신

외부 Figure를 활용한 경우 미리보기 또는 해당 원본 근처에 원문 출처 URL을 작성합니다.

## Global character spacing

- Entire library standard: **condensed 1.0 pt** (`-1pt`), for headings, body, labels, footnotes and gallery.
- HTML: shared `--character-spacing` CSS token; do not use per-component exceptions.
- PPTX: `CHARACTER_SPACING_PT` is applied in the common `textbox()` helper to every editable run; inspect `a:rPr@spc="-100"` after regeneration.
- Review previews after changing spacing: word wrapping and line breaks can change.


## 6. Scroll / Slide 이중 모드 실행

```bash
# repository root
python -m http.server 8000
```

브라우저에서 `http://localhost:8000/templates/dual-mode-learning/index.html`에 접속합니다.

- Scroll: 왼쪽 목차/세로 스크롤/상세 설명/필터 실습
- Slide: 16:9, 이전/다음 버튼, 화살표, PageUp/PageDown, URL hash
- 동일한 `assets/js/lesson.js`와 `assets/js/lab.js`를 사용합니다.
- 공통 테마는 `templates/html/styles.css`에서 상속하며 문자 간격은 모두 -1pt입니다.


## 7. 통합 갤러리

[HTML 갤러리](../templates/html/index.html)에서 기본 3종과 Dual-mode 예시를 함께 확인할 수 있습니다. 기본 3종에는 편집 가능한 PPTX가 있으며, 새 인터랙티브 5장은 HTML/CSS/JavaScript 기반이고 PPTX 버전은 아직 없습니다. 모든 예시는 계속 개선합니다.
