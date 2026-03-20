import os
import platform
import urllib.request
import urllib.parse
import json

# ─────────────────────────────────────────────
#  send_poyo — cross-platform push notifier
#  Works locally (OS notification) AND in CI
#  (ntfy.sh push) via NTFY_TOPIC env var.
# ─────────────────────────────────────────────

NTFY_TOPIC = os.environ.get("NTFY_TOPIC")   # set this in GitHub Actions secrets


def send_via_ntfy(title: str, message: str, topic: str) -> None:
    """Send a push notification through ntfy.sh (works from any server/CI)."""
    url = f"https://ntfy.sh/{topic}"
    payload = json.dumps({"topic": topic, "title": title, "message": message}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        status = resp.status
    print(f"[ntfy] Notification sent → {url} (HTTP {status})")


def send_via_os(title: str, message: str) -> None:
    """Send a native desktop notification (local use only)."""
    system = platform.system()

    if system == "Darwin":
        os.system(
            f"osascript -e 'display notification \"{message}\" "
            f"with title \"{title}\" sound name \"Glass\"'"
        )
    elif system == "Linux":
        os.system(f"notify-send '{title}' '{message}' -i face-smile")
    elif system == "Windows":
        try:
            from win10toast import ToastNotifier
            ToastNotifier().show_toast(title, message, duration=5)
        except ImportError:
            print("[warn] win10toast not installed — pip install win10toast")
    else:
        print(f"[warn] Unsupported OS: {system}")


def send_poyo(title: str, message: str) -> None:
    """
    Route to the right notification backend automatically:
      • In GitHub Actions / any CI  → ntfy.sh  (needs NTFY_TOPIC env var)
      • Locally                     → native OS popup
    """
    if NTFY_TOPIC:
        send_via_ntfy(title, message, NTFY_TOPIC)
    else:
        send_via_os(title, message)


if __name__ == "__main__":
    send_poyo("Kirby System", "Poyo! Go, ready! (っ^‿^)っ")
