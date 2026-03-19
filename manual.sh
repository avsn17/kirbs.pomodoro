#!/bin/bash
# 📖 kirbs.pomodoro — Manual Viewer
# Usage: manual  (after adding alias to .bashrc)

PINK='\033[38;5;218m'
CYAN='\033[0;36m'
WHITE='\033[97m'
VOID='\033[0;90m'
BOLD='\033[1m'
NC='\033[0m'

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANUAL="$DIR/MANUAL.md"

if [[ ! -f "$MANUAL" ]]; then
    echo -e "${PINK}❌ MANUAL.md not found in $DIR${NC}"
    echo -e "${VOID}Run: git pull origin main${NC}"
    exit 1
fi

clear
echo -e "${PINK}${BOLD}"
echo "  ╔══════════════════════════════════════════╗"
echo "  ║   📖 KIRBS.POMODORO — MANUAL             ║"
echo "  ║       Pilot: avsn17 · Cosmic Kirbs       ║"
echo "  ╚══════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "${VOID}  Scroll: arrows / PgUp / PgDn   Exit: q${NC}\n"
sleep 0.6

# Use bat if available (syntax highlighting), else less
if command -v bat &>/dev/null; then
    bat --style=plain --language=markdown --paging=always "$MANUAL"
elif command -v less &>/dev/null; then
    less -R "$MANUAL"
else
    cat "$MANUAL"
fi