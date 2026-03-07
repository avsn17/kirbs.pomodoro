#!/bin/bash
# Erstellt ein Backup der User-Daten

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
mkdir -p "$BACKUP_DIR"

echo "📂 Erstelle Kirby-Backup..."
# Packe data und logs Ordner
tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" data/ logs/ 2>/dev/null

# Behalte nur die letzten 5 Backups (lösche ältere)
ls -t $BACKUP_DIR/backup_*.tar.gz | tail -n +6 | xargs rm -f 2>/dev/null

echo "✅ Backup gespeichert: backup_$TIMESTAMP.tar.gz"
