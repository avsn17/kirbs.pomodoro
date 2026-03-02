#!/usr/bin/env bash
# ┌─────────────────────────────────────────────────┐
# │   kirbs — Cosmic Mission Control Launcher        │
# │   Usage: chmod +x kirbs.sh && ./kirbs.sh         │
# └─────────────────────────────────────────────────┘

PINK='\033[38;5;218m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMER="$SCRIPT_DIR/pomodoro_timer.py"
SIGNAL="$SCRIPT_DIR/music_signal.txt"

# ── Clean exit ────────────────────────────────────
cleanup() {
    kill $(jobs -p) 2>/dev/null
    rm -f "$SIGNAL"
    echo -e "\n${PINK}<( 'o' )> Poyo! Cockpit closed, Cosmic Kirbs.${NC}"
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# ── Pre-flight ────────────────────────────────────
clear
echo -e "${CYAN}${BOLD}"
echo "  ╔══════════════════════════════════════╗"
echo "  ║  🌟 COSMIC MISSION CONTROL  ★ kirbs  ║"
echo "  ║       Pilot: Cosmic Kirbs / avsn17   ║"
echo "  ╚══════════════════════════════════════╝"
echo -e "${NC}"

if [[ ! -f "$TIMER" ]]; then
    echo -e "❌ ${BOLD}[ERROR]${NC} pomodoro_timer.py not found in $SCRIPT_DIR"
    exit 1
fi

# Ensure signal file exists
: > "$SIGNAL"
echo -e "${YELLOW}🚀 Launching cockpit...${NC}\n"

# ── Launch ────────────────────────────────────────
python3 "$TIMER"