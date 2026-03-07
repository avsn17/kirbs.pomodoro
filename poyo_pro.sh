#!/bin/bash
# --- START ---
clear
python3 check_system.py # Dein Organizer

# 1. Backup beim Start ausführen
./kirby_backup.sh

# 2. Willkommens-Popup
python3 -c "import kirby_notify; kirby_notify.send_poyo('Kirby OS', 'System gestartet! Viel Erfolg beim Einsaugen! 🌟')"

# 3. Hintergrund-Prozesse starten
python3 music_player.py > logs/music.log 2>&1 &
PID_MUSIC=$!
python3 timetodime2/pomodoro_y2k.py > logs/timer.log 2>&1 &
PID_TIMER=$!
python3 timetodime2/kirby_widget.py > logs/widget.log 2>&1 &
PID_WIDGET=$!

echo -e "\033[1;35m(⪧ •◡• ⪧) <( System läuft! )\033[0m"

# 4. Cleanup & End-Popup bei STRG+C
trap "
    echo -e '\nStopping...'; 
    kill $PID_MUSIC $PID_TIMER $PID_WIDGET; 
    python3 -c 'import kirby_notify; kirby_notify.send_poyo(\"Kirby OS\", \"Feierabend! Alles sicher gespeichert. ✨\")'; 
    ./kirby_backup.sh; 
    exit" INT TERM EXIT

wait
