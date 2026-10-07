#!/usr/bin/env bash
# defdo shadow - GNOME Terminal (Ubuntu 20.04+) profile installer.
# Creates a dconf profile; pick it in Preferences > Profiles. Safe to re-run.
set -euo pipefail
command -v dconf >/dev/null || { echo "dconf not found - sudo apt install dconf-cli" >&2; exit 1; }
command -v uuidgen >/dev/null || { echo "uuidgen not found - sudo apt install uuid-runtime" >&2; exit 1; }

UUID=$(uuidgen | tr 'A-Z' 'a-z')
P="/org/gnome/terminal/legacy/profiles:/:$UUID"

dconf write "$P/name" "'defdo shadow'"
dconf write "$P/palette" "'#131c21:#e24f4f:#0dbc79:#f9bc02:#006ee8:#8954ac:#11a8cd:#e5e5e5:#666666:#f65757:#23d18b:#f9e802:#3b8eea:#a870d6:#29b8db:#fffefe'"
dconf write "$P/background-color" "'#191a19'"
dconf write "$P/foreground-color" "'#eeffff'"
dconf write "$P/cursor-background-color" "'#bebc2e'"
dconf write "$P/cursor-foreground-color" "'#191a19'"
dconf write "$P/selection-background-color" "'#bebc2e'"
dconf write "$P/selection-foreground-color" "'#191a19'"
dconf write "$P/bold-color" "'#eeffff'"
dconf write "$P/use-theme-colors" "false"
dconf write "$P/use-theme-transparency" "false"
dconf write "$P/use-transparent-background" "false"
dconf write "$P/visible-name" "'defdo shadow'"

# register the profile (append to profile-list)
LIST=$(gsettings get org.gnome.Terminal profile-list)
if [[ "$LIST" == "[]" ]]; then
  LIST="['profile:$UUID']"
else
  LIST="${LIST%]}, 'profile:$UUID']"
fi
gsettings set org.gnome.Terminal profile-list "$LIST"
echo "defdo shadow installed - choose it in GNOME Terminal > Preferences > Profiles"
