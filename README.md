# 🌸 kirbs.pomodoro

> Cosmic focus timer for Pilot avsn17. Terminal-based Pomodoro with Kirby energy, galactic ranks, and local music control.

---
## WHAT the poyo IS THIS?

A Kirby-themed productivity suite. You set a focus goal, Kirby flies across the screen as you work, and you earn galactic ranks the more time you put in.

**4 parts that work together:**

| Component | Description | Location |
|-----------|-------------|----------|
| ⏱ **TIMER** | Your main focus session | Terminal |
| 🌐 **DASHBOARD** | Task list with XP + levels | Browser |
| 🎵 **MUSIC** | Streams your playlist | Terminal |
| 🛰 **WIDGET** | Live status panel | Second terminal |

---

## HOW TO START

### 🎮 Launcher Menu (Easiest Way)

```bash
./kirbs.sh
```

**Menu Options:**
- `[1]` Timer only — just start focusing
- `[2]` Timer + Music Player — focus with music
- `[3]` Widget only — status panel only
- `[4]` Music Player only — just the music
- `[5]` Install dependencies — first time setup

### 🚀 Direct Launch

```bash
python3 pomodoro_timer.py     # Timer
python3 web_app.py            # Dashboard (localhost:5000)
python3 music_player.py       # Music
python3 widget.py              # Widget (split terminal)
```

---

## ⏱ USING THE TIMER

When it starts, type how many **meters** you want to travel. Meters = minutes of focus time:

| Meters | Minutes | Session Type |
|--------|---------|--------------|
| 10m | 1 min | Quick task |
| 100m | 10 min | Short session |
| 250m | 25 min | Classic pomodoro |
| 500m | 50 min | Deep work |
| 1000m | 100 min | Marathon |

Kirby slides across the screen as you progress. A progress bar shows distance covered vs goal.

### ⌨️ Keyboard Controls

| Key | Action |
|-----|--------|
| `Space` | Pause / Resume |
| `Q` | Quit and save progress |
| `N` | Save and start a new session |
| `S` | See your stats + leaderboard |
| `C` | Open the wisdom chat |
| `A` | Settings (reminders, mood, colors) |
| `M` | Toggle music on/off |
| `O` | Change background color |

---

## 🏆 GALACTIC RANKS

Every minute you focus = **10 meters** toward your rank. Ranks are based on **total distance** across all sessions.

| Rank | Required Meters | Approx. Total Time |
|------|----------------|-------------------|
| 🛸 Space Cadet | 0m+ | Just starting |
| 🌙 Moon Walker | 100m+ | ~10 minutes |
| ☄️ Comet Rider | 500m+ | ~50 minutes |
| 🚀 Orbit Master | 1,000m+ | ~100 minutes |
| ⭐ Star Pilot | 2,500m+ | ~250 minutes |
| 🌌 Galactic Overlord | 5,000m+ | ~500 minutes |

Your rank shows live in the timer header and leaderboard.

---

## 💬 WISDOM CHAT (Press `C` during timer)

Type anything to get a motivational quote. Use these keywords to pick a specific source:

| Keyword | Source |
|---------|--------|
| `iro` | Uncle Iroh (Avatar) |
| `bronte` | Emily Brontë |
| `kant` | Immanuel Kant |
| `lyrics` | MJ, Lana, Bee Gees, Billie, Bowie, CAS |
| `heroic` | Classic heroic quotes |
| `kirby` | Kirby says poyo |
| `vibe` | Gen-Z energy |
| `wisdom` | General wisdom |
| `back` | Return to your session |

---

## 🌐 WEB DASHBOARD (Browser Task Tracker)

### Start It:
```bash
python3 web_app.py
```

### Open In Browser:
```
http://localhost:5000
```

**Codespace URL:**
```
https://effective-waffle-x57p9gr566j926vjw-8080.app.github.dev/
```

### How It Works:
1. Type a task in the box, click **POYO!** to add it
2. Click **INHALE** on a task to complete it
3. Each completed task = **+20 XP**
4. Hit **100 XP** = level up!
5. Water reminder counts down (default 25 min)
6. Confetti fires when all tasks are done 🎉

### Run in Background:
```bash
bash start_poyo.sh
tail -f logs/web_server.log   # Watch the logs
```

---

## 🎵 MUSIC PLAYER

### Start It:
```bash
python3 music_player.py
```

