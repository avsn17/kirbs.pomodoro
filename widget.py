#!/usr/bin/env python3
"""
🛰️ COSMIC WIDGET — Terminal Notification System
Run this in a SECOND terminal split alongside the Pomodoro timer.
Shows live status, Kirby animations, session notifications, and music state.

Usage:
  # Split your terminal (Ctrl+Shift+5 in Codespaces), then:
  python3 widget.py
"""

import os, sys, time, json, random, signal
from pathlib import Path
from datetime import datetime

SIGNAL_FILE  = Path('music_signal.txt')
STATS_FILE   = Path.home() / '.pomodoro_stats.json'
HISTORY_FILE = Path('music_history.json')

C = {
    'pink':   '\033[38;5;218m',
    'cyan':   '\033[96m',
    'solar':  '\033[93m',
    'green':  '\033[92m',
    'void':   '\033[90m',
    'red':    '\033[91m',
    'bold':   '\033[1m',
    'reset':  '\033[0m',
}

KIRBY_FRAMES = [
    "<( \" )>",
    "<( ' )>",
    "<( ^ )>",
    "<( o )>",
    "(> \" <)",
    "<( * )>",
]

KIRBY_MOODS = {
    'idle':     ["<( \" )>  *waiting*",      "<(  -  )>  zzzz",    "(> o <)  ..."],
    'active':   ["<( ! )>  GO GO GO!",       "(> ^ <) *poyo*",     "<( \" )>  LFG!!"],
    'complete': ["<( * )>  MISSION DONE!!",  "(> V <)  YESSS!",   "<( ^ )>  POYO!!"],
    'paused':   ["<(  - )>  taking a breath","<( . )>  hmm...",    "<( _ )>  resting"],
}

NOTIFICATIONS = [
    "💧 Hydration check — drink some water!",
    "👀 Look away from the screen for 20 seconds.",
    "🧘 Take a deep breath.",
    "🚶 Stand up and stretch!",
    "💪 You're doing amazing, Cosmic Kirbs.",
    "🌟 Stay focused — the stars are watching.",
    "☕ How's your energy? Maybe a quick snack.",
    "🎵 Music fuels the mission.",
]


