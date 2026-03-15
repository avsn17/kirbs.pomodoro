# 🌸 kirbs.pomodoro

> Cosmic focus timer for Pilot avsn17. Terminal-based Pomodoro with Kirby energy, galactic ranks, and local music control.

---

## 🚀 Quick Start

```bash
git clone https://github.com/avsn17/kirbs.pomodoro
cd kirbs.pomodoro
pip install -r requirements.txt  # if applicable
python3 pomodoro_timer.py
```

Or via alias (add to `~/.zshrc` or `~/.bashrc`):
```bash
echo "alias poyo='cd $(pwd) && python3 pomodoro_timer.py'" >> ~/.zshrc
source ~/.zshrc
poyo
```

---

## 📁 Files

| File | Description |
|------|-------------|
| `pomodoro_timer.py` | Main terminal Pomodoro timer |
| `kirby_desktop.py` | Floating Kirby desktop widget (tkinter) |
| `kirby_notify.py` | Cross-platform desktop notifications |
| `local_vibe.py` | Local music controller (mpv) with signal watcher |
| `music_satellite.py` | Background signal listener for music autoplay |

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| `Space` | Pause / Resume |
| `C` | Open Wisdom Chat |
| `S` | Show Stats Leaderboard |
| `A` | Kirby Config / Settings |
| `M` | Toggle Music (writes signal to `music_signal.txt`) |
| `O` | Change Background Color |
| `N` | Save & Start New Session |
| `Q` | Save & Quit |

---

## 📊 Galactic Ranking System

| Distance | Rank |
|----------|------|
| 0 m | 🛸 Space Cadet |
| 100 m | 🌙 Moon Walker |
| 500 m | ☄️ Comet Rider |
| 1,000 m | 🚀 Orbit Master |
| 2,500 m | ⭐ Star Pilot |
| 5,000 m+ | 🌌 Galactic Overlord |

> 10 meters = 1 minute of focus time

---

## 💬 Wisdom Chat Categories

Type any of these in chat to get targeted quotes:

`iro` · `bronte` · `kant` · `lyrics` · `heroic` · `kirby` · `vibe` · `wisdom`

Or just type anything for a random one.

---

## 🖥️ Desktop Widget

Floating Kirby widget that reads `data/kirby_stats.json` and shows your progress live.

```bash
python3 kirby_desktop.py
```

**Features:**
- Mood-based Kirby faces (idle, working, done, sleepy, hungry)
- Animated bounce
- 5 color themes (pink, blue, green, peach, lavender) — saved between sessions
- Progress bar + session timer
- Milestone flash celebrations at 25%, 50%, 75%, 100%
- Right-click menu: stats popup, color change, celebrate

---

## 🔔 Notifications (`kirby_notify.py`)

Cross-platform desktop notifications wired into the timer.

```bash
python3 kirby_notify.py                        # test
python3 kirby_notify.py session_start 100
python3 kirby_notify.py milestone 50
python3 kirby_notify.py rank "⭐ Star Pilot"
python3 kirby_notify.py session_end 100 "🚀 Orbit Master"
```

Fires automatically on:
- Session start
- Session end (with distance + rank)
- Milestones (25%, 50%, 75%, 100%) *(coming soon)*

---

## 🎵 Local Music (`local_vibe.py`)

Controls a local `mpv` music player. Hooks into the `M` key via `music_signal.txt`.

```bash
# Drop your mp3
mkdir -p data && cp ~/music.mp3 data/focus_music.mp3

# Start the signal watcher in background
python3 local_vibe.py watch &

# Then run the timer — M key controls music live
poyo
```

**Commands:**
```bash
python3 local_vibe.py play
python3 local_vibe.py pause
python3 local_vibe.py resume
python3 local_vibe.py stop
python3 local_vibe.py volume 70
python3 local_vibe.py watch    # background signal watcher
```

**Signal file protocol (`music_signal.txt`):**

| Signal | Action |
|--------|--------|
| `PLAY_NEXT` | Start playing |
| `STOP` | Stop playback |
| `PAUSE` | Freeze playback |
| `RESUME` | Resume playback |

---

## 🌐 Web Dashboard

Live Base44 app with full Kirby UI, timer, leaderboard, and wisdom chat:

👉 https://app.base44.com/apps/69b68c64327ec9ecda6aa19b

---

## 🛠️ Requirements

- Python 3.10+
- `mpv` (for local music): `sudo apt install mpv` / `brew install mpv`
- `libnotify-bin` (Linux notifications): `sudo apt install libnotify-bin`
- `tkinter` (desktop widget): usually bundled with Python

---

## 👾 Pilot

**avsn17** — Cosmic Kirbs  
Branch: `kirbs`

---

*May your productivity journey be guided by wisdom. 🌌*

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/7e530e07-7de2-4301-8f5a-96d135ae4341" />
