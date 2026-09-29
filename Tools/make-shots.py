#!/usr/bin/env python3
"""Turns the raw simulator captures into App Store screenshots: caption on top, the app below.

    python3 Tools/make-shots.py [asc-locale ...]

Output: store/screenshots/<asc-locale>/<iphone-6.9|ipad-13>/<n>-<scene>.png
"""
import concurrent.futures, html, pathlib, subprocess, sys, tempfile, time
from captions import CAPTIONS
from locales import ASC, RTL, SCENES

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHOTS = ROOT / "store" / "screenshots"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DEVICES = {
    "iphone": dict(folder="iphone-6.9", w=1320, h=2868, font=112, top=170, shot_w=1090, shot_top=640, radius=118, pad=100, crop=0),
    "ipad": dict(folder="ipad-13", w=2064, h=2752, font=150, top=150, shot_w=1780, shot_top=520, radius=80, pad=160, crop=72),
}

def page(device: dict, raw: pathlib.Path, caption: str, rtl: bool) -> str:
    return f"""<!doctype html><html dir="{'rtl' if rtl else 'ltr'}"><meta charset=utf-8><style>
html,body{{margin:0;width:{device['w']}px;height:{device['h']}px;overflow:hidden;background:#0B0908}}
body{{position:relative;font-family:-apple-system,"SF Pro Display","Helvetica Neue",sans-serif;
  background:radial-gradient(120% 60% at 50% 0%,#4a2f1c 0%,#24170f 45%,#0B0908 100%)}}
h1{{position:absolute;left:{device['pad']}px;right:{device['pad']}px;top:{device['top']}px;margin:0;text-align:center;
  font-size:{device['font']}px;line-height:1.1;font-weight:800;letter-spacing:-0.02em;color:#FBEBD8;text-wrap:balance}}
.frame{{position:absolute;top:{device['shot_top']}px;left:50%;width:{device['shot_w']}px;transform:translateX(-50%);
  height:{device['h']}px;overflow:hidden;border-radius:{device['radius']}px;box-shadow:0 0 0 3px rgba(255,255,255,.14)}}
img{{display:block;width:100%;margin-top:-{device['crop'] * device['shot_w'] // device['w']}px}}
</style><h1>{html.escape(caption)}</h1><div class="frame"><img src="file://{raw}"></div></html>"""

def shoot(source: str, target: pathlib.Path, w: int, h: int):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.unlink(missing_ok=True)
    profile = tempfile.mkdtemp(prefix="umber-chrome-")
    chrome = subprocess.Popen([CHROME, "--headless=new", f"--user-data-dir={profile}", "--no-first-run", "--disable-gpu",
                               "--hide-scrollbars", "--force-device-scale-factor=1", f"--window-size={w},{h}",
                               f"--screenshot={target}", f"file://{f.name}"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(240):
            if target.exists() and target.stat().st_size > 0:
                time.sleep(0.6)
                return
            time.sleep(0.5)
        raise RuntimeError(f"Chrome never wrote {target}")
    finally:
        chrome.kill()

def job(asc: str, kind: str, index: int, scene: str):
    lang = ASC[asc]
    device = DEVICES[kind]
    raw = SHOTS / "raw" / kind / lang / f"{scene}.png"
    if not raw.exists():
        raise FileNotFoundError(raw)
    target = SHOTS / asc / device["folder"] / f"{index + 1}-{scene}.png"
    shoot(page(device, raw, CAPTIONS[lang][index], lang in RTL), target, device["w"], device["h"])
    return target

def main():
    wanted = sys.argv[1:] or list(ASC)
    jobs = [(asc, kind, i, scene) for asc in wanted for kind in DEVICES for i, scene in enumerate(SCENES)]
    with concurrent.futures.ThreadPoolExecutor(4) as pool:
        for n, target in enumerate(pool.map(lambda j: job(*j), jobs), 1):
            if n % 10 == 0:
                print(f"{n}/{len(jobs)}", flush=True)

main()
