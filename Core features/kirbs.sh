#!/usr/bin/env bash
# ┌─────────────────────────────────────────────────────┐
# │   kirbs.sh — Cosmic Mission Control (bash edition)  │
# │   Launches: Timer + Music Player + Widget           │
# └─────────────────────────────────────────────────────┘

PINK='\033[38;5;218m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
VOID='\033[0;90m'
BOLD='\033[1m'
NC='\033[0m'

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cleanup() {
    kill $(jobs -p) 2>/dev/null
    echo -e "\n${PINK}<( 'o' )> Cockpit closed. Fly safe, Cosmic Kirbs.${NC}"
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

clear
echo -e "${PINK}${BOLD}"
echo "  ╔════════════════════════════════════════╗"
echo "  ║   🌟 COSMIC MISSION CONTROL — kirbs    ║"
echo "  ╚════════════════════════════════════════╝"
echo -e "${NC}"

# ── File checks ───────────────────────────────────────
missing=0
for f in pomodoro_timer.py music_player.py widget.py; do
    if [[ ! -f "$DIR/$f" ]]; then
        echo -e "  ❌ Missing: ${BOLD}$f${NC}"
        missing=1
    fi
done
[[ $missing -eq 1 ]] && echo -e "  ${YELLOW}Some files missing. Only available modules will run.${NC}\n"

# Ensure signal file
: > "$DIR/music_signal.txt"

# ── Menu ──────────────────────────────────────────────
echo -e "  ${CYAN}What would you like to launch?${NC}\n"
echo -e "  ${GREEN}[1]${NC} Timer only"
echo -e "  ${GREEN}[2]${NC} Timer + Music Player (two terminals needed)"
echo -e "  ${GREEN}[3]${NC} Widget only (run in a split pane)"
echo -e "  ${GREEN}[4]${NC} Music Player only"
echo -e "  ${GREEN}[5]${NC} Setup — install dependencies (yt-dlp, ffmpeg)"
echo -e "  ${VOID}[q] Quit${NC}\n"

read -rp "  Select: " choice

case "$choice" in
    1)
        echo -e "\n  ${YELLOW}🚀 Launching Timer...${NC}\n"
        python3 "$DIR/pomodoro_timer.py"
        ;;
    2)
        echo -e "\n  ${YELLOW}🚀 Launching Timer...${NC}"
        echo -e "  ${VOID}→ Open a second terminal and run: python3 widget.py${NC}"
        echo -e "  ${VOID}→ Open a third terminal and run:  python3 music_player.py${NC}\n"
        python3 "$DIR/pomodoro_timer.py"
        ;;
    3)
        echo -e "\n  ${PINK}🛰  Launching Widget...${NC}\n"
        python3 "$DIR/widget.py"
        ;;
    4)
        echo -e "\n  ${CYAN}🎵 Launching Music Player...${NC}\n"
        python3 "$DIR/music_player.py"
        ;;
    5)
        echo -e "\n  ${CYAN}Installing dependencies...${NC}"
        pip install yt-dlp --quiet --break-system-packages 2>/dev/null || pip install yt-dlp --quiet
        sudo apt-get install -y ffmpeg mpv -qq 2>/dev/null
        echo -e "  ${GREEN}Done! Re-run kirbs.sh to launch.${NC}"
        ;;
    q|Q)
        echo -e "  ${VOID}Aborted.${NC}"
        ;;
    *)
        echo -e "  ${YELLOW}Invalid choice. Run ./kirbs.sh again.${NC}"
        ;;
