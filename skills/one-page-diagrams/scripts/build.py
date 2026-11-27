#!/usr/bin/env python3
"""명세(spec.json)로 .drawio 또는 .excalidraw 파일을 만든다. 표준 라이브러리만 사용.

사용법:
    python3 build.py 이름.spec.json --to drawio      -> 이름.drawio (+ 편집 링크 출력)
    python3 build.py 이름.spec.json --to excalidraw  -> 이름.excalidraw
    python3 build.py 이름.spec.json --to both
    옵션: -o 출력경로(확장자 제외)

명세 형식은 references/drawio.md 참고.
"""
import argparse
import json
import os
import random
import sys
import time
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawio_link import drawio_url  # noqa: E402

KINDS = {
    #            drawio fill, drawio stroke, excalidraw bg
    "start":    ("#dbeafe", "#2563eb", "#a5d8ff"),
    "end":      ("#dbeafe", "#2563eb", "#a5d8ff"),
    "step":     ("#f1f5f9", "#64748b", "#e9ecef"),
    "decision": ("#fef3c7", "#d97706", "#ffec99"),
    "done":     ("#dcfce7", "#16a34a", "#b2f2bb"),
    "error":    ("#fee2e2", "#dc2626", "#ffc9c9"),
    "data":     ("#ede9fe", "#7c3aed", "#d0bfff"),
    "external": ("#ffffff", "#94a3b8", "transparent"),
}

CELL_W, CELL_H = 230, 130
NODE_W, NODE_H, DEC_H = 170, 64, 84
LANE_H, LANE_HEAD = 150, 48
MARGIN_X, TOP = 30, 90


def fail(msg):
    print("오류: " + msg, file=sys.stderr)
    sys.exit(1)


def text_width(line, size):
    return sum(size * (1.0 if ord(ch) > 0x1100 else 0.6) for ch in line)


def node_size(node, size=16):
    lines = node["label"].split("\n")
    w = max(text_width(l, size) for l in lines) + 44
    w = max(140, min(w, CELL_W - 30))
    h = DEC_H if node["kind"] == "decision" else NODE_H
    h = max(h, len(lines) * size * 1.3 + 30)
    return w, h


def load_spec(path):
    try:
        with open(path, encoding="utf-8") as f:
            spec = json.load(f)
    except (OSError, ValueError) as e:
        fail(f"명세 파일을 읽지 못했습니다: {e}")
    nodes = spec.get("nodes") or fail("nodes가 비어 있습니다.")
    lanes = spec.get("lanes") or []
    direction = spec.get("direction", "LR" if lanes else "TB").upper()
    ids = set()
    lane_count = {}
    for i, n in enumerate(nodes):
        if "id" not in n or "label" not in n:
            fail(f"{i}번째 노드에 id 또는 label이 없습니다.")
        if n["id"] in ids:
            fail(f"노드 id가 중복됩니다: {n['id']}")
        ids.add(n["id"])
        n["kind"] = n.get("kind", "step")
        if n["kind"] not in KINDS:
            fail(f"알 수 없는 kind: {n['kind']} (가능: {', '.join(KINDS)})")
        if lanes:
            if n.get("lane") not in lanes:
                fail(f"노드 {n['id']}의 lane '{n.get('lane')}'이 lanes 목록에 없습니다.")
            if "col" not in n:
                n["col"] = lane_count.get(n["lane"], 0)
            lane_count[n["lane"]] = n["col"] + 1
        else:
            if "row" not in n and "col" not in n:
                n["row"], n["col"] = (i, 0) if direction == "TB" else (0, i)
            n.setdefault("row", 0)
            n.setdefault("col", 0)
    seen = {}
    for n in nodes:
        key = (n.get("lane"), n.get("row"), n["col"])
        if key in seen:
            fail(f"노드 {seen[key]}와 {n['id']}가 같은 칸에 있습니다. row/col을 바꾸세요.")
        seen[key] = n["id"]
    for e in spec.get("edges", []):
        for k in ("from", "to"):
            if e.get(k) not in ids:
                fail(f"연결선의 {k} '{e.get(k)}' 노드가 없습니다.")
    spec["lanes"] = lanes
    return spec


