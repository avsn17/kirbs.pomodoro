from flask import Flask, render_template_string, jsonify, request
import json, os, urllib.request, urllib.error
from datetime import datetime

app = Flask(__name__)

# ── Storage backend — Vercel KV (Redis) when available, local file otherwise ──
_IS_VERCEL = os.environ.get('VERCEL') == '1'
_DATA_DIR  = '/tmp' if _IS_VERCEL else 'data'
DATA_FILE  = os.path.join(_DATA_DIR, 'kirby_stats.json')
KV_URL     = os.environ.get('KV_REST_API_URL')
KV_TOKEN   = os.environ.get('KV_REST_API_TOKEN')
KV_KEY     = 'kirby_stats'
TASK_LIMIT = 20

os.makedirs(_DATA_DIR, exist_ok=True)

DEFAULTS = lambda: {
    "tasks": [], "done_today": 0, "total_poyos": 0,
    "water_int": 25, "level": 1, "xp": 0, "last_date": ""
}

# ── KV helpers ─────────────────────────────────────────────────────────────────
def _kv_get() -> dict | None:
    try:
        payload = json.dumps(["GET", KV_KEY]).encode()
        req = urllib.request.Request(
            KV_URL, data=payload,
            headers={"Authorization": f"Bearer {KV_TOKEN}",
                     "Content-Type": "application/json"},
            method="POST")
        with urllib.request.urlopen(req, timeout=5) as r:
            result = json.loads(r.read()).get('result')
        return json.loads(result) if result else None
    except Exception:
        return None

def _kv_set(data: dict) -> bool:
    try:
        payload = json.dumps(["SET", KV_KEY, json.dumps(data)]).encode()
        req = urllib.request.Request(
            KV_URL, data=payload,
            headers={"Authorization": f"Bearer {KV_TOKEN}",
                     "Content-Type": "application/json"},
            method="POST")
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False

# ── Data access ────────────────────────────────────────────────────────────────
def get_data() -> dict:
    d = None
    if KV_URL and KV_TOKEN:
        d = _kv_get()
    if d is None:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE) as f:
                d = json.load(f)
        else:
            d = DEFAULTS()
    today = datetime.now().strftime('%Y-%m-%d')
    if d.get('last_date') != today:
        d['done_today'] = 0
        d['last_date']  = today
        save_data(d)
    return d

def save_data(d: dict) -> None:
    if KV_URL and KV_TOKEN:
        _kv_set(d)
    os.makedirs(_DATA_DIR, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(d, f)

def sanitize(t: str) -> str:
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KIRBY OS ✦ MISSION CONTROL</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='26' font-size='28'>🌟</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root{
  --pink:#ff5fa0;--pink-dim:#c4437a;--pink-dark:#7a1f49;
  --cyan:#00f5ff;--cyan-dim:#007a80;
  --gold:#ffd84d;--green:#39ff6e;--red:#ff4466;
  --bg:#05060f;--bg2:#0b0e22;--panel:#0d1128;
  --border:#1e2a5e;--border-hi:#3a4f9e;
  --text:#dce8ff;--text-dim:#6a7aaa;
  --fp:'Press Start 2P',monospace;--fv:'VT323',monospace;
  --gp:0 0 12px #ff5fa088,0 0 30px #ff5fa033;
  --gc:0 0 12px #00f5ff88,0 0 30px #00f5ff33;
}

html,body{height:100%;width:100%;background:var(--bg);color:var(--text);font-family:var(--fv);font-size:18px}
body{overflow:hidden}

#canvas-bg{position:fixed;inset:0;pointer-events:none;z-index:0}
body::after{content:'';position:fixed;inset:0;z-index:1;pointer-events:none;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.13) 2px,rgba(0,0,0,.13) 4px)}

/* ── Layout ── */
#app{position:relative;z-index:2;height:100vh;display:grid;
  grid-template-columns:320px 1fr;grid-template-rows:48px 1fr;
  max-width:960px;margin:0 auto;padding:14px;gap:10px}

