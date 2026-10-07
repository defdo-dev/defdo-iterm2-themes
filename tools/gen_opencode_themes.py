#!/usr/bin/env python3
import subprocess, json, glob, os

THEMES_DIR = "themes"
OUT_DIR = "opencode"
INSTALL_DIR = os.path.expanduser("~/.config/opencode/themes")


def hexc(c):
    return "#%02x%02x%02x" % tuple(round(c[k] * 255) for k in
                                  ("Red Component", "Green Component", "Blue Component"))


def parse(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def fmt(rgb):
    return "#%02x%02x%02x" % tuple(round(v) for v in rgb)


def lighten(h, amt):
    a, b = parse(h), (238, 255, 255)
    return fmt(tuple(x + (y - x) * amt for x, y in zip(a, b)))


def darken(h, amt):
    a = parse(h)
    return fmt(tuple(x * (1 - amt) for x in a))


for f in sorted(glob.glob(f"{THEMES_DIR}/*.itermcolors")):
    slug = os.path.basename(f).replace("defdo-theme.", "").replace(".itermcolors", "")
    d = json.loads(subprocess.check_output(["plutil", "-convert", "json", "-o", "-", f]))
    a = {i: hexc(d[f"Ansi {i} Color"]) for i in range(16)}
    fg = hexc(d["Foreground Color"])
    bg = hexc(d["Background Color"])
    sel = hexc(d["Selection Color"])

    panel = lighten(bg, 0.05)
    element = lighten(bg, 0.09)
    border = lighten(bg, 0.16)
    subtle = lighten(bg, 0.10)
    muted = lighten(bg, 0.34)

    def t(c):
        return {"dark": c, "light": c}

    theme = {
        "primary": t(a[6]), "secondary": t(a[12]), "accent": t(a[3]),
        "error": t(a[9]), "warning": t(a[11]), "success": t(a[10]), "info": t(a[14]),
        "text": t(fg), "textMuted": t(muted),
        "background": t(bg), "backgroundPanel": t(panel), "backgroundElement": t(element),
        "border": t(border), "borderActive": t(a[6]), "borderSubtle": t(subtle),
        "diffAdded": t(a[10]), "diffRemoved": t(a[9]), "diffContext": t(muted),
        "diffHunkHeader": t(a[12]), "diffHighlightAdded": t(a[2]), "diffHighlightRemoved": t(a[1]),
        "diffAddedBg": t(lighten(a[2], 0.12)), "diffRemovedBg": t(lighten(a[1], 0.12)),
        "diffContextBg": t(panel), "diffLineNumber": t(muted),
        "diffAddedLineNumberBg": t(lighten(a[2], 0.12)),
        "diffRemovedLineNumberBg": t(lighten(a[1], 0.12)),
        "markdownText": t(fg), "markdownHeading": t(a[6]), "markdownLink": t(a[12]),
        "markdownLinkText": t(a[14]), "markdownCode": t(a[10]),
        "markdownBlockQuote": t(muted), "markdownEmph": t(a[3]), "markdownStrong": t(a[11]),
        "markdownHorizontalRule": t(muted), "markdownListItem": t(a[6]),
        "markdownListEnumeration": t(a[14]), "markdownImage": t(a[12]),
        "markdownImageText": t(a[14]), "markdownCodeBlock": t(fg),
        "syntaxComment": t(muted), "syntaxKeyword": t(a[13]), "syntaxFunction": t(a[6]),
        "syntaxVariable": t(a[7]), "syntaxString": t(a[10]), "syntaxNumber": t(a[13]),
        "syntaxType": t(a[14]), "syntaxOperator": t(a[12]), "syntaxPunctuation": t(a[7]),
    }

    doc = {"$schema": "https://opencode.ai/theme.json", "defs": {
        "defdo-cyan": a[6], "defdo-green": a[10], "defdo-yellow": a[3],
        "defdo-red": a[9], "defdo-purple": a[13], "defdo-blue": a[12],
        "defdo-bg": bg, "defdo-fg": fg, "defdo-selection": sel},
        "theme": theme}

    name = f"defdo-{slug}.json"
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(f"{OUT_DIR}/{name}", "w") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    os.makedirs(INSTALL_DIR, exist_ok=True)
    with open(f"{INSTALL_DIR}/{name}", "w") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    print("wrote", name, "bg", bg)
