#!/usr/bin/env python3
"""Writes store/<locale>/*.txt for all 39 App Store Connect locales and checks every limit.

Run from anywhere:  python3 Tools/make-store.py
"""
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from locales import ASC
from listing_data import L, VARIANTS

LIMITS = dict(name=30, sub=30, kw=100, promo=170, description=4000)
FILES = dict(name="name.txt", sub="subtitle.txt", kw="keywords.txt", promo="promotional_text.txt", description="description.txt")
SOUNDS = "sound.brown sound.pink sound.white sound.green sound.fan sound.rain sound.ocean sound.wind sound.womb".split()

catalog = json.loads((ROOT / "Umber/Resources/Localizable.xcstrings").read_text())["strings"]

def sound_names(lang):
    return [catalog[k]["localizations"][lang]["stringUnit"]["value"] for k in SOUNDS]

def description(lang, d):
    lines = [d["hook"], "", d["label"] + ":", " · ".join(sound_names(lang)), ""]
    lines += ["• " + f for f in d["feats"]]
    lines += ["", "Connexa GmbH"]
    return "\n".join(lines)

def words(text):
    return re.findall(r"[\w]+", text.lower())

problems = []
def check(locale, field, value):
    if len(value) > LIMITS[field]:
        problems.append(f"{locale} {field}: {len(value)} > {LIMITS[field]}")
    if not value.strip():
        problems.append(f"{locale} {field}: empty")
    if value != value.strip() or "  " in value:
        problems.append(f"{locale} {field}: stray whitespace")

out = ROOT / "store"
count = 0
for locale, lang in ASC.items():
    d = dict(L[lang])
    d.update(VARIANTS.get(locale, {}))
    d["description"] = description(lang, d)
    folder = out / locale
    folder.mkdir(parents=True, exist_ok=True)
    for field, fname in FILES.items():
        check(locale, field, d[field])
        (folder / fname).write_text(d[field] + "\n")
    kw = d["kw"]
    if ", " in kw or kw.endswith(",") or kw.startswith(","):
        problems.append(f"{locale} kw: malformed separators")
    terms = kw.split(",")
    if len(terms) != len(set(terms)):
        problems.append(f"{locale} kw: repeated term")
    seen = set(words(d["name"])) | set(words(d["sub"]))
    for t in terms:
        for w in words(t):
            if w in seen and len(w) > 2:
                problems.append(f"{locale} kw: '{w}' already in name/subtitle")
    if re.search(r"\b(free|gratis|kostenlos|gratuit|grátis|gratuito|бесплатн|免费|無料|무료)\b", " ".join([d["name"], d["sub"], kw]).lower()):
        problems.append(f"{locale}: price word in name/subtitle/keywords")
    if "umber" in kw.lower():
        problems.append(f"{locale} kw: repeats the app name")
    count += 1

sheet = ["# Paste sheet", "", "One block per App Store Connect locale. Descriptions are in `store/<locale>/description.txt`.", ""]
for locale, lang in ASC.items():
    d = dict(L[lang]); d.update(VARIANTS.get(locale, {}))
    sheet += [f"## {locale}", "", f"- Name: `{d['name']}`", f"- Subtitle: `{d['sub']}`", f"- Keywords: `{d['kw']}`", f"- Promotional text: {d['promo']}", ""]
(out / "PASTE.md").write_text("\n".join(sheet))

if problems:
    print("\n".join(problems))
    sys.exit(1)
print(f"{count} locales written, every limit holds")
