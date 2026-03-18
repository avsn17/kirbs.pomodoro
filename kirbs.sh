#!/usr/bin/env bash
# ┌─────────────────────────────────────────────────────┐
# │   kirbs.sh — Cosmic Mission Control (bash edition)  │
# │   Launches: Timer + Music Player + Widget           │
# └─────────────────────────────────────────────────────┘

PINK='\033[38;5;218m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
VOID='\033[0;90m'
BOLD='\033[1m'
NC='\033[0m'

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cleanup() {
    kill $(jobs -p) 2>/dev/null
    echo -e "\n${PINK}<( 'o' )> Cockpit closed. Fly safe, Cosmic Kirbs.${NC}"
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

clear
echo -e "${PINK}${BOLD}"
echo "  ╔════════════════════════════════════════╗"
echo "  ║   🌟 COSMIC MISSION CONTROL — kirbs    ║"
echo "  ╚════════════════════════════════════════╝"
echo -e "${NC}"

# ── File checks ───────────────────────────────────────
missing=0
for f in pomodoro_timer.py music_player.py widget.py; do
    if [[ ! -f "$DIR/$f" ]]; then
        echo -e "  ❌ Missing: ${BOLD}$f${NC}"
        missing=1
    fi
done
[[ $missing -eq 1 ]] && echo -e "  ${YELLOW}Some files missing. Only available modules will run.${NC}\n"

# Ensure signal file
: > "$DIR/music_signal.txt"

# ── Menu ──────────────────────────────────────────────
echo -e "  ${CYAN}What would you like to launch?${NC}\n"
echo -e "  ${GREEN}[1]${NC} Timer only"
echo -e "  ${GREEN}[2]${NC} Timer + Music Player (two terminals needed)"
echo -e "  ${GREEN}[3]${NC} Widget only (run in a split pane)"
echo -e "  ${GREEN}[4]${NC} Music Player only"
echo -e "  ${GREEN}[5]${NC} Setup — install dependencies (yt-dlp, ffmpeg)"
echo -e "  ${VOID}[q] Quit${NC}\n"

read -rp "  Select: " choice

case "$choice" in
    1)
        echo -e "\n  ${YELLOW}🚀 Launching Timer...${NC}\n"
        python3 "$DIR/pomodoro_timer.py"
        ;;
    2)
        echo -e "\n  ${YELLOW}🚀 Launching Timer...${NC}"
        echo -e "  ${VOID}→ Open a second terminal and run: python3 widget.py${NC}"
        echo -e "  ${VOID}→ Open a third terminal and run:  python3 music_player.py${NC}\n"
        python3 "$DIR/pomodoro_timer.py"
        ;;
    3)
        echo -e "\n  ${PINK}🛰  Launching Widget...${NC}\n"
        python3 "$DIR/widget.py"
        ;;
    4)
        echo -e "\n  ${CYAN}🎵 Launching Music Player...${NC}\n"
        python3 "$DIR/music_player.py"
        ;;
    5)
        echo -e "\n  ${CYAN}Installing dependencies...${NC}"
        pip install yt-dlp --quiet --break-system-packages 2>/dev/null || pip install yt-dlp --quiet
        sudo apt-get install -y ffmpeg mpv -qq 2>/dev/null
        echo -e "  ${GREEN}Done! Re-run kirbs.sh to launch.${NC}"
        ;;
    q|Q)
        echo -e "  ${VOID}Aborted.${NC}"
        ;;
    *)
        echo -e "  ${YELLOW}Invalid choice. Run ./kirbs.sh again.${NC}"
        ;;
esac