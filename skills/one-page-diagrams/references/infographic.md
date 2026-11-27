# 인포그래픽 (AntV Infographic)

출처: [antvis/infographic](https://github.com/antvis/infographic)의 `infographic-creator` 스킬(MIT)을 한국어로 옮기고 줄인 것이다.

결과물은 HTML 파일 하나다. 그림은 브라우저에서 AntV Infographic 라이브러리(CDN)가 그린다. 따라서 열 때 인터넷 연결이 필요하다.

## 작성 순서

1. 내용을 목록·순서·비교·계층·관계·수치 중 하나로 분류한다.
2. 아래 "모델 선택"에서 템플릿 하나를 고른다. 목록에 없는 템플릿 이름을 만들지 않는다.
3. 인포그래픽 문법을 쓴다.
4. `assets/infographic-template.html`을 복사해 `{{TITLE}}`과 `{{SYNTAX}}`를 바꾼다.
5. `python3 scripts/check.py <파일>`로 검사한다.

## 문법 규칙

```infographic
infographic list-row-horizontal-icon-arrow
data
  title 제목
  desc 설명 한 줄
  lists
    - label 항목
      desc 설명
      icon document text
theme
  palette #2563eb #7c3aed #f97316
```

- 첫 줄은 반드시 `infographic <템플릿 이름>`.
- `data`, `theme` 블록 안은 공백 두 칸 들여쓰기. 탭 금지.
- 키와 값은 `키 공백 값`. 배열 항목은 `- `로 시작.
- `data` 안에는 템플릿에 맞는 주 데이터 필드를 하나만 쓴다. `lists`, `sequences`, `compares`, `values`, `root`, `nodes`, `items`를 섞지 않는다.
- 주요 항목에는 `icon`을 넣는다. 아이콘 ID를 모르면 영어 키워드를 공백으로 구분해 쓴다(예: `rocket launch`, `shield check`, `users`, `database`, `chart line`). 하이픈으로 잇지 않는다.
- 한국어 `desc`는 10자 안팎, `label`은 8자 안팎. 길면 단어 중간에서 줄이 바뀐다.
- 아이콘은 열 때 인터넷에서 불러온다. 오프라인이면 아이콘 없이 그려진다.
- `value`는 숫자만 쓴다. 단위는 `label`이나 `desc`에 쓴다.
- `palette` 색은 따옴표·쉼표 없이 공백으로 구분한다.
- 백틱(`)과 `${`는 쓰지 않는다. HTML 템플릿 문자열을 깨뜨린다.

### 템플릿 종류별 주 데이터 필드

| 템플릿 접두어 | 주 데이터 필드 | 주의 |
|---|---|---|
| `list-*` | `lists` | |
| `sequence-*` | `sequences` | 순서 지정 `order asc` 또는 `order desc` 가능 |
| `sequence-interaction-*` | `sequences` + `relations` | `sequences` 각 항목이 참여자(레인). 레인의 `children` 각 항목에 `label`, 필요하면 `id`, `step`(같은 값은 같은 높이) |
| `compare-binary-*`, `compare-hierarchy-left-right-*` | `compares` | 최상위 항목은 정확히 2개. 비교 내용은 각자의 `children` 아래에 |
| `compare-swot` | `compares` | 최상위 4개(강점, 약점, 기회, 위협), 각자 `children` |
| `compare-quadrant-*` | `compares` | 최상위 4개 |
| `hierarchy-structure` | `items` | |
| 그 외 `hierarchy-*` | `root` | `children`으로 재귀 |
| `relation-*` | `nodes` + `relations` | 관계는 `A - 라벨 -> B` |
| `chart-*` | `values` | 각 항목 `label`, `value` |

### 예시

순서:
```infographic
infographic sequence-ascending-steps
data
  title 신규 과정 개설 절차
  sequences
    - label 수요 조사
      icon clipboard check
    - label 커리큘럼 설계
      icon book open
    - label 시범 운영
      icon rocket launch
  order asc
```

두 대상 비교:
```infographic
infographic compare-binary-horizontal-badge-card-arrow
data
  title 온라인과 오프라인 과정 비교
  compares
    - label 온라인
      icon laptop
      children
        - label 시간 제약이 적다
          icon clock
        - label 질문 응답이 늦다
          icon message
    - label 오프라인
      icon users
      children
        - label 즉석 피드백
          icon check circle
        - label 장소 비용 발생
          icon wallet
```

계층:
```infographic
infographic hierarchy-tree-curved-line-rounded-rect-node
data
  title 교육팀 구성
  root
    label 교육팀
    children
      - label 기획
      - label 운영
      - label 콘텐츠 개발
```

SWOT:
```infographic
infographic compare-swot
data
  title 사내 AI 교육 SWOT
  compares
    - label 강점
      icon trophy
      children
        - label 실습 위주 구성
    - label 약점
      icon alert circle
      children
        - label 강사 수 부족
    - label 기회
      icon trending up
      children
        - label 업무 자동화 수요 증가
    - label 위협
      icon shield alert
      children
        - label 무료 외부 강의 증가
```

수치(사용자가 준 수치만):
```infographic
infographic chart-column-simple
data
  title 분기별 수강 인원
  values
    - label 1분기
      value 120
    - label 2분기
      value 150
```

관계:
```infographic
infographic relation-dagre-flow-tb-simple-circle-node
data
  title 데이터 흐름
  nodes
    - id src
      label 원천 데이터
    - id etl
      label 정제
    - id bi
      label 대시보드
  relations
    src - 적재 -> etl
    etl - 집계 -> bi
```

## 모델 선택

- 순서, 단계, 절차, 로드맵, 타임라인: `sequence-ascending-steps`, `sequence-snake-steps-simple`, `sequence-timeline-simple`, `sequence-roadmap-vertical-simple`, `sequence-stairs-front-compact-card`, `sequence-funnel-simple`(깔때기), `sequence-pyramid-simple`(피라미드), `sequence-circular-simple`(순환)
- 여러 사람·시스템이 주고받는 흐름: `sequence-interaction-default-badge-card`, `sequence-interaction-default-compact-card`
- 나란한 요점: `list-row-horizontal-icon-arrow`, `list-grid-badge-card`, `list-grid-candy-card-lite`, `list-column-vertical-icon-arrow`, `list-column-done-list`(체크리스트), `list-zigzag-down-simple`
- 두 대상 비교: `compare-binary-horizontal-badge-card-arrow`, `compare-binary-horizontal-simple-fold`, `compare-binary-horizontal-underline-text-vs`
- SWOT: `compare-swot` / 사분면: `compare-quadrant-quarter-simple-card`, `compare-quadrant-quarter-circular`
- 계층, 조직도: `hierarchy-tree-curved-line-rounded-rect-node`, `hierarchy-tree-tech-style-badge-card`, `hierarchy-structure`
- 마인드맵: `hierarchy-mindmap-branch-gradient-capsule-item`, `hierarchy-mindmap-level-gradient-compact-card`
- 관계, 의존: `relation-dagre-flow-tb-simple-circle-node`, `relation-dagre-flow-tb-badge-card`
- 수치: `chart-column-simple`, `chart-bar-plain-text`, `chart-line-plain-text`, `chart-pie-donut-plain-text`, `chart-pie-compact-card`, `chart-wordcloud`

## 테마

- 기본 팔레트(보고서용): `palette #2563eb #7c3aed #f97316 #059669`
- 손그림 느낌: `theme` 아래 `stylize rough`
- 색을 3~4개 이하로 유지한다.

## 검사 목록

- 첫 줄이 `infographic <목록에 있는 템플릿>`인가
- 주 데이터 필드가 하나뿐이고 템플릿과 맞는가
- `compare-binary-*`는 최상위 항목이 정확히 2개이고 각자 `children`이 있는가
- `children` 아래 모든 항목에 `label`이 있는가
- 사용자 글에 없는 수치가 없는가
