import os
import json
import tkinter as tk
from tkinter import messagebox
from src.views import BaseView, LoggerView, NewLogFileView, SettingsView
from .utils import get_files_in_dir


BASE_LOG_FILE_DIR = "logs"
CONFIG_FILE = "config.json"
DEFAULT_LOG_INTERVAL_MINS = 1
DEFAULT_LOG_FILE_NAME = "logs.md"


class Controller:

    def __init__(self, model):
        self.model = model
        self.root: tk.Tk = None
        self._after_id = None
        self._is_scheduler_running = False

        self.views = {}
        self.current_view: BaseView = None

        self.log_interval_mins = DEFAULT_LOG_INTERVAL_MINS

    def setup_views(self, root):
        self.root = root

        self.views["logger"] = LoggerView(root, self)
        self.views["settings"] = SettingsView(root, self)
        self.views["new_log_file"] = NewLogFileView(root, self)

        self.show_settings_view()

    def handle_close_request(self):
        """
        Handles the WM_DELETE_WINDOW protocol.
        Prevents closing if the LoggerView is active.
        """

        self.root.withdraw()

    def show_logger_view(self):
        self._hide_current_view()
        self.stop_scheduler()
        self.root.deiconify()
        self.current_view = self.views["logger"]
        self.current_view.pack(expand=True, fill="both")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

    def show_settings_view(self):
        self._hide_current_view()
        self.refresh_file_list()
        self.current_view = self.views["settings"]
        self.current_view.pack(expand=True, fill="both")

    def show_new_log_file_view(self):
        self._hide_current_view()
        self.current_view = self.views["new_log_file"]
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
        if not self._is_scheduler_running:
            print("Scheduler not running...")

            return

        self.show_logger_view()
        # Schedule the next run. This is what creates the loop.
        self._after_id = self.root.after(
            int(self.log_interval_mins * 60 * 1000), self._run_scheduled_task
        )

    def start_scheduler(self):
        """Starts the recurring task."""
        if self._is_scheduler_running:
            return

        self._is_scheduler_running = True
        self._after_id = self.root.after(
            self.log_interval_mins * 60 * 1000, self._run_scheduled_task
        )
        print("Scheduler started.")

    def stop_scheduler(self):
        """Stops the recurring task."""
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None
            print("Scheduler stopped.")

        self._is_scheduler_running = False

    def restart_scheduler(self):
        self.stop_scheduler()
        self.start_scheduler()

    def select_current_log_file(self, filename):
        settings_view: SettingsView = self.views["settings"]
        settings_view.log_options.set(filename)

    def refresh_file_list(self):
        try:
            file_options = get_files_in_dir(BASE_LOG_FILE_DIR, [".md"])
            settings_view: SettingsView = self.views["settings"]
            if file_options:
                settings_view.log_options["values"] = file_options
                selected_option = settings_view.log_options_var.get()
                self.select_current_log_file(
                    selected_option
                    if selected_option in file_options
                    else file_options[0]
                )
            else:
                settings_view.log_options["values"] = []
                self.create_log_file(DEFAULT_LOG_FILE_NAME, notify_user=False)
                settings_view.log_options.set(DEFAULT_LOG_FILE_NAME)

        except Exception as e:
            # If you're running as .pyw (no console), show errors visibly
            messagebox.showerror("Error", f"Failed to read files:\n{e}")

    def create_log_file(self, custom_filename: str = None, notify_user: bool = True):

        new_log_file: NewLogFileView = self.views["new_log_file"]
        filename = custom_filename
        if not custom_filename:
            filename = new_log_file.new_log_file_name_var.get().strip()
        if filename:
            # For now just print, but here’s where you’d call your util
            try:
                if not filename.endswith(".md"):
                    filename += ".md"

                if not os.path.exists(BASE_LOG_FILE_DIR):
                    os.makedirs(BASE_LOG_FILE_DIR)

                filepath = os.path.join(BASE_LOG_FILE_DIR, filename)

                with open(filepath, "x") as f:
                    f.write("")

                if notify_user:
                    messagebox.showinfo("Success", f"{filename} created.")

                self.refresh_file_list()

                settings_view: SettingsView = self.views["settings"]
                settings_view.log_options.set(filename)

                self.show_settings_view()

            except FileExistsError:
                messagebox.showerror("Error", f"{filename} already exists.")
        else:
            print("Please enter a file name.")

    def set_log_interval(self, interval_mins: int):
        """
        Set the log interval in minutes. Must be a positive integer.
        Raises ValueError if input is invalid.
        """

        # Validate
        if not isinstance(interval_mins, int):
            raise ValueError("Log interval must be an integer (minutes).")
        if interval_mins <= 0:
            raise ValueError("Log interval must be greater than 0 minutes.")

        # Load, update, and save config
        config = self.load_config()
        config["log_interval_mins"] = interval_mins
        self.save_config(config)

    def settings_save_and_run(self):
        settings_view: SettingsView = self.views["settings"]
        log_interval_mins = settings_view.log_interval_var.get()
        self.log_interval_mins = log_interval_mins
        self.set_log_interval(log_interval_mins)
        messagebox.showinfo(
            "Success",
            f"You will be promted to log every {log_interval_mins} minute(s)",
        )
        self.restart_scheduler()
        self.root.withdraw()

    def load_config(self):
        """Load config.json or return defaults if not found"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return {"log_interval_mins": DEFAULT_LOG_INTERVAL_MINS}

    def save_config(self, config):
        """Save config to config.json"""
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
