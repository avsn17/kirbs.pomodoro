#!/usr/bin/env python3
"""
🌟 KIRBY'S MUSIC STAR 🌟
A cute Kirby-themed terminal music player!
Plays music via yt-dlp + mpv/ffplay/afplay (Mac).
Reads music_signal.txt for autoplay triggers from the Pomodoro timer.
"""

import os
import sys
import time
import json
import random
import subprocess
import threading
from pathlib import Path

SIGNAL_FILE  = Path("music_signal.txt")
HISTORY_FILE = Path("music_history.json")

# ── Colors ─────────────────────────────────────────────────────────────────────
C = {
    "pink":     "\033[38;5;218m",
    "hotpink":  "\033[38;5;205m",
    "star":     "\033[38;5;228m",
    "sky":      "\033[38;5;117m",
    "mint":     "\033[38;5;121m",
    "lavender": "\033[38;5;183m",
    "peach":    "\033[38;5;223m",
    "void":     "\033[38;5;240m",
    "white":    "\033[97m",
    "bold":     "\033[1m",
    "reset":    "\033[0m",
}

# ── Kirby dance frames ─────────────────────────────────────────────────────────
KIRBY_DANCE = [
    ["  (\\(\\   ", "  ( ^ᴗ^) ♪", "  ＼(  )   ", "   (_)_)  "],
    ["  (/)(/) ", "  (ᵕ̈   ) ♫", "   (  )/  ",  "   (_)_)  "],
    ["  (\\(\\   ", "  ( •ω•) ♪", "   (  )＼  ", "   (_)_)  "],
    ["  (/)(/) ", "  ( ᗒᗨᗕ) ♫", "  ＼(  )   ", "   (_)_)  "],
]

KIRBY_STAR_ART = """
       ★彡
    (\\(\\  彡★
    ( •ᴗ•) ★
    (つ★つ彡
     (  )
     |__|
"""

# ── Playlist (artists only) ────────────────────────────────────────────────────
PLAYLIST = [
    # 🌹 Lana Del Rey
    {"title": "Summertime Sadness",            "artist": "Lana Del Rey",    "yt": "TdrL3QxjyVw"},
    {"title": "Young and Beautiful",           "artist": "Lana Del Rey",    "yt": "domMDtbODaY"},
    {"title": "Video Games",                   "artist": "Lana Del Rey",    "yt": "J4-6VYiTBE0"},
    {"title": "Born To Die",                   "artist": "Lana Del Rey",    "yt": "Bag1gUxuU0g"},
    {"title": "Blue Jeans",                    "artist": "Lana Del Rey",    "yt": "9YGiAHuZCNc"},
    {"title": "Ride",                          "artist": "Lana Del Rey",    "yt": "oUCmmN3dPZg"},
    # 🕺 Bee Gees
    {"title": "Stayin' Alive",                 "artist": "Bee Gees",        "yt": "I_izvAbhExY"},
    {"title": "Night Fever",                   "artist": "Bee Gees",        "yt": "hA5VH2vJBls"},
    {"title": "How Deep Is Your Love",         "artist": "Bee Gees",        "yt": "XpqqjU7u5Yc"},
    {"title": "More Than a Woman",             "artist": "Bee Gees",        "yt": "UgKMCJnzoS8"},
    # 🎤 Michael Jackson
    {"title": "Thriller",                      "artist": "Michael Jackson", "yt": "sOnqjkJTMaA"},
    {"title": "Billie Jean",                   "artist": "Michael Jackson", "yt": "Zi_XLOBDo_Y"},
    {"title": "Beat It",                       "artist": "Michael Jackson", "yt": "oRdxUFDoQe0"},
    {"title": "Man in the Mirror",             "artist": "Michael Jackson", "yt": "PivWY9wn5ps"},
    {"title": "Speed Demon",                   "artist": "Michael Jackson", "yt": "1CFP9bPnN_I"},
    # 🎹 Chopin
    {"title": "Nocturne Op. 9 No. 2",          "artist": "Chopin",          "yt": "9E6b3swbnWg"},
    {"title": "Ballade No. 1 in G minor",      "artist": "Chopin",          "yt": "VmFmAvwAOXI"},
    {"title": "Fantasie Impromptu",            "artist": "Chopin",          "yt": "tvm2ZsRv3Zs"},
    {"title": "Raindrop Prelude Op. 28 No. 15","artist": "Chopin",          "yt": "XeX4X_1_lo0"},
    {"title": "Waltz in C-sharp minor",        "artist": "Chopin",          "yt": "X1mECSPKvbE"},
    # 🖤 Billie Eilish
    {"title": "bad guy",                       "artist": "Billie Eilish",   "yt": "DyDfgMOUjCI"},
    {"title": "Ocean Eyes",                    "artist": "Billie Eilish",   "yt": "viimfQi_pUw"},
    {"title": "You Should See Me in a Crown",  "artist": "Billie Eilish",   "yt": "ao_XfSMDYME"},
    {"title": "lovely (with Khalid)",          "artist": "Billie Eilish",   "yt": "akjqkZAFgcA"},
    {"title": "Happier Than Ever",             "artist": "Billie Eilish",   "yt": "5GJWxDKyk3A"},
    # ✨ CAS
    {"title": "I Am a Dreamer",                "artist": "CAS",             "yt": "VuNIsY6JdUw"},
    {"title": "Thinking of You",               "artist": "CAS",             "yt": "dVXMKtYyGnI"},
]