def layout(spec):
    """각 노드의 절대 좌표(x, y, w, h)와 레인 영역을 계산한다."""
    nodes, lanes = spec["nodes"], spec["lanes"]
    max_col = max(n["col"] for n in nodes)
    pos = {}
    lane_boxes = []
    if lanes:
        width = LANE_HEAD + 30 + (max_col + 1) * CELL_W
        for i, name in enumerate(lanes):
            lane_boxes.append((name, MARGIN_X, TOP + i * LANE_H, width, LANE_H))
        for n in nodes:
            w, h = node_size(n)
            li = lanes.index(n["lane"])
            cx = MARGIN_X + LANE_HEAD + 30 + n["col"] * CELL_W + CELL_W / 2 - 15
            cy = TOP + li * LANE_H + LANE_H / 2
            pos[n["id"]] = (cx - w / 2, cy - h / 2, w, h)
    else:
        for n in nodes:
            w, h = node_size(n)
            cx = MARGIN_X + n["col"] * CELL_W + CELL_W / 2
            cy = TOP + n["row"] * CELL_H + CELL_H / 2
            pos[n["id"]] = (cx - w / 2, cy - h / 2, w, h)
    return pos, lane_boxes


# ---------------------------------------------------------------- draw.io

def drawio_value(label):
    return escape(label, {'"': "&quot;"}).replace("\n", "&lt;br&gt;")


