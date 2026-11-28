"""Build lite/ (directory edition: Markdown, JSON and PNG only) from the full skill.

Run: python3 tools/make_lite.py
The icon (lite/.claude-plugin/icon.png) is kept; its source is tools/icon.svg.
"""
import json, os, re, shutil, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "skills", "one-page-diagrams")
OUT = os.path.join(ROOT, "lite")
DST = os.path.join(OUT, "skills", "one-page-diagrams")
ICON = os.path.join(OUT, ".claude-plugin", "icon.png")
icon = open(ICON, "rb").read() if os.path.exists(ICON) else None
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.join(DST, "references"))
os.makedirs(os.path.join(OUT, ".claude-plugin"))


def rd(p):
    return open(p, encoding="utf-8").read()


def wr(p, s):
    open(p, "w", encoding="utf-8").write(s)


def sub(s, old, new):
    assert old in s, old[:60]
    return s.replace(old, new)


def cut(s, start, end):
    """Replace from the line starting with `start` up to (not including) the line starting with `end`."""
    i = s.index(start)
    j = s.index(end, i) if end else len(s)
    return s[:i], s[j:]


# ---------- SKILL.md
s = rd(os.path.join(SRC, "SKILL.md"))
s = sub(s, "| 담당자별 칸(스윔레인)이 있는 업무 흐름도, 나중에 고칠 그림 | draw.io | `.drawio` + 편집 링크 |",
        "| 담당자별 칸(스윔레인)이 있는 업무 흐름도, 나중에 고칠 그림 | draw.io | `.drawio` |")
s = sub(s, "draw.io와 엑스칼리드로는 명세에 `\"direction\": \"LR\"`을 쓴다.",
        "draw.io와 엑스칼리드로는 진행 순서를 왼쪽에서 오른쪽 열로 놓는다.")
s = sub(s, "HTML 틀(`assets/`)을 쓸 때는", "HTML 틀(`references/*-template.md`)을 쓸 때는")
a, b = cut(s, "- `scripts/`의 Python 스크립트는", "## 4단계: 검사")
s = a + "- 이 스킬에는 실행 파일이 없다. 모든 결과는 모델이 텍스트로 직접 쓴다. 좌표도 참고 문서의 격자 규칙으로 직접 계산한다.\n\n" + b
a, b = cut(s, "## 4단계: 검사", "## 6단계: 전달 문구")
s = a + """## 4단계: 검사

파일을 넘기기 전에 쓴 내용을 다시 읽고 확인한다.

- 형식: 태그와 괄호가 모두 닫혔는지, id가 겹치지 않는지, `&`와 `<`를 `&amp;`와 `&lt;`로 썼는지 본다. JSON은 마지막 쉼표가 없는지 본다.
- 글자가 상자 밖으로 넘치지 않는지, 화살표가 상자를 가로지르지 않는지 좌표로 확인한다. 글자 폭은 한글 한 글자를 글꼴 크기의 1.0배, 영문·숫자 한 글자를 0.55배로 잡는다. (가장 긴 줄의 글자 폭) + 32가 상자 폭보다 크면 상자를 넓히거나 줄을 나눈다.
- 그림 전체가 viewBox(또는 캔버스) 안에 사방 40 여백을 두고 들어가는지 본다.
- 사용자 글에 없던 내용이 들어가지 않았는지 다시 본다.

## 5단계: PNG 받기

이 스킬은 PNG를 직접 만들지 않는다. 사용자가 이미지·PNG를 원하거나 보고서·슬라이드에 넣는다고 했으면 원본 파일과 함께 아래 방법을 한 줄로 안내한다.

- 인포그래픽·구조도 `.html`: 브라우저로 열고 오른쪽 위 "PNG로 저장" 버튼.
- `.svg`: PowerPoint·Word·한글에 그대로 넣을 수 있다. PNG가 필요하면 브라우저로 열어 화면을 캡처한다.
- `.drawio`: https://app.diagrams.net 에서 열고 파일 → 내보내기 → PNG.
- `.excalidraw`: https://excalidraw.com 에서 열고 메뉴 → 이미지 내보내기 → PNG.

지금 대화에 화면을 캡처하거나 이미지를 만드는 도구가 이미 있으면 그 도구로 PNG를 만들어 함께 준다. 만든 PNG는 열어 보고 글자 겹침, 잘림, 빈 그림이 없는지 확인한다.

""" + b
s = sub(s, "만든 파일 목록(원본, PNG).", "만든 파일 목록.")
s = sub(s, "   - `.drawio`: https://app.diagrams.net 에서 파일 열기(설치 불필요). 링크를 만들었으면 링크도 준다.",
        "   - `.drawio`: https://app.diagrams.net 에서 파일 열기(설치 불필요).")
