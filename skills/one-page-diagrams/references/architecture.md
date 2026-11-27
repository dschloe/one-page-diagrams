# 구조도 (서비스·시스템 아키텍처)

출처: [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator)(MIT)의 디자인 규칙(역할별 색, 화살표 가림 처리, 범례 위치)을 밝은 배경·한글용으로 바꾼 것이다. 원본과 달리 웹 글꼴과 외부 스크립트를 쓰지 않는다.

결과물: `이름.html` 한 파일(제목 + SVG 구조도 + 요약 카드 3개 + PNG 저장 버튼). 가능하면 `이름.png`도.

## 작성 순서

1. 구성 요소를 계층으로 나눈다. 예: 사용자 → 화면(프론트엔드) → 서버(백엔드) → 저장소 → 외부 서비스.
2. 계층을 왼쪽→오른쪽(또는 위→아래) 열로 배치하고 좌표를 정한다.
3. `assets/architecture-template.html`을 복사해 `{{TITLE}}`, `{{SUBTITLE}}`, `{{SVG_BODY}}`, `{{CARDS}}`, `{{FOOTER}}`를 채운다.
4. 기본 viewBox는 `0 0 1160 620`. 다 그린 뒤 viewBox를 실제 내용 범위 + 사방 20으로 줄인다(예: 내용이 x 40~1080, y 80~560이면 `20 60 1080 520`). 위아래 빈 공간이 남지 않게 한다. 내용이 넘치면 viewBox와 배경 `rect`를 함께 늘린다.
5. `python3 scripts/check.py 이름.html`, `python3 scripts/to_png.py 이름.html`.

## 역할별 색 (밝은 배경)

| 역할 | 채움 | 테두리 |
|---|---|---|
| 사용자·화면(프론트엔드) | `#cffafe` | `#0891b2` |
| 서버·처리(백엔드) | `#d1fae5` | `#059669` |
| 데이터베이스·저장소 | `#ede9fe` | `#7c3aed` |
| 클라우드·영역 | 채움 없음 | `#d97706` 점선 `8,5` |
| 보안·인증 | `#ffe4e6` | `#e11d48` (경계는 점선 `4,4`) |
| 메시지 큐·연결 | `#ffedd5` | `#ea580c` |
| 외부 서비스 | `#f1f5f9` | `#64748b` |

## 그리는 순서 (`{{SVG_BODY}}` 안)

1. 영역 테두리(클라우드, 보안 그룹)
2. 화살표 `<path ... marker-end="url(#arrow)"/>`
3. 가림 상자: 각 구성 요소와 같은 위치에 `fill="#ffffff"` 상자(화살표가 비쳐 보이지 않게)
4. 구성 요소 상자: `rx="10"`, 테두리 2px
5. 글자: 이름 16px/600, 설명 12px `#475569`
6. 범례: 모든 영역 테두리보다 20px 이상 아래

구성 요소 예:
```svg
<rect x="60" y="120" width="180" height="70" rx="10" fill="#ffffff"/>
<rect x="60" y="120" width="180" height="70" rx="10" fill="#cffafe" stroke="#0891b2" stroke-width="2"/>
<text x="150" y="150" font-size="16" font-weight="600" fill="#0f172a" text-anchor="middle">수강생 웹</text>
<text x="150" y="172" font-size="12" fill="#475569" text-anchor="middle">React</text>
```

데이터베이스는 원통(위·아래 타원 + 사각형)으로, 메시지 큐는 상자 사이 빈칸에 높이 24의 납작한 상자로 그린다.

## 간격

- 구성 요소 높이 70(설명 2줄이면 90), 상자 사이 세로 50 이상, 가로 60 이상.
- 영역 테두리 안쪽 여백 24.
- 화살표 라벨은 상자 테두리에서 10 이상 떨어뜨리고, 다른 상자와 겹치지 않는 선분 위에 둔다. 공간이 좁으면 라벨을 2~4글자로 줄인다.

## 요약 카드 (`{{CARDS}}`)

카드 3개: 보통 "구성", "데이터 흐름", "보안·운영". 사용자가 준 정보만 쓴다.
```html
<div class="card"><h3><span class="dot" style="background:#0891b2"></span>구성</h3>
<ul><li>수강생 웹 (React)</li><li>API 서버</li></ul></div>
```

## 금지

- 사용자 글에 없는 제품명·버전·수치를 넣지 않는다. 기술 스택을 모르면 설명 줄을 비우거나 `[확인 필요]`.
- 웹 글꼴(Google Fonts 등)과 외부 스크립트를 추가하지 않는다.
