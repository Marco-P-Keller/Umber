#!/usr/bin/env python3
"""Photographs the app in every language on the iPhone and iPad simulators.

    python3 Tools/capture-screens.py iphone|ipad [lang ...]

Needs a Debug simulator build in /tmp/umber-dd. Raw captures go to store/screenshots/raw/<device>/<lang>/<scene>.png.
"""
import pathlib, subprocess, sys, time
from locales import APP_LANGUAGES, IPAD, IPHONE, SCENES

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = "/tmp/umber-dd/Build/Products/Debug-iphonesimulator/Umber.app"
BUNDLE = "com.connexa.umber"

def sh(*args, check=True):
    return subprocess.run(args, check=check, capture_output=True, text=True)

def main():
    device_name = sys.argv[1]
    udid = {"iphone": IPHONE, "ipad": IPAD}[device_name]
    languages = sys.argv[2:] or APP_LANGUAGES
    sh("xcrun", "simctl", "boot", udid, check=False)
    sh("xcrun", "simctl", "bootstatus", udid, "-b")
    sh("xcrun", "simctl", "install", udid, APP)
    sh("xcrun", "simctl", "status_bar", udid, "override", "--time", "9:41", "--batteryState", "charged",
       "--batteryLevel", "100", "--cellularBars", "4", "--wifiBars", "3", "--operatorName", "")
    for lang in languages:
        folder = ROOT / "store" / "screenshots" / "raw" / device_name / lang
        folder.mkdir(parents=True, exist_ok=True)
        for scene in SCENES:
            sh("xcrun", "simctl", "terminate", udid, BUNDLE, check=False)
            sh("xcrun", "simctl", "launch", udid, BUNDLE, "-AppleLanguages", f"({lang})", "-AppleLocale", lang.replace("-", "_"),
               "-UmberSilent", "-UmberScene", scene)
            time.sleep(3.2)
            sh("xcrun", "simctl", "io", udid, "screenshot", str(folder / f"{scene}.png"))
        print(device_name, lang, flush=True)

main()
