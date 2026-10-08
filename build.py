"""Собирает сайт для GitHub Pages из konspekt.html: index.html, иконки, manifest."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)

body = (ROOT / "konspekt.html").read_text(encoding="utf-8")

HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Конспект">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#FFFFFF">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-512.png">
<link rel="manifest" href="manifest.json">
<style>
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);height:100%}
body{margin:0}
img{max-width:100%}
[hidden]{display:none!important}
</style>
"""

title_end = body.index("</title>") + len("</title>")
style_end = body.index("</style>") + len("</style>")
page = HEAD + body[:style_end] + "\n</head>\n<body>\n" + body[style_end:] + "\n</body>\n</html>\n"
(OUT / "index.html").write_text(page, encoding="utf-8")


def icon(size: int) -> Image.Image:
    k = size / 512
    im = Image.new("RGB", (size, size), "#2A54C6")
    d = ImageDraw.Draw(im)
    # лист бумаги в линейку
    d.rounded_rectangle([110 * k, 80 * k, 402 * k, 432 * k], radius=26 * k, fill="#FDFDF9")
    for y in range(170, 400, 44):
        d.line([140 * k, y * k, 372 * k, y * k], fill="#DAE3EE", width=max(1, round(5 * k)))
    d.line([172 * k, 100 * k, 172 * k, 412 * k], fill="#ECB6AC", width=max(1, round(5 * k)))
    # кнопка «плей» — метка времени
    d.polygon([(200 * k, 180 * k), (200 * k, 280 * k), (290 * k, 230 * k)], fill="#2A54C6")
    # рукописная линия
    pts = [((200 + i * 8) * k, (340 + (6 if i % 2 else -6)) * k) for i in range(20)]
    d.line(pts, fill="#C62828", width=max(2, round(10 * k)), joint="curve")
    return im


for s in (180, 192, 512):
    icon(s).save(OUT / f"icon-{s}.png")

(OUT / "manifest.json").write_text(json.dumps({
    "name": "Конспект",
    "short_name": "Конспект",
    "start_url": "./",
    "display": "standalone",
    "background_color": "#E8EBEE",
    "theme_color": "#FFFFFF",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
    ],
}, ensure_ascii=False, indent=2), encoding="utf-8")
print("ok:", sorted(p.name for p in OUT.iterdir()))
