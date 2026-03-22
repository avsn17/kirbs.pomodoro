#!/usr/bin/env bash
P=$'\e[38;5;207m'; C=$'\e[38;5;205m'; G=$'\e[92m'; Y=$'\e[93m'; E=$'\e[0m'; B=$'\e[1m'

clear
echo -e "
${P}  ~* kirbs.pomodoro — pilot handbook *~${E}

${B}${C}  LAUNCH${E}
  python3 pomodoro_timer.py     main timer
  ./kirbs.sh                    launch menu
  ./wid.sh                      widget + music
  python3 widget.py             widget only
  python3 music_player.py       music only

${B}${C}  TIMER KEYS${E}
  space       pause / resume
  c           wisdom chat
  s           stats leaderboard
  a           kirby config
  m           toggle music signal
  o           change background colour
  n           save + new session
  q           save + quit

${B}${C}  RANKS${E}
  ${G}0 m${E}        🛸 Space Cadet
  ${G}100 m${E}      🌙 Moon Walker
  ${G}500 m${E}      ☄️  Comet Rider
  ${G}1000 m${E}     🚀 Orbit Master
  ${G}2500 m${E}     ⭐ Star Pilot
  ${G}5000 m+${E}    🌌 Galactic Overlord

${B}${C}  WISDOM CHAT TAGS${E}
  iro · bronte · kant · lyrics · heroic · kirby · vibe · wisdom

${B}${C}  FILES${E}
  pomodoro_timer.py   core timer
  widget.py           live dashboard
  music_player.py     yt-dlp music
  local_vibe.py       offline mp3 player
  healer.py           system check
  bashrc.py           shell aliases + menu
  data/               stats + history
  templates/          manual html

${B}${C}  MUSIC${E}
  drop an mp3 →  data/focus_music.mp3
  or use music_player.py for youtube streaming

  ${P}10 metres = 1 minute of focus. fly far, avi. 🌌${E}
"
read -rp "  press enter to return ~ " _