/* ── Topbar ── */
#topbar{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--border);padding-bottom:8px}
.logo{font-family:var(--fp);font-size:9px;color:var(--pink);text-shadow:var(--gp);letter-spacing:2px}
.sys-info{font-family:var(--fp);font-size:7px;color:var(--text-dim);display:flex;gap:16px;align-items:center}
.sys-info span{color:var(--cyan)}
#conn-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--text-dim);
  margin-right:4px;transition:background .4s}
#conn-dot.ok{background:var(--green);box-shadow:0 0 6px var(--green)}
#conn-dot.err{background:var(--red);box-shadow:0 0 6px var(--red)}

/* ── Pixel box ── */
.pixel-box{background:var(--panel);border:2px solid var(--border);position:relative}
.pixel-box::before{content:'';position:absolute;inset:3px;border:1px solid var(--border-hi);
  pointer-events:none;opacity:.35}

/* ── Left panel ── */
#left-panel{display:flex;flex-direction:column;gap:10px;min-height:0}

/* Kirby stage */
#kirby-stage{padding:16px 0 10px;text-align:center;cursor:pointer;flex-shrink:0;
  border:2px solid var(--pink-dim);transition:border-color .2s;overflow:hidden}
#kirby-stage:hover{border-color:var(--pink)}
#kirby-stage:hover #kirby-sprite{filter:drop-shadow(0 0 22px var(--pink))}
#kirby-stage:active #kirby-sprite{animation:kirby-squish .35s ease-out}

#kirby-sprite{width:112px;height:112px;object-fit:contain;display:block;margin:0 auto 8px;
  filter:drop-shadow(0 0 10px var(--pink));image-rendering:pixelated;
  animation:kirby-float 3.4s ease-in-out infinite}
@keyframes kirby-float{
  0%{transform:translateY(0) scaleX(1) scaleY(1) rotate(-1deg)}
  40%{transform:translateY(-11px) scaleX(.97) scaleY(1.04) rotate(.5deg)}
  60%{transform:translateY(-13px) scaleX(.96) scaleY(1.05) rotate(1deg)}
  100%{transform:translateY(0) scaleX(1) scaleY(1) rotate(-1deg)}
}
@keyframes kirby-squish{
  0%{transform:scaleX(1) scaleY(1)}
  25%{transform:scaleX(1.3) scaleY(.7)}
  60%{transform:scaleX(.9) scaleY(1.15)}
  100%{transform:scaleX(1) scaleY(1)}
}
@keyframes kirby-poke{
  0%,100%{transform:translateX(0)}
  20%{transform:translateX(-4px) rotate(-3deg)}
  50%{transform:translateX(6px) rotate(3deg)}
  80%{transform:translateX(-3px)}
}
.stage-label{font-family:var(--fp);font-size:6px;color:var(--pink);
  letter-spacing:3px;text-shadow:var(--gp);margin-bottom:4px}
.stage-sub{font-size:15px;color:var(--text-dim)}

/* Stats */
#stats-box{padding:12px 14px}
.stat-row{display:flex;justify-content:space-between;align-items:center;
  padding:5px 0;border-bottom:1px solid var(--border);font-size:17px}
.stat-row:last-child{border-bottom:none}
.stat-label{color:var(--text-dim)}
.stat-val{color:var(--gold);font-family:var(--fp);font-size:7px}
.stat-val.cyan{color:var(--cyan)}.stat-val.green{color:var(--green)}
.xp-track{height:5px;background:var(--border);overflow:hidden;margin-top:7px}
.xp-fill{height:100%;background:linear-gradient(90deg,var(--cyan),var(--green));
  width:0%;transition:width .8s cubic-bezier(.23,1,.32,1);box-shadow:0 0 5px var(--cyan)}

/* Water */
#water-box{padding:12px 14px;border:2px solid var(--cyan-dim);flex-shrink:0}
.water-hdr{font-family:var(--fp);font-size:6px;color:var(--cyan);text-shadow:var(--gc);
  letter-spacing:2px;margin-bottom:8px}
