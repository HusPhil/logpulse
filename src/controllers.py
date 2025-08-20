from math import exp
from src.views import BaseView, LoggerView, SettingsView


class Controller:

    def __init__(self, model):
        self.model = model
        self.root = None

        self.views = {}
        self.current_view: BaseView = None

    def setup_views(self, root):
        self.root = root

        self.views["logger"] = LoggerView(root, self)
        self.views["settings"] = SettingsView(root, self)

        self.show_logger_view()

    def show_logger_view(self):
        self._hide_current_view()
        self.current_view = self.views["logger"]
        self.current_view.pack(expand=True, fill="both")

    def show_settings_view(self):
        self._hide_current_view()
        self.current_view = self.views["settings"]
        self.current_view.pack(expand=True, fill="both")

    def _hide_current_view(self):
        """A helper method to hide the currently visible view."""
        if self.current_view:
            self.current_view.pack_forget()
