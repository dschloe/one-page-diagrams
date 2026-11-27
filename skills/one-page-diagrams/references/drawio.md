# draw.io (수정 가능한 업무 흐름도)

출처: [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp)의 draw.io 스킬과 XML 규칙(Apache-2.0)을 줄이고 한국어로 옮긴 것이다. draw.io 데스크톱 앱이나 커넥터 없이 동작하도록 바꿨다.

결과물:
- `이름.drawio` — https://app.diagrams.net 에서 열어 바로 수정(설치·로그인 불필요)
- 편집 링크 — 클릭하면 같은 그림이 diagrams.net에서 열림
- `이름.png` — 가능하면 함께

## 방법 A: 명세 파일로 만들기 (권장, Python 실행 가능할 때)

좌표 계산을 스크립트가 한다. 모델은 내용 구조만 쓴다.

1. `이름.spec.json`을 쓴다(형식은 아래).
2. `python3 scripts/build.py 이름.spec.json --to drawio` → `이름.drawio`와 편집 링크 출력
3. `python3 scripts/to_png.py 이름.drawio` → `이름.png` (Chrome·Edge와 인터넷이 있으면)

### 명세 형식 (draw.io, 엑스칼리드로 공통)

```json
{
  "title": "교육 신청 승인 절차",
  "direction": "LR",
  "lanes": ["신청자", "팀장", "교육팀"],
  "nodes": [
    {"id": "s",  "label": "교육 신청",     "lane": "신청자", "col": 0, "kind": "start"},
    {"id": "r",  "label": "신청서 검토",   "lane": "팀장",   "col": 1, "kind": "step"},
    {"id": "d",  "label": "승인?",         "lane": "팀장",   "col": 2, "kind": "decision"},
    {"id": "e",  "label": "수강 등록",     "lane": "교육팀", "col": 3, "kind": "done"},
    {"id": "x",  "label": "반려 통보",     "lane": "신청자", "col": 3, "kind": "error"}
  ],
  "edges": [
    {"from": "s", "to": "r"},
    {"from": "r", "to": "d"},
    {"from": "d", "to": "e", "label": "예"},
    {"from": "d", "to": "x", "label": "아니오", "dashed": true}
  ]
}
```

- `direction`: `TB`(위→아래, 기본) 또는 `LR`(왼→오른쪽). 레인이 있으면 `LR`이 읽기 쉽다.
- `lanes`: 담당자·부서 칸. 없으면 생략. 레인이 있으면 각 노드에 `lane`과 `col`(가로 순서)을 준다.
- 레인이 없으면 각 노드에 `row`, `col`을 준다(0부터). 같은 칸에 두 노드를 두지 않는다.
- `kind`: `start`, `step`, `decision`, `done`, `error`, `data`, `external` 중 하나. 생략하면 `step`.
- `label` 안 줄바꿈은 `\n`.
- 화살표 `label`은 1~4단어. `dashed`는 예외·반려 같은 보조 흐름에만.

## 방법 B: XML 직접 쓰기 (Python 실행이 안 될 때, 또는 모양을 세밀하게 정할 때)

`.drawio` 파일은 아래 XML이다.

```xml
<mxfile><diagram name="Page-1"><mxGraphModel adaptiveColors="auto"><root>
<mxCell id="0"/>
<mxCell id="1" parent="0"/>
<mxCell id="a" value="교육 신청" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;fontSize=14;" vertex="1" parent="1"><mxGeometry x="40" y="40" width="160" height="64" as="geometry"/></mxCell>
<mxCell id="b" value="승인?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#d97706;fontSize=14;" vertex="1" parent="1"><mxGeometry x="40" y="170" width="160" height="80" as="geometry"/></mxCell>
<mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;" edge="1" source="a" target="b" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
</root></mxGraphModel></diagram></mxfile>
```

규칙:
- `id="0"`, `id="1"` 셀은 항상 맨 앞. 모든 id는 서로 달라야 한다.
- XML 주석 금지. 값 안의 `&`, `<`, `>`, `"`는 `&amp;`, `&lt;`, `&gt;`, `&quot;`.
- 모든 스타일에 `html=1;whiteSpace=wrap;`. 줄바꿈은 `&lt;br&gt;`.
- 연결선 셀은 자기 닫힘(`/>`)으로 쓰지 않는다. 안에 `<mxGeometry relative="1" as="geometry"/>`가 있어야 한다.
- 좌표는 격자: `x = col*200 + 40`, `y = row*130 + 40`. 상자 160×64, 마름모 160×80.
- 레인(스윔레인): `style="swimlane;horizontal=0;startSize=40;html=1;"`, x=0, y=레인번호*150, 높이 150. 레인 안 노드는 `parent="레인id"`, 좌표는 레인 기준(x=60+col*200, y=43). 서로 다른 레인을 잇는 선은 `parent="1"`.
- 모양: 판단 `rhombus;`, 데이터 `shape=cylinder3;`, 시작·끝 `rounded=1;arcSize=40;`.
- 색은 `svg-diagram.md`의 팔레트와 같은 값을 쓴다.

파일을 쓴 뒤 실행할 수 있으면 `python3 scripts/check.py 이름.drawio`로 검사하고, `python3 scripts/drawio_link.py 이름.drawio`로 편집 링크를 만든다.

## 방법 C: Mermaid 링크 (시퀀스·ER·클래스 다이어그램처럼 배치가 복잡할 때)

1. Mermaid 코드를 `이름.mmd`로 쓴다(라벨은 큰따옴표: `A["교육 신청"]`).
2. `python3 scripts/drawio_link.py 이름.mmd` → 링크를 열면 diagrams.net이 편집 가능한 도형으로 바꿔 준다.
3. 이 방법은 `.drawio` 파일과 PNG를 바로 만들지 못한다. 사용자에게 링크를 열어 `파일 → 다른 이름으로 저장`, `파일 → 내보내기 → PNG`를 하라고 안내한다.
4. Python이 없으면 Mermaid 코드만 주고, diagrams.net에서 `정렬(Arrange) → 삽입(Insert) → 고급(Advanced) → Mermaid`에 붙여 넣으라고 안내한다.

## 전달 시 안내 문구

- ".drawio 파일을 https://app.diagrams.net 에서 열면 상자와 선을 끌어서 고칠 수 있습니다."
- PNG를 못 만들었으면: "diagrams.net에서 파일 → 내보내기 → PNG로 이미지를 받을 수 있습니다."
