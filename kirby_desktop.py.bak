import tkinter as tk
import json, os, random, time

# ─── Kirby faces by mood ───────────────────────────────────────────────────────
FACES = {
    "idle":    ["(っ^‿^)っ", "(◕‿◕)っ", "( ´ ▽ ` )っ", "(｡◕‿◕｡)"],
    "working": ["(ง •_•)ง",  "(╯°□°）╯", "( •̀ᴗ•́ )و",  "(ᗒᗨᗕ)"],
    "done":    ["(★^O^★)",    "٩(◕‿◕｡)۶", "(≧◡≦)",       "ヽ(•‿•)ノ"],
    "sleepy":  ["(－_－) zzZ", "(¬_¬)",     "(-_-)zzz",    "(´-ω-`)"],
    "hungry":  ["(＾་།＾)",    "(o゜▽゜)o",  "( ͡° ͜ʖ ͡°)",  "(ﾉ´ヮ`)ﾉ*: ･ﾟ"],
}

MILESTONE_MSGS = {
    0:   "let's gooo!",
    25:  "quarter way!",
    50:  "halfway!!",
    75:  "almost there!",
    100: "POYO COMPLETE!",
}

COLORS = [
    {"bg": "#ffc0cb", "fg": "#a0004a", "accent": "#ff80a0"},  # pink (default)
    {"bg": "#b5eaff", "fg": "#003d6b", "accent": "#0088cc"},  # blue
    {"bg": "#d4f5c4", "fg": "#1a5e00", "accent": "#44bb22"},  # green
    {"bg": "#ffe4b5", "fg": "#7a3b00", "accent": "#ff9922"},  # peach
    {"bg": "#e8d5ff", "fg": "#4b0082", "accent": "#9933ff"},  # lavender
]

DATA_FILE  = "data/kirby_stats.json"
COLOR_FILE = "data/kirby_widget_color.json"


class KirbyWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kirby")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        self.color_index   = self._load_color()
        self.colors        = COLORS[self.color_index]
        self.face_index    = 0
        self.bounce_dir    = 1
        self.bounce_offset = 0
        self.last_percent  = -1
        self.session_start = time.time()

        self._build_ui()
        self._bind_events()
        self._tick_face()
        self._tick_bounce()
        self.update_widget()

    # ── UI BUILD ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        c = self.colors
        self.root.config(bg=c["bg"])
        self.root.geometry("140x115+100+100")

        # Drag bar (top stripe)
        self.topbar = tk.Frame(self.root, bg=c["accent"], height=14, cursor="fleur")
        self.topbar.pack(fill="x")

        self.color_btn = tk.Label(self.topbar, text="●", bg=c["accent"], fg=c["bg"],
                                   font=("Courier", 8, "bold"), cursor="hand2")
        self.color_btn.pack(side="left", padx=3)
        self.color_btn.bind("<Button-1>", lambda e: self.cycle_color())

        self.close_btn = tk.Label(self.topbar, text="✕", bg=c["accent"], fg=c["bg"],
                                   font=("Courier", 8, "bold"), cursor="hand2")
        self.close_btn.pack(side="right", padx=3)
        self.close_btn.bind("<Button-1>", lambda e: self.root.destroy())

        # Kirby face
        self.face_label = tk.Label(self.root, text=FACES["idle"][0],
                                    bg=c["bg"], fg=c["fg"],
                                    font=("Courier", 13, "bold"))
        self.face_label.pack(pady=(4, 0))

        # Progress bar
        self.bar_canvas = tk.Canvas(self.root, width=120, height=10,
                                     bg=c["bg"], highlightthickness=0)
        self.bar_canvas.pack(pady=2)
        self.bar_bg   = self.bar_canvas.create_rectangle(2, 2, 118, 9,
                                                          fill=c["accent"] + "44", outline="")
        self.bar_fill = self.bar_canvas.create_rectangle(2, 2, 2, 9,
                                                          fill=c["accent"], outline="")

        # Percent + milestone message
        self.stat_label = tk.Label(self.root, text="0% · let's gooo!",
                                    bg=c["bg"], fg=c["fg"],
                                    font=("Courier", 8, "bold"))
        self.stat_label.pack()

        # Session timer
        self.time_label = tk.Label(self.root, text="⏱ 0m",
                                    bg=c["bg"], fg=c["fg"],
                                    font=("Courier", 8))
        self.time_label.pack(pady=(0, 4))

    # ── EVENTS ──────────────────────────────────────────────────────────────────

    def _bind_events(self):
        self.topbar.bind("<Button-1>",  self._start_move)
        self.topbar.bind("<B1-Motion>", self._do_move)
        self.root.bind("<Button-3>",    self._show_menu)
        self.face_label.bind("<Double-Button-1>", lambda e: self._celebrate())

    def _start_move(self, e):
        self.root._x, self.root._y = e.x, e.y

    def _do_move(self, e):
        self.root.geometry(f"+{e.x_root - self.root._x}+{e.y_root - self.root._y}")

    def _show_menu(self, e):
        c = self.colors
        menu = tk.Menu(self.root, tearoff=0,
                       bg=c["bg"], fg=c["fg"],
                       activebackground=c["accent"], activeforeground=c["bg"],
                       font=("Courier", 9))
        menu.add_command(label="🎨 Change Color",  command=self.cycle_color)
        menu.add_command(label="🎉 Celebrate!",    command=self._celebrate)
        menu.add_command(label="📊 Stats",         command=self._show_stats_popup)
        menu.add_separator()
        menu.add_command(label="✕ Close",          command=self.root.destroy)
        menu.tk_popup(e.x_root, e.y_root)

    # ── ANIMATIONS ──────────────────────────────────────────────────────────────

    def _tick_face(self):
        """Rotate faces based on current mood every 2.5s."""
        try:
            data    = self._load_data()
            percent = self._calc_percent(data)
            mood    = self._get_mood(percent, data)
            faces   = FACES[mood]
            self.face_index = (self.face_index + 1) % len(faces)
            self.face_label.config(text=faces[self.face_index])
        except tk.TclError:
            return
        self.root.after(2500, self._tick_face)

    def _tick_bounce(self):
        """Subtle vertical bounce on the face label."""
        try:
            self.bounce_offset += self.bounce_dir
            if abs(self.bounce_offset) >= 3:
                self.bounce_dir *= -1
            self.face_label.pack_configure(pady=(4 + self.bounce_offset, 0))
        except tk.TclError:
            return
        self.root.after(110, self._tick_bounce)

    def _celebrate(self, flashes=8):
        """Flash colors rapidly to celebrate a milestone."""
        def _flash(n=0):
            try:
                if n >= flashes:
                    self._apply_colors()
                    return
                c = random.choice(COLORS)
                self.root.config(bg=c["bg"])
                self.face_label.config(bg=c["bg"], fg=c["fg"],
                                        text=random.choice(FACES["done"]))
                self.stat_label.config(bg=c["bg"], fg=c["fg"], text="★ POYO!! ★")
                self.bar_canvas.config(bg=c["bg"])
            except tk.TclError:
                return
            self.root.after(110, lambda: _flash(n + 1))
        _flash()

    # ── DATA ────────────────────────────────────────────────────────────────────

    def _load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {}

    def _calc_percent(self, data):
        done  = data.get("done_today", 0)
        total = len(data.get("tasks", []))
        return int((done / total) * 100) if total > 0 else 0

    def _get_mood(self, percent, data):
        if percent == 100:
            return "done"
        if percent >= 50:
            return "working"
        elapsed = time.time() - self.session_start
        if elapsed > 3600:
            return "sleepy"
        if data.get("done_today", 0) == 0 and elapsed > 600:
            return "hungry"
        return "idle"

    def _get_rank(self, dist):
        for threshold, name in [(5000, "🌌 Galactic Overlord"), (2500, "⭐ Star Pilot"),
                                  (1000, "🚀 Orbit Master"),     (500,  "☄️  Comet Rider"),
                                  (100,  "🌙 Moon Walker"),      (0,    "🛸 Space Cadet")]:
            if dist >= threshold:
                return name
        return "🛸 Space Cadet"

    def _load_color(self):
        try:
            if os.path.exists(COLOR_FILE):
                with open(COLOR_FILE, "r") as f:
                    return json.load(f).get("index", 0) % len(COLORS)
        except Exception:
            pass
        return 0

    def _save_color(self):
        os.makedirs("data", exist_ok=True)
        with open(COLOR_FILE, "w") as f:
            json.dump({"index": self.color_index}, f)

    # ── COLORS ──────────────────────────────────────────────────────────────────

    def cycle_color(self):
        self.color_index = (self.color_index + 1) % len(COLORS)
        self.colors = COLORS[self.color_index]
        self._apply_colors()
        self._save_color()

    def _apply_colors(self):
        c = self.colors
        self.root.config(bg=c["bg"])
        self.topbar.config(bg=c["accent"])
        self.close_btn.config(bg=c["accent"], fg=c["bg"])
        self.color_btn.config(bg=c["accent"], fg=c["bg"])
        self.face_label.config(bg=c["bg"], fg=c["fg"])
        self.stat_label.config(bg=c["bg"], fg=c["fg"])
        self.time_label.config(bg=c["bg"], fg=c["fg"])
        self.bar_canvas.config(bg=c["bg"])
        self.bar_canvas.itemconfig(self.bar_bg,   fill=c["accent"] + "44")
        self.bar_canvas.itemconfig(self.bar_fill, fill=c["accent"])

    # ── STATS POPUP ─────────────────────────────────────────────────────────────

    def _show_stats_popup(self):
        data   = self._load_data()
        done   = data.get("done_today", 0)
        total  = len(data.get("tasks", []))
        dist   = data.get("distance_m", 0)
        streak = data.get("streak", 0)
        rank   = self._get_rank(dist)

        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.config(bg=self.colors["bg"])
        popup.geometry(f"+{self.root.winfo_x() + 150}+{self.root.winfo_y()}")

        for line in [
            "── KIRBY STATS ──",
            f"Tasks:   {done}/{total}",
            f"Dist:    {dist}m",
            f"Streak:  {streak} days 🔥",
            f"Rank:    {rank}",
            "",
            "[ close ]",
        ]:
            lbl = tk.Label(popup, text=line, bg=self.colors["bg"], fg=self.colors["fg"],
                            font=("Courier", 9, "bold"), anchor="w")
            lbl.pack(padx=10, pady=1, anchor="w")
            if line == "[ close ]":
                lbl.config(fg=self.colors["accent"], cursor="hand2")
                lbl.bind("<Button-1>", lambda e: popup.destroy())

        popup.after(6000, lambda: popup.destroy() if popup.winfo_exists() else None)

    # ── MAIN UPDATE LOOP ────────────────────────────────────────────────────────

    def update_widget(self):
        try:
            data    = self._load_data()
            percent = self._calc_percent(data)

            # Trigger celebration on milestone hits
            if percent != self.last_percent and percent in MILESTONE_MSGS:
                self._celebrate()
            self.last_percent = percent

            # Pick the right milestone message
            msg = MILESTONE_MSGS.get(
                max((k for k in MILESTONE_MSGS if k <= percent), default=0),
                "keep going!"
            )
            self.stat_label.config(text=f"{percent}% · {msg}")

            # Update progress bar
            w = int(116 * percent / 100)
            self.bar_canvas.coords(self.bar_fill, 2, 2, 2 + w, 9)

            # Session timer
            elapsed_m = int((time.time() - self.session_start) / 60)
            self.time_label.config(text=f"⏱ {elapsed_m}m")

        except Exception:
            try:
                self.stat_label.config(text="0% · let's gooo!")
                self.bar_canvas.coords(self.bar_fill, 2, 2, 2, 9)
            except tk.TclError:
                return

        self.root.after(5000, self.update_widget)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    KirbyWidget().run()