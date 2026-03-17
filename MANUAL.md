#!/usr/bin/env bash
# 🌸 EXECUTABLE MANUAL - Type ./MANUAL.md to view me!

# If script is executed directly, show the manual
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo -e "\033[38;5;213m"
    cat << "BANNER"
    ╭──────────────────────────────╮
    │  🌸 MARIO & KIRBS MANUAL 🌸  │
    │  🍄  EXECUTABLE EDITION!  🍄  │
    ╰──────────────────────────────╯
BANNER
    echo -e "\033[0m"
    echo -e "\033[38;5;226m🍄 Opening manual in browser...\033[0m"
    
    # Check if file exists
    if [[ -f "manual.html" ]]; then
        # Try different methods to open
        if command -v open &> /dev/null; then
            open manual.html 2>/dev/null || true
        elif command -v xdg-open &> /dev/null; then
            xdg-open manual.html 2>/dev/null || true
        elif command -v python3 &> /dev/null; then
            echo -e "\033[38;5;082m📡 Starting server at http://localhost:8765/manual.html\033[0m"
            python3 -m http.server 8765 --bind 127.0.0.1 &
            sleep 2
            open http://localhost:8765/manual.html 2>/dev/null || \
            xdg-open http://localhost:8765/manual.html 2>/dev/null || \
            echo -e "\033[38;5;196mPlease open http://localhost:8765/manual.html manually\033[0m"
        fi
    else
        echo -e "\033[38;5;196m❌ manual.html not found! Run ./create_mega_manual.sh first!\033[0m"
    fi
    exit 0
fi

: << 'MARKDOWN'
# 🌸 kirbs.pomodoro - MARIO KIRBY EXECUTABLE MANUAL 🌸

<div align="center">
<img src="https://raw.githubusercontent.com/avsn17/kirbs.pomodoro/main/assets/kirby_cute.gif" width="100">
<span style="font-size: 3em;">👨⭐</span>
</div>

> **✨ Type `./MANUAL.md` to open the interactive HTML version! ✨**

---

## 🍄 MARIO STICKER FOUND!


**Mario says:** *"It's-a me! I'm here to help Kirby focus!"*

---

## 🚀 QUICK START

```bash
# Clone and go!
git clone https://github.com/avsn17/kirbs.pomodoro
cd kirbs.pomodoro
pip install -r requirements.txt

# Run the cute timer
./poyo

# Or open this manual in browser!
./MANUAL.md
# 🌸 Create Executable Manual.md with Mario Magic! 🌸

Here's a bash script that creates an **executable** `MANUAL.md` file that you can run directly!

```bash
#!/bin/bash

# 🌸🍄 CREATE EXECUTABLE MANUAL.MD WITH MARIO MAGIC 🍄🌸
# This creates a MANUAL.md that's also runnable!

set -e

# Colors
PINK='\033[38;5;213m'
RED='\033[38;5;196m'
GREEN='\033[38;5;082m'
YELLOW='\033[38;5;226m'
NC='\033[0m'

echo -e "${PINK}🌸 Creating executable MANUAL.md with Mario power!${NC}"

# Create the executable MANUAL.md
cat > MANUAL.md << 'EOF'
#!/usr/bin/env bash
# 🌸 EXECUTABLE MANUAL - Type ./MANUAL.md to view me!

# If script is executed directly, show the manual
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo -e "\033[38;5;213m"
    cat << "BANNER"
    ╭──────────────────────────────╮
    │  🌸 MARIO & KIRBS MANUAL 🌸  │
    │  🍄  EXECUTABLE EDITION!  🍄  │
    ╰──────────────────────────────╯
