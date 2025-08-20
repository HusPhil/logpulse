import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.controllers import Controller


class BaseView(tk.Frame):
    def __init__(self, parent: tk.Tk, controller: "Controller"):
        super().__init__(parent)
        self.controller = controller


class LoggerView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.label = tk.Label(self, text="Logger UI", font=("Arial", 24))
        self.label.pack(pady=20)

        self.button = tk.Button(
            self, text="Change Message", command=self.controller.show_settings_view
        )
        self.button.pack(pady=50, padx=100)


class SettingsView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        self.label = tk.Label(self, text="Settings UI", font=("Arial", 24))
        self.label.pack(pady=20)

        self.button = tk.Button(
            self, text="Change Message", command=self.controller.show_logger_view
        )
        self.button.pack(pady=50, padx=100)
