# architecture HTML 틀

아래 HTML을 `.html` 파일로 옮겨 적는다. `{{TITLE}}`, `{{SUBTITLE}}`, `{{SVG_BODY}}`, `{{CARDS}}`, `{{FOOTER}}`만 바꾼다. 나머지는 그대로 둔다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Pretendard', 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', 'Noto Sans CJK KR', sans-serif;
    background: #ffffff; color: #0f172a; padding: 32px;
  }
  #capture { width: 1200px; margin: 0 auto; background: #ffffff; padding: 8px; }
  .head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
  h1 { font-size: 26px; font-weight: 700; }
  .sub { color: #475569; font-size: 15px; margin-top: 6px; }
  .btn { font: inherit; font-size: 13px; padding: 6px 12px; border: 1px solid #cbd5e1; border-radius: 6px; background: #f8fafc; cursor: pointer; }
  .frame { border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; }
  #diagram { display: block; width: 100%; height: auto; }
  .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 16px; }
  .card { border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 16px; }
  .card h3 { font-size: 15px; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
  .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
  .card li { font-size: 13px; color: #475569; margin-left: 16px; margin-bottom: 4px; }
  .foot { color: #94a3b8; font-size: 12px; margin-top: 12px; text-align: right; }
  @media print { .btn { display: none; } }
  .capture .btn { display: none; }
  .capture body { padding: 16px; } .capture #capture { margin: 0; }
</style>
</head>
<body>
<div id="capture">
  <div class="head">
    <div>
      <h1>{{TITLE}}</h1>
      <p class="sub">{{SUBTITLE}}</p>
    </div>
    <button class="btn" onclick="savePng()">PNG로 저장</button>
  </div>

  <div class="frame">
    <svg id="diagram" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1160 620">
      <style>text { font-family: 'Pretendard','Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR','Noto Sans CJK KR',sans-serif; }</style>
      <defs>
        <marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
          <polygon points="0 0, 10 4, 0 8" fill="#475569"/>
        </marker>
      </defs>
      <rect width="1160" height="620" fill="#ffffff"/>
      {{SVG_BODY}}
    </svg>
  </div>

  <div class="cards">
    {{CARDS}}
  </div>
  <p class="foot">{{FOOTER}}</p>
</div>

<script>
function savePng() {
  var svg = document.getElementById('diagram');
  var vb = svg.viewBox.baseVal;
  var scale = 2;
  var xml = new XMLSerializer().serializeToString(svg);
  var img = new Image();
  img.onload = function () {
    var c = document.createElement('canvas');
    c.width = vb.width * scale; c.height = vb.height * scale;
    var ctx = c.getContext('2d');
    ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, c.width, c.height);
    ctx.drawImage(img, 0, 0, c.width, c.height);
    var a = document.createElement('a');
    a.download = (document.title || 'diagram') + '.png';
    a.href = c.toDataURL('image/png');
    a.click();
  };
  img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(xml);
}
</script>
</body>
</html>
```
