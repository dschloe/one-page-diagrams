#!/usr/bin/env python3
"""그림 파일을 PNG(기본 2배 해상도)로 바꾼다. 표준 라이브러리만 사용.

사용법:
    python3 to_png.py 파일 [-o 출력.png] [--scale 2]

지원: .svg, .html, .drawio, .excalidraw
필요: PC에 설치된 Chrome, Edge 또는 Chromium (Windows에는 Edge가 기본 설치되어 있음).
      .html(인포그래픽), .drawio, .excalidraw는 그릴 때 인터넷 연결이 필요하다.
브라우저를 찾지 못하면 Playwright(설치된 경우)를 쓰고, 그것도 없으면 대안을 출력하고 종료 코드 3으로 끝난다.

환경 변수(선택):
    CHROME_PATH                  브라우저 실행 파일 경로 직접 지정
    ONEPAGE_DRAWIO_VIEWER_JS     draw.io 뷰어 스크립트 주소 (기본: viewer.diagrams.net)
    ONEPAGE_EXCALIDRAW_ESM       Excalidraw ESM 모듈 주소 (기본: esm.sh)
"""
import argparse
import html
import json
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import tempfile

DRAWIO_VIEWER = os.environ.get("ONEPAGE_DRAWIO_VIEWER_JS", "https://viewer.diagrams.net/js/viewer-static.min.js")
EXCALIDRAW_ESM = os.environ.get("ONEPAGE_EXCALIDRAW_ESM", "https://esm.sh/@excalidraw/excalidraw@0.18.1?bundle")
PAD = 24

FALLBACK = {
    ".svg": "브라우저로 SVG를 열어 캡처하거나, PowerPoint·Word에 SVG를 그대로 삽입하세요.",
    ".html": "HTML을 브라우저로 열고 오른쪽 위 'PNG로 저장' 버튼을 누르세요.",
    ".drawio": "https://app.diagrams.net 에서 파일을 열고 파일 → 내보내기 → PNG를 선택하세요.",
    ".excalidraw": "https://excalidraw.com 에서 파일을 열고 메뉴 → 이미지 내보내기 → PNG를 선택하세요.",
}

# 페이지에 넣는 측정 스크립트: 그림이 다 그려지면 그 영역의 오른쪽 아래 좌표를 <meta>에 적는다.
PROBE = """
<script>
(function () {
  document.documentElement.classList.add('capture');
  var SEL = ['#capture', '#container > svg', '#container > *', '.mxgraph svg', '#out svg'];
  var tries = 0;
  function ready() {
    if (document.getElementById('container') && !document.body.hasAttribute('data-rendered') && tries < 80) return null;
    for (var i = 0; i < SEL.length; i++) {
      var el = document.querySelector(SEL[i]);
      if (el) { var r = el.getBoundingClientRect(); if (r.width > 20 && r.height > 20) return r; }
    }
    return tries > 80 ? document.body.getBoundingClientRect() : null;
  }
  function tick() {
    tries++;
    var r = ready();
    if (!r) { setTimeout(tick, 250); return; }
    setTimeout(function () {
      r = ready() || r;
      var m = document.createElement('meta');
      m.name = 'onepage-bounds';
      m.content = [Math.ceil(r.right + window.scrollX), Math.ceil(r.bottom + window.scrollY)].join(',');
      document.head.appendChild(m);
    }, 800);
  }
  if (document.readyState === 'complete') tick(); else window.addEventListener('load', tick);
})();
</script>
"""


# ------------------------------------------------------------------ browser

def find_browser():
    env = os.environ.get("CHROME_PATH")
    if env and os.path.exists(env):
        return env
    cands = []
    system = platform.system()
    if system == "Windows":
        for base in filter(None, [os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"),
                                  os.environ.get("LOCALAPPDATA")]):
            cands += [os.path.join(base, "Google", "Chrome", "Application", "chrome.exe"),
                      os.path.join(base, "Microsoft", "Edge", "Application", "msedge.exe")]
    elif system == "Darwin":
        for app in ["Google Chrome", "Microsoft Edge", "Chromium", "Brave Browser"]:
            for root in ["/Applications", os.path.expanduser("~/Applications")]:
                cands.append(f"{root}/{app}.app/Contents/MacOS/{app}")
    for name in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
                 "microsoft-edge", "microsoft-edge-stable", "chrome", "msedge"]:
        p = shutil.which(name)
        if p:
            cands.append(p)
    cands += ["/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
              "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"]
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


def to_uri(path, browser):
    p = os.path.abspath(path)
    if browser and browser.startswith("/mnt/") and browser.endswith(".exe"):
        try:
            win = subprocess.check_output(["wslpath", "-w", p], text=True).strip()
            return "file:///" + win.replace("\\", "/")
        except (OSError, subprocess.CalledProcessError):
            pass
    return pathlib.Path(p).as_uri()


def run_browser(browser, extra, page, width, height, wait_ms):
    with tempfile.TemporaryDirectory() as prof:
        args = [browser, "--headless=new", f"--user-data-dir={prof}", "--disable-gpu", "--hide-scrollbars",
                "--no-first-run", "--no-default-browser-check", "--allow-file-access-from-files",
                f"--window-size={width},{height}", f"--virtual-time-budget={wait_ms}"]
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            args.append("--no-sandbox")
        args += extra + [to_uri(page, browser)]
        return subprocess.run(args, capture_output=True, timeout=240, text=True, encoding="utf-8", errors="replace")


