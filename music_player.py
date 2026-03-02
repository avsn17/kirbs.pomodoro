#!/usr/bin/env python3
"""
🎵 COSMIC MUSIC PLAYER
Works in Codespaces — plays music via terminal using yt-dlp + ffmpeg,
or falls back to a pure ASCII visualizer with lofi playlist links.
Reads music_signal.txt for autoplay triggers from the Pomodoro timer.
"""

import os, sys, time, json, random, subprocess, threading, signal
from pathlib import Path

SIGNAL_FILE = Path('music_signal.txt')
HISTORY_FILE = Path('music_history.json')

C = {
    'pink':   '\033[38;5;218m',
    'cyan':   '\033[96m',
    'solar':  '\033[93m',
    'green':  '\033[92m',
    'void':   '\033[90m',
    'bold':   '\033[1m',
    'reset':  '\033[0m',
}

# ── Playlist ──────────────────────────────────────────────────────────────────
# These are YouTube IDs for lofi/focus tracks (no copyright issues for personal use)
PLAYLIST = [
    {"title": "Lofi Hip Hop Radio — beats to relax/study",  "yt": "jfKfPfyJRdk"},
    {"title": "Chillhop Essentials — focus beats",           "yt": "5yx6BWlEVcY"},
    {"title": "Synthwave Radio — cyberpunk vibes",           "yt": "4xDzrJKXOOY"},
    {"title": "Jazz Hop Café — chill jazz",                  "yt": "Dx5qFachd3A"},
    {"title": "Tokyo Lofi Hip Hop",                          "yt": "lTRiuFIWV54"},
    {"title": "Cozy Coffee Shop Ambience",                   "yt": "h2zkV-yZW4s"},
    {"title": "Studio Ghibli Piano Collection",              "yt": "pECGpF5Qyow"},
]

# ── Check tools ───────────────────────────────────────────────────────────────
def check_tool(name):
    return subprocess.run(['which', name], capture_output=True).returncode == 0

HAS_YTDLP  = check_tool('yt-dlp')
HAS_FFPLAY = check_tool('ffplay')
HAS_MPV    = check_tool('mpv')
CAN_PLAY   = HAS_YTDLP and (HAS_FFPLAY or HAS_MPV)

def install_tools():
    """Try to install yt-dlp in Codespaces"""
    print(f"{C['cyan']}Installing yt-dlp...{C['reset']}")
    os.system('pip install yt-dlp --quiet --break-system-packages 2>/dev/null || pip install yt-dlp --quiet')
    print(f"{C['cyan']}Installing ffmpeg...{C['reset']}")
    os.system('sudo apt-get install -y ffmpeg -qq 2>/dev/null')

# ── Player ────────────────────────────────────────────────────────────────────
class CosmicPlayer:
    def __init__(self):
        self.current       = None
        self.track_idx     = 0
        self.playing       = False
        self.proc          = None
        self.history       = self._load_history()
        self._stop_event   = threading.Event()

    def _load_history(self):
        if HISTORY_FILE.exists():
            try: return json.loads(HISTORY_FILE.read_text())
            except: pass
        return []

    def _save_history(self, title):
        self.history.append({"title": title, "ts": time.strftime("%Y-%m-%d %H:%M")})
        HISTORY_FILE.write_text(json.dumps(self.history[-50:], indent=2))  # keep last 50

    def _get_url(self, yt_id):
        return f"https://www.youtube.com/watch?v={yt_id}"

    def play_track(self, track):
        self.stop()
        self.current = track
        self.playing = True
        url = self._get_url(track['yt'])

        print(f"\n{C['pink']}▶ Now Playing: {track['title']}{C['reset']}")
        print(f"{C['void']}  {url}{C['reset']}")

        self._save_history(track['title'])

        if not CAN_PLAY:
            self._show_fallback(url)
            return

        # Build command
        if HAS_MPV:
            cmd = ['mpv', '--no-video', '--really-quiet',
                   f'ytdl://{track["yt"]}']
        elif HAS_YTDLP and HAS_FFPLAY:
            # Get audio stream URL via yt-dlp then pipe to ffplay
            cmd = ['sh', '-c',
                   f'yt-dlp -f bestaudio -g "https://www.youtube.com/watch?v={track["yt"]}" | xargs ffplay -nodisp -autoexit -loglevel quiet']
        else:
            self._show_fallback(url)
            return

        try:
            self.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            threading.Thread(target=self._watch_proc, daemon=True).start()
        except Exception as e:
            print(f"{C['void']}  Playback error: {e}{C['reset']}")
            self._show_fallback(url)

    def _watch_proc(self):
        """Auto-advance to next track when current ends"""
        if self.proc:
            self.proc.wait()
            if self.playing and not self._stop_event.is_set():
                self.next_track()

    def _show_fallback(self, url):
        """Can't play audio — show the link + ASCII art instead"""
        print(f"\n{C['solar']}  🎵 Open this link to listen:{C['reset']}")
        print(f"  {C['cyan']}{url}{C['reset']}")
        print(f"\n{C['void']}  (Install mpv for terminal playback: sudo apt-get install mpv){C['reset']}")
        self._ascii_visualizer()

    def _ascii_visualizer(self):
        """Purely visual — animated bars to simulate playing"""
        frames = 0
        bars = 12
        print()
        try:
            while self.playing and frames < 50:
                heights = [random.randint(1, 8) for _ in range(bars)]
                viz = ''.join(['█' * h + ' ' for h in heights])
                sys.stdout.write(f"\r  {C['pink']}{viz}{C['reset']}  ♪")
                sys.stdout.flush()
                time.sleep(0.3)
                frames += 1
        except KeyboardInterrupt:
            pass
        print()

    def stop(self):
        self.playing = False
        if self.proc:
            try:
                self.proc.terminate()
                self.proc = None
            except: pass

    def next_track(self):
        self.track_idx = (self.track_idx + 1) % len(PLAYLIST)
        self.play_track(PLAYLIST[self.track_idx])

    def prev_track(self):
        self.track_idx = (self.track_idx - 1) % len(PLAYLIST)
        self.play_track(PLAYLIST[self.track_idx])

    def random_track(self):
        self.track_idx = random.randint(0, len(PLAYLIST) - 1)
        self.play_track(PLAYLIST[self.track_idx])

    def show_playlist(self):
        print(f"\n{C['solar']}{C['bold']}🎵 COSMIC PLAYLIST{C['reset']}")
        print("─" * 50)
        for i, t in enumerate(PLAYLIST):
            marker = f"{C['pink']}▶{C['reset']}" if i == self.track_idx else " "
            print(f"  {marker} [{i+1}] {t['title']}")
        print()

    def show_history(self):
        print(f"\n{C['cyan']}{C['bold']}📻 RECENTLY PLAYED{C['reset']}")
        print("─" * 50)
        if not self.history:
            print("  Nothing yet.")
        for entry in self.history[-10:]:
            print(f"  {C['void']}{entry['ts']}{C['reset']}  {entry['title']}")
        print()

