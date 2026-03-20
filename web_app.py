from flask import Flask, render_template_string, jsonify, request
import json, os
from datetime import datetime

app = Flask(__name__)

_IS_VERCEL = os.environ.get('VERCEL') == '1'
_DATA_DIR  = '/tmp' if _IS_VERCEL else 'data'
DATA_FILE  = os.path.join(_DATA_DIR, 'kirby_stats.json')

os.makedirs(_DATA_DIR, exist_ok=True)


def get_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {"tasks": [], "done_today": 0, "total_poyos": 0,
                "water_int": 25, "level": 1, "xp": 0, "last_date": ""}
    with open(DATA_FILE, 'r') as f:
        d = json.load(f)
    today = datetime.now().strftime('%Y-%m-%d')
    if d.get('last_date') != today:
        d['done_today'] = 0
        d['last_date']  = today
        save_data(d)
    return d


def sanitize(t: str) -> str:
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')


def save_data(d: dict) -> None:
    os.makedirs(_DATA_DIR, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(d, f)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KIRBY OS ✦ MISSION CONTROL</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323:wght@400&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
<style>
/* ── Reset & Base ─────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --pink:       #ff5fa0;
  --pink-dim:   #c4437a;
  --cyan:       #00f5ff;
  --cyan-dim:   #007a80;
  --gold:       #ffd84d;
  --green:      #39ff6e;
  --bg:         #05060f;
  --bg2:        #0b0e22;
  --panel:      #0d1128;
  --border:     #1e2a5e;
  --border-hi:  #3a4f9e;
  --text:       #dce8ff;
  --text-dim:   #6a7aaa;
  --font-pixel: 'Press Start 2P', monospace;
  --font-vt:    'VT323', monospace;
  --glow-pink:  0 0 12px #ff5fa088, 0 0 30px #ff5fa033;
  --glow-cyan:  0 0 12px #00f5ff88, 0 0 30px #00f5ff33;
}

html, body {
  height: 100%; width: 100%;
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-vt);
  font-size: 18px;
  overflow: hidden;
}

/* ── Starfield ────────────────────────────────────────────────────── */
#canvas-bg {
  position: fixed; inset: 0;
  pointer-events: none; z-index: 0;
}

/* ── Scanlines overlay ────────────────────────────────────────────── */
body::after {
  content: '';
  position: fixed; inset: 0; z-index: 1;
  pointer-events: none;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.13) 2px,
    rgba(0,0,0,0.13) 4px
  );
}

/* ── Layout ───────────────────────────────────────────────────────── */
#app {
  position: relative; z-index: 2;
  height: 100vh;
  display: grid;
  grid-template-columns: 340px 1fr;
  grid-template-rows: 44px 1fr;
  gap: 0;
  max-width: 960px;
  margin: 0 auto;
  padding: 16px;
  gap: 12px;
}

/* ── Top bar ──────────────────────────────────────────────────────── */
#topbar {
  grid-column: 1 / -1;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 4px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
}
#topbar .logo {
  font-family: var(--font-pixel);
  font-size: 9px;
  color: var(--pink);
  text-shadow: var(--glow-pink);
  letter-spacing: 2px;
}
#topbar .sys-info {
  font-family: var(--font-pixel);
  font-size: 7px;
  color: var(--text-dim);
  display: flex; gap: 18px;
}
#topbar .sys-info span { color: var(--cyan); }

/* ── Left Panel — Kirby ───────────────────────────────────────────── */
#left-panel {
  display: flex; flex-direction: column; gap: 10px;
}

.pixel-box {
  background: var(--panel);
  border: 2px solid var(--border);
  border-radius: 4px;
  position: relative;
  /* pixel corner decoration */
}
.pixel-box::before {
  content: '';
  position: absolute; inset: 3px;
  border: 1px solid var(--border-hi);
  border-radius: 2px;
  pointer-events: none;
  opacity: 0.4;
}

