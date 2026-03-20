#!/usr/bin/env bash
# organize.sh — kirbs.pomodoro file organizer

set -euo pipefail

P=$'\e[38;5;207m'; G=$'\e[92m'; R=$'\e[91m'; E=$'\e[0m'

ok()  { echo "  ${G}OK${E}  ${P}$1${E}"; }
bad() { echo "  ${R}!!${E}  ${P}$1${E}"; }
hdr() { echo -e "\n  ${P}$1${E}"; }

move() {
    local src="$1" dst_dir="$2"
    if [ -e "$src" ]; then
        mkdir -p "$dst_dir"
        if [ -e "$dst_dir/$(basename "$src")" ]; then
            bad "$src → $dst_dir  (already exists, skipped)"
        else
            mv "$src" "$dst_dir/"
            ok "$src → $dst_dir/"
        fi
    fi
}

hdr "core"
move pomodoro_timer.py  src
move web_app.py         src
move kirby_desktop.py   src
move kirby_notify.py    src
move music_player.py    src
move volume.py          src
move widget.py          src
move healer.py          src

hdr "launchers"
move kirbs.sh           launchers
move start_poyo.sh      launchers
move poyo_pro.sh        launchers
move poyo_ultimate.sh   launchers
move wid.sh             launchers
move kirby_backup.sh    launchers

hdr "deployment"
move Procfile           deploy
move dockerfile         deploy
move docker_compose.yml deploy
move deploy.sh          deploy
move vercel.json        deploy

hdr "assets"
move mario.gif          assets
move mario_sticker.gif  assets
move index.html         assets

hdr "runtime (generated)"
move music_signal.txt   runtime
[ -d __pycache__ ] && { mv __pycache__ runtime/ && ok "__pycache__ → runtime/"; } || true

hdr "done"
echo
find src launchers deploy assets runtime data logs templates -maxdepth 0 2>/dev/null \
    | sort | while read -r d; do
        count=$(find "$d" | tail -n +2 | wc -l | tr -d ' ')
        echo "    ${P}$d/${E}  ($count files)"
    done
echo