def shoot_cli(browser, page, out, width, height, scale, wait_ms, measure):
    if measure:
        r = run_browser(browser, [f"--force-device-scale-factor={scale}", "--dump-dom"], page, width, height, wait_ms)
        m = re.search(r'name="onepage-bounds" content="(\d+),(\d+)"', r.stdout or "")
        if m:
            width, height = int(m.group(1)) + PAD, int(m.group(2)) + PAD
    if os.path.exists(out):
        os.remove(out)
    r = run_browser(browser, [f"--force-device-scale-factor={scale}", f"--screenshot={out}"],
                    page, width, height, wait_ms)
    return os.path.exists(out) and os.path.getsize(out) > 0, (r.stderr or "")[-600:]


def shoot_playwright(page, out, width, height, scale, wait_ms, measure):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False, "playwright 없음"
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": width, "height": height}, device_scale_factor=scale)
            pg.goto(pathlib.Path(os.path.abspath(page)).as_uri())
            if measure:
                pg.wait_for_selector('meta[name="onepage-bounds"]', state="attached", timeout=wait_ms + 15000)
                w, h = map(int, pg.get_attribute('meta[name="onepage-bounds"]', "content").split(","))
                pg.set_viewport_size({"width": w + PAD, "height": h + PAD})
            else:
                pg.wait_for_timeout(1000)
            pg.screenshot(path=out)
            b.close()
        return True, ""
    except Exception as e:  # noqa: BLE001
        return False, str(e)


# --------------------------------------------------------------- 페이지 준비

def svg_size(text):
    m = re.search(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', text)
    return (int(float(m.group(1))), int(float(m.group(2)))) if m else (1200, 800)


def prepare(src, tmpdir, scale=2):
    """(브라우저로 열 페이지, 창 폭, 창 높이, 대기 ms, 크기 측정 여부)"""
    ext = os.path.splitext(src)[1].lower()
    text = open(src, encoding="utf-8").read()
    page = os.path.join(tmpdir, "page.html")
    head = '<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#fff}'
    if ext == ".svg":
        w, h = svg_size(text)
        text = re.sub(r"<\?xml[^>]*\?>", "", text)
        doc = f'{head}svg{{display:block;width:{w}px;height:{h}px}}</style></head><body>{text}</body></html>'
        open(page, "w", encoding="utf-8").write(doc)
        return page, w, h, 3000, False
    if ext in (".html", ".htm"):
        # 상대 경로 자원이 깨지지 않게 원본과 같은 폴더에 측정용 사본을 둔다.
        page = os.path.join(os.path.dirname(os.path.abspath(src)), ".onepage-capture.html")
        doc = text.replace("</body>", PROBE + "</body>") if "</body>" in text else text + PROBE
        open(page, "w", encoding="utf-8").write(doc)
        return page, 1320, 2400, 20000, True
    if ext == ".drawio":
        cfg = json.dumps({"xml": text, "lightbox": False, "nav": False, "toolbar": "", "border": 10,
                          "resize": True, "highlight": "none"}, ensure_ascii=False)
        doc = (f'{head}.mxgraph{{display:inline-block;padding:16px}}</style></head><body>'
               f'<div class="mxgraph" data-mxgraph="{html.escape(cfg)}"></div>'
               f'<script src="{DRAWIO_VIEWER}"></script>{PROBE}</body></html>')
        open(page, "w", encoding="utf-8").write(doc)
        return page, 2400, 2000, 25000, True
    if ext == ".excalidraw":
        scene = json.loads(text)
        doc = (f'{head}#out svg{{display:block}}</style></head><body><div id="out"></div>'
               f'<script type="module">import {{ exportToSvg }} from "{EXCALIDRAW_ESM}";\n'
               f'const scene = {json.dumps(scene, ensure_ascii=False)};\n'
               'const svg = await exportToSvg({ elements: scene.elements, files: scene.files || {}, '
               'appState: Object.assign({}, scene.appState || {}, { exportBackground: true, exportPadding: 24, exportScale: ' + str(scale) + ' }) });\n'
               'document.getElementById("out").appendChild(svg);\n'
               f'</script>{PROBE}</body></html>')
        open(page, "w", encoding="utf-8").write(doc)
        return page, 2400, 2000, 25000, True
    raise SystemExit(f"지원하지 않는 형식: {ext}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("-o", "--output")
    ap.add_argument("--scale", type=int, default=2)
    args = ap.parse_args()
    ext = os.path.splitext(args.src)[1].lower()
    out = os.path.abspath(args.output or os.path.splitext(args.src)[0] + ".png")
    ok, err = False, "Chrome/Edge를 찾지 못했습니다."
    with tempfile.TemporaryDirectory() as tmp:
        page, w, h, wait, measure = prepare(args.src, tmp, args.scale)
        # Excalidraw는 exportScale로 이미 확대하므로 화면 배율은 1로 둔다.
        scale = 1 if ext == ".excalidraw" else args.scale
        try:
            browser = find_browser()
            if browser:
                ok, err = shoot_cli(browser, page, out, w, h, scale, wait, measure)
            if not ok:
                ok, err2 = shoot_playwright(page, out, w, h, scale, wait, measure)
                if not ok:
                    err = f"{err} {err2}".strip()
        finally:
            if page.endswith(".onepage-capture.html") and os.path.exists(page):
                os.remove(page)
    if not ok:
        last = err.strip().splitlines()[-1] if err.strip() else ""
        print("PNG를 만들지 못했습니다. " + last)
        print("대안: " + FALLBACK.get(ext, ""))
        sys.exit(3)
    print(f"저장: {out}")


if __name__ == "__main__":
    main()
