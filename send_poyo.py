import os
import platform
import subprocess
import urllib.request
import json
import sys

# ─────────────────────────────────────────────
#  send_poyo — cross-platform push notifier
#  Works locally (OS notification) AND in CI
#  (ntfy.sh push) via NTFY_TOPIC env var.
# ─────────────────────────────────────────────


def send_via_ntfy(title: str, message: str, topic: str, priority: int = 3, tags: list[str] | None = None) -> None:
    """Send a push notification through ntfy.sh (works from any server/CI)."""
    url = f"https://ntfy.sh/{topic}"
    payload = json.dumps({
        "topic": topic,
        "title": title,
        "message": message,
        "priority": priority,
        **({"tags": tags} if tags else {}),
    }).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
        print(f"[ntfy] Notification sent → {url} (HTTP {status})")
    except Exception as e:
        print(f"[ntfy] ERROR: Could not send notification — {e}", file=sys.stderr)


def send_via_os(title: str, message: str) -> None:
    """Send a native desktop notification (local use only)."""
    system = platform.system()

    if system == "Darwin":
        # Use subprocess.run to avoid shell injection via title/message
        subprocess.run(
            ["osascript", "-e",
             f'display notification "{message}" with title "{title}" sound name "Glass"'],
            check=False,
        )
    elif system == "Linux":
        subprocess.run(["notify-send", title, message, "-i", "face-smile"], check=False)
    elif system == "Windows":
        try:
            from win10toast import ToastNotifier
            ToastNotifier().show_toast(title, message, duration=5)
        except ImportError:
            print("[warn] win10toast not installed — pip install win10toast")
    else:
        print(f"[warn] Unsupported OS: {system}")


def send_poyo(title: str, message: str, priority: int = 3, tags: list[str] | None = None) -> None:
    """
    Route to the right notification backend automatically:
      • In GitHub Actions / any CI  → ntfy.sh  (needs NTFY_TOPIC env var)
      • Locally                     → native OS popup
    """
    topic = os.environ.get("NTFY_TOPIC")   # read at call time, not import time
    if topic:
        send_via_ntfy(title, message, topic, priority=priority, tags=tags)
    else:
        send_via_os(title, message)


if __name__ == "__main__":
    # Optionally accept title + message as CLI args for workflow flexibility:
    #   python send_poyo.py "My Title" "My message" [priority] [tag1,tag2]
    args = sys.argv[1:]
    _title    = args[0] if len(args) > 0 else "Kirby System"
    _message  = args[1] if len(args) > 1 else "Poyo! Go, ready! (っ^‿^)っ"
    _priority = int(args[2]) if len(args) > 2 else 3
    _tags     = args[3].split(",") if len(args) > 3 else None

    send_poyo(_title, _message, priority=_priority, tags=_tags)
