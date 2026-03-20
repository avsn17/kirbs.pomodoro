#!/bin/bash
# 🌸 kirbs.pomodoro — One-time setup
# Adds 'manual', 'wid', 'kirbs', 'poyo' commands to your shell
# Usage: bash setup.sh

PINK='\033[38;5;218m'
GREEN='\033[0;32m'
VOID='\033[0;90m'
NC='\033[0m'
BOLD='\033[1m'

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASHRC="$HOME/.bashrc"
MARKER="# kirbs.pomodoro aliases"

echo -e "${PINK}${BOLD}"
echo "  ╔══════════════════════════════════════════╗"
echo "  ║   🌸 KIRBS.POMODORO SETUP                ║"
echo "  ╚══════════════════════════════════════════╝"
echo -e "${NC}"

# Check if already installed
if grep -q "$MARKER" "$BASHRC" 2>/dev/null; then
    echo -e "${VOID}  Already installed. Updating...${NC}"
    # Remove old block
    sed -i "/$MARKER/,/# end kirbs.pomodoro/d" "$BASHRC"
fi

# Append alias block
cat >> "$BASHRC" << ALIASES

$MARKER
KIRBS_DIR="$DIR"
alias manual='bash "\$KIRBS_DIR/manual.sh"'
alias wid='bash "\$KIRBS_DIR/wid.sh"'
alias kirbs='bash "\$KIRBS_DIR/kirbs.sh"'
alias poyo='python3 "\$KIRBS_DIR/pomodoro_timer.py"'
alias healer='python3 "\$KIRBS_DIR/healer.py"'
# end kirbs.pomodoro
ALIASES

chmod +x "$DIR/manual.sh" "$DIR/kirbs.sh" "$DIR/wid.sh" "$DIR/kirby_backup.sh" "$DIR/start_poyo.sh"

echo -e "${GREEN}  ✅ Commands installed:${NC}"
echo -e "     ${PINK}manual${NC}  — open the manual"
echo -e "     ${PINK}kirbs${NC}   — launcher menu"
echo -e "     ${PINK}poyo${NC}    — start timer directly"
echo -e "     ${PINK}wid${NC}     — start widget / clean station"
echo -e "     ${PINK}healer${NC}  — system check"
echo ""
echo -e "${VOID}  Run this to activate now:${NC}"
echo -e "     ${PINK}source ~/.bashrc${NC}"
echo ""
echo -e "${PINK}  <( ^ )> Poyo! You're all set, avsn17.${NC}"