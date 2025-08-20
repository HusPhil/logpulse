import tkinter as tk

from src.controllers import Controller
from src.models import ConfigModel

try:
    import ctypes

    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Log Tracker")

    app_model = ConfigModel()
    app_controller = Controller(model=app_model)

    app_controller.setup_views(root)

    root.mainloop()