### Requirements:
```bash
sudo apt install mpv ffmpeg
```

Streams from YouTube — no downloads needed. **27 tracks** across 6 artists:

- 🌹 Lana Del Rey
- 🕺 Bee Gees
- 🎤 Michael Jackson
- 🎹 Chopin
- 🖤 Billie Eilish
- ✨ CAS

The timer's `M` key triggers music automatically. When a session completes, the next track plays.

---

## 🛰 TERMINAL WIDGET

Start it in a **SECOND terminal** while the timer is running:
```bash
python3 widget.py   # OR
bash wid.sh
```

### Live Display Shows:
- Current Kirby mood animation
- Session time + uptime
- Total distance + session count
- Last track playing
- Hydration reminder every 5 min

### Kirby Moods:

| Mood | Animation | Meaning |
|------|-----------|---------|
| Idle | `<(" )>` | Waiting for you |
| Active | `<(! )>` | GO GO GO! |
| Paused | `<( - )>` | Taking a breath |
| Complete | `<(* )>` | MISSION DONE!! |

---

## 💾 BACKUPS

### Create a Backup:
```bash
bash kirby_backup.sh
```
Saves to: `backups/backup-YYYY-MM-DD-HH-MM.tar.gz`

Keeps last 5 backups automatically.

### Restore a Backup:
```bash
tar -xzf backups/backup_2026-03-04_14-16.tar.gz
```

---

## 🔧 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| `No module named flask` | `pip install -r requirements.txt --break-system-packages` |
| `mpv not found` | `sudo apt install mpv ffmpeg` |
| Port 5000 in use | `PORT=8080 python3 web_app.py` |
| `manual.md not found` | `git pull origin main` |
| Dashboard data wrong | `echo '{"tasks":[],"done_today":0,"total_poyos":0,"water_int":25,"level":1,"xp":0}' > data/kirby_stats.json` |

---

## 📋 FULL COMMANDS OVERVIEW

### `kirbs.sh` (Launch Menu)
```
1      Timer only
2      Timer + Music Player
3      Widget only
4      Music Player only
5      Install dependencies (yt-dlp, ffmpeg, mpv)
h      Show all commands (this overview)
q      Quit
```

### `pomodoro_timer.py` (Keys During Session)
```
Space  Pause / Resume
N      Save & start new session
Q      Save & quit
C      Open Wisdom Chat
S      Stats leaderboard
A      Settings / Kirby Config
M      Toggle music autoplay
O      Change background color
H      Show help screen
```

### Wisdom Chat Categories (Press `C`, then type keyword)
```
iro      Uncle Iroh quotes
bronte   Emily Brontë quotes
kant     Immanuel Kant quotes
lyrics   MJ · Lana · Bee Gees · Billie · Bowie · CAS
heroic   Classic heroic quotes
kirby    Kirby says poyo
vibe     Gen-Z energy
wisdom   General wisdom
back     Return to session
(anything else = random category)
```

### `music_player.py` (Commands at Prompt)
```
lana     Play Lana Del Rey
beegees  Play Bee Gees
mj       Play Michael Jackson
chopin   Play Chopin
billie   Play Billie Eilish
cas      Play CAS
p        Play current track
n        Next track
b        Previous track
r        Random track
s        Stop
l        Show full playlist
h        Show history
h/help   Show help
q        Quit + stop music
(1-27)   Play track by number
```

### `wid.sh` (Pink Station Commands)
```
save     Commit & push to GitHub
next     Skip to next music track
help     Show help
exit     Exit the station
```

### `kirby_notify.py` (Run Directly for Testing)
```bash
python3 kirby_notify.py session_start 100
python3 kirby_notify.py milestone 50
python3 kirby_notify.py rank "⭐ Star Pilot"
python3 kirby_notify.py session_end 100 "🚀 Orbit Master"
```

### Utility Scripts
```bash
bash kirby_backup.sh     # Run a manual backup
bash start_poyo.sh       # Start web dashboard in background
bash setup.sh            # Full environment setup
bash poyo_ultimate.sh    # Launch everything at once
```


## 👾 Pilot

**avsn17** — Cosmic Kirbs  
Branch: main
---

```
<(o-o)>
```
---

*May your productivity journey be guided by wisdom. 🌌*

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/7e530e07-7de2-4301-8f5a-96d135ae4341" />
