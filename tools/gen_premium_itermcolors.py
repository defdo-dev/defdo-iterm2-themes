#!/usr/bin/env python3
"""Generate premium .itermcolors files from palette.json.

Free-tier .itermcolors files in themes/ are hand-canonical and untouched.
Premium variants (tier == "premium" in palette.json) are derived here so the
brand palettes stay regenerable. Run from the repo root.
"""
import json, plistlib, os

pal = json.load(open("palette.json"))
FG_DEFAULT = pal["foreground"]
ANSI_DEFAULT = pal["ansi"]


def comp(h):
    return {"Alpha Component": 1, "Color Space": "sRGB",
            "Red Component": int(h[1:3], 16) / 255,
            "Green Component": int(h[3:5], 16) / 255,
            "Blue Component": int(h[5:7], 16) / 255}


for slug, t in pal["themes"].items():
    if t.get("tier") != "premium":
        continue
    fg = t.get("foreground", FG_DEFAULT)
    ansi = t.get("ansi", ANSI_DEFAULT)
    cursor = t.get("cursor", t["accent"])
    d = {f"Ansi {i} Color": comp(ansi[str(i)]) for i in range(16)}
    d.update({
        "Background Color": comp(t["background"]),
        "Foreground Color": comp(fg),
        "Bold Color": comp(fg),
        "Cursor Color": comp(cursor),
        "Cursor Text Color": comp(t["background"]),
        "Selected Text Color": comp(t["background"]),
        "Selection Color": comp(t["selection"]),
        "Link Color": comp(t["accent"]),
    })
    out = f"themes/defdo-theme.{slug}.itermcolors"
    with open(out, "wb") as f:
        plistlib.dump(d, f, fmt=plistlib.FMT_XML)
    print("wrote", out)
