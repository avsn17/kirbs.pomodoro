#!/usr/bin/env python3
import os, json, subprocess, sys
from pathlib import Path
P=chr(27)+"[38;5;207m"; A=chr(27)+"[38;5;205m"
G=chr(27)+"[92m"; R=chr(27)+"[91m"; E=chr(27)+"[0m"
issues=[]
def ok(m): print(f"  {G}OK{E}  {P}{m}{E}")
def bad(m): print(f"  {R}XX{E}  {P}{m}{E}"); issues.append(m)
def hdr(m): print(f"\n  {A}{m}{E}")
print(f"\n{P}  ~* kirbs.pomodoro healer *~{E}\n")
hdr("syntax")
for f in sorted(Path(".").glob("*.py")):
    r=subprocess.run(["python3","-c",f"import py_compile; py_compile.compile(chr(39)+str(f)+chr(39),doraise=True)"],capture_output=True)
    ok(str(f)) if r.returncode==0 else bad(f"{f}: syntax error")
hdr("logic fixes")
for fname,token,inv,label in [
    ("web_app.py","canvas-confetti",False,"CDN fix"),
    ("web_app.py","sanitize",False,"XSS fix"),
    ("web_app.py","last_date",False,"daily reset"),
    ("pomodoro_timer.py","_session_lock",False,"double-save lock"),
    ("pomodoro_timer.py","_session_saved",False,"session_saved flag"),
    ("music_player.py","returncode",False,"skip loop fix"),
    ("widget.py","sync_github",True,"broken fragment removed"),
    ("wid.sh",'eval "$USER_INPUT"',True,"eval hole removed"),
    ("poyo_ultimate.sh","timetodime2/",True,"broken paths removed"),
]:
    try:
        found=token in open(fname).read()
        bad(f"{fname}: {label}") if (inv and found) or (not inv and not found) else ok(f"{fname}: {label}")
    except: bad(f"{fname}: not found")
hdr("stats schema")
try:
    d=json.load(open("data/kirby_stats.json"))
    for k in ["tasks","done_today","total_poyos","water_int","level","xp"]:
        bad(f"kirby_stats.json: missing {k}") if k not in d else ok(f"kirby_stats.json: {k}")
except Exception as e: bad(str(e))
hdr("junk files")
for f in ["FETCH_HEAD","Cosmic","package.json","vercel.json","dockerfile","index.py","app.py","server.py"]:
    bad(f"{f}: present") if os.path.exists(f) else ok(f"{f}: absent")
print()
if issues: print(f"  {R}{len(issues)} issue(s){E}\n"); sys.exit(1)