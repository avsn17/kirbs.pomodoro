import os

bashrc = os.path.expanduser('~/.bashrc')
with open(bashrc, 'r') as f:
    content = f.read()

safe_end = '#if [ -f /etc/bash_completion ] && ! shopt -oq posix; then\n#    . /etc/bash_completion\n#fi'
cut = content.find(safe_end)
base = content[:cut + len(safe_end)] if cut != -1 else '\n'.join(content.split('\n')[:100])

fresh = """

# nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"

# kirbs.pomodoro
KIRBS_DIR="/workspaces/kirbs.pomodoro"
alias poyo='python3 "$KIRBS_DIR/pomodoro_timer.py"'
alias kirbs='bash "$KIRBS_DIR/kirbs.sh"'
alias wid='bash "$KIRBS_DIR/wid.sh"'
alias manual='bash "$KIRBS_DIR/manual.sh"'
alias healer='python3 "$KIRBS_DIR/healer.py"'

kirbs_type() {
    local text="$1"
    local delay="${2:-0.03}"
    echo -ne "\\033[38;5;207m"
    local i=0
    while [ $i -lt ${#text} ]; do
        echo -ne "${text:$i:1}"
        sleep "$delay"
        i=$((i+1))
    done
    echo -e "\\033[0m"
}

kirbs_walk() {
    local f
    for f in "(>w<) ~" " (>w<)~" "  (>w<)" "   ~(>w<)" "    ~(>w<)"; do
        echo -ne "\\r  \\033[38;5;207m$f\\033[0m"
        sleep 0.12
    done
    echo ""
}

kirbs_bounce() {
    local msg="$1"
    local f
    for f in "(>w<)" "(-w-)" "(>w<)" "(^w^)" "(>w<)"; do
        echo -ne "\\r  \\033[38;5;207m$f  $msg\\033[0m"
        sleep 0.15
    done
    echo ""
}

kirbs_stars() {
    echo -ne "\\033[38;5;205m  "
    local i
    for i in $(seq 1 40); do echo -ne "* "; sleep 0.02; done
    echo -e "\\033[0m"
}

kirbs_stats() {
    python3 /tmp/kirbs_stats.py
}

kirbs_greeting() {
    local HOUR
    HOUR=$(date +%H)
    if [ "$HOUR" -lt 6 ]; then echo "still up?"
    elif [ "$HOUR" -lt 12 ]; then echo "good morning"
    elif [ "$HOUR" -lt 17 ]; then echo "good afternoon"
    elif [ "$HOUR" -lt 21 ]; then echo "good evening"
    else echo "burning the midnight oil"; fi
}

kirbs_storyline() {
    local PILOT="$1"
    local HOUR
    HOUR=$(date +%H)
    clear
    echo ""
    sleep 0.2
    echo -ne "\\033[38;5;205m  "
    local i
    for i in $(seq 1 35); do echo -ne "* "; sleep 0.03; done
    echo -e "\\033[0m"
    sleep 0.2
    for sp in "" " " "  " "   " "    " "     "; do
        echo -ne "\\r\\033[38;5;207m${sp}(>w<) ~\\033[0m"
        sleep 0.08
    done
    echo ""
    sleep 0.1
    echo -e "\\033[38;5;207m      (>w<)"
    echo -e "      (> <3\\033[0m"
    sleep 0.3
    echo ""
    if [ "$HOUR" -lt 6 ]; then
        kirbs_type "  the stars are still out, $PILOT..." 0.04
        sleep 0.2
        kirbs_type "  kirby finds you here in the dark..." 0.04
        sleep 0.2
        kirbs_type "  brave pilot. the cosmos never sleeps." 0.04
    elif [ "$HOUR" -lt 12 ]; then
        kirbs_type "  a new day begins, $PILOT..." 0.04
        sleep 0.2
        kirbs_type "  kirby has been waiting at the cockpit." 0.04
        sleep 0.2
        kirbs_type "  the galaxy needs your focus today." 0.04
    elif [ "$HOUR" -lt 17 ]; then
        kirbs_type "  afternoon mission control, $PILOT." 0.04
        sleep 0.2
        kirbs_type "  kirby checked your stats. looking good." 0.04
        sleep 0.2
        kirbs_type "  the stars are aligned. lock in." 0.04
    elif [ "$HOUR" -lt 21 ]; then
        kirbs_type "  evening, $PILOT. kirby saved you a seat." 0.04
        sleep 0.2
        kirbs_type "  the cosmic station is quiet now." 0.04
        sleep 0.2
        kirbs_type "  perfect conditions for deep work." 0.04
    else
        kirbs_type "  midnight run, $PILOT?" 0.04
        sleep 0.2
        kirbs_type "  kirby puts on the lofi playlist..." 0.04
        sleep 0.2
        kirbs_type "  legends are built in the quiet hours." 0.04
    fi
    sleep 0.3
    echo ""
    kirbs_stars
    sleep 0.2
    kirbs_stats
    echo ""
    sleep 0.2
}

kirbs_menu() {
    local KIRBS_PILOT
    KIRBS_PILOT=$(cat "$HOME/.kirbs_pilot" 2>/dev/null || echo "pilot")
    kirbs_storyline "$KIRBS_PILOT"
    while true; do
        echo -e "\\033[38;5;207m  \\033[38;5;205mwhat do you want to do, $KIRBS_PILOT?\\033[38;5;207m"
        echo ""
        echo -e "  \\033[1m1\\033[0m\\033[38;5;207m  \\033[38;5;205mwid\\033[38;5;207m     > chill and vibe    music and widget"
        echo -e "  \\033[1m2\\033[0m\\033[38;5;207m  \\033[38;5;205mpoyo\\033[38;5;207m    > lock in           focus timer"
        echo -e "  \\033[1m3\\033[0m\\033[38;5;207m  \\033[38;5;205mkirbs\\033[38;5;207m   > mission control   launch menu"
        echo -e "  \\033[1m4\\033[0m\\033[38;5;207m  \\033[38;5;205mmanual\\033[38;5;207m  > read me           pilot handbook"
        echo -e "  \\033[1m5\\033[0m\\033[38;5;207m  \\033[38;5;205mhealer\\033[38;5;207m  > check vitals      system status"
        echo -e "  \\033[1m6\\033[0m\\033[38;5;207m  \\033[38;5;205msave\\033[38;5;207m    > push to cloud     git sync"
        echo -e "  \\033[1m7\\033[0m\\033[38;5;207m  \\033[38;5;205mgit\\033[38;5;207m     > repo status       quick overview"
        echo -e "  \\033[1m8\\033[0m\\033[38;5;207m  \\033[38;5;205mrename\\033[38;5;207m  > change pilot name"
        echo -e "  \\033[1mq\\033[0m\\033[38;5;207m  \\033[38;5;205mquit\\033[38;5;207m    > just the terminal"
        echo ""
        echo -ne "  \\033[1mpick\\033[0m\\033[38;5;207m > "
        read -r CHOICE
        case "$CHOICE" in
            1|wid)
                kirbs_bounce "launching wid..."
                bash "$KIRBS_DIR/wid.sh"
                echo -e "\\033[38;5;207m"
                kirbs_type "  back at base ~ press enter to return" 0.02
                read -r ;;
            2|poyo)
                kirbs_bounce "locking in..."
                python3 "$KIRBS_DIR/pomodoro_timer.py"
                echo -e "\\033[38;5;207m"
                kirbs_type "  session saved ~ press enter to return" 0.02
                read -r
                kirbs_stats
                echo "" ;;
            3|kirbs)
                kirbs_bounce "mission control..."
                bash "$KIRBS_DIR/kirbs.sh"
                echo -e "\\033[38;5;207m"
                kirbs_type "  back at base ~ press enter to return" 0.02
                read -r ;;
            4|manual)
                kirbs_bounce "opening handbook..."
                bash "$KIRBS_DIR/manual.sh"
                echo -e "\\033[38;5;207m"
                kirbs_type "  press enter to return" 0.02
                read -r ;;
            5|healer)
                kirbs_bounce "scanning vitals..."
                python3 "$KIRBS_DIR/healer.py"
                echo -e "\\033[38;5;207m"
                kirbs_type "  press enter to return" 0.02
                read -r ;;
            6|save)
                kirbs_bounce "syncing to cloud..."
                cd "$KIRBS_DIR" && bash save
                echo -e "\\033[38;5;207m"
                kirbs_type "  press enter to return" 0.02
                read -r ;;
            7|git)
                echo -e "\\033[38;5;207m"
                cd "$KIRBS_DIR"
                kirbs_type "  checking repo status..." 0.02
                echo -e "\\033[38;5;207m  branch  > \\033[38;5;175m$(git branch --show-current)\\033[0m"
                echo -e "\\033[38;5;207m  commit  > \\033[38;5;175m$(git log --oneline -1)\\033[0m"
                echo -e "\\033[38;5;207m  changes > \\033[38;5;175m$(git status --short | wc -l | tr -d ' ') files\\033[0m"
                git status --short | head -8 | sed 's/^/    /'
                echo -e "\\033[0m"
                kirbs_type "  press enter to return" 0.02
                read -r ;;
            8|rename)
                echo -ne "\\033[38;5;207m\\n  current: \\033[1m${KIRBS_PILOT}\\033[0m\\033[38;5;207m  new name > \\033[0m"
                read -r NEW_NAME
                if [ -n "$NEW_NAME" ]; then
                    echo "$NEW_NAME" > "$HOME/.kirbs_pilot"
                    KIRBS_PILOT="$NEW_NAME"
                    kirbs_bounce "saved! welcome, $KIRBS_PILOT ~"
                    sleep 0.5
                fi ;;
            q|quit|exit)
                clear
                kirbs_walk
                kirbs_type "  fly safe, $KIRBS_PILOT. the stars await ~" 0.03
                echo ""
                break ;;
            *)
                kirbs_type "  (>w<)?  try 1-8 or q ~" 0.02
                sleep 0.5 ;;
        esac
        echo ""
    done
}

kirbs_welcome() {
    local PILOT_FILE="$HOME/.kirbs_pilot"
    if [ ! -f "$PILOT_FILE" ]; then
        clear
        echo ""
        echo -ne "\\033[38;5;205m  "
        local i
        for i in $(seq 1 35); do echo -ne "* "; sleep 0.03; done
        echo -e "\\033[0m"
        echo ""
        kirbs_type "  a new pilot has arrived..." 0.05
        sleep 0.3
        echo -e "\\033[38;5;207m  (\\\\(\\\\"
        echo -e "  (>w<)  !!!"
        echo -e "  (> <3\\033[0m"
        sleep 0.3
        kirbs_type "  kirby is SO excited to meet you." 0.04
        sleep 0.2
        kirbs_type "  what should we call you, pilot?" 0.04
        echo ""
        echo -ne "  \\033[1mname\\033[0m\\033[38;5;207m > "
        read -r KIRBS_PILOT
        [ -z "$KIRBS_PILOT" ] && KIRBS_PILOT="pilot"
        echo "$KIRBS_PILOT" > "$PILOT_FILE"
        echo ""
        kirbs_bounce "welcome aboard, $KIRBS_PILOT!"
        kirbs_type "  your cosmic journey begins now ~" 0.04
        sleep 0.5
    fi
    kirbs_menu
}

kirbs_welcome
# end kirbs.pomodoro
"""

with open(bashrc, 'w') as f:
    f.write(base + fresh)

print('bashrc written!')