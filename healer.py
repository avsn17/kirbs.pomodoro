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
        pass  # music file optional

if __name__ == "__main__":
    validate()
