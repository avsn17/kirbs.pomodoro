import os
import platform
import subprocess
import shutil
import sys

# ─────────────────────────────────────────────────────────────────────
#  local_vibe.py — volume control + background focus music player
# ─────────────────────────────────────────────────────────────────────

_mpv_process: subprocess.Popen | None = None   # module-level handle so we can stop it


def _check_tool(name: str) -> bool:
    """Return True if a CLI tool is available on PATH."""
    return shutil.which(name) is not None


def set_system_volume(level: int) -> None:
    """
    Set system volume. Level must be 0–100.
    Works on macOS (osascript) and Linux (amixer).
    """
    # FIX: clamp to valid range — values outside 0-100 silently corrupt state
    level = max(0, min(100, level))
    system = platform.system()

    if system == "Darwin":
        if not _check_tool("osascript"):
            print("[warn] osascript not found — cannot set volume on this Mac", file=sys.stderr)
            return
        # FIX: subprocess.run list form — no shell, no injection risk
        subprocess.run(
            ["osascript", "-e", f"set volume output volume {level}"],
            check=False,
        )
    elif system == "Linux":
        if not _check_tool("amixer"):
            print("[warn] amixer not found — install alsa-utils: sudo apt install alsa-utils", file=sys.stderr)
            return
        # FIX: subprocess.run list form — no shell, no injection risk
        subprocess.run(
            ["amixer", "set", "Master", f"{level}%"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    else:
        print(f"[warn] set_system_volume: unsupported OS '{system}'", file=sys.stderr)


def play_focus_sound(path: str = "data/focus_music.mp3") -> subprocess.Popen | None:
    """
    Start mpv playing a local file in the background.
    Returns the Popen handle so the caller can stop it later.
    Call stop_focus_sound() or use the returned handle directly.
    """
    global _mpv_process

    # FIX: check if the file actually exists before trying to play it
    if not os.path.isfile(path):
        print(f"[warn] Music file not found: {path}", file=sys.stderr)
        return None

    # FIX: check if mpv is installed
    if not _check_tool("mpv"):
        print("[warn] mpv not found — install it: https://mpv.io/installation/", file=sys.stderr)
        return None

    # FIX: store process handle so stop_focus_sound() can terminate it
    print(f"🎵 Starte lokale Focus-Playlist: {path}")
    _mpv_process = subprocess.Popen(
        ["mpv", "--loop-file=inf", path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return _mpv_process


def stop_focus_sound() -> None:
    """Stop the background mpv player started by play_focus_sound()."""
    global _mpv_process
    if _mpv_process is None:
        print("[info] No focus sound is currently playing.")
        return
    if _mpv_process.poll() is None:        # still running
        _mpv_process.terminate()
        try:
            _mpv_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            _mpv_process.kill()
        print("🎵 Focus sound stopped.")
    _mpv_process = None
