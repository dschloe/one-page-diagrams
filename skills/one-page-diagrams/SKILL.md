---
name: one-page-diagrams
description: Make one-page diagrams and PNG images for slides and reports (infographic, flowchart, sequence, swimlane workflow, hand-drawn whiteboard, system architecture) as free, no-install files - HTML, SVG, .drawio or .excalidraw. Use whenever the user asks to draw, diagram, visualize or chart a process, structure, comparison, steps or system, including Korean requests such as 그림, 도식, 순서도, 흐름도, 인포그래픽, 구조도, 다이어그램, 그려줘.
license: MIT (bundles adapted material under MIT and Apache-2.0; see NOTICE.md)
---

# 한 장 그림 (One-Page Diagrams)

글 몇 줄을 보고서·강의자료에 바로 넣을 그림 한 장으로 바꾼다. 다섯 가지 방식 중 하나를 골라 파일 하나를 만든다. 유료 API, 이미지 생성 모델, 로그인, 설치가 필요한 도구는 쓰지 않는다. 모델이 텍스트(HTML, SVG, XML, JSON)를 직접 쓴다.

## 1단계: 방식 고르기

사용자가 방식이나 도구 이름(AntV, 바오위, draw.io, 엑스칼리드로, 구조도)을 말했으면 그대로 따른다. 말하지 않았으면 아래 표로 고른다. 애매하면 표에서 위쪽 행을 우선한다.

| 내용의 모양 | 방식 | 결과 파일 | 읽을 문서 |
|---|---|---|---|
| 요점 나열, 단계, 비교, SWOT, 타임라인, 간단한 수치 | 인포그래픽 | `.html` | `references/infographic.md` |
| 분기가 있는 순서도, 시퀀스, 상태도, 마인드맵 (그대로 붙여 넣을 그림) | SVG 다이어그램 | `.svg` | `references/svg-diagram.md` |
| 담당자별 칸(스윔레인)이 있는 업무 흐름도, 나중에 고칠 그림 | draw.io | `.drawio` + 편집 링크 | `references/drawio.md` |
| 손그림 느낌, 화이트보드, 수업 중 함께 고칠 스케치 | 엑스칼리드로 | `.excalidraw` | `references/excalidraw.md` |
| 서비스·시스템 구성도, 계층과 연결 | 구조도 | `.html` | `references/architecture.md` |

고른 방식의 참고 문서를 읽은 뒤에 작성한다. 참고 문서를 읽지 않고 형식을 추측하지 않는다.

예외: 대화창 안에 그림을 바로 띄우는 커넥터 도구(draw.io의 `create_diagram`, 엑스칼리드로의 `create_view` 등)가 이 대화에 연결되어 있고 사용자가 파일을 요구하지 않았으면, 그 도구를 써도 된다. 연결되어 있지 않으면 파일로 만든다. 커넥터 설치를 요구하지 않는다.

## 2단계: 내용 정리 (모든 방식 공통)

1. 사용자의 글에서 제목, 항목, 순서, 관계를 뽑는다. 사용자 글에 없는 수치, 이름, 단계를 지어내지 않는다. 빠진 정보가 그림에 꼭 필요하면 `[확인 필요]`라고 그림 안에 적는다.
2. 그림 속 글자는 사용자가 쓴 언어로 쓴다. 한국어 요청이면 한국어로 쓴다.
3. 한 장에 메시지 하나만 담는다. 항목이 많으면(대략 9개 초과) 묶거나 두 장으로 나누자고 제안한다.
4. 제목은 결론이 드러나는 짧은 문장으로 쓴다. 예: "승인은 팀장 단계에서 가장 오래 걸린다".
5. 같은 개념은 그림 전체에서 같은 단어로 쓴다.

## 3단계: 파일 만들기

- 파일 이름: 내용을 나타내는 영문 소문자와 하이픈. 예: `approval-flow.drawio`, `course-roadmap-infographic.html`.
- 기본 테마는 밝은 배경이다(보고서·슬라이드용). 사용자가 어두운 배경을 원하면 바꾼다.
- 방향(가로·세로): 순서도, 업무 흐름도, 타임라인, 단계 그림처럼 흐름이 한 방향으로 이어지는 그림에 적용한다.
  - 사용자가 방향이나 용도를 말했으면 그대로 따른다. 슬라이드·발표·16:9는 가로(왼쪽→오른쪽), 보고서·문서·A4는 세로(위→아래).
  - 말하지 않았으면 고른 방식의 기본 방향으로 초안을 먼저 만든다. 만들기 전에는 묻지 않는다. 초안을 보여 준 뒤 6단계에서 한 번 묻는다.
  - 가로로 만들 때: SVG는 상자를 왼쪽에서 오른쪽으로 놓고 분기는 위아래로 벌린다. draw.io와 엑스칼리드로는 명세에 `"direction": "LR"`을 쓴다.
