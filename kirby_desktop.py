import tkinter as tk
import json, os

def update_widget():
    try:
        if os.path.exists('data/kirby_stats.json'):
            with open('data/kirby_stats.json', 'r') as f:
                data = json.load(f)
                done = data.get('done_today', 0)
                total = len(data.get('tasks', []))
                percent = int((done / total) * 100) if total > 0 else 0
                label.config(text=f"(っ^‿^)っ\n{percent}% POYO!")
        else:
            label.config(text="(っ^‿^)っ\n0% POYO!")
    except Exception:
        try:
            label.config(text="(っ^‿^)っ\n?% POYO!")
        except tk.TclError:
            return

    root.after(5000, update_widget)

root = tk.Tk()
root.title("Kirby")
root.overrideredirect(True)
root.geometry("120x80+100+100")
root.attributes("-topmost", True)
root.config(bg='#ffc0cb')

label = tk.Label(root, text="(っ^‿^)っ\n0% POYO!", bg='#ffc0cb', font=("Courier", 12, "bold"))
label.pack(expand=True)

def start_move(event): root.x, root.y = event.x, event.y
def do_move(event): root.geometry(f"+{event.x_root - root.x}+{event.y_root - root.y}")
root.bind("<Button-1>", start_move)
root.bind("<B1-Motion>", do_move)

update_widget()
root.mainloop()
