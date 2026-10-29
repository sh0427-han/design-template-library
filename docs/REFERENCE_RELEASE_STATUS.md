# 8종 레퍼런스 검토 완료 상태

<!-- documentation-role:start -->
> **문서 역할:** 시점별 배포·검토 상태 기록. 과거 승인·실행 결과는 현재 checkout의 신규 검증이나 새 변경의 승인으로 승계되지 않습니다.
> [정본 위치·규칙 강도·현행/이력 구분](DOCUMENTATION_MAP.md)
<!-- documentation-role:end -->

8개 디자인 예제는 모두 사용자 검토를 마쳤습니다. 이 문서는 **현재 출처·보관할 결과·이후 작업의 기준**을 기록합니다. 초기 통합 이력은 [2026-10-22 기록](INTEGRATION_REPORT_2026-10-22.md), 실제 데이터·배치는 [페이지 명세](REFERENCE_PAGE_SPECS.md)가 담당합니다.

## 기준 소스

최초 문서 정리의 역사적 기준은 `main`의 **`889cc6e30fc7b8a957bce315207f9f856f37cd45`**입니다. 아래 PR은 모두 이 커밋에 반영되어 있습니다. 그 시점에는 승인된 8종 HTML/CSS/JS를 다시 설계하지 않았습니다.

| 번호 | 최종 소스와 프리뷰 | 구현 출처 | 유지할 핵심 계약 |
| --- | --- | --- | --- |
| 01 | [Concept](../templates/html/concept.html) · [PNG](../previews/html-concept.png) | #15 | 실제 RGB 채널 → 같은 ROI → 16픽셀/48성분 → 선택 RGB/HEX. 원본과 표시색 분리 |
| 02 | [Process](../templates/html/process.html) · [PNG](../previews/html-process.png) | #9→#12, #13, #18 | 4단계 역할·고정 필터 맵/예시 확률의 구분. 외부 연결은 카드 전체 중앙 |
| 03 | [Comparison](../templates/html/comparison.html) · [PNG](../previews/html-comparison.png) | #9→#12, #14 | 사람의 규칙/데이터 학습, 준비/예측 분리·대칭·8px/16px 간격 |
| 04 | [Step-by-Step](../templates/html/step-by-step.html) · [JPG](../previews/html-step-by-step.jpg) | #11→#12 | 5×5·3×3·3×3, 곱 9개와 합 −6 |
| 05 | [Interactive](../templates/html/interactive.html) · [JPG](../previews/html-interactive.jpg) | 승인본 `ae26ba0`→#12 | 이상 우선 그룹·임계값→개별 예측/행렬/지표 동시 갱신·분모 0 |
| 06 | [Architecture](../templates/html/architecture.html) · [JPG](../previews/html-architecture.jpg) | #10→#12 | 두 Conv Block→Flatten 8,192→FC 3 logits→Softmax |
| 07 | [Experiment](../templates/html/experiment.html) · [JPG](../previews/html-experiment.jpg) | 승인본 `3ad7079`→#12 | TP4 FP1 / FN2 TN5, 12개, 75.0/80.0/66.7/72.7% |
| 08 | [Executive Summary](../templates/html/executive-summary.html) · [JPG](../previews/html-executive-summary.jpg) | 기존 승인 레이아웃→#12 | 원래 값·단위·지표별 기준100%, −33.3/−33.3/−60.0% |

PR URL은 `https://github.com/sh0427-han/design-template-library/pull/번호`입니다. #9/#10/#11은 초기 통합 #12로 정리됐습니다. #16은 PC 전용 제작 기준, #17은 같은 8개 원본을 직접 표시하는 Scroll/Slide 및 용어 첫 등장 기준입니다.

## PR #22 사용자 확정 후속 반영

2026-10-27 사용자가 8종의 제목/라벨 체계와 과적합 시안을 확정하고 Markdown 정리·병합을 승인했습니다. 기존 치수/기술 계약 위에 핵심 제목 Navy/분류·단계 라벨 Blue와 설명 단위 소유 관계를 명시합니다. #1의 IMAGE REPRESENTATION 라벨을 포함한 원본6개 경로 변경은 [정확한 전후 SHA manifest](../previews/heading-review/change-scope.json)로 한정합니다. 숫자·수식·이미지 데이터·조작 계약은 보존합니다.

