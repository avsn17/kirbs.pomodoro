#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════╗
║     🌟 COSMIC POMODORO TIMER                     Kirbs
║         Pilot: Cosmic Kirbs | avsn17             ║
╚══════════════════════════════════════════════════╝
"""

import os, sys, time, json, random, threading, select, signal
import termios, tty, shutil, re
from datetime import datetime
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────────────
DATA_FILE     = Path.home() / '.pomodoro_stats.json'
SIGNAL_FILE   = Path('music_signal.txt')
METERS_PER_MINUTE = 10
USER_ID       = "Cosmic Kirbs"

# ─── COLORS ───────────────────────────────────────────────────────────────────
C = {
    'stars':      '\033[97m',
    'deep_space': '\033[94m',
    'nebula':     '\033[95m',
    'cosmic':     '\033[96m',
    'solar':      '\033[93m',
    'void':       '\033[90m',
    'green':      '\033[92m',
    'red':        '\033[91m',
    'pink':       '\033[38;5;218m',
    'bold':       '\033[1m',
    'reset':      '\033[0m',
}

# ─── QUOTES ───────────────────────────────────────────────────────────────────
QUOTES = {
    'iro': [
        'While it is always best to believe in oneself, a little help can be a blessing.',
        'Sharing tea with a fascinating stranger is one of life\'s true delights.',
        'Hope is something you give yourself. That is the meaning of inner strength.',
    ],
    'bronte': [
        'I am no bird; and no net ensnares me.',
        'I would always rather be happy than dignified.',
        'The soul that sees beauty may sometimes walk alone.',
    ],
    'kant': [
        'Two things fill the mind with wonder: the starry heavens and the moral law.',
        'Seek not the favor of the multitude; it is seldom got by honest means.',
        'Act only according to that maxim whereby you can at the same time will it to be universal.',
    ],
    'lyrics': [
        'MJ: If you want to make the world a better place, take a look at yourself.',
        'MJ: Speed demon, minding my own business. Speedin\' on the highway of life.',
        'Lana: Will you still love me when I am no longer young and beautiful?',
        'Lana: Heaven is a place on earth with you.',
        'Bee Gees: Whether you are a brother or whether you are a mother, you are stayin\' alive.',
        'Billie: I am the bad guy, duh.',
        'Billie: You should see me in a crown.',
        'Bowie: Ground Control to Major Tom, commencing countdown.',
        'CAS: I am a dreamer, and you are the dream.',
    ],
    'heroic': [
        'Success is not final, failure is not fatal.',
        'Fortune favors the brave.',
        'With great power comes great responsibility.',
        'Marcus Aurelius: The impediment to action advances action.',
        'I can do this all day.',
    ],
    'kirby': [
        '<( " )> Poyo! You are doing amazing, Cosmic Kirbs!',
        '<( o_o )> Focus mode: MAXIMUM PINK POWER.',
        '(> ^_^ )> <3 Sending positive vibes to the cockpit!',
        '<( ^.^ )> You are a LEGEND. Keep going!',
    ],
    'vibe': [
        'Main Character Energy detected. 📈',
        'No cap, your productivity is skyrocketing.',
        'Vibe check: ABSOLUTE LEGEND.',
        'Big brain moves only.',
    ],
    'wisdom': [
        'The journey is the reward.',
        'Be like water, my friend.',
        'Focus on the step, not the mountain.',
        'Silence is a source of great strength.',
        'He who has a why to live can bear almost any how.',
    ],
}

BREAK_ADVICES = [
    "Take a 5-minute walk to refresh your mind.",
    "Stretch your body and relax your shoulders.",
    "Look away from the screen — give your eyes a rest.",
    "Drink some water and stay hydrated. 💧",
    "Take deep breaths and practice mindfulness.",
    "Step outside for fresh air if possible.",
    "Do a quick exercise — jumping jacks or push-ups!",
    "Listen to your favorite song.",
    "Message a friend or loved one.",
    "Enjoy a healthy snack.",
]

RANK_TIERS = [
    (0,    "🛸 Space Cadet"),
    (100,  "🌙 Moon Walker"),
    (500,  "☄️  Comet Rider"),
    (1000, "🚀 Orbit Master"),
    (2500, "⭐ Star Pilot"),
    (5000, "🌌 Galactic Overlord"),
]

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def get_rank(total_m: float) -> str:
    rank = RANK_TIERS[0][1]
    for threshold, label in RANK_TIERS:
        if total_m >= threshold:
            rank = label
    return rank


def clear():
    sys.stdout.write("\033[H\033[2J")
    sys.stdout.flush()


def signal_music(state: str = "PLAY_NEXT"):
    try:
        SIGNAL_FILE.write_text(state)
    except Exception:
        pass


# ─── MAIN CLASS ───────────────────────────────────────────────────────────────
class CosmicPomodoro:
    def __init__(self):
        self.user_name        = USER_ID
        self.distance_goal    = 0
        self.time_goal        = 0.0        # seconds
        self.elapsed          = 0.0        # seconds
        self.running          = False
        self.paused           = False
        self.in_subscreen     = False
        self.chat_messages    = []         # recent lines shown in sidebar
        self.stats            = self._load_stats()
        self.star_offset      = 0
        self.bg_color         = 'deep_space'
        self.timer_thread     = None
        # Settings (persist in memory)
        self.mood             = "Hype"
        self.remind_interval  = "10"
        self.session_count    = 0
        self.music_enabled    = True
        # Terminal state
        self._old_termios     = None

    # ── Stats I/O ─────────────────────────────────────────────────────────────
    def _load_stats(self) -> dict:
        if DATA_FILE.exists():
            try:
                return json.loads(DATA_FILE.read_text())
            except Exception:
                pass
        return {}

    def _save_stats(self):
        DATA_FILE.write_text(json.dumps(self.stats, indent=2))

    def _add_session(self, distance: float, duration: float, completed: bool = True):
        u = self.user_name
        if u not in self.stats:
            self.stats[u] = {
                'sessions': [], 'total_distance': 0.0,
                'total_time': 0.0, 'completed_sessions': 0,
            }
        self.stats[u]['sessions'].append({
            'date': datetime.now().isoformat(),
            'distance': round(distance, 2),
            'duration': round(duration, 1),
            'completed': completed,
        })
        self.stats[u]['total_distance'] += distance
        self.stats[u]['total_time']     += duration
        if completed:
            self.stats[u]['completed_sessions'] += 1
            self.session_count += 1
        self._save_stats()

    def _user_total_distance(self) -> float:
        return self.stats.get(self.user_name, {}).get('total_distance', 0.0)

    # ── Timer thread ──────────────────────────────────────────────────────────
    def _timer_loop(self):
        while self.running:
            if not self.paused and not self.in_subscreen:
                time.sleep(0.1)
                self.elapsed      += 0.1
                self.star_offset   = (self.star_offset + 1) % 200
                if self.elapsed >= self.time_goal:
                    self._complete()
                    break
            else:
                time.sleep(0.05)

    def _start_timer(self):
        self.running      = True
        self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        self.timer_thread.start()

    def _complete(self):
        self.running = False
        dist = (self.elapsed / 60) * METERS_PER_MINUTE
        self._add_session(dist, self.elapsed, completed=True)
        if self.music_enabled:
            signal_music("PLAY_NEXT")

    # ── UI drawing ────────────────────────────────────────────────────────────
    def _draw_stars(self, cols, rows):
        chars  = ['·', '∙', '•', '✦', '✧', '*']
        n      = (cols * rows) // 35
        grid   = [[' '] * cols for _ in range(rows)]
        for _ in range(n):
            x  = random.randint(0, cols - 1)
            y  = random.randint(0, rows - 1)
            ch = random.choice(chars)
            nx = (x + self.star_offset) % cols
            grid[y][nx] = ch
        return grid

    def _draw_ui(self):
        clear()
        try:
            cols, rows = os.get_terminal_size()
        except Exception:
            cols, rows = 80, 24

        color     = C[self.bg_color]
        print(color, end='')

        star_grid = self._draw_stars(cols, rows - 1)
        progress  = min(self.elapsed / self.time_goal, 1.0) if self.time_goal > 0 else 0.0
        bar_w     = max(cols - 32, 20)
        filled    = int(bar_w * progress)
        dist_done = (self.elapsed / 60) * METERS_PER_MINUTE
        mins, sec = divmod(int(self.elapsed), 60)
        total_dist = self._user_total_distance()

        header  = (f"🎯 Goal: {self.distance_goal}m  |  Pilot: {self.user_name}  |  "
                   f"Sessions: {self.session_count}  |  Rank: {get_rank(total_dist)}")
        timer_d = f"⏱  {mins:02d}:{sec:02d}"
        bar_str = f"[{'█' * filled}{'░' * (bar_w - filled)}] {dist_done:.0f}/{self.distance_goal}m"

        if self.running and not self.paused:
            status_str = "▶ RUNNING"
        elif self.paused:
            status_str = "⏸ PAUSED"
        else:
            status_str = "⏹ STOPPED"

        # Kirby animation: slides across row 9
        kirby_frames = ['<( " )>', '<( ´ )>', '<( ^ )>']
        kf    = kirby_frames[int(self.elapsed) % len(kirby_frames)]
        kirby_x = int((dist_done / max(self.distance_goal, 1)) * max(cols - 10, 1))

        # Sidebar chat
        chat_col = cols - 50

        def _write_row(row_idx: int, text: str, start: int = 0):
            ln = star_grid[row_idx]
            for i, ch in enumerate(text):
                pos = start + i
                if 0 <= pos < len(ln):
                    ln[pos] = ch

        for r in range(rows - 1):
            ln = star_grid[r]

            if r == 1:
                _write_row(r, header[:cols])
            elif r == 3:
                _write_row(r, timer_d, 2)
            elif r == 5:
                _write_row(r, bar_str, 2)
            elif r == 7:
                _write_row(r, status_str, 2)
            elif r == 9 and self.distance_goal > 0:
                _write_row(r, C['pink'] + kf + color, kirby_x)
                # strip color codes for grid (just show kirby text)
                _write_row(r, kf, kirby_x)

            # Sidebar
            if chat_col > 40:
                if r == 11:
                    _write_row(r, "💬 WISDOM SIDEBAR", chat_col)
                elif 12 <= r <= rows - 3:
                    idx = r - 12
                    visible = self.chat_messages[-(rows - 3 - 12 + 1):]
                    if idx < len(visible):
                        msg = visible[idx][:47]
                        _write_row(r, msg, chat_col)

            print(''.join(ln))

        controls = ("[Space] Pause  [N] New  [S] Stats  [A] Settings  "
                    "[C] Chat  [M] Music  [O] Color  [Q] Quit")
        print(controls[:cols] + C['reset'])
        sys.stdout.flush()

    # ── Subscreen helpers ─────────────────────────────────────────────────────
    def _enter_sub(self):
        """Restore cooked mode before a subscreen."""
        self.in_subscreen = True
        if self._old_termios:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_termios)

    def _exit_sub(self):
        """Re-enter cbreak after returning from a subscreen."""
        self.in_subscreen = False
        tty.setcbreak(sys.stdin.fileno())

    # ── Chat ──────────────────────────────────────────────────────────────────
    def _chat(self):
        self._enter_sub()
        clear()
        print(f"{C['cosmic']}{C['bold']}💬 WISDOM CHAT{C['reset']}")
        print(f"{C['void']}Categories: iro · bronte · kant · lyrics · heroic · kirby · vibe · wisdom{C['reset']}")
        print(f"{C['void']}Type 'back' to return to your mission.\n{C['reset']}")
        while True:
            try:
                raw = input(f"{C['green']}You: {C['reset']}").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if raw.lower() == 'back':
                break
            if raw:
                resp = self._bot_reply(raw)
                self.chat_messages.append(f"You: {raw[:43]}")
                self.chat_messages.append(f"Bot: {resp[:43]}")
                print(f"\n{C['cosmic']}Bot: {resp}{C['reset']}\n")
        self._exit_sub()

    def _bot_reply(self, msg: str) -> str:
        ml = msg.lower()
        if any(w in ml for w in ['iro', 'tea', 'uncle']):            cat = 'iro'
        elif any(w in ml for w in ['bronte', 'emily', 'love', 'soul']): cat = 'bronte'
        elif any(w in ml for w in ['kant', 'moral', 'reason']):      cat = 'kant'
        elif any(w in ml for w in ['song', 'music', 'lyric', 'sing']):  cat = 'lyrics'
        elif any(w in ml for w in ['hero', 'brave', 'courage']):     cat = 'heroic'
        elif any(w in ml for w in ['kirby', 'poyo', 'pink']):        cat = 'kirby'
        elif any(w in ml for w in ['vibe', 'cap', 'legend']):        cat = 'vibe'
        else:                                                         cat = random.choice(list(QUOTES))
        return random.choice(QUOTES[cat])

    # ── Stats ─────────────────────────────────────────────────────────────────
    def _show_stats(self):
        self._enter_sub()
        clear()
        print(f"{C['solar']}{C['bold']}📊 COSMIC LEADERBOARD{C['reset']}\n")
        print("═" * 82)
        if not self.stats:
            print("No data yet. Complete a session to appear on the board!")
        else:
            print(f"{'Rank':<5} {'Pilot':<22} {'Distance':<12} {'Time':<12} {'Sessions':<10} {'Rank'}")
            print("─" * 82)
            ordered = sorted(self.stats.items(),
                             key=lambda x: x[1].get('total_distance', 0), reverse=True)
            for i, (name, d) in enumerate(ordered, 1):
                total_d   = d.get('total_distance', 0)
                total_t   = d.get('total_time', 0)
                sessions  = len(d.get('sessions', []))
                completed = d.get('completed_sessions', 0)
                h, m      = divmod(int(total_t) // 60, 60)
                t_str     = f"{h}h {m:02d}m" if h else f"{m}m"
                rank_icon = get_rank(total_d)
                col       = C['solar'] if i == 1 else C['green'] if i <= 3 else ''
                rst       = C['reset']
                print(f"{col}{i:<5} {name:<22} {total_d:.0f}m{'':<6} {t_str:<12} {sessions}/{completed}{'':<4} {rank_icon}{rst}")
        print("\nPress ENTER to return to your mission...")
        input()
        self._exit_sub()

    # ── Settings ──────────────────────────────────────────────────────────────
    def _open_settings(self):
        self._enter_sub()
        clear()
        print(f"\n{C['pink']}{C['bold']}{'★' * 20}{C['reset']}")
        print(f"{C['pink']}🛠  KIRBY CONFIG  ★ avsn17{C['reset']}")
        print(f"{C['pink']}{'★' * 20}{C['reset']}\n")
        print(f"  [1] Hydration Reminder  (Every: {self.remind_interval}m)")
        print(f"  [2] Kirby Mood          ({self.mood})")
        print(f"  [3] Reset Session Count ({self.session_count})")
        print(f"  [4] Toggle Music Auto   ({'ON 🎵' if self.music_enabled else 'OFF 🔇'})")
        print(f"  [5] Change BG Color")
        print(f"  [6] Back\n")
        try:
            ch = input(f"{C['cosmic']}Select: {C['reset']}").strip()
            if ch == '1':
                v = input("  Interval (minutes): ").strip()
                if v.isdigit():
                    self.remind_interval = v
                    print(f"  <( \" )> Updated to {v}m!")
            elif ch == '2':
                self.mood = 'Calm' if self.mood == 'Hype' else 'Hype'
                print(f"  <( ^.^ )> Mood: {self.mood}!")
            elif ch == '3':
                self.session_count = 0
                print("  🔄 Session count reset.")
            elif ch == '4':
                self.music_enabled = not self.music_enabled
                print(f"  Music: {'ON 🎵' if self.music_enabled else 'OFF 🔇'}")
            elif ch == '5':
                self._choose_color()
        except (EOFError, KeyboardInterrupt):
            pass
        time.sleep(0.6)
        self._exit_sub()

    def _choose_color(self):
        opts = {
            '1': 'stars', '2': 'deep_space', '3': 'nebula',
            '4': 'cosmic', '5': 'solar',     '6': 'void',
        }
        labels = {
            'stars': 'Bright Stars ⭐', 'deep_space': 'Deep Space 🌌',
            'nebula': 'Nebula 🟣',      'cosmic': 'Cosmic Cyan 🔵',
            'solar': 'Solar Gold 🌟',   'void': 'Dark Void 🖤',
        }
        print()
        for k, v in opts.items():
            print(f"  [{k}] {labels[v]}")
        ch = input("  Pick (1-6): ").strip()
        if ch in opts:
            self.bg_color = opts[ch]
            print(f"  Color set to {labels[opts[ch]]}!")

    # ── Splash ────────────────────────────────────────────────────────────────
    def _splash(self):
        clear()
        lines = [
            "",
            f"{C['pink']}{C['bold']}  ╔══════════════════════════════════════════╗{C['reset']}",
            f"{C['pink']}{C['bold']}  ║   🌟 COSMIC POMODORO — PERFECT EDITION  ║{C['reset']}",
            f"{C['pink']}{C['bold']}  ║          Pilot: Cosmic Kirbs ✦           ║{C['reset']}",
            f"{C['pink']}{C['bold']}  ╚══════════════════════════════════════════╝{C['reset']}",
            "",
            f"  {C['cosmic']}>> PILOT IDENTIFIED: {self.user_name} <<{C['reset']}",
            f"  {C['solar']}Rank: {get_rank(self._user_total_distance())}{C['reset']}",
            "",
            f"  {C['void']}{random.choice(QUOTES['iro'])}{C['reset']}",
            "",
        ]
        for l in lines:
            print(l)

    # ── Main run loop ─────────────────────────────────────────────────────────
    def run(self):
        self._splash()

        # Distance input
        while True:
            try:
                raw = input(f"\n  {C['green']}Enter distance goal in meters (10 m = 1 min): {C['reset']}").strip()
                dist = int(raw)
                if dist <= 0:
                    raise ValueError
                self.distance_goal = dist
                self.time_goal     = (dist / METERS_PER_MINUTE) * 60
                self.elapsed       = 0.0
                break
            except ValueError:
                print(f"  {C['red']}Please enter a positive integer.{C['reset']}")

        self._start_timer()

        # Save termios state for subscreen toggling
        self._old_termios = termios.tcgetattr(sys.stdin)

        try:
            tty.setcbreak(sys.stdin.fileno())

            while self.running or self.paused:
                if not self.in_subscreen:
                    self._draw_ui()

                if select.select([sys.stdin], [], [], 0.08)[0]:
                    key = sys.stdin.read(1).lower()

                    if key == ' ':
                        self.paused = not self.paused

                    elif key == 'q':
                        dist = (self.elapsed / 60) * METERS_PER_MINUTE
                        self._add_session(dist, self.elapsed, completed=False)
                        self.running = False
                        break

                    elif key == 'n':
                        dist = (self.elapsed / 60) * METERS_PER_MINUTE
                        self._add_session(dist, self.elapsed, completed=False)
                        self.running = False
                        break

                    elif key == 'c':
                        self._chat()

                    elif key == 's':
                        self._show_stats()

                    elif key == 'a':
                        self._open_settings()

                    elif key == 'm':
                        self.music_enabled = not self.music_enabled
                        self.chat_messages.append(
                            f"🎵 Music {'ON' if self.music_enabled else 'OFF'}")

                    elif key == 'o':
                        self._enter_sub()
                        clear()
                        self._choose_color()
                        time.sleep(0.4)
                        self._exit_sub()

                time.sleep(0.05)

        finally:
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_termios)
            except Exception:
                pass
            print(C['reset'])

        # ── Post-session ──────────────────────────────────────────────────────
        if self.elapsed >= self.time_goal > 0:
            self._finish_screen()
        else:
            self._ask_restart()

    def _finish_screen(self):
        clear()
        dist = (self.elapsed / 60) * METERS_PER_MINUTE
        print(f"\n{C['solar']}{C['bold']}  🎉 MISSION COMPLETE! 🎉{C['reset']}")
        print(f"  {C['green']}Distance covered: {dist:.0f} m{C['reset']}")
        print(f"  {C['cosmic']}New rank:  {get_rank(self._user_total_distance())}{C['reset']}")
        print(f"\n  💡 Break tip: {random.choice(BREAK_ADVICES)}")
        print(f"\n  ✨ {random.choice(QUOTES['kirby'])}")
        if self.music_enabled:
            signal_music("PLAY_NEXT")
            print(f"\n  🎵 Music autoplay triggered.")
        self._ask_restart()

    def _ask_restart(self):
        try:
            ch = input(f"\n  {C['green']}Start a new mission? (y/n): {C['reset']}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            ch = 'n'
        if ch == 'y':
            # Reset state and re-run
            self.elapsed       = 0.0
            self.running       = False
            self.paused        = False
            self.chat_messages = []
            self.run()
        else:
            print(f"\n  {C['cosmic']}👋 Fly safe, {self.user_name}. The stars await. 🌌{C['reset']}\n")


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        CosmicPomodoro().run()
    except KeyboardInterrupt:
        print(f"\n\n{C['cosmic']}👋 Mission aborted. Goodbye, Cosmic Kirbs.{C['reset']}\n")