ARTIST_COLORS = {
    "Lana Del Rey":    C["hotpink"],
    "Bee Gees":        C["star"],
    "Michael Jackson": C["sky"],
    "Chopin":          C["lavender"],
    "Billie Eilish":   C["void"],
    "CAS":             C["mint"],
}
ARTIST_ICONS = {
    "Lana Del Rey":    "🌹",
    "Bee Gees":        "🕺",
    "Michael Jackson": "🎤",
    "Chopin":          "🎹",
    "Billie Eilish":   "🖤",
    "CAS":             "✨",
}
ARTIST_VIBES = {
    "Lana Del Rey":    "dreamy & cinematic",
    "Bee Gees":        "disco fever ★",
    "Michael Jackson": "legendary pop",
    "Chopin":          "romantic classical",
    "Billie Eilish":   "dark & ethereal",
    "CAS":             "soft indie dream",
}
KIRBY_ARTIST_FACE = {
    "Lana Del Rey":    "🌹 ( •ᴗ•) 🌹",
    "Bee Gees":        "🕺 (ᗒᗨᗕ) 🕺",
    "Michael Jackson": "🎤 ( •ω•) 🎤",
    "Chopin":          "🎹 ( -ω-) 🎹",
    "Billie Eilish":   "🖤 ( •̀ᴗ•́) 🖤",
    "CAS":             "✨ ( ᵕ̈ ) ✨",
}

# ── Tool detection ─────────────────────────────────────────────────────────────
def check_tool(name: str) -> bool:
    return subprocess.run(["which", name], capture_output=True).returncode == 0

def detect_player():
    has_ytdlp  = check_tool("yt-dlp")
    has_mpv    = check_tool("mpv")
    has_ffplay = check_tool("ffplay")
    if has_mpv    and has_ytdlp: return "mpv"
    if has_ffplay and has_ytdlp: return "ffplay"
    if check_tool("afplay") and has_ytdlp: return "afplay"
    return None

PLAYER = detect_player()

def install_tools():
    print(f"\n  {C['pink']}(>•ᴗ•)> Installing yt-dlp for Kirby!{C['reset']}")
    os.system(
        "pip install yt-dlp --quiet --break-system-packages 2>/dev/null "
        "|| pip3 install yt-dlp --quiet 2>/dev/null "
        "|| brew install yt-dlp 2>/dev/null"
    )
    if not check_tool("mpv") and not check_tool("ffplay"):
        print(f"  {C['star']}Kirby needs an audio player too!")
        print(f"  Mac:        brew install mpv")
        print(f"  Codespaces: sudo apt-get install -y mpv{C['reset']}")

# ── Kirby UI helpers ───────────────────────────────────────────────────────────
def kirby_spin(message: str, duration: float = 1.0):
    """Kirby spins while loading."""
    frames = ["(>•ᴗ•)>", "<(•ᴗ•<)", "(>•ᴗ•)>", "^(•ᴗ•)^"]
    stars  = ["★", "✦", "⭐", "✧"]
    end_t  = time.time() + duration
    i = 0
    while time.time() < end_t:
        f = frames[i % 4]
        s = stars[i % 4]
        sys.stdout.write(f"\r  {C['pink']}{f}{C['reset']} {C['star']}{s}{C['reset']} {message}  ")
        sys.stdout.flush()
        time.sleep(0.18)
        i += 1
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()