#w-timer{font-family:var(--fp);font-size:19px;color:var(--cyan);text-shadow:var(--gc);line-height:1}
#w-timer.urgent{color:var(--gold);text-shadow:0 0 12px var(--gold)}
.water-int-row{font-size:15px;color:var(--text-dim);display:flex;align-items:center;gap:6px;margin-top:6px}
#int-val{width:34px;background:var(--bg2);border:1px solid var(--border-hi);color:var(--cyan);
  font-family:var(--fp);font-size:7px;text-align:center;padding:3px;outline:none}
#int-val:focus{border-color:var(--cyan);box-shadow:var(--gc)}
.water-track{height:4px;background:var(--border);margin-top:6px;overflow:hidden}
.water-fill{height:100%;background:linear-gradient(90deg,var(--cyan-dim),var(--cyan));
  width:100%;transition:width 1s linear;box-shadow:0 0 4px var(--cyan)}

/* ── Right panel ── */
#right-panel{display:flex;flex-direction:column;gap:10px;min-height:0}

/* Progress */
#progress-box{padding:12px 14px;flex-shrink:0}
.prog-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:9px}
.prog-title{font-family:var(--fp);font-size:6px;color:var(--pink);letter-spacing:2px}
#progress-pct{font-family:var(--fp);font-size:9px;color:var(--pink);text-shadow:var(--gp)}
.mission-track{height:10px;background:var(--border);border:1px solid var(--border-hi);overflow:hidden;position:relative}
.mission-fill{height:100%;background:linear-gradient(90deg,var(--pink),#ff1a6e);width:0%;
  transition:width 1s cubic-bezier(.23,1,.32,1);box-shadow:0 0 8px var(--pink);position:relative}
.mission-fill::after{content:'';position:absolute;right:0;top:0;bottom:0;width:3px;background:#fff;opacity:.5}

/* Task list */
#task-box{flex:1;min-height:0;display:flex;flex-direction:column;border:2px solid var(--border)}
.task-hdr{padding:8px 14px;border-bottom:1px solid var(--border);font-family:var(--fp);font-size:6px;
  color:var(--text-dim);letter-spacing:2px;display:flex;justify-content:space-between;flex-shrink:0}
#task-count{color:var(--gold)}
#task-count.limit{color:var(--red)}

#task-list{flex:1;overflow-y:auto;padding:4px 8px;scrollbar-width:thin;scrollbar-color:var(--border-hi) transparent}

.task-item{display:flex;align-items:center;gap:6px;padding:7px 8px;margin:3px 0;
  background:var(--bg2);border:1px solid var(--border);border-left:3px solid var(--pink-dim);
  font-size:17px;color:var(--text);transition:border-color .15s,background .15s;
  animation:slideIn .18s ease-out}
.task-item:hover{background:#141830;border-left-color:var(--pink)}
@keyframes slideIn{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:translateX(0)}}
.task-text{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.task-arrow{color:var(--gold);flex-shrink:0;font-size:13px}

.task-btns{display:flex;gap:4px;flex-shrink:0}
.inhale-btn,.del-btn{border:1px solid;font-family:var(--fp);font-size:6px;
  padding:4px 7px;cursor:pointer;letter-spacing:1px;transition:all .15s;background:transparent}
.inhale-btn{border-color:var(--pink-dim);color:var(--pink)}
.inhale-btn:hover{background:var(--pink);color:var(--bg);border-color:var(--pink);box-shadow:var(--gp)}
.del-btn{border-color:var(--border-hi);color:var(--text-dim)}
.del-btn:hover{background:var(--red);color:#fff;border-color:var(--red);box-shadow:0 0 8px #ff446688}
.inhale-btn:active,.del-btn:active{transform:scale(.94)}

/* Empty */
#empty-state{display:none;flex-direction:column;align-items:center;justify-content:center;
  height:100%;color:var(--text-dim);font-size:18px;gap:7px;padding:20px;text-align:center}
.empty-icon{font-size:32px}
.empty-hint{font-family:var(--fp);font-size:6px;color:var(--border-hi);line-height:2;letter-spacing:1px}

/* Add box */
#add-box{padding:10px 12px;flex-shrink:0;border:2px solid var(--border);display:flex;gap:7px;align-items:center}
#task-input{flex:1;background:var(--bg2);border:1px solid var(--border-hi);color:var(--text);
  font-family:var(--fv);font-size:20px;padding:7px 11px;outline:none;caret-color:var(--pink);min-width:0}
#task-input::placeholder{color:var(--text-dim)}
#task-input:focus{border-color:var(--pink-dim);background:#0f1225}
#add-btn{background:var(--pink);color:var(--bg);border:none;font-family:var(--fp);font-size:7px;
  padding:10px 13px;cursor:pointer;letter-spacing:1px;transition:all .15s;flex-shrink:0;white-space:nowrap}
#add-btn:hover{background:#ff80b8;box-shadow:var(--gp);transform:translateY(-1px)}
#add-btn:active{transform:scale(.96)}
#add-btn:disabled{opacity:.4;cursor:not-allowed;transform:none}

/* Toast */
#toast{position:fixed;bottom:18px;right:18px;z-index:50;background:var(--panel);
  border:2px solid var(--pink);padding:9px 16px;font-family:var(--fp);font-size:7px;
  color:var(--pink);box-shadow:var(--gp);opacity:0;pointer-events:none;
  transform:translateY(8px);transition:all .22s;letter-spacing:1px}
