from flask import Flask, render_template_string, jsonify, request # type: ignore
import json, os, urllib.request, urllib.error
from datetime import datetime

app = Flask(__name__)

_IS_VERCEL  = os.environ.get('VERCEL') == '1'
_DATA_DIR   = '/tmp' if _IS_VERCEL else 'data'
DATA_FILE   = os.path.join(_DATA_DIR, 'kirby_stats.json')
KV_URL      = os.environ.get('KV_REST_API_URL')
KV_TOKEN    = os.environ.get('KV_REST_API_TOKEN')
ANTHROPIC_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
KV_KEY      = 'kirby_stats'
TASK_LIMIT  = 20

os.makedirs(_DATA_DIR, exist_ok=True)

DEFAULTS = lambda: {
    "tasks": [], "done_today": 0, "total_poyos": 0,
    "water_int": 25, "level": 1, "xp": 0, "last_date": "",
    "pomodoro_sessions": 0, "focus_minutes": 0
}

# ── KV helpers ────────────────────────────────────────────────────────────────
def _kv_get():
    try:
        payload = json.dumps(["GET", KV_KEY]).encode()
        req = urllib.request.Request(KV_URL, data=payload,
            headers={"Authorization": f"Bearer {KV_TOKEN}", "Content-Type": "application/json"},
            method="POST")
        with urllib.request.urlopen(req, timeout=5) as r:
            result = json.loads(r.read()).get('result')
        return json.loads(result) if result else None
    except Exception:
        return None

def _kv_set(data):
    try:
        payload = json.dumps(["SET", KV_KEY, json.dumps(data)]).encode()
        req = urllib.request.Request(KV_URL, data=payload,
            headers={"Authorization": f"Bearer {KV_TOKEN}", "Content-Type": "application/json"},
            method="POST")
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False

def get_data():
    d = None
    if KV_URL and KV_TOKEN:
        d = _kv_get()
    if d is None:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE) as f:
                d = json.load(f)
        else:
            d = DEFAULTS()
    for k, v in DEFAULTS().items():
        d.setdefault(k, v)
    today = datetime.now().strftime('%Y-%m-%d')
    if d.get('last_date') != today:
        d['done_today'] = 0
        d['last_date']  = today
        save_data(d)
    return d

