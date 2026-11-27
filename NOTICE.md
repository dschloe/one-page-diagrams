# Third-party notices

이 프로젝트(MIT)는 아래 공개 프로젝트의 설계 규칙, 문법 설명, 링크 형식을 참고해 한국어로 다시 쓰고 줄였습니다. 원본 코드를 그대로 복사해 넣지는 않았으며, 각 참고 문서 첫머리에 출처를 적었습니다.

| 프로젝트 | 라이선스 | 참고한 부분 | 사용 위치 |
|---|---|---|---|
| [antvis/infographic](https://github.com/antvis/infographic) | MIT, Copyright (c) 2025 AntV | 인포그래픽 문법, 템플릿 목록, HTML 렌더링 방식 | `references/infographic.md`, `assets/infographic-template.html` |
| [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) (`baoyu-diagram`) | MIT, Copyright (c) 2026 Jim Liu | SVG 다이어그램 디자인 규칙(그리는 순서, 간격, 역할별 색) | `references/svg-diagram.md` |
| [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp) | Apache-2.0, Copyright JGraph Ltd | draw.io XML 규칙, 편집 링크(#R, #create) 형식, 뷰어 임베드 방식 | `references/drawio.md`, `scripts/drawio_link.py`, `scripts/to_png.py` |
| [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw), [excalidraw/excalidraw-mcp](https://github.com/excalidraw/excalidraw-mcp) | MIT | .excalidraw 파일 형식, `exportToSvg` | `references/excalidraw.md`, `scripts/build.py`, `scripts/to_png.py` |
| [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) | MIT, Copyright (c) 2025 Cocoon AI | 구조도 디자인 규칙(역할별 색, 화살표 가림 처리, 범례 위치) | `references/architecture.md`, `assets/architecture-template.html` |

## 포함된 글꼴

| 글꼴 | 라이선스 | 사용 위치 |
|---|---|---|
| [Gaegu](https://github.com/google/fonts/tree/main/ofl/gaegu) (`Gaegu-Regular.ttf`) | SIL Open Font License 1.1, Copyright 2018 The Gaegu Project Authors | `assets/fonts/` — 엑스칼리드로 그림을 PNG로 바꿀 때 쓰는 한글 손글씨 글꼴. 라이선스 원문은 `assets/fonts/OFL.txt` |

실행 시 브라우저가 인터넷에서 불러오는 라이브러리(AntV Infographic, draw.io 뷰어, Excalidraw)는 이 저장소에 포함되어 있지 않으며 각 라이선스를 따릅니다.

Apache-2.0 원문: https://www.apache.org/licenses/LICENSE-2.0