assert "scripts/" not in s and "python" not in s.lower(), "SKILL.md still mentions scripts"
wr(os.path.join(DST, "SKILL.md"), s)

# ---------- infographic.md
s = rd(os.path.join(SRC, "references", "infographic.md"))
s = sub(s, "4. `assets/infographic-template.html`을 복사해 `{{TITLE}}`과 `{{SYNTAX}}`를 바꾼다.\n5. `python3 scripts/check.py <파일>`로 검사한다.",
        "4. `references/infographic-template.md`의 HTML을 그대로 옮겨 적고 `{{TITLE}}`과 `{{SYNTAX}}`를 바꾼다.\n5. 문법의 들여쓰기(공백 2칸)와 템플릿 이름 철자를 다시 읽어 확인한다. `{{TITLE}}`은 브라우저 탭과 저장 파일 이름에 쓰이므로 문법의 `title`과 같은 글을 넣는다.")
s = re.sub(r"python3 scripts/\S+[^\n]*", "", s)
assert "scripts/" not in s and "assets/" not in s, "infographic.md"
wr(os.path.join(DST, "references", "infographic.md"), s)

# ---------- architecture.md
s = rd(os.path.join(SRC, "references", "architecture.md"))
s = sub(s, "3. `assets/architecture-template.html`을 복사해", "3. `references/architecture-template.md`의 HTML을 그대로 옮겨 적고")
s = sub(s, "5. `python3 scripts/check.py 이름.html`, `python3 scripts/to_png.py 이름.html`.",
        "5. 상자 좌표와 글자 폭을 다시 계산해 겹침과 넘침이 없는지 확인한다.")
s = sub(s, "PNG 저장 버튼). 가능하면 `이름.png`도.", "PNG 저장 버튼).")
assert "scripts/" not in s and "assets/" not in s, "architecture.md"
wr(os.path.join(DST, "references", "architecture.md"), s)

# ---------- svg-diagram.md
s = rd(os.path.join(SRC, "references", "svg-diagram.md"))
s = sub(s, ", PNG 변환은 `scripts/to_png.py` 사용.", ".")
s = sub(s, "결과물은 `.svg` 파일 하나와, 가능하면 같은 이름의 `.png`.", "결과물은 `.svg` 파일 하나.")
a, _ = cut(s, "## 완성 후", None)
s = a + """## 완성 후

1. 쓴 SVG를 다시 읽어 태그가 모두 닫혔는지, 상자마다 (가장 긴 줄의 글자 폭) + 32가 상자 폭 이하인지, 모든 좌표가 viewBox 안인지 확인한다.
2. SVG는 PowerPoint·Word·한글에 그대로 넣을 수 있다. PNG가 필요하면 브라우저에서 열어 캡처하라고 안내한다.
"""
assert "scripts/" not in s, "svg-diagram.md"
wr(os.path.join(DST, "references", "svg-diagram.md"), s)

