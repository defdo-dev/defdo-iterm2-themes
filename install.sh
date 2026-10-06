#!/usr/bin/env bash
# Install defdo themes for iTerm2 and OpenCode.
# Usage: ./install.sh [theme-slug]   (default: base)
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SLUG="${1:-base}"
ITTERM_DIR="$HOME/Library/Application Support/iTerm2"
OPENCODE_THEME_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/opencode/themes"

THEME_FILE="$REPO_DIR/themes/defdo-theme.${SLUG}.itermcolors"
[[ -f "$THEME_FILE" ]] || { echo "unknown theme: $SLUG (available: $(cd "$REPO_DIR/themes" && ls defdo-theme.*.itermcolors | sed -e 's/defdo-theme\.//' -e 's/\.itermcolors//' | tr '\n' ' '))" >&2; exit 1; }

# 1. iTerm2 color preset
mkdir -p "$ITTERM_DIR"
cp "$THEME_FILE" "$ITTERM_DIR/defdo-theme.${SLUG}.itermcolors"
open "$THEME_FILE"
echo "iTerm2: imported defdo-theme.${SLUG} (assign it in Profile → Colors → Presets)"

# 2. OpenCode theme JSON
mkdir -p "$OPENCODE_THEME_DIR"
cp "$REPO_DIR/opencode/defdo-${SLUG}.json" "$OPENCODE_THEME_DIR/"
echo "OpenCode: installed defdo-${SLUG} to $OPENCODE_THEME_DIR"

# 3. Activate in tui.json (create if missing, preserve other keys)
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