#toast.show{opacity:1;transform:translateY(0)}
#toast.err{border-color:var(--red);color:var(--red);box-shadow:0 0 16px #ff446644}

/* Boot */
#boot{position:fixed;inset:0;z-index:100;background:var(--bg);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;
  animation:bootFade .4s ease 1.9s forwards}
@keyframes bootFade{to{opacity:0;pointer-events:none}}
.boot-logo{font-family:var(--fp);font-size:12px;color:var(--pink);text-shadow:var(--gp);
  letter-spacing:4px;animation:blinkIn .3s steps(1) .2s both}
.boot-sub{font-family:var(--fp);font-size:7px;color:var(--cyan);letter-spacing:3px;
  animation:blinkIn .3s steps(1) .6s both}
.boot-line{font-family:var(--fp);font-size:6px;color:var(--text-dim);letter-spacing:1px;
  animation:blinkIn .3s steps(1) 1s both}
.boot-bar-wrap{width:180px;height:7px;border:1px solid var(--border-hi);overflow:hidden;
  animation:blinkIn .3s steps(1) 1s both}
.boot-bar-fill{height:100%;background:var(--pink);box-shadow:var(--gp);
  animation:bootLoad .7s ease 1.1s forwards;width:0%}
@keyframes bootLoad{to{width:100%}}
@keyframes blinkIn{from{opacity:0}to{opacity:1}}

/* ── Mobile ── */
@media(max-width:680px){
  body{overflow-y:auto}
  #app{grid-template-columns:1fr;grid-template-rows:auto;height:auto;min-height:100vh;padding:10px;gap:8px}
  #topbar{grid-column:1/-1}
  #left-panel{order:2}
  #right-panel{order:3;min-height:70vh}
  #kirby-sprite{width:90px;height:90px}
  .logo{font-size:7px}
  .sys-info{gap:10px;font-size:6px}
  #w-timer{font-size:15px}
  #task-input{font-size:18px}
}
</style>
</head>
<body>

<div id="boot">
  <div class="boot-logo">KIRBY OS</div>
  <div class="boot-sub">MISSION CONTROL</div>
  <div class="boot-line">LOADING SYSTEMS...</div>
  <div class="boot-bar-wrap"><div class="boot-bar-fill"></div></div>
</div>

<canvas id="canvas-bg"></canvas>
<div id="toast"></div>

