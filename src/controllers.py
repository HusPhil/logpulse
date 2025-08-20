import tkinter as tk
from tkinter import messagebox
from src.views import BaseView, LoggerView, SettingsView


class Controller:

    def __init__(self, model):
        self.model = model
        self.root: tk.Tk = None

        self.views = {}
        self.current_view: BaseView = None

    def setup_views(self, root):
        self.root = root

        self.views["logger"] = LoggerView(root, self)
        self.views["settings"] = SettingsView(root, self)

        self.show_logger_view()

    def handle_close_request(self):
        """
        Handles the WM_DELETE_WINDOW protocol.
        Prevents closing if the LoggerView is active.
        """
        if isinstance(self.current_view, LoggerView):
            messagebox.showinfo(
                "Cannot Close",
                "You cannot close the application from the Logger View. Please navigate to Settings to close.",
            )
        else:
            # Allow closing for all other views
            self.root.destroy()

    def show_logger_view(self):
        self._hide_current_view()
        self.current_view = self.views["logger"]
        self.current_view.pack(expand=True, fill="both")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

    def show_settings_view(self):
        self._hide_current_view()
        self.current_view = self.views["settings"]
        self.current_view.pack(expand=True, fill="both")
        

    def _hide_current_view(self):
        """A helper method to hide the currently visible view."""
        if self.current_view:
            self.root.overrideredirect(False)
            self.root.attributes("-topmost", False)
            self.current_view.pack_forget()

    
