#!/usr/bin/env bash
# Install defdo themes for iTerm2 and OpenCode.
# Usage: ./install.sh [theme-slug]   (default: base)
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SLUG="${1:-base}"
ITTERM_DIR="$HOME/Library/Application Support/iTerm2"
OPENCODE_THEME_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/opencode/themes"
ALL_SLUGS=$(cd "$REPO_DIR/themes" && ls defdo-theme.*.itermcolors | sed -e 's/defdo-theme\.//' -e 's/\.itermcolors//')

THEME_FILE="$REPO_DIR/themes/defdo-theme.${SLUG}.itermcolors"
[[ -f "$THEME_FILE" ]] || { echo "unknown theme: $SLUG (available: $(cd "$REPO_DIR/themes" && ls defdo-theme.*.itermcolors | sed -e 's/defdo-theme\.//' -e 's/\.itermcolors//' | tr '\n' ' '))" >&2; exit 1; }

# 1. iTerm2 color preset (skip if already imported — the Dynamic Profiles
#    carry inline colors anyway; re-importing triggers the duplicate dialog)
mkdir -p "$ITTERM_DIR"
cp "$THEME_FILE" "$ITTERM_DIR/defdo-theme.${SLUG}.itermcolors"
if defaults read com.googlecode.iterm2 "Custom Color Presets" 2>/dev/null | grep -q "defdo-theme.${SLUG}"; then
  echo "iTerm2: preset defdo-theme.${SLUG} already imported — skipping"
else
  open "$THEME_FILE"
  echo "iTerm2: imported defdo-theme.${SLUG} (assign it in Profile → Colors → Presets)"
fi

# 1b. IDE exports (manual import; documented in README)
for d in jetbrains arduino xcode vscode vim; do
  [[ -d "$REPO_DIR/$d" ]] || continue
  f=$(ls "$REPO_DIR/$d"/defdo-${SLUG}.* "$REPO_DIR/$d"/defdo-theme-${SLUG}.* "$REPO_DIR/$d"/defdo_${SLUG//-/_}.* 2>/dev/null | head -1) || true
  if [[ -n "$f" ]]; then echo "IDE: $d export available -> $f"; fi
done
[[ -d "$REPO_DIR/gnome" ]] && echo "Linux: ./gnome/defdo-${SLUG}.sh installs a GNOME Terminal profile"

# 2. iTerm2 Dynamic Profiles (all themes, live-editable, keeps plist clean)
if command -v jq >/dev/null 2>&1 && [[ -f "$REPO_DIR/tools/gen_iterm2_profiles.py" ]]; then
  python3 "$REPO_DIR/tools/gen_iterm2_profiles.py" --install
fi

# 3. OpenCode theme JSON — every theme (Cmd+/theme picker needs them all)
mkdir -p "$OPENCODE_THEME_DIR"
for slug in $ALL_SLUGS; do
  cp "$REPO_DIR/opencode/defdo-${slug}.json" "$OPENCODE_THEME_DIR/"
done
echo "OpenCode: installed $(echo "$ALL_SLUGS" | wc -w | tr -d ' ') themes to $OPENCODE_THEME_DIR"

# 3b. vim / Neovim colorscheme (both dirs unconditionally — nvim's rtp is
#     ~/.config/nvim and it may not exist yet on first install)
for cd in "$HOME/.vim/colors" "$HOME/.config/nvim/colors"; do
  mkdir -p "$cd"
  for slug in $ALL_SLUGS; do
    cp "$REPO_DIR/vim/defdo_${slug//-/_}.vim" "$cd/" 2>/dev/null
  done
  echo "vim: installed all colorschemes -> $cd"
done

# 4. Activate in tui.json (create if missing, preserve other keys)
TUI_JSON="${XDG_CONFIG_HOME:-$HOME/.config}/opencode/tui.json"
if command -v jq >/dev/null 2>&1; then
  if [[ -f "$TUI_JSON" ]]; then
    jq --arg t "defdo-${SLUG}" '.theme = $t' "$TUI_JSON" > "$TUI_JSON.tmp" && mv "$TUI_JSON.tmp" "$TUI_JSON"
  else
    printf '{\n  "theme": "defdo-%s"\n}\n' "$SLUG" > "$TUI_JSON"
  fi
  echo "OpenCode: tui.json theme → defdo-${SLUG} (restart opencode to apply)"
else
  echo "OpenCode: jq not found — select via /theme (defdo-${SLUG}) or set \"theme\" in $TUI_JSON"
fi
