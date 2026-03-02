# 🌟 Cosmic Pomodoro Timer — 2.03.2026

> *A terminal productivity timer with philosophical wisdom, animated starfields, and Kirby energy.*
> Pilot: **Cosmic Kirbs** | avsn17

---

## ✨ Features

- **Animated starfield** background that scrolls in real-time
- **Kirby mascot** that slides across the screen as you progress
- **Galactic Ranking System** — earn titles from Space Cadet to Galactic Overlord
- **Wisdom sidebar** — chat with the bot mid-session for quotes from Brontë, Kant, MJ, Billie, and more
- **Persistent stats** — leaderboard saved to `~/.pomodoro_stats.json`
- **Kirby Config** — toggle mood, hydration reminders, music autoplay, and color themes
- **Music signal** — writes `music_signal.txt` on completion for external autoplay integration
- **Session auto-save** — progress logged on quit/new, not just on completion

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/avsn17/timetodime2.git
cd timetodime2

# Run directly
python3 pomodoro_timer.py

# Or use the launcher (recommended)
chmod +x kirbs.sh
./kirbs.sh

# Install alias (add to ~/.bashrc or ~/.zshrc)
echo "alias poyo='cd $(pwd) && python3 pomodoro_timer.py'" >> ~/.zshrc
source ~/.zshrc

Pomodoro by using poyo

Widget by using wid 


---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| `Space` | Pause / Resume |
| `C` | Open Wisdom Chat |
| `S` | Show Stats Leaderboard |
| `A` | Kirby Config / Settings |
| `M` | Toggle Music Signal |
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

## 🎵 Music Autoplay Integration

On session completion, `music_signal.txt` is written with `PLAY_NEXT`.
Hook this up with a file watcher or the included satellite listener:

```bash
# Example with a separate listener process
python3 music_satellite.py &
```

---

## 📦 File Structure

```
timetodime2/
├── pomodoro_timer.py     ← Main app (run this)
├── kirbs.sh              ← Shell launcher with alias setup
├── music_signal.txt      ← Auto-created; triggers music autoplay
└── README.md
```

Stats are saved to `~/.pomodoro_stats.json` (outside the project directory).

---

*May your productivity journey be guided by wisdom. 🌌*

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/7e530e07-7de2-4301-8f5a-96d135ae4341" />
