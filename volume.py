# local_vibe.py
import os
import platform

def set_system_volume(level):
    """Level 0-100 (Funktioniert auf Mac/Linux)"""
    if platform.system() == "Darwin": # Mac
        os.system(f"osascript -e 'set volume output volume {level}'")
    elif platform.system() == "Linux":
        os.system(f"amixer set Master {level}% > /dev/null")

def play_focus_sound():
    # Startet einen lokalen Player im Hintergrund
    print("🎵 Starte lokale Focus-Playlist...")
    os.system("mpv --loop-file=inf data/focus_music.mp3 > /dev/null 2>&1 &")