def save_data(d):
    if KV_URL and KV_TOKEN:
        _kv_set(d)
    os.makedirs(_DATA_DIR, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(d, f)

def sanitize(t):
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

# ── Anthropic chat ────────────────────────────────────────────────────────────
KIRBY_SYSTEM = """You are Kirby — the cheerful pink puffball from Planet Popstar — acting as a helpful productivity companion inside Kirby OS. You speak with warmth, playful energy, and occasional "Poyo!"s, but you're genuinely smart and helpful. Keep responses concise (2-4 sentences max unless the user needs detail). You can help with: task planning, focus advice, motivation, quick questions, or just chatting. Never break character."""

def kirby_chat(messages):
    if not ANTHROPIC_KEY:
        return "Poyo! Chat needs an ANTHROPIC_API_KEY set in your Vercel environment variables. Check the setup guide!"
    try:
        payload = json.dumps({
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 300,
            "system": KIRBY_SYSTEM,
            "messages": messages
        }).encode()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "x-api-key": ANTHROPIC_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
        return data['content'][0]['text']
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if e.code == 401:
            return "Poyo! My API key isn't working — check that ANTHROPIC_API_KEY is set correctly in Vercel!"
        return f"Poyo! Something went wrong (HTTP {e.code}). Try again!"
    except Exception as e:
        return "Poyo! I got a little lost in the stars — try again in a moment!"


HTML_TEMPLATE = r"""<!DOCTYPE html>
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
  --gold:#ffd84d;--green:#39ff6e;--red:#ff4466;--purple:#bf7fff;
  --bg:#05060f;--bg2:#0b0e22;--panel:#0d1128;
  --border:#1e2a5e;--border-hi:#3a4f9e;
  --text:#dce8ff;--text-dim:#6a7aaa;
  --fp:'Press Start 2P',monospace;--fv:'VT323',monospace;
  --gp:0 0 12px #ff5fa088,0 0 30px #ff5fa033;
  --gc:0 0 12px #00f5ff88,0 0 30px #00f5ff33;
  --gg:0 0 10px #39ff6e88;
}
html,body{height:100%;width:100%;background:var(--bg);color:var(--text);font-family:var(--fv);font-size:18px}
body{overflow:hidden}
#canvas-bg{position:fixed;inset:0;pointer-events:none;z-index:0}
body::after{content:'';position:fixed;inset:0;z-index:1;pointer-events:none;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.12) 2px,rgba(0,0,0,.12) 4px)}

/* ── Shell layout ── */
#app{position:relative;z-index:2;height:100vh;display:grid;
  grid-template-columns:280px 1fr;grid-template-rows:46px 1fr 42px;
  max-width:1000px;margin:0 auto;padding:12px;gap:10px}

/* ── Topbar ── */
#topbar{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--border);padding-bottom:8px}
.logo{font-family:var(--fp);font-size:9px;color:var(--pink);text-shadow:var(--gp);letter-spacing:2px}
.sys-info{font-family:var(--fp);font-size:7px;color:var(--text-dim);display:flex;gap:14px;align-items:center}
.sys-info span{color:var(--cyan)}
#conn-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--text-dim);margin-right:3px;transition:background .4s}
#conn-dot.ok{background:var(--green);box-shadow:var(--gg)}
#conn-dot.err{background:var(--red);box-shadow:0 0 6px var(--red)}

/* ── Bottom tab bar ── */
#tabbar{grid-column:1/-1;display:flex;gap:4px;border-top:1px solid var(--border);padding-top:8px;align-items:center}
.tab-btn{font-family:var(--fp);font-size:6px;padding:6px 14px;background:transparent;
  border:1px solid var(--border);color:var(--text-dim);cursor:pointer;letter-spacing:1px;
  transition:all .15s;white-space:nowrap}
.tab-btn:hover{border-color:var(--border-hi);color:var(--text)}
.tab-btn.active{border-color:var(--pink);color:var(--pink);background:#1a0a14;box-shadow:var(--gp)}
.tab-indicator{flex:1;height:1px;background:var(--border)}

/* ── Left panel (Kirby sidebar — always visible) ── */
#left-panel{display:flex;flex-direction:column;gap:8px;min-height:0;overflow:hidden}
.pixel-box{background:var(--panel);border:2px solid var(--border);position:relative}
.pixel-box::before{content:'';position:absolute;inset:3px;border:1px solid var(--border-hi);pointer-events:none;opacity:.3}

/* Kirby stage */
#kirby-stage{padding:14px 0 8px;text-align:center;cursor:pointer;flex-shrink:0;
  border:2px solid var(--pink-dim);transition:border-color .2s}
#kirby-stage:hover{border-color:var(--pink)}
#kirby-stage:hover #kirby-sprite{filter:drop-shadow(0 0 20px var(--pink))}
#kirby-sprite{width:100px;height:100px;object-fit:contain;display:block;margin:0 auto 6px;
  filter:drop-shadow(0 0 10px var(--pink));image-rendering:pixelated;
  animation:kfloat 3.4s ease-in-out infinite}
@keyframes kfloat{
  0%,100%{transform:translateY(0) scaleX(1) scaleY(1) rotate(-1deg)}
  45%{transform:translateY(-10px) scaleX(.97) scaleY(1.04) rotate(.8deg)}
}
@keyframes ksquish{0%{transform:scaleX(1) scaleY(1)}30%{transform:scaleX(1.3) scaleY(.65)}65%{transform:scaleX(.9) scaleY(1.15)}100%{transform:scaleX(1) scaleY(1)}}
@keyframes kpoke{0%,100%{transform:translateX(0)}25%{transform:translateX(-5px) rotate(-4deg)}70%{transform:translateX(7px) rotate(4deg)}}
.stage-label{font-family:var(--fp);font-size:6px;color:var(--pink);letter-spacing:3px;text-shadow:var(--gp);margin-bottom:3px}
.stage-sub{font-size:14px;color:var(--text-dim)}

/* Stats */
#stats-box{padding:10px 12px;flex-shrink:0}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid var(--border);font-size:16px}
.stat-row:last-child{border-bottom:none}
.stat-label{color:var(--text-dim)}
.stat-val{color:var(--gold);font-family:var(--fp);font-size:7px}
.stat-val.cyan{color:var(--cyan)}.stat-val.green{color:var(--green)}.stat-val.purple{color:var(--purple)}
.xp-track{height:4px;background:var(--border);overflow:hidden;margin-top:6px}
.xp-fill{height:100%;background:linear-gradient(90deg,var(--cyan),var(--green));width:0%;transition:width .8s cubic-bezier(.23,1,.32,1);box-shadow:0 0 4px var(--cyan)}

/* Water */
#water-box{padding:10px 12px;border:2px solid var(--cyan-dim);flex-shrink:0}
.water-hdr{font-family:var(--fp);font-size:6px;color:var(--cyan);text-shadow:var(--gc);letter-spacing:2px;margin-bottom:7px}
#w-timer{font-family:var(--fp);font-size:17px;color:var(--cyan);text-shadow:var(--gc);line-height:1}
#w-timer.urgent{color:var(--gold);text-shadow:0 0 12px var(--gold)}
.water-int-row{font-size:14px;color:var(--text-dim);display:flex;align-items:center;gap:5px;margin-top:5px}
#int-val{width:32px;background:var(--bg2);border:1px solid var(--border-hi);color:var(--cyan);
  font-family:var(--fp);font-size:7px;text-align:center;padding:2px;outline:none}
#int-val:focus{border-color:var(--cyan)}
.water-track{height:3px;background:var(--border);margin-top:5px;overflow:hidden}
.water-fill{height:100%;background:linear-gradient(90deg,var(--cyan-dim),var(--cyan));width:100%;transition:width 1s linear}

/* ── Right panel (tabbed) ── */
#right-panel{display:flex;flex-direction:column;min-height:0;overflow:hidden}
.tab-pane{display:none;flex-direction:column;flex:1;min-height:0;gap:8px}
.tab-pane.active{display:flex}

/* ── MISSIONS tab ── */
#progress-box{padding:10px 12px;flex-shrink:0}
.prog-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.prog-title{font-family:var(--fp);font-size:6px;color:var(--pink);letter-spacing:2px}
#progress-pct{font-family:var(--fp);font-size:9px;color:var(--pink);text-shadow:var(--gp)}
.mission-track{height:9px;background:var(--border);border:1px solid var(--border-hi);overflow:hidden;position:relative}
.mission-fill{height:100%;background:linear-gradient(90deg,var(--pink),#ff1a6e);width:0%;
  transition:width 1s cubic-bezier(.23,1,.32,1);box-shadow:0 0 7px var(--pink);position:relative}
.mission-fill::after{content:'';position:absolute;right:0;top:0;bottom:0;width:3px;background:#fff;opacity:.45}

#task-box{flex:1;min-height:0;display:flex;flex-direction:column;border:2px solid var(--border)}
.task-hdr{padding:7px 12px;border-bottom:1px solid var(--border);font-family:var(--fp);font-size:6px;
  color:var(--text-dim);letter-spacing:2px;display:flex;justify-content:space-between;flex-shrink:0}
#task-count{color:var(--gold)}#task-count.limit{color:var(--red)}
#task-list{flex:1;overflow-y:auto;padding:4px 7px;scrollbar-width:thin;scrollbar-color:var(--border-hi) transparent}
.task-item{display:flex;align-items:center;gap:6px;padding:7px 8px;margin:3px 0;
  background:var(--bg2);border:1px solid var(--border);border-left:3px solid var(--pink-dim);
  font-size:17px;color:var(--text);transition:border-color .15s;animation:slideIn .18s ease-out}
.task-item:hover{background:#141830;border-left-color:var(--pink)}
@keyframes slideIn{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:translateX(0)}}
.task-text{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.task-arrow{color:var(--gold);flex-shrink:0;font-size:12px}
.task-btns{display:flex;gap:4px;flex-shrink:0}
.inhale-btn,.del-btn{border:1px solid;font-family:var(--fp);font-size:6px;padding:4px 7px;cursor:pointer;letter-spacing:1px;transition:all .15s;background:transparent}
.inhale-btn{border-color:var(--pink-dim);color:var(--pink)}
.inhale-btn:hover{background:var(--pink);color:var(--bg);border-color:var(--pink);box-shadow:var(--gp)}
.del-btn{border-color:var(--border-hi);color:var(--text-dim)}
.del-btn:hover{background:var(--red);color:#fff;border-color:var(--red)}
.inhale-btn:active,.del-btn:active{transform:scale(.93)}
#empty-state{display:none;flex-direction:column;align-items:center;justify-content:center;
  height:100%;color:var(--text-dim);font-size:17px;gap:6px;padding:20px;text-align:center}
.empty-icon{font-size:30px}
.empty-hint{font-family:var(--fp);font-size:6px;color:var(--border-hi);line-height:2;letter-spacing:1px}
#add-box{padding:9px 11px;flex-shrink:0;border:2px solid var(--border);display:flex;gap:7px;align-items:center}
#task-input{flex:1;background:var(--bg2);border:1px solid var(--border-hi);color:var(--text);
  font-family:var(--fv);font-size:19px;padding:6px 10px;outline:none;caret-color:var(--pink);min-width:0}
#task-input::placeholder{color:var(--text-dim)}
#task-input:focus{border-color:var(--pink-dim)}
#add-btn{background:var(--pink);color:var(--bg);border:none;font-family:var(--fp);font-size:7px;
  padding:9px 12px;cursor:pointer;letter-spacing:1px;transition:all .15s;flex-shrink:0;white-space:nowrap}
#add-btn:hover{background:#ff80b8;box-shadow:var(--gp)}
#add-btn:active{transform:scale(.96)}
#add-btn:disabled{opacity:.35;cursor:not-allowed;transform:none}

/* ── FOCUS (Pomodoro) tab ── */
#pomo-box{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;padding:20px}
.pomo-label{font-family:var(--fp);font-size:7px;color:var(--text-dim);letter-spacing:3px}
#pomo-display{font-family:var(--fp);font-size:52px;color:var(--cyan);text-shadow:var(--gc);line-height:1;letter-spacing:4px}
#pomo-display.work{color:var(--pink);text-shadow:var(--gp)}
#pomo-display.rest{color:var(--green);text-shadow:var(--gg)}
.pomo-phase{font-family:var(--fp);font-size:8px;letter-spacing:2px;margin-top:-8px}
.pomo-phase.work{color:var(--pink)}.pomo-phase.rest{color:var(--green)}
.pomo-ring{width:200px;height:200px;position:relative;flex-shrink:0}
.pomo-ring svg{position:absolute;inset:0;transform:rotate(-90deg)}
.pomo-ring-bg{fill:none;stroke:var(--border);stroke-width:6}
.pomo-ring-fill{fill:none;stroke-width:6;stroke-linecap:round;stroke-dasharray:565;stroke-dashoffset:0;transition:stroke-dashoffset .8s ease,stroke .4s}
.pomo-ring-center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px}
.pomo-controls{display:flex;gap:10px}
.pomo-btn{font-family:var(--fp);font-size:7px;padding:8px 16px;background:transparent;cursor:pointer;letter-spacing:1px;transition:all .15s;border:1px solid}
#pomo-start{border-color:var(--cyan);color:var(--cyan)}
#pomo-start:hover{background:var(--cyan);color:var(--bg);box-shadow:var(--gc)}
#pomo-reset{border-color:var(--border-hi);color:var(--text-dim)}
#pomo-reset:hover{border-color:var(--red);color:var(--red)}
.pomo-btn:active{transform:scale(.95)}
.pomo-settings{display:flex;gap:20px;font-size:15px;color:var(--text-dim);align-items:center}
.pomo-settings label{font-family:var(--fp);font-size:6px;color:var(--text-dim);letter-spacing:1px}
.pomo-num{width:36px;background:var(--bg2);border:1px solid var(--border-hi);color:var(--text);
  font-family:var(--fp);font-size:7px;text-align:center;padding:3px;outline:none}
.pomo-num:focus{border-color:var(--cyan)}
.pomo-stats-row{display:flex;gap:24px;font-family:var(--fp);font-size:7px;color:var(--text-dim)}
.pomo-stat{text-align:center}
.pomo-stat-val{font-size:14px;display:block;color:var(--gold);margin-top:4px}

/* ── CHAT tab ── */
#chat-box{flex:1;min-height:0;display:flex;flex-direction:column;border:2px solid var(--border)}
.chat-hdr{padding:8px 14px;border-bottom:1px solid var(--border);font-family:var(--fp);font-size:6px;
  color:var(--pink);letter-spacing:2px;flex-shrink:0;display:flex;justify-content:space-between;align-items:center}
#chat-status{font-size:6px;color:var(--text-dim)}
#chat-messages{flex:1;overflow-y:auto;padding:10px 12px;display:flex;flex-direction:column;gap:8px;
  scrollbar-width:thin;scrollbar-color:var(--border-hi) transparent}
.msg{max-width:85%;display:flex;flex-direction:column;gap:3px;animation:slideIn .2s ease-out}
.msg.user{align-self:flex-end;align-items:flex-end}
.msg.kirby{align-self:flex-start;align-items:flex-start}
.msg-bubble{padding:8px 12px;font-size:17px;line-height:1.4}
.msg.user .msg-bubble{background:#1a1040;border:1px solid var(--pink-dim);color:var(--text)}
.msg.kirby .msg-bubble{background:#0a1530;border:1px solid var(--cyan-dim);color:var(--text)}
.msg-meta{font-family:var(--fp);font-size:5px;color:var(--text-dim);padding:0 4px}
.msg.kirby .msg-meta::before{content:'✦ KIRBY  '}
.msg.user .msg-meta::before{content:'YOU  '}
#typing-indicator{display:none;align-self:flex-start}
#typing-indicator .msg-bubble{color:var(--cyan);font-size:22px;letter-spacing:4px;animation:blink 1s steps(1) infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
#chat-input-row{padding:9px 11px;border-top:1px solid var(--border);display:flex;gap:7px;flex-shrink:0}
#chat-input{flex:1;background:var(--bg2);border:1px solid var(--border-hi);color:var(--text);
  font-family:var(--fv);font-size:19px;padding:6px 10px;outline:none;caret-color:var(--cyan);resize:none;
  height:38px;overflow:hidden}
#chat-input:focus{border-color:var(--cyan-dim)}
#chat-input::placeholder{color:var(--text-dim)}
#chat-send{background:var(--cyan);color:var(--bg);border:none;font-family:var(--fp);font-size:7px;
  padding:9px 12px;cursor:pointer;letter-spacing:1px;transition:all .15s;flex-shrink:0;white-space:nowrap}
#chat-send:hover{background:#66f9ff;box-shadow:var(--gc)}
#chat-send:active{transform:scale(.96)}
#chat-send:disabled{opacity:.35;cursor:not-allowed}
.chat-welcome{text-align:center;color:var(--text-dim);font-size:17px;padding:30px 20px;line-height:1.6}
.chat-welcome .cw-icon{font-size:36px;margin-bottom:10px}
.chat-welcome .cw-hint{font-family:var(--fp);font-size:6px;color:var(--border-hi);line-height:2;margin-top:10px}
#chat-clear{font-family:var(--fp);font-size:6px;color:var(--text-dim);background:transparent;
  border:1px solid var(--border);padding:4px 8px;cursor:pointer;letter-spacing:1px}
#chat-clear:hover{border-color:var(--red);color:var(--red)}

/* ── VIBES tab ── */
#vibes-box{flex:1;display:flex;flex-direction:column;padding:20px;gap:16px;overflow-y:auto}
.vibes-title{font-family:var(--fp);font-size:7px;color:var(--purple);letter-spacing:3px;margin-bottom:4px;
  text-shadow:0 0 12px #bf7fff88}
.vibe-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.vibe-card{padding:12px 14px;background:var(--bg2);border:1px solid var(--border);cursor:pointer;
  transition:all .2s;position:relative;overflow:hidden}
.vibe-card:hover{border-color:var(--purple);background:#0f0a1e}
.vibe-card.playing{border-color:var(--purple);background:#110d20;box-shadow:0 0 14px #bf7fff33}
.vibe-card.playing::after{content:'▶ PLAYING';position:absolute;top:6px;right:8px;
  font-family:var(--fp);font-size:5px;color:var(--purple)}
.vibe-name{font-family:var(--fp);font-size:7px;color:var(--text);letter-spacing:1px;margin-bottom:5px}
.vibe-desc{font-size:15px;color:var(--text-dim)}
.vibe-wave{height:24px;display:flex;align-items:flex-end;gap:2px;margin-top:8px;opacity:.4}
.vibe-card.playing .vibe-wave{opacity:1}
.vibe-bar{width:4px;background:var(--purple);border-radius:1px;transition:height .1s}
.vibe-card.playing .vibe-bar{animation:vwave var(--s) ease-in-out infinite alternate}
@keyframes vwave{0%{height:4px}100%{height:20px}}
.vibes-vol{display:flex;align-items:center;gap:12px;font-size:16px;color:var(--text-dim)}
.vibes-vol label{font-family:var(--fp);font-size:6px;color:var(--text-dim);letter-spacing:1px}
#vol-slider{-webkit-appearance:none;width:140px;height:4px;background:var(--border);outline:none;cursor:pointer}
#vol-slider::-webkit-slider-thumb{-webkit-appearance:none;width:12px;height:12px;background:var(--purple);cursor:pointer}
.vibes-stop{font-family:var(--fp);font-size:6px;padding:7px 14px;background:transparent;
  border:1px solid var(--border-hi);color:var(--text-dim);cursor:pointer;letter-spacing:1px;transition:all .15s}
.vibes-stop:hover{border-color:var(--red);color:var(--red)}

/* ── Toast ── */
#toast{position:fixed;bottom:16px;right:16px;z-index:50;background:var(--panel);
  border:2px solid var(--pink);padding:8px 14px;font-family:var(--fp);font-size:7px;
  color:var(--pink);box-shadow:var(--gp);opacity:0;pointer-events:none;
  transform:translateY(6px);transition:all .2s;letter-spacing:1px}
#toast.show{opacity:1;transform:translateY(0)}
#toast.err{border-color:var(--red);color:var(--red);box-shadow:0 0 16px #ff446633}
#toast.ok{border-color:var(--green);color:var(--green);box-shadow:var(--gg)}

/* ── Boot ── */
#boot{position:fixed;inset:0;z-index:100;background:var(--bg);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;
  animation:bootFade .4s ease 2s forwards}
@keyframes bootFade{to{opacity:0;pointer-events:none}}
.boot-logo{font-family:var(--fp);font-size:11px;color:var(--pink);text-shadow:var(--gp);
  letter-spacing:4px;animation:blinkIn .3s steps(1) .2s both}
.boot-sub{font-family:var(--fp);font-size:7px;color:var(--cyan);letter-spacing:3px;animation:blinkIn .3s steps(1) .7s both}
.boot-line{font-family:var(--fp);font-size:6px;color:var(--text-dim);letter-spacing:1px;animation:blinkIn .3s steps(1) 1.1s both}
.boot-bar-wrap{width:180px;height:7px;border:1px solid var(--border-hi);overflow:hidden;animation:blinkIn .3s steps(1) 1.1s both}
.boot-bar-fill{height:100%;background:var(--pink);box-shadow:var(--gp);animation:bootLoad .7s ease 1.2s forwards;width:0%}
@keyframes bootLoad{to{width:100%}}@keyframes blinkIn{from{opacity:0}to{opacity:1}}

/* ── Mobile ── */
@media(max-width:680px){
  body{overflow-y:auto}
  #app{grid-template-columns:1fr;grid-template-rows:auto 1fr auto auto;height:auto;min-height:100vh;padding:8px;gap:7px}
  #left-panel{order:2;display:grid;grid-template-columns:1fr 1fr;gap:7px}
  #kirby-stage{grid-column:1/-1}
  #right-panel{order:3;min-height:60vh}
  #tabbar{order:4;flex-wrap:wrap}
  .logo{font-size:7px}.sys-info{gap:8px;font-size:6px}
  #pomo-display{font-size:36px}
  .vibe-grid{grid-template-columns:1fr}
}
</style>
</head>
<body>

<div id="boot">
  <div class="boot-logo">KIRBY OS</div>
  <div class="boot-sub">MISSION CONTROL v4</div>
  <div class="boot-line">LOADING ALL SYSTEMS...</div>
  <div class="boot-bar-wrap"><div class="boot-bar-fill"></div></div>
</div>

<canvas id="canvas-bg"></canvas>
<div id="toast"></div>

<div id="app">

  <!-- ── Topbar ── -->
  <div id="topbar">
    <div class="logo">✦ KIRBY OS ✦</div>
    <div class="sys-info">
      <div>LVL <span id="lvl-val">1</span></div>
      <div>POYOS <span id="total-val">0</span></div>
      <div><span id="conn-dot"></span><span id="kv-label">LOCAL</span></div>
      <div id="clock-val">--:--</div>
    </div>
  </div>

  <!-- ── Left sidebar ── -->
  <div id="left-panel">

    <div id="kirby-stage" class="pixel-box" onclick="playPoyo()">
      <img id="kirby-sprite"
           src="https://upload.wikimedia.org/wikipedia/en/3/35/Kirby_%28character%29.png"
           onerror="this.style.display='none'" alt="Kirby">
      <div class="stage-label">PILOT</div>
      <div class="stage-sub">click for poyo ♡</div>
    </div>

    <div id="stats-box" class="pixel-box">
      <div class="stat-row"><span class="stat-label">LEVEL</span><span class="stat-val cyan" id="stat-lvl">1</span></div>
      <div class="stat-row"><span class="stat-label">XP</span><span class="stat-val" id="stat-xp">0/100</span></div>
      <div class="xp-track"><div class="xp-fill" id="xp-fill"></div></div>
      <div class="stat-row" style="margin-top:7px"><span class="stat-label">POYOS</span><span class="stat-val green" id="stat-poyos">0</span></div>
      <div class="stat-row"><span class="stat-label">TODAY</span><span class="stat-val" id="stat-today">0</span></div>
      <div class="stat-row"><span class="stat-label">SESSIONS</span><span class="stat-val purple" id="stat-sessions">0</span></div>
      <div class="stat-row"><span class="stat-label">FOCUS HRS</span><span class="stat-val purple" id="stat-focus">0m</span></div>
    </div>

    <div id="water-box" class="pixel-box">
      <div class="water-hdr">💧 HYDRATION</div>
      <div id="w-timer">--:--</div>
      <div class="water-int-row">every <input type="number" id="int-val" value="25" min="1" max="99" onchange="saveInt()"> min</div>
      <div class="water-track"><div class="water-fill" id="water-fill"></div></div>
    </div>

  </div>

  <!-- ── Right panel (tabs) ── -->
  <div id="right-panel">

    <!-- MISSIONS -->
    <div id="tab-missions" class="tab-pane active">
      <div id="progress-box" class="pixel-box">
        <div class="prog-hdr">
          <span class="prog-title">⬛ MISSION PROGRESS</span>
          <span id="progress-pct">0%</span>
        </div>
        <div class="mission-track"><div class="mission-fill" id="p-bar"></div></div>
      </div>
      <div id="task-box" class="pixel-box">
        <div class="task-hdr"><span>ACTIVE MISSIONS</span><span id="task-count">0 queued</span></div>
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

    <!-- FOCUS (Pomodoro) -->
    <div id="tab-focus" class="tab-pane">
      <div id="pomo-box" class="pixel-box" style="flex:1">
        <div class="pomo-label">POMODORO TIMER</div>
        <div class="pomo-ring">
          <svg viewBox="0 0 200 200" width="200" height="200">
            <circle class="pomo-ring-bg" cx="100" cy="100" r="90"/>
            <circle id="pomo-ring-fill" class="pomo-ring-fill" cx="100" cy="100" r="90" stroke="var(--pink)"/>
          </svg>
          <div class="pomo-ring-center">
            <div id="pomo-display" class="work">25:00</div>
            <div id="pomo-phase" class="pomo-phase work">WORK</div>
          </div>
        </div>
        <div class="pomo-controls">
          <button id="pomo-start" class="pomo-btn" onclick="pomoToggle()">START</button>
          <button id="pomo-reset" class="pomo-btn" onclick="pomoReset()">RESET</button>
        </div>
        <div class="pomo-settings">
          <div><label>WORK MIN</label><br><input type="number" id="pomo-work" class="pomo-num" value="25" min="1" max="90" onchange="pomoReset()"></div>
          <div><label>BREAK MIN</label><br><input type="number" id="pomo-break" class="pomo-num" value="5" min="1" max="30" onchange="pomoReset()"></div>
          <div><label>LONG BREAK</label><br><input type="number" id="pomo-long" class="pomo-num" value="15" min="1" max="60" onchange="pomoReset()"></div>
          <div><label>UNTIL LONG</label><br><input type="number" id="pomo-count" class="pomo-num" value="4" min="2" max="8" onchange="pomoReset()"></div>
        </div>
        <div class="pomo-stats-row">
          <div class="pomo-stat">SESSIONS TODAY<span class="pomo-stat-val" id="pomo-sess-display">0</span></div>
          <div class="pomo-stat">STREAK<span class="pomo-stat-val" id="pomo-streak">0</span></div>
          <div class="pomo-stat">PHASE<span class="pomo-stat-val" id="pomo-phase-num">1/4</span></div>
        </div>
      </div>
    </div>

    <!-- CHAT -->
    <div id="tab-chat" class="tab-pane">
      <div id="chat-box" class="pixel-box" style="flex:1">
        <div class="chat-hdr">
          ✦ KIRBY CHAT
          <div style="display:flex;gap:8px;align-items:center">
            <span id="chat-status">AI READY</span>
            <button id="chat-clear" onclick="clearChat()">CLEAR</button>
          </div>
        </div>
        <div id="chat-messages">
          <div class="chat-welcome">
            <div class="cw-icon">🌟</div>
            <div>Hey pilot! I'm Kirby — your cosmic co-pilot.</div>
            <div class="cw-hint">ask me anything · task help · focus tips<br>or just say poyo!</div>
          </div>
        </div>
        <div id="typing-indicator" class="msg kirby">
          <div class="msg-bubble">···</div>
        </div>
        <div id="chat-input-row">
          <input id="chat-input" placeholder="say something..." maxlength="300">
          <button id="chat-send" onclick="sendChat()">SEND</button>
        </div>
      </div>
    </div>

    <!-- VIBES -->
    <div id="tab-vibes" class="tab-pane">
      <div id="vibes-box" class="pixel-box" style="flex:1">
        <div class="vibes-title">🎵 AMBIENT VIBES</div>
        <div class="vibe-grid" id="vibe-grid"></div>
        <div class="vibes-vol">
          <label>VOLUME</label>
          <input type="range" id="vol-slider" min="0" max="100" value="40" oninput="setVibeVol(this.value)">
          <span id="vol-val" style="font-family:var(--fp);font-size:7px;color:var(--purple)">40%</span>
        </div>
        <button class="vibes-stop" onclick="stopVibe()">■ STOP ALL</button>
      </div>
    </div>

  </div>

  <!-- ── Tab bar ── -->
  <div id="tabbar">
    <button class="tab-btn active" onclick="switchTab('missions',this)">⬛ MISSIONS</button>
    <button class="tab-btn" onclick="switchTab('focus',this)">⏱ FOCUS</button>
    <button class="tab-btn" onclick="switchTab('chat',this)">✦ CHAT</button>
    <button class="tab-btn" onclick="switchTab('vibes',this)">🎵 VIBES</button>
    <div class="tab-indicator"></div>
  </div>

</div><!-- /app -->

<script>
// ═══════════════════════════════════════════════════════════════
//  KIRBY OS — client script
// ═══════════════════════════════════════════════════════════════

// ── Starfield ────────────────────────────────────────────────────
(()=>{
  const c=document.getElementById('canvas-bg'),ctx=c.getContext('2d'),S=[];
  const resize=()=>{c.width=innerWidth;c.height=innerHeight};
  window.addEventListener('resize',resize);resize();
  for(let i=0;i<160;i++) S.push({x:Math.random(),y:Math.random(),r:Math.random()*1.3+.2,sp:Math.random()*.004+.001,ph:Math.random()*Math.PI*2});
  const draw=t=>{
    ctx.clearRect(0,0,c.width,c.height);
    S.forEach(s=>{
      const a=.15+.65*(.5+.5*Math.sin(t*s.sp*60+s.ph));
      ctx.beginPath();ctx.arc(s.x*c.width,s.y*c.height,s.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(180,210,255,${a})`;ctx.fill();
    });
    requestAnimationFrame(draw);
  };
  requestAnimationFrame(draw);
})();

// ── Tabs ─────────────────────────────────────────────────────────
function switchTab(name, btn){
  document.querySelectorAll('.tab-pane').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  btn.classList.add('active');
}

// ── State ────────────────────────────────────────────────────────

// ── Rich Notifications ───────────────────────────────────────────
function kirbyNotify(title, opts={}){
  if(notifPerm!=='granted') return;
  const base={
    icon:'https://em-content.zobj.net/source/google/387/star_2b50.png',
    badge:'https://em-content.zobj.net/source/google/387/star_2b50.png',
    vibrate:[200,100,200],
    silent:false,
    requireInteraction:false,
    ...opts
  };
  if('serviceWorker' in navigator && navigator.serviceWorker.controller){
    navigator.serviceWorker.ready.then(reg=>{
      reg.showNotification(title, base);
    });
  } else {
    // fallback — basic Notification (no actions support)
    new Notification(title, {body:base.body, icon:base.icon, tag:base.tag});
  }
}

// ── Service Worker registration ──────────────────────────────────
if('serviceWorker' in navigator){
  navigator.serviceWorker.register('/sw.js').then(reg=>{
    reg.addEventListener('updatefound',()=>console.log('SW updated'));
  }).catch(()=>{});
  navigator.serviceWorker.addEventListener('message',e=>{
    if(e.data?.action==='snooze-water'){waterSecs=5*60;}
    if(e.data?.action==='snooze-focus'){pomoSecs+=2*60;}
  });
}

let waterSecs=null,waterTotal=null,notifPerm=Notification.permission;

function loadWaterState(def){
  const s=localStorage.getItem('waterSecs'),at=parseInt(localStorage.getItem('waterSavedAt')||0);
  if(s&&at){const rem=parseInt(s)-Math.floor((Date.now()-at)/1000);if(rem>0)return rem;}
  return def;
}
function saveWaterState(){if(waterSecs!==null){localStorage.setItem('waterSecs',waterSecs);localStorage.setItem('waterSavedAt',Date.now());}}

// ── Clock ────────────────────────────────────────────────────────
(function tick(){
  const n=new Date();
  document.getElementById('clock-val').textContent=String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0');
  setTimeout(tick,(60-n.getSeconds())*1000);
})();

// ── Toast ────────────────────────────────────────────────────────
let _tt=null;
function showToast(msg,type=''){
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='show'+(type?' '+type:'');
  clearTimeout(_tt);_tt=setTimeout(()=>t.className='',type==='err'?3200:2200);
}

// ── API ──────────────────────────────────────────────────────────
async function api(url,opts={}){
  try{
    const r=await fetch(url,{headers:{'Content-Type':'application/json'},...opts});
    if(!r.ok) throw new Error('HTTP '+r.status);
    return await r.json();
  }catch(e){showToast('⚠ CONNECTION ERROR','err');throw e;}
}

// ── Data update ──────────────────────────────────────────────────
async function update(){
  let d; try{d=await api('/api/data');}catch(e){return;}

  const si=parseInt(d.water_int)||25;
  document.getElementById('int-val').value=si;
  if(waterSecs===null){waterTotal=si*60;waterSecs=loadWaterState(waterTotal);}

  const dot=document.getElementById('conn-dot'),lbl=document.getElementById('kv-label');
  dot.className=d.kv?'ok':'';lbl.textContent=d.kv?'KV SYNC':'LOCAL';

  const total=d.tasks.length+d.done_today,pct=total===0?0:Math.round(d.done_today/total*100);
  document.getElementById('p-bar').style.width=pct+'%';
  document.getElementById('progress-pct').textContent=pct+'%';
  document.getElementById('lvl-val').textContent=d.level;
  document.getElementById('stat-lvl').textContent=d.level;
  document.getElementById('stat-poyos').textContent=d.total_poyos;
  document.getElementById('stat-today').textContent=d.done_today;
  document.getElementById('total-val').textContent=d.total_poyos;
  document.getElementById('stat-xp').textContent=(d.xp%100)+'/100';
  document.getElementById('xp-fill').style.width=(d.xp%100)+'%';
  document.getElementById('stat-sessions').textContent=d.pomodoro_sessions||0;
  const fm=d.focus_minutes||0;
  document.getElementById('stat-focus').textContent=fm>=60?Math.floor(fm/60)+'h '+(fm%60)+'m':fm+'m';
  document.getElementById('pomo-sess-display').textContent=d.pomodoro_sessions||0;

  const atLimit=d.tasks.length>=20;
  const tc=document.getElementById('task-count');
  tc.textContent=d.tasks.length?d.tasks.length+'/20 queued':'all clear!';
  tc.className=atLimit?'limit':'';
  document.getElementById('add-btn').disabled=atLimit;
  document.getElementById('task-input').disabled=atLimit;

  if(pct===100&&d.done_today>0){
    confetti({particleCount:130,spread:80,origin:{y:.55},colors:['#ff5fa0','#ffd84d','#00f5ff','#39ff6e']});
    showToast('✦ ALL MISSIONS COMPLETE ✦','ok');
  }

  const list=document.getElementById('task-list'),empty=document.getElementById('empty-state');
  if(d.tasks.length===0){list.innerHTML='';list.appendChild(empty);empty.style.display='flex';}
  else{
    empty.style.display='none';
    list.innerHTML=d.tasks.map((t,i)=>`
      <div class="task-item">
        <span class="task-arrow">▸</span>
        <span class="task-text">${t}</span>
        <div class="task-btns">
          <button class="inhale-btn" onclick="inhale(${i})">INHALE</button>
          <button class="del-btn" onclick="deleteTask(${i})">✕</button>
        </div>
      </div>`).join('');
  }
}

// ── Water timer ──────────────────────────────────────────────────
setInterval(()=>{
  if(waterSecs===null)return;
  if(waterSecs>0)waterSecs--;
  else{
    const v=parseInt(document.getElementById('int-val').value)||25;
    waterTotal=v*60;waterSecs=waterTotal;
    showToast('💧 WATER TIME! TRINKEN!');
    kirbyNotify('💧 Hydration Check!',{body:'Time for a sip! Your brain needs water to fly far.',tag:'water',renotify:true,actions:[{action:'done',title:'💧 Done!'},{action:'snooze',title:'⏰ 5 min'}]});
  }
  const m=Math.floor(waterSecs/60),sc=waterSecs%60;
  const el=document.getElementById('w-timer');
  el.textContent=m+':'+(sc<10?'0':'')+sc;el.className=waterSecs<60?'urgent':'';
  if(waterTotal)document.getElementById('water-fill').style.width=(waterSecs/waterTotal*100)+'%';
  saveWaterState();
},1000);

async function saveInt(){const v=parseInt(document.getElementById('int-val').value)||25;waterTotal=v*60;waterSecs=waterTotal;await api('/api/config',{method:'POST',body:JSON.stringify({interval:v})});}

// ── Tasks ────────────────────────────────────────────────────────
async function addTask(){
  const inp=document.getElementById('task-input'),v=inp.value.trim();if(!v)return;
  try{await api('/api/add',{method:'POST',body:JSON.stringify({task:v})});inp.value='';update();}catch(e){}
}
document.getElementById('task-input').addEventListener('keydown',e=>{if(e.key==='Enter')addTask();});
async function inhale(i){try{await api('/api/inhale/'+i,{method:'POST'});showToast('POYO! +20 XP ✦','ok');update();}catch(e){}}
async function deleteTask(i){try{await api('/api/delete/'+i,{method:'POST'});showToast('MISSION REMOVED');update();}catch(e){}}

// ── Kirby click ──────────────────────────────────────────────────
const poyos=['POYO! ✦ YOU GOT THIS!','HIII ✦ KIRBY IS CHEERING!','✦ COSMIC ENERGY BOOST ✦','POYO POYO! ✦ STAY FOCUSED!','⭐ BELIEVE IN YOURSELF ✦'];
let pi=0;
function playPoyo(){
  if(Notification.permission==='default')Notification.requestPermission().then(p=>{notifPerm=p;});
  kirbyNotify('🌟 Poyo!',{body:'Kirby believes in you! The cosmos is cheering.',tag:'poyo',actions:[{action:'focus',title:'🚀 Lock In'},{action:'music',title:'🎵 Play Music'}]});
  showToast(poyos[pi++%poyos.length]);
  const s=document.getElementById('kirby-sprite');
  s.style.animation='kpoke .5s ease-out';
  setTimeout(()=>s.style.animation='kfloat 3.4s ease-in-out infinite',530);
}

// ═══════════════════════════════════════════════════════════════
//  POMODORO
// ═══════════════════════════════════════════════════════════════
let pomoRunning=false,pomoSecs=25*60,pomoIsWork=true,pomoCycle=0,pomoSessionsToday=0,pomoStreak=0,pomoTimer=null;

function pomoReset(){
  clearInterval(pomoTimer);pomoTimer=null;pomoRunning=false;
  pomoIsWork=true;
  pomoSecs=parseInt(document.getElementById('pomo-work').value)*60;
  document.getElementById('pomo-start').textContent='START';
  renderPomo();
}

function pomoToggle(){
  if(pomoRunning){
    clearInterval(pomoTimer);pomoTimer=null;pomoRunning=false;
    document.getElementById('pomo-start').textContent='RESUME';
  } else {
    pomoRunning=true;
    document.getElementById('pomo-start').textContent='PAUSE';
    pomoTimer=setInterval(pomoTick,1000);
  }
}

function pomoTick(){
  if(pomoSecs>0){pomoSecs--;renderPomo();return;}
  // Phase complete
  if(pomoIsWork){
    pomoCycle++;pomoSessionsToday++;pomoStreak++;
    api('/api/pomo_complete',{method:'POST',body:JSON.stringify({minutes:parseInt(document.getElementById('pomo-work').value)})}).catch(()=>{});
    const longEvery=parseInt(document.getElementById('pomo-count').value);
    const isLong=pomoCycle%longEvery===0;
    pomoIsWork=false;
    pomoSecs=(isLong?parseInt(document.getElementById('pomo-long').value):parseInt(document.getElementById('pomo-break').value))*60;
    showToast(isLong?'🎉 LONG BREAK! GREAT WORK!':'✦ BREAK TIME! REST UP!','ok');
    kirbyNotify(isLong?'🎉 Long Break! You earned it!':'☕ Short Break Time!',{body:isLong?'Stretch, hydrate, touch grass. Kirby is proud.':'Quick rest — you locked in hard.',tag:'break',renotify:true,actions:[{action:'done',title:'✅ Ready'},{action:'water',title:'💧 Get Water'}]});
    confetti({particleCount:60,spread:50,origin:{y:.6},colors:['#39ff6e','#00f5ff']});
  } else {
    pomoIsWork=true;
    pomoSecs=parseInt(document.getElementById('pomo-work').value)*60;
    showToast('⏱ FOCUS TIME! LOCK IN!');
    kirbyNotify('⏱ Focus Time!',{body:'Break over — the galaxy waits. Lock in, pilot.',tag:'focus',renotify:true,actions:[{action:'start',title:'🚀 Lets go!'},{action:'snooze',title:'⏰ 2 more min'}]});
  }
  document.getElementById('pomo-phase-num').textContent=pomoCycle+'/'+document.getElementById('pomo-count').value;
  document.getElementById('pomo-sess-display').textContent=pomoSessionsToday;
  document.getElementById('pomo-streak').textContent=pomoStreak;
  renderPomo();
}

function renderPomo(){
  const m=Math.floor(pomoSecs/60),s=pomoSecs%60;
  const disp=document.getElementById('pomo-display'),phase=document.getElementById('pomo-phase');
  disp.textContent=m+':'+(s<10?'0':'')+s;
  const cls=pomoIsWork?'work':'rest';
  disp.className=cls;phase.className='pomo-phase '+cls;
  phase.textContent=pomoIsWork?'WORK':'BREAK';
  // Ring
  const total=(pomoIsWork?parseInt(document.getElementById('pomo-work').value):
    (pomoCycle%parseInt(document.getElementById('pomo-count').value)===0?parseInt(document.getElementById('pomo-long').value):parseInt(document.getElementById('pomo-break').value)))*60;
  const pct=pomoSecs/total;
  const circ=2*Math.PI*90;
  const fill=document.getElementById('pomo-ring-fill');
  fill.style.strokeDashoffset=circ*(1-pct);
  fill.style.stroke=pomoIsWork?'var(--pink)':'var(--green)';
  // Tab title
  document.title=pomoRunning?m+':'+(s<10?'0':'')+s+' '+phase.textContent+' — KIRBY OS':'KIRBY OS ✦ MISSION CONTROL';
}

renderPomo();

// ═══════════════════════════════════════════════════════════════
//  CHAT
// ═══════════════════════════════════════════════════════════════
let chatHistory=[],chatBusy=false;

async function sendChat(){
  const inp=document.getElementById('chat-input');
  const text=inp.value.trim();if(!text||chatBusy)return;
  inp.value='';chatBusy=true;
  document.getElementById('chat-send').disabled=true;
  document.getElementById('chat-status').textContent='THINKING...';

  chatHistory.push({role:'user',content:text});
  appendMsg('user',text);

  const typing=document.getElementById('typing-indicator');
  typing.style.display='flex';
  scrollChat();

  try{
    const r=await api('/api/chat',{method:'POST',body:JSON.stringify({messages:chatHistory})});
    typing.style.display='none';
    const reply=r.reply||'Poyo! Something went wrong!';
    chatHistory.push({role:'assistant',content:reply});
    appendMsg('kirby',reply);
  }catch(e){
    typing.style.display='none';
    appendMsg('kirby','Poyo! I lost signal for a moment — try again!');
  }
  chatBusy=false;
  document.getElementById('chat-send').disabled=false;
  document.getElementById('chat-status').textContent='AI READY';
}

function appendMsg(role,text){
  const msgs=document.getElementById('chat-messages');
  // Remove welcome message on first real message
  const welcome=msgs.querySelector('.chat-welcome');if(welcome)welcome.remove();
  const div=document.createElement('div');
  div.className='msg '+role;
  const ts=new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});
  div.innerHTML=`<div class="msg-meta">${ts}</div><div class="msg-bubble">${text.replace(/\n/g,'<br>')}</div>`;
  msgs.appendChild(div);
  scrollChat();
}

function scrollChat(){
  const msgs=document.getElementById('chat-messages');
  msgs.scrollTop=msgs.scrollHeight;
}

function clearChat(){
  chatHistory=[];
  const msgs=document.getElementById('chat-messages');
  msgs.innerHTML=`<div class="chat-welcome"><div class="cw-icon">🌟</div><div>Chat cleared! Ready to help, pilot.</div><div class="cw-hint">ask me anything · task help · focus tips<br>or just say poyo!</div></div>`;
}

document.getElementById('chat-input').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendChat();}});

// ═══════════════════════════════════════════════════════════════
//  VIBES (Web Audio ambient sound engine)
// ═══════════════════════════════════════════════════════════════
let audioCtx=null,currentVibe=null,vibeNodes=[];

const VIBES=[
  {id:'rain',    name:'RAIN',        desc:'soft rainfall · focus',      color:'var(--cyan)',   gen:'rain'},
  {id:'lofi',    name:'LO-FI BEATS', desc:'chill vibes · study mode',   color:'var(--purple)', gen:'lofi'},
  {id:'space',   name:'DEEP SPACE',  desc:'cosmic drone · meditation',  color:'var(--pink)',   gen:'space'},
  {id:'forest',  name:'FOREST',      desc:'birds & wind · calm',        color:'var(--green)',  gen:'forest'},
  {id:'brown',   name:'BROWN NOISE', desc:'deep rumble · block out',    color:'var(--gold)',   gen:'brown'},
  {id:'cafe',    name:'CAFÉ',        desc:'soft chatter · productivity',color:'var(--text)',   gen:'cafe'},
];

function buildVibeGrid(){
  const g=document.getElementById('vibe-grid');
  g.innerHTML=VIBES.map(v=>`
    <div class="vibe-card" id="vc-${v.id}" onclick="playVibe('${v.id}')">
      <div class="vibe-name" style="color:${v.color}">${v.name}</div>
      <div class="vibe-desc">${v.desc}</div>
      <div class="vibe-wave">${Array(7).fill(0).map((_,i)=>`<div class="vibe-bar" style="height:${4+Math.random()*12}px;--s:${.3+i*.08}s"></div>`).join('')}</div>
    </div>`).join('');
}
buildVibeGrid();

function ensureAudio(){
  if(!audioCtx||audioCtx.state==='closed') audioCtx=new(window.AudioContext||window.webkitAudioContext)();
  if(audioCtx.state==='suspended') audioCtx.resume();
}

function stopVibe(){
  vibeNodes.forEach(n=>{try{n.stop&&n.stop();n.disconnect&&n.disconnect();}catch(e){}});
  vibeNodes=[];currentVibe=null;
  document.querySelectorAll('.vibe-card').forEach(c=>c.classList.remove('playing'));
}

function setVibeVol(v){
  document.getElementById('vol-val').textContent=v+'%';
  vibeNodes.forEach(n=>{if(n.gain)n.gain.value=v/100*1.5;});
}

function playVibe(id){
  if(currentVibe===id){stopVibe();return;}
  stopVibe();ensureAudio();
  currentVibe=id;
  document.getElementById('vc-'+id).classList.add('playing');
  const vol=parseInt(document.getElementById('vol-slider').value)/100*1.5;
  const v=VIBES.find(x=>x.id===id);
  genVibe(v.gen,vol);
  showToast('🎵 '+v.name+' — PLAYING');
}

function makeNoise(type='white'){
  const bufSize=audioCtx.sampleRate*2;
  const buf=audioCtx.createBuffer(1,bufSize,audioCtx.sampleRate);
  const d=buf.getChannelData(0);
  if(type==='white'){for(let i=0;i<bufSize;i++)d[i]=Math.random()*2-1;}
  else if(type==='brown'){let last=0;for(let i=0;i<bufSize;i++){const w=Math.random()*2-1;d[i]=(last+.02*w)/1.02;last=d[i]*3.5;if(d[i]>1)d[i]=1;if(d[i]<-1)d[i]=-1;}}
  const src=audioCtx.createBufferSource();src.buffer=buf;src.loop=true;return src;
}

function makeGain(val){const g=audioCtx.createGain();g.gain.value=val;vibeNodes.push({gain:g.gain,disconnect:()=>g.disconnect(),stop:()=>{}});return g;}

function genVibe(type,vol){
  const out=audioCtx.destination;
  if(type==='rain'){
    const src=makeNoise('white');
    const f=audioCtx.createBiquadFilter();f.type='bandpass';f.frequency.value=1200;f.Q.value=.8;
    const g=makeGain(vol*.6);src.connect(f);f.connect(g);g.connect(out);src.start();vibeNodes.push(src);
    // Extra high shimmer
    const s2=makeNoise('white'),f2=audioCtx.createBiquadFilter();
    f2.type='highpass';f2.frequency.value=4000;
    const g2=makeGain(vol*.2);s2.connect(f2);f2.connect(g2);g2.connect(out);s2.start();vibeNodes.push(s2);
  }
  else if(type==='brown'){
    const src=makeNoise('brown');
    const f=audioCtx.createBiquadFilter();f.type='lowpass';f.frequency.value=500;
    const g=makeGain(vol*1.2);src.connect(f);f.connect(g);g.connect(out);src.start();vibeNodes.push(src);
  }
  else if(type==='space'){
    [60,80,110,150,200].forEach((hz,i)=>{
      const osc=audioCtx.createOscillator();osc.type='sine';osc.frequency.value=hz;
      const lfo=audioCtx.createOscillator();lfo.frequency.value=.05+i*.02;
      const lfoG=audioCtx.createGain();lfoG.gain.value=hz*.15;
      lfo.connect(lfoG);lfoG.connect(osc.frequency);
      const g=makeGain(vol*.08);osc.connect(g);g.connect(out);
      osc.start();lfo.start();vibeNodes.push(osc);vibeNodes.push(lfo);
    });
  }
  else if(type==='lofi'){
    // Chord drone: Cmaj7-ish
    [130.8,164.8,196,246.9,261.6].forEach((hz,i)=>{
      const osc=audioCtx.createOscillator();osc.type='triangle';osc.frequency.value=hz;
      const g=makeGain(vol*.06);
      // subtle wobble
      const lfo=audioCtx.createOscillator();lfo.frequency.value=3+i*.3;
      const lfoG=audioCtx.createGain();lfoG.gain.value=.5;
      lfo.connect(lfoG);lfoG.connect(osc.frequency);
      osc.connect(g);g.connect(out);osc.start();lfo.start();vibeNodes.push(osc);vibeNodes.push(lfo);
    });
    // vinyl crackle
    const cr=makeNoise('white');
    const cf=audioCtx.createBiquadFilter();cf.type='highpass';cf.frequency.value=8000;
    const cg=makeGain(vol*.04);cr.connect(cf);cf.connect(cg);cg.connect(out);cr.start();vibeNodes.push(cr);
  }
  else if(type==='forest'){
    // Wind
    const w=makeNoise('white');
    const wf=audioCtx.createBiquadFilter();wf.type='bandpass';wf.frequency.value=600;wf.Q.value=.3;
    const wg=makeGain(vol*.3);w.connect(wf);wf.connect(wg);wg.connect(out);w.start();vibeNodes.push(w);
    // Bird chirps (periodic sine pings)
    const chirp=()=>{
      if(currentVibe!=='forest')return;
      const o=audioCtx.createOscillator();o.type='sine';o.frequency.value=2000+Math.random()*1500;
      const g=audioCtx.createGain();g.gain.setValueAtTime(0,audioCtx.currentTime);
      g.gain.linearRampToValueAtTime(vol*.15,audioCtx.currentTime+.02);
      g.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+.25);
      o.connect(g);g.connect(out);o.start();o.stop(audioCtx.currentTime+.3);
      setTimeout(chirp,800+Math.random()*2500);
    };
    chirp();
  }
  else if(type==='cafe'){
    // Low murmur
    const m=makeNoise('white');
    const mf=audioCtx.createBiquadFilter();mf.type='bandpass';mf.frequency.value=400;mf.Q.value=1.5;
    const mg=makeGain(vol*.25);m.connect(mf);mf.connect(mg);mg.connect(out);m.start();vibeNodes.push(m);
    // Distant cutlery tinks
    const tink=()=>{
      if(currentVibe!=='cafe')return;
      const o=audioCtx.createOscillator();o.type='sine';o.frequency.value=2500+Math.random()*500;
      const g=audioCtx.createGain();g.gain.setValueAtTime(0,audioCtx.currentTime);
      g.gain.linearRampToValueAtTime(vol*.08,audioCtx.currentTime+.005);
      g.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+.4);
      o.connect(g);g.connect(out);o.start();o.stop(audioCtx.currentTime+.45);
      setTimeout(tink,1500+Math.random()*4000);
    };
    tink();
  }
}

// ═══════════════════════════════════════════════════════════════
//  INIT
// ═══════════════════════════════════════════════════════════════
update();
setInterval(update,15000);
</script>
</body>
</html>"""


@app.route('/sw.js')
def sw():
    from flask import Response
    return Response(open('sw.js').read(), mimetype='application/javascript')

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data')
def data():
    d = get_data()
    d['kv'] = bool(KV_URL and KV_TOKEN)
    return jsonify(d)

@app.route('/api/config', methods=['POST'])
def config():
    d = get_data()
    d['water_int'] = max(1, min(99, int(request.json['interval'])))
    save_data(d); return jsonify(ok=True)

@app.route('/api/add', methods=['POST'])
def add():
    d = get_data()
    if len(d['tasks']) >= TASK_LIMIT:
        return jsonify(ok=False, error='limit reached'), 400
    d['tasks'].append(sanitize(request.json['task']))
    save_data(d); return jsonify(ok=True)

@app.route('/api/inhale/<int:i>', methods=['POST'])
def inhale(i):
    d = get_data()
    if 0 <= i < len(d['tasks']):
        d['tasks'].pop(i)
        d['done_today'] += 1; d['total_poyos'] += 1; d['xp'] += 20
        if d['xp'] >= 100: d['level'] += 1; d['xp'] = 0
        save_data(d)
    return jsonify(ok=True)

@app.route('/api/delete/<int:i>', methods=['POST'])
def delete_task(i):
    d = get_data()
    if 0 <= i < len(d['tasks']):
        d['tasks'].pop(i); save_data(d)
    return jsonify(ok=True)

@app.route('/api/pomo_complete', methods=['POST'])
def pomo_complete():
    d = get_data()
    d['pomodoro_sessions'] = d.get('pomodoro_sessions', 0) + 1
    d['focus_minutes']     = d.get('focus_minutes', 0) + int(request.json.get('minutes', 25))
    d['xp'] += 50
    if d['xp'] >= 100: d['level'] += 1; d['xp'] = d['xp'] % 100
    save_data(d); return jsonify(ok=True)

@app.route('/api/chat', methods=['POST'])
def chat():
    messages = request.json.get('messages', [])[-20:]  # keep last 20 turns
    reply = kirby_chat(messages)
    return jsonify(reply=reply)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
