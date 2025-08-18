# src/tray.py
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image
from gui import show_popup
import sys
import os


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def run_tray(root):
    icon = Icon("LogTracker")
    icon.icon = Image.open(resource_path("app.ico"))
    icon.title = "Log Tracker"
    icon.menu = Menu(
        MenuItem("Log now", lambda icon, item: root.after(0, show_popup, root)),
        MenuItem("Exit", lambda icon, item: icon.stop()),
    )
    icon.run()