class CosmicWidget:
    def __init__(self):
        self.running        = True
        self.last_signal    = ''
        self.session_active = False
        self.frame_idx      = 0
        self.notif_timer    = 0
        self.notif_interval = 300   # seconds between reminders (5 min default)
        self.last_notif     = ''
        self.start_time     = time.time()
        self.session_start  = None

        signal.signal(signal.SIGINT, self._exit)
        signal.signal(signal.SIGTERM, self._exit)

    def _exit(self, *_):
        self.running = False
        sys.stdout.write("\033[?25h\033[0m\n")   # restore cursor + reset color
        sys.stdout.flush()
        sys.exit(0)

    def _clear(self):
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()

    def _load_stats(self):
        try:
            if STATS_FILE.exists():
                return json.loads(STATS_FILE.read_text())
        except Exception:
            pass
        return {}

    def _load_last_music(self):
        try:
            if HISTORY_FILE.exists():
                h = json.loads(HISTORY_FILE.read_text())
                if h: return h[-1]['title']
        except Exception:
            pass
        return None

    def _read_signal(self):
        try:
            if SIGNAL_FILE.exists():
                return SIGNAL_FILE.read_text().strip()
        except Exception:
            pass
        return ''

    def _get_kirby(self, mood='idle'):
        frames = KIRBY_MOODS.get(mood, KIRBY_MOODS['idle'])
        return frames[self.frame_idx % len(frames)]

    def _elapsed_str(self):
        s = int(time.time() - self.start_time)
        h, rem = divmod(s, 3600)
        m, sec = divmod(rem, 60)
        if h:
            return f"{h}h {m:02d}m"
        return f"{m}m {sec:02d}s"

    def _session_str(self):
        if not self.session_start:
            return "—"
        s = int(time.time() - self.session_start)
        m, sec = divmod(s, 60)
        return f"{m:02d}:{sec:02d}"

    def _draw(self):
        try:
            cols, rows = os.get_terminal_size()
        except Exception:
            cols, rows = 60, 30

        w = min(cols, 58)

        signal_val  = self._read_signal()
        stats       = self._load_stats()
        last_music  = self._load_last_music()
        now_str     = datetime.now().strftime("%H:%M:%S")

        # Determine mood from signal
        if signal_val == 'PLAY_NEXT':
            mood = 'complete'
            self.session_active = False
        elif signal_val == 'toggle':
            mood = 'active'
            self.session_active = True
            if not self.session_start:
                self.session_start = time.time()
        elif signal_val == 'pause':
            mood = 'paused'
        elif self.session_active:
            mood = 'active'
        else:
            mood = 'idle'

        kirby = self._get_kirby(mood)

        # Notification logic
        self.notif_timer += 1
        notif = ''
        if self.session_active and self.notif_timer >= self.notif_interval:
            notif = random.choice(NOTIFICATIONS)
            self.last_notif = notif
            self.notif_timer = 0

        # Stats summary
        user_stats = stats.get('Cosmic Kirbs', {})
        total_m    = user_stats.get('total_distance', 0)
        sessions   = user_stats.get('completed_sessions', 0)

        # ── Draw ──────────────────────────────────────────────────────────────
        self._clear()
        sys.stdout.write(C['pink'])

        def line(text='', color=None):
            col = color or C['pink']
            sys.stdout.write(f"{col}  {text}{C['pink']}\n")

        line('┌' + '─' * (w - 4) + '┐')
        line('│' + f"  🛰  COSMIC WIDGET  ✦  {now_str}".center(w - 4) + '│')
        line('├' + '─' * (w - 4) + '┤')

        # Kirby
        line('│' + f"  {kirby}".ljust(w - 4) + '│', C['pink'])

        # Status
        status_icon = {
            'active':   f"{C['green']}▶ SESSION ACTIVE",
            'paused':   f"{C['solar']}⏸ PAUSED",
            'complete': f"{C['cyan']}🎉 MISSION COMPLETE",
            'idle':     f"{C['void']}● IDLE",
        }.get(mood, f"{C['void']}● IDLE")
        line('│' + f"  {status_icon}{C['pink']}".ljust(w + 6) + '│')

        line('├' + '─' * (w - 4) + '┤')

        # Session info
        line('│' + f"  ⏱  Session:   {self._session_str()}".ljust(w - 4) + '│', C['cyan'])
        line('│' + f"  🕐 Uptime:    {self._elapsed_str()}".ljust(w - 4) + '│', C['void'])
        line('│' + f"  🏆 Total:     {total_m:.0f}m  ({sessions} sessions)".ljust(w - 4) + '│', C['solar'])

        if last_music:
            track_short = last_music[:w - 16]
            line('│' + f"  🎵 Last:      {track_short}".ljust(w - 4) + '│', C['void'])

        line('├' + '─' * (w - 4) + '┤')

        # Notification
        if self.last_notif:
            notif_short = self.last_notif[:w - 6]
            line('│' + f"  💬 {notif_short}".ljust(w - 4) + '│', C['solar'])
        else:
            line('│' + f"  💬 Waiting for mission start...".ljust(w - 4) + '│', C['void'])

        # Signal state
        sig_display = signal_val if signal_val else '—'
        line('│' + f"  📡 Signal:    {sig_display}".ljust(w - 4) + '│', C['void'])

        line('└' + '─' * (w - 4) + '┘')

        line()
        line(f"  Ctrl+C to exit widget", C['void'])

        sys.stdout.write(C['reset'])
        sys.stdout.flush()

    def run(self):
        # Hide cursor for clean look
        sys.stdout.write("\033[?25l")

        print(f"{C['pink']}{C['bold']}  🛰  Cosmic Widget starting...{C['reset']}")
        print(f"{C['void']}  Watching: music_signal.txt + stats{C['reset']}\n")
        time.sleep(1)

        tick = 0
        while self.running:
            self._draw()
            time.sleep(1)
            tick += 1
            if tick % 2 == 0:
                self.frame_idx += 1


if __name__ == "__main__":
    CosmicWidget().run()

    import os, sys, time, json, random, signal, subprocess
from pathlib import Path
from datetime import datetime

# CONFIG for avsn17
REPO_PATH = Path('/workspaces/timetodime2')
SIGNAL_FILE = REPO_PATH / 'music_signal.txt'

def sync_github(state):
    """Auto-syncs session to GitHub for stats"""
    try:
        os.chdir(REPO_PATH)
        subprocess.run(["git", "pull", "origin", "main", "--rebase", "--autostash"], capture_output=True)
        SIGNAL_FILE.write_text(state)
        subprocess.run(["git", "add", "music_signal.txt"], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"avsn17 Session: {state} at {datetime.now()}"], capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)
     dream_mix = [
        "ytdl://ytsearch10:Michael Jackson Thriller Original",
        "ytdl://ytsearch10:Lana Del Rey Born to Die Original",
        "ytdl://ytsearch10:Cigarettes After Sex Apocalypse Original",
        "ytdl://ytsearch10:Bee Gees Stayin Alive Original",
        "ytdl://ytsearch10:Billie Eilish Bad Guy Original",
        "ytdl://ytsearch10:Chopin Nocturnes Original"
    ]
    if state == "toggle":
        subprocess.Popen(["mpv", "--no-video", "--shuffle"] + dream_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ... (Keep the rest of your existing CosmicWidget class and UI code here) ...