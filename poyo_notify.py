#!/usr/bin/env python3
import os, sys, platform, random

FACES = {
    "session_start": ["(っ^‿^)っ", "( ´ ▽ ` )っ", "(>^_^)>"],
    "session_end":   ["(★^O^★)", "٩(◕‿◕｡)۶", "ヽ(•‿•)ノ"],
    "break_start":   ["(－_－) zzZ", "(´-ω-`)", "(-_-)zzz"],
    "milestone":     ["(ง •_•)ง", "( •̀ᴗ•́ )و", "(ᗒᗨᗕ)"],
    "rank_up":       ["(≧◡≦)", "(★^O^★)", "٩(◕‿◕｡)۶"],
    "reminder":      ["(＾་།＾)", "(o゜▽゜)o", "(っ^‿^)っ"],
    "default":       ["(っ^‿^)っ", '<( " )>', "(◕‿◕)っ"],
}
MESSAGES = {
    "session_start": ["Mission launched! Let's go, Cosmic Kirbs!", "Focus mode: MAXIMUM PINK POWER. GO!", "Timer is running. You've got this!"],
    "session_end":   ["MISSION COMPLETE! You crushed it!", "Session done! Take a well-earned break.", "Poyo! Another one in the books!"],
    "break_start":   ["Break time! Stretch those legs.", "Rest up, pilot. You've earned it.", "Hydrate! Water = cosmic fuel. 💧"],
    "reminder":      ["Still going strong? Drink some water!", "Hydration check! 💧", "Quick stretch — your back will thank you."],
}
MAC_SOUNDS = {"session_start":"Blow","session_end":"Glass","break_start":"Purr","milestone":"Ping","rank_up":"Hero","reminder":"Tink","default":"Pop"}

def _face(e): return random.choice(FACES.get(e, FACES["default"]))
def _msg(e):  pool = MESSAGES.get(e); return random.choice(pool) if pool else "Poyo!"
def _esc(s):  return s.replace("'", "\\'").replace('"', '\\"')

def send_poyo(title, message, event="default"):
    system = platform.system()
    if system == "Darwin":
        sound = MAC_SOUNDS.get(event, "Pop")
        os.system(f'osascript -e \'display notification "{_esc(message)}" with title "{_esc(title)}" sound name "{sound}"\'')
    elif system == "Linux":
        urgency = "critical" if event == "session_end" else "normal"
        icon = "face-smile" if event != "break_start" else "face-tired"
        os.system(f"notify-send -u {urgency} -i {icon} '{_esc(title)}' '{_esc(message)}'")
    elif system == "Windows":
        try:
            from win10toast import ToastNotifier
            ToastNotifier().show_toast(title, message, duration=5, threaded=True)
        except ImportError:
            t, m = title.replace("'",""), message.replace("'","")
            os.system(f"powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('{m}', '{t}')\"")
    else:
        print(f"\n🔔 {title}\n   {message}\n")

def notify_session_start(goal_m):  send_poyo(f"{_face('session_start')} Mission Launched!", f"Goal: {goal_m}m · Focus time, Cosmic Kirbs!", "session_start")
def notify_session_end(dist, rank): send_poyo(f"{_face('session_end')} Mission Complete!", f"{dist:.0f}m covered · Rank: {rank}", "session_end")
def notify_break(tip=""):          send_poyo(f"{_face('break_start')} Break Time!", tip or _msg("break_start"), "break_start")
def notify_milestone(pct):
    labels = {25:"Quarter way!", 50:"Halfway!!", 75:"Almost there!", 100:"DONE!"}
    send_poyo(f"{_face('milestone')} {pct}% POYO!", labels.get(pct, f"{pct}% — keep going!"), "milestone")
def notify_rank_up(new_rank):      send_poyo(f"{_face('rank_up')} RANK UP!", f"New rank: {new_rank}", "rank_up")
def notify_reminder(text=""):      send_poyo(f"{_face('reminder')} Kirby Reminder", text or _msg("reminder"), "reminder")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:                              send_poyo("(っ^‿^)っ Kirby System", "Poyo! Notifications working!", "default")
    elif args[0] == "session_start":          notify_session_start(int(args[1]) if len(args)>1 else 100)
    elif args[0] == "session_end":            notify_session_end(float(args[1]) if len(args)>1 else 100, args[2] if len(args)>2 else "🛸 Space Cadet")
    elif args[0] == "break_start":            notify_break(args[1] if len(args)>1 else "")
    elif args[0] == "milestone":              notify_milestone(int(args[1]) if len(args)>1 else 50)
    elif args[0] == "rank":                   notify_rank_up(args[1] if len(args)>1 else "⭐ Star Pilot")
    elif args[0] == "reminder":               notify_reminder(args[1] if len(args)>1 else "")
    elif args[0] == "custom" and len(args)>=3: send_poyo(args[1], args[2])
