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

# UI responsiveness
defaults write NSGlobalDomain NSAutomaticWindowAnimationsEnabled -bool false
defaults write NSGlobalDomain NSWindowResizeTime -float 0.001
defaults write NSGlobalDomain QLPanelAnimationDuration -float 0
defaults write NSGlobalDomain NSScrollAnimationEnabled -bool false

defaults write com.apple.dock autohide -bool true
defaults write com.apple.dock autohide-delay -float 0
defaults write com.apple.dock autohide-time-modifier -float 0
defaults write com.apple.dock launchanim -bool false
defaults write com.apple.dock expose-animation-duration -float 0.1
defaults write com.apple.dock mru-spaces -bool false

defaults write com.apple.finder DisableAllAnimations -bool true
defaults write com.apple.universalaccess reduceMotion -bool true
defaults write com.apple.universalaccess reduceTransparency -bool true
defaults write com.apple.screencapture disable-shadow -bool true

# Keep VM fully awake and responsive on AC
prompt_sudo pmset -c sleep 0 displaysleep 0 disksleep 0 powernap 0 proximitywake 0

# Reduce background indexing load (big win in VMs)
prompt_sudo mdutil -a -i off >/dev/null 2>&1 || true

# Disable recent-app suggestions in Dock
defaults write com.apple.dock show-recents -bool false

# Reload UI services
killall Dock >/dev/null 2>&1 || true
killall Finder >/dev/null 2>&1 || true
killall SystemUIServer >/dev/null 2>&1 || true

echo "Applied blazing profile"
