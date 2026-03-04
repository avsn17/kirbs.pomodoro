#!/bin/bash
# Kirby-OS Bootloader
PINK='\033[1;35m'
NC='\033[0m'

echo -e "${PINK}🚀 Poyo! Kirby-OS wird deployed...${NC}"

# Backup der alten Stats falls vorhanden
if [ -f "data/kirby_stats.json" ]; then
    cp data/kirby_stats.json backups/stats_backup_$(date +%F).json
fi

# Starte die Web-App im Hintergrund
nohup python3 web_app.py > logs/web_server.log 2>&1 &
PID=$!

echo -e "${PINK}✨ System ist ONLINE!${NC}"
echo -e "🔗 URL: http://localhost:5000"
echo -e "📝 Logs: tail -f logs/web_server.log"
echo -e "🛑 Stoppen mit: kill $PID"

# Zeige die Logs kurz an
sleep 2
tail -n 5 logs/web_server.log