# ---------- drawio.md
s = rd(os.path.join(SRC, "references", "drawio.md"))
head, _ = cut(s, "결과물:", None)
rest = s[s.index("`.drawio` 파일은 아래 XML이다."):]
xml_part, tail = rest.split("파일을 쓴 뒤 실행할 수 있으면", 1)
s = head + """결과물: `이름.drawio` — https://app.diagrams.net 에서 열어 바로 수정(설치·로그인 불필요).

## 작성 순서

1. 단계마다 담당자(레인), 순서(col), 종류(시작, 단계, 판단, 완료, 반려)를 표로 먼저 정리한다. 같은 칸에 두 단계를 두지 않는다.
2. 아래 격자 규칙으로 좌표를 계산해 XML을 쓴다.
3. 가로형(기본, 레인이 있을 때)은 col이 진행 순서다. 세로형은 row가 진행 순서다.
4. 화살표 라벨은 1~4단어. 점선(`dashed=1;`)은 예외·반려 같은 보조 흐름에만 쓴다.

## XML 형식

""" + xml_part.rstrip() + """

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
"""
assert "scripts/" not in s and "spec.json" not in s, "drawio.md"
wr(os.path.join(DST, "references", "drawio.md"), s)

# ---------- excalidraw.md
s = rd(os.path.join(SRC, "references", "excalidraw.md"))
head, _ = cut(s, "결과물:", None)
rest = s[s.index("파일 뼈대:"):]
body, _ = cut(rest, "## 전달 시 안내 문구", None)
s = head + """결과물: `이름.excalidraw` — https://excalidraw.com 에서 왼쪽 위 메뉴 → 열기. 설치·로그인 불필요.

## 작성 순서

1. 상자를 격자에 놓는다. 가로형은 `x = 100 + col*280`, `y = 100 + row*150`. 상자는 180×70, 글자가 길면 폭을 `fontSize × 글자 수 + 40`으로 넓힌다.
2. 상자마다 글자 요소를 하나씩 만들고 서로 참조하게 한다.
3. 화살표는 앞 상자의 오른쪽 가운데에서 뒤 상자의 왼쪽 가운데로 긋는다(세로형은 아래 가운데에서 위 가운데로).
4. 손그림 정도는 요소의 `roughness`로 정한다. 0(깔끔) ~ 2(거친 손그림), 기본 1.

## JSON 형식

""" + body.rstrip() + """

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
"""
assert "scripts/" not in s and "spec.json" not in s and "Gaegu" not in s, "excalidraw.md"
wr(os.path.join(DST, "references", "excalidraw.md"), s)

# ---------- HTML templates as Markdown
for name, note in (("infographic", "`{{TITLE}}`과 `{{SYNTAX}}`만 바꾼다. 나머지는 그대로 둔다."),
                   ("architecture", "`{{TITLE}}`, `{{SUBTITLE}}`, `{{SVG_BODY}}`, `{{CARDS}}`, `{{FOOTER}}`만 바꾼다. 나머지는 그대로 둔다.")):
    html = rd(os.path.join(SRC, "assets", name + "-template.html")).rstrip()
    wr(os.path.join(DST, "references", name + "-template.md"),
       "# " + name + " HTML 틀\n\n아래 HTML을 `.html` 파일로 옮겨 적는다. " + note + "\n\n```html\n" + html + "\n```\n")

# ---------- plugin.json, LICENSE, NOTICE, README
full = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8"))
full["description"] = "글 몇 줄을 보고서·강의자료용 그림 한 장으로. 인포그래픽, 순서도, draw.io 업무 흐름도, 엑스칼리드로 손그림, 구조도를 무료·무설치 파일(HTML, SVG, .drawio, .excalidraw)로 만든다."
wr(os.path.join(OUT, ".claude-plugin", "plugin.json"), json.dumps(full, ensure_ascii=False, indent=2) + "\n")
shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(OUT, "LICENSE"))

