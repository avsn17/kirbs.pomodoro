import os, subprocess, time, webbrowser

VIBES = {
    "lana":    {"artist": "Lana Del Rey",     "mood": "idle",    "face": "(◕‿◕)っ", "tag": "dreamy"},
    "beegees": {"artist": "Bee Gees",        "mood": "done",    "face": "٩(◕‿◕｡)۶", "tag": "disco"},
    "mj":      {"artist": "Michael Jackson", "mood": "working", "face": "(ง •_•)ง", "tag": "energy"},
    "chopin":  {"artist": "Chopin",          "mood": "sleepy",  "face": "(－_－)zZ", "tag": "calm"},
    "billie":  {"artist": "Billie Eilish",   "mood": "hungry",  "face": "(＾་།＾)",  "tag": "dark"},
    "cas":     {"artist": "CAS",             "mood": "idle",    "face": "( ᵕ̈ )っ",  "tag": "soft"},
    "poyo":    {"action": "status",  "face": "★"},
    "wid":     {"action": "reset",   "face": "🔄"},
    "save":    {"action": "cloud",   "face": "☁️"},
    "q":       {"action": "exit",    "face": "✨"}
}

def sync(mood, artist="Station", track="Active"):
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
                if v["action"] == "exit": break
                elif v["action"] == "cloud": subprocess.run("./save", shell=True)
                elif v["action"] == "reset": subprocess.run("pkill -f kirby_desktop.py && python3 kirby_desktop.py &", shell=True)
                elif v["action"] == "status":
                    sync("done")
                    print(f"    {v['face']} System Nominal.")
            else:
                print(f"    {v['face']} Playing {v['artist']}...")
                sync(v['mood'], v['artist'])
        else:
            print("    (•ө•)? Unknown command.")
    except EOFError: break