원본21단위+과적합2단위의 색/소유 관계를 PC4×두 모드의72자료 화면/184쌍에서 검사합니다. 기존 원본48화면/두 모드64화면 회귀와 새 개념의 재사용 범위는 별개입니다. [공통 적용표](DESIGN_COMPONENT_RECIPES.md#제목라벨-검사의-적용-단위) · [현재 감사 JSON](../previews/heading-review/validation.json) · [문서 확정 결과](../previews/heading-review/documentation-finalization.json). 실제 병합 상태·SHA는 [PR #22](https://github.com/sh0427-han/design-template-library/pull/22)에서 확인합니다.

아래 최초 정리의 소스/브라우저 수치·삭제 내역은 당시 기록이며 최신 실행값은 현재 JSON을 따릅니다.

## 문서의 책임

- [DESIGN_SYSTEM](../DESIGN_SYSTEM.md): 색·폰트·행간·간격·프레임·강조·정렬·원본/표시색·첫 용어 정의.
- [DESIGN_COMPONENT_RECIPES](DESIGN_COMPONENT_RECIPES.md): #1–#8 전체의 실제 수치, 역할별 선택 기준, 새 자료에 작성할 설계 기록표.
- [FIGURE_PRODUCTION_STANDARD](FIGURE_PRODUCTION_STANDARD.md): 학습 목표→기술 검산→도형→좌표→실제 렌더링의 제작 절차.
- [REFERENCE_PAGE_SPECS](REFERENCE_PAGE_SPECS.md): 각 원본을 재현할 데이터·공식·좌표·상태·삭제 금지 정보.
- [재사용 워크플로](REFERENCE_REUSE_WORKFLOW.md): 새 개념에 적용할 작업 순서. [두 모드 명세](DUAL_MODE_REFERENCE_REUSE.md): 같은 원본을 표시하는 프레임·탐색·상태 계약.

#1 제외/진행 중 문구는 제거했습니다. #1의 실제 픽셀 경로·채널/ROI·표시 보간·배지 노출·축/라벨 정렬을 공통 규격에 포함했습니다. #2의 카드 중심과 그림 중심을 혼용한 설명도 최종 구현과 맞췄습니다. 과거 보고서는 역사적 기록으로 표시하며 현행 규격으로 사용하지 않습니다.

## 현행 검증과 정리

검증 결과는 [전체 원본](../previews/review/reference-validation.json), [Interactive](../previews/review/interactive-validation.json), [Scroll/Slide](../previews/review/dual-mode-validation.json) 세 JSON으로 관리합니다. 파일별 `status`, 실행 시각, 소스·프리뷰 해시를 확인합니다. 실제 검증·사용자 디자인 검토·PR/병합 여부는 서로 구분합니다.

이번 로컬 실행은 Chromium **154.0.8037.57**에서 원본 **48/48**, 두 모드 원본 대조 **64/64**, #5 기본 임계값 **126개**·변경 데이터 **42개**, #2 실패/재사용 **12개**·#3 연속 resize **5개**를 통과했습니다. 원본 48개 화면의 실제 텍스트는 모두 Pretendard Variable이며 폴백·미출력·자간 오류·JS/요청 오류가 없었습니다. PC 기준 캡처와 두 모드 대표 프리뷰를 직접 확인했습니다.

원본 8종의 승인된 HTML/CSS/JS와 개별 프리뷰는 유지했습니다. 두 모드 대표 프리뷰는 최신 #1을 포함해 다시 캡처했고, #5 단일 HTML 공유본도 현재 공통 행간/간격 토큰을 내장하도록 재생성했습니다. 원격 CI·main 반영은 이 문서가 포함된 PR의 실제 상태로 확인합니다.

중복된 과거 before 이미지 10개, 오래된 회귀 JSON 1개, 전체 결과를 복사한 파생 JSON 7개, 별칭 검사 스크립트 7개, 역할이 끝난 폰트 비교 페이지/전용 검사/워크플로 3개, 초기 통합 게시문 초안·조사 JSON·일회성 게시기 3개를 제거했습니다. 합계 **31개**이며 사용처와 import를 정리했습니다. 상세 수학/기하 모듈, 공식 폰트/라이선스, 현재 프리뷰 10개, #5 공유본과 초기 소스 manifest는 유지합니다. 제거 파일은 Git 이력으로 복구할 수 있습니다.

새 부분 검사는 `validate_references.py --templates … --report /tmp/…`를 사용합니다. 같은 결과를 이름만 바꿔 Git에 늘리지 않으며, 전체 실행은 파생 JSON을 재생성하지 않습니다. 화면별 캡처는 임시 디렉터리와 CI artifact로 보관합니다. 실행 명령과 경로는 [검증 증거 안내](../previews/review/README.md)에 있습니다.

## 다음 템플릿 검증

다음 라운드의 기준은 **기존8종 레퍼런스와 갱신한 공통 Markdown**입니다. 로지스틱 회귀는 첫 검토 사례이며 다음 제작의 기준 템플릿이 아닙니다. 현재 보존한 개념 한 장의8개 화면/161점 검증과, 검토에서 얻은 일반 원칙·전용 값·한계는 [검증 기준](TEMPLATE_REUSE_VALIDATION.md)에 연결했습니다.

[검증 프롬프트](CONCEPT_REUSE_PROMPT.md)로 다른 개념을 제작하며 `DESIGN.md`에 규칙 출처, `VALIDATION.md`에 시작 문서D0/보완 후D1·문서 누락·고유 설계·구현 오류·검증/미검증 패턴을 기록합니다. 목적은 새 슬라이드의 완성도와 템플릿/문서의 재현 가능성을 함께 확인하는 것입니다. 이후 경사하강법과 과적합·일반화의 새 주제 검증을 수행했으며 각각의 VALIDATION 기록에 한정합니다.

기존8종의 사용자 승인·기술 회귀·새 개념의 재사용·문서 충분성·main 반영을 구분합니다. 원본의 통과가 다른 개념의 기술적 정확성과8종 전체의 일반화를 자동 보장하지 않습니다.
