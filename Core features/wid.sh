#!/bin/bash
# 🌸 PINK COSMIC STATION: GHOST CLEANUP | avsn17
cd /workspaces/kirbs.pomodoro

# 1. WEBHOOK SYNC
echo "active" > music_signal.txt
git add music_signal.txt && git commit -m "avsn17 Session Start" --quiet && git push origin main --quiet &

# 2. THE PLAYLIST
URLS=(
  "https://youtu.be/5XJNg8x89yo" "https://youtu.be/QNJL6nfu__Q" 
  "https://youtu.be/AmXdpVnJwt8" "https://youtu.be/ukgluvJpL4U" 
  "https://youtu.be/9-HhuD6D_3U"
)

play_legend() {
    RAND_URL=${URLS[$RANDOM % ${#URLS[@]}]}
    xdg-open "$RAND_URL" &>/dev/null &
}
play_legend

# 3. UI CONFIG
PINK='\033[38;5;218m'; WHITE='\033[97m'; NC='\033[0m'
KIRBYS=("(> ^.^)>" "<(^.^ <)" "(> ' ' )>" "<( ' ' <)")

trap 'echo "paused" > music_signal.txt; git add music_signal.txt; git commit -m "End Session" --quiet; git push origin main --quiet; clear; echo -e "${PINK}Bye avsn17! 🌸${NC}"; exit' SIGINT

clear
echo -e "${PINK}╭──────────────────────────────────────────────────╮"
echo -e "│  ➣ ${WHITE}CLEAN STATION ACTIVE | avsn17             ${PINK}│"
echo -e "├──────────────────────────────────────────────────┤"
echo -e "│  ${WHITE}Type 'save' to clear ghosts & push to cloud.   ${PINK}│"
echo -e "╰──────────────────────────────────────────────────╯${NC}"
echo -e "       ${PINK}♥  ${WHITE}${KIRBYS[$RANDOM % 4]}  ${PINK}♥${NC}"

while true; do
    echo -ne "\n${PINK}avsn17 > ${NC}"
    read -r USER_INPUT
    
    if [[ "$USER_INPUT" == "exit" ]]; then break; fi

    if [[ "$USER_INPUT" == "save" ]]; then
        echo -e "${PINK}Gemini > ${WHITE}Cleaning ghosts and saving...${NC}"
    
        
        echo -ne "${PINK}Message: ${WHITE}"
        read -r MSG
        if [ -z "$MSG" ]; then MSG="Cleaned ghosts for avsn17"; fi
        
        git commit -m "$MSG"
        git push origin main
        echo -e "${PINK}✅ Ghosts cleared. Git is clean!${NC}"
        continue
    fi

    if [[ "$USER_INPUT" == "next" ]]; then
        play_legend
        echo -e "${PINK}✨ Legend Swapped!${NC}"
        continue
    fi

    echo -e "\033[91m  Unknown command: $USER_INPUT\n  Try: save, next, exit\033[0m"
done