# ── Signal watcher ────────────────────────────────────────────────────────────
def watch_signal(player):
    """Background thread — watches music_signal.txt for triggers from pomodoro"""
    print(f"{C['void']}  Watching for pomodoro signal...{C['reset']}")
    while True:
        try:
            if SIGNAL_FILE.exists():
                content = SIGNAL_FILE.read_text().strip()
                if content in ('PLAY_NEXT', 'toggle'):
                    SIGNAL_FILE.write_text('')   # clear signal
                    if not player.playing:
                        print(f"\n{C['pink']}🍅 Pomodoro complete! Auto-playing music...{C['reset']}")
                        player.random_track()
                    else:
                        player.next_track()
                elif content == 'pause':
                    SIGNAL_FILE.write_text('')
                    player.stop()
                    print(f"{C['void']}  Music paused by timer.{C['reset']}")
        except Exception:
            pass
        time.sleep(1)

# ── Main UI ───────────────────────────────────────────────────────────────────
def main():
    print(f"\n{C['pink']}{C['bold']}  ♪ COSMIC MUSIC PLAYER ♪{C['reset']}")
    print(f"  {C['void']}Paired with Cosmic Pomodoro Timer{C['reset']}\n")

    # Auto-install if needed
    if not HAS_YTDLP:
        print(f"{C['solar']}  yt-dlp not found.{C['reset']}")
        ch = input("  Install now for audio playback? (y/n): ").strip().lower()
        if ch == 'y':
            install_tools()
        else:
            print(f"  {C['void']}Running in link-display mode.{C['reset']}\n")

    player = CosmicPlayer()

    # Start signal watcher
    threading.Thread(target=watch_signal, args=(player,), daemon=True).start()

    # Ensure signal file exists
    if not SIGNAL_FILE.exists():
        SIGNAL_FILE.write_text('')

    print(f"  {C['green']}Commands: [P] Play  [N] Next  [B] Back  [R] Random")
    print(f"  [L] Playlist  [H] History  [S] Stop  [Q] Quit{C['reset']}\n")

    player.show_playlist()

    while True:
        try:
            cmd = input(f"{C['pink']}♪ > {C['reset']}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if cmd in ('p', 'play', ''):
            player.play_track(PLAYLIST[player.track_idx])
        elif cmd in ('n', 'next'):
            player.next_track()
        elif cmd in ('b', 'back', 'prev'):
            player.prev_track()
        elif cmd in ('r', 'random'):
            player.random_track()
        elif cmd in ('s', 'stop'):
            player.stop()
            print(f"  {C['void']}Stopped.{C['reset']}")
        elif cmd in ('l', 'list', 'playlist'):
            player.show_playlist()
        elif cmd in ('h', 'history'):
            player.show_history()
        elif cmd in ('q', 'quit'):
            break
        elif cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(PLAYLIST):
                player.track_idx = idx
                player.play_track(PLAYLIST[idx])
            else:
                print(f"  {C['void']}Track {cmd} not found.{C['reset']}")
        else:
            print(f"  {C['void']}Unknown command. Try P, N, B, R, L, H, S, Q or a track number.{C['reset']}")

    player.stop()
    print(f"\n{C['pink']}  Goodbye, Cosmic Kirbs. 🎵{C['reset']}\n")

if __name__ == "__main__":
    main()