/* Kirby stage */
#kirby-stage {
  padding: 18px 0 10px;
  text-align: center;
  cursor: pointer;
  flex-shrink: 0;
  border: 2px solid var(--pink-dim);
  transition: border-color 0.2s;
}
#kirby-stage:hover { border-color: var(--pink); }
#kirby-stage:hover #kirby-sprite { filter: drop-shadow(0 0 18px var(--pink)); }

#kirby-sprite {
  width: 120px; height: 120px;
  object-fit: contain;
  filter: drop-shadow(0 0 10px var(--pink));
  animation: float 3.2s ease-in-out infinite;
  display: block; margin: 0 auto 8px;
  image-rendering: pixelated;
}
@keyframes float {
  0%, 100% { transform: translateY(0) rotate(-1deg); }
  50%       { transform: translateY(-12px) rotate(1deg); }
}

.stage-label {
  font-family: var(--font-pixel);
  font-size: 6px;
  color: var(--pink);
  letter-spacing: 3px;
  text-shadow: var(--glow-pink);
  margin-bottom: 4px;
}
.stage-sub {
  font-size: 16px;
  color: var(--text-dim);
}

/* Stats box */
#stats-box { padding: 14px 16px; }
.stat-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 5px 0;
  border-bottom: 1px solid var(--border);
  font-size: 17px;
}
.stat-row:last-child { border-bottom: none; }
.stat-label { color: var(--text-dim); }
.stat-val   { color: var(--gold); font-family: var(--font-pixel); font-size: 8px; }
.stat-val.cyan  { color: var(--cyan); }
.stat-val.green { color: var(--green); }

/* XP bar inside stats */
.xp-track {
  height: 6px;
  background: var(--border);
  border-radius: 0;
  overflow: hidden;
  margin-top: 8px;
}
.xp-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--cyan), var(--green));
  width: 0%;
  transition: width 0.8s cubic-bezier(.23,1,.32,1);
  box-shadow: 0 0 6px var(--cyan);
}

/* Water box */
#water-box {
  padding: 14px 16px;
  border: 2px solid var(--cyan-dim);
  flex-shrink: 0;
}
.water-header {
  font-family: var(--font-pixel);
  font-size: 6px;
  color: var(--cyan);
  text-shadow: var(--glow-cyan);
  letter-spacing: 2px;
  margin-bottom: 10px;
}
.water-display {
  display: flex; align-items: baseline; gap: 10px;
  margin-bottom: 8px;
}
#w-timer {
  font-family: var(--font-pixel);
  font-size: 20px;
  color: var(--cyan);
  text-shadow: var(--glow-cyan);
  line-height: 1;
}
.water-int-row {
  font-size: 15px; color: var(--text-dim);
  display: flex; align-items: center; gap: 6px;
}
#int-val {
  width: 36px;
  background: var(--bg2);
  border: 1px solid var(--border-hi);
  color: var(--cyan);
  font-family: var(--font-pixel);
  font-size: 8px;
  text-align: center;
  padding: 3px;
  outline: none;
}
#int-val:focus { border-color: var(--cyan); box-shadow: var(--glow-cyan); }

/* water progress bar */
.water-track {
  height: 4px; background: var(--border);
  margin-top: 6px; overflow: hidden;
}
.water-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--cyan-dim), var(--cyan));
  width: 100%;
  transition: width 1s linear;
  box-shadow: 0 0 4px var(--cyan);
}

/* ── Right Panel — Mission Control ────────────────────────────────── */
#right-panel {
  display: flex; flex-direction: column; gap: 10px;
  min-height: 0;
}

/* Mission progress */
#progress-box { padding: 14px 16px; flex-shrink: 0; }
.progress-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 10px;
}
.progress-title {
  font-family: var(--font-pixel);
  font-size: 6px;
  color: var(--pink);
  letter-spacing: 2px;
}
#progress-pct {
  font-family: var(--font-pixel);
  font-size: 9px;
  color: var(--pink);
  text-shadow: var(--glow-pink);
}
.mission-track {
  height: 10px; background: var(--border);
  border: 1px solid var(--border-hi);
  overflow: hidden; position: relative;
}
.mission-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--pink), #ff1a6e);
  width: 0%;
  transition: width 1s cubic-bezier(.23,1,.32,1);
  box-shadow: 0 0 8px var(--pink);
  position: relative;
}
.mission-fill::after {
  content: '';
  position: absolute; right: 0; top: 0; bottom: 0;
  width: 3px;
  background: white;
  opacity: 0.6;
}