esac

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>kirbs.pomodoro — Cosmic Terminal Timer</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>
  :root {
    --void: #03010a;
    --deep: #070314;
    --nebula: #0d0828;
    --pink: #ff2d78;
    --cyan: #00f5ff;
    --gold: #ffd966;
    --lavender: #c084fc;
    --mint: #4ade80;
    --dim: rgba(255,255,255,0.07);
    --border: rgba(0,245,255,0.15);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  html { scroll-behavior: smooth; }

  body {
    background: var(--void);
    color: #e2d9f3;
    font-family: 'Space Mono', monospace;
    overflow-x: hidden;
    min-height: 100vh;
  }

  /* ── STARFIELD ── */
  #starfield {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
  }

  /* ── SCANLINES ── */
  body::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0,0,0,0.08) 2px,
      rgba(0,0,0,0.08) 4px
    );
    pointer-events: none;
    z-index: 9999;
  }

  /* ── LAYOUT ── */
  .wrapper {
    position: relative;
    z-index: 1;
    max-width: 860px;
    margin: 0 auto;
    padding: 0 24px 80px;
  }

  /* ── HERO ── */
  .hero {
    text-align: center;
    padding: 80px 0 60px;
    position: relative;
  }

  .hero-eyebrow {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 4px;
    color: var(--cyan);
    text-transform: uppercase;
    margin-bottom: 24px;
    opacity: 0.7;
  }

  .hero-kirby {
    font-size: 72px;
    line-height: 1;
    margin-bottom: 16px;
    animation: float 4s ease-in-out infinite;
    display: block;
  }

  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
  }

  .hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(28px, 6vw, 56px);
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #fff 0%, var(--cyan) 40%, var(--lavender) 70%, var(--pink) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
  }

  .hero-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    color: var(--lavender);
    letter-spacing: 2px;
    margin-bottom: 32px;
  }

  .hero-meta {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 2px;
    margin-bottom: 48px;
  }

  .hero-meta span { color: var(--gold); }

  /* ── TERMINAL BLOCK ── */
  .terminal {
    background: rgba(0,0,0,0.6);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 60px;
    backdrop-filter: blur(8px);
    box-shadow: 0 0 40px rgba(0,245,255,0.05), 0 20px 60px rgba(0,0,0,0.5);
  }

  .terminal-bar {
    background: rgba(0,245,255,0.04);
    border-bottom: 1px solid var(--border);
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .dot.r { background: var(--pink); }
  .dot.y { background: var(--gold); }
  .dot.g { background: var(--mint); }

  .terminal-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: rgba(255,255,255,0.3);
    margin-left: 8px;
    letter-spacing: 1px;
  }

  .terminal-body {
    padding: 24px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    line-height: 2;
  }

  .t-comment { color: rgba(255,255,255,0.2); }
  .t-prompt { color: var(--cyan); }
  .t-cmd { color: #fff; }
  .t-out { color: var(--mint); }
  .t-dim { color: rgba(255,255,255,0.4); }
  .t-pink { color: var(--pink); }
  .t-gold { color: var(--gold); }
  .cursor {
    display: inline-block;
    width: 8px;
    height: 14px;
    background: var(--cyan);
    vertical-align: middle;
    animation: blink 1s step-end infinite;
  }
  @keyframes blink { 50% { opacity: 0; } }

  /* ── SECTION TITLES ── */
  .section-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 4px;
    color: var(--cyan);
    text-transform: uppercase;
    opacity: 0.6;
    margin-bottom: 6px;
  }

  .section-title {
    font-family: 'Orbitron', monospace;
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 32px;
    letter-spacing: 1px;
  }

  /* ── FEATURES GRID ── */
  .features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
    margin-bottom: 60px;
  }

  .feat {
    background: var(--dim);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
    transition: border-color 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
  }

  .feat::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0;
    transition: opacity 0.3s;
  }

  .feat:hover { border-color: rgba(0,245,255,0.35); transform: translateY(-2px); }
  .feat:hover::before { opacity: 1; }

  .feat-icon { font-size: 24px; margin-bottom: 10px; display: block; }
  .feat-name {
    font-family: 'Orbitron', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--cyan);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }
  .feat-desc {
    font-size: 12px;
    line-height: 1.7;
    color: rgba(255,255,255,0.55);
  }

  /* ── CONTROLS TABLE ── */
  .controls-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 60px;
  }

  .ctrl {
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    border-bottom: 1px solid var(--border);
    border-right: 1px solid var(--border);
    background: rgba(0,0,0,0.3);
    transition: background 0.15s;
  }

  .ctrl:hover { background: rgba(0,245,255,0.04); }
  .ctrl:nth-child(even) { border-right: none; }
  .ctrl:nth-last-child(-n+2) { border-bottom: none; }

  .kbd {
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    color: var(--void);
    background: var(--cyan);
    border-radius: 4px;
    padding: 2px 10px;
    min-width: 44px;
    text-align: center;
    flex-shrink: 0;
    letter-spacing: 1px;
  }

  .kbd.space { background: var(--lavender); min-width: 80px; font-size: 11px; }
  .ctrl-label { font-size: 12px; color: rgba(255,255,255,0.6); font-family: 'Share Tech Mono', monospace; }

  /* ── RANKS ── */
  .ranks {
    display: flex;
    flex-direction: column;
    gap: 0;
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 60px;
  }

  .rank {
    display: flex;
    align-items: center;
    padding: 14px 24px;
    border-bottom: 1px solid var(--border);
    background: rgba(0,0,0,0.25);
    gap: 20px;
    transition: background 0.15s;
  }

  .rank:last-child { border-bottom: none; }
  .rank:hover { background: rgba(255,45,120,0.04); }

  .rank-dist {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: rgba(255,255,255,0.3);
    min-width: 64px;
    letter-spacing: 1px;
  }

  .rank-bar-wrap {
    flex: 1;
    height: 3px;
    background: rgba(255,255,255,0.06);
    border-radius: 2px;
    overflow: hidden;
  }

  .rank-bar {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--cyan), var(--lavender));
    transition: width 1s ease;
  }

  .rank-title {
    font-family: 'Orbitron', monospace;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    min-width: 180px;
    text-align: right;
    color: #fff;
  }

  .rank:nth-child(1) .rank-title { color: rgba(255,255,255,0.4); }
  .rank:nth-child(2) .rank-title { color: #c0d8ff; }
  .rank:nth-child(3) .rank-title { color: var(--cyan); }
  .rank:nth-child(4) .rank-title { color: var(--lavender); }
  .rank:nth-child(5) .rank-title { color: var(--gold); }
  .rank:nth-child(6) .rank-title { color: var(--pink); text-shadow: 0 0 16px var(--pink); }

  /* ── WISDOM PILLS ── */
  .pills {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 60px;
  }

  .pill {
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    letter-spacing: 2px;
    padding: 8px 18px;
    border-radius: 4px;
    border: 1px solid;
    cursor: default;
    transition: all 0.2s;
  }

  .pill:hover { transform: translateY(-2px); filter: brightness(1.3); }

  .pill.p1 { color: var(--cyan); border-color: rgba(0,245,255,0.3); background: rgba(0,245,255,0.05); }
  .pill.p2 { color: var(--lavender); border-color: rgba(192,132,252,0.3); background: rgba(192,132,252,0.05); }
  .pill.p3 { color: var(--pink); border-color: rgba(255,45,120,0.3); background: rgba(255,45,120,0.05); }
  .pill.p4 { color: var(--gold); border-color: rgba(255,217,102,0.3); background: rgba(255,217,102,0.05); }
  .pill.p5 { color: var(--mint); border-color: rgba(74,222,128,0.3); background: rgba(74,222,128,0.05); }

  /* ── FILE TREE ── */
  .filetree {
    background: rgba(0,0,0,0.5);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 24px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    line-height: 2.2;
    margin-bottom: 60px;
  }

  .ft-dir { color: var(--cyan); }
  .ft-file { color: rgba(255,255,255,0.7); }
  .ft-comment { color: rgba(255,255,255,0.25); }
  .ft-indent { padding-left: 24px; display: block; }

  /* ── CTA ── */
  .cta {
    text-align: center;
    padding: 60px 0 20px;
  }

  .cta-text {
    font-family: 'Orbitron', monospace;
    font-size: 14px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 3px;
    margin-bottom: 28px;
  }

  .btn-group { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }

  .btn {
    font-family: 'Orbitron', monospace;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 14px 32px;
    border-radius: 4px;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s;
    border: none;
    display: inline-block;
  }

  .btn-primary {
    background: var(--cyan);
    color: var(--void);
    box-shadow: 0 0 24px rgba(0,245,255,0.3);
  }
  .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 0 40px rgba(0,245,255,0.5); }

  .btn-ghost {
    background: transparent;
    color: var(--lavender);
    border: 1px solid rgba(192,132,252,0.4);
  }
  .btn-ghost:hover { border-color: var(--lavender); background: rgba(192,132,252,0.06); transform: translateY(-2px); }

  /* ── FOOTER ── */
  .footer {
    text-align: center;
    padding: 40px 0 0;
    border-top: 1px solid var(--border);
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: rgba(255,255,255,0.2);
    letter-spacing: 2px;
    line-height: 2;
  }

  .footer span { color: var(--pink); }

  /* ── DIVIDER ── */
  .divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 60px 0;
  }

  /* ── NEBULA GLOW ── */
  .nebula-glow {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    pointer-events: none;
    z-index: 0;
  }

  .ng1 {
    width: 400px; height: 400px;
    background: rgba(192,132,252,0.06);
    top: -100px; right: -100px;
  }

  .ng2 {
    width: 300px; height: 300px;
    background: rgba(0,245,255,0.05);
    bottom: 200px; left: -80px;
  }

  .ng3 {
    width: 200px; height: 200px;
    background: rgba(255,45,120,0.05);
    top: 60%; right: 10%;
  }

  /* ── SECTION SPACING ── */
  section { margin-bottom: 4px; }

  /* ── RESPONSIVE ── */
  @media (max-width: 600px) {
    .controls-grid { grid-template-columns: 1fr; }
    .ctrl:nth-child(even) { border-right: none; }
    .ctrl:nth-last-child(-n+2) { border-bottom: 1px solid var(--border); }
    .ctrl:last-child { border-bottom: none; }
    .rank-title { min-width: 120px; font-size: 10px; }
  }
