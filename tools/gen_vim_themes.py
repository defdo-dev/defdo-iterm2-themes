#!/usr/bin/env python3
"""Generate vim/Neovim colorschemes from palette.json.

Emits vim/defdo_<slug>.vim — plain vimscript, loads in both vim
(~/.vim/colors/) and Neovim (~/.config/nvim/colors/). GUI (guifg) and
256-color terminal (cterm) values are both set; terminal color palette
is exported via g:terminal_color_* for nvim's :terminal.

Run from the repo root: python3 tools/gen_vim_themes.py
"""
import json, os

pal = json.load(open("palette.json"))
ANSI = pal["ansi"]
FG = pal["foreground"]

SYNTAX = {
    "dark": {
        "comment": "#546e7a", "keyword": "#bfa6f1", "function": "#0291f7",
        "string": "#a6c27b", "number": "#f78c6c", "type": "#f9bc02",
        "variable": "#eeffff", "punctuation": "#89c6df", "tag": "#f07178",
        "constant": "#f78c6c", "error": "#fd4d6a",
    },
    "light": {
        "comment": "#6b7a80", "keyword": "#7a4fd0", "function": "#0055b8",
        "string": "#0a7a4f", "number": "#b3541e", "type": "#9c7a02",
        "variable": "#16181d", "punctuation": "#3e7e9b", "tag": "#d3405a",
        "constant": "#b3541e", "error": "#c62828",
    },
}


def parse(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def mix(a, b, t):
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(parse(a), parse(b)))


def xterm256(h):
    """Nearest xterm 256 color index for a hex color."""
    r, g, b = parse(h)
    best, idx = None, 16
    for i in range(16, 256):
        if i < 232:
            j = i - 16
            rr, gg, bb = (j // 36, (j // 6) % 6, j % 6)
            pr, pg, pb = [0 if v == 0 else 55 + v * 40 for v in (rr, gg, bb)]
        else:
            v = 8 + (i - 232) * 10
            pr = pg = pb = v
        d = (pr - r) ** 2 + (pg - g) ** 2 + (pb - b) ** 2
        if best is None or d < best:
            best, idx = d, i
    return idx


def hl(group, fg_c=None, bg_c=None, style=None):
    parts = [f"hi! {group}"]
    if fg_c:
        parts.append(f"guifg={fg_c}")
        parts.append(f"ctermfg={xterm256(fg_c)}")
    else:
        parts.append("guifg=NONE ctermfg=NONE")
    if bg_c:
        parts.append(f"guibg={bg_c}")
        parts.append(f"ctermbg={xterm256(bg_c)}")
    else:
        parts.append("guibg=NONE ctermbg=NONE")
    if style:
        parts.append(f"gui={style}")
        parts.append(f"cterm={style}")
    return " ".join(parts)


def colorscheme(slug, t):
    fg = t.get("foreground", FG)
    ansi = t.get("ansi", ANSI)
    bg = t["background"]
    appear = t.get("appearance", "dark")
    sx = SYNTAX[appear]
    accent = t["accent"]
    sel = t["selection"]
    line = mix(bg, fg, 0.06)
    panel = mix(bg, fg, 0.04)
    gutter = mix(bg, fg, 0.02)
    ln = mix(bg, fg, 0.30)
    cursor = t.get("cursor", accent)

    L = [
        f'" defdo {slug} — generated from palette.json (defdo theme family)',
        '" vim: use in ~/.vim/colors/  ·  nvim: use in ~/.config/nvim/colors/',
        'set background=' + ("light" if appear == "light" else "dark"),
        "hi clear",
        "if exists('syntax_on')",
        "  syntax reset",
        "endif",
        f'let g:colors_name = "defdo_{slug.replace("-", "_")}"',
        "",
        "let s:ansi = " + json.dumps(ansi),
        "for s:i in range(16)",
        f"  execute 'let g:terminal_' . s:i . '_color = \"' + s:ansi[string(s:i)] + '\"'",
        "endfor",
        f'let g:terminal_ansi_colors = map(range(16), {{i -> s:ansi[string(i)]}})',
        "",
        hl("Normal", fg, bg),
        hl("NonText", ln, None),
        hl("EndOfBuffer", ln, None),
        hl("LineNr", ln, gutter),
        hl("CursorLineNr", accent, gutter, "bold"),
        hl("CursorLine", None, line),
        hl("ColorColumn", None, line),
        hl("Visual", None, sel),
        hl("MatchParen", bg, accent, "bold"),
        hl("StatusLine", fg, panel),
        hl("StatusLineNC", ln, gutter),
        hl("WinSeparator", ln, None),
        hl("VertSplit", ln, gutter),
        hl("Directory", accent, None, "bold"),
        hl("Search", bg, accent),
        hl("IncSearch", bg, sx["string"]),
        hl("Cursor", None, None, "reverse"),
        hl("lCursor", None, None, "reverse"),
        "",
        hl("Comment", sx["comment"], None, "italic"),
        hl("Todo", sx["constant"], None, "bold,italic"),
        hl("Constant", sx["constant"]),
        hl("String", sx["string"]),
        hl("Character", sx["string"]),
        hl("Number", sx["number"]),
        hl("Boolean", sx["number"]),
        hl("Float", sx["number"]),
        hl("Identifier", sx["variable"]),
        hl("Function", sx["function"]),
        hl("Statement", sx["keyword"]),
        hl("Keyword", sx["keyword"]),
        hl("Conditional", sx["keyword"]),
        hl("Repeat", sx["keyword"]),
        hl("Label", sx["keyword"]),
        hl("Operator", sx["punctuation"]),
        hl("Exception", sx["keyword"]),
        hl("PreProc", sx["tag"]),
        hl("Include", sx["keyword"]),
        hl("Define", sx["tag"]),
        hl("Macro", sx["tag"]),
        hl("Type", sx["type"]),
        hl("StorageClass", sx["keyword"]),
        hl("Structure", sx["type"]),
        hl("Typedef", sx["type"]),
        hl("Special", sx["type"]),
        hl("SpecialComment", sx["comment"], None, "italic"),
        hl("Delimiter", sx["punctuation"]),
        hl("SpecialKey", sx["punctuation"]),
        hl("Tag", sx["type"]),
        hl("Error", sx["error"], mix(sx["error"], bg, 0.85)),
        "",
        hl("DiffAdd", sx["string"], mix(sx["string"], bg, 0.88)),
        hl("DiffChange", sx["type"], mix(sx["type"], bg, 0.88)),
        hl("DiffDelete", sx["error"], mix(sx["error"], bg, 0.88)),
        hl("DiffText", sx["function"], mix(sx["function"], bg, 0.85)),
        "",
        hl("Pmenu", fg, panel),
        hl("PmenuSel", bg, accent),
        hl("PmenuSbar", None, gutter),
        hl("PmenuThumb", None, ln),
        hl("TabLine", ln, gutter),
        hl("TabLineSel", fg, panel, "bold"),
        hl("TabLineFill", None, gutter),
        hl("Folded", ln, panel),
        hl("FoldColumn", ln, gutter),
        hl("SignColumn", ln, gutter),
        "",
    ]
    return "\n".join(L) + "\n"


def main():
    os.makedirs("vim", exist_ok=True)
    for slug, t in pal["themes"].items():
        out = f"vim/defdo_{slug.replace('-', '_')}.vim"
        with open(out, "w") as f:
            f.write(colorscheme(slug, t))
        print("wrote", out)


if __name__ == "__main__":
    main()
