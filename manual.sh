#!/usr/bin/env bash
# manual.sh — kirbs.pomodoro pilot handbook

P=$'\e[38;5;207m'
C=$'\e[38;5;205m'
G=$'\e[92m'
Y=$'\e[93m'
D=$'\e[38;5;240m'
W=$'\e[97m'
B=$'\e[1m'
E=$'\e[0m'

div()  { echo -e "${D}  $(printf '·%.0s' {1..58})${E}"; }
hdr()  { echo -e "\n  ${B}${P}$1${E}  ${D}$2${E}\n"; div; }
row()  { printf "  ${C}%-24s${E} ${D}→${E}  %s\n" "$1" "$2"; }
tag()  { printf "  ${Y}%-10s${E} ${D}·${E}  ${W}%s${E}\n" "$1" "$2"; }
rank() { printf "  ${G}%-10s${E} %s  ${D}%s${E}\n" "$1" "$2" "$3"; }

clear
echo -e "
  ${P}  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·${E}
  ${P}     transmission incoming...                  ${E}
  ${P}     source: kirby's cosmic archive            ${E}
  ${P}  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·${E}

       ${P}(\(\${E}
       ${P}(>w<)${E}  this is everything i know, pilot.
       ${P}(ss <3${E}
"
div

hdr "① LAUNCH" "how to take off"
row "./kirbs.sh"                "main launch menu — start here"
row "./wid.sh"                  "widget + music in one shot"
row "python3 pomodoro_timer.py" "timer only, pure focus"
row "python3 widget.py"         "live dashboard (split pane)"
row "python3 music_player.py"   "youtube stream player"
row "python3 local_vibe.py"     "offline mp3 — no internet needed"
row "python3 healer.py"         "system check — run if things feel off"
row "python3 kirby_notify.py"   "desktop pop-up notifications"
row "python3 kirby_desktop.py"  "floating desktop widget"

hdr "② TIMER KEYS" "in-session controls"
tag "space"   "pause / resume the mission"
tag "c"       "open wisdom chat — ask anything"
tag "s"       "leaderboard — see your stats"
tag "a"       "kirby config — mood, hydration, themes"
tag "m"       "toggle music signal on / off"
tag "o"       "cycle background colour"
tag "n"       "save progress + start fresh session"
tag "q"       "save + quit — fly safe"

hdr "③ GALACTIC RANKS" "10 m = 1 min of focus"
rank "0 m"       "🛸  Space Cadet"       "just arrived"
rank "100 m"     "🌙  Moon Walker"       "getting started"
rank "500 m"     "☄️   Comet Rider"      "building momentum"
rank "1,000 m"   "🚀  Orbit Master"      "seriously locking in"
rank "2,500 m"   "⭐  Star Pilot"        "the stars know your name"
rank "5,000 m+"  "🌌  Galactic Overlord" "you are the cosmos"

hdr "④ WISDOM CHAT" "type a tag mid-session"
tag "iro"     "stoic / iroha — quiet strength"
tag "bronte"  "charlotte brontë — fire + longing"
tag "kant"    "immanuel kant — duty + reason"
tag "lyrics"  "billie / mj / bowie — pure feeling"
tag "heroic"  "epic + motivational — battle cries"
tag "kirby"   "kirby energy only — pure joy"
tag "vibe"    "lofi chill — soft focus"
tag "wisdom"  "mixed — surprise me"
echo -e "\n  ${D}  or just type anything for a random one. kirby always has something.${E}"

hdr "⑤ MUSIC SETUP" "two ways to vibe"
echo -e "  ${W}streaming${E}   python3 music_player.py"
echo -e "  ${D}            needs yt-dlp + ffmpeg — run option 5 in kirbs.sh to install${E}\n"
echo -e "  ${W}offline${E}     drop any mp3 →  ${C}data/focus_music.mp3${E}"
echo -e "  ${D}            then: python3 local_vibe.py play${E}"
echo -e "  ${D}            or:   python3 local_vibe.py watch   (auto-triggers on session end)${E}\n"
echo -e "  ${D}  on session complete, music_signal.txt is written → triggers autoplay${E}"

hdr "⑥ STATS & DATA" "where your progress lives"
row "~/.pomodoro_stats.json" "main leaderboard — persists forever"
row "data/kirby_stats.json"  "session detail + xp + water"
row "logs/"                  "per-session logs"
echo -e "\n  ${D}  stats survive across codespaces — they live in your home dir${E}"

hdr "⑦ FILE MAP" "the ship's manifest"
row "pomodoro_timer.py"  "core timer — the heart"
row "widget.py"          "live status dashboard"
row "music_player.py"    "youtube stream"
row "local_vibe.py"      "offline mp3 controller"
row "kirby_notify.py"    "desktop notifications"
row "kirby_desktop.py"   "floating desktop widget"
row "healer.py"          "health checker"
row "bashrc.py"          "shell menu + aliases"
row "volume.py"          "volume control helper"
row "manual.sh"          "you are here"
row "data/"              "stats, history, music files"
row "logs/"              "session logs"
row "templates/"         "html manual"

div
echo -e "
       ${P}(\(\${E}
       ${P}(>w<)${E}  transmission complete.
       ${P}(>  <3${E} the galaxy is quiet. your mission awaits.

  ${D}  · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·${E}
  ${P}  fly far, avi. kirby believes in you. poyo. 🌌${E}
  ${D}  · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·${E}
"
read -rp "  press enter to return to menu ~ " _