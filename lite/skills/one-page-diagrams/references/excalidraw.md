# 엑스칼리드로 (손그림 화이트보드)

[Excalidraw](https://github.com/excalidraw/excalidraw)(MIT)의 공개 파일 형식을 쓴다. 공식 MCP([excalidraw/excalidraw-mcp](https://github.com/excalidraw/excalidraw-mcp), MIT) 없이 `.excalidraw` 파일을 직접 만든다.

결과물: `이름.excalidraw` — https://excalidraw.com 에서 왼쪽 위 메뉴 → 열기. 설치·로그인 불필요.

## 작성 순서

1. 상자를 격자에 놓는다. 가로형은 `x = 100 + col*280`, `y = 100 + row*150`. 상자는 180×70, 글자가 길면 폭을 `fontSize × 글자 수 + 40`으로 넓힌다.
2. 상자마다 글자 요소를 하나씩 만들고 서로 참조하게 한다.
3. 화살표는 앞 상자의 오른쪽 가운데에서 뒤 상자의 왼쪽 가운데로 긋는다(세로형은 아래 가운데에서 위 가운데로).
4. 손그림 정도는 요소의 `roughness`로 정한다. 0(깔끔) ~ 2(거친 손그림), 기본 1.

## JSON 형식

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

추가 규칙:
- 제목과 화살표 라벨은 상자에 묶이지 않은 글자 요소로 쓴다. 위 글자 요소에서 `containerId`를 `null`, `textAlign`을 `"left"`, `verticalAlign`을 `"top"`으로 바꾼다. `width`는 `fontSize × 글자 수`, `height`는 `fontSize × 1.25`.
- 제목: x=100, y=30, `fontSize` 28. 상자는 y=100부터 놓는다.
- 화살표 라벨: `fontSize` 16, 화살표 가운데에서 위로 30 떨어진 곳에 둔다. 상자나 다른 화살표와 겹치지 않게 한다.
- 갈라지거나 합쳐지는 흐름: 주 경로는 row 0에 한 줄로 놓고, 옆으로 빠지는 단계는 row 1에 둔다. 한 상자에서 화살표가 둘 나가면 하나는 오른쪽 가운데, 하나는 아래 가운데에서 시작한다.

쓴 뒤 다시 읽어 JSON이 올바른지, 화살표의 `elementId`가 실제 상자 id인지, 상자의 `boundElements`에 글자와 화살표가 들어 있는지 확인한다.

## 전달 시 안내 문구

- ".excalidraw 파일을 https://excalidraw.com 에서 열면 함께 그리며 고칠 수 있습니다. 공유 버튼으로 실시간 협업도 됩니다."
- "excalidraw.com에서 메뉴 → 이미지 내보내기 → PNG로 받을 수 있습니다."
- excalidraw.com은 한글을 시스템 글꼴로 보여 준다(손글씨 글꼴에 한글이 없다).