n = rd(os.path.join(ROOT, "NOTICE.md"))
a, _ = cut(n, "## 포함된 글꼴", None)
n = a + "그림을 열 때 브라우저가 인터넷에서 불러오는 라이브러리(AntV Infographic)는 이 폴더에 포함되어 있지 않으며 그 라이선스를 따릅니다.\n\nApache-2.0 원문: https://www.apache.org/licenses/LICENSE-2.0\n"
n = n.replace("`references/infographic.md`, `assets/infographic-template.html`", "`references/infographic.md`, `references/infographic-template.md`")
n = n.replace("`references/drawio.md`, `scripts/drawio_link.py`, `scripts/to_png.py`", "`references/drawio.md`")
n = n.replace("`references/excalidraw.md`, `scripts/build.py`, `scripts/to_png.py`", "`references/excalidraw.md`")
n = n.replace("`references/architecture.md`, `assets/architecture-template.html`", "`references/architecture.md`, `references/architecture-template.md`")
n = n.replace(", 편집 링크(#R, #create) 형식, 뷰어 임베드 방식", "").replace(", `exportToSvg`", "")
assert "scripts/" not in n and "assets/" not in n, "NOTICE"
wr(os.path.join(OUT, "NOTICE.md"), n)

wr(os.path.join(OUT, "README.md"), """# 한 장 그림 (One-Page Diagrams)

글 몇 줄을 보고서·강의자료에 넣을 그림 한 장으로 바꾸는 스킬입니다. 유료 API, 이미지 생성 모델, 로그인 없이 모델이 파일을 직접 씁니다.

## 만드는 그림

| 방식 | 알맞은 내용 | 결과 파일 |
|---|---|---|
| 인포그래픽 | 요점, 단계, 비교, SWOT, 타임라인 | `.html` |
| SVG 다이어그램 | 순서도, 시퀀스, 상태도, 마인드맵 | `.svg` |
| draw.io | 담당자별 업무 흐름도, 나중에 고칠 그림 | `.drawio` |
| 엑스칼리드로 | 손그림 느낌의 화이트보드 스케치 | `.excalidraw` |
| 구조도 | 서비스·시스템 구성 | `.html` |

## 쓰는 법

그리고 싶은 내용을 글로 적고 "그려줘"라고 하면 됩니다.

```
교육 신청 승인 절차를 담당자별 흐름도로 그려줘. 신청자가 신청하면 팀장이 검토하고, 승인되면 교육팀이 수강 등록을 해.
```

그리기 전에 넣을 곳(문서·슬라이드), 느낌(기본·손그림·어두운 배경), 색을 한 번 묻습니다. "알아서 해줘"라고 하면 묻지 않고 기본값으로 만듭니다.

## 지키는 규칙

- 사용자가 쓰지 않은 수치, 이름, 단계를 지어내지 않습니다. 꼭 필요한데 없는 정보는 그림에 `[확인 필요]`라고 적습니다.
- 제목은 결론이 드러나는 짧은 문장으로 씁니다.
- 웹 글꼴을 불러오지 않습니다. PC에 있는 한글 글꼴을 씁니다.

## 이 판과 전체 판의 차이

이 폴더는 Claude 플러그인 목록용 판입니다. 문서와 틀만 들어 있고 실행 파일이 없습니다.

- PNG는 결과 파일을 연 뒤 받습니다. HTML은 "PNG로 저장" 버튼, draw.io와 엑스칼리드로는 각 사이트의 내보내기 메뉴를 씁니다.
- 좌표 자동 계산, 형식 검사, PNG 자동 변환, 한글 손글씨 글꼴은 전체 판에 있습니다: https://github.com/dschloe/one-page-diagrams

## 데이터

이 스킬은 사용자의 글을 외부로 보내지 않습니다. 인포그래픽 HTML은 열 때 브라우저가 AntV Infographic 라이브러리를 인터넷에서 불러옵니다. 그림 내용은 PC 안에서만 처리됩니다.

## 라이선스

MIT. 참고한 공개 프로젝트는 `NOTICE.md`에 적었습니다.
""")

if icon:
    open(ICON, "wb").write(icon)

# ---------- report
bad = []
for d, _, fs in os.walk(OUT):
    for f in fs:
        p = os.path.join(d, f)
        ext = os.path.splitext(f)[1].lower()
        if ext not in (".md", ".json", ".png", "") or os.path.getsize(p) > 250000:
            bad.append(p)
        print(os.path.getsize(p), os.path.relpath(p, ROOT))
print("not allowed:", bad)
