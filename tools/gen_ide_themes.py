#!/usr/bin/env python3
"""Generate IDE themes from palette.json: JetBrains (Android Studio), Arduino IDE 2, Xcode.

All free defdo variants are emitted into:
  jetbrains/defdo-<slug>.theme        -> Settings > Editor > Color Scheme > gear > Import Scheme
  arduino/defdo-<slug>.settings.json  -> paste into Arduino IDE 2 settings.json (File > Preferences)
  xcode/defdo-<slug>.xccolortheme     -> drop into ~/Library/Developer/Xcode/UserData/FontAndColorThemes/

Run from the repo root: python3 tools/gen_ide_themes.py
"""
import json, os, plistlib
from xml.sax.saxutils import escape

pal = json.load(open("palette.json"))
ANSI = pal["ansi"]
FG = pal["foreground"]

# Syntax palette per appearance (mirrors the VS Code tokenColors of the family)
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


def lighten(h, amt, toward):
    a, b = parse(h), parse(toward)
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * amt) for x, y in zip(a, b))


def themes():
    for slug, t in pal["themes"].items():
        fg = t.get("foreground", FG)
        ansi = t.get("ansi", ANSI)
        appear = t.get("appearance", "dark")
        yield slug, t, fg, ansi, appear


# ---------------------------------------------------------------- JetBrains
def jetbrains(slug, t, fg, ansi, appear):
    bg = t["background"][1:]
    sx = SYNTAX[appear]
    sel = t["selection"]
    caret = t.get("cursor", t["accent"])
    line = lighten(t["background"], 0.06, fg)[1:]
    gutter = bg
    ln = lighten(t["background"], 0.30, fg)[1:]
    guide = lighten(t["background"], 0.18, fg)[1:]

    def c(name, value):
        return f'    <option name="{name}" value="{value}"/>'

    def attr(name, color, bold=False, italic=False):
        ft = 1 if bold else 0
        if italic:
            ft |= 2
        opts = f'<option name="FOREGROUND" value="{color[1:]}"/>'
        if ft:
            opts += f'<option name="FONT_TYPE" value="{ft}"/>'
        return f'    <option name="{name}">\n      <value>\n        {opts}\n      </value>\n    </option>'

    colors = "\n".join([
        c("BACKGROUND", bg), c("CARET_COLOR", caret[1:]), c("CARET_ROW_COLOR", line),
        c("SELECTION_BACKGROUND", sel[1:]), c("SELECTION_FOREGROUND", ""),
        c("GUTTER_BACKGROUND", gutter), c("LINE_NUMBERS_COLOR", ln),
        c("FOLDING_LINES_COLOR", guide), c("INDENT_GUIDE", guide),
        c("SELECTED_INDENT_GUIDE", sel[1:]), c("WHITESPACES", guide),
        c("METHOD_SEPARATORS_COLOR", guide),
        c("ADDED_LINES_COLOR", ansi["2"][1:]), c("MODIFIED_LINES_COLOR", ansi["3"][1:]),
        c("DELETED_LINES_COLOR", ansi["1"][1:]),
        c("TELEPATHY_COLOR", ansi["6"][1:]),
        c("HYPERLINK_COLOR", sx["function"][1:]),
        c("FOLLOWED_HYPERLINK_COLOR", sx["punctuation"][1:]),
    ])
    attrs = "\n".join([
        attr("TEXT", fg), attr("FOLLOWED_HYPERLINK_ATTRIBUTES", sx["function"][1:], italic=True),
        attr("KEYWORD", sx["keyword"]), attr("CONTROL_FLOW_KEYWORD", sx["keyword"], bold=True),
        attr("STRING", sx["string"]), attr("CHARACTER", sx["string"]),
        attr("ESCAPE_CHARACTER", sx["constant"]),
        attr("NUMBER", sx["number"]), attr("CONSTANT", sx["constant"]),
        attr("STATIC_FINAL_FIELD", sx["constant"]),
        attr("FUNCTION_DECLARATION", sx["function"]), attr("FUNCTION_CALL", sx["function"]),
        attr("GLOBAL_FUNCTION", sx["function"]),
        attr("CLASS_NAME", sx["type"]), attr("INTERFACE_NAME", sx["type"]),
        attr("ABSTRACT_CLASS_NAME_ATTRIBUTES", sx["type"], italic=True),
        attr("ANNOTATION_NAME_ATTRIBUTES", sx["type"], italic=True),
        attr("DOC_COMMENT", sx["comment"], italic=True), attr("COMMENT", sx["comment"], italic=True),
        attr("BLOCK_COMMENT", sx["comment"], italic=True), attr("LINE_COMMENT", sx["comment"], italic=True),
        attr("OPERATOR", sx["punctuation"]), attr("PARENTHETS", sx["punctuation"]),
        attr("BRACKETS", sx["punctuation"]), attr("BRACES", sx["punctuation"]),
        attr("COMMA", sx["punctuation"]), attr("SEMICOLON", sx["punctuation"]),
        attr("DOT", sx["punctuation"]),
        attr("GLOBAL_VARIABLE", sx["variable"]), attr("LOCAL_VARIABLE", sx["variable"]),
        attr("PARAMETER", sx["variable"]),
        attr("TAG_NAME", sx["tag"]), attr("ATTRIBUTE_NAME", sx["type"]),
    ])
    parent = "Default" if appear == "light" else "Darcula"
    return f'''<scheme name="defdo {slug}" version="142" parent_scheme="{parent}">
  <meta>
    <property name="author" value="defdo"/>
  </meta>
  <colors>
{colors}
  </colors>
  <attributes>
{attrs}
  </attributes>
</scheme>
'''


