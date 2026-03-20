import os
import platform

def send_poyo(title, message):
    system = platform.system()
    # macOS
    if system == "Darwin":
        os.system(f"osascript -e 'display notification \"{message}\" with title \"{title}\" sound name \"Glass\"'")
    # Linux (erfordert libnotify-bin)
    elif system == "Linux":
        os.system(f"notify-send '{title}' '{message}' -i face-smile")
    # Windows
    elif system == "Windows":
        from win10toast import ToastNotifier # type: ignore
        ToastNotifier().show_toast(title, message, duration=5)

if __name__ == "__main__":
    send_poyo("Kirby System", "Poyo! Go, ready! (っ^‿^)っ")
