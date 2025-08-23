import os
from PIL import Image
import tkinter as tk
from tkinter import ttk
import threading
from pystray import Icon as TrayIcon, Menu as TrayMenu, MenuItem as TrayMenuItem
from src.controllers import Controller
from src.models import ConfigModel
from .views import HEIGHT, WIDTH


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


def center_window(root: tk.Tk):
    """
    Centers the Tkinter window on the screen.

    Args:
        root (tk.Tk): The main Tkinter window instance.
    """
    root.update_idletasks()  # Ensures the window's geometry is up-to-date

    # Get the screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get the window's dimensions after it's been drawn
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Calculate the x and y coordinates for the center
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the new geometry to position the window
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Log Tracker")

    style = ttk.Style()
    style.theme_use("default")

    # Remove blue focus highlight
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", "white")],  # normal background
        selectbackground=[("!disabled", "white")],  # text select background
        selectforeground=[("!disabled", "black")],  # text select foreground
    )

    root.geometry(f"{HEIGHT}x{WIDTH}")

    app_model = ConfigModel()
    app_controller = Controller(model=app_model)

    app_controller.setup_views(root)

    root.protocol("WM_DELETE_WINDOW", app_controller.handle_close_request)
    threading.Thread(target=run_tray, daemon=True).start()

    center_window(root)
    root.mainloop()
