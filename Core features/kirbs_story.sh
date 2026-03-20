#!/bin/bash
P='\033[38;5;207m'
A='\033[38;5;205m'
D='\033[38;5;175m'
R='\033[0m'

PILOT=$(cat "$HOME/.kirbs_pilot" 2>/dev/null || echo "pilot")
HOUR=$(date +%H)

type_out() {
    local text="$1" delay="${2:-0.035}"
    echo -ne "$P"
    local i=0
    while [ $i -lt ${#text} ]; do
        echo -ne "${text:$i:1}"
        sleep "$delay"
        i=$((i+1))
    done
    echo -e "$R"
}

stars_in() {
    echo -ne "$A  "
    for i in $(seq 1 38); do echo -ne "* "; sleep 0.025; done
    echo -e "$R"
}

stars_out() {
    echo -ne "$D  "
    for i in $(seq 1 38); do echo -ne ". "; sleep 0.015; done
    echo -e "$R"
}

kirby_enter() {
    for sp in "" " " "  " "   " "    " "     " "      "; do
        echo -ne "\r${P}${sp}(>w<) ~${R}"
        sleep 0.07
    done
    echo ""
    sleep 0.1
    echo -e "${P}       (>w<)"
    echo -e "${A}       (>  <3${R}"
    sleep 0.3
}

kirby_dance() {
    local msg="$1"
    for f in "(>w<)" "(-w-)" "(^w^)" "(>w<)" "(OwO)" "(>w<)"; do
        echo -ne "\r  ${P}$f  ${A}$msg${R}"
        sleep 0.18
    done
    echo ""
}

kirby_sleep() {
    for f in "(-_-)" "(-_-)z" "(-_-)zz" "(-.-)zzz" "(-_-)zzz"; do
        echo -ne "\r  ${P}$f${R}"
        sleep 0.22
    done
    echo ""
}

kirby_spin() {
    for f in "(>w<)" "(>w>)" "(-w-)" "(<w<)" "(-w-)" "(>w<)"; do
        echo -ne "\r  ${P}$f${R}"
        sleep 0.14
    done
    echo ""
}

kirby_fly_out() {
    for sp in "      " "     " "    " "   " "  " " " ""; do
        echo -ne "\r${P}${sp}~ (>w<)${R}"
        sleep 0.07
    done
    echo ""
}

kirby_excited() {
    for f in "(>w<)!" " (>w<)!" "(>w<)!" "  !!  " "(>w<)!"; do
        echo -ne "\r  ${P}$f${R}"
        sleep 0.15
    done
    echo ""
}

morning_story() {
    type_out "  transmission incoming..." 0.05
    sleep 0.5
    type_out "  source: kirby's cosmic station" 0.04
    sleep 0.3
    echo ""
    kirby_enter
    sleep 0.2
    type_out "  good morning, ${PILOT}." 0.04
    sleep 0.3
    type_out "  kirby has been at the cockpit since sunrise." 0.04
    sleep 0.3
    type_out "  the stars from last night are still visible." 0.04
    sleep 0.4
    echo ""
    kirby_dance "running systems check..."
    sleep 0.2
    type_out "  everything is nominal." 0.04
    sleep 0.2
    type_out "  the galaxy is quiet." 0.04
    sleep 0.2
    type_out "  your mission awaits." 0.04
    sleep 0.4
    echo ""
    stars_in
    type_out "  today's objective: lock in. focus. fly far." 0.04
    sleep 0.3
    type_out "  kirby believes in you, ${PILOT}. poyo." 0.04
}

afternoon_story() {
    type_out "  the sun is at its peak." 0.04
    sleep 0.3
    type_out "  somewhere in the cosmos..." 0.05
    sleep 0.5
    echo ""
    kirby_enter
    sleep 0.2
    type_out "  ${PILOT}. you made it to the afternoon." 0.04
    sleep 0.3
    type_out "  kirby checked your orbit path." 0.04
    sleep 0.2
    type_out "  trajectory: looking good." 0.04
    sleep 0.4
    echo ""
    kirby_spin
    sleep 0.2
    type_out "  the station is warm and humming." 0.04
    sleep 0.2
    type_out "  perfect conditions for deep focus." 0.04
    sleep 0.4
    echo ""
    stars_in
    type_out "  lock in, ${PILOT}. the cosmos is watching." 0.04
    sleep 0.3
    type_out "  kirby has snacks ready. poyo." 0.04
}

evening_story() {
    type_out "  the stars are coming out." 0.04
    sleep 0.4
    type_out "  kirby lights the station beacons..." 0.05
    sleep 0.5
    echo ""
    kirby_enter
    sleep 0.2
    type_out "  evening, ${PILOT}." 0.04
    sleep 0.3
    type_out "  the quiet hours have arrived." 0.04
    sleep 0.3
    type_out "  this is when the best work happens." 0.04
    sleep 0.4
    echo ""
    kirby_dance "setting the vibe..."
    sleep 0.3
    type_out "  lofi is playing softly in the cockpit." 0.04
    sleep 0.2
    type_out "  the galaxy is yours tonight." 0.04
    sleep 0.4
    echo ""
    stars_in
    type_out "  no distractions. just you and the stars." 0.04
    sleep 0.3
    type_out "  kirby will be here. fly well. poyo." 0.04
}

midnight_story() {
    type_out "  signal detected... late night frequency." 0.05
    sleep 0.5
    type_out "  kirby wakes up..." 0.06
    sleep 0.4
    echo ""
    kirby_sleep
    sleep 0.3
    kirby_excited
    sleep 0.2
    type_out "  ${PILOT}?! you're here at this hour?" 0.04
    sleep 0.3
    type_out "  kirby rubs eyes... grabs a star chart." 0.04
    sleep 0.4
    echo ""
    kirby_dance "midnight mode activated!"
    sleep 0.3
    type_out "  the cosmos belongs to the brave." 0.04
    sleep 0.2
    type_out "  legends are written in the quiet hours." 0.04
    sleep 0.4
    echo ""
    stars_in
    type_out "  kirby puts on the lofi. lights dimmed." 0.04
    sleep 0.3
    type_out "  whatever you're building, it matters. poyo." 0.04
}

predawn_story() {
    type_out "  deep space. all systems dim." 0.06
    sleep 0.6
    type_out "  a signal cuts through the dark..." 0.05
    sleep 0.5
    echo ""
    kirby_enter
    sleep 0.3
    type_out "  ${PILOT}..." 0.07
    sleep 0.5
    type_out "  the stars are still out." 0.05
    sleep 0.4
    type_out "  kirby has never seen you sleep." 0.04
    sleep 0.4
    echo ""
    kirby_spin
    sleep 0.2
    type_out "  this kind of dedication is rare." 0.04
    sleep 0.3
    type_out "  the cosmos takes note of those who push on." 0.04
    sleep 0.4
    echo ""
    stars_in
    type_out "  rest when you can. but if you must go on..." 0.04
    sleep 0.3
    type_out "  kirby is with you. always. poyo." 0.04
}

rank_scene() {
    echo ""
    sleep 0.3
    python3 /tmp/kirbs_stats.py 2>/dev/null || echo -e "${A}  rank > Space Cadet  (no sessions yet)${R}"
    echo ""
}

outro() {
    sleep 0.4
    echo ""
    stars_out
    sleep 0.3
    echo -e "${A}  transmission complete${R}"
    sleep 0.3
    kirby_fly_out
    sleep 0.2
    echo ""
}

clear
echo ""

if   [ "$HOUR" -lt 5 ];  then predawn_story
elif [ "$HOUR" -lt 12 ]; then morning_story
elif [ "$HOUR" -lt 17 ]; then afternoon_story
elif [ "$HOUR" -lt 21 ]; then evening_story
else                          midnight_story
fi

rank_scene
outro
