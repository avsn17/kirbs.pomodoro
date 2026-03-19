import os, subprocess, time, webbrowser

# -- MASTER VIBE DICTIONARY WITH PLAYLIST IDS --
VIBES = {
    "lana":    {"artist": "Lana Del Rey",     "mood": "idle",    "face": "(◕‿◕)っ", "id": 1},
    "beegees": {"artist": "Bee Gees",        "mood": "done",    "face": "٩(◕‿◕｡)۶", "id": 7},
    "mj":      {"artist": "Michael Jackson", "mood": "working", "face": "(ง •_•)ง", "id": 11},
    "chopin":  {"artist": "Chopin",          "mood": "sleepy",  "face": "(－_－)zZ", "id": 16},
    "billie":  {"artist": "Billie Eilish",   "mood": "hungry",  "face": "(＾་།＾)",  "id": 21},
    "cas":     {"artist": "CAS",             "mood": "idle",    "face": "( ᵕ̈ )っ",  "id": 26},
    "poyo":    {"action": "status",  "face": "★"},
    "wid":     {"action": "reset",   "face": "🔄"},
    "save":    {"action": "cloud",   "face": "☁️"},
    "q":       {"action": "exit",    "face": "✨"}
}

def play_music(playlist_pos):
    # Kill any existing mpv instance to switch tracks cleanly
    subprocess.run("pkill -f mpv", shell=True)
    # Start mpv in the background with randomized playback from the specific start point
    cmd = f"mpv --playlist-start={playlist_pos-1} --shuffle --no-video --volume=60 music_list.txt &"
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def sync(mood, artist="Station", track="Cosmic Mix"):
    os.makedirs("data", exist_ok=True)
    with open("data/now_playing.txt", "w") as f: f.write(f"{artist} - {track}")
    with open("data/kirby_mood.txt", "w") as f: f.write(mood)

os.system('clear')
print("\n    ╭──────────────────────────────────────────╮")
print("    │  ⭐ KIRBY'S COSMIC STATION | v2.0        │")
print("    ╰──────────────────────────────────────────╯\n")

while True:
    try:
        cmd = input("    (•ᴗ•)♪ > ").lower().strip()
        if not cmd: continue
        
        if cmd in VIBES:
            v = VIBES[cmd]
            if "action" in v:
                if v["action"] == "exit": 
                    subprocess.run("pkill -f mpv", shell=True)
                    break
                elif v["action"] == "cloud": subprocess.run("./save", shell=True)
                elif v["action"] == "reset": subprocess.run("pkill -f kirby_desktop.py && xvfb-run -a python3 kirby_desktop.py &", shell=True)
                elif v["action"] == "status":
                    sync("done")
                    print(f"    {v['face']} System Nominal.")
            else:
                print(f"    {v['face']} Tuning into {v['artist']}...")
                sync(v['mood'], v['artist'])
                play_music(v['id'])
        else:
            print("    (•ө•)? Unknown command.")
    except EOFError: break