def draw_header():
    print(f"\n{C['pink']}{C['bold']}")
    print("  ✦·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·✦")
    print("  ✦                                       ✦")
    print(f"  ✦    {C['star']}(\\(\\{C['pink']}                             ✦")
    print(f"  ✦    {C['star']}( •ᴗ•){C['pink']}  ★ KIRBY'S MUSIC STAR ★   ✦")
    print(f"  ✦    {C['star']}(つ🌟つ{C['pink']}   dreamland radio player  ✦")
    print("  ✦                                       ✦")
    print("  ✦·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·✦")
    print(f"{C['reset']}")

def draw_now_playing(track: dict):
    artist = track["artist"]
    col    = ARTIST_COLORS.get(artist, C["pink"])
    icon   = ARTIST_ICONS.get(artist, "♪")
    face   = KIRBY_ARTIST_FACE.get(artist, "( •ᴗ•)")
    vibe   = ARTIST_VIBES.get(artist, "")
    sep    = f"{C['pink']}  ·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·{C['reset']}"
    print(f"\n{sep}")
    print(f"  {C['star']}{C['bold']} ♪ NOW PLAYING ♪{C['reset']}")
    print(f"  {col}{C['bold']}{icon}  {artist}{C['reset']}  {C['void']}{vibe}{C['reset']}")
    print(f"  {C['peach']}🎵 {track['title']}{C['reset']}")
    print(f"  {col}{face}{C['reset']}")
    print(f"{sep}\n")

def draw_commands():
    print(f"  {C['star']}{C['bold']}✦ Commands ✦{C['reset']}")
    rows = [
        (["P","play"],   "play current"),
        (["N","next"],   "next track"),
        (["B","back"],   "previous"),
        (["R","random"], "surprise! ★"),
        (["S","stop"],   "stop"),
        (["L","list"],   "show playlist"),
        (["H","history"],"listening diary"),
        (["Q","quit"],   "goodbye~"),
        (["1-27"],       "play by number"),
    ]
    shortcuts = [
        ("lana",    "Lana Del Rey"),
        ("beegees", "Bee Gees"),
        ("mj",      "Michael Jackson"),
        ("chopin",  "Chopin"),
        ("billie",  "Billie Eilish"),
        ("cas",     "CAS"),
    ]
    for keys, desc in rows:
        key_str = "/".join(keys)
        print(f"  {C['pink']}[{key_str}]{C['reset']} {C['peach']}{desc}{C['reset']}")
    print(f"\n  {C['void']}Artist shortcuts:{C['reset']}")
    for k, v in shortcuts:
        print(f"  {C['pink']}[{k}]{C['reset']} {C['void']}{v}{C['reset']}")
    print()

