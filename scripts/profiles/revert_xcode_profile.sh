#!/bin/zsh
set -euo pipefail

SUDO_PASS="${1:-}"

prompt_sudo() {
  if [[ -n "$SUDO_PASS" ]]; then
    echo "$SUDO_PASS" | sudo -S "$@"
  else
    sudo "$@"
  fi
}

for key in NSAutomaticWindowAnimationsEnabled NSWindowResizeTime NSScrollAnimationEnabled; do
  defaults delete NSGlobalDomain "$key" >/dev/null 2>&1 || true
done
for key in autohide-delay autohide-time-modifier expose-animation-duration launchanim mru-spaces show-recents; do
  defaults delete com.apple.dock "$key" >/dev/null 2>&1 || true
done
defaults write com.apple.dock autohide -bool false >/dev/null 2>&1 || true

defaults delete com.apple.finder DisableAllAnimations >/dev/null 2>&1 || true
defaults delete com.apple.universalaccess reduceMotion >/dev/null 2>&1 || true

prompt_sudo pmset -c sleep 1 displaysleep 10 disksleep 10 powernap 1 proximitywake 1
prompt_sudo mdutil -a -i on >/dev/null 2>&1 || true

killall Dock >/dev/null 2>&1 || true
killall Finder >/dev/null 2>&1 || true
killall SystemUIServer >/dev/null 2>&1 || true

echo "Reverted xcode profile"