</style>
</head>
<body>

<div class="nebula-glow ng1"></div>
<div class="nebula-glow ng2"></div>
<div class="nebula-glow ng3"></div>

<canvas id="starfield"></canvas>

<div class="wrapper">

  <!-- HERO -->
  <div class="hero">
    <div class="hero-eyebrow">✦ terminal productivity ✦</div>
    <span class="hero-kirby">🌸</span>
    <h1 class="hero-title">kirbs.pomodoro</h1>
    <div class="hero-sub">COSMIC TERMINAL TIMER</div>
    <div class="hero-meta">v2.03.2026 &nbsp;·&nbsp; Pilot: <span>Cosmic Kirbs</span> &nbsp;·&nbsp; avsn17</div>

    <div class="terminal">
      <div class="terminal-bar">
        <div class="dot r"></div>
        <div class="dot y"></div>
        <div class="dot g"></div>
        <span class="terminal-label">kirbs.sh — bash</span>
      </div>
      <div class="terminal-body">
        <div><span class="t-comment"># clone the cosmos</span></div>
        <div><span class="t-prompt">$ </span><span class="t-cmd">git clone https://github.com/avsn17/timetodime2.git</span></div>
        <div><span class="t-out">Cloning into 'timetodime2'...</span></div>
        <div><span class="t-out">✓ Starfield loaded. Kirby online. Wisdom unlocked.</span></div>
        <div>&nbsp;</div>
        <div><span class="t-prompt">$ </span><span class="t-cmd">cd timetodime2 &amp;&amp; chmod +x kirbs.sh &amp;&amp; ./kirbs.sh</span></div>
        <div><span class="t-gold">🌌 Welcome, Space Cadet. Your focus journey begins.</span></div>
        <div>&nbsp;</div>
        <div><span class="t-comment"># install the alias</span></div>
        <div><span class="t-prompt">$ </span><span class="t-cmd">echo "alias poyo='cd $(pwd) &amp;&amp; python3 pomodoro_timer.py'" >> ~/.zshrc</span></div>
        <div><span class="t-prompt">$ </span><span class="t-cmd">poyo</span></div>
        <div><span class="t-pink">★ Timer active. May your productivity be guided by wisdom. ★</span></div>
        <div><span class="t-prompt">$ </span><span class="cursor"></span></div>
      </div>
    </div>
  </div>

  <!-- FEATURES -->
  <section>
    <div class="section-label">✦ capabilities</div>
    <div class="section-title">What Kirbs Brings</div>

    <div class="features">
      <div class="feat">
        <span class="feat-icon">✨</span>
        <div class="feat-name">Animated Starfield</div>
        <div class="feat-desc">Live scrolling star background rendered directly in your terminal as you focus.</div>
      </div>
      <div class="feat">
        <span class="feat-icon">🌸</span>
        <div class="feat-name">Kirby Mascot</div>
        <div class="feat-desc">Kirby slides across the screen in real-time, tracking your session progress.</div>
      </div>
      <div class="feat">
        <span class="feat-icon">🏆</span>
        <div class="feat-name">Galactic Rankings</div>
        <div class="feat-desc">Earn titles from Space Cadet to Galactic Overlord. 10 meters = 1 minute of focus.</div>
      </div>
      <div class="feat">
        <span class="feat-icon">💬</span>
        <div class="feat-name">Wisdom Sidebar</div>
        <div class="feat-desc">Chat mid-session for quotes from Brontë, Kant, MJ, Billie, and more.</div>
      </div>
      <div class="feat">
        <span class="feat-icon">📊</span>
        <div class="feat-name">Persistent Stats</div>
        <div class="feat-desc">Leaderboard saved to <code style="color:var(--cyan)">~/.pomodoro_stats.json</code> across all sessions.</div>
      </div>
      <div class="feat">
        <span class="feat-icon">🎵</span>
        <div class="feat-name">Music Signal</div>
        <div class="feat-desc">Writes <code style="color:var(--cyan)">music_signal.txt</code> on completion for external autoplay integration.</div>
      </div>
      <div class="feat">
        <span class="feat-icon">⚙️</span>
        <div class="feat-name">Kirby Config</div>
        <div class="feat-desc">Toggle mood, hydration reminders, music autoplay, and color themes on the fly.</div>
      </div>
      <div class="feat">
        <span class="feat-icon">💾</span>
        <div class="feat-name">Auto-Save</div>
        <div class="feat-desc">Progress is logged on quit or new session — never lose your focus data.</div>
      </div>
    </div>
  </section>

  <hr class="divider">

  <!-- CONTROLS -->
  <section>
    <div class="section-label">⌨️ keybindings</div>
    <div class="section-title">Controls</div>

    <div class="controls-grid">
      <div class="ctrl"><div class="kbd space">SPACE</div><div class="ctrl-label">Pause / Resume</div></div>
      <div class="ctrl"><div class="kbd">C</div><div class="ctrl-label">Open Wisdom Chat</div></div>
      <div class="ctrl"><div class="kbd">S</div><div class="ctrl-label">Stats Leaderboard</div></div>
      <div class="ctrl"><div class="kbd">A</div><div class="ctrl-label">Kirby Config / Settings</div></div>
      <div class="ctrl"><div class="kbd">M</div><div class="ctrl-label">Toggle Music Signal</div></div>
      <div class="ctrl"><div class="kbd">O</div><div class="ctrl-label">Change Background Color</div></div>
      <div class="ctrl"><div class="kbd">N</div><div class="ctrl-label">Save & Start New Session</div></div>
      <div class="ctrl"><div class="kbd">Q</div><div class="ctrl-label">Save & Quit</div></div>
    </div>
  </section>

  <hr class="divider">

  <!-- RANKS -->
  <section>
    <div class="section-label">🚀 progression</div>
    <div class="section-title">Galactic Ranking System</div>

    <div class="ranks">
      <div class="rank">
        <span class="rank-dist">0 m</span>
        <div class="rank-bar-wrap"><div class="rank-bar" style="width:3%"></div></div>
        <span class="rank-title">🛸 SPACE CADET</span>
      </div>
      <div class="rank">
        <span class="rank-dist">100 m</span>
        <div class="rank-bar-wrap"><div class="rank-bar" style="width:20%"></div></div>
        <span class="rank-title">🌙 MOON WALKER</span>
      </div>
      <div class="rank">
        <span class="rank-dist">500 m</span>
        <div class="rank-bar-wrap"><div class="rank-bar" style="width:40%"></div></div>
        <span class="rank-title">☄️ COMET RIDER</span>
      </div>
      <div class="rank">
        <span class="rank-dist">1,000 m</span>
        <div class="rank-bar-wrap"><div class="rank-bar" style="width:60%"></div></div>
        <span class="rank-title">🚀 ORBIT MASTER</span>
      </div>
      <div class="rank">
        <span class="rank-dist">2,500 m</span>
        <div class="rank-bar-wrap"><div class="rank-bar" style="width:80%"></div></div>
        <span class="rank-title">⭐ STAR PILOT</span>
      </div>
      <div class="rank">
        <span class="rank-dist">5,000 m+</span>
        <div class="rank-bar-wrap"><div class="rank-bar" style="width:100%"></div></div>
        <span class="rank-title">🌌 GALACTIC OVERLORD</span>
      </div>
    </div>

    <div style="font-family:'Share Tech Mono',monospace;font-size:11px;color:rgba(255,255,255,0.3);letter-spacing:2px;margin-top:12px;text-align:center;">
      10 meters = 1 minute of focus time
    </div>
  </section>

  <hr class="divider">

  <!-- WISDOM -->
  <section>
    <div class="section-label">💬 wisdom chat</div>
    <div class="section-title">Chat Categories</div>
    <p style="font-size:13px;color:rgba(255,255,255,0.45);margin-bottom:24px;font-family:'Share Tech Mono',monospace;line-height:1.8;">
      Press <span style="color:var(--cyan)">C</span> mid-session to open the sidebar. Type any keyword — or just anything for a random quote.
    </p>
    <div class="pills">
      <span class="pill p1">iro</span>
      <span class="pill p2">bronte</span>
      <span class="pill p3">kant</span>
      <span class="pill p4">lyrics</span>
      <span class="pill p5">heroic</span>
      <span class="pill p1">kirby</span>
      <span class="pill p2">vibe</span>
      <span class="pill p3">wisdom</span>
    </div>
  </section>

  <hr class="divider">

  <!-- FILE TREE -->
  <section>
    <div class="section-label">📦 structure</div>
    <div class="section-title">File Layout</div>

    <div class="filetree">
      <span class="ft-dir">timetodime2/</span>
      <span class="ft-indent"><span class="ft-file">├── pomodoro_timer.py</span> &nbsp;<span class="ft-comment">← main app (run this)</span></span>
      <span class="ft-indent"><span class="ft-file">├── kirbs.sh</span> &nbsp;<span class="ft-comment">← shell launcher with alias setup</span></span>
      <span class="ft-indent"><span class="ft-file">├── music_satellite.py</span> &nbsp;<span class="ft-comment">← optional music listener process</span></span>
      <span class="ft-indent"><span class="ft-file">├── music_signal.txt</span> &nbsp;<span class="ft-comment">← auto-created; triggers autoplay</span></span>
      <span class="ft-indent"><span class="ft-file">└── README.md</span></span>
      <br>
      <span class="ft-comment">~/.pomodoro_stats.json &nbsp;&nbsp;&nbsp;← persistent stats (outside project)</span>
    </div>
  </section>

  <!-- CTA -->
  <div class="cta">
    <div class="cta-text">ready to enter the cosmos?</div>
    <div class="btn-group">
      <a class="btn btn-primary" href="https://github.com/avsn17/timetodime2" target="_blank">
        ↗ View on GitHub
      </a>
      <a class="btn btn-ghost" href="https://github.com/avsn17/timetodime2/archive/refs/heads/main.zip">
        ↓ Download ZIP
      </a>
    </div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div>kirbs.pomodoro &nbsp;·&nbsp; v2.03.2026</div>
    <div>built with <span>♥</span> by avsn17 &nbsp;·&nbsp; Cosmic Kirbs pilot program</div>
    <div style="margin-top:8px;opacity:0.5">may your productivity journey be guided by wisdom 🌌</div>
  </div>

