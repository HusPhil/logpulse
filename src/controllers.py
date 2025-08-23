import tkinter as tk
from tkinter import messagebox
from src.views import BaseView, LoggerView, SettingsView


class Controller:

    def __init__(self, model):
        self.model = model
        self.root: tk.Tk = None
        self._after_id = None

        self.views = {}
        self.current_view: BaseView = None

    def setup_views(self, root):
        self.root = root

        self.views["logger"] = LoggerView(root, self)
        self.views["settings"] = SettingsView(root, self)

        self.show_settings_view()

    def handle_close_request(self):
        """
        Handles the WM_DELETE_WINDOW protocol.
        Prevents closing if the LoggerView is active.
        """
        self.root.withdraw()

    def show_logger_view(self):
        self._hide_current_view()
        self.root.deiconify()
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

    def _run_scheduled_task(self):
        """The function that gets called repeatedly."""
        print("Running scheduled task...")
        # Show the scheduled view
        if self.current_view != self.views["logger"]:
            self.show_logger_view()
        # Schedule the next run. This is what creates the loop.
        # Here, it's set to 5 seconds (5000 milliseconds).
        self._after_id = self.root.after(5000, self._run_scheduled_task)

    def start_scheduler(self):
        """Starts the recurring task."""
        if not self._after_id:
            # Show the scheduled view immediately and start the loop
            self.show_logger_view()
            self._after_id = self.root.after(5000, self._run_scheduled_task)
            # Disable the start button and enable the stop button
            # self.views["main"].start_button.config(state=tk.DISABLED)
            # self.views["main"].stop_button.config(state=tk.NORMAL)
            print("Scheduler started.")

    def stop_scheduler(self):
        """Stops the recurring task."""
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None
            # Re-enable the start button and disable the stop button
            # self.views["main"].start_button.config(state=tk.NORMAL)
            # self.views["main"].stop_button.config(state=tk.DISABLED)
            print("Scheduler stopped.")
