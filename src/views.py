import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.controllers import Controller

SCALE = 3
BOX_SIZE = 10 * SCALE
WIDTH = 10 * BOX_SIZE
HEIGHT = 20 * BOX_SIZE


class BaseView(tk.Frame):
    def __init__(self, parent: tk.Tk, controller: "Controller"):
        super().__init__(parent)
        self.controller = controller


class LoggerView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.label = tk.Label(self, text="Logger UI", font=("Arial", 24))
        self.label.pack(pady=BOX_SIZE // 2)

        self.view_settings_btn = tk.Button(
            self, text="View Settings", command=self.controller.show_settings_view
        )
        self.view_settings_btn.pack()

        self.start_log_pulse_btn = tk.Button(
            self, text="Start Log Pulse", command=self.controller.start_scheduler
        )
        self.start_log_pulse_btn.pack()


class SettingsView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        # TITLE
        self.label = tk.Label(self, text="Settings UI", font=("Arial", 24))
        self.label.pack(pady=20)

        self._build_log_options_frame()
        self._build_log_interval_frame()

        # NAVIGATE TO LOGGER
        self.button = tk.Button(
            self, text="Save & Run", command=self.controller.restart_scheduler()
        )
        self.button.pack(pady=BOX_SIZE)

    def _build_log_options_frame(self):
        """Creates the log file selection UI"""
        self.log_option_frame = tk.Frame(self)

        # dropdown
        self.log_options_var = tk.StringVar()
        self.log_options = ttk.Combobox(
            self.log_option_frame,
            textvariable=self.log_options_var,
            state="readonly",
        )
        self.log_options.pack(side="left", padx=5)

        # refresh button (small, next to dropdown)
        self.refresh_options_btn = tk.Button(
            self.log_option_frame,
            text="Refresh",
            command=self.controller.refresh_file_list,
        )
        self.refresh_options_btn.pack(side="left", padx=5)

        # refresh button (small, next to dropdown)
        self.add_new_log_file_btn = tk.Button(
            self.log_option_frame,
            text="New",
            command=self.controller.show_new_log_file_view,
        )
        self.add_new_log_file_btn.pack(side="left", padx=5)

        self.log_option_frame.pack(pady=10)

    def _build_log_interval_frame(self):
        """Creates the log interval setting UI"""

        self.log_interval_frame = tk.Frame(self)

        config = self.controller.load_config()

        # Label
        self.log_interval_label = tk.Label(
            self.log_interval_frame, text="Log Interval (mins):"
        )
        self.log_interval_label.pack(side="left", padx=5)

        # Entry field
        self.log_interval_var = tk.IntVar(value=config.get("log_interval_mins", 10))
        self.log_interval_entry = tk.Entry(
            self.log_interval_frame, textvariable=self.log_interval_var, width=8
        )
        self.log_interval_entry.pack(side="left", padx=5)

        self.log_interval_frame.pack(pady=10)


class NewLogFileView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        # TITLE
        self.label = tk.Label(self, text="New Logfile", font=("Arial", 24))
        self.label.pack(pady=20)

        # TEXT FIELD: new_log_file_name
        self.new_log_file_name_var = tk.StringVar()
        self.entry_label = tk.Label(self, text="Log File Name:")
        self.entry_label.pack(pady=(10, 0))
        self.new_log_file_name = tk.Entry(self, textvariable=self.new_log_file_name_var)
        self.new_log_file_name.pack(pady=10, padx=20)
        self.note_label = tk.Label(
            self, text="Note: You can press Enter to create log file"
        )
        self.note_label.pack()

        self.new_log_file_name.bind(
            "<Return>", lambda e: self.controller.create_log_file()
        )

        # CREATE + CANCEL FRAME
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        # CREATE BUTTON
        self.create_button = tk.Button(
            button_frame, text="Create", command=self.controller.create_log_file
        )
        self.create_button.pack(side=tk.LEFT, padx=10)

        # CANCEL BUTTON
        self.cancel_button = tk.Button(
            button_frame, text="Cancel", command=self.controller.show_settings_view
        )
        self.cancel_button.pack(side=tk.LEFT, padx=10)
