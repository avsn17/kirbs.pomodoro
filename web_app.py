from flask import Flask, render_template_string, jsonify, request
import json, os
from datetime import datetime          # already imported — no need for __import__ hack

app = Flask(__name__)
DATA_FILE = 'data/kirby_stats.json'

# ── Ensure the data directory always exists before any read/write ──────────────
os.makedirs('data', exist_ok=True)


def get_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {
            "tasks": [], "done_today": 0, "total_poyos": 0,
            "water_int": 25, "level": 1, "xp": 0,
            "last_date": ""
        }
    with open(DATA_FILE, 'r') as f:
        d = json.load(f)

    today = datetime.now().strftime('%Y-%m-%d')   # FIX: use already-imported datetime
    if d.get('last_date') != today:
        d['done_today'] = 0
        d['last_date'] = today
        save_data(d)
    return d


def sanitize(t: str) -> str:
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def save_data(d: dict) -> None:
    os.makedirs('data', exist_ok=True)           # FIX: guard before every write
    with open(DATA_FILE, 'w') as f:
        json.dump(d, f)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><title>Kirby OS Ultimate V10</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
    <style>
        :root { --poyo-pink: #ff69b4; --star-gold: #ffd700; }
        body {
            background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
            margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center;
            font-family: 'Courier New', monospace; overflow: hidden; color: white;
        }
        .star { position: absolute; background: white; border-radius: 50%; opacity: 0.5; animation: twinkle var(--d) infinite; }
        @keyframes twinkle { 0%, 100% { opacity: 0.3; transform: scale(1); } 50% { opacity: 1; transform: scale(1.2); } }

        .window {
            background: rgba(255,255,255,0.1); backdrop-filter: blur(20px);
            border: 2px solid rgba(255,192,203,0.3); border-radius: 30px;
            width: 450px; padding: 25px; text-align: center;
            box-shadow: 0 0 50px rgba(255,105,180,0.2);
        }

        .hud { position: absolute; top: 15px; left: 15px; text-align: left; font-size: 12px; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px; }

        .kirby-box { height: 160px; display: flex; justify-content: center; align-items: center; cursor: pointer; }
        /* FIX: use a working Kirby GIF from the correct CDN path */
        .kirby-img { width: 140px; filter: drop-shadow(0 0 20px var(--poyo-pink)); animation: float 3s infinite ease-in-out; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }

        .bar-wrap { border: 2px solid rgba(255,255,255,0.2); height: 12px; border-radius: 10px; margin: 10px 0; overflow: hidden; background: rgba(0,0,0,0.3); }
        .bar-fill { height: 100%; width: 0%; transition: 1s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        .progress { background: linear-gradient(90deg, var(--poyo-pink), #ff1493); }
        .xp-bar   { background: linear-gradient(90deg, #00eeff, #55ff00); }

        .task-item { background: rgba(255,255,255,0.05); border-radius: 15px; margin: 8px 0; padding: 10px; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(255,255,255,0.1); font-size: 13px; }
        .btn { background: var(--poyo-pink); color: white; border: none; border-radius: 10px; padding: 6px 12px; cursor: pointer; font-weight: bold; }
        input { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.3); color: white; padding: 8px; border-radius: 10px; width: 60%; outline: none; }

        .water-timer { color: #00eeff; font-weight: bold; font-size: 14px; margin-top: 5px; }
    </style>
</head>
<body>
    <div id="stars"></div>

    <div class="hud">
        ⭐ LEVEL: <span id="lvl-val">1</span><br>
        🏆 TOTAL POYOS: <span id="total-val">0</span><br>
        💧 INT: <input type="number" id="int-val" value="25"
            style="width:30px; background:none; border:none; color:cyan;"
            onchange="saveInt()">m
    </div>

    <div class="window">
        <div class="kirby-box" onclick="playPoyo()">
            <!-- FIX: corrected Kirby image URL -->
            <img id="kirby"
                 src="https://media.tenor.com/images/5d3f02f24e27dc90bbd30d72f31ad8ba/tenor.gif"
                 class="kirby-img"
                 onerror="this.src='https://www.kirby.jp/common/images/character/kirby.png'">
        </div>

        <div class="water-timer">NÄCHSTER SCHLUCK: <span id="w-timer">--:--</span></div>

        <div style="font-size: 10px; margin-top: 15px; opacity:0.7;">MISSION PROGRESS</div>
        <div class="bar-wrap"><div id="p-bar" class="bar-fill progress"></div></div>

        <div style="font-size: 10px; opacity:0.7;">XP TO NEXT LEVEL</div>
        <div class="bar-wrap" style="height:6px;"><div id="xp-bar" class="bar-fill xp-bar"></div></div>

        <div id="list" style="max-height: 120px; overflow-y: auto; margin-top: 10px;"></div>

        <div style="margin-top: 20px;">
            <input type="text" id="task-input" placeholder="Was einsaugen?">
            <button class="btn" onclick="add()">POYO!</button>
        </div>
    </div>

    <audio id="snd-inhale"  src=""></audio>
    <audio id="snd-victory" src=""></audio>

    <script>
        // FIX: waterSecs initialised from server on first update(), not hardcoded
        let waterSecs = null;
        let notifPermission = Notification.permission;

        // ── Stars ─────────────────────────────────────────────────────────────
        const starContainer = document.getElementById('stars');
        for (let i = 0; i < 100; i++) {
            const el = document.createElement('div');
            el.className = 'star';
            el.style.left = Math.random() * 100 + '%';
            el.style.top  = Math.random() * 100 + '%';
            const sz = Math.random() * 2 + 'px';
            el.style.width  = sz;
            el.style.height = sz;
            el.style.setProperty('--d', (Math.random() * 3 + 2) + 's');
            starContainer.appendChild(el);
        }

        // ── Data update ───────────────────────────────────────────────────────
        async function update() {
            const r = await fetch('/api/data');
            const d = await r.json();

            // FIX: sync water interval input AND waterSecs from server on first load
            const savedInt = parseInt(d.water_int, 10) || 25;
            document.getElementById('int-val').value = savedInt;
            if (waterSecs === null) waterSecs = savedInt * 60;

            const total = d.tasks.length + d.done_today;
            const p = total === 0 ? 0 : Math.round((d.done_today / total) * 100);

            document.getElementById('p-bar').style.width    = p + '%';
            document.getElementById('total-val').innerText  = d.total_poyos;
            document.getElementById('lvl-val').innerText    = d.level;
            document.getElementById('xp-bar').style.width   = (d.xp % 100) + '%';

            if (p === 100 && d.done_today > 0) {
                confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 }, colors: ['#ff69b4', '#ffd700'] });
                document.getElementById('snd-victory').play().catch(() => {});
            }

            document.getElementById('list').innerHTML = d.tasks.map((t, i) =>
                `<div class="task-item">
                    <span>⭐ ${t}</span>
                    <button class="btn" style="padding:2px 8px; font-size:10px;" onclick="inhale(${i})">INHALE</button>
                </div>`
            ).join('');
        }

        // ── Water timer ───────────────────────────────────────────────────────
        setInterval(() => {
            if (waterSecs === null) return;   // wait until server data is loaded
            if (waterSecs > 0) {
                waterSecs--;
            } else {
                const interval = parseInt(document.getElementById('int-val').value, 10) || 25;
                waterSecs = interval * 60;
                // FIX: check permission before firing notification
                if (notifPermission === 'granted') {
                    new Notification('💧 TRINKEN!', { body: 'Zeit für einen Schluck Wasser!' });
                }
            }
            const m  = Math.floor(waterSecs / 60);
            const sc = waterSecs % 60;
            document.getElementById('w-timer').innerText = `${m}:${sc < 10 ? '0' : ''}${sc}`;
        }, 1000);

        // ── Interval config ───────────────────────────────────────────────────
        async function saveInt() {
            const v = parseInt(document.getElementById('int-val').value, 10);
            waterSecs = v * 60;
            await fetch('/api/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ interval: v })
            });
        }

        // ── Task add ──────────────────────────────────────────────────────────
        async function add() {
            const input = document.getElementById('task-input');   // FIX: id renamed from 'in' (reserved word)
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

        // ── Inhale task ───────────────────────────────────────────────────────
        async function inhale(i) {
            document.getElementById('snd-inhale').play().catch(() => {});
            await fetch('/api/inhale/' + i, { method: 'POST' });
            update();
        }

        // ── Kirby click — FIX: replaced blocking alert() with notification request ──
        function playPoyo() {
            if (Notification.permission === 'default') {
                Notification.requestPermission().then(p => {
                    notifPermission = p;
                    if (p === 'granted') new Notification('🌟 Poyo!', { body: 'Kirby glaubt an dich!' });
                });
            } else if (Notification.permission === 'granted') {
                new Notification('🌟 Poyo!', { body: 'Kirby glaubt an dich!' });
            }
        }

        update();
        setInterval(update, 10000);
    </script>
</body>
</html>
"""


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
        d['done_today']   += 1
        d['total_poyos']  += 1
        d['xp']           += 20
        if d['xp'] >= 100:
            d['level'] += 1
            d['xp']     = 0
        save_data(d)
    return jsonify(ok=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
