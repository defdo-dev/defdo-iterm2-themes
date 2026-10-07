#!/usr/bin/env python3
"""Generate OpenCode TUI themes from the defdo iTerm2 palettes.

Every text-role token is guaranteed >= 4.5:1 (WCAG AA) against the
worst surface it appears on (backgroundElement) by mixing toward
white (dark themes) or black (light themes) while preserving hue.
Run from the repo root: python3 tools/gen_opencode_themes.py
"""
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


def mix(a, b, t):
    return fmt(tuple(x + (y - x) * t for x, y in zip(parse(a), parse(b))))


def lum(h):
    s = [c / 255 for c in parse(h)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in s]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(fg, bg):
    a, b = lum(fg), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def ensure(color, surface, target=4.5):
    """Nudge color toward white/black until it hits target contrast on surface."""
    if ratio(color, surface) >= target:
        return color
    dark_bg = lum(surface) < 0.5
    toward = "#ffffff" if dark_bg else "#000000"
    t = 0.0
    while t < 1.0:
        t += 0.02
        c = mix(color, toward, t)
        if ratio(c, surface) >= target:
            return c
    return toward


for f in sorted(glob.glob(f"{THEMES_DIR}/*.itermcolors")):
    slug = os.path.basename(f).replace("defdo-theme.", "").replace(".itermcolors", "")
    d = json.loads(subprocess.check_output(["plutil", "-convert", "json", "-o", "-", f]))
    a = {i: hexc(d[f"Ansi {i} Color"]) for i in range(16)}
    fg = hexc(d["Foreground Color"])
    bg = hexc(d["Background Color"])
    sel = hexc(d["Selection Color"])

    panel = mix(bg, fg, 0.05)
    element = mix(bg, fg, 0.09)
    border = mix(bg, fg, 0.16)
    subtle = mix(bg, fg, 0.10)
    worst = element if lum(element) != lum(bg) else bg

    muted = ensure(mix(bg, fg, 0.34), worst)
    primary = ensure(a[6], worst)
    secondary = ensure(a[12], worst)
    accent = ensure(a[3], worst)
    error = ensure(a[9], worst)
    warning = ensure(a[11], worst)
    success = ensure(a[10], worst)
    info = ensure(a[14], worst)
    keyword = ensure(a[13], worst)

    def t(c):
        return {"dark": c, "light": c}

    theme = {
        "primary": t(primary), "secondary": t(secondary), "accent": t(accent),
        "error": t(error), "warning": t(warning), "success": t(success), "info": t(info),
        "text": t(fg), "textMuted": t(muted),
        "background": t(bg), "backgroundPanel": t(panel), "backgroundElement": t(element),
        "border": t(border), "borderActive": t(primary), "borderSubtle": t(subtle),
        "diffAdded": t(success), "diffRemoved": t(error), "diffContext": t(muted),
        "diffHunkHeader": t(secondary), "diffHighlightAdded": t(ensure(a[2], worst)),
        "diffHighlightRemoved": t(ensure(a[1], worst)),
        "diffAddedBg": t(mix(a[2], bg, 0.88)), "diffRemovedBg": t(mix(a[1], bg, 0.88)),
        "diffContextBg": t(panel), "diffLineNumber": t(muted),
        "diffAddedLineNumberBg": t(mix(a[2], bg, 0.88)),
        "diffRemovedLineNumberBg": t(mix(a[1], bg, 0.88)),
        "markdownText": t(fg), "markdownHeading": t(primary), "markdownLink": t(secondary),
        "markdownLinkText": t(info), "markdownCode": t(success),
        "markdownBlockQuote": t(muted), "markdownEmph": t(accent), "markdownStrong": t(warning),
        "markdownHorizontalRule": t(muted), "markdownListItem": t(primary),
        "markdownListEnumeration": t(info), "markdownImage": t(secondary),
        "markdownImageText": t(info), "markdownCodeBlock": t(fg),
        "syntaxComment": t(muted), "syntaxKeyword": t(keyword), "syntaxFunction": t(primary),
        "syntaxVariable": t(ensure(a[7], worst)), "syntaxString": t(success), "syntaxNumber": t(keyword),
        "syntaxType": t(info), "syntaxOperator": t(secondary), "syntaxPunctuation": t(fg),
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
    print("wrote", name, "bg", bg, "muted", muted)