# ── Player ─────────────────────────────────────────────────────────────────────
class KirbyPlayer:
    def __init__(self):
        self.current   = None
        self.track_idx = 0
        self.playing   = False
        self.proc      = None
        self.history   = self._load_history()
        self._stop_evt = threading.Event()
        self._lock     = threading.Lock()

    def _load_history(self):
        if HISTORY_FILE.exists():
            try:    return json.loads(HISTORY_FILE.read_text())
            except: pass
        return []

    def _save_history(self, title: str):
        self.history.append({"title": title, "ts": time.strftime("%Y-%m-%d %H:%M")})
        try:
            HISTORY_FILE.write_text(json.dumps(self.history[-50:], indent=2))
        except Exception:
            pass

    @staticmethod
    def _yt_url(yt_id: str) -> str:
        return f"https://www.youtube.com/watch?v={yt_id}"

    def play_track(self, track: dict):
        self.stop()
        self._stop_evt.clear()
        with self._lock:
            self.current = track
            self.playing = True

        url = self._yt_url(track["yt"])
        draw_now_playing(track)
        print(f"  {C['void']}{url}{C['reset']}\n")
        self._save_history(f"{track['artist']} — {track['title']}")

        global PLAYER
        if PLAYER is None:
            PLAYER = detect_player()
        if PLAYER is None:
            self._show_fallback(url)
            return

        try:
            cmd = self._build_cmd(track, PLAYER)
            self.proc = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            threading.Thread(target=self._watch_proc, daemon=True).start()
        except Exception as exc:
            print(f"  {C['void']}Playback error: {exc}{C['reset']}")
            self._show_fallback(url)

    @staticmethod
    def _build_cmd(track: dict, player: str) -> list:
        yt_id = track["yt"]
        url   = f"https://www.youtube.com/watch?v={yt_id}"
        if player == "mpv":
            return ["mpv", "--no-video", "--really-quiet", f"ytdl://{yt_id}"]
        if player == "ffplay":
            return ["sh", "-c",
                f'yt-dlp -f bestaudio -g "{url}" | xargs ffplay -nodisp -autoexit -loglevel quiet']
        if player == "afplay":
            tmp = f"/tmp/kirby_{yt_id}.m4a"
            return ["sh", "-c",
                f'yt-dlp -f bestaudio -o "{tmp}" "{url}" -q && afplay "{tmp}"; rm -f "{tmp}"']
        raise ValueError(f"Unknown player: {player}")

    def _watch_proc(self):
        if self.proc:
            self.proc.wait()
        if self.playing and not self._stop_evt.is_set():
            self.next_track()

    def _show_fallback(self, url: str):
        print(f"  {C['star']}🌟 Kirby found your link! Open it to listen:{C['reset']}")
        print(f"  {C['sky']}{url}{C['reset']}")
        print(f"\n  {C['void']}Mac tip:    brew install mpv yt-dlp")
        print(f"  Codespaces: sudo apt-get install -y mpv && pip install yt-dlp{C['reset']}\n")
        self._kirby_visualizer()

    def _kirby_visualizer(self):
        """Kirby dances since we can't play audio."""
        notes  = ["♩", "♪", "♫", "♬", "🎵", "🎶"]
        colors = [C["pink"], C["hotpink"], C["star"], C["sky"], C["lavender"], C["mint"]]
        frame  = 0
        try:
            while self.playing and frame < 80:
                d     = KIRBY_DANCE[frame % 4]
                nl    = notes[frame % len(notes)]
                nr    = notes[(frame + 2) % len(notes)]
                col   = colors[frame % len(colors)]
                if frame > 0:
                    sys.stdout.write("\033[4A")
                for line in d:
                    sys.stdout.write(f"\r  {col}{line}{C['reset']}  {nl} {nr}\n")
                sys.stdout.flush()
                time.sleep(0.35)
                frame += 1
        except KeyboardInterrupt:
            pass
        print()

    def stop(self):
        self._stop_evt.set()
        with self._lock:
            self.playing = False
        if self.proc:
            try:    self.proc.terminate()
            except: pass
            self.proc = None

    def next_track(self):
        self.track_idx = (self.track_idx + 1) % len(PLAYLIST)
        self.play_track(PLAYLIST[self.track_idx])

    def prev_track(self):
        self.track_idx = (self.track_idx - 1) % len(PLAYLIST)
        self.play_track(PLAYLIST[self.track_idx])

    def random_track(self):
        self.track_idx = random.randint(0, len(PLAYLIST) - 1)
        self.play_track(PLAYLIST[self.track_idx])

    def show_playlist(self, filter_artist: str = None):
        grouped: dict = {}
        for i, t in enumerate(PLAYLIST):
            if filter_artist and filter_artist.lower() not in t["artist"].lower():
                continue
            grouped.setdefault(t["artist"], []).append((i, t))

        print(f"\n{C['star']}{C['bold']}  ✦ KIRBY'S DREAMLAND PLAYLIST ✦{C['reset']}")
        print(f"  {C['pink']}·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·{C['reset']}")

        for artist, tracks in grouped.items():
            col  = ARTIST_COLORS.get(artist, C["pink"])
            icon = ARTIST_ICONS.get(artist, "♪")
            vibe = ARTIST_VIBES.get(artist, "")
            face = KIRBY_ARTIST_FACE.get(artist, "( •ᴗ•)")
            print(f"\n  {col}{C['bold']}{icon} {artist}{C['reset']}  {C['void']}{vibe}{C['reset']}")
            print(f"  {col}{face}{C['reset']}")
            for i, t in tracks:
                if i == self.track_idx:
                    marker = f"{C['hotpink']}▶ {C['reset']}"
                    badge  = f" {C['star']}★{C['reset']}"
                else:
                    marker = "  "
                    badge  = ""
                print(f"    {marker}{C['void']}[{i+1:02d}]{C['reset']} {t['title']}{badge}")

        print(f"\n  {C['pink']}·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·{C['reset']}\n")

    def show_history(self):
        print(f"\n{C['star']}{C['bold']}  ✦ KIRBY'S LISTENING DIARY ✦{C['reset']}")
        print(f"  {C['pink']}·:·:·:·:·:·:·:·:·:·:·{C['reset']}")
        if not self.history:
            print(f"  {C['void']}( -ᴗ-) zzz  Nothing yet... Kirby is sleepy.{C['reset']}")
        else:
            for entry in self.history[-10:]:
                print(f"  {C['void']}{entry['ts']}{C['reset']}  {C['peach']}{entry['title']}{C['reset']}")
        print()