BANNER
    echo -e "\033[0m"
    echo -e "\033[38;5;226m🍄 Opening manual in browser...\033[0m"
    
    # Check if file exists
    if [[ -f "manual.html" ]]; then
        # Try different methods to open
        if command -v open &> /dev/null; then
            open manual.html 2>/dev/null || true
        elif command -v xdg-open &> /dev/null; then
            xdg-open manual.html 2>/dev/null || true
        elif command -v python3 &> /dev/null; then
            echo -e "\033[38;5;082m📡 Starting server at http://localhost:8765/manual.html\033[0m"
            python3 -m http.server 8765 --bind 127.0.0.1 &
            sleep 2
            open http://localhost:8765/manual.html 2>/dev/null || \
            xdg-open http://localhost:8765/manual.html 2>/dev/null || \
            echo -e "\033[38;5;196mPlease open http://localhost:8765/manual.html manually\033[0m"
        fi
    else
        echo -e "\033[38;5;196m❌ manual.html not found! Run ./create_mega_manual.sh first!\033[0m"
    fi
    exit 0
fi

: << 'MARKDOWN'
# 🌸 kirbs.pomodoro - MARIO KIRBY EXECUTABLE MANUAL 🌸

<div align="center">
<img src="https://raw.githubusercontent.com/avsn17/kirbs.pomodoro/main/assets/kirby_cute.gif" width="100">
<span style="font-size: 3em;">👨⭐</span>
</div>

> **✨ Type `./MANUAL.md` to open the interactive HTML version! ✨**

---

## 🍄 MARIO STICKER FOUND!

```
        ⭐
       🍄🍄
      👕👖👞
     🧤🧤🧤
    🧢🧧🧢🧢
   👨👨👨👨👨
  ⭐⭐⭐⭐⭐⭐
```

**Mario says:** *"It's-a me! I'm here to help Kirby focus!"*

---

## 🚀 QUICK START

```bash
# Clone and go!
git clone https://github.com/avsn17/kirbs.pomodoro
cd kirbs.pomodoro
pip install -r requirements.txt

# Run the cute timer
./poyo

# Or open this manual in browser!
./MANUAL.md
```

---

## 🎮 MAGIC CONTROLS

| Key | What It Does |
|:---:|-------------|
| **Space** | ⏯️ Pause/Resume |
| **C** | 💭 Wisdom Chat |
| **S** | 📊 Show Stats |
| **M** | 🎵 Toggle Music |
| **Q** | 👋 Save & Quit |

---

## 📊 GALACTIC RANKS

| Minutes | = Meters | Rank |
|---------|----------|------|
| 0 | 0m | 🛸 Space Cadet |
| 10 | 100m | 🌙 Moon Walker |
| 50 | 500m | ☄️ Comet Rider |
| 100 | 1000m | 🚀 Orbit Master |
| 250 | 2500m | ⭐ Star Pilot |
| 500+ | 5000m+ | 🌌 Galactic Overlord |

---

## 💭 WISDOM CHAT

Press **C** and type:
`iro` `bronte` `kant` `lyrics` `heroic` `kirby` `vibe` `mario`

---

## 🖥️ FLOATING KIRBY

```bash
python3 kirby_desktop.py
```

Right-click Kirby for:
- 🎨 Color themes
- 📊 Stats popup
- 🎉 Celebrations!

---

## 🎵 MUSIC MODE

```bash
# 1. Add music
cp song.mp3 data/focus_music.mp3

# 2. Start listener
python3 local_vibe.py watch &

# 3. Press M in timer!
```

---

## 🆘 QUICK FIXES

| Problem | Solution |
|---------|----------|
| `poyo` not found | `chmod +x poyo` |
| No widget | `brew install python-tk` |
| No music | `brew install mpv` |
| Mario lost | `echo "It's-a me!"` |

---

## 🌐 WEB DASHBOARD

👉 [Click for web version!](https://app.base44.com/apps/69b68c64327ec9ecda6aa19b)

---

<div align="center">

## 🎀 **EXTRA CUTE!** 🎀

**Type `./MANUAL.md` to open the INTERACTIVE version!**

<img src="https://raw.githubusercontent.com/avsn17/kirbs.pomodoro/main/assets/kirby_happy.gif" width="150">

**Made with 🍰 by avsn17**  
**Guest appearance: 👨 Mario**

```
     (◕‿◕✿) + 👨 = ⭐
```

</div>

MARKDOWN
