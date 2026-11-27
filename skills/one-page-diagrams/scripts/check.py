#!/usr/bin/env python3
"""그림 파일 형식 검사. 표준 라이브러리만 사용.

사용법:
    python3 check.py 파일 [파일 ...]

지원: .svg, .drawio, .excalidraw, .html(인포그래픽·구조도), .spec.json
오류가 있으면 종료 코드 1, 경고만 있으면 0.
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

TEMPLATES = """chart-bar-plain-text chart-column-simple chart-line-plain-text chart-pie-compact-card
chart-pie-donut-pill-badge chart-pie-donut-plain-text chart-pie-plain-text chart-wordcloud
compare-binary-horizontal-badge-card-arrow compare-binary-horizontal-simple-fold
compare-binary-horizontal-underline-text-vs compare-hierarchy-left-right-circle-node-pill-badge
compare-quadrant-quarter-circular compare-quadrant-quarter-simple-card compare-swot
hierarchy-mindmap-branch-gradient-capsule-item hierarchy-mindmap-level-gradient-compact-card hierarchy-structure
hierarchy-tree-curved-line-rounded-rect-node hierarchy-tree-tech-style-badge-card hierarchy-tree-tech-style-capsule-item
list-column-done-list list-column-simple-vertical-arrow list-column-vertical-icon-arrow list-grid-badge-card
list-grid-candy-card-lite list-grid-ribbon-card list-row-horizontal-icon-arrow list-sector-plain-text
list-waterfall-badge-card list-waterfall-compact-card list-zigzag-down-compact-card list-zigzag-down-simple
list-zigzag-up-compact-card list-zigzag-up-simple relation-dagre-flow-tb-animated-badge-card
relation-dagre-flow-tb-animated-simple-circle-node relation-dagre-flow-tb-badge-card
relation-dagre-flow-tb-simple-circle-node sequence-ascending-stairs-3d-underline-text sequence-ascending-steps
sequence-circular-simple sequence-color-snake-steps-horizontal-icon-line sequence-cylinders-3d-simple
sequence-filter-mesh-simple sequence-funnel-simple sequence-horizontal-zigzag-underline-text
sequence-mountain-underline-text sequence-pyramid-simple sequence-roadmap-vertical-plain-text
sequence-roadmap-vertical-simple sequence-snake-steps-compact-card sequence-snake-steps-simple
sequence-snake-steps-underline-text sequence-stairs-front-compact-card sequence-stairs-front-pill-badge
sequence-timeline-rounded-rect-node sequence-timeline-simple sequence-zigzag-pucks-3d-simple
sequence-zigzag-steps-underline-text sequence-interaction-default-badge-card
sequence-interaction-default-animated-badge-card sequence-interaction-default-compact-card
sequence-interaction-default-capsule-item sequence-interaction-default-rounded-rect-node""".split()
MAIN_FIELDS = {"lists", "sequences", "compares", "values", "root", "nodes", "items"}


class Report:
    def __init__(self, name):
        self.name, self.errors, self.warnings = name, [], []

    def err(self, m):
        self.errors.append(m)

    def warn(self, m):
        self.warnings.append(m)


def text_units(s):
    """글자 폭을 글꼴 크기 단위로 어림한다. 한글·한자·전각 기호 1.0, 영문·숫자 0.55."""
    total = 0.0
    for ch in s:
        if ch == " ":
            total += 0.3
        elif ch in ".,:;'!|()[]{}/-":
            total += 0.35
        elif ord(ch) < 0x2000:
            total += 0.4 if ch in "·" else 0.55 if ord(ch) < 0x80 else 0.6
        else:
            total += 1.0
    return total


def _num(v):
    try:
        return float(re.sub(r"[^0-9.+-]", "", str(v)))
    except ValueError:
        return None


def check_svg_overflow(root, r):
    """글자가 자기 상자(또는 그림 가장자리) 밖으로 나가는지 폭을 어림해 확인한다."""
    vb = [_num(v) for v in root.attrib.get("viewBox", "").replace(",", " ").split()]
    vb_w = vb[2] if len(vb) == 4 and vb[2] else None
    rects = []
    for el in root.iter():
        if el.tag.endswith("rect") and el.attrib.get("fill", "") != "none":
            x, y = _num(el.attrib.get("x", 0)) or 0.0, _num(el.attrib.get("y", 0)) or 0.0
            w, h = _num(el.attrib.get("width")), _num(el.attrib.get("height"))
            if not w or not h or (vb_w and w >= vb_w):
                continue
            rects.append((x, y, w, h))
    for t in root.iter():
        if not (t.tag.endswith("text") and t.text and t.text.strip()):
            continue
        s = t.text.strip()
        size = _num(t.attrib.get("font-size", 16)) or 16.0
        x, y = _num(t.attrib.get("x")), _num(t.attrib.get("y"))
        if x is None or y is None:
            continue
        width = text_units(s) * size
        anchor = t.attrib.get("text-anchor", "start")
        left = x - width / 2 if anchor == "middle" else x - width if anchor == "end" else x
        right = left + width
        inside = [b for b in rects if b[0] <= x <= b[0] + b[2] and b[1] <= y <= b[1] + b[3]]
        short = s if len(s) <= 20 else s[:20] + "..."
        if inside:
            bx, _, bw, _ = min(inside, key=lambda b: b[2] * b[3])
            if left < bx + 8 or right > bx + bw - 8:
                r.warn(f"글자가 상자 밖으로 나갈 수 있습니다(글자 약 {width:.0f}px, 상자 {bw:.0f}px): '{short}'")
        elif vb_w and (left < 0 or right > vb_w):
            r.warn(f"글자가 그림 밖으로 나갈 수 있습니다(글자 약 {width:.0f}px): '{short}'")


def check_svg_text(text, r, where="SVG"):
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        r.err(f"{where} XML 오류: {e}")
        return
    if not root.tag.endswith("svg"):
        r.err(f"{where} 최상위 요소가 <svg>가 아닙니다.")
    if "viewBox" not in root.attrib:
        r.err(f"{where}에 viewBox가 없습니다.")
    if "var(--" in text:
        r.warn(f"{where}에 CSS 변수(var(--...))가 있습니다. PowerPoint·Word에서 색이 빠질 수 있습니다.")
    if re.search(r"<script|@import|https?://(?!www\.w3\.org)", text):
        r.warn(f"{where}에 외부 자원이나 스크립트가 있습니다.")
    check_svg_overflow(root, r)


def check_svg(path, r):
    check_svg_text(open(path, encoding="utf-8").read(), r)


def check_drawio(path, r):
    text = open(path, encoding="utf-8").read()
    if "<!--" in text:
        r.err("XML 주석이 있습니다. 지우세요.")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        r.err(f"XML 오류: {e}")
        return
    cells = list(root.iter("mxCell"))
    if not cells:
        r.err("mxCell이 없습니다.")
        return
    ids = [c.get("id") for c in cells]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        r.err(f"중복 id: {', '.join(sorted(dup))}")
    if "0" not in ids or "1" not in ids:
        r.err('기본 셀 id="0", id="1"이 없습니다.')
    idset = set(ids)
    for c in cells:
        cid = c.get("id")
        if cid not in ("0",) and c.get("parent") not in idset:
            r.err(f"셀 {cid}의 parent '{c.get('parent')}'가 없습니다.")
        if c.get("parent") == cid:
            r.err(f"셀 {cid}가 자기 자신을 parent로 가집니다.")
        if c.get("edge") == "1":
            if c.find("mxGeometry") is None:
                r.err(f"연결선 {cid}에 <mxGeometry relative=\"1\" as=\"geometry\"/>가 없습니다.")
            for k in ("source", "target"):
                if c.get(k) and c.get(k) not in idset:
                    r.err(f"연결선 {cid}의 {k} '{c.get(k)}'가 없습니다.")
        if c.get("vertex") == "1" and c.find("mxGeometry") is None:
            r.err(f"도형 {cid}에 mxGeometry가 없습니다.")


def check_excalidraw(path, r):
    try:
        data = json.load(open(path, encoding="utf-8"))
    except ValueError as e:
        r.err(f"JSON 오류: {e}")
        return
    if data.get("type") != "excalidraw":
        r.err('"type": "excalidraw"가 아닙니다.')
    els = data.get("elements")
    if not isinstance(els, list) or not els:
        r.err("elements가 비어 있습니다.")
        return
    byid = {}
    for e in els:
        if "id" not in e or "type" not in e:
            r.err("id나 type이 없는 요소가 있습니다.")
            continue
        if e["id"] in byid:
            r.err(f"중복 id: {e['id']}")
        byid[e["id"]] = e
    for e in els:
        for k in ("x", "y", "width", "height"):
            if not isinstance(e.get(k), (int, float)):
                r.err(f"요소 {e.get('id')}의 {k}가 숫자가 아닙니다.")
        if e.get("type") == "text":
            if "text" not in e:
                r.err(f"글자 요소 {e['id']}에 text가 없습니다.")
            c = e.get("containerId")
            if c:
                if c not in byid:
                    r.err(f"글자 {e['id']}의 containerId '{c}'가 없습니다.")
                elif {"type": "text", "id": e["id"]} not in (byid[c].get("boundElements") or []):
                    r.warn(f"{c}의 boundElements에 글자 {e['id']}가 없습니다.")
        if e.get("type") in ("arrow", "line"):
            pts = e.get("points")
            if not isinstance(pts, list) or len(pts) < 2:
                r.err(f"선 {e['id']}의 points가 2개 미만입니다.")
            for b in ("startBinding", "endBinding"):
                bd = e.get(b)
                if bd and bd.get("elementId") not in byid:
                    r.err(f"화살표 {e['id']}의 {b} 대상 '{bd.get('elementId')}'가 없습니다.")


def check_infographic(syntax, r):
    lines = [l for l in syntax.strip("\n").splitlines() if l.strip()]
    if not lines:
        r.err("인포그래픽 문법이 비어 있습니다.")
        return
    m = re.match(r"^infographic\s+(\S+)\s*$", lines[0])
    if not m:
        r.err("첫 줄이 'infographic <템플릿 이름>'이 아닙니다.")
        return
    tpl = m.group(1)
    if tpl not in TEMPLATES:
        r.err(f"알 수 없는 템플릿: {tpl}")
    if "\t" in syntax:
        r.err("탭 문자가 있습니다. 공백 두 칸으로 들여쓰세요.")
    if "`" in syntax or "${" in syntax:
        r.err("백틱(`)이나 ${ 가 있습니다. HTML 템플릿이 깨집니다.")
    fields = {l.strip() for l in lines if re.match(r"^  \S", l) and l.strip() in MAIN_FIELDS}
    if len(fields) > 1:
        r.err(f"주 데이터 필드가 여러 개입니다: {', '.join(sorted(fields))}")
    if tpl.startswith(("compare-binary", "compare-hierarchy-left-right")):
        tops = [l for l in lines if re.match(r"^    - ", l)]
        if len(tops) != 2:
            r.err(f"{tpl}은 compares 최상위 항목이 정확히 2개여야 합니다(현재 {len(tops)}개).")


def check_html(path, r):
    text = open(path, encoding="utf-8").read()
    if "{{" in text and "}}" in text and re.search(r"\{\{[A-Z_]+\}\}", text):
        r.err("채우지 않은 자리표시자가 남아 있습니다: " + ", ".join(sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", text)))))
    m = re.search(r"String\.raw`(.*?)`;", text, re.S)
    if m:
        check_infographic(m.group(1), r)
    m = re.search(r'(<svg id="diagram".*?</svg>)', text, re.S)
    if m:
        check_svg_text(m.group(1), r, "구조도 SVG")
    if re.search(r"fonts\.googleapis|fonts\.gstatic", text):
        r.warn("웹 글꼴을 불러옵니다. 오프라인에서 글꼴이 바뀔 수 있습니다.")


def check_spec(path, r):
    try:
        spec = json.load(open(path, encoding="utf-8"))
    except ValueError as e:
        r.err(f"JSON 오류: {e}")
        return
    nodes = spec.get("nodes") or []
    if not nodes:
        r.err("nodes가 비어 있습니다.")
    ids = {n.get("id") for n in nodes}
    for n in nodes:
        for line in str(n.get("label", "")).split("\n"):
            if text_units(line) > 12:
                r.warn(f"노드 {n.get('id')} 라벨 한 줄이 깁니다. \\n으로 나누세요: '{line}'")
    for e in spec.get("edges", []):
        for k in ("from", "to"):
            if e.get(k) not in ids:
                r.err(f"연결선 {k} '{e.get(k)}' 노드가 없습니다.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    failed = False
    for path in sys.argv[1:]:
        r = Report(path)
        if not os.path.exists(path):
            r.err("파일이 없습니다.")
        elif path.endswith(".spec.json"):
            check_spec(path, r)
        else:
            ext = os.path.splitext(path)[1].lower()
            fn = {".svg": check_svg, ".drawio": check_drawio, ".excalidraw": check_excalidraw,
                  ".html": check_html, ".htm": check_html}.get(ext)
            if fn:
                fn(path, r)
            else:
                r.err(f"검사할 수 없는 형식: {ext}")
        status = "오류" if r.errors else "통과"
        print(f"[{status}] {path}")
        for m in r.errors:
            print("  오류: " + m)
        for m in r.warnings:
            print("  경고: " + m)
        failed = failed or bool(r.errors)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
