# draw.io (수정 가능한 업무 흐름도)

출처: [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp)의 draw.io 스킬과 XML 규칙(Apache-2.0)을 줄이고 한국어로 옮긴 것이다. draw.io 데스크톱 앱이나 커넥터 없이 동작하도록 바꿨다.

결과물: `이름.drawio` — https://app.diagrams.net 에서 열어 바로 수정(설치·로그인 불필요).

## 작성 순서

1. 단계마다 담당자(레인), 순서(col), 종류(시작, 단계, 판단, 완료, 반려)를 표로 먼저 정리한다. 같은 칸에 두 단계를 두지 않는다.
2. 아래 격자 규칙으로 좌표를 계산해 XML을 쓴다.
3. 가로형(기본, 레인이 있을 때)은 col이 진행 순서다. 세로형은 row가 진행 순서다.
4. 화살표 라벨은 1~4단어. 점선(`dashed=1;`)은 예외·반려 같은 보조 흐름에만 쓴다.

## XML 형식

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

추가 규칙:
- 제목: 맨 위에 글자 셀 하나를 둔다. `style="text;html=1;align=left;verticalAlign=middle;fontSize=20;fontStyle=1;"`, x=40, y=20, 폭 800, 높이 40, `parent="1"`. 제목이 있으면 레인과 상자는 y를 80만큼 내리고, 레인은 x=40에서 시작한다.
- 레인 폭: `60 + (열 개수)*200 + 20`. 모든 레인의 폭을 같게 한다.
- 레인 안 마름모는 y=35(높이 80), 상자는 y=43(높이 64)으로 세로 가운데를 맞춘다.
- 연결선의 `parent`: 같은 레인 안이면 그 레인 id, 다른 레인을 이으면 `1`.
- 연결선 라벨: 연결선 스타일에는 `whiteSpace=wrap;`을 넣지 않는다(라벨이 한 글자씩 세로로 꺾인다). `html=1;fontSize=12;labelBackgroundColor=#ffffff;`를 쓴다.
- 판단에서 두 갈래가 나갈 때는 나가는 변을 다르게 준다. 한쪽은 `exitX=1;exitY=0.5;`(오른쪽), 다른 쪽은 `exitX=0.5;exitY=1;`(아래) 또는 `exitX=0.5;exitY=0;`(위). 두 갈래 모두에 라벨을 붙인다.
- 색(채움/테두리): 시작 `#dbeafe`/`#2563eb`, 단계 `#f1f5f9`/`#64748b`, 판단 `#fef3c7`/`#d97706`, 완료 `#dcfce7`/`#16a34a`, 반려·오류 `#fee2e2`/`#dc2626`, 데이터 `#ede9fe`/`#7c3aed`, 선 `#475569`.
- 판단 상자는 사용자가 조건이나 갈래(승인되면/반려되면)를 말했을 때만 넣는다.

쓴 뒤 다시 읽어 id가 겹치지 않는지, 모든 `source`와 `target`이 실제 id인지, 태그가 닫혔는지 확인한다.

## Mermaid로 넘기기 (시퀀스·ER·클래스 다이어그램처럼 배치가 복잡할 때)

1. Mermaid 코드를 준다(라벨은 큰따옴표: `A["교육 신청"]`).
2. diagrams.net에서 `정렬(Arrange) → 삽입(Insert) → 고급(Advanced) → Mermaid`에 붙여 넣으면 편집 가능한 도형이 된다고 안내한다.

## 전달 시 안내 문구

- ".drawio 파일을 https://app.diagrams.net 에서 열면 상자와 선을 끌어서 고칠 수 있습니다."
- "diagrams.net에서 파일 → 내보내기 → PNG로 이미지를 받을 수 있습니다."
