# check_system.py
import os

def validate():
    print("🛠️ Kirby System-Check...")
    required = ['logs', 'data', 'backups']
    for folder in required:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"  ✅ Ordner '{folder}' erstellt.")
    
    # Prüfe ob Sound-Dateien da sind (wichtig für Offline-Vibe)
    if not os.path.exists('kirby_lowfi.mp3'):
        print("  ⚠️ Warnung: Keine Musikdatei gefunden. Musik-Player wird stumm sein.")

if __name__ == "__main__":
    validate()
