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

쓴 뒤 다시 읽어 id가 겹치지 않는지, 모든 `source`와 `target`이 실제 id인지, 태그가 닫혔는지 확인한다.

## Mermaid로 넘기기 (시퀀스·ER·클래스 다이어그램처럼 배치가 복잡할 때)

1. Mermaid 코드를 준다(라벨은 큰따옴표: `A["교육 신청"]`).
2. diagrams.net에서 `정렬(Arrange) → 삽입(Insert) → 고급(Advanced) → Mermaid`에 붙여 넣으면 편집 가능한 도형이 된다고 안내한다.

## 전달 시 안내 문구

- ".drawio 파일을 https://app.diagrams.net 에서 열면 상자와 선을 끌어서 고칠 수 있습니다."
- "diagrams.net에서 파일 → 내보내기 → PNG로 이미지를 받을 수 있습니다."
