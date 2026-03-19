╔══════════════════════════════════════════════════════════╗
║         📖 KIRBS.POMODORO — PILOT MANUAL                 ║
║              Cosmic Kirbs · avsn17                       ║
╚══════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  WHAT IS THIS?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  A Kirby-themed productivity suite. You set a focus goal,
  Kirby flies across the screen as you work, and you earn
  galactic ranks the more time you put in.

  4 parts that work together:

  ⏱  TIMER      → your main focus session (terminal)
  🌐  DASHBOARD  → task list with XP + levels (browser)
  🎵  MUSIC      → streams your playlist (terminal)
  🛰  WIDGET     → live status panel (second terminal)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HOW TO START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Easiest way — the launcher menu:

    ./kirbs.sh

  Pick what you want:
    [1] Timer only                ← just start focusing
    [2] Timer + Music Player      ← focus with music
    [3] Widget only               ← status panel only
    [4] Music Player only         ← just the music
    [5] Install dependencies      ← first time setup

  Or start things directly:

    python3 pomodoro_timer.py     ← timer
    python3 web_app.py            ← dashboard (localhost:5000)
    python3 music_player.py       ← music
    python3 widget.py             ← widget (split terminal)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⏱  USING THE TIMER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  When it starts, type how many meters you want to travel.
  Meters = minutes of focus time:

    10m  =  1 min      ← quick task
    100m =  10 min     ← short session
    250m =  25 min     ← classic pomodoro
    500m =  50 min     ← deep work
    1000m = 100 min    ← marathon

  Kirby slides across the screen as you progress.
  A progress bar shows distance covered vs goal.

  KEYS WHILE TIMER IS RUNNING:

    Space  →  pause or resume
    Q      →  quit and save progress
    N      →  save and start a new session
    S      →  see your stats + leaderboard
    C      →  open the wisdom chat
    A      →  settings (reminders, mood, colors)
    M      →  toggle music on/off
    O      →  change background color

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🏆 GALACTIC RANKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Every minute you focus = 10 meters toward your rank.
  Ranks are based on total distance across all sessions.

    🛸  Space Cadet      0m+      ← everyone starts here
    🌙  Moon Walker      100m+    ← ~10 min total
    ☄️   Comet Rider      500m+    ← ~50 min total
    🚀  Orbit Master     1,000m+  ← ~100 min total
    ⭐  Star Pilot       2,500m+  ← ~250 min total
    🌌  Galactic Overlord 5,000m+ ← ~500 min total

  Your rank shows live in the timer header and leaderboard.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💬 WISDOM CHAT  (press C during timer)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Type anything to get a motivational quote.
  Use these keywords to pick a specific source:

    iro      → Uncle Iroh (Avatar)
    bronte   → Emily Brontë
    kant     → Immanuel Kant
    lyrics   → MJ, Lana, Bee Gees, Billie, Bowie, CAS
    heroic   → classic heroic quotes
    kirby    → Kirby says poyo
    vibe     → gen-z energy
    wisdom   → general wisdom

  Type  back  to return to your session.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🌐 WEB DASHBOARD  (browser task tracker)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Start it:   python3 web_app.py
  Open:       http://localhost:5000
  Codespace:  https://effective-waffle-x57p9gr566j926vjw-8080.app.github.dev/

  HOW IT WORKS:
  → Type a task in the box, click POYO! to add it
  → Click INHALE on a task to complete it
  → Each completed task = +20 XP
  → Hit 100 XP = level up!
  → Water reminder counts down (default 25 min)
  → Confetti fires when all tasks are done 🎉

  To run it in the background:
    bash start_poyo.sh
    tail -f logs/web_server.log   ← watch the logs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎵 MUSIC PLAYER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Start it:   python3 music_player.py
  Needs:      sudo apt install mpv ffmpeg

  Streams from YouTube — no downloads needed.
  27 tracks across 6 artists:

    🌹 Lana Del Rey    🕺 Bee Gees     🎤 Michael Jackson
    🎹 Chopin          🖤 Billie Eilish  ✨ CAS

  The timer's M key triggers music automatically.
  When a session completes, the next track plays.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🛰 TERMINAL WIDGET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Start it in a SECOND terminal while the timer is running:
    python3 widget.py   OR   bash wid.sh

  Shows you live:
  → Current Kirby mood animation
  → Session time + uptime
  → Total distance + session count
  → Last track playing
  → Hydration reminder every 5 min

  Kirby moods:
    idle     → <( " )>  waiting for you
    active   → <( ! )>  GO GO GO!
    paused   → <(  - )>  taking a breath
    complete → <( * )>  MISSION DONE!!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💾 BACKUPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Run a backup:    bash kirby_backup.sh
  Saves to:        backups/backup-YYYY-MM-DD-HH-MM.tar.gz
  Keeps last 5 backups automatically.

  Restore:
    tar -xzf backups/backup_2026-03-04_14-16.tar.gz

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔧 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  "No module named flask"
    pip install -r requirements.txt --break-system-packages

  "mpv not found" (no music)
    sudo apt install mpv ffmpeg

  "Port 5000 in use"
    PORT=8080 python3 web_app.py

  "manual.md not found"
    git pull origin main

  Dashboard data looks wrong
    echo '{"tasks":[],"done_today":0,"total_poyos":0,"water_int":25,"level":1,"xp":0}' > data/kirby_stats.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  <( ^ )>  Poyo! May your sessions be focused, avsn17. 🌌

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
