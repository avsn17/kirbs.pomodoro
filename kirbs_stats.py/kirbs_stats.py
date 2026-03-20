import json, os
from datetime import datetime
try:
    pilot = open(os.path.expanduser('~/.kirbs_pilot')).read().strip()
    d = json.load(open(os.path.expanduser('~/.pomodoro_stats.json')))
    u = d.get(pilot, list(d.values())[0] if d else {})
    dist = u.get('total_distance', 0)
    sess = u.get('completed_sessions', 0)
    mins = round(u.get('total_time', 0) / 60)
    ranks = [(5000,'Galactic Overlord'),(2500,'Star Pilot'),(1000,'Orbit Master'),(500,'Comet Rider'),(100,'Moon Walker'),(0,'Space Cadet')]
    rank = next(r for t,r in ranks if dist >= t)
    nxt = next(((t,r) for t,r in ranks if t > dist), None)
    today = datetime.now().strftime('%Y-%m-%d')
    today_s = [s for s in u.get('sessions',[]) if s.get('date','').startswith(today)]
    today_m = round(sum(s.get('duration',0) for s in today_s)/60)
    gap = f"  {nxt[1]} in {nxt[0]-dist:.0f}m" if nxt else "  MAX RANK ACHIEVED"
    print(f"  \033[38;5;205m rank    \033[38;5;207m> {rank}")
    print(f"  \033[38;5;205m all time\033[38;5;207m> {dist:.0f}m  |  {sess} sessions  |  {mins} min")
    print(f"  \033[38;5;205m today   \033[38;5;207m> {len(today_s)} sessions  |  {today_m} min")
    print(f"  \033[38;5;205m next    \033[38;5;207m>{gap}")
except:
    print("  \033[38;5;205m rank    \033[38;5;207m> Space Cadet  (no sessions yet)")