/* Task list */
#task-box {
  flex: 1; min-height: 0;
  padding: 0;
  display: flex; flex-direction: column;
  border: 2px solid var(--border);
}
.task-box-header {
  padding: 10px 16px;
  border-bottom: 1px solid var(--border);
  font-family: var(--font-pixel);
  font-size: 6px;
  color: var(--text-dim);
  letter-spacing: 2px;
  display: flex; justify-content: space-between;
  flex-shrink: 0;
}
#task-count { color: var(--gold); }

#task-list {
  flex: 1; overflow-y: auto;
  padding: 6px 10px;
  scrollbar-width: thin;
  scrollbar-color: var(--border-hi) transparent;
}

.task-item {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 10px;
  margin: 4px 0;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-left: 3px solid var(--pink-dim);
  font-size: 18px;
  color: var(--text);
  transition: border-color 0.15s, background 0.15s;
  animation: slideIn 0.2s ease-out;
}
.task-item:hover {
  background: #141830;
  border-color: var(--border-hi);
  border-left-color: var(--pink);
}
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-8px); }
  to   { opacity: 1; transform: translateX(0); }
}

.task-text {
  flex: 1;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.task-star { color: var(--gold); flex-shrink: 0; font-size: 14px; }

.inhale-btn {
  flex-shrink: 0;
  background: transparent;
  border: 1px solid var(--pink-dim);
  color: var(--pink);
  font-family: var(--font-pixel);
  font-size: 6px;
  padding: 4px 7px;
  cursor: pointer;
  letter-spacing: 1px;
  transition: all 0.15s;
}
.inhale-btn:hover {
  background: var(--pink);
  color: var(--bg);
  border-color: var(--pink);
  box-shadow: var(--glow-pink);
}
.inhale-btn:active { transform: scale(0.95); }

/* Empty state */
#empty-state {
  display: none;
  flex-direction: column; align-items: center; justify-content: center;
  height: 100%;
  color: var(--text-dim);
  font-size: 20px;
  gap: 8px;
  padding: 20px;
  text-align: center;
}
#empty-state .empty-icon { font-size: 36px; }
#empty-state .empty-hint {
  font-family: var(--font-pixel);
  font-size: 6px;
  color: var(--border-hi);
  line-height: 2;
  letter-spacing: 1px;
}

/* Add task */
#add-box {
  padding: 12px 14px;
  flex-shrink: 0;
  border: 2px solid var(--border);
  display: flex; gap: 8px; align-items: center;
}
#task-input {
  flex: 1;
  background: var(--bg2);
  border: 1px solid var(--border-hi);
  color: var(--text);
  font-family: var(--font-vt);
  font-size: 20px;
  padding: 8px 12px;
  outline: none;
  caret-color: var(--pink);
}
#task-input::placeholder { color: var(--text-dim); }
#task-input:focus {
  border-color: var(--pink-dim);
  background: #0f1225;
}
#add-btn {
  background: var(--pink);
  color: var(--bg);
  border: none;
  font-family: var(--font-pixel);
  font-size: 7px;
  padding: 10px 14px;
  cursor: pointer;
  letter-spacing: 1px;
  transition: all 0.15s;
  flex-shrink: 0;
}
#add-btn:hover {
  background: #ff80b8;
  box-shadow: var(--glow-pink);
  transform: translateY(-1px);
}
#add-btn:active { transform: translateY(0) scale(0.97); }