- 한글 글꼴 순서: `'Pretendard', 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', 'Noto Sans CJK KR', sans-serif`. 웹 글꼴을 불러오지 않는다(오프라인에서도 보이게).
- 실행 환경별 처리:
  - 파일을 쓸 수 있으면(Claude Code, Codex, claude.ai·ChatGPT의 코드 실행) 파일로 저장하고 사용자에게 전달한다.
  - 파일을 쓸 수 없으면 전체 내용을 코드 블록 하나로 주고, 어떤 확장자로 저장하는지 한 줄로 알려 준다.
- `scripts/`의 Python 스크립트는 표준 라이브러리만 쓴다. 실행할 수 있으면 쓰고, 실행할 수 없으면 건너뛴다. 명령은 `python3`로 쓰고, 없으면 `python` 또는 `py`(Windows)로 바꾼다. 스크립트 경로는 이 SKILL.md가 있는 폴더 기준이다.
  - `scripts/build.py` — 명세(JSON)로 .drawio·.excalidraw 생성 (좌표 자동 계산)
  - `scripts/check.py` — 형식 검사
  - `scripts/to_png.py` — PNG 변환 (PC의 Chrome·Edge 사용)
  - `scripts/drawio_link.py` — draw.io 편집 링크

## 4단계: 검사

파일을 넘기기 전에 확인한다.

- 실행 가능하면 `python3 scripts/check.py <파일>`로 형식(XML/JSON/SVG 구조)을 검사한다. 오류가 나오면 고친 뒤 다시 검사한다.
- 글자가 상자 밖으로 넘치지 않는지, 화살표가 상자를 가로지르지 않는지 좌표로 확인한다. 한글은 영문보다 넓으므로 글자당 폭을 글꼴 크기의 1.0배로 잡는다.
- 사용자 글에 없던 내용이 들어가지 않았는지 다시 본다.

## 5단계: PNG 만들기

사용자가 이미지·PNG·그림 파일을 원하거나, 보고서·슬라이드에 넣는다고 했으면 `python3 scripts/to_png.py <파일>`로 PNG를 만든다(기본 2배 해상도, `--scale 3` 가능). 결과 파일과 같은 폴더에 같은 이름의 `.png`가 생긴다.

- 종료 코드 3(브라우저 없음 등)이면 PNG 없이 원본을 전달하고, 스크립트가 출력한 "대안" 문장을 그대로 안내한다.
- PNG를 만들었으면 직접 열어 보고(이미지를 볼 수 있는 환경이면) 글자 겹침, 잘림, 빈 그림이 없는지 확인한다. 문제가 있으면 원본을 고치고 다시 만든다.

## 6단계: 전달 문구

결과와 함께 아래 내용만 짧게 알린다.

1. 어떤 방식을 골랐는지와 이유 한 줄. 만든 파일 목록(원본, PNG).
2. 여는 방법:
   - `.html`, `.svg`: 웹 브라우저로 열기. 인포그래픽 HTML은 인터넷 연결이 필요하다.
   - `.drawio`: https://app.diagrams.net 에서 파일 열기(설치 불필요). 링크를 만들었으면 링크도 준다.
   - `.excalidraw`: https://excalidraw.com 에서 메뉴 → 열기(설치 불필요).
3. 고칠 수 있는 것 한 줄. 예: "색, 순서, 문구를 말씀하시면 바꿉니다."
4. 방향 질문 한 줄(3단계의 방향 규칙에 해당하고, 사용자가 방향·용도를 말하지 않았을 때만). 지금 방향을 밝히고 반대 방향을 제안한다. 예: "지금은 세로형입니다. 슬라이드에 넣으실 거면 가로형으로 다시 만들까요?" 사용자가 답하면 같은 내용으로 방향만 바꿔 다시 만들고, 이 질문은 다시 하지 않는다.

과정 설명, 사과, 장식 문구는 넣지 않는다.
