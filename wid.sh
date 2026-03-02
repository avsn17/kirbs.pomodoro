#!/bin/bash
# 🌸 PINK COSMIC STATION: GOD MODE PATCHED | avsn17
cd /workspaces/kirbs.pomodoro

# 1. WEBHOOK SYNC
echo "active" > music_signal.txt
git add music_signal.txt && git commit -m "avsn17 Session Start" --quiet && git push origin main --quiet &

# 2. START MUSIC
pkill mpv 2>/dev/null
mpv --no-video --shuffle --input-ipc-server=/tmp/mpv-socket \
--ytdl-raw-options="cookies=cookies.txt" \
"https://youtu.be/5XJNg8x89yo" "https://youtu.be/QNJL6nfu__Q" \
"https://youtu.be/AmXdpVnJwt8" "https://youtu.be/ukgluvJpL4U" \
"https://youtu.be/9-HhuD6D_3U" &>/dev/null &

# 3. UI ENGINE
PINK='\033[38;5;218m'; WHITE='\033[97m'; NC='\033[0m'
trap 'pkill mpv; echo "paused" > music_signal.txt; git add music_signal.txt; git commit -m "End Session" --quiet; git push origin main --quiet; exit' SIGINT

clear
echo -e "${PINK}╭──────────────────────────────────────────────────╮"
echo -e "│  🛡️  ${WHITE}GOD MODE PATCHED | avsn17                 ${PINK}│"
echo -e "├──────────────────────────────────────────────────┤"
echo -e "│  ${WHITE}Status: Running MJ, Lana, CAS, BeeGees, Billie ${PINK}│"
echo -e "╰──────────────────────────────────────────────────╯${NC}"

while true; do
    SONG=$(echo '{ "command": ["get_property", "media-title"] }' | socat - /tmp/mpv-socket 2>/dev/null | cut -d'"' -f4)
    echo -ne "\n${PINK}🎵 ${SONG:0:35}... \n${WHITE}avsn17 > ${NC}"
    read -r USER_INPUT
    
    if [[ "$USER_INPUT" == "exit" ]]; then break; fi

    if [[ "$USER_INPUT" == "fix" ]]; then
        # Check if wid is actually set up in .bashrc
        if ! grep -q "alias wid=" ~/.bashrc; then
            FIX="echo \"alias wid='/workspaces/kirbs.pomodoro/wid.sh'\" >> ~/.bashrc && source ~/.bashrc"
            REASON="The 'wid' command wasn't permanently saved in your system."
        else
            FIX="chmod +x /workspaces/kirbs.pomodoro/wid.sh"
            REASON="Permissions might be reset."
        fi

        echo -e "${PINK}Gemini > ${WHITE}$REASON${NC}"
        echo -e "${PINK}Suggested Fix: ${WHITE}$FIX${NC}"
        echo -ne "${PINK}Apply? (y/n): ${NC}"
        read -r CONFIRM
        if [[ "$CONFIRM" == "y" ]]; then 
            eval "$FIX"
            echo -e "${PINK}Applied!${NC}"
        fi
        continue
    fi

    # Execute and capture error
    eval "$USER_INPUT"
    LAST_EXIT=$?
    if [ $LAST_EXIT -eq 127 ]; then
        echo -e "${PINK}⚠ Command not found. (If you typed 'wid', remember you are ALREADY inside it!)${NC}"
    fi
done