# ------------------------------------------------------------------ Arduino
def arduino(slug, t, fg, ansi, appear):
    sx = SYNTAX[appear]
    colors = {
        "editor.background": t["background"],
        "editor.foreground": fg,
        "editorLineNumber.foreground": lighten(t["background"], 0.30, fg),
        "editorLineNumber.activeForeground": t["accent"],
        "editor.selectionBackground": t["selection"] + "80",
        "editor.lineHighlightBackground": lighten(t["background"], 0.06, fg),
        "editorCursor.foreground": t.get("cursor", t["accent"]),
        "editorIndentGuide.background1": lighten(t["background"], 0.18, fg),
        "activityBar.background": t["background"],
        "sideBar.background": lighten(t["background"], 0.03, fg),
        "editorGroupHeader.tabsBackground": t["background"],
        "statusBar.background": t["background"],
        "statusBar.foreground": t["accent"],
        "tab.activeBorderTop": t["accent"],
        "list.activeSelectionBackground": t["selection"] + "40",
        "terminal.background": t["background"],
        "terminal.foreground": fg,
        "terminal.selectionBackground": t["selection"] + "80",
        "terminalCursor.foreground": t.get("cursor", t["accent"]),
    }
    for i in range(8):
        colors[f"terminal.ansi{['Black','Red','Green','Yellow','Blue','Magenta','Cyan','White'][i]}"] = ansi[str(i)]
        colors[f"terminal.ansiBright{['Black','Red','Green','Yellow','Blue','Magenta','Cyan','White'][i]}"] = ansi[str(i + 8)]
    rules = [
        ("Comment", ["comment"], sx["comment"], "italic"),
        ("Keyword", ["keyword"], sx["keyword"], None),
        ("String", ["string"], sx["string"], None),
        ("Number", ["constant.numeric"], sx["number"], None),
        ("Function", ["entity.name.function", "support.function"], sx["function"], None),
        ("Type", ["entity.name.type", "support.type", "entity.name.class"], sx["type"], None),
        ("Variable", ["variable"], sx["variable"], None),
        ("Punctuation", ["punctuation"], sx["punctuation"], None),
        ("Tag", ["entity.name.tag"], sx["tag"], None),
        ("Error", ["invalid"], sx["error"], None),
    ]
    return json.dumps({
        "workbench.colorCustomizations": colors,
        "editor.tokenColorCustomizations": {
            "textMateRules": [
                {"name": n, "scope": s,
                 "settings": {"foreground": f, **({"fontStyle": st} if st else {})}}
                for n, s, f, st in rules
            ]
        },
    }, indent=2) + "\n"


