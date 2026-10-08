#!/usr/bin/env python3
"""Generate iTerm2 Dynamic Profiles from the defdo .itermcolors palettes.

Produces ~/Library/Application Support/iTerm2/DynamicProfiles/defdo-profiles.json
(one profile per theme) so the whole defdo family is selectable with Cmd+O /
Profile menu, live-editable, and never written into com.googlecode.iterm2.plist.

Build-then-move outside the watched folder with jq validation, per iTerm2's
Dynamic Profiles docs (iTerm loads every file in the dir and would pick up
half-written or backup JSON).

Usage:
  python3 tools/gen_iterm2_profiles.py            # print to stdout for review
  python3 tools/gen_iterm2_profiles.py --install  # validate + atomic install
"""
import json, os, subprocess, sys, tempfile, glob

DYN_DIR = os.path.expanduser("~/Library/Application Support/iTerm2/DynamicProfiles")
OUT_FILE = "defdo-profiles.json"
FONT = os.environ.get("DEFDO_ITERM_FONT", "JetBrainsMonoNF-Regular 12")

COLOR_KEYS = ["Background Color", "Bold Color", "Cursor Color", "Cursor Text Color",
              "Foreground Color", "Link Color", "Selected Text Color", "Selection Color"]


def load_palette(path):
    d = json.loads(subprocess.check_output(["plutil", "-convert", "json", "-o", "-", path]))
    return {k: v for k, v in d.items()
            if k.startswith("Ansi ") or k in COLOR_KEYS}


def profile(slug, colors):
    name = f"defdo {slug.replace('-', ' ')}"
    return {
        "Name": name,
        "Guid": f"defdo-iterm-{slug}",
        "Tags": ["defdo"],
        "Normal Font": FONT,
        "Use Non-ASCII Font": False,
        "Columns": 132,
        "Rows": 40,
        "Unlimited Scrollback": True,
        "Cursor Type": 1,
        "Blinking Cursor": False,
        "Silence Bell": True,
        "Option Key Sends": 2,
        "Right Option Key Sends": 0,
        "Use Bold Font": True,
        "Use Bright Bold": True,
        **colors,
    }


def studio_profile(base_colors):
    """Auto-launch profile: opens iTerm straight into the default studio space."""
    p = profile("studio", base_colors)
    p["Custom Command"] = "Yes"
    p["Command"] = ("zsh -ic 'command -v studio >/dev/null && studio default"
                    " || echo \"studio not found — see ~/.dotfiles/defdo-ai-studio/README.md\" && zsh -l'")
    return p


def main():
    install = "--install" in sys.argv
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    profiles = []
    base_colors = None
    for f in sorted(glob.glob(f"{repo}/themes/*.itermcolors")):
        slug = os.path.basename(f).replace("defdo-theme.", "").replace(".itermcolors", "")
        colors = load_palette(f)
        profiles.append(profile(slug, colors))
        if slug == "base":
            base_colors = colors
    if base_colors:
        profiles.append(studio_profile(base_colors))
    doc = {"Profiles": profiles}

    payload = json.dumps(doc, indent=2) + "\n"
    if not install:
        sys.stdout.write(payload)
        return

    fd, tmp = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(payload)
        subprocess.run(["jq", "empty", tmp], check=True)
        os.makedirs(DYN_DIR, exist_ok=True)
        os.replace(tmp, os.path.join(DYN_DIR, OUT_FILE))
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    print(f"installed {len(profiles)} profiles -> {DYN_DIR}/{OUT_FILE}")


if __name__ == "__main__":
    main()