<div id="app">

  <div id="topbar">
    <div class="logo">✦ KIRBY OS ✦</div>
    <div class="sys-info">
      <div>LVL <span id="lvl-val">1</span></div>
      <div>POYOS <span id="total-val">0</span></div>
      <div><span id="conn-dot"></span><span id="kv-label">LOCAL</span></div>
      <div id="clock-val">--:--</div>
    </div>
  </div>

  <!-- Left panel -->
  <div id="left-panel">

    <div id="kirby-stage" class="pixel-box" onclick="playPoyo()">
      <img id="kirby-sprite"
           src="https://upload.wikimedia.org/wikipedia/en/3/35/Kirby_%28character%29.png"
           onerror="this.style.display='none'" alt="Kirby">
      <div class="stage-label">PILOT</div>
      <div class="stage-sub">click for poyo ♡</div>
    </div>

    <div id="stats-box" class="pixel-box">
      <div class="stat-row">
        <span class="stat-label">LEVEL</span>
        <span class="stat-val cyan" id="stat-lvl">1</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">XP</span>
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
      <div class="water-hdr">💧 HYDRATION TIMER</div>
      <div id="w-timer">--:--</div>
      <div class="water-int-row">
        interval: <input type="number" id="int-val" value="25" min="1" max="99" onchange="saveInt()"> min
      </div>
      <div class="water-track"><div class="water-fill" id="water-fill"></div></div>
    </div>

  </div>

  <!-- Right panel -->
  <div id="right-panel">

    <div id="progress-box" class="pixel-box">
      <div class="prog-hdr">
        <span class="prog-title">⬛ MISSION PROGRESS</span>
        <span id="progress-pct">0%</span>
      </div>
      <div class="mission-track"><div class="mission-fill" id="p-bar"></div></div>
    </div>

    <div id="task-box" class="pixel-box">
      <div class="task-hdr">
        <span>ACTIVE MISSIONS</span>
        <span id="task-count">0 queued</span>
      </div>
      <div id="task-list">
        <div id="empty-state">
          <div class="empty-icon">⭐</div>
          <div>no missions queued</div>
          <div class="empty-hint">type below + enter<br>inhale to complete · ✕ to delete</div>
        </div>
      </div>
    </div>

    <div id="add-box" class="pixel-box">
      <input type="text" id="task-input" placeholder="new mission..." maxlength="80">
      <button id="add-btn" onclick="addTask()">POYO!</button>
    </div>

  </div>
</div>