# -------------------------------------------------------------------- Xcode
def xcode(slug, t, fg, ansi, appear):
    sx = SYNTAX[appear]

    def rgba(h, a=1.0):
        r, g, b = parse(h if h.startswith("#") else "#" + h)
        return f"{r/255} {g/255} {b/255} {a}"

    sel = t["selection"]
    accent = t.get("cursor", t["accent"])
    d = {
        "DVTFontAndColorVersion": 1,
        "DVTLineSpacing": 1.2,
        "DVTSourceTextBackground": rgba(t["background"]),
        "DVTSourceTextInsertionPointColor": rgba(accent),
        "DVTSourceTextSelectionColor": rgba(sel, 0.5),
        "DVTSourceTextCurrentLineHighlightColor": rgba(lighten(t["background"], 0.06, fg)),
        "DVTSourceTextInvisiblesColor": rgba(lighten(t["background"], 0.18, fg)),
        "DVTSourceTextBlockDimBackgroundColor": rgba(lighten(t["background"], 0.12, fg)),
        "DVTConsoleTextBackgroundColor": rgba(t["background"]),
        "DVTConsoleTextInsertionPointColor": rgba(accent),
        "DVTConsoleTextSelectionColor": rgba(sel, 0.5),
        "DVTConsoleDebuggerInputTextColor": rgba(fg),
        "DVTConsoleDebuggerInputTextFont": "Menlo-Regular - 12.0",
        "DVTConsoleDebuggerOutputTextColor": rgba(fg),
        "DVTConsoleDebuggerOutputTextFont": "Menlo-Regular - 12.0",
        "DVTConsoleDebuggerPromptTextColor": rgba(t["accent"]),
        "DVTConsoleDebuggerPromptTextFont": "Menlo-Regular - 12.0",
        "DVTConsoleExectuableInputTextColor": rgba(fg),
        "DVTConsoleExectuableInputTextFont": "Menlo-Regular - 12.0",
        "DVTConsoleExectuableOutputTextColor": rgba(fg),
        "DVTConsoleExectuableOutputTextFont": "Menlo-Regular - 12.0",
        "DVTMarkupTextBackgroundColor": rgba(lighten(t["background"], 0.04, fg)),
        "DVTMarkupTextEmphasisColor": rgba(fg),
        "DVTMarkupTextInlineCodeColor": rgba(fg),
        "DVTMarkupTextLinkColor": rgba(sx["function"]),
        "DVTMarkupTextNormalColor": rgba(fg),
        "DVTMarkupTextOtherHeadingColor": rgba(t["accent"]),
        "DVTMarkupTextPrimaryHeadingColor": rgba(t["accent"]),
        "DVTMarkupTextSecondaryHeadingColor": rgba(t["accent"]),
        "DVTMarkupTextStrongColor": rgba(fg),
        "DVTScrollbarMarkerAnalyzerColor": rgba(t["accent"]),
        "DVTScrollbarMarkerBreakpointColor": rgba(sx["error"]),
        "DVTScrollbarMarkerDiffColor": rgba(sx["type"]),
        "DVTScrollbarMarkerDiffConflictColor": rgba(sx["error"]),
        "DVTScrollbarMarkerErrorColor": rgba(sx["error"]),
        "DVTScrollbarMarkerRuntimeIssueColor": rgba(t["accent"]),
        "DVTScrollbarMarkerWarningColor": rgba(sx["number"]),
        "Default Text Font": "Menlo-Regular - 12.0",
        "DVTSourceTextSyntaxColors": {
            "xcode.syntax.attribute": rgba(sx["type"]),
            "xcode.syntax.character": rgba(sx["string"]),
            "xcode.syntax.comment": rgba(sx["comment"]),
            "xcode.syntax.comment.doc": rgba(sx["comment"]),
            "xcode.syntax.comment.doc.keyword": rgba(sx["keyword"]),
            "xcode.syntax.declaration.other": rgba(sx["function"]),
            "xcode.syntax.declaration.type": rgba(sx["type"]),
            "xcode.syntax.identifier.class": rgba(sx["type"]),
            "xcode.syntax.identifier.class.system": rgba(sx["type"]),
            "xcode.syntax.identifier.constant": rgba(sx["constant"]),
            "xcode.syntax.identifier.constant.system": rgba(sx["constant"]),
            "xcode.syntax.identifier.function": rgba(sx["function"]),
            "xcode.syntax.identifier.function.system": rgba(sx["function"]),
            "xcode.syntax.identifier.macro": rgba(sx["type"]),
            "xcode.syntax.identifier.macro.system": rgba(sx["type"]),
            "xcode.syntax.identifier.type": rgba(sx["keyword"]),
            "xcode.syntax.identifier.type.system": rgba(sx["keyword"]),
            "xcode.syntax.identifier.variable": rgba(sx["variable"]),
            "xcode.syntax.identifier.variable.system": rgba(sx["punctuation"]),
            "xcode.syntax.keyword": rgba(sx["keyword"]),
            "xcode.syntax.mark": rgba(sx["comment"]),
            "xcode.syntax.number": rgba(sx["number"]),
            "xcode.syntax.plain": rgba(fg),
            "xcode.syntax.preprocessor": rgba(sx["tag"]),
            "xcode.syntax.string": rgba(sx["string"]),
            "xcode.syntax.url": rgba(sx["function"]),
        },
    }
    import io
    buf = io.BytesIO()
    plistlib.dump(d, buf, fmt=plistlib.FMT_XML)
    return buf.getvalue().decode()


def main():
    for out in ("jetbrains", "arduino", "xcode"):
        os.makedirs(out, exist_ok=True)
    for slug, t, fg, ansi, appear in themes():
        name = slug
        with open(f"jetbrains/defdo-{name}.theme", "w") as f:
            f.write(jetbrains(slug, t, fg, ansi, appear))
        with open(f"arduino/defdo-{name}.settings.json", "w") as f:
            f.write(arduino(slug, t, fg, ansi, appear))
        with open(f"xcode/defdo-{name}.xccolortheme", "w") as f:
            f.write(xcode(slug, t, fg, ansi, appear))
        print("wrote", name, "x3")


if __name__ == "__main__":
    main()
