#!/usr/bin/env python3
"""Draws the app icon (standard, dark, tinted) as HTML and photographs it with headless Chrome."""
import pathlib, subprocess, tempfile, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "Umber" / "Resources" / "Assets.xcassets" / "AppIcon.appiconset"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# The brown-noise spectrum, low to high: what the app's first tile draws.
BARS = [1.0, 0.70, 0.46, 0.28, 0.17, 0.10, 0.06]

def page(background: str, fill: str, glow: str) -> str:
    width, gap, tallest = 72, 42, 640
    total = len(BARS) * width + (len(BARS) - 1) * gap
    x0 = (1024 - total) / 2
    bars = ""
    for i, h in enumerate(BARS):
        height = max(tallest * h, width)
        bars += f'<rect x="{x0 + i * (width + gap):.1f}" y="{(1024 - height) / 2:.1f}" width="{width}" height="{height:.1f}" rx="{width / 2}" fill="url(#bar)"/>'
    return f"""<!doctype html><meta charset=utf-8><style>html,body{{margin:0;background:#000}}svg{{display:block}}</style>
<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
<defs>{background}{fill}{glow}</defs>
<rect width="1024" height="1024" fill="url(#bg)"/>
<rect width="1024" height="1024" fill="url(#glow)"/>
{bars}
</svg>"""

STANDARD = page(
    '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2B1C12"/><stop offset="1" stop-color="#0B0908"/></linearGradient>',
    '<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6BE7E"/><stop offset="1" stop-color="#D68A45"/></linearGradient>',
    '<radialGradient id="glow" cx="0.3" cy="0.5" r="0.6"><stop offset="0" stop-color="#E8A25B" stop-opacity="0.22"/><stop offset="1" stop-color="#E8A25B" stop-opacity="0"/></radialGradient>')
DARK = page(
    '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#120D09"/><stop offset="1" stop-color="#060505"/></linearGradient>',
    '<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0B574"/><stop offset="1" stop-color="#C77C3A"/></linearGradient>',
    '<radialGradient id="glow" cx="0.3" cy="0.5" r="0.6"><stop offset="0" stop-color="#E8A25B" stop-opacity="0.12"/><stop offset="1" stop-color="#E8A25B" stop-opacity="0"/></radialGradient>')
TINTED = page(
    '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#000"/></linearGradient>',
    '<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#BDBDBD"/></linearGradient>',
    '<radialGradient id="glow" cx="0.3" cy="0.5" r="0.6"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')

def shoot(html: str, name: str):
    """Chrome writes the screenshot and then sometimes never exits, so wait for the file, not the process."""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
    target = OUT / name
    target.unlink(missing_ok=True)
    profile = tempfile.mkdtemp(prefix="umber-chrome-")
    chrome = subprocess.Popen([CHROME, "--headless=new", f"--user-data-dir={profile}", "--no-first-run", "--disable-gpu",
                               "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1024,1024",
                               f"--screenshot={target}", f"file://{f.name}"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(120):
            if target.exists() and target.stat().st_size > 0:
                time.sleep(0.5)
                return
            time.sleep(0.5)
        raise RuntimeError(f"Chrome never wrote {name}")
    finally:
        chrome.kill()

shoot(STANDARD, "icon-any.png")
shoot(DARK, "icon-dark.png")
shoot(TINTED, "icon-tinted.png")
(OUT / "Contents.json").write_text("""{
  "images" : [
    { "filename" : "icon-any.png", "idiom" : "universal", "platform" : "ios", "size" : "1024x1024" },
    { "appearances" : [ { "appearance" : "luminosity", "value" : "dark" } ], "filename" : "icon-dark.png", "idiom" : "universal", "platform" : "ios", "size" : "1024x1024" },
    { "appearances" : [ { "appearance" : "luminosity", "value" : "tinted" } ], "filename" : "icon-tinted.png", "idiom" : "universal", "platform" : "ios", "size" : "1024x1024" }
  ],
  "info" : { "author" : "xcode", "version" : 1 }
}
""")
print("icons written to", OUT.relative_to(ROOT))
