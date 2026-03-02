#!/bin/bash
# 🌸 PINK COSMIC STATION: CUTE EDITION | avsn17
cd /workspaces/kirbs.pomodoro

# 1. WEBHOOK SYNC
echo "active" > music_signal.txt
git add music_signal.txt && git commit -m "avsn17 Session Start" --quiet && git push origin main --quiet &

# 2. THE PLAYLIST
URLS=(
  "https://youtu.be/5XJNg8x89yo" # Lana
  "https://youtu.be/QNJL6nfu__Q" # MJ
  "https://youtu.be/AmXdpVnJwt8" # CAS
  "https://youtu.be/ukgluvJpL4U" # Bee Gees
  "https://youtu.be/9-HhuD6D_3U" # Billie
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
echo -e "│  ✨ ${WHITE}CUTE STATION ACTIVE | avsn17     ${PINK}           │"
echo -e "├──────────────────────────────────────────────────┤"
echo -e "│  ${WHITE}Type 'save' to backup wid.sh & your work.      ${PINK}│"
echo -e "╰──────────────────────────────────────────────────╯${NC}"
echo -e "       ${PINK}♥  ${WHITE}${KIRBYS[$RANDOM % 4]}  ${PINK}♥${NC}"

while true; do
    echo -ne "\n${PINK}avsn17 > ${NC}"
    read -r USER_INPUT
    
    if [[ "$USER_INPUT" == "exit" ]]; then break; fi

    if [[ "$USER_INPUT" == "save" ]]; then
        echo -e "${PINK}Gemini > ${WHITE}Saving wid.sh and friends...${NC}"
        echo -ne "${PINK}Message: ${WHITE}"
        read -r MSG
        if [ -z "$MSG" ]; then MSG="Aesthetic Patch for avsn17"; fi
        
        # Specific File Save Logic
        git add wid.sh .gitignore README.md
        git commit -m "$MSG"
        git push origin main
        echo -e "${PINK}✅ wid.sh is safely in the cloud.${NC}"
        continue
    fi

    if [[ "$USER_INPUT" == "next" ]]; then
        play_legend
        echo -e "${PINK}✨ Legend Swapped!${NC}"
        continue
    fi

    eval "$USER_INPUT"
done
