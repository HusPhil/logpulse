import tkinter as tk


class BaseView(tk.Frame):
    """Base class for all views in the application."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


class LoggerView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)


class ConfigView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
