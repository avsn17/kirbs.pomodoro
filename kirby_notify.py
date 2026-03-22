#!/usr/bin/env python3
# kirby_notify.py — terminal + desktop notifications for kirbs.pomodoro

import subprocess, sys, time, os

P = "\033[38;5;207m"
G = "\033[92m"
Y = "\033[93m"
E = "\033[0m"

def bell():
    sys.stdout.write("\a")
    sys.stdout.flush()

def notify(title, body, urgency="normal"):
    """Send desktop notification via notify-send + terminal bell."""
    bell()
    try:
        subprocess.run([
            "notify-send",
            "--urgency", urgency,
            "--expire-time", "8000",
            "--icon", "dialog-information",
            title, body
        ], check=False)
    except FileNotFoundError:
        pass
    # Always print to terminal too
    print(f"\n{P}  ✦ {title}{E}")
    print(f"  {body}\n")

def water():
    notify("💧 Hydration Check!", "Time for a sip, pilot. Your brain needs water.", "low")

def session_complete(minutes, rank):
    notify("🌌 Session Complete!", f"Poyo! {minutes} min locked in. Rank: {rank}", "normal")

def break_start(long=False):
    if long:
        notify("🎉 Long Break!", "You earned it. Stretch, hydrate, touch grass.", "normal")
    else:
        notify("☕ Short Break!", "Quick rest — kirby is proud of you.", "low")

def focus_start():
    notify("🚀 Focus Time!", "Break over. The galaxy waits. Lock in, pilot.", "normal")

def poyo(name="pilot"):
    notify("🌟 Poyo!", f"Kirby believes in you, {name}. Fly far.", "low")

def xp_gained(xp, total):
    notify("⭐ XP Gained!", f"+{xp} XP — Total: {total} XP", "low")

# ── CLI usage ────────────────────────────────────────────────────
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "poyo"
    if cmd == "water":       water()
    elif cmd == "break":     break_start(long="--long" in sys.argv)
    elif cmd == "focus":     focus_start()
    elif cmd == "complete":  session_complete(sys.argv[2] if len(sys.argv)>2 else "?", sys.argv[3] if len(sys.argv)>3 else "?")
    elif cmd == "xp":        xp_gained(sys.argv[2] if len(sys.argv)>2 else "?", sys.argv[3] if len(sys.argv)>3 else "?")
    else:                    poyo()