def to_drawio(spec):
    pos, lane_boxes = layout(spec)
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    if spec.get("title"):
        cells.append(
            f'<mxCell id="title" value="{drawio_value(spec["title"])}" '
            'style="text;html=1;fontSize=22;fontStyle=1;align=left;verticalAlign=middle;" '
            f'vertex="1" parent="1"><mxGeometry x="{MARGIN_X}" y="24" width="900" height="40" as="geometry"/></mxCell>')
    lane_id = {}
    for i, (name, x, y, w, h) in enumerate(lane_boxes):
        lid = f"lane{i}"
        lane_id[name] = (lid, x, y)
        cells.append(
            f'<mxCell id="{lid}" value="{drawio_value(name)}" '
            f'style="swimlane;horizontal=0;startSize={LANE_HEAD};html=1;fontSize=15;fontStyle=1;'
            'fillColor=#f8fafc;strokeColor=#cbd5e1;swimlaneFillColor=#ffffff;" '
            f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    parent_of = {}
    for n in spec["nodes"]:
        fill, stroke, _ = KINDS[n["kind"]]
        x, y, w, h = pos[n["id"]]
        parent = "1"
        if n.get("lane"):
            parent, lx, ly = lane_id[n["lane"]]
            x, y = x - lx, y - ly
        parent_of[n["id"]] = parent
        shape = {
            "decision": "rhombus;",
            "data": "shape=cylinder3;boundedLbl=1;size=10;",
            "start": "rounded=1;arcSize=40;",
            "end": "rounded=1;arcSize=40;",
        }.get(n["kind"], "rounded=1;arcSize=14;")
        dashed = "dashed=1;" if n["kind"] == "external" else ""
        style = (f"{shape}{dashed}whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
                 "strokeWidth=2;fontSize=15;fontColor=#0f172a;")
        cells.append(
            f'<mxCell id="n_{n["id"]}" value="{drawio_value(n["label"])}" style="{style}" vertex="1" '
            f'parent="{parent}"><mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            'as="geometry"/></mxCell>')
    for i, e in enumerate(spec.get("edges", [])):
        pa, pb = parent_of[e["from"]], parent_of[e["to"]]
        parent = pa if pa == pb else "1"
        dashed = "dashed=1;" if e.get("dashed") else ""
        # 분기(마름모)에서 나가는 선이 겹치지 않도록 위/아래/오른쪽 꼭짓점을 나눠 쓴다.
        exits = ""
        src = next(n for n in spec["nodes"] if n["id"] == e["from"])
        if src["kind"] == "decision":
            sx, sy, sw, sh = pos[e["from"]]
            tx, ty, tw, th = pos[e["to"]]
            dy = (ty + th / 2) - (sy + sh / 2)
            if dy > 10:
                exits = "exitX=0.5;exitY=1;exitDx=0;exitDy=0;"
            elif dy < -10:
                exits = "exitX=0.5;exitY=0;exitDx=0;exitDy=0;"
            else:
                exits = "exitX=1;exitY=0.5;exitDx=0;exitDy=0;"
        style = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;"
                 f"strokeColor=#475569;strokeWidth=2;fontSize=13;labelBackgroundColor=#ffffff;{dashed}{exits}")
        cells.append(
            f'<mxCell id="e{i}" value="{drawio_value(e.get("label", ""))}" style="{style}" edge="1" '
            f'source="n_{e["from"]}" target="n_{e["to"]}" parent="{parent}">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>')
    body = "\n".join(cells)
    return ('<mxfile host="one-page-diagrams"><diagram name="Page-1">'
            '<mxGraphModel adaptiveColors="auto" grid="0" page="0"><root>\n'
            f"{body}\n</root></mxGraphModel></diagram></mxfile>\n")


# ------------------------------------------------------------- excalidraw

class Ex:
    def __init__(self, roughness):
        self.elements = []
        self.roughness = roughness
        self.rng = random.Random(42)
        self.now = int(time.time() * 1000)

    def base(self, eid, etype, x, y, w, h, **kw):
        el = {
            "id": eid, "type": etype, "x": round(x, 1), "y": round(y, 1),
            "width": round(w, 1), "height": round(h, 1), "angle": 0,
            "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
            "roughness": self.roughness, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": None, "seed": self.rng.randint(1, 2**31 - 1), "version": 1,
            "versionNonce": self.rng.randint(1, 2**31 - 1), "isDeleted": False,
            "boundElements": [], "updated": self.now, "link": None, "locked": False,
        }
        el.update(kw)
        self.elements.append(el)
        return el

    def text(self, eid, txt, x, y, size=18, container=None, align="center", color="#1e1e1e"):
        lines = txt.split("\n")
        w = max(text_width(l, size) for l in lines)
        h = len(lines) * size * 1.25
        if container is not None:
            cx = container["x"] + container["width"] / 2
            cy = container["y"] + container["height"] / 2
            x, y = cx - w / 2, cy - h / 2
        return self.base(
            eid, "text", x, y, w, h, strokeColor=color, text=txt, fontSize=size, fontFamily=5,
            textAlign=align, verticalAlign="middle" if container else "top",
            containerId=container["id"] if container else None, originalText=txt,
            lineHeight=1.25, autoResize=True)


def anchor(box, other):
    x, y, w, h = box
    ox, oy, ow, oh = other
    cx, cy, ocx, ocy = x + w / 2, y + h / 2, ox + ow / 2, oy + oh / 2
    dx, dy = ocx - cx, ocy - cy
    if abs(dx) >= abs(dy):
        return (x + w if dx > 0 else x, cy), "h"
    return (cx, y + h if dy > 0 else y), "v"


def to_excalidraw(spec):
    pos, lane_boxes = layout(spec)
    ex = Ex(int(spec.get("roughness", 1)))
    for i, (name, x, y, w, h) in enumerate(lane_boxes):
        ex.base(f"lane{i}", "rectangle", x, y, w, h, backgroundColor="#f8f9fa",
                strokeColor="#adb5bd", strokeWidth=1, roughness=0)
        ex.text(f"lane{i}-t", name, x + 12, y + 12, size=16, align="left", color="#495057")
    if spec.get("title"):
        ex.text("title", spec["title"], MARGIN_X, 30, size=28, align="left")
    elems = {}
    for n in spec["nodes"]:
        x, y, w, h = pos[n["id"]]
        _, _, bg = KINDS[n["kind"]]
        etype = {"decision": "diamond", "start": "ellipse", "end": "ellipse"}.get(n["kind"], "rectangle")
        if etype == "ellipse":
            x, w = x - 10, w + 20
        el = ex.base(n["id"], etype, x, y, w, h, backgroundColor=bg,
                     fillStyle="hachure" if bg != "transparent" else "solid",
                     strokeStyle="dashed" if n["kind"] == "external" else "solid",
                     roundness={"type": 3} if etype == "rectangle" else {"type": 2})
        t = ex.text(n["id"] + "-t", n["label"], 0, 0, size=18, container=el)
        el["boundElements"].append({"type": "text", "id": t["id"]})
        elems[n["id"]] = el
    for i, e in enumerate(spec.get("edges", [])):
        a, b = elems[e["from"]], elems[e["to"]]
        ba = (a["x"], a["y"], a["width"], a["height"])
        bb = (b["x"], b["y"], b["width"], b["height"])
        (sx, sy), mode = anchor(ba, bb)
        bx, by, bw, bh = bb
        src_kind = next(n["kind"] for n in spec["nodes"] if n["id"] == e["from"])
        acy = a["y"] + a["height"] / 2
        if src_kind == "decision" and abs((by + bh / 2) - acy) > 10:
            # 분기에서 위/아래 대상으로 가는 선은 위/아래 꼭짓점에서 나간다(선 겹침 방지).
            mode = "v"
            sx = a["x"] + a["width"] / 2
            sy = a["y"] + a["height"] if by + bh / 2 > acy else a["y"]
        bcx, bcy = bx + bw / 2, by + bh / 2
        if abs(sy - bcy) < 2 or abs(sx - bcx) < 2:
            (tx, ty), _ = anchor(bb, ba)
        elif mode == "h":
            # 가로로 나가서 꺾어 대상의 위/아래로 들어간다 (L자)
            tx, ty = bcx, (by if bcy > sy else by + bh)
        else:
            tx, ty = (bx if bcx > sx else bx + bw), bcy
        dx, dy = tx - sx, ty - sy
        if abs(dx) < 1 or abs(dy) < 1:
            pts = [[0, 0], [round(dx, 1), round(dy, 1)]]
        elif mode == "h":
            pts = [[0, 0], [round(dx, 1), 0], [round(dx, 1), round(dy, 1)]]
        else:
            pts = [[0, 0], [0, round(dy, 1)], [round(dx, 1), round(dy, 1)]]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        aid = f"arrow{i}"
        arrow = ex.base(
            aid, "arrow", sx, sy, max(xs) - min(xs), max(ys) - min(ys),
            strokeStyle="dashed" if e.get("dashed") else "solid", roundness={"type": 2},
            points=pts, lastCommittedPoint=None,
            startBinding={"elementId": a["id"], "focus": 0, "gap": 4},
            endBinding={"elementId": b["id"], "focus": 0, "gap": 4},
            startArrowhead=None, endArrowhead="arrow", elbowed=False)
        a["boundElements"].append({"type": "arrow", "id": aid})
        b["boundElements"].append({"type": "arrow", "id": aid})
        if e.get("label"):
            mid = [pts[1][0] / 2, pts[1][1] / 2] if len(pts) > 2 else [dx / 2, dy / 2]
            size = 16
            tw, th = text_width(e["label"], size), size * 1.25
            t = ex.base(
                aid + "-t", "text", sx + mid[0] - tw / 2, sy + mid[1] - th / 2, tw, th,
                text=e["label"], fontSize=size, fontFamily=5, textAlign="center",
                verticalAlign="middle", containerId=aid, originalText=e["label"],
                lineHeight=1.25, autoResize=True)
            arrow["boundElements"].append({"type": "text", "id": t["id"]})
    scene = {
        "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
        "elements": ex.elements,
        "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
        "files": {},
    }
    return json.dumps(scene, ensure_ascii=False, indent=1) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--to", choices=["drawio", "excalidraw", "both"], default="drawio")
    ap.add_argument("-o", "--output", help="출력 경로(확장자 제외)")
    args = ap.parse_args()
    spec = load_spec(args.spec)
    if args.output:
        stem = args.output
    elif args.spec.endswith(".spec.json"):
        stem = args.spec[:-len(".spec.json")]
    else:
        stem = os.path.splitext(args.spec)[0]
    if args.to in ("drawio", "both"):
        xml = to_drawio(spec)
        path = stem + ".drawio"
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"저장: {path}")
        print(f"편집 링크: {drawio_url(xml)}")
    if args.to in ("excalidraw", "both"):
        path = stem + ".excalidraw"
        with open(path, "w", encoding="utf-8") as f:
            f.write(to_excalidraw(spec))
        print(f"저장: {path}")


if __name__ == "__main__":
    main()
