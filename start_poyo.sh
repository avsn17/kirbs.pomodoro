#!/bin/bash
# ─────────────────────────────────────────────────────────────
#  Kirby-OS Bootloader
# ─────────────────────────────────────────────────────────────
PINK='\033[1;35m'
NC='\033[0m'
PID_FILE="logs/kirby.pid"
PORT="${PORT:-5000}"

echo -e "${PINK}🚀 Poyo! Kirby-OS wird deployed...${NC}"

# FIX: create required directories before any read/write attempt
mkdir -p data logs backups

# FIX: check if already running on the target port to avoid silent double-start
if lsof -iTCP:"$PORT" -sTCP:LISTEN -t &>/dev/null; then
    echo -e "⚠️  Port $PORT ist bereits belegt — Kirby-OS läuft möglicherweise schon."
    echo -e "    Stoppen mit: kill \$(cat $PID_FILE) oder lsof -ti:$PORT | xargs kill"
    exit 1
fi

# Backup existing stats
if [ -f "data/kirby_stats.json" ]; then
    cp data/kirby_stats.json "backups/stats_backup_$(date +%F).json"
    echo "💾 Stats gesichert → backups/stats_backup_$(date +%F).json"
fi

# Start the web app
nohup python3 web_app.py > logs/web_server.log 2>&1 &
APP_PID=$!

# FIX: save PID to file so it can be killed even after this terminal closes
echo "$APP_PID" > "$PID_FILE"

echo -e "${PINK}✨ System ist ONLINE! (PID: $APP_PID)${NC}"
echo -e "🔗 URL:    http://localhost:$PORT"
echo -e "📝 Logs:   tail -f logs/web_server.log"
echo -e "🛑 Stoppen: kill \$(cat $PID_FILE)"

# FIX: wait for the server to actually start before tailing logs
echo -e "\n⏳ Warte auf Server-Start..."
for i in {1..10}; do
    if lsof -iTCP:"$PORT" -sTCP:LISTEN -t &>/dev/null; then
        echo -e "${PINK}✅ Server antwortet auf Port $PORT${NC}"
        break
    fi
    sleep 1
done

echo -e "\n── Letzte Log-Zeilen ──────────────────────────────────────"
tail -n 8 logs/web_server.log