<script>
// ── Starfield ────────────────────────────────────────────────────────
(()=>{
  const c=document.getElementById('canvas-bg'),ctx=c.getContext('2d'),stars=[];
  const resize=()=>{c.width=innerWidth;c.height=innerHeight};
  window.addEventListener('resize',resize);resize();
  for(let i=0;i<160;i++) stars.push({x:Math.random(),y:Math.random(),
    r:Math.random()*1.3+.2,speed:Math.random()*.004+.001,phase:Math.random()*Math.PI*2});
  const draw=t=>{
    ctx.clearRect(0,0,c.width,c.height);
    stars.forEach(s=>{
      const a=.15+.65*(0.5+0.5*Math.sin(t*s.speed*60+s.phase));
      ctx.beginPath();ctx.arc(s.x*c.width,s.y*c.height,s.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(180,210,255,${a})`;ctx.fill();
    });
    requestAnimationFrame(draw);
  };
  requestAnimationFrame(draw);
})();

// ── State ────────────────────────────────────────────────────────────
const TASK_LIMIT = {{ task_limit }};
let waterSecs=null, waterTotal=null, notifPerm=Notification.permission;

// Persist water timer across page refreshes via sessionStorage
function loadWaterState(defaultSecs){
  const saved = sessionStorage.getItem('waterSecs');
  const savedAt = parseInt(sessionStorage.getItem('waterSavedAt')||'0');
  if(saved && savedAt){
    const elapsed = Math.floor((Date.now()-savedAt)/1000);
    const remaining = parseInt(saved)-elapsed;
    return remaining > 0 ? remaining : defaultSecs;
  }
  return defaultSecs;
}
function saveWaterState(){
  if(waterSecs!==null){
    sessionStorage.setItem('waterSecs', waterSecs);
    sessionStorage.setItem('waterSavedAt', Date.now());
  }
}

// ── Clock ────────────────────────────────────────────────────────────
(function tickClock(){
  const now=new Date();
  document.getElementById('clock-val').textContent=
    String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0');
  setTimeout(tickClock, (60-now.getSeconds())*1000);
})();

// ── Toast ────────────────────────────────────────────────────────────
let _toastTimer=null;
function showToast(msg, isErr=false){
  const t=document.getElementById('toast');
  t.textContent=msg;
  t.className='show'+(isErr?' err':'');
  clearTimeout(_toastTimer);
  _toastTimer=setTimeout(()=>t.className='',isErr?3000:2200);
}

// ── API wrapper with error handling ──────────────────────────────────
async function api(url, opts={}){
  try{
    const r=await fetch(url,{headers:{'Content-Type':'application/json'},...opts});
    if(!r.ok) throw new Error('HTTP '+r.status);
    return await r.json();
  }catch(e){
    showToast('⚠ CONNECTION ERROR',true);
    setConnStatus(false);
    throw e;
  }
}

function setConnStatus(ok){
  const dot=document.getElementById('conn-dot');
  const lbl=document.getElementById('kv-label');
  dot.className=ok?'ok':'err';
  if(!ok) lbl.textContent='OFFLINE';
}

// ── Update ────────────────────────────────────────────────────────────
async function update(){
  let d;
  try{ d=await api('/api/data'); }catch(e){ return; }

  const savedInt=parseInt(d.water_int)||25;
  document.getElementById('int-val').value=savedInt;
  if(waterSecs===null){
    waterTotal=savedInt*60;
    waterSecs=loadWaterState(waterTotal);
  }

  // KV status indicator
  const dot=document.getElementById('conn-dot');
  const lbl=document.getElementById('kv-label');
  dot.className=d.kv?'ok':'';
  lbl.textContent=d.kv?'KV SYNC':'LOCAL';

  const total=d.tasks.length+d.done_today;
  const pct=total===0?0:Math.round(d.done_today/total*100);

  document.getElementById('p-bar').style.width=pct+'%';
  document.getElementById('progress-pct').textContent=pct+'%';
  document.getElementById('lvl-val').textContent=d.level;
  document.getElementById('stat-lvl').textContent=d.level;
  document.getElementById('stat-poyos').textContent=d.total_poyos;
  document.getElementById('stat-today').textContent=d.done_today;
  document.getElementById('total-val').textContent=d.total_poyos;
  document.getElementById('stat-xp').textContent=(d.xp%100)+' / 100';
  document.getElementById('xp-fill').style.width=(d.xp%100)+'%';

  const atLimit=d.tasks.length>=TASK_LIMIT;
  const tc=document.getElementById('task-count');
  tc.textContent=d.tasks.length?d.tasks.length+' / '+TASK_LIMIT+' queued':'all clear!';
  tc.className=atLimit?'limit':'';
  document.getElementById('add-btn').disabled=atLimit;
  document.getElementById('task-input').disabled=atLimit;

  if(pct===100&&d.done_today>0){
    confetti({particleCount:130,spread:80,origin:{y:.55},colors:['#ff5fa0','#ffd84d','#00f5ff','#39ff6e']});
    showToast('✦ ALL MISSIONS COMPLETE ✦');
  }

  const list=document.getElementById('task-list');
  const empty=document.getElementById('empty-state');
  if(d.tasks.length===0){
    list.innerHTML='';list.appendChild(empty);empty.style.display='flex';
  } else {
    empty.style.display='none';
    list.innerHTML=d.tasks.map((t,i)=>`
      <div class="task-item">
        <span class="task-arrow">▸</span>
        <span class="task-text">${t}</span>
        <div class="task-btns">
          <button class="inhale-btn" onclick="inhale(${i})">INHALE</button>
          <button class="del-btn" onclick="deleteTask(${i})" title="remove">✕</button>
        </div>
      </div>`).join('');
  }
}

// ── Water timer ───────────────────────────────────────────────────────
setInterval(()=>{
  if(waterSecs===null) return;
  if(waterSecs>0) waterSecs--;
  else{
    const v=parseInt(document.getElementById('int-val').value)||25;
    waterTotal=v*60; waterSecs=waterTotal;
    showToast('💧 TRINKEN! WATER TIME!');
    if(notifPerm==='granted')
      new Notification('💧 Hydration Check!',{body:'Zeit für einen Schluck Wasser!'});
  }
  const m=Math.floor(waterSecs/60),sc=waterSecs%60;
  const el=document.getElementById('w-timer');
  el.textContent=m+':'+(sc<10?'0':'')+sc;
  el.className=waterSecs<60?'urgent':'';
  if(waterTotal) document.getElementById('water-fill').style.width=(waterSecs/waterTotal*100)+'%';
  saveWaterState();
},1000);

// ── Config ────────────────────────────────────────────────────────────
async function saveInt(){
  const v=parseInt(document.getElementById('int-val').value)||25;
  waterTotal=v*60; waterSecs=waterTotal;
  await api('/api/config',{method:'POST',body:JSON.stringify({interval:v})});
}

// ── Add task ──────────────────────────────────────────────────────────
async function addTask(){
  const inp=document.getElementById('task-input');
  const v=inp.value.trim(); if(!v) return;
  try{
    await api('/api/add',{method:'POST',body:JSON.stringify({task:v})});
    inp.value=''; update();
  }catch(e){}
}
document.getElementById('task-input').addEventListener('keydown',e=>{ if(e.key==='Enter') addTask(); });

// ── Inhale ────────────────────────────────────────────────────────────
async function inhale(i){
  try{
    await api('/api/inhale/'+i,{method:'POST'});
    showToast('POYO! +20 XP ✦'); update();
  }catch(e){}
}

// ── Delete task ────────────────────────────────────────────────────────
async function deleteTask(i){
  try{
    await api('/api/delete/'+i,{method:'POST'});
    showToast('MISSION REMOVED'); update();
  }catch(e){}
}

// ── Kirby click ───────────────────────────────────────────────────────
const poyoMsgs=['POYO! ✦ KIRBY BELIEVES IN YOU','HIII ✦ YOU GOT THIS!',
  '✦ STAY FOCUSED PILOT ✦','POYO POYO! ✦','⭐ COSMIC ENERGY ACTIVATED'];
let poyoIdx=0;
function playPoyo(){
  if(Notification.permission==='default'){
    Notification.requestPermission().then(p=>{
      notifPerm=p;
      if(p==='granted') new Notification('🌟 Poyo!',{body:'Kirby glaubt an dich!'});
    });
  } else if(Notification.permission==='granted'){
    new Notification('🌟 Poyo!',{body:'Kirby glaubt an dich!'});
  }
  showToast(poyoMsgs[poyoIdx++ % poyoMsgs.length]);
  // Extra poke animation
  const s=document.getElementById('kirby-sprite');
  s.style.animation='kirby-poke .5s ease-out';
  setTimeout(()=>s.style.animation='kirby-float 3.4s ease-in-out infinite',520);
}

update();
setInterval(update,15000);
</script>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, task_limit=TASK_LIMIT)

@app.route('/api/data')
def data():
    d = get_data()
    d['kv'] = bool(KV_URL and KV_TOKEN)
    return jsonify(d)

@app.route('/api/config', methods=['POST'])
def config():
    d = get_data()
    d['water_int'] = max(1, min(99, int(request.json['interval'])))
    save_data(d)
    return jsonify(ok=True)

@app.route('/api/add', methods=['POST'])
def add():
    d = get_data()
    if len(d['tasks']) >= TASK_LIMIT:
        return jsonify(ok=False, error='task limit reached'), 400
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

@app.route('/api/delete/<int:i>', methods=['POST'])
def delete_task(i):
    d = get_data()
    if 0 <= i < len(d['tasks']):
        d['tasks'].pop(i)
        save_data(d)
    return jsonify(ok=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
