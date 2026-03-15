# paste file contents
#!/usr/bin/env python3
"""
local_vibe.py — Local music controller for Cosmic Pomodoro
Hooks into the M command and music_signal.txt watcher.

Usage (standalone):
    python3 local_vibe.py play
    python3 local_vibe.py pause
    python3 local_vibe.py resume
    python3 local_vibe.py stop
    python3 local_vibe.py volume 60
    python3 local_vibe.py watch          # watches music_signal.txt (run in background)
"""

import os, sys, platform, subprocess, signal, time
from pathlib import Path

SIGNAL_FILE  = Path('music_signal.txt')
PID_FILE     = Path('data/vibe_pid.txt')
MUSIC_FILE   = Path('data/focus_music.mp3')
DEFAULT_VOL  = 60

# ─── VOLUME ───────────────────────────────────────────────────────────────────
def set_volume(level: int):
    """Set system volume 0–100."""
    level = max(0, min(100, level))
    system = platform.system()
    if system == "Darwin":
        os.system(f"osascript -e 'set volume output volume {level}'")
    elif system == "Linux":
        os.system(f"amixer set Master {level}% > /dev/null 2>&1")
    elif system == "Windows":
        # Uses nircmd if available, silent fail otherwise
        os.system(f"nircmd.exe setsysvolume {int(level * 655.35)} > nul 2>&1")

# ─── PLAYER CONTROL ───────────────────────────────────────────────────────────
def _save_pid(pid: int):
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(pid))

def _load_pid() -> int | None:
    try:
        return int(PID_FILE.read_text().strip())
    except Exception:
        return None

def _is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False

def play(music_path: Path = MUSIC_FILE, volume: int = DEFAULT_VOL):
    """Start mpv in background. Kills any existing instance first."""
    stop()
    set_volume(volume)

    if not music_path.exists():
        print(f"⚠️  Music file not found: {music_path}")
        print("    Drop an mp3 into data/focus_music.mp3 to enable local playback.")
        return

    proc = subprocess.Popen(
        ["mpv", "--loop-file=inf", "--no-video",
         "--really-quiet", str(music_path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _save_pid(proc.pid)
    print(f"🎵 Playing {music_path.name} (pid {proc.pid})")

def pause():
    """Send SIGSTOP to mpv — freezes playback without killing."""
    pid = _load_pid()
    if pid and _is_running(pid):
        os.kill(pid, signal.SIGSTOP)
        print(f"⏸  Music paused (pid {pid})")
    else:
        print("⚠️  No music running to pause.")

def resume():
    """Send SIGCONT to mpv — resumes from where it paused."""
    pid = _load_pid()
    if pid and _is_running(pid):
        os.kill(pid, signal.SIGCONT)
        print(f"▶  Music resumed (pid {pid})")
    else:
        print("⚠️  No paused music found. Starting fresh...")
        play()

def stop():
    """Kill mpv and clean up pid file."""
    pid = _load_pid()
    if pid and _is_running(pid):
        os.kill(pid, signal.SIGTERM)
        print(f"⏹  Music stopped (pid {pid})")
    try:
        PID_FILE.unlink(missing_ok=True)
    except Exception:
        pass

def toggle():
    """Toggle between play and pause based on current state."""
    pid = _load_pid()
    if pid and _is_running(pid):
        pause()
    else:
        resume()

# ─── SIGNAL FILE WATCHER (for M command integration) ──────────────────────────
def watch():
    """
    Watch music_signal.txt and react to signals written by pomodoro_timer.py.
    Run this in the background:  python3 local_vibe.py watch &
    """
    print("👁  Watching music_signal.txt for signals...")
    last_signal = ""

    while True:
        try:
            if SIGNAL_FILE.exists():
                sig = SIGNAL_FILE.read_text().strip()
                if sig != last_signal:
                    last_signal = sig
                    if sig == "PLAY_NEXT":
                        print("📡 Signal: PLAY_NEXT → playing")
                        play()
                        SIGNAL_FILE.write_text("IDLE")
                    elif sig == "STOP":
                        print("📡 Signal: STOP → stopping")
                        stop()
                        SIGNAL_FILE.write_text("IDLE")
                    elif sig == "PAUSE":
                        print("📡 Signal: PAUSE → pausing")
                        pause()
                        SIGNAL_FILE.write_text("IDLE")
                    elif sig == "RESUME":
                        print("📡 Signal: RESUME → resuming")
                        resume()
                        SIGNAL_FILE.write_text("IDLE")
        except Exception as e:
            print(f"⚠️  Watcher error: {e}")
        time.sleep(1)

# ─── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] == "play":
        play()
    elif args[0] == "pause":
        pause()
    elif args[0] == "resume":
        resume()
    elif args[0] == "stop":
        stop()
    elif args[0] == "toggle":
        toggle()
    elif args[0] == "volume" and len(args) > 1:
        set_volume(int(args[1]))
        print(f"🔊 Volume set to {args[1]}%")
    elif args[0] == "watch":
        watch()
    else:
        print(__doc__)