# 엑스칼리드로 (손그림 화이트보드)

[Excalidraw](https://github.com/excalidraw/excalidraw)(MIT)의 공개 파일 형식을 쓴다. 공식 MCP([excalidraw/excalidraw-mcp](https://github.com/excalidraw/excalidraw-mcp), MIT) 없이 `.excalidraw` 파일을 직접 만든다.

결과물:
- `이름.excalidraw` — https://excalidraw.com 에서 왼쪽 위 메뉴 → 열기. 설치·로그인 불필요
- `이름.png` — 가능하면 함께

## 방법 A: 명세 파일로 만들기 (권장)

1. `이름.spec.json`을 쓴다. 형식은 `references/drawio.md`의 "명세 형식"과 같다.
2. `python3 scripts/build.py 이름.spec.json --to excalidraw` → `이름.excalidraw`
3. `python3 scripts/to_png.py 이름.excalidraw` → `이름.png` (Chrome·Edge와 인터넷이 있으면)

손그림 정도는 `"roughness": 0`(깔끔) ~ `2`(거친 손그림)로 명세 최상위에 줄 수 있다. 기본 1.

## 방법 B: JSON 직접 쓰기 (Python 실행이 안 될 때)

파일 뼈대:
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {"viewBackgroundColor": "#ffffff", "gridSize": null},
  "files": {}
}
```

상자와 그 안의 글자(서로 참조해야 글자가 상자를 따라 움직인다):
```json
{"id":"box1","type":"rectangle","x":100,"y":100,"width":180,"height":70,"angle":0,
 "strokeColor":"#1e1e1e","backgroundColor":"#a5d8ff","fillStyle":"hachure","strokeWidth":2,
 "strokeStyle":"solid","roughness":1,"opacity":100,"groupIds":[],"frameId":null,
 "roundness":{"type":3},"seed":101,"version":1,"versionNonce":1,"isDeleted":false,
 "boundElements":[{"type":"text","id":"box1-t"},{"type":"arrow","id":"a1"}],
 "updated":1,"link":null,"locked":false},
{"id":"box1-t","type":"text","x":110,"y":122,"width":160,"height":25,"angle":0,
 "strokeColor":"#1e1e1e","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":2,
 "strokeStyle":"solid","roughness":1,"opacity":100,"groupIds":[],"frameId":null,"roundness":null,
 "seed":102,"version":1,"versionNonce":1,"isDeleted":false,"boundElements":[],"updated":1,
 "link":null,"locked":false,"text":"교육 신청","fontSize":20,"fontFamily":5,
 "textAlign":"center","verticalAlign":"middle","containerId":"box1","originalText":"교육 신청",
 "lineHeight":1.25,"autoResize":true}
```

화살표(시작·끝 상자에 붙임):
```json
{"id":"a1","type":"arrow","x":280,"y":135,"width":100,"height":0,"angle":0,
 "strokeColor":"#1e1e1e","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":2,
 "strokeStyle":"solid","roughness":1,"opacity":100,"groupIds":[],"frameId":null,
 "roundness":{"type":2},"seed":103,"version":1,"versionNonce":1,"isDeleted":false,
 "boundElements":[],"updated":1,"link":null,"locked":false,
 "points":[[0,0],[100,0]],"lastCommittedPoint":null,
 "startBinding":{"elementId":"box1","focus":0,"gap":4},
 "endBinding":{"elementId":"box2","focus":0,"gap":4},
 "startArrowhead":null,"endArrowhead":"arrow","elbowed":false}
```

규칙:
- `type`: `rectangle`, `ellipse`, `diamond`, `text`, `arrow`, `line`.
- 화살표의 `x`, `y`는 시작점. `points`는 시작점 기준 상대 좌표.
- 화살표가 붙은 상자의 `boundElements`에 그 화살표를 넣는다.
- `seed`는 요소마다 다른 정수.
- 한글 글자 폭은 `fontSize × 글자 수`로 잡는다.
- 색(손그림 기본 팔레트): 파랑 `#a5d8ff`, 초록 `#b2f2bb`, 노랑 `#ffec99`, 빨강 `#ffc9c9`, 보라 `#d0bfff`, 선·글자 `#1e1e1e`.

## 전달 시 안내 문구

- ".excalidraw 파일을 https://excalidraw.com 에서 열면 함께 그리며 고칠 수 있습니다. 공유 버튼으로 수강생과 실시간 협업도 됩니다."
- PNG를 못 만들었으면: "excalidraw.com에서 메뉴 → 이미지 내보내기 → PNG로 받을 수 있습니다."
- 한글은 excalidraw 손글씨 글꼴에 없어서 시스템 글꼴로 보인다.
