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

# Keep UI snappy with minimal visual overhead
defaults write NSGlobalDomain NSAutomaticWindowAnimationsEnabled -bool false
defaults write NSGlobalDomain NSWindowResizeTime -float 0.001
defaults write NSGlobalDomain NSScrollAnimationEnabled -bool false
defaults write com.apple.dock autohide -bool true
defaults write com.apple.dock autohide-delay -float 0
defaults write com.apple.dock autohide-time-modifier -float 0
defaults write com.apple.dock launchanim -bool false
defaults write com.apple.dock expose-animation-duration -float 0.1
defaults write com.apple.dock mru-spaces -bool false
defaults write com.apple.dock show-recents -bool false
defaults write com.apple.finder DisableAllAnimations -bool true
defaults write com.apple.universalaccess reduceMotion -bool true

# Build-friendly power profile (no sleep while preserving display timeout)
prompt_sudo pmset -c sleep 0 displaysleep 30 disksleep 0 powernap 0 proximitywake 0

# Keep Spotlight ON for Xcode/SourceKit/search workflows
prompt_sudo mdutil -a -i on >/dev/null 2>&1 || true

killall Dock >/dev/null 2>&1 || true
killall Finder >/dev/null 2>&1 || true
killall SystemUIServer >/dev/null 2>&1 || true

echo "Applied xcode profile"
