#!/usr/bin/env bash
# manual.sh — kirbs.pomodoro pilot handbook

P=$'\e[38;5;207m'   # pink
C=$'\e[38;5;205m'   # light pink
G=$'\e[92m'         # green
Y=$'\e[93m'         # yellow
D=$'\e[38;5;240m'   # dim
B=$'\e[1m'          # bold
E=$'\e[0m'          # reset

divider() { echo -e "${D}  $(printf '─%.0s' {1..60})${E}"; }
hdr()     { echo -e "\n${B}${P}  ✦ $1${E}"; divider; }

clear
echo -e "
${P}  (\(\
  (>w<)  pilot handbook
  (ss  <3${E}
  ${D}kirbs.pomodoro — cosmic focus system${E}
"
divider

hdr "LAUNCH"
echo -e "  ${C}./kirbs.sh${E}              ${D}→${E} main launch menu"
echo -e "  ${C}./wid.sh${E}                ${D}→${E} widget + music (split pane)"
echo -e "  ${C}python3 pomodoro_timer.py${E} ${D}→${E} timer only"
echo -e "  ${C}python3 widget.py${E}        ${D}→${E} live dashboard"
echo -e "  ${C}python3 music_player.py${E}  ${D}→${E} youtube music stream"
echo -e "  ${C}python3 local_vibe.py${E}    ${D}→${E} offline mp3 player"
echo -e "  ${C}python3 healer.py${E}        ${D}→${E} system health check"

hdr "TIMER CONTROLS"
printf "  ${Y}%-12s${E} %s\n" "space"   "pause / resume"
printf "  ${Y}%-12s${E} %s\n" "c"       "open wisdom chat"
printf "  ${Y}%-12s${E} %s\n" "s"       "stats leaderboard"
printf "  ${Y}%-12s${E} %s\n" "a"       "kirby config / settings"
printf "  ${Y}%-12s${E} %s\n" "m"       "toggle music signal"
printf "  ${Y}%-12s${E} %s\n" "o"       "change background colour"
printf "  ${Y}%-12s${E} %s\n" "n"       "save + start new session"
printf "  ${Y}%-12s${E} %s\n" "q"       "save + quit"

hdr "GALACTIC RANKS"
printf "  ${G}%-10s${E} %s\n" "0 m"      "🛸  Space Cadet"
printf "  ${G}%-10s${E} %s\n" "100 m"    "🌙  Moon Walker"
printf "  ${G}%-10s${E} %s\n" "500 m"    "☄️   Comet Rider"
printf "  ${G}%-10s${E} %s\n" "1,000 m"  "🚀  Orbit Master"
printf "  ${G}%-10s${E} %s\n" "2,500 m"  "⭐  Star Pilot"
printf "  ${G}%-10s${E} %s\n" "5,000 m+" "🌌  Galactic Overlord"
echo -e "\n  ${D}10 metres = 1 minute of focus time${E}"

hdr "WISDOM CHAT"
echo -e "  type a tag mid-session to get targeted quotes:\n"
printf "  ${C}%-10s${E} %s\n" "iro"    "stoic / iroha"
printf "  ${C}%-10s${E} %s\n" "bronte" "charlotte brontë"
printf "  ${C}%-10s${E} %s\n" "kant"   "immanuel kant"
printf "  ${C}%-10s${E} %s\n" "lyrics" "billie / mj / bowie"
printf "  ${C}%-10s${E} %s\n" "heroic" "epic + motivational"
printf "  ${C}%-10s${E} %s\n" "kirby"  "kirby energy only"
printf "  ${C}%-10s${E} %s\n" "vibe"   "lofi chill"
printf "  ${C}%-10s${E} %s\n" "wisdom" "mixed wisdom"
echo -e "  ${D}or just type anything for a random one${E}"

hdr "MUSIC SETUP"
echo -e "  ${B}streaming${E}  python3 music_player.py   ${D}(requires yt-dlp + ffmpeg)${E}"
echo -e "  ${B}offline${E}    drop mp3 →  ${C}data/focus_music.mp3${E}"
echo -e "             then run  ${C}python3 local_vibe.py play${E}"
echo -e "\n  ${D}on session complete, music_signal.txt is written with PLAY_NEXT${E}"

hdr "FILE MAP"
printf "  ${C}%-26s${E} %s\n" "pomodoro_timer.py"   "core timer"
printf "  ${C}%-26s${E} %s\n" "widget.py"            "live status dashboard"
printf "  ${C}%-26s${E} %s\n" "music_player.py"      "youtube stream player"
printf "  ${C}%-26s${E} %s\n" "local_vibe.py"        "offline mp3 controller"
printf "  ${C}%-26s${E} %s\n" "kirby_notify.py"      "desktop notifications"
printf "  ${C}%-26s${E} %s\n" "kirby_desktop.py"     "desktop widget"
printf "  ${C}%-26s${E} %s\n" "healer.py"            "system health checker"
printf "  ${C}%-26s${E} %s\n" "bashrc.py"            "shell menu + aliases"
printf "  ${C}%-26s${E} %s\n" "volume.py"            "volume control"
printf "  ${C}%-26s${E} %s\n" "data/"                "stats, history, music"
printf "  ${C}%-26s${E} %s\n" "logs/"                "session logs"
printf "  ${C}%-26s${E} %s\n" "templates/"           "manual html"

divider
echo -e "\n  ${P}fly far, avi. the galaxy is yours. 🌌${E}\n"
read -rp "  press enter to return ~ " _