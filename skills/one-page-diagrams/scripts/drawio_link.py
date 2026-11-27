#!/usr/bin/env python3
"""draw.io 편집 링크를 만든다. 표준 라이브러리만 사용.

사용법:
    python3 drawio_link.py 이름.drawio   -> XML을 담은 app.diagrams.net 링크
    python3 drawio_link.py 이름.mmd      -> Mermaid를 열 때 도형으로 바꿔 주는 링크

링크 형식은 jgraph/drawio-mcp(Apache-2.0)의 링크 생성 방식과 같다.
"""
import base64
import json
import sys
import urllib.parse
import zlib

EDITOR = "https://app.diagrams.net/"


def encode_uri_component(s):
    return urllib.parse.quote(s, safe="-_.!~*'()")


def deflate_raw_b64(text):
    comp = zlib.compressobj(9, zlib.DEFLATED, -15)
    data = comp.compress(encode_uri_component(text).encode("utf-8")) + comp.flush()
    return base64.b64encode(data).decode("ascii")


def drawio_url(xml):
    return EDITOR + "?grid=0&pv=0&border=10&edit=_blank#R" + encode_uri_component(deflate_raw_b64(xml))


def mermaid_url(code):
    create = {"type": "mermaid", "compressed": True, "data": deflate_raw_b64(code), "version": "12"}
    return EDITOR + "?pv=0&grid=0#create=" + encode_uri_component(json.dumps(create, separators=(",", ":")))


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if path.endswith((".mmd", ".mermaid")):
        print(mermaid_url(text))
    else:
        print(drawio_url(text))


if __name__ == "__main__":
    main()
