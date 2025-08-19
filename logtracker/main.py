import tkinter as tk
from datetime import datetime
import pystray
import winsound
from PIL import Image
import os
import sys
import threading

base_path = "logs"

# Ensure base directory exists
if not os.path.exists(base_path):
    os.makedirs(base_path)

log_file = base_path + "/log.md"

# --- defaults ---
interval = 60 * 1
log_title_format = "# %Y-%m-%d"  # default = date
popup_lock = threading.Lock()
current_dialog = None
current_text_box = None
stop_event = threading.Event()

def ensure_date_header():
    """Ensure today's header exists in log file (based on log_title_format)."""
    today = datetime.now().strftime(log_title_format)
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(today + "\n\n")
    else:
        with open(log_file, "r+", encoding="utf-8") as f:
            content = f.read()
            if today not in content:
                f.write("\n" + today + "\n\n")

def show_popup():
    global current_dialog, current_text_box
    if stop_event.is_set():
        return
    if current_dialog and current_dialog.winfo_exists():
        current_dialog.lift()
        current_dialog.attributes("-topmost", True)
        current_text_box.focus_force()
        return
    if not popup_lock.acquire(blocking=False):
        return

    def on_enter(event=None):
        text = current_text_box.get("1.0", tk.END).strip()
        if text:
            ensure_date_header()
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            md_text = "\n".join(f"- {line}" for line in lines)
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"**{datetime.now():%I:%M %p}**\n{md_text}\n\n")
            cleanup()
        else:
            dialog.bell()
        return "break"

    def on_shift_enter(event=None):
        current_text_box.insert(tk.INSERT, "\n")
        return "break"

    def force_focus():
        if dialog.winfo_exists():
            dialog.lift()
            dialog.attributes("-topmost", True)
            current_text_box.focus_force()
            dialog.after(500, force_focus)

    def cleanup():
        global current_dialog, current_text_box
        if popup_lock.locked():
            popup_lock.release()
        if dialog.winfo_exists():
            dialog.destroy()
        current_dialog = None
        current_text_box = None
        if not stop_event.is_set():
            root.after(interval * 1000, schedule_popup)

    dialog = tk.Toplevel(root)
    dialog.overrideredirect(True)
    dialog.geometry("400x250+500+300")
    dialog.attributes("-topmost", True)
    dialog.grab_set()

    label = tk.Label(dialog, text="What did you do? (Shift+Enter=new line, Enter=save)")
    label.pack(pady=5)

    text_box = tk.Text(dialog, wrap="word", height=10, width=50)
    text_box.pack(padx=10, pady=10, expand=True, fill="both")
    text_box.bind("<Return>", on_enter)
    text_box.bind("<Shift-Return>", on_shift_enter)

    current_dialog = dialog
    current_text_box = text_box
    dialog.after(100, lambda: text_box.focus_force())
    dialog.after(500, force_focus)
    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)

def schedule_popup():
    if not stop_event.is_set():
        show_popup()

def open_config():
    """Open a configuration dialog for interval and log title."""
    config_win = tk.Toplevel(root)
    config_win.title("Configuration")
    config_win.geometry("300x300")
    config_win.attributes("-topmost", True)

    # Interval
    tk.Label(config_win, text="Interval (minutes):").pack(pady=5)
    interval_var = tk.StringVar(value=str(int(interval / 60)))
    tk.Entry(config_win, textvariable=interval_var).pack(pady=5)

    # Log title
    tk.Label(config_win, text="Log title:").pack(pady=5)
    # Only use the filename, not full path
    current_filename = os.path.basename(log_file)
    log_title_var = tk.StringVar(value=current_filename)
    tk.Entry(config_win, textvariable=log_title_var).pack(pady=5)

    # Log title format
    tk.Label(config_win, text="Log title format:").pack(pady=5)
    tk.Label(config_win, text="(uses datetime format, e.g. '# %Y-%m-%d')").pack()
    title_var = tk.StringVar(value=log_title_format)
    tk.Entry(config_win, textvariable=title_var).pack(pady=5, fill="x")

    def save_config():
        global interval, log_title_format, log_file
        try:
            interval_val = int(interval_var.get())
            title_input = log_title_var.get().strip()
            # Remove any existing .md to avoid double extension
            if title_input.lower().endswith(".md"):
                title_input = title_input[:-3]
            # Join properly with base_path and add .md
            log_file = os.path.join(base_path, title_input + ".md")
            if interval_val < 1:
                raise ValueError
            interval = interval_val * 60
        except ValueError:
            tk.messagebox.showerror("Error", "Interval must be a positive integer.")
            return
        log_title_format = title_var.get().strip()
        config_win.destroy()

    tk.Button(config_win, text="Save", command=save_config).pack(pady=10)

def on_exit(icon, item):
    stop_event.set()  # Stop any scheduled popups
    icon.stop()  # Stop the system tray icon
    root.quit()  # Stop Tkinter loop
    os._exit(0)

def on_log_now(icon, item):
    root.after(0, show_popup)

def on_config(icon, item):
    root.after(0, open_config)

def resource_path(relative_path):
    """Get absolute path to resource, works for dev, PyInstaller, and shiv"""
    # Check if running from PyInstaller
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    
    # Check if we're in a shiv environment
    if "__shiv_python__" in os.environ:
        # Get the directory where the pyz is located
        pyz_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        return os.path.join(pyz_dir, relative_path)
    
    return os.path.join(os.path.abspath("."), relative_path)

def run_tray():
    icon = pystray.Icon("LogTracker")
    icon_path = resource_path("app.ico")
    icon.icon = Image.open(icon_path)
    icon.title = "Log Tracker"
    icon.menu = pystray.Menu(
        pystray.MenuItem("Log now", on_log_now),
        pystray.MenuItem("Config", on_config),
        pystray.MenuItem("Exit", on_exit),
    )
    icon.run()

# --- main ---
root = tk.Tk()
root.withdraw()

def main():
    """Main entry point for the application."""
    threading.Thread(target=run_tray, daemon=True).start()
    root.after(interval * 1000, schedule_popup)
    root.mainloop()

if __name__ == "__main__":
    main()