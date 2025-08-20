import os
from PIL import Image
import tkinter as tk
import threading
from pystray import Icon as TrayIcon, Menu as TrayMenu, MenuItem as TrayMenuItem
from src.controllers import Controller
from src.models import ConfigModel

try:
    import ctypes

    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def on_exit(icon, item):
    icon.stop()  # Stop the system tray icon
    root.quit()  # Stop Tkinter loop
    os._exit(0)

def run_tray():
    icon = TrayIcon("LogTracker")
    icon_path = "app.ico"
    icon.icon = Image.open(icon_path)
    icon.title = "Log Tracker"
    icon.menu = TrayMenu(
        TrayMenuItem("Log now", None),
        TrayMenuItem("Config", None),
        TrayMenuItem("Pause/Resume", None),  # <-- Added button
        TrayMenuItem("Exit", on_exit),
    )
    icon.run()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    root.title("Log Tracker")

    app_model = ConfigModel()
    app_controller = Controller(model=app_model)

    app_controller.setup_views(root)

    root.protocol("WM_DELETE_WINDOW", app_controller.handle_close_request)
    threading.Thread(target=run_tray, daemon=True).start()

    root.mainloop()
