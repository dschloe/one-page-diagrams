# SVG 다이어그램 (순서도, 시퀀스, 상태도, 마인드맵, 타임라인)

출처: [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)의 `baoyu-diagram`(MIT) 디자인 규칙을 보고서·슬라이드용으로 바꾼 것이다. 원본과 다른 점: 밝은 배경이 기본, 글자를 키움, CSS 변수 대신 색을 직접 씀(PowerPoint·Word·한글에 붙여 넣을 때 색이 깨지지 않게), PNG 변환은 `scripts/to_png.py` 사용.

결과물은 `.svg` 파일 하나와, 가능하면 같은 이름의 `.png`.

## 기본 규칙

1. 루트: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H" width="W" height="H">`. 모든 내용 + 사방 40px 여백이 들어가게 W, H를 잡는다.
2. 외부 자원 금지: `@import`, 웹 글꼴, 외부 이미지, 스크립트를 넣지 않는다.
3. 색은 아래 팔레트의 16진수 값을 속성에 직접 쓴다. `var(--...)`를 쓰지 않는다.
4. 맨 위에 `<style>` 한 번: `text { font-family: 'Pretendard','Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR','Noto Sans CJK KR',sans-serif; }`
   - 영어로만 된 그림은 `text { font-family: 'Inter','Segoe UI','Helvetica Neue',Arial,sans-serif; }`로 바꾼다.
   - 파일 이름·명령어·코드는 그 `<text>`에만 `style="font-family:'SF Mono','Cascadia Code',Consolas,Menlo,monospace"`를 붙인다. `font-family` 속성으로 쓰면 위 `<style>`에 덮여 적용되지 않는다.
5. 그리는 순서(뒤에서 앞으로): 배경 → 영역 테두리 → 화살표 → 상자 → 글자 → 범례 → 제목.
6. 상자 안 글자는 `text-anchor="middle"`. 상자 폭은 (가장 긴 줄의 글자 폭) + 32 이상. 글자 폭은 한글 한 글자를 글꼴 크기 × 1.0, 영문·숫자 한 글자를 글꼴 크기 × 0.55로 더한다. 고정폭 글꼴은 글자당 0.6.
7. XML 주석을 넣지 않는다. `&`는 `&amp;`, `<`는 `&lt;`로 쓴다.

## 크기

| 역할 | 글꼴 크기 | 굵기 | 색 |
|---|---|---|---|
| 제목 | 26 | 700 | `#0f172a` |
| 부제 | 15 | 400 | `#475569` |
| 상자 이름 | 17 | 600 | `#0f172a` |
| 상자 설명 | 13 | 400 | `#475569` |
| 화살표 라벨 | 13 | 500 | `#334155` |

- 상자: 높이 64(설명 있으면 84), 모서리 `rx="10"`, 테두리 2px.
- 상자 사이 간격: 세로 56 이상, 가로 48 이상.
- 제목은 왼쪽 위(40, 56). 본문은 y=110부터.

## 팔레트 (밝은 배경, 기본)

| 역할 | 채움 | 테두리 |
|---|---|---|
| 배경 | `#ffffff` | |
| 시작·끝, 강조 | `#dbeafe` | `#2563eb` |
| 일반 단계 | `#f1f5f9` | `#64748b` |
| 판단(분기) | `#fef3c7` | `#d97706` |
| 완료·성공 | `#dcfce7` | `#16a34a` |
| 오류·반려 | `#fee2e2` | `#dc2626` |
| 데이터·저장 | `#ede9fe` | `#7c3aed` |
| 외부 | `#ffffff` | `#94a3b8` (점선 `stroke-dasharray="6,4"`) |
| 화살표 | | `#475569` |

사용자가 색을 지정하면: 일반 단계의 테두리를 그 색으로, 채움은 같은 색을 밝게 한 값으로 바꾼다. 시작·끝 상자는 그 색으로 채우고 글자를 `#ffffff`로 쓴다. 판단과 오류 색은 그대로 둔다.

어두운 배경을 요청받으면: 배경 `#0f172a`, 글자 `#f8fafc`, 설명 `#94a3b8`, 채움은 위 테두리 색에 `fill-opacity="0.18"`.

한 그림에 역할 색은 3~4가지만 쓴다.

## 부품

화살표 머리(맨 위 `<defs>`에 한 번):
```svg
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
    <polygon points="0 0, 10 4, 0 8" fill="#475569"/>
  </marker>
</defs>
```

단계 상자:
```svg
<rect x="X" y="Y" width="200" height="64" rx="10" fill="#f1f5f9" stroke="#64748b" stroke-width="2"/>
<text x="X+100" y="Y+38" font-size="17" font-weight="600" fill="#0f172a" text-anchor="middle">교육 신청</text>
```

판단 마름모 (중심 CX, CY):
```svg
<polygon points="CX,CY-44 CX+90,CY CX,CY+44 CX-90,CY" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
<text x="CX" y="CY+6" font-size="16" font-weight="600" fill="#0f172a" text-anchor="middle">승인?</text>
```

화살표와 라벨:
```svg
<path d="M X1 Y1 L X2 Y2" fill="none" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>
<text x="LX" y="LY" font-size="13" font-weight="500" fill="#334155">예</text>
```
꺾이는 연결은 `M x1 y1 L x1 ym L x2 ym L x2 y2`처럼 직각으로. 화살표 끝은 상자 테두리에서 멈춘다(상자 안으로 들어가지 않게).

영역(묶음) 테두리:
```svg
<rect x="X" y="Y" width="W" height="H" rx="14" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="8,5"/>
<text x="X+16" y="Y+24" font-size="14" font-weight="600" fill="#475569">기획 단계</text>
```

## 종류별 배치

| 종류 | 배치 |
|---|---|
| 순서도 | 기본은 위에서 아래(세로). 주 경로는 가운데 직선, "아니오" 분기는 오른쪽. 되돌아가는 선은 바깥쪽으로 돌려 연결. 시작·끝은 `rx="32"` 둥근 상자. 가로형(슬라이드용)을 요청받으면 왼쪽에서 오른쪽으로 놓고, 주 경로는 가운데 가로 직선, 분기는 위아래로 벌린다. 상자 폭은 200~240으로 줄이고 설명은 두 줄로 나눈다 |
| 시퀀스 | 참여자 상자를 맨 위에 가로로, 아래로 점선 생명선. 메시지는 가로 화살표(요청 실선, 응답 점선), 위에서 아래로 시간 순. 메시지에 번호 |
| 상태도 | 상태는 둥근 상자. 시작은 채운 원, 끝은 이중 원. 전이 라벨은 `이벤트 [조건]` |
| 마인드맵 | 가운데 중심 주제, 바깥으로 곡선 가지(`C` 베지어). 가지마다 색 하나. 바깥으로 갈수록 글자 작게 |
| 타임라인 | 가로 축 하나, 시점마다 원 표시, 설명은 위아래 번갈아 |
| 계층·조직도 | 위에서 아래 트리, 같은 단계는 같은 y |

## 완성 후

1. `python3 scripts/check.py 파일.svg`로 형식을 검사한다.
2. `python3 scripts/to_png.py 파일.svg`로 PNG를 만든다(2배 해상도). 변환 도구가 없다고 나오면 SVG만 전달하고, 브라우저에서 열어 캡처하거나 PowerPoint에 SVG를 바로 넣을 수 있다고 알린다.
