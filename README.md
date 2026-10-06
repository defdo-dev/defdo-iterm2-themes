# defdo-iterm2-themes

iTerm2 color schemes for the Defdo theme family, companion to [defdo-vscode-themes](https://github.com/defdo-dev/defdo-vscode-themes). Terminal colors are grouped per theme so the shell matches the editor.

## Themes

| Theme | Background | Notes |
| --- | --- | --- |
| `defdo-theme.base` | warm near-black (33, 28, 19) | Default Defdo palette, matches "defdo base" in VS Code |
| `defdo-theme.halloween` | deep red (54, 29, 31) | Matches "defdo halloween" in VS Code |
| `defdo-theme.dark` | neutral dark (20, 20, 20) | |
| `defdo-theme.gray` | medium gray (49, 49, 49) | |
| `defdo-theme.solid-gray` | warm gray (65, 56, 48) | |
| `defdo-theme.shadow` | near-black green tint (25, 26, 25) | |

## OpenCode themes

`opencode/` contains the same palettes converted to the OpenCode TUI theme format (JSON, `$schema: https://opencode.ai/theme.json`). All six share one ANSI palette; only the background shades differ.

Install:

```
cp opencode/defdo-*.json ~/.config/opencode/themes/
```

Activate via `/theme` in the TUI, or pin in `~/.config/opencode/tui.json`:

```json
{ "theme": "defdo-base" }
```

Regenerate after editing the `.itermcolors` files:

```
python3 tools/gen_opencode_themes.py
```

## Install

```
./install.sh [slug]   # default: base — slugs: base dark gray halloween shadow solid-gray
```

Imports the iTerm2 preset, installs the OpenCode theme JSON to
`~/.config/opencode/themes/` and pins `theme` in `tui.json` (preserving
existing keys, needs `jq`). Restart opencode afterwards.

## Install (iTerm2, manual)

Open iTerm2, then either:

- **Preferences → Colors → Presets → Import…**, select a `.itermcolors` file, pick the preset in a profile; or
- double-click a `.itermcolors` file (imports directly), then assign it in your profile.

## Layout

```
themes/
  defdo-theme.base.itermcolors
  defdo-theme.dark.itermcolors
  defdo-theme.gray.itermcolors
  defdo-theme.halloween.itermcolors
  defdo-theme.shadow.itermcolors
  defdo-theme.solid-gray.itermcolors
```

## Related

- [defdo-vscode-themes](https://github.com/defdo-dev/defdo-vscode-themes) — VS Code versions of base/halloween
- `defdo-prompt` in dotfiles — powerlevel10k configs for the same themes

## License

Apache License 2.0. See [LICENSE](LICENSE).