# ── Signal watcher ─────────────────────────────────────────────────────────────
def watch_signal(player: KirbyPlayer):
    while True:
        try:
            if SIGNAL_FILE.exists():
                content = SIGNAL_FILE.read_text().strip()
                if content in ("PLAY_NEXT", "toggle"):
                    SIGNAL_FILE.write_text("")
                    if not player.playing:
                        print(f"\n  {C['pink']}🍅 Pomodoro done! Kirby brings music~ (>•ᴗ•)>{C['reset']}")
                        player.random_track()
                    else:
                        player.next_track()
                elif content == "pause":
                    SIGNAL_FILE.write_text("")
                    player.stop()
                    print(f"  {C['void']}( -ᴗ-) zzz  Kirby takes a nap...{C['reset']}")
        except Exception:
            pass
        time.sleep(1)


# ── Artist shortcut map ────────────────────────────────────────────────────────
ARTIST_CMDS = {
    ("lana",):                       "Lana Del Rey",
    ("beegees", "bee gees", "bee"):  "Bee Gees",
    ("mj", "michael", "jackson"):    "Michael Jackson",
    ("chopin",):                     "Chopin",
    ("billie", "eilish"):            "Billie Eilish",
    ("cas",):                        "CAS",
}


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    draw_header()

    if not check_tool("yt-dlp"):
        print(f"  {C['star']}(>•ᴗ•)> Kirby needs yt-dlp to play music!{C['reset']}")
        ch = input(f"  {C['pink']}Install now? (y/n): {C['reset']}").strip().lower()
        if ch == "y":
            install_tools()
        else:
            print(f"  {C['void']}Running in link-display mode~ ( •ᴗ•){C['reset']}\n")

    player = KirbyPlayer()
    SIGNAL_FILE.touch(exist_ok=True)
    threading.Thread(target=watch_signal, args=(player,), daemon=True).start()

    draw_commands()
    player.show_playlist()

    while True:
        try:
            cmd = input(f"  {C['pink']}(•ᴗ•)♪ > {C['reset']}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if cmd in ("p", "play", ""):
            kirby_spin("Kirby loads your song...", 0.8)
            player.play_track(PLAYLIST[player.track_idx])
        elif cmd in ("n", "next"):
            kirby_spin("Next track!", 0.5)
            player.next_track()
        elif cmd in ("b", "back", "prev"):
            kirby_spin("Going back!", 0.5)
            player.prev_track()
        elif cmd in ("r", "random"):
            kirby_spin("Kirby picks a surprise ★", 0.8)
            player.random_track()
        elif cmd in ("s", "stop"):
            player.stop()
            print(f"  {C['lavender']}( -ᴗ-) zzz  Kirby rests...{C['reset']}")
        elif cmd in ("l", "list", "playlist"):
            player.show_playlist()
        elif cmd in ("h", "history"):
            player.show_history()
        elif cmd in ("q", "quit"):
            break
        elif cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(PLAYLIST):
                player.track_idx = idx
                kirby_spin("Kirby loads your song...", 0.6)
                player.play_track(PLAYLIST[idx])
            else:
                print(f"  {C['void']}(>ᴗ<) Kirby can't find track {cmd}!{C['reset']}")
        else:
            matched = False
            for aliases, artist in ARTIST_CMDS.items():
                if cmd in aliases:
                    player.show_playlist(artist)
                    matched = True
                    break
            if not matched:
                print(f"  {C['void']}(>ᴗ<) Kirby doesn't know that~ Try P, N, B, R, L, H, S, Q or a number!{C['reset']}")

    player.stop()
    print(f"\n{C['star']}{KIRBY_STAR_ART}{C['reset']}")
    print(f"  {C['pink']}{C['bold']}Bye bye! Kirby loves you~ 🌟{C['reset']}\n")


if __name__ == "__main__":
    main()