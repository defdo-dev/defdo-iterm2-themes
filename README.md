# defdo-iterm2-themes

Source of truth for the Defdo theme family. `palette.json` defines the
canonical palette — one shared ANSI 0-15 set; each variant changes only
background, selection and accent. Every format in the family is generated
from these colors:

| Format | Repo / folder | Variants |
| --- | --- | --- |
| iTerm2 color presets | `themes/` (this repo) | 7 |
| iTerm2 Dynamic Profiles | `tools/gen_iterm2_profiles.py` → `DynamicProfiles/defdo-profiles.json` | 7 |
| OpenCode TUI | `opencode/` (this repo) | 7 |
| powerlevel10k | `prompt/` (this repo) | 7 |
| VS Code | [defdo-vscode-themes](https://github.com/defdo-dev/defdo-vscode-themes) | 7 |
| Zed | [zed-themes](https://github.com/defdo-dev/zed-themes) | 7 |
| JetBrains / Android Studio | `jetbrains/` (this repo) | 7 |
| Arduino IDE 2 | `arduino/` (this repo) | 7 |
| Xcode | `xcode/` (this repo) | 7 |

## Themes

| Theme | Background | Accent | Notes |
| --- | --- | --- | --- |
| `base` | `#131c21` | `#bebc2e` | Default Defdo palette |
| `halloween` | `#140021` | `#afa6f6` | Purple variant |
| `dark` | `#141414` | `#bebc2e` | |
| `gray` | `#313131` | `#bebc2e` | |
| `solid-gray` | `#303841` | `#bebc2e` | |
| `shadow` | `#191a19` | `#bebc2e` | |
| `yellow` | `#0f0f0a` | `#f9bc02` | Matches the defdo-yellow VS Code theme |


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

## Dynamic Profiles (recommended)

`tools/gen_iterm2_profiles.py --install` writes all six themes as
iTerm2 Dynamic Profiles (`~/Library/Application Support/iTerm2/DynamicProfiles/defdo-profiles.json`,
tagged `defdo`, font `JetBrainsMonoNF-Regular 12` — override with
`DEFDO_ITERM_FONT`). iTerm2 hot-reloads the folder; switch with `Cmd+O`.
Nothing is written into `com.googlecode.iterm2.plist`.

## powerlevel10k

`prompt/p10k.defdo-theme-<slug>.zsh` — rainbow powerline configs. Use one as
your `~/.p10k.zsh` (or source it from it):

```
cp prompt/p10k.defdo-theme-base.zsh ~/.p10k.zsh && source ~/.p10k.zsh
```

All variants share the ANSI palette, so segment colors are identical; the
terminal background comes from the iTerm2 profile, not the p10k file.

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

## IDE exports (JetBrains, Arduino, Xcode)

`tools/gen_ide_themes.py` emits all ten variants for the editors your stack
actually uses:

```
jetbrains/defdo-<slug>.theme        # Android Studio / IntelliJ: Settings → Editor → Color Scheme → gear → Import Scheme
arduino/defdo-<slug>.settings.json  # Arduino IDE 2: merge into settings.json (File → Preferences → Settings JSON)
xcode/defdo-<slug>.xccolortheme     # Xcode: copy to ~/Library/Developer/Xcode/UserData/FontAndColorThemes/
```

## Premium line

`latte`, `pro` and `legend` live in the private
[defdo-themes-premium](https://github.com/defdo-dev/defdo-themes-premium)
repo (commercial license). This repo is the free tier only.