/* ── Boot animation ───────────────────────────────────────────────── */
#boot-overlay {
  position: fixed; inset: 0; z-index: 100;
  background: var(--bg);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 16px;
  animation: bootFade 0.5s ease 1.8s forwards;
}
@keyframes bootFade {
  to { opacity: 0; pointer-events: none; }
}
.boot-logo {
  font-family: var(--font-pixel);
  font-size: 13px;
  color: var(--pink);
  text-shadow: var(--glow-pink);
  letter-spacing: 4px;
  animation: blinkIn 0.3s steps(1) 0.2s both;
}
.boot-sub {
  font-family: var(--font-pixel);
  font-size: 7px;
  color: var(--cyan);
  letter-spacing: 3px;
  animation: blinkIn 0.3s steps(1) 0.6s both;
}
.boot-bar-wrap {
  width: 200px; height: 8px;
  border: 1px solid var(--border-hi);
  overflow: hidden;
  animation: blinkIn 0.3s steps(1) 0.9s both;
}
.boot-bar-fill {
  height: 100%;
  background: var(--pink);
  box-shadow: var(--glow-pink);
  animation: bootLoad 0.8s ease 1s forwards;
  width: 0%;
}
@keyframes bootLoad { to { width: 100%; } }
@keyframes blinkIn { from { opacity: 0; } to { opacity: 1; } }

/* ── Poyo toast ───────────────────────────────────────────────────── */
#poyo-toast {
  position: fixed; bottom: 20px; right: 20px; z-index: 50;
  background: var(--panel);
  border: 2px solid var(--pink);
  padding: 10px 18px;
  font-family: var(--font-pixel);
  font-size: 7px;
  color: var(--pink);
  box-shadow: var(--glow-pink);
  opacity: 0; pointer-events: none;
  transform: translateY(10px);
  transition: all 0.25s;
  letter-spacing: 1px;
}
#poyo-toast.show {
  opacity: 1; transform: translateY(0);
}

/* ── Responsive ───────────────────────────────────────────────────── */
@media (max-width: 700px) {
  #app {
    grid-template-columns: 1fr;
    grid-template-rows: 44px auto 1fr;
    overflow-y: auto;
    height: auto; min-height: 100vh;
  }
  #left-panel { order: 2; }
  #right-panel { order: 3; min-height: 60vh; }
  body { overflow: auto; }
}
</style>
</head>
<body>

<!-- Boot splash -->
<div id="boot-overlay">
  <div class="boot-logo">KIRBY OS</div>
  <div class="boot-sub">MISSION CONTROL v3.0</div>
  <div class="boot-bar-wrap"><div class="boot-bar-fill"></div></div>
</div>

<canvas id="canvas-bg"></canvas>
<div id="poyo-toast">POYO! ✦</div>

<div id="app">

  <!-- Top bar -->
  <div id="topbar">
    <div class="logo">✦ KIRBY OS ✦</div>
    <div class="sys-info">
      <div>LVL <span id="lvl-val">1</span></div>
      <div>POYOS <span id="total-val">0</span></div>
      <div id="clock-val">--:--</div>
    </div>
  </div>

  <!-- Left panel -->
  <div id="left-panel">

    <div id="kirby-stage" class="pixel-box" onclick="playPoyo()">
      <img id="kirby-sprite"
           src="https://upload.wikimedia.org/wikipedia/en/3/35/Kirby_%28character%29.png"
           onerror="this.style.display='none'"
           alt="Kirby">
      <div class="stage-label">PILOT</div>
      <div class="stage-sub">click for poyo!</div>
    </div>

    <div id="stats-box" class="pixel-box">
      <div class="stat-row">
        <span class="stat-label">LEVEL</span>
        <span class="stat-val cyan" id="stat-lvl">1</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">XP PROGRESS</span>
        <span class="stat-val" id="stat-xp">0 / 100</span>
      </div>
      <div class="xp-track"><div class="xp-fill" id="xp-fill"></div></div>
      <div class="stat-row" style="margin-top:8px">
        <span class="stat-label">TOTAL POYOS</span>
        <span class="stat-val green" id="stat-poyos">0</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">TODAY</span>
        <span class="stat-val" id="stat-today">0</span>
      </div>
    </div>

    <div id="water-box" class="pixel-box">
      <div class="water-header">💧 HYDRATION TIMER</div>
      <div class="water-display">
        <div id="w-timer">--:--</div>
      </div>
      <div class="water-int-row">
        interval:
        <input type="number" id="int-val" value="25" min="1" max="99" onchange="saveInt()">
        min
      </div>
      <div class="water-track"><div class="water-fill" id="water-fill"></div></div>
    </div>

  </div><!-- /left-panel -->

  <!-- Right panel -->
  <div id="right-panel">

    <div id="progress-box" class="pixel-box">
      <div class="progress-header">
        <span class="progress-title">⬛ MISSION PROGRESS</span>
        <span id="progress-pct">0%</span>
      </div>
      <div class="mission-track">
        <div class="mission-fill" id="p-bar"></div>
      </div>
    </div>

    <div id="task-box" class="pixel-box">
      <div class="task-box-header">
        <span>ACTIVE MISSIONS</span>
        <span id="task-count">0 queued</span>
      </div>
      <div id="task-list">
        <div id="empty-state">
          <div class="empty-icon">⭐</div>
          <div>no missions queued</div>
          <div class="empty-hint">add a task below<br>and inhale it when done</div>
        </div>
      </div>
    </div>

    <div id="add-box" class="pixel-box">
      <input type="text" id="task-input" placeholder="new mission..." maxlength="80">
      <button id="add-btn" onclick="addTask()">POYO!</button>
    </div>

  </div><!-- /right-panel -->
