#!/bin/bash
PINK='\033[1;35m'
NC='\033[0m'

echo -e "${PINK}✨ Kirby-OS wird initialisiert...${NC}"
mkdir -p logs data backups templates

# Organizer
mv *.log logs/ 2>/dev/null
mv *.json data/ 2>/dev/null

# Einfaches Web-Interface erstellen, falls weg
if [ ! -f "templates/index.html" ]; then
    echo "<html><body style='background:pink;text-align:center;font-family:sans-serif;'><h1>(っ^‿^)っ Kirby Web Hub</h1><p>Poyo! Dein Timer läuft.</p></body></html>" > templates/index.html
fi

# Backup-Skript Dummy erstellen, falls es fehlt
if [ ! -f "kirby_backup.sh" ]; then
    echo "#!/bin/bash" > kirby_backup.sh
    echo "tar -czf backups/backup_\$(date +%F_%H-%M).tar.gz data/ logs/ 2>/dev/null" >> kirby_backup.sh
    chmod +x kirby_backup.sh
fi

./kirby_backup.sh

echo -e "${PINK}🌐 Starte Web-Interface (Docker)...${NC}"
docker compose up -d --build 2>/dev/null || python3 web_app.py &

echo -e "${PINK}🖥️ Starte Desktop-Suite...${NC}"
python3 music_player.py > logs/music.log 2>&1 &
PID_MUSIC=$!
python3 timetodime2/pomodoro_y2k.py > logs/timer.log 2>&1 &
PID_TIMER=$!
python3 timetodime2/kirby_widget.py > logs/widget.log 2>&1 &
PID_WIDGET=$!

echo -e "${PINK}🚀 ALLES BEREIT! (STRG+C zum Beenden)${NC}"

trap "kill $PID_MUSIC $PID_TIMER $PID_WIDGET; docker compose down 2>/dev/null; exit" INT TERM EXIT
wait
