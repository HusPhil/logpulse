# src/gui.py
import tkinter as tk
import threading
import winsound
from logger import append_log

popup_lock = threading.Lock()
current_dialog = None
current_text_box = None


def show_popup(root):
    global current_dialog, current_text_box
    if current_dialog and current_dialog.winfo_exists():
        current_dialog.lift()
        current_dialog.attributes("-topmost", True)
        current_text_box.focus_force()
        return

    if not popup_lock.acquire(blocking=False):
        return

    def cleanup():
        global current_dialog, current_text_box
        if popup_lock.locked():
            popup_lock.release()
        if current_dialog.winfo_exists():
            current_dialog.destroy()
        current_dialog = None
        current_text_box = None

    dialog = tk.Toplevel(root)
    dialog.overrideredirect(True)
    dialog.geometry("400x250+500+300")
    dialog.attributes("-topmost", True)
    dialog.grab_set()

    label = tk.Label(dialog, text="What did you do? (Shift+Enter=new line, Enter=save)")
    label.pack(pady=5)

    text_box = tk.Text(dialog, wrap="word", height=10, width=50)
    text_box.pack(padx=10, pady=10, expand=True, fill="both")

    def on_enter(event=None):
        lines = text_box.get("1.0", tk.END).strip().split("\n")
        if lines:
            append_log(lines)
        cleanup()

    def on_shift_enter(event=None):
        text_box.insert(tk.INSERT, "\n")
        return "break"

    text_box.bind("<Return>", on_enter)
    text_box.bind("<Shift-Return>", on_shift_enter)

    current_dialog = dialog
    current_text_box = text_box
    dialog.after(100, lambda: text_box.focus_force())
    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