</div><!-- /app -->

<script>
// ── Starfield canvas ─────────────────────────────────────────────────
(function() {
  const c = document.getElementById('canvas-bg');
  const ctx = c.getContext('2d');
  const stars = [];
  function resize() { c.width = window.innerWidth; c.height = window.innerHeight; }
  window.addEventListener('resize', resize); resize();
  for (let i = 0; i < 160; i++) {
    stars.push({
      x: Math.random(), y: Math.random(),
      r: Math.random() * 1.4 + 0.2,
      a: Math.random(),
      speed: Math.random() * 0.004 + 0.001,
      phase: Math.random() * Math.PI * 2
    });
  }
  function draw(t) {
    ctx.clearRect(0, 0, c.width, c.height);
    stars.forEach(s => {
      const alpha = 0.2 + 0.6 * (0.5 + 0.5 * Math.sin(t * s.speed * 60 + s.phase));
      ctx.beginPath();
      ctx.arc(s.x * c.width, s.y * c.height, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(180,210,255,${alpha})`;
      ctx.fill();
    });
    requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);
})();

// ── State ────────────────────────────────────────────────────────────
let waterSecs    = null;
let waterTotal   = null;
let notifPerm    = Notification.permission;

// ── Clock ────────────────────────────────────────────────────────────
function tickClock() {
  const now = new Date();
  const h = String(now.getHours()).padStart(2,'0');
  const m = String(now.getMinutes()).padStart(2,'0');
  document.getElementById('clock-val').textContent = h + ':' + m;
}
tickClock();
setInterval(tickClock, 10000);

// ── Toast ────────────────────────────────────────────────────────────
function showToast(msg) {
  const t = document.getElementById('poyo-toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2200);
}

// ── Data ─────────────────────────────────────────────────────────────
async function update() {
  const r = await fetch('/api/data');
  const d = await r.json();

  const savedInt = parseInt(d.water_int, 10) || 25;
  document.getElementById('int-val').value = savedInt;
  if (waterSecs === null) {
    waterTotal = savedInt * 60;
    waterSecs  = waterTotal;
  }

  const total = d.tasks.length + d.done_today;
  const pct   = total === 0 ? 0 : Math.round((d.done_today / total) * 100);

  document.getElementById('p-bar').style.width     = pct + '%';
  document.getElementById('progress-pct').textContent = pct + '%';
  document.getElementById('lvl-val').textContent   = d.level;
  document.getElementById('stat-lvl').textContent  = d.level;
  document.getElementById('stat-poyos').textContent = d.total_poyos;
  document.getElementById('stat-today').textContent = d.done_today;
  document.getElementById('total-val').textContent  = d.total_poyos;
  document.getElementById('stat-xp').textContent    = (d.xp % 100) + ' / 100';
  document.getElementById('xp-fill').style.width    = (d.xp % 100) + '%';
  document.getElementById('task-count').textContent = d.tasks.length
    ? d.tasks.length + ' queued'
    : 'all clear!';

  if (pct === 100 && d.done_today > 0) {
    confetti({ particleCount: 120, spread: 80, origin: { y: 0.55 },
               colors: ['#ff5fa0','#ffd84d','#00f5ff','#39ff6e'] });
    showToast('ALL MISSIONS COMPLETE ✦');
  }

  const list = document.getElementById('task-list');
  const empty = document.getElementById('empty-state');

  if (d.tasks.length === 0) {
    list.innerHTML = '';
    list.appendChild(empty);
    empty.style.display = 'flex';
  } else {
    empty.style.display = 'none';
    list.innerHTML = d.tasks.map((t, i) => `
      <div class="task-item">
        <span class="task-star">▸</span>
        <span class="task-text">${t}</span>
        <button class="inhale-btn" onclick="inhale(${i})">INHALE</button>
      </div>`).join('');
  }
}

// ── Water timer ───────────────────────────────────────────────────────
setInterval(() => {
  if (waterSecs === null) return;
  if (waterSecs > 0) waterSecs--;
  else {
    const interval = parseInt(document.getElementById('int-val').value, 10) || 25;
    waterTotal = interval * 60;
    waterSecs  = waterTotal;
    showToast('💧 TRINKEN! WATER TIME!');
    if (notifPerm === 'granted')
      new Notification('💧 Hydration Check!', { body: 'Zeit für einen Schluck Wasser!' });
  }
  const m  = Math.floor(waterSecs / 60);
  const sc = waterSecs % 60;
  document.getElementById('w-timer').textContent = m + ':' + (sc < 10 ? '0' : '') + sc;
  if (waterTotal) {
    document.getElementById('water-fill').style.width = (waterSecs / waterTotal * 100) + '%';
  }
}, 1000);

// ── Config ────────────────────────────────────────────────────────────
async function saveInt() {
  const v = parseInt(document.getElementById('int-val').value, 10);
  waterTotal = v * 60;
  waterSecs  = waterTotal;
  await fetch('/api/config', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ interval: v })
  });
}

// ── Add task ──────────────────────────────────────────────────────────
async function addTask() {
  const input = document.getElementById('task-input');
  const v = input.value.trim();
  if (!v) return;
  await fetch('/api/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task: v })
  });
  input.value = '';
  update();
}

document.getElementById('task-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') addTask();
});

// ── Inhale ────────────────────────────────────────────────────────────
async function inhale(i) {
  await fetch('/api/inhale/' + i, { method: 'POST' });
  showToast('POYO! +20 XP ✦');
  update();
}

// ── Kirby click ───────────────────────────────────────────────────────
function playPoyo() {
  if (Notification.permission === 'default') {
    Notification.requestPermission().then(p => {
      notifPerm = p;
      if (p === 'granted') new Notification('🌟 Poyo!', { body: 'Kirby glaubt an dich!' });
    });
  } else if (Notification.permission === 'granted') {
    new Notification('🌟 Poyo!', { body: 'Kirby glaubt an dich!' });
  }
  showToast('POYO! ✦ KIRBY BELIEVES IN YOU');
}

update();
setInterval(update, 15000);
</script>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data')
def data():
    return jsonify(get_data())

@app.route('/api/config', methods=['POST'])
def config():
    d = get_data()
    d['water_int'] = int(request.json['interval'])
    save_data(d)
    return jsonify(ok=True)

@app.route('/api/add', methods=['POST'])
def add():
    d = get_data()
    d['tasks'].append(sanitize(request.json['task']))
    save_data(d)
    return jsonify(ok=True)

@app.route('/api/inhale/<int:i>', methods=['POST'])
def inhale(i):
    d = get_data()
    if 0 <= i < len(d['tasks']):
        d['tasks'].pop(i)
        d['done_today']  += 1
        d['total_poyos'] += 1
        d['xp']          += 20
        if d['xp'] >= 100:
            d['level'] += 1
            d['xp']     = 0
        save_data(d)
    return jsonify(ok=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