</div>

<script>
// ── STARFIELD ──
const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');

function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

const STAR_COUNT = 200;
const stars = Array.from({ length: STAR_COUNT }, () => ({
  x: Math.random() * window.innerWidth,
  y: Math.random() * window.innerHeight,
  r: Math.random() * 1.4 + 0.3,
  speed: Math.random() * 0.15 + 0.03,
  opacity: Math.random() * 0.6 + 0.1,
  twinkle: Math.random() * Math.PI * 2,
  twinkleSpeed: Math.random() * 0.02 + 0.005,
}));

function drawStars(t) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (const s of stars) {
    s.twinkle += s.twinkleSpeed;
    const op = s.opacity * (0.6 + 0.4 * Math.sin(s.twinkle));
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(255,255,255,${op})`;
    ctx.fill();

    s.y += s.speed;
    if (s.y > canvas.height) {
      s.y = 0;
      s.x = Math.random() * canvas.width;
    }
  }
  requestAnimationFrame(drawStars);
}
requestAnimationFrame(drawStars);

// ── RANK BAR ANIMATION ──
const bars = document.querySelectorAll('.rank-bar');
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.width = e.target.dataset.w || e.target.style.width;
    }
  });
}, { threshold: 0.1 });
bars.forEach(b => {
  b.dataset.w = b.style.width;
  b.style.width = '0%';
  observer.observe(b);
});

// Trigger after a moment for initial view
setTimeout(() => {
  bars.forEach(b => {
    b.style.width = b.dataset.w;
  });
}, 400);
</script>
</body